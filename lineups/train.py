"""Rolling-origin fitting of the event model.

For an origin (outer quarter) the protocol is:

1. **Inner fit**: train on the five-year prefix before the previous completed
   quarter. After every epoch, score that quarter (inputs frozen at its
   start). Select the epoch with the lowest validation objective; patience 8,
   minimum improvement 1e-5, cap 96.
2. **Final fit**: start again from the same initialization on the five-year
   prefix before the outer quarter, and train exactly the selected number of
   epochs. Keep the last five epochs' weights.
3. **Forecast** the outer quarter with inputs frozen at its start: the final
   weights ("direct") and the mixture of the last five checkpoints.

Training rows are game x offense five x defense five aggregates with event
counts. Each row has weight 2^(-age/730 days). The objective averages four
event-family likelihoods (action counts, shot location, conversion,
offensive-rebound recovery), each divided by a shared untrained reference
level, plus 0.25 x the possession-weighted squared error of points/100,
pooled by game and offense five.
"""
import copy
import math
import time
from dataclasses import dataclass

import numpy as np
import torch
from torch.nn import functional as F

from lineups.model import average_ledgers

FAMILIES = ("counts", "location", "conversion", "recovery")
LABELS = ("possessions", "points", "fga", "fta", "turnover", "loc_attempt", "loc_make", "rebound",
          "fga_observed", "fta_observed", "location_observed")


@dataclass(frozen=True)
class FitConfig:
    lr: float = 1e-3
    weight_decay: float = 1e-4
    clip: float = 5.
    max_epochs: int = 96
    patience: int = 8
    min_delta: float = 1e-5
    point_weight: float = .25
    half_life_days: float = 730.
    lookback_days: int = 5 * 365
    batch_rows: int = 4096
    checkpoints: int = 5
    pair_lr_scale: float = 1.     # PairInteractions only (model.parameter_groups)
    pair_decay: float = 0.


# ---- losses ----------------------------------------------------------------
def event_statistics(pred, labels, weight):
    """Summed negative log likelihoods and exposures for the four event families."""
    n = labels["possessions"].double()
    w = weight.double()
    count = n.new_zeros(())
    count_den = count.clone()
    for name, mask in (("fga", "fga_observed"), ("fta", "fta_observed"), ("turnover", None)):
        valid = torch.ones_like(n) if mask is None else labels[mask].double()
        mu = (getattr(pred, name).double() * n[:, None]).clamp(min=1e-8)
        y = labels[name].double()
        count = count + ((mu - y * mu.log() + torch.lgamma(y + 1)).sum(1) * w * valid).sum()
        count_den = count_den + (n * w * valid).sum()
    observed = w[:, None, None] * (labels["fga_observed"] & labels["location_observed"])[:, None, None]
    attempts, makes = labels["loc_attempt"].double(), labels["loc_make"].double()
    exposure = (attempts * observed).sum()
    location = -(attempts * pred.location.double().clamp(min=1e-8).log() * observed).sum()
    conversion = (F.binary_cross_entropy(pred.make.double(), makes / attempts.clamp(min=1), weight=attempts,
                                         reduction="none") * observed).sum()
    recoveries = labels["rebound"].double()
    return dict(counts=(count, count_den), location=(location, exposure), conversion=(conversion, exposure),
                recovery=(-(recoveries * pred.rebound_log_prob * w[:, None]).sum(), (recoveries * w[:, None]).sum()))


def point_statistics(pred, labels, weight, group):
    """Squared error of points/100 after pooling rows to game x offense five."""
    _, inverse = torch.unique(group, sorted=True, return_inverse=True)
    size = int(inverse.max()) + 1
    n, w = labels["possessions"].double(), weight.double()
    pool = lambda values: n.new_zeros(size).index_add(0, inverse, values)
    total = pool(n)
    error = pool(n * pred.points100) / total - 100 * pool(labels["points"].double()) / total
    weights = total * pool(n * w) / total
    return (weights * error.square()).sum(), weights.sum()


def objective(events, point, reference, config, batches):
    """Per-batch training loss; sums over batches to the full-prefix objective."""
    exposure = reference["exposure"]
    terms = [events[f][0] / events[f][0].new_tensor(exposure["event"][f]) / reference["reference"]["event"][f]
             for f in FAMILIES]
    value = torch.stack(terms).mean() * batches
    if config.point_weight:
        value = value + config.point_weight * point[0] / exposure["point"] / reference["reference"]["point"] * batches
    return value


