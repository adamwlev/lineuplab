"""Can the network learn the interactions itself? (exploratory screen, 2026-10-13)

Protocol: reports/nonlinearity_screen_protocol_2026_10_13.md (committed before any arm was trained).

Arms at the 20 quarters of 2022-2026, seed 17, full reference protocol from the v14 parent:
    reference    the saved J_POINT_BOTH fit (inference only)
    pairs        + PairInteractions, no weight decay on it
    pairs_fast   pairs with the module's learning rate x5
    reward       Adam's nonlinearity reward, strength k from the pilot
    pairs_held   pairs with partner sums held at their measured range (second screen,
                 reports/nonlinearity_screen2_protocol_2026_10_13.md)
    pairs_out    the pairs weights with outputs held at their measured range (third screen,
                 reports/nonlinearity_screen3_protocol_2026_10_13.md; no refit)
    pairs_joint  pairs_out plus a joint (ellipsoid) bound on each lineup's outputs (fourth screen,
                 reports/nonlinearity_screen4_protocol_2026_10_13.md; no refit)
    frozen_joint the saved reference frozen, only a held (joint) PairInteractions trained on top
                 (fifth screen, reports/nonlinearity_screen5_protocol_2026_10_13.md)
    frozen_fixed frozen_joint trained a fixed FIXED_EPOCHS on the final rows, no early stopping
                 (fifth screen, variant b: reports/nonlinearity_screen5b_protocol_2026_10_13.md)
    frozen_pure  frozen_fixed with the module a pure interaction (centered features; sixth screen,
                 reports/nonlinearity_screen6_protocol_2026_10_13.md)

--seed (default 17) fits or reads another seed; its files carry an _s<seed> suffix.

    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --pilot 10        # at 2024q2, labeled pilot
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --arm pairs --origin 2024q2
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --arm reference --origin 2024q2
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --summary
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --fixtures      # second screen
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --properties
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --held-diagnostic  # post hoc
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --arm pairs_out --origin 2024q2  # third screen
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --summary --name screen3_summary
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --out-diagnostic   # post hoc
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --arm pairs --origin 2024q2 --seed 23
    PYTHONPATH=.:scripts python -u scripts/nonlinearity_screen.py --fixtures --arms reference pairs pairs_out \
        --name screen3_fixture_sweep        (and --properties with --name screen3_properties)
"""
import argparse
import json
import os
import time

import numpy as np
import pandas as pd
import torch

from lineups import evaluate, history, legacy, paths
from lineups.coherence import fixtures, matchup
from lineups.history import checkpoint_models     # the active cache root's history (lineups.history, 2026-10-16)
from lineups.learned import measure_holds, rates
from lineups.features import Store
from lineups.model import EventModel, PairInteractions, average_ledgers, load_legacy
from lineups.train import FitConfig, Rows, fit_origin, game_batches, nonadditivity_reward

OUT = paths.CACHE / "nonlinearity_screen_2026_10_13"
THREADS = int(os.environ.get("LINEUPS_THREADS", 4))     # torch threads for the summaries (the refresh: 1)
V14 = paths.CACHE / "joint_capability_2026_09_15_v14_prod"
DEFAULT_SEED, PILOT_ORIGIN, PILOT_KS, PILOT_FACTOR = 17, "2024q2", (1, 10, 100), 5.
SEED = DEFAULT_SEED  # set by --seed
ERA = (2022, 2026)   # origin seasons; set by --era (the screens: 2022-2026)
ARMS = ("reference", "pairs", "pairs_fast", "reward", "pairs_held", "pairs_out", "pairs_joint", "frozen_joint",
        "frozen_fixed", "frozen_pure")
HOLD = dict(pairs_held="inputs", pairs_out="outputs", pairs_joint="joint", frozen_joint="joint", frozen_fixed="joint",
            frozen_pure="joint")
FIXED = ("frozen_fixed", "frozen_pure")   # trained a fixed number of epochs
FIXED_EPOCHS = 8   # frozen_fixed: the co-trained pairs arm's median selected epoch (first screen)
EVENT_FAMILIES = ("rim_share", "three_share", "tov", "fta")
FIXTURE_PAIRS = (("legal_pure_centers", "jokic_westbrook"), ("legal_pure_centers", "jokic_korver"),
                 ("five_goberts", "jokic_westbrook"), ("five_jokics", "jokic_westbrook"))


def league_of(tag, n, g):
    """The origin's dated league level for n rows (lineups.history.league_at; equals the saved controls' league)."""
    return np.full(n, history.league_at(g, legacy.day(legacy.schedule().set_index("tag").loc[tag].start)))


def module(arm):
    """The arm's pair module, freshly initialized."""
    return PairInteractions(hold=HOLD.get(arm), centered=arm == "frozen_pure")


def stem(arm):
    """An arm's file stem: seed 17 unsuffixed, as in the first three screens."""
    return arm if SEED == DEFAULT_SEED else f"{arm}_s{SEED}"


def origins():
    s = legacy.schedule()
    return s[s.season.between(*ERA)].reset_index(drop=True)


def forecast(models, data, rows, normalizer, env, origin_index):
    """Checkpoint-mixture rates for outer rows, in row order."""
    out = []
    with torch.no_grad():
        for ix in game_batches(data.game, rows):
            inputs, _, _ = data.batch(ix, normalizer, origin_index=origin_index)
            out.append((ix, rates(average_ledgers([m.eval()(inputs, env) for m in models]))))
    ids = np.concatenate([o[0] for o in out])
    order = np.argsort(ids)
    return ids[order], {k: np.concatenate([o[1][k] for o in out])[order] for k in out[0][1]}


def make_model(arm, tag):
    def make(phase):
        if arm.startswith("frozen"):
            # the reference for this phase, frozen; only the pair module trains. The final phase comes from the
            # active root's history (lineups.history); the inner phase exists only for the saved v16 reference
            if phase == "final":
                model = history.final_model(tag, SEED).train()
            else:
                state = torch.load(paths.V16_RUN / "origins" / tag / "J_POINT_BOTH" / f"s{SEED}" / phase / "fit.pt",
                                   map_location="cpu", weights_only=False)["state_dict"]
                model = load_legacy(state).train()
            for p in model.parameters():
                p.requires_grad_(False)
        else:
            parent = torch.load(V14 / "origins" / tag / "RB_RENEW_FAC" / f"s{SEED}" / f"{phase}.pt",
                                map_location="cpu", weights_only=False)["state_dict"]
            model = EventModel.from_parent(parent, SEED)
        if arm in HOLD or arm.startswith("pairs"):
            with torch.random.fork_rng():
                torch.manual_seed(SEED + 1800)
                model.pairs = module(arm)
        return model
    return make


def hold_outputs(arm, tag, data, rows, normalizer, log=print):
    """Third and fourth screens: the pairs arm's checkpoints, each with its outputs' measured range on its
    training rows.

    Inputs are built as in training (each game's own features); the quantiles are unweighted over rows."""
    saved = torch.load(OUT / f"{stem('pairs')}_{tag}.pt", map_location="cpu", weights_only=False)
    models = []
    for state in saved["checkpoints"]:
        m = make_model(arm, tag)("final")
        missing, unexpected = m.load_state_dict(state, strict=False)
        assert not unexpected and sorted(missing) == sorted(f"pairs.{b}" for b, _ in m.pairs.named_buffers()), \
            (missing, unexpected)
        models.append(m.eval())
    measure_holds([m.pairs for m in models], data, rows, normalizer, log)
    return models


