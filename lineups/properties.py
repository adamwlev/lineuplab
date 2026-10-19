"""Directional property suite for hypothetical lineups (pillar 2).

Each property perturbs real lineups in a basketball-meaningful way and states
the direction the forecast must move. Directions were declared before any model
was run on the suite (2026-10-09). A property constrains the sign or shape of a
change, never which lineup wins.

Every case reports a ``violation``: how far the change goes in the forbidden
direction (positive is bad). A case passes when the violation is at most the
property's tolerance.

Offense properties (against a neutral defense):

    spacing_rim         Replace the lineup's top shooter (3PA rate >= 5/100) by
                        the non-shooter (< 1/100) nearest in usage. No teammate's
                        rim make probability may rise.  [per teammate, tol .002]
    handler_turnovers   Replace the top passer (assist rate) by the low-assist
                        player (bottom quartile) nearest in usage. Team
                        turnovers per possession may not fall.  [tol .001]
    handler_conversion  Same swap. The other four's attempt-weighted make
                        probability may not rise.  [tol .002]
    handler_teammate_turnovers
                        Same swap. The other four's turnovers per possession may
                        not fall.  [tol .001]  Added after the first run (post
                        hoc): handler_turnovers mixes this teammate effect with
                        the incoming player's own lower turnover rate.
    clone_synergy       Copies of the lineup's highest-usage player replace the
                        other slots, lowest usage first. Replacing k slots at once
                        may not gain more points than the k single replacements
                        added up (one ball: duplicates have no synergy).
                        [k = 2..4, tol 0.5 points/100]

Defense properties (against a fixed panel of real offenses):

    rim_synergy         The three lowest-block defenders are replaced by distinct
                        rim protectors (height >= 82 in, top-decile blocks).
                        Adding k at once may not lower opponent rim make by more
                        than the k single additions added up (one rim).
                        [k = 2..3, tol .002]
    rebound_synergy     Same with top-decile defensive rebounders (height >= 82
                        in), lowest-rebounding slots first; metric is opponent
                        offensive capture.  [k = 2..3, tol .002]

    The three synergy properties replace ladder versions used in the first run,
    which compared successive marginal steps. Those mixed the copy count with
    which player was replaced and, on defense, added newcomers best-first, so an
    additive model could pass or fail by construction.
    perimeter_coverage  Replace the shortest defender by a non-spacing big (height
                        >= 83 in, 3PA rate < 1/100, median blocks among such bigs).
                        Opponent three-point make probability may not fall.  [tol .002]
    coverage_targeting  Same swap. The opponent's shooters must gain more in
                        three-point make probability than its non-shooters.
                        (Broadcast defenses cannot pass this by construction;
                        it marks whether coverage structure exists.)  [tol 0]

Invariance:

    permutation         Reordering offense and defense slots does not change
                        team points.  [tol .001 points/100]

Roles use origin-dated information only: offensive states (3PA rate, assist
rate, usage), defensive descriptors (blocks, defensive rebounds) and listed
height (nba.players). A predictor is any callable ``predict(offense[B,5], defense[B,5] |
None)`` returning a ledger (lineups.model fields); None is the neutral defense.
"""
import numpy as np
import pandas as pd
import torch

from lineups import db, legacy

TOLERANCE = dict(spacing_rim=.002, handler_turnovers=.001, handler_conversion=.002, handler_teammate_turnovers=.001,
                 clone_synergy=.5, rim_synergy=.002, rebound_synergy=.002, perimeter_coverage=.002,
                 coverage_targeting=0., permutation=.001)
SHOOTER, NON_SHOOTER, BIG = 5., 1., 82
CHUNK = 8192


# ---- roles ------------------------------------------------------------------
def roles(store, origin_tag, pids):
    """Per-player role table at an origin (players without an origin state are dropped)."""
    origin = store.schedule().query("tag == @origin_tag").iloc[0]
    pids = np.unique(np.asarray(pids, np.int64))
    t = store.offense_origins
    known = np.isin(pids, t["pid"][t["origin_index"] == origin.origin_index])
    pids = pids[known]
    base = store.offense(pids, origin_index=int(origin.origin_index))["base"].astype(float)
    loc = np.exp(base[:, 3:9] - base[:, 3:9].max(1, keepdims=True))
    loc /= loc.sum(1, keepdims=True)
    rate = np.exp(np.clip(base[:, :3], -12, 4))
    defense = store.defense(pids, origin_index=int(origin.origin_index)).astype(float)
    height = db.heights().reindex(pids).to_numpy()
    return pd.DataFrame(dict(three_rate=100 * rate[:, 0] * loc[:, 4:].sum(1),
                             assist_rate=100 * np.exp(np.clip(base[:, 16], -12, 4)),
                             usage=rate[:, 0] + .44 * rate[:, 1] + rate[:, 2],
                             height=height, block=defense[:, 1], drb=defense[:, 2]), index=pids)


def nearest(pool, target_usage, exclude):
    """Pool player nearest in usage, excluding the lineup's own players."""
    pool = pool[~pool.index.isin(exclude)]
    return int((pool.usage - target_usage).abs().idxmin())