def validation_score(totals, reference, config):
    events = np.mean([totals[f][0] / totals[f][1] / reference["reference"]["event"][f] for f in FAMILIES])
    point = totals["point"][0] / totals["point"][1] / reference["reference"]["point"]
    return float(events + config.point_weight * point)


def references(model, data, rows, normalizer, env, config=FitConfig()):
    """Shared loss normalizers: the starting model's weighted event and point rates on the training rows.

    Ported from v16 ``references`` (rung 5): the model is the zero-head start of
    the fit (parent or phase-A offense), rows are the training prefix and the
    weights are the training row weights. Returns the reference.json layout.
    """
    cutoff = int(normalizer["cutoff_day"])
    totals = {f: [0., 0.] for f in FAMILIES} | {"point": [0., 0.]}
    model.eval()
    with torch.no_grad():
        for ix in game_batches(data.game, rows):
            inputs, labels, group = data.batch(ix, normalizer)
            weight = torch.as_tensor(np.exp2(-(cutoff - data.date[ix]) / config.half_life_days))
            pred = model(inputs, env)
            for f, (num, den) in event_statistics(pred, labels, weight).items():
                totals[f][0] += float(num)
                totals[f][1] += float(den)
            num, den = point_statistics(pred, labels, weight, group)
            totals["point"][0] += float(num)
            totals["point"][1] += float(den)
    rate = {f: totals[f][0] / totals[f][1] for f in totals}
    return dict(reference=dict(event={f: rate[f] for f in FAMILIES}, point=rate["point"]),
                exposure=dict(event={f: totals[f][1] for f in FAMILIES}, point=totals["point"][1]))


def self_references(data):
    """Fit references in which each phase is normalized by its own starting model.

    The definition for origins without saved references: pass
    ``reference=self_references(data)`` to fit_origin.
    """
    return lambda phase, model, rows, normalizer, env: references(model, data, rows, normalizer, env)


# ---- Adam's nonlinearity reward (exploratory screen) -------------------------------
OFFENSE_KEYS = ("base", "msg", "role", "rb_input", "rb_prior", "adjusted_offense", "offense_height", "offense_position")
DEFENSE_KEYS = ("defense", "adjusted_defense", "defense_height", "defense_position", "defense_tiebreak")


def second_difference(model, inputs, env, pick, side_offense, slots, donors, base_points):
    """f(L) - f(L, i swapped) - f(L, j swapped) + f(L, both) for lineups ``pick`` (zero if f adds up players).

    side_offense [m] bool; slots (i, j) [m] each; donors ((row, slot), (row, slot)) [m] each.
    """
    pick = torch.as_tensor(pick)
    chosen = {k: v[pick] for k, v in inputs.items()}

    def swapped(which):
        out = {k: v.clone() for k, v in chosen.items()}
        for w in which:
            slot, (row, donor_slot) = slots[w], donors[w]
            for side, keys in ((side_offense, OFFENSE_KEYS), (~side_offense, DEFENSE_KEYS)):
                at = np.flatnonzero(side)
                for k in keys:
                    if k in out and len(at):
                        out[k][torch.as_tensor(at), torch.as_tensor(slot[at])] = \
                            inputs[k][torch.as_tensor(row[at]), torch.as_tensor(donor_slot[at])]
        return model(out, env).points100

    return base_points - swapped((0,)) - swapped((1,)) + swapped((0, 1))


def nonadditivity_reward(lam, rows=256, seed=17):
    """Adam's linearity penalty: -lam * mean squared second difference of native points/100.

    Each batch: ``rows`` lineups, a random side, two slots and two donor players
    drawn from the batch. reports/nonlinearity_screen_protocol_2026_10_13.md.
    """
    rng = np.random.default_rng(seed)

    def reward(model, inputs, env, pred):
        n = pred.points100.shape[0]
        m = min(rows, n)
        pick = rng.choice(n, m, replace=False)
        side = rng.random(m) < .5
        i = rng.integers(0, 5, m)
        j = (i + rng.integers(1, 5, m)) % 5
        donors = tuple((rng.integers(0, n, m), rng.integers(0, 5, m)) for _ in range(2))
        delta = second_difference(model, inputs, env, pick, side, (i, j), donors, pred.points100[torch.as_tensor(pick)])
        return -lam * delta.double().square().mean()

    return reward