def fixed_fit(model, data, store, origin, log=print):
    """frozen_fixed: FIXED_EPOCHS on the origin's final training rows with the reference's saved loss
    references; no inner phase, since no epoch is selected."""
    from lineups.train import train
    day = int(np.datetime64(origin.start, "D").astype(np.int64))
    rows = data.prefix(day, FitConfig().lookback_days)
    log(f"FIXED {origin.tag}/s{SEED} rows={len(rows):,} epochs={FIXED_EPOCHS}")
    out = train(model, data, rows, store.normalizer(origin.tag, "final"), store.env(origin.tag, "final"),
                history.final_references(origin.tag, SEED, store), SEED, FitConfig(), epochs=FIXED_EPOCHS, log=log)
    return dict(selected_epoch=FIXED_EPOCHS, checkpoint_states=[out["checkpoints"][e] for e in sorted(out["checkpoints"])])


def reward_strength(store, tag, k):
    return k * FitConfig().point_weight / store.references[f"{tag}/final/s{SEED}"]["reference"]["point"]


def nonadditive_share(frame, points):
    """Possession-weighted share of forecast variance left after the best additive (player dummies) fit."""
    from synergy_check import additive_projection
    f = frame.assign(R=points)
    a = additive_projection(f)
    w = f.possessions.to_numpy(float)
    c = lambda v: v - np.average(v, weights=w)
    return float(np.average(c(points - a) ** 2, weights=w) / np.average(c(points) ** 2, weights=w))


def fit_arm(arm, tag, k=None, out=OUT, label=None):
    torch.set_num_threads(1)
    out.mkdir(parents=True, exist_ok=True)
    name = label or stem(arm)
    tick = time.monotonic()
    log = lambda m: print(f"[{name} {tag} {time.monotonic() - tick:6.0f}s] {m}", flush=True)
    store, g = Store(), legacy.matchups()
    data = Rows(g, store)
    schedule = legacy.schedule()
    origin = schedule[schedule.tag == tag].iloc[0]
    normalizer, env = store.normalizer(tag, "final"), store.env(tag, "final")
    rows = np.sort(legacy.quarter_rows(origin, g))
    if arm == "reference":
        models = checkpoint_models(tag, seeds=(SEED,))
        record = dict(arm=arm, origin=tag)
    elif arm in ("pairs_out", "pairs_joint"):
        final_rows = data.prefix(int(np.datetime64(origin.start, "D").astype(np.int64)), FitConfig().lookback_days)
        models = hold_outputs(arm, tag, data, final_rows, normalizer, log)
        torch.save(dict(checkpoints=[m.state_dict() for m in models]), out / f"{name}_{tag}.pt")
        record = dict(arm=arm, origin=tag, seed=SEED, training_rows=len(final_rows),
                      selected_epoch=json.loads((OUT / f"{stem('pairs')}_{tag}.json").read_text())["selected_epoch"])
    elif arm.startswith("frozen"):
        if arm in FIXED:
            fit = fixed_fit(make_model(arm, tag)("final"), data, store, origin, log)
        else:
            fit = fit_origin(make_model(arm, tag), data, store, origin,
                             schedule[schedule.stop <= origin.start].iloc[-1], SEED, FitConfig(), log=log)
        frozen, final = make_model(arm, tag)("final").state_dict(), fit["checkpoint_states"][-1]
        moved = [k for k in frozen if not k.startswith("pairs.") and not torch.equal(frozen[k], final[k])]
        if moved:
            raise ValueError(f"frozen network weights moved at {tag}: {moved[:5]}")
        trained = module(arm)
        trained.load_state_dict({k[len("pairs."):]: v for k, v in final.items() if k.startswith("pairs.")})
        final_rows = data.prefix(int(np.datetime64(origin.start, "D").astype(np.int64)), FitConfig().lookback_days)
        measure_holds([trained], data, final_rows, normalizer, log)
        torch.save(dict(module=trained.state_dict(), selected=fit["selected_epoch"]), out / f"{name}_{tag}.pt")
        models = load_models(arm, tag)
        record = dict(arm=arm, origin=tag, seed=SEED, selected_epoch=fit["selected_epoch"],
                      training_rows=len(final_rows))
    else:
        config = FitConfig(pair_lr_scale=5.) if arm == "pairs_fast" else FitConfig()
        regularizer = nonadditivity_reward(reward_strength(store, tag, k), seed=SEED) if arm == "reward" else None
        fit = fit_origin(make_model(arm, tag), data, store, origin,
                         schedule[schedule.stop <= origin.start].iloc[-1], SEED, config, log=log, regularizer=regularizer)
        models = []
        for state in fit["checkpoint_states"]:
            m = make_model(arm, tag)("final")
            m.load_state_dict(state)
            models.append(m.eval())
        torch.save(dict(checkpoints=fit["checkpoint_states"], selected=fit["selected_epoch"], k=k),
                   out / f"{name}_{tag}.pt")
        record = dict(arm=arm, origin=tag, seed=SEED, k=k, selected_epoch=fit["selected_epoch"],
                      lam=None if k is None else reward_strength(store, tag, k))
    ids, r = forecast(models, data, rows, normalizer, env, int(origin.origin_index))
    assert np.array_equal(ids, rows)
    if arm == "reference":
        saved_ids, saved = history.native(tag, SEED, "checkpoint_average")
        gap = float(np.abs(r["points"] - saved).max())
        if not np.array_equal(saved_ids, rows) or gap > 1e-5:
            raise ValueError(f"rebuilt reference differs from the saved forecast at {tag}: {gap}")
    frame = legacy.row_frame(rows, g)
    pd.DataFrame(dict(row=rows, **r)).to_pickle(out / f"{name}_{tag}_rows.pkl")
    record["nonadditive_share"] = nonadditive_share(frame, r["points"])
    if tag == "2026q4":
        fx = fixtures()
        record["fixtures"] = {f"{a}|{b}": matchup(models, store, fx[a]["pids"], fx[b]["pids"], tag)["margin"]
                              for a, b in FIXTURE_PAIRS}
    (out / f"{name}_{tag}.json").write_text(json.dumps(record, indent=1, default=float))
    log(f"done: {json.dumps(record, default=float)}")


# ---- summary --------------------------------------------------------------------------------
def prior_calibrations(tags):
    """The reference's prior-only affine (seed 17, direct) at each origin, in one pass (as coverage_screen)."""
    g = legacy.matchups()
    cells, out = [], {}
    for o in legacy.origins().itertuples():
        if o.tag in tags:
            out[o.tag] = evaluate.affine(pd.concat(cells, ignore_index=True) if cells else None, o.start)
        if len(out) == len(tags):
            return out
        rows = legacy.row_frame(legacy.quarter_rows(o, g), g)
        ids, native = history.native(o.tag, SEED, "direct")
        assert np.array_equal(ids, rows.row.to_numpy())
        cells.append(evaluate.history_cells(rows, native, league_of(o.tag, len(rows), g), o.stop))
    return out