# ---- ledger summaries ---------------------------------------------------------
def predict_all(predict, offense, defense=None):
    """Evaluate in chunks and concatenate the fields the suite reads."""
    out = {k: [] for k in ("points100", "make", "attempts", "makes", "turnover", "turnovers", "capture")}
    for i in range(0, len(offense), CHUNK):
        p = predict(offense[i:i + CHUNK], None if defense is None else defense[i:i + CHUNK])
        out["points100"].append(p.points100.double())
        out["make"].append(p.make.double())
        out["attempts"].append(p.expected_attempts.double())
        out["makes"].append(p.expected_makes.double())
        out["turnover"].append(p.turnover.double().sum(1))
        out["turnovers"].append(p.turnover.double())
        out["capture"].append(p.rebound_log_prob.double()[:, :5].exp().sum(1))
    return {k: torch.cat(v).numpy() for k, v in out.items()}


def synergy_cases(five, slots, newcomers):
    """Base, each single replacement, then the first k replaced together (k >= 2)."""
    rows = [five.copy()]
    for slot, pid in zip(slots, newcomers):
        one = five.copy()
        one[slot] = pid
        rows.append(one)
    for k in range(2, len(slots) + 1):
        joint = five.copy()
        joint[list(slots[:k])] = newcomers[:k]
        rows.append(joint)
    return rows


def synergy(metric, n_slots):
    """metric: [cases, 1 + n + (n - 1)] laid out as synergy_cases; joint(k) - sum of singles, k = 2..n."""
    single = metric[:, 1:1 + n_slots] - metric[:, :1]
    joint = metric[:, 1 + n_slots:] - metric[:, :1]
    return joint - np.cumsum(single, 1)[:, 1:]


def weighted_make(p, players, locations):
    """Attempt-weighted make probability over the given player mask [B,5] and location slice."""
    att = (p["attempts"][:, :, locations] * players[:, :, None]).sum((1, 2))
    mk = (p["makes"][:, :, locations] * players[:, :, None]).sum((1, 2))
    return mk / np.maximum(att, 1e-12)


# ---- properties ---------------------------------------------------------------
def offense_cases(lineups, table):
    """Swaps for the offense properties: (kind, base row, swapped row, slot)."""
    non_shooters = table[table.three_rate < NON_SHOOTER]
    low_assist = table[table.assist_rate <= table.assist_rate.quantile(.25)]
    cases = []
    for i, five in enumerate(lineups):
        r = table.reindex(five)
        if r.usage.isna().any():
            continue
        top = int(np.argmax(r.three_rate.to_numpy()))
        if r.three_rate.iloc[top] >= SHOOTER:
            swapped = five.copy()
            swapped[top] = nearest(non_shooters, r.usage.iloc[top], five)
            cases.append(("spacing", i, five, swapped, top))
        passer = int(np.argmax(r.assist_rate.to_numpy()))
        swapped = five.copy()
        swapped[passer] = nearest(low_assist, r.usage.iloc[passer], five)
        cases.append(("handler", i, five, swapped, passer))
    return cases


def run_offense(predict, lineups, table):
    cases = offense_cases(lineups, table)
    base = np.array([c[2] for c in cases])
    swapped = np.array([c[3] for c in cases])
    p0, p1 = predict_all(predict, base), predict_all(predict, swapped)
    others = np.ones((len(cases), 5))
    others[np.arange(len(cases)), [c[4] for c in cases]] = 0
    conversion = weighted_make(p1, others, slice(0, 6)) - weighted_make(p0, others, slice(0, 6))
    rows = []
    for j, (kind, i, five, new, slot) in enumerate(cases):
        if kind == "spacing":
            for t in np.flatnonzero(others[j]):
                rows.append(dict(property="spacing_rim", lineup=i, detail=int(five[t]),
                                 violation=p1["make"][j, t, 0] - p0["make"][j, t, 0]))
        else:
            rows.append(dict(property="handler_turnovers", lineup=i, detail=int(new[slot]),
                             violation=p0["turnover"][j] - p1["turnover"][j]))
            rows.append(dict(property="handler_conversion", lineup=i, detail=int(new[slot]),
                             violation=conversion[j]))
            rows.append(dict(property="handler_teammate_turnovers", lineup=i, detail=int(new[slot]),
                             violation=(p0["turnovers"][j] * others[j]).sum() - (p1["turnovers"][j] * others[j]).sum()))
    # Clone synergy: copies of the highest-usage player, lowest-usage slots first.
    stacks, owners = [], []
    for i, five in enumerate(lineups):
        r = table.reindex(five)
        if r.usage.isna().any():
            continue
        order = np.argsort(r.usage.to_numpy())
        stacks += synergy_cases(five, order[:4], [five[order[-1]]] * 4)
        owners.append(i)
    points = predict_all(predict, np.array(stacks))["points100"].reshape(len(owners), -1)
    for n, extra in enumerate(synergy(points, 4)):
        for k, value in enumerate(extra, start=2):
            rows.append(dict(property="clone_synergy", lineup=owners[n], detail=k, violation=value))
    return rows