# ---- data plumbing ----------------------------------------------------------
def game_batches(game, rows, target_rows=4096, shuffle=False, seed=17):
    """Whole games per batch, so point pooling by game and offense five stays intact."""
    rows = np.asarray(rows, np.int64)
    ordered = rows[np.argsort(game[rows], kind="stable")]
    _, starts = np.unique(game[ordered], return_index=True)
    blocks = np.split(ordered, starts[1:])
    if shuffle:
        np.random.default_rng(seed).shuffle(blocks)
    current, size = [], 0
    for block in blocks:
        if current and size + len(block) > target_rows:
            yield np.concatenate(current)
            current, size = [], 0
        current.append(block)
        size += len(block)
    if current:
        yield np.concatenate(current)


class Rows:
    """Matchup rows and their labels; inputs come from a features.Store."""

    def __init__(self, g, store):
        self.g, self.store = g, store
        self.game = np.asarray(g["game_id"])
        self.date = np.asarray(g["date"])

    def prefix(self, cutoff_day, lookback_days):
        return np.flatnonzero((self.date < cutoff_day) & (self.date >= cutoff_day - lookback_days))

    def window(self, start_day, stop_day):
        return np.flatnonzero((self.date >= start_day) & (self.date < stop_day))

    def batch(self, rows, normalizer, *, origin_index=None):
        g = self.g
        mode = dict(origin_index=origin_index) if origin_index is not None else dict(game_ids=self.game[rows])
        inputs = self.store.batch(np.asarray(g["pids"][rows]), np.asarray(g["defense"][rows]), self.date[rows],
                                  normalizer, **mode)
        labels = {k: torch.as_tensor(np.asarray(g[k][rows])) for k in LABELS}
        return inputs, labels, torch.as_tensor(np.asarray(g["parent"][rows]))


# ---- fitting ----------------------------------------------------------------
def evaluate(model, data, rows, normalizer, env, *, origin_index, checkpoints=None):
    """Event/point totals and per-row ledgers; checkpoints -> mixture forecast."""
    model.eval()
    totals = {f: [0., 0.] for f in FAMILIES} | {"point": [0., 0.]}
    outputs = []
    original = copy.deepcopy(model.state_dict()) if checkpoints else None
    try:
        with torch.no_grad():
            for ix in game_batches(data.game, rows):
                inputs, labels, group = data.batch(ix, normalizer, origin_index=origin_index)
                if checkpoints:
                    preds = []
                    for state in checkpoints:
                        model.load_state_dict(state)
                        preds.append(model(inputs, env))
                    pred = average_ledgers(preds)
                else:
                    pred = model(inputs, env)
                weight = torch.ones(len(ix), dtype=torch.float64)
                for f, (num, den) in event_statistics(pred, labels, weight).items():
                    totals[f][0] += float(num)
                    totals[f][1] += float(den)
                num, den = point_statistics(pred, labels, weight, group)
                totals["point"][0] += float(num)
                totals["point"][1] += float(den)
                outputs.append((ix, pred.points100.numpy()))
    finally:
        if original is not None:
            model.load_state_dict(original)
    rows_out = np.concatenate([o[0] for o in outputs])
    order = np.argsort(rows_out)
    return totals, rows_out[order], np.concatenate([o[1] for o in outputs])[order]