def frame_with_actuals(g, rows_by_tag):
    import nn_vs_linear
    parts = []
    for tag, rows in rows_by_tag.items():
        f = legacy.row_frame(rows, g)
        for k, (num, e) in nn_vs_linear.actual(g, rows).items():
            if k in ("points",) + EVENT_FAMILIES:
                f[f"{k}_num"], f[f"{k}_exp"] = num, e
        o = origins().set_index("tag").loc[tag]
        parts.append(f.assign(origin=tag, season=int(o.season)))
    return pd.concat(parts, ignore_index=True)


def summary(name="summary"):
    import interaction_discovery as d
    from capacity_screen import oracle
    g = legacy.matchups()
    tags = origins().tag.tolist()
    arms = [a for a in ARMS if all((OUT / f"{stem(a)}_{t}_rows.pkl").exists() for t in tags)]
    fc = {a: {t: pd.read_pickle(OUT / f"{stem(a)}_{t}_rows.pkl") for t in tags} for a in arms}
    frame = frame_with_actuals(g, {t: fc["reference"][t].row.to_numpy() for t in tags})
    for a in arms:
        cat = pd.concat([fc[a][t] for t in tags], ignore_index=True)
        assert np.array_equal(cat.row.to_numpy(), frame.row.to_numpy())
        for k in ("points",) + EVENT_FAMILIES:
            frame[f"{a}_{k}"] = cat[k].to_numpy()
    lines, result = [f"arms: {arms}; origins {tags[0]}-{tags[-1]} ({len(tags)})"], dict(arms=arms)

    # 2. accuracy: calibrated points r2 on outer broad cells
    acc, priors = [], prior_calibrations(set(tags))
    for t in tags:
        q = frame[frame.origin == t]
        league = league_of(t, len(q), g)
        prior = priors[t]
        for a in arms:
            native = q[f"{a}_points"].to_numpy()
            for how, cal in (("prior", prior), ("oracle", oracle(native, q, league))):
                f = q.assign(cal=evaluate.calibrate(cal, native, league))
                c = evaluate.cells(f, ["cal"])
                c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
                acc.append(dict(origin=t, arm=a, how=how,
                                r2=evaluate.metrics(evaluate.sufficient(c.actual, c.cal, c.possessions))["r2"]))
    acc = pd.DataFrame(acc)
    result["accuracy"] = {}
    for how in ("prior", "oracle"):
        tab = acc[acc.how == how].pivot(index="origin", columns="arm", values="r2")
        for a in arms:
            if a == "reference":
                continue
            diff = tab[a] - tab["reference"]
            result["accuracy"][f"{a}_{how}"] = dict(mean=float(diff.mean()), se=float(diff.std(ddof=1) / np.sqrt(len(diff))),
                                                    positive=int((diff > 0).sum()))
            lines.append(f"accuracy {how:<6} {a:<11} - reference: {diff.mean():+.5f} (SE {diff.std(ddof=1) / np.sqrt(len(diff)):.5f}), "
                         f"positive {int((diff > 0).sum())}/{len(diff)}")

    # 3. nonlinearity
    result["nonadditive_share"] = {}
    for a in arms:
        shares = [json.loads((OUT / f"{stem(a)}_{t}.json").read_text())["nonadditive_share"] for t in tags]
        result["nonadditive_share"][a] = float(np.mean(shares))
        lines.append(f"non-additive share of points-forecast variance, {a:<11}: {np.mean(shares):.4f}")

    # 1. interactions
    feats, _ = d.features(frame, False)
    held = json.loads((d.OUT / "result.json").read_text())["families"]
    H = {(fam, c["candidate"]) for fam, v in held.items() for c in v["confirmed"] if c["label"].startswith("held up")}
    off, de = frame[evaluate.FIVE].to_numpy(), frame[legacy.DEFENSE].to_numpy()

    def column(family, values):
        f = frame.copy()
        if family == "points":
            f["w_points"] = f.possessions.astype(float)
        else:
            f[f"w_{family}"] = f[f"{family}_exp"].astype(float)
        f[f"y_{family}"] = values
        return f

    def actual_rate(family):
        num, e = frame[f"{family}_num"].to_numpy(float), frame[f"{family}_exp"].to_numpy(float)
        return np.divide(num, e, out=np.zeros(len(frame)), where=e > 0)

    def projection(family, values):
        out = np.full(len(frame), np.nan)
        w = (frame.possessions if family == "points" else frame[f"{family}_exp"]).to_numpy(float)
        for t in tags:
            m = (frame.origin == t).to_numpy()
            out[m] = d.project(off[m], de[m], values[m], w[m])
        return out

    scale = lambda family: 1. if family == "points" else 100.
    coef = {}
    for family in ("points",) + EVENT_FAMILIES:
        y = actual_rate(family) * (100 if family == "points" else 1)
        ref_add = projection(family, frame[f"reference_{family}"].to_numpy())
        targets = {"actual": scale(family) * (y - ref_add)}
        for a in arms:
            fcast = frame[f"{a}_{family}"].to_numpy()
            targets[f"residual_{a}"] = scale(family) * (y - fcast)
            targets[f"implied_{a}"] = scale(family) * (fcast - projection(family, fcast))
        for target, values in targets.items():
            data = d.window_data(column(family, values), feats, family, ERA)
            for c in d.CANDIDATES:
                r = d.test(data, c)
                coef[(family, d.name(c), target)] = (r["coef"], r["se"])
        print("interactions", family, flush=True)
    cells = sorted({(f, c) for f, c, _ in coef})
    result["interactions"] = {}
    for a in arms:
        z2 = {cell: (coef[cell + (f"residual_{a}",)][0] / coef[cell + (f"residual_{a}",)][1]) ** 2 for cell in cells}
        chi_h = float(sum(v for cell, v in z2.items() if cell in H))
        chi_n = float(sum(v for cell, v in z2.items() if cell not in H))
        act = np.array([coef[cell + ("actual",)][0] for cell in cells if cell in H])
        imp = np.array([coef[cell + (f"implied_{a}",)][0] for cell in cells if cell in H])
        capture = float(imp @ act / (act @ act))
        imp_n = np.array([coef[cell + (f"implied_{a}",)][0] / coef[cell + ("actual",)][1] for cell in cells if cell not in H])
        result["interactions"][a] = dict(chi2_H=chi_h, chi2_N=chi_n, capture=capture, cells_H=len(act),
                                         cells_N=len(cells) - len(act), implied_N_rms_in_se=float(np.sqrt(np.mean(imp_n ** 2))))
        lines.append(f"interactions {a:<11}: chi2_H {chi_h:7.1f} ({len(act)} cells)  chi2_N {chi_n:7.1f} "
                     f"({len(cells) - len(act)} cells)  capture {capture:+.2f}  implied on N, RMS in SE units "
                     f"{np.sqrt(np.mean(imp_n ** 2)):.2f}")
    pd.DataFrame([dict(family=f, candidate=c, kind=n, coef=v[0], se=v[1]) for (f, c, n), v in coef.items()]).to_csv(
        OUT / ("interaction_coefficients.csv" if name == "summary" else f"{name}_interaction_coefficients.csv"),
        index=False)

    # 4. fixtures
    result["fixtures"] = {a: json.loads((OUT / f"{stem(a)}_{tags[-1]}.json").read_text()).get("fixtures") for a in arms}
    for a in arms:
        lines.append(f"fixtures {tags[-1]} {a:<11}: " + ", ".join(f"{k} {v:+.1f}" for k, v in (result["fixtures"][a] or {}).items()))
    result["selected_epochs"] = {a: [json.loads((OUT / f"{stem(a)}_{t}.json").read_text()).get("selected_epoch")
                                     for t in tags]
                                 for a in arms}
    (OUT / f"{name}.json").write_text(json.dumps(result, indent=1, default=float))
    text = "\n".join(lines)
    (OUT / f"{name}.txt").write_text(text)
    print(text)