def run_defense(predict, defenses, panel, table):
    eligible = table.dropna(subset=["height"])
    protectors = eligible[(eligible.height >= BIG) & (eligible.block >= eligible.block.quantile(.9))]
    rebounders = eligible[(eligible.height >= BIG) & (eligible.drb >= eligible.drb.quantile(.9))]
    bigs = eligible[(eligible.height >= BIG + 1) & (eligible.three_rate < NON_SHOOTER)]
    plug = int((bigs.block - bigs.block.median()).abs().idxmin())
    shooter = (table.reindex(panel.ravel()).three_rate.to_numpy().reshape(panel.shape) >= SHOOTER)

    def opponent(defense_rows):
        """Each defense against every panel offense: [D, P] ledgers flattened."""
        d = np.repeat(defense_rows, len(panel), 0)
        o = np.tile(panel, (len(defense_rows), 1))
        return predict_all(predict, o, d)

    rows = []
    for name, stock, field in (("rim_synergy", protectors.sort_values("block", ascending=False), "block"),
                               ("rebound_synergy", rebounders.sort_values("drb", ascending=False), "drb")):
        stacks, owners = [], []
        for i, five in enumerate(defenses):
            r = table.reindex(five)
            add = [int(p) for p in stock.index if p not in five][:3]
            if r[field].isna().any() or len(add) < 3:
                continue
            stacks += synergy_cases(five, np.argsort(r[field].to_numpy())[:3], add)
            owners.append(i)
        p = opponent(np.array(stacks))
        if name == "rim_synergy":
            metric = weighted_make(p, np.ones((len(p["points100"]), 5)), slice(0, 1))
        else:
            metric = p["capture"]
        metric = metric.reshape(len(owners), -1, len(panel)).mean(2)
        for n, extra in enumerate(synergy(metric, 3)):
            for k, value in enumerate(extra, start=2):    # joint more negative than the singles: violation
                rows.append(dict(property=name, lineup=owners[n], detail=k, violation=-value))
    # Perimeter coverage: the shortest defender replaced by a non-spacing big.
    base, swapped, owners = [], [], []
    for i, five in enumerate(defenses):
        r = table.reindex(five)
        if r.height.isna().any() or plug in five:
            continue
        new = five.copy()
        new[int(np.argmin(r.height.to_numpy()))] = plug
        base.append(five)
        swapped.append(new)
        owners.append(i)
    p0, p1 = opponent(np.array(base)), opponent(np.array(swapped))
    every = np.ones((len(p0["points100"]), 5))
    three = slice(4, 6)
    change = (weighted_make(p1, every, three) - weighted_make(p0, every, three)).reshape(len(owners), -1).mean(1)
    sh = np.tile(shooter, (len(owners), 1)).astype(float)
    gain_sh = weighted_make(p1, sh, three) - weighted_make(p0, sh, three)
    gain_non = weighted_make(p1, 1 - sh, three) - weighted_make(p0, 1 - sh, three)
    targeting = (gain_sh - gain_non).reshape(len(owners), -1).mean(1)
    for n, i in enumerate(owners):
        rows.append(dict(property="perimeter_coverage", lineup=i, detail=plug, violation=-change[n]))
        rows.append(dict(property="coverage_targeting", lineup=i, detail=plug, violation=-targeting[n]))
    return rows


def run_permutation(predict, offense, defense, seed=0):
    """Each base offense against a randomly drawn base defense, slots shuffled."""
    rng = np.random.default_rng(seed)
    defense = defense[rng.integers(len(defense), size=len(offense))]
    perm_o = np.array([rng.permutation(x) for x in offense])
    perm_d = np.array([rng.permutation(x) for x in defense])
    a = predict_all(predict, offense, defense)["points100"]
    b = predict_all(predict, perm_o, perm_d)["points100"]
    return [dict(property="permutation", lineup=i, detail=0, violation=abs(a[i] - b[i])) for i in range(len(a))]


def run(predict, store, origin_tag, offense, defense, panel):
    """All properties at one origin.

    offense/defense: [N,5] real fives that serve as base lineups; panel: [P,5]
    real offenses that attack the perturbed defenses.
    """
    table = roles(store, origin_tag, np.concatenate([offense.ravel(), defense.ravel(), panel.ravel()]))
    rows = run_offense(predict, offense, table) + run_defense(predict, defense, panel, table)
    rows += run_permutation(predict, offense, defense)
    frame = pd.DataFrame(rows)
    frame["passed"] = frame.violation <= frame.property.map(TOLERANCE)
    return frame


def summarize(frame):
    g = frame.groupby("property", sort=False)
    return pd.DataFrame(dict(cases=g.size(), pass_rate=g.passed.mean(), median_violation=g.violation.median(),
                             p90_violation=g.violation.quantile(.9), tolerance=pd.Series(TOLERANCE)))\
        .dropna(subset=["cases"])