def train(model, data, rows, normalizer, env, reference, seed, config=FitConfig(), *, validation=None,
          epochs=None, log=print, regularizer=None):
    """Inner fit (validation given: select an epoch) or final fit (epochs given).

    regularizer(model, inputs, env, pred) -> a term added to each batch's training loss (not to
    the validation score that selects the epoch).
    """
    if (validation is None) == (epochs is None):
        raise ValueError("give validation (inner fit) or a fixed number of epochs (final fit)")
    torch.use_deterministic_algorithms(True)
    groups = (model.parameter_groups(config.lr, config.weight_decay, config.pair_lr_scale, config.pair_decay)
              if hasattr(model, "parameter_groups") else model.parameters())
    optimizer = torch.optim.Adam(groups, lr=config.lr, weight_decay=config.weight_decay)
    torch.manual_seed(seed)
    cutoff = int(normalizer["cutoff_day"])
    best, threshold, best_epoch, stale, best_state = math.inf, math.inf, 0, 0, None
    checkpoints, curve = {}, []
    cap = epochs if epochs is not None else config.max_epochs
    for epoch in range(1, cap + 1):
        if validation is not None and stale >= config.patience:
            break
        tick = time.monotonic()
        model.train()
        batches = list(game_batches(data.game, rows, config.batch_rows, shuffle=True, seed=seed + epoch))
        loss_sum = 0.
        for ix in batches:
            inputs, labels, group = data.batch(ix, normalizer)
            weight = torch.as_tensor(np.exp2(-(cutoff - data.date[ix]) / config.half_life_days))
            optimizer.zero_grad(set_to_none=True)
            pred = model(inputs, env)
            loss = objective(event_statistics(pred, labels, weight), point_statistics(pred, labels, weight, group),
                             reference, config, len(batches))
            if regularizer is not None:
                loss = loss + regularizer(model, inputs, env, pred)
            if not torch.isfinite(loss):
                raise FloatingPointError("nonfinite training objective")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.clip)
            optimizer.step()
            model.project()
            loss_sum += float(loss.detach()) / len(batches)
        row = dict(epoch=epoch, train=loss_sum, seconds=time.monotonic() - tick)
        if validation is not None:
            val_rows, val_normalizer, val_env, val_origin = validation
            totals, *_ = evaluate(model, data, val_rows, val_normalizer, val_env, origin_index=val_origin)
            value = validation_score(totals, reference, config)
            if value < best:
                best, best_epoch, best_state = value, epoch, copy.deepcopy(model.state_dict())
            if value < threshold - config.min_delta:
                threshold, stale = value, 0
            else:
                stale += 1
            row.update(validation=value, best_epoch=best_epoch, stale=stale)
        elif epoch > cap - config.checkpoints:
            checkpoints[epoch] = copy.deepcopy(model.state_dict())
        curve.append(row)
        log(f"EPOCH {epoch}/{cap} " + " ".join(f"{k}={v:.7f}" if isinstance(v, float) else f"{k}={v}"
                                              for k, v in row.items() if k != "epoch"))
    if validation is not None:
        model.load_state_dict(best_state)
        return dict(selected_epoch=best_epoch, curve=curve, cap_hit=len(curve) == config.max_epochs)
    return dict(curve=curve, checkpoints=checkpoints)


def fit_origin(make_model, data, store, origin, inner, seed, config=FitConfig(), log=print, reference=None,
               regularizer=None):
    """Inner selection + fresh final refit for one origin; returns forecasts for the outer quarter.

    make_model(phase) -> a freshly initialized EventModel for that phase.
    origin/inner: schedule rows (tag, start, stop, origin_index).
    reference(phase, model, rows, normalizer, env) -> loss references; by default the store's saved
    references (v16 production); ``self_references(data)`` normalizes each phase by its own starting model.
    """
    day = lambda d: int(np.datetime64(d, "D").astype(np.int64))
    saved = lambda phase, *_: store.references[f"{origin.tag}/{phase}/s{seed}"]
    reference = reference or saved
    inner_norm, final_norm = store.normalizer(origin.tag, "inner"), store.normalizer(origin.tag, "final")
    inner_env, final_env = store.env(origin.tag, "inner"), store.env(origin.tag, "final")
    inner_rows = data.prefix(day(inner.start), config.lookback_days)
    validation = data.window(day(inner.start), day(inner.stop))
    log(f"INNER {origin.tag}/s{seed} rows={len(inner_rows):,} validation={len(validation):,}")
    model = make_model("inner")
    inner_ref = reference("inner", model, inner_rows, inner_norm, inner_env)
    inner_fit = train(model, data, inner_rows, inner_norm, inner_env, inner_ref, seed, config,
                      validation=(validation, inner_norm, inner_env, int(inner.origin_index)), log=log,
                      regularizer=regularizer)
    selected = inner_fit["selected_epoch"]
    inner_state = copy.deepcopy(model.state_dict())
    final_rows = data.prefix(day(origin.start), config.lookback_days)
    log(f"FINAL {origin.tag}/s{seed} rows={len(final_rows):,} epochs={selected}")
    model = make_model("final")
    final_ref = reference("final", model, final_rows, final_norm, final_env)
    final_fit = train(model, data, final_rows, final_norm, final_env, final_ref, seed, config,
                      epochs=selected, log=log, regularizer=regularizer)
    outer = data.window(day(origin.start), day(origin.stop))
    states = [final_fit["checkpoints"][e] for e in sorted(final_fit["checkpoints"])]
    rows = direct = averaged = np.empty(0)          # a prospective origin has no outer games yet
    if len(outer):
        _, rows, direct = evaluate(model, data, outer, final_norm, final_env, origin_index=int(origin.origin_index))
        _, _, averaged = evaluate(model, data, outer, final_norm, final_env, origin_index=int(origin.origin_index),
                                  checkpoints=states)
    return dict(selected_epoch=selected, inner_state=inner_state, references=dict(inner=inner_ref, final=final_ref),
                inner_curve=inner_fit["curve"],
                final_curve=final_fit["curve"],
                rows=rows, direct=direct, checkpoint_average=averaged, final_state=model.state_dict(),
                checkpoint_states=states)