def load_models(arm, tag):
    """An arm's checkpoint mixture at one origin (the reference: the saved seed-17 fit)."""
    if arm == "reference":
        return checkpoint_models(tag, seeds=(SEED,))
    saved = torch.load(OUT / f"{stem(arm)}_{tag}.pt", map_location="cpu", weights_only=False)
    if arm.startswith("frozen"):
        # one module on each of the reference's checkpoints (its outputs read only lineup inputs)
        models = checkpoint_models(tag, seeds=(SEED,))
        for m in models:
            m.pairs = module(arm)
            m.pairs.load_state_dict(saved["module"])
            m.eval()
        return models
    models = []
    for state in saved["checkpoints"]:
        m = make_model(arm, tag)("final")
        m.load_state_dict(state)
        models.append(m.eval())
    return models


def fixture_sweep(arms=("reference", "pairs", "pairs_held"), name="fixture_sweep"):
    """Second screen, contrast 2: fixture margins and offenses at every origin, arm minus reference."""
    torch.set_num_threads(THREADS)
    store, fx, out = Store(), fixtures(), []
    for tag in origins().tag:
        for arm in arms:
            models = load_models(arm, tag)
            with torch.no_grad():
                for a, b in FIXTURE_PAIRS:
                    r = matchup(models, store, fx[a]["pids"], fx[b]["pids"], tag)
                    out.append(dict(origin=tag, arm=arm, fixture=f"{a}|{b}", a_offense=r["a_offense"],
                                    b_offense=r["b_offense"], margin=r["margin"]))
        print("fixtures", tag, flush=True)
    f = pd.DataFrame(out)
    f.to_csv(OUT / f"{name}.csv", index=False)
    lines = []
    for fixture, q in f.groupby("fixture", sort=False):
        t = q.pivot(index="origin", columns="arm")
        for arm in arms:
            parts = [f"{k} {t[(k, arm)].mean():6.1f}" for k in ("a_offense", "b_offense", "margin")]
            if arm != "reference":
                for k in ("a_offense", "b_offense", "margin"):
                    d = t[(k, arm)] - t[(k, "reference")]
                    parts.append(f"d{k} {d.mean():+.1f} (SE {d.std(ddof=1) / np.sqrt(len(d)):.1f})")
            lines.append(f"{fixture:<38} {arm:<11} " + "  ".join(parts))
    text = "\n".join(lines)
    (OUT / f"{name}.txt").write_text(text)
    print(text)


def property_check(arms=("reference", "pairs", "pairs_held"), tag="2026q4", name="properties"):
    """Second screen, contrast 3: the property suite at 2026q4."""
    import property_suite
    from lineups import properties
    from lineups.coherence import ledgers
    torch.set_num_threads(THREADS)
    store, g = Store(), legacy.matchups()
    offense = property_suite.real_fives(tag, g, evaluate.FIVE)
    defense = property_suite.real_fives(tag, g, legacy.DEFENSE)
    rates = {}
    for arm in arms:
        models = load_models(arm, tag)
        suite = properties.run(lambda o, d, m=models: ledgers(m, store, o, d, tag), store, tag, offense, defense,
                               offense[:40])
        suite.to_csv(OUT / f"{name}_{arm}_{tag}.csv", index=False)
        rates[arm] = properties.summarize(suite).pass_rate
        print("properties", arm, flush=True)
    table = pd.DataFrame(rates).round(3)
    (OUT / f"{name}_{tag}.txt").write_text(table.to_string())
    print(table.to_string())


def held_diagnostic(tag="2026q4"):
    """Second screen, post hoc: how often the clamp binds, and what it leaves.

    1. Each fixture under pairs_held with the clamp on and off (same weights).
    2. The last checkpoint's offensive pair outputs (15 channels) on the origin's real outer rows,
       per player and summed over the lineup, against five Goberts' with the clamp on."""
    from lineups.model import PairInteractions
    torch.set_num_threads(THREADS)
    store, g, fx = Store(), legacy.matchups(), fixtures()
    models = load_models("pairs_held", tag)
    seen, held = [], PairInteractions.held

    def spy(self, partners, side):
        out = held(self, partners, side)
        if self.hold == "inputs" and not self.training:
            b = getattr(self, f"{side}_range")
            flat = partners.reshape(-1, b.shape[1])
            seen.append((side, float(((flat > b[1]) | (flat < b[0])).float().mean())))
        return out

    lines = []
    PairInteractions.held = spy
    try:
        with torch.no_grad():
            for a, b in FIXTURE_PAIRS:
                seen.clear()
                on = matchup(models, store, fx[a]["pids"], fx[b]["pids"], tag)
                share = {s: np.mean([v for k, v in seen if k == s]) for s in ("offense", "defense")}
                for m in models:
                    m.pairs.hold = None
                off = matchup(models, store, fx[a]["pids"], fx[b]["pids"], tag)
                for m in models:
                    m.pairs.hold = "inputs"
                lines.append(f"{a}|{b}: held A {on['a_offense']:.1f} B {on['b_offense']:.1f} margin "
                             f"{on['margin']:+.1f}; unheld A {off['a_offense']:.1f} B {off['b_offense']:.1f} "
                             f"margin {off['margin']:+.1f}; components clamped offense {share['offense']:.3f} "
                             f"defense {share['defense']:.3f}")
    finally:
        PairInteractions.held = held

    data, s = Rows(g, store), legacy.schedule()
    origin = s[s.tag == tag].iloc[0]
    normalizer, env = store.normalizer(tag, "final"), store.env(tag, "final")
    m, captured = models[-1], []
    hook = m.pairs.register_forward_hook(lambda mod, i, o: captured.append(o[0]))
    with torch.no_grad():
        for ix in game_batches(data.game, np.sort(legacy.quarter_rows(origin, g))):
            m(data.batch(ix, normalizer, origin_index=int(origin.origin_index))[0], env)
        real = torch.cat(captured)
        captured.clear()
        matchup([m], store, fx["five_goberts"]["pids"], fx["jokic_westbrook"]["pids"], tag)
    hook.remove()
    goberts = captured[0][0]
    q = lambda x: torch.quantile(x, torch.tensor([.005, .995]), dim=0)
    per, total = q(real.reshape(-1, 15)), q(real.sum(1))
    outside = lambda x, r: int(((x > r[1]) | (x < r[0])).sum())
    lines.append(f"offensive pair outputs, {len(real)} real rows at {tag}, last checkpoint; channel: "
                 "real per-player 0.5-99.5% | five Goberts per player | real lineup total 0.5-99.5% | Goberts total")
    for c in range(15):
        lines.append(f"  {c:2d}: {per[0, c]:+.3f} {per[1, c]:+.3f} | {goberts[0, c]:+.3f} | "
                     f"{total[0, c]:+.3f} {total[1, c]:+.3f} | {goberts[:, c].sum():+.3f}")
    lines.append(f"channels outside the real range: per player {outside(goberts[0], per)}/15, "
                 f"lineup total {outside(goberts.sum(0), total)}/15")
    text = "\n".join(lines)
    (OUT / f"held_diagnostic_{tag}.txt").write_text(text)
    print(text)


def out_diagnostic(tag="2026q4"):
    """Third screen, post hoc: which held outputs bind for the fixtures, and how often real lineups sit
    at their lineup bound in as many channels at once. Last checkpoint; outer rows of the origin."""
    store, g, fx = Store(), legacy.matchups(), fixtures()
    m = load_models("pairs_out", tag)[-1]
    data, s = Rows(g, store), legacy.schedule()
    origin = s[s.tag == tag].iloc[0]
    normalizer, env = store.normalizer(tag, "final"), store.env(tag, "final")
    captured = []
    hook = m.pairs.register_forward_hook(lambda mod, i, o: captured.append(o[0].sum(1)))
    lo, hi = m.pairs.lineup_bounds
    at_bound = lambda t: ((t >= hi - 1e-6) & (hi > 0)) | ((t <= lo + 1e-6) & (lo < 0))
    lines = []
    with torch.no_grad():
        for ix in game_batches(data.game, np.sort(legacy.quarter_rows(origin, g))):
            m(data.batch(ix, normalizer, origin_index=int(origin.origin_index))[0], env)
        real = at_bound(torch.cat(captured)).sum(1)
        for a, b in FIXTURE_PAIRS[::2] + FIXTURE_PAIRS[3:]:
            captured.clear()
            matchup([m], store, fx[a]["pids"], fx[b]["pids"], tag)
            bound = at_bound(captured[0][0])
            lines.append(f"{a} on offense: lineup sum at its bound in {int(bound.sum())}/15 channels "
                         f"{bound.nonzero().flatten().tolist()}; real lineups with at least as many: "
                         f"{float((real >= int(bound.sum())).float().mean()):.4f}")
    hook.remove()
    lines.append(f"real outer lineups ({len(real)}) by channels at bound: "
                 + ", ".join(f"{k}: {float((real == k).float().mean()):.4f}" for k in range(int(real.max()) + 1)))
    text = "\n".join(lines)
    (OUT / f"out_diagnostic_{tag}.txt").write_text(text)
    print(text)


def backbone_diagnostic(arm="pairs_joint"):
    """Fourth screen, post hoc: the arm's fixture offenses with its pair module switched off, at every origin.

    The pairs arms train the whole network with the module, so part of an arm-minus-reference change can
    come from the co-trained network rather than from the module's outputs. Switching a path off is an
    accounting split, not a causal effect."""
    torch.set_num_threads(THREADS)
    store, fx, out = Store(), fixtures(), []
    for tag in origins().tag:
        models = load_models(arm, tag)
        modules = [m.pairs for m in models]
        with torch.no_grad():
            for a, b in FIXTURE_PAIRS[::2] + FIXTURE_PAIRS[3:]:
                on = matchup(models, store, fx[a]["pids"], fx[b]["pids"], tag)
                for m in models:
                    m.pairs = None
                off = matchup(models, store, fx[a]["pids"], fx[b]["pids"], tag)
                for m, pairs in zip(models, modules):
                    m.pairs = pairs
                if tag == "2026q4" and a == "five_goberts":
                    captured = []
                    hook = models[-1].pairs.register_forward_hook(lambda mod, i, o: captured.append(o))
                    matchup(models[-1:], store, fx[a]["pids"], fx[b]["pids"], tag)
                    hook.remove()
                    pm, (offense, _) = models[-1].pairs, captured[0]
                    total = offense[0].sum(0)
                    radius = f"{float(((total @ pm.lineup_metric) * total).sum().sqrt()):.2f} vs radius " \
                             f"{float(pm.lineup_radius):.2f}" if pm.hold == "joint" else "n/a"
                out.append(dict(origin=tag, fixture=f"{a}|{b}", a_on=on["a_offense"], a_off=off["a_offense"],
                                b_on=on["b_offense"], b_off=off["b_offense"]))
        print("backbone", tag, flush=True)
    f = pd.DataFrame(out)
    ref = pd.read_csv(OUT / "screen4_fixture_sweep.csv").query("arm == 'reference'").set_index(["origin", "fixture"])
    f = f.join(ref[["a_offense", "b_offense"]], on=["origin", "fixture"])
    lines = [f"{arm}: fixture offenses vs the reference, mean over 20 origins (origin SE)"]
    se = lambda d: d.std(ddof=1) / np.sqrt(len(d))
    for fixture, q in f.groupby("fixture", sort=False):
        for side in ("a", "b"):
            total, network = q[f"{side}_on"] - q[f"{side}_offense"], q[f"{side}_off"] - q[f"{side}_offense"]
            lines.append(f"  {fixture:<36} {side} offense: arm {total.mean():+.1f} ({se(total):.1f}) = co-trained "
                         f"network {network.mean():+.1f} ({se(network):.1f}) + module {(total - network).mean():+.1f} "
                         f"({se(total - network):.1f})")
    lines.append(f"five Goberts' offensive sum at 2026q4, last checkpoint: distance {radius}")
    f.to_csv(OUT / f"backbone_diagnostic_{arm}.csv", index=False)
    text = "\n".join(lines)
    (OUT / f"backbone_diagnostic_{arm}.txt").write_text(text)
    print(text)


UNTUNED = ("limited_centers", "small_guards") + tuple(f"clone_ladder_{n}" for n in range(1, 6))


def confirm(arm="frozen_joint", seeds=(23, 41), name="screen5_confirm"):
    """Fifth screen, Part B: the declared fixture criteria on fresh seeds (seed-matched reference, the two
    seeds averaged within each origin), plus lineups no screen looked at, reported without a bar."""
    global SEED
    torch.set_num_threads(THREADS)
    store, fx, out = Store(), fixtures(), []
    pairs = list(FIXTURE_PAIRS) + [(u, "jokic_westbrook") for u in UNTUNED]
    for seed in seeds:
        SEED = seed
        for tag in origins().tag:
            for which in ("reference", arm):
                models = load_models(which, tag)
                with torch.no_grad():
                    for a, b in pairs:
                        r = matchup(models, store, fx[a]["pids"], fx[b]["pids"], tag)
                        out.append(dict(seed=seed, origin=tag, arm=which, fixture=f"{a}|{b}", a_offense=r["a_offense"],
                                        b_offense=r["b_offense"], margin=r["margin"]))
            print("confirm", seed, tag, flush=True)
    SEED = DEFAULT_SEED
    f = pd.DataFrame(out)
    f.to_csv(OUT / f"{name}.csv", index=False)
    wide = f.pivot_table(index=["fixture", "origin", "seed"], columns="arm", values=["a_offense", "b_offense", "margin"])
    diff = pd.DataFrame({k: wide[(k, arm)] - wide[(k, "reference")] for k in ("a_offense", "b_offense", "margin")})
    per_origin = diff.groupby(level=["fixture", "origin"]).mean()          # the two seeds averaged within origin
    stat = lambda d: (float(d.mean()), float(d.std(ddof=1) / np.sqrt(len(d))))
    lines = [f"{arm} minus seed-matched reference, seeds {seeds} averaged within origin; mean over origins (SE)"]
    for fixture, q in per_origin.groupby(level="fixture", sort=False):
        lines.append(f"  {fixture:<38} " + "  ".join(f"{k} {stat(q[k])[0]:+.1f} ({stat(q[k])[1]:.1f})"
                                                     for k in ("a_offense", "b_offense", "margin")))
    get = lambda fixture, k: stat(per_origin.xs(fixture, level="fixture")[k])[0]
    checks = {"five Goberts' offense <= +1": get("five_goberts|jokic_westbrook", "a_offense") <= 1,
              "legal centers' offense <= +1": get("legal_pure_centers|jokic_westbrook", "a_offense") <= 1,
              "Jokic/Westbrook's offense vs Goberts > 0": get("five_goberts|jokic_westbrook", "b_offense") > 0}
    lines += [f"criterion: {k}: {'pass' if v else 'FAIL'}" for k, v in checks.items()]
    text = "\n".join(lines)
    (OUT / f"{name}.txt").write_text(text)
    print(text)


def own_calibration(arms=("reference", "frozen_fixed"), seeds=(17, 23, 41), first=4, name="screen5b_own_calibration"):
    """Fifth screen, post hoc: accuracy when every arm, the reference included, is calibrated only by its
    own earlier 2022+ quarters (expanding, strictly before each scored quarter), so no arm borrows another's
    calibration. Scored quarters: the 20 origins after the first `first`. Points r2 on outer broad cells."""
    global SEED
    g, tags, rows = legacy.matchups(), origins().tag.tolist(), {}
    stops = origins().set_index("tag")
    out = []
    for seed in seeds:
        SEED = seed
        past = {a: [] for a in arms}
        for i, t in enumerate(tags):
            frame = rows.setdefault(t, legacy.row_frame(np.sort(legacy.quarter_rows(stops.loc[t], g)), g))
            league = league_of(t, len(frame), g)
            for a in arms:
                fc = pd.read_pickle(OUT / f"{stem(a)}_{t}_rows.pkl")
                assert np.array_equal(fc.row.to_numpy(), frame.row.to_numpy())
                native = fc.points.to_numpy()
                if i >= first:
                    cal = evaluate.affine(pd.concat(past[a], ignore_index=True), stops.loc[t].start)
                    c = evaluate.cells(frame.assign(cal=evaluate.calibrate(cal, native, league)), ["cal"])
                    c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
                    out.append(dict(seed=seed, origin=t, arm=a, slope=cal["slope"],
                                    r2=evaluate.metrics(evaluate.sufficient(c.actual, c.cal, c.possessions))["r2"]))
                past[a].append(evaluate.history_cells(frame, native, league, stops.loc[t].stop))
        print("own calibration, seed", seed, flush=True)
    SEED = DEFAULT_SEED
    f = pd.DataFrame(out)
    f.to_csv(OUT / f"{name}.csv", index=False)
    wide = f.pivot_table(index=["origin", "seed"], columns="arm", values=["r2", "slope"])
    lines = [f"own 2022+ calibration, quarters {tags[first]}-{tags[-1]}; arm minus reference, mean over quarters (SE)"]
    for a in arms[1:]:
        for seed in seeds:
            d = (wide[("r2", a)] - wide[("r2", "reference")]).xs(seed, level="seed")
            lines.append(f"  {a} seed {seed}: {d.mean():+.5f} ({d.std(ddof=1) / np.sqrt(len(d)):.5f}), positive "
                         f"{int((d > 0).sum())}/{len(d)}; mean slope {wide[('slope', a)].xs(seed, level='seed').mean():.3f} "
                         f"vs reference {wide[('slope', 'reference')].xs(seed, level='seed').mean():.3f}")
        d = (wide[("r2", a)] - wide[("r2", "reference")]).groupby(level="origin").mean()
        lines.append(f"  {a} seeds averaged within quarter: {d.mean():+.5f} ({d.std(ddof=1) / np.sqrt(len(d)):.5f}), "
                     f"positive {int((d > 0).sum())}/{len(d)}")
    text = "\n".join(lines)
    (OUT / f"{name}.txt").write_text(text)
    print(text)


def stacked_calibration(arm="frozen_fixed", seeds=(17, 23, 41), first=4, name="stacked_calibration"):
    """Post hoc, exploratory: how much of a frozen arm's module survives calibration on top, and at what cost.
    Every forecast is calibrated forward on its own earlier 2022+ quarters (scored: the quarters after `first`).
    Frozen arms share the reference's network, so module = arm - reference exactly. Variants:
      scale s     affine on network + s * module, per seed, then seeds averaged (the benchmark convention);
      stacked     (actual - league) = a + b (network - league) + c module, c fitted forward;
      seed-mean   the same on the three seeds' mean network and module;
      level-free  the module minus its possession-weighted mean over the quarter's rows. This uses which
                  lineups played (no outcomes), so it bounds what a legitimate centering could reach;
      previous / train  the module minus its level measured before the origin (`prior_level`), if saved.
    Kept = the module's printed weight relative to the network's (s, or c / b). Points r2 on outer broad cells."""
    global SEED
    g, tags, stops = legacy.matchups(), origins().tag.tolist(), origins().set_index("tag")
    data = {}
    for t in tags:
        frame = legacy.row_frame(np.sort(legacy.quarter_rows(stops.loc[t], g)), g)
        q = dict(tag=t, frame=frame, net={}, module={}, league={})
        for seed in seeds:
            SEED = seed
            q["league"][seed] = league_of(t, len(frame), g)
            net, full = (pd.read_pickle(OUT / f"{stem(a)}_{t}_rows.pkl") for a in ("reference", arm))
            assert np.array_equal(net.row.to_numpy(), frame.row.to_numpy()) and np.array_equal(full.row, net.row)
            q["net"][seed], q["module"][seed] = net.points.to_numpy(), full.points.to_numpy() - net.points.to_numpy()
        data[t] = q
    SEED = DEFAULT_SEED
    prior = pd.read_csv(OUT / "prior_level.csv").set_index(["origin", "seed", "where"]).level \
        if (OUT / "prior_level.csv").exists() else None

    def level_free(m, frame):
        return m - np.average(m, weights=frame.possessions.to_numpy(float))

    def run(design, pooled=False):
        """design(q, seed) -> (league, columns); the first column is the network-side forecast (minus league
        inside), the rest enter raw. Returns per-quarter r2 and the fitted coefficients."""
        groups = ["mean"] if pooled else list(seeds)
        past, r2s, coefs = {s: [] for s in groups}, [], []
        for i, t in enumerate(tags):
            q, preds = data[t], []
            for s in groups:
                if pooled:
                    designs = [design(q, x) for x in seeds]
                    league, cols = np.mean([d[0] for d in designs], 0), [np.mean(c, 0) for c in zip(*[d[1] for d in designs])]
                else:
                    league, cols = design(q, s)
                z = np.c_[cols[0] - league, np.stack(cols[1:], 1) if len(cols) > 1 else np.empty((len(league), 0))]
                if i >= first:
                    h = pd.concat(past[s], ignore_index=True)
                    sw = np.sqrt(h.possessions.to_numpy(float))
                    X = np.c_[np.ones(len(h)), h[[f"z{k}" for k in range(z.shape[1])]].to_numpy()]
                    b = np.linalg.lstsq(X * sw[:, None], (h.actual - h.league).to_numpy() * sw, rcond=None)[0]
                    preds.append(league + b[0] + z @ b[1:])
                    coefs.append(b)
                c = evaluate.cells(q["frame"].assign(league=league, **{f"z{k}": z[:, k] for k in range(z.shape[1])}),
                                   ["league"] + [f"z{k}" for k in range(z.shape[1])])
                past[s].append(c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS])
            if i >= first:
                c = evaluate.cells(q["frame"].assign(p=np.mean(preds, 0)), ["p"])
                c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
                r2s.append(evaluate.metrics(evaluate.sufficient(c.actual, c.p, c.possessions))["r2"])
        return np.array(r2s), np.array(coefs)

    variants = {f"scale {s:g}": (lambda s: lambda q, x: (q["league"][x], [q["net"][x] + s * q["module"][x]]))(s)
                for s in (0, .25, .5, 1)}
    variants |= {f"level-free scale {s:g}": (lambda s: lambda q, x: (
        q["league"][x], [q["net"][x] + s * level_free(q["module"][x], q["frame"])]))(s) for s in (.25, .5, 1)}
    if prior is not None:
        for where in ("previous", "train"):
            for s in (.5, 1):
                variants[f"{where}-centered scale {s:g}"] = (lambda s, where: lambda q, x: (
                    q["league"][x], [q["net"][x] + s * (q["module"][x] - prior[(q["tag"], x, where)])]))(s, where)
    stacked = lambda q, x: (q["league"][x], [q["net"][x], q["module"][x]])
    stacked_free = lambda q, x: (q["league"][x], [q["net"][x], level_free(q["module"][x], q["frame"])])
    runs = {k: run(v) for k, v in variants.items()}
    runs |= {"stacked": run(stacked), "stacked seed-mean": run(stacked, pooled=True),
             "level-free stacked": run(stacked_free), "level-free stacked seed-mean": run(stacked_free, pooled=True)}
    if prior is not None:
        for where in ("previous", "train"):
            design = (lambda where: lambda q, x: (q["league"][x], [q["net"][x], q["module"][x] - prior[(q["tag"], x, where)]]))(where)
            runs[f"{where}-centered stacked"] = run(design)
    base = runs["scale 0"][0]
    lines = [f"{arm}: forward calibration on own {ERA[0]}+ quarters, scored {tags[first]}-{tags[-1]} ({len(base)}); "
             f"reference r2 {base.mean():.4f}", "variant: r2 minus reference (SE over quarters); kept = module weight / network weight"]
    rows = []
    for k, (r2, b) in runs.items():
        d = r2 - base
        kept = float(np.mean(b[:, 2] / b[:, 1])) if k.endswith(("stacked", "seed-mean")) else float(k.split()[-1])
        rows.append(dict(variant=k, diff=d.mean(), se=d.std(ddof=1) / np.sqrt(len(d)), positive=int((d > 0).sum()), kept=kept))
        lines.append(f"  {k:<30} {d.mean():+.5f} ({d.std(ddof=1) / np.sqrt(len(d)):.5f}), positive {int((d > 0).sum())}/{len(d)}; "
                     f"kept {kept:.2f}")
    pd.DataFrame(rows).to_csv(OUT / f"{name}.csv", index=False)
    text = "\n".join(lines)
    (OUT / f"{name}.txt").write_text(text)
    print(text)


class _Part(torch.nn.Module):
    """A pair module with one side's output switched off (accounting split, not a causal effect)."""
    def __init__(self, pairs, keep):
        super().__init__()
        self.pairs, self.keep = pairs, keep

    def forward(self, batch):
        offense, defense = self.pairs(batch)
        return (offense if self.keep == "offense" else torch.zeros_like(offense),
                defense if self.keep == "defense" else torch.zeros_like(defense))


def level_diagnostic(arm="frozen_pure", name=None):
    """Sixth screen, post hoc: the arm's possession-weighted level shift vs the reference on each origin's
    outer rows, split into the offensive and the defensive pair terms, and the same on a sample of the
    origin's training rows (inputs as in training)."""
    torch.set_num_threads(THREADS)
    store, g = Store(), legacy.matchups()
    data, schedule = Rows(g, store), legacy.schedule()
    out = []
    for tag in origins().tag:
        origin = schedule[schedule.tag == tag].iloc[0]
        normalizer, env = store.normalizer(tag, "final"), store.env(tag, "final")
        models = load_models(arm, tag)
        full = [m.pairs for m in models]
        outer = np.sort(legacy.quarter_rows(origin, g))
        train = data.prefix(int(np.datetime64(origin.start, "D").astype(np.int64)), FitConfig().lookback_days)
        train = np.sort(np.random.default_rng(0).choice(train, 40000, replace=False))
        for where, rows, mode in (("outer", outer, dict(origin_index=int(origin.origin_index))), ("train", train, {})):
            w = np.asarray(g["possessions"][rows], float)
            level = {}
            for part in ("none", "offense", "defense", "both"):
                for m, pairs in zip(models, full):
                    m.pairs = None if part == "none" else pairs if part == "both" else _Part(pairs, part)
                pts = []
                with torch.no_grad():
                    for ix in game_batches(data.game, rows):
                        inputs = data.batch(ix, normalizer, **mode)[0]
                        pts.append((ix, average_ledgers([m.eval()(inputs, env) for m in models]).points100.double().numpy()))
                ids = np.concatenate([i for i, _ in pts])
                order = np.argsort(ids)
                level[part] = np.concatenate([p for _, p in pts])[order]
            for m, pairs in zip(models, full):
                m.pairs = pairs
            assert np.array_equal(np.sort(ids), rows)
            out.append(dict(origin=tag, where=where, **{k: float(np.average(level[k] - level["none"], weights=w))
                                                       for k in ("offense", "defense", "both")}))
        print("level", tag, flush=True)
    f = pd.DataFrame(out)
    name = name or f"level_diagnostic_{stem(arm)}"
    f.to_csv(OUT / f"{name}.csv", index=False)
    lines = [f"{stem(arm)}: possession-weighted level shift vs the module switched off (points/100)"]
    for where, q in f.groupby("where", sort=False):
        lines.append(f"  {where}: " + "  ".join(f"{k} mean {q[k].mean():+.2f} SD {q[k].std(ddof=1):.2f}"
                                               for k in ("offense", "defense", "both")))
    piv = f.pivot(index="origin", columns="where", values="both")
    lines.append(f"  corr(train level, outer level) over origins: {np.corrcoef(piv.train, piv.outer)[0, 1]:.2f}")
    text = "\n".join(lines)
    (OUT / f"{name}.txt").write_text(text)
    print(text)


def product_fixtures(arm="frozen_fixed", name="confirm", scales=(1, .5)):
    """The confirmation's pillar-2 bars on the product number: network + s (module - level on the previous
    quarter's rows). From `--confirm` output and `prior_level.csv`. A common shift moves both offenses and
    leaves the margin unchanged. Seed-matched reference; seeds averaged within origin, then origins averaged."""
    f = pd.read_csv(OUT / f"{name}.csv")
    level = pd.read_csv(OUT / "prior_level.csv").query("where == 'previous'").set_index(["origin", "seed"]).level
    wide = f.pivot_table(index=["fixture", "origin", "seed"], columns="arm", values=["a_offense", "b_offense", "margin"])
    shift = level.reindex(wide.index.droplevel("fixture")).to_numpy()
    stat = lambda d: (float(d.mean()), float(d.std(ddof=1) / np.sqrt(len(d))))
    lines = [f"{arm} product minus seed-matched reference over {wide.index.get_level_values('origin').nunique()} origins "
             f"(seeds averaged within origin), mean (SE)"]
    for s in (0,) + tuple(scales):
        raw = s == 0
        k = 1 if raw else s
        diff = pd.DataFrame({c: k * (wide[(c, arm)] - wide[(c, "reference")]) - (0 if raw or c == "margin" else s * shift)
                             for c in ("a_offense", "b_offense", "margin")})
        per_origin = diff.groupby(level=["fixture", "origin"]).mean()
        lines.append(f" {'raw module (s = 1, uncentered)' if raw else f'product, s = {s:g}'}")
        for fixture, q in per_origin.groupby(level="fixture", sort=False):
            lines.append(f"  {fixture:<38} " + "  ".join(f"{c} {stat(q[c])[0]:+.1f} ({stat(q[c])[1]:.1f})"
                                                         for c in ("a_offense", "b_offense", "margin")))
        if not raw:
            get = lambda fixture, c: stat(per_origin.xs(fixture, level="fixture")[c])[0]
            checks = {"five Goberts' offense <= +1": get("five_goberts|jokic_westbrook", "a_offense") <= 1,
                      "legal centers' offense <= +1": get("legal_pure_centers|jokic_westbrook", "a_offense") <= 1,
                      "Jokic/Westbrook's offense vs Goberts > 0": get("five_goberts|jokic_westbrook", "b_offense") > 0}
            lines += [f"  criterion (s = {s:g}): {c}: {'pass' if v else 'FAIL'}" for c, v in checks.items()]
    text = "\n".join(lines)
    (OUT / f"{name}_product.txt").write_text(text)
    print(text)


def prior_level(arm="frozen_fixed", seeds=(17, 23, 41), name="prior_level"):
    """Post hoc: each origin's module level (possession-weighted, module on minus off), measured only on rows
    known before the origin: the previous quarter's rows with inputs as of this origin, and a 40,000-row sample
    of the training window with inputs as in training. Used to center the module forward."""
    global SEED
    torch.set_num_threads(THREADS)
    store, g = Store(), legacy.matchups()
    data, schedule = Rows(g, store), legacy.schedule()
    out = []
    for seed in seeds:
        SEED = seed
        for tag in origins().tag:
            i = int(np.flatnonzero(schedule.tag.to_numpy() == tag)[0])
            origin, previous = schedule.iloc[i], schedule.iloc[i - 1]
            normalizer, env = store.normalizer(tag, "final"), store.env(tag, "final")
            models = load_models(arm, tag)
            full = [m.pairs for m in models]
            before = np.sort(legacy.quarter_rows(previous, g))
            train = data.prefix(int(np.datetime64(origin.start, "D").astype(np.int64)), FitConfig().lookback_days)
            train = np.sort(np.random.default_rng(0).choice(train, 40000, replace=False))
            for where, rows, mode in (("previous", before, dict(origin_index=int(origin.origin_index))),
                                      ("train", train, {})):
                w = np.asarray(g["possessions"][rows], float)
                level = {}
                for on in (False, True):
                    for m, pairs in zip(models, full):
                        m.pairs = pairs if on else None
                    pts = []
                    with torch.no_grad():
                        for ix in game_batches(data.game, rows):
                            inputs = data.batch(ix, normalizer, **mode)[0]
                            pts.append((ix, average_ledgers([m.eval()(inputs, env) for m in models]).points100.double().numpy()))
                    ids = np.concatenate([i for i, _ in pts])
                    assert np.array_equal(np.sort(ids), rows)
                    level[on] = np.concatenate([p for _, p in pts])[np.argsort(ids)]
                for m, pairs in zip(models, full):
                    m.pairs = pairs
                out.append(dict(origin=tag, seed=seed, where=where, level=float(np.average(level[True] - level[False], weights=w))))
            print("prior level", seed, tag, flush=True)
    SEED = DEFAULT_SEED
    pd.DataFrame(out).to_csv(OUT / f"{name}.csv", index=False)


def pilot(k):
    fit_arm("reward", PILOT_ORIGIN, k=k, out=OUT / "pilot", label=f"pilot_k{k}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--arm", choices=ARMS)
    p.add_argument("--origin")
    p.add_argument("--k", type=float)
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument("--era", type=int, nargs=2, help="first and last origin seasons (default 2022 2026)")
    p.add_argument("--out", help="output directory under the cache (default: the screens' directory)")
    p.add_argument("--pilot", type=float)
    p.add_argument("--summary", action="store_true")
    p.add_argument("--fixtures", action="store_true")
    p.add_argument("--properties", action="store_true")
    p.add_argument("--held-diagnostic", action="store_true")
    p.add_argument("--out-diagnostic", action="store_true")
    p.add_argument("--backbone-diagnostic", action="store_true")
    p.add_argument("--confirm", action="store_true")
    p.add_argument("--seeds", type=int, nargs="+", help="seeds for --confirm and --prior-level")
    p.add_argument("--own-calibration", action="store_true")
    p.add_argument("--level-diagnostic", action="store_true")
    p.add_argument("--stacked-calibration", action="store_true")
    p.add_argument("--prior-level", action="store_true")
    p.add_argument("--product-fixtures", action="store_true")
    p.add_argument("--arms", nargs="+", choices=ARMS)
    p.add_argument("--name", help="output file stem for --summary, --fixtures and --properties")
    a = p.parse_args()
    SEED = a.seed
    if a.era:
        ERA = tuple(a.era)
    if a.out:
        OUT = paths.CACHE / a.out
        OUT.mkdir(parents=True, exist_ok=True)
    named = lambda f, **kw: f(**kw, **({"arms": tuple(a.arms)} if a.arms else {}), **({"name": a.name} if a.name else {}))
    if a.summary:
        summary(**({"name": a.name} if a.name else {}))
    elif a.fixtures:
        named(fixture_sweep)
    elif a.properties:
        named(property_check)
    elif a.held_diagnostic:
        held_diagnostic()
    elif a.out_diagnostic:
        out_diagnostic()
    elif a.backbone_diagnostic:
        backbone_diagnostic()
    elif a.own_calibration:
        own_calibration()
    elif a.product_fixtures:
        product_fixtures(**({"name": a.name} if a.name else {}))
    elif a.prior_level:
        prior_level(**({"seeds": tuple(a.seeds)} if a.seeds else {}), **({"name": a.name} if a.name else {}))
    elif a.stacked_calibration:
        stacked_calibration(**({"arm": a.arms[0]} if a.arms else {}), **({"name": a.name} if a.name else {}))
    elif a.level_diagnostic:
        level_diagnostic(**({"arm": a.arms[0]} if a.arms else {}))
    elif a.confirm:
        confirm(**({"arm": a.arms[0]} if a.arms else {}), **({"name": a.name} if a.name else {}),
                **({"seeds": tuple(a.seeds)} if a.seeds else {}))
    elif a.pilot is not None:
        pilot(a.pilot)
    else:
        fit_arm(a.arm, a.origin, k=a.k, out=OUT)
