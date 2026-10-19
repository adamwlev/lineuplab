"""Overall quality: each player's linear approximation strength (UI feature, Adam 2026-10-14).

Adam: users will want each player's linear strength, called "overall
quality", shown as an approximation since the model is nonlinear.

**Definition.** A player-season's overall quality is his coefficient in the
least-squares additive fit

    rating(five) ~ level + sum of the five players' qualities

of the network's calibrated ratings (arm R, network alone, against the
league-average panel). Offense and defense are fitted separately. Defense is
points allowed, so lower is better, and net is offense minus defense. The
fit runs over position-balanced random fives across all player-seasons
2002–2026: two guards, two wings and a big by listed position. ROUNDS
passes give every player-season about ROUNDS appearances, each rated
against OPPONENTS panel fives per side.

**Level.** The constants are set so that the real 2025–26 panel fives add
up on average. A typical 2025–26 player is about 0.

**Checks** on real fives held out of the level: 2025–26 fives with 50–99
possessions, and real 2016–17 and 2007–08 fives.

**Designs tried (2026-10-14).**
- Anchored swaps: a player's average change when replacing a same-position
  player in real 2025–26 fives. Worse on held-out lineups: mean absolute
  gap 1.6–2.2 points against 0.85–0.92 for this fit.
- This fit without the level step: biased by up to 8 points as-was, because
  random rosters from mixed eras are a different regime from real
  rotations.

    PYTHONPATH=. python -u scripts/player_values.py [--level-only]

Output: experiments/cache/player_values_2026_10_14/{values.npz, report.json}. --level-only reuses
the saved fit and recomputes the level and checks.
"""
import argparse
import os
import json
import time

import numpy as np
import torch
from scipy import sparse
from scipy.sparse.linalg import lsqr

from lineups import legacy, paths, players, release

OUT = release.SOURCE["values"]                 # the release's (lineups.release.DATA)
ROUNDS, OPPONENTS, SEED = 40, 6, 20261014
GUARD, BIG = 2.5, 4.0                     # listed position: guard <= 2.5 < wing < 4.0 <= big
PATTERN = ("guard", "guard", "wing", "wing", "big")
BATCH = 20000
HELD = ((2026, 50, 100, "held_2026_small"), (2017, 100, 10 ** 9, "held_2017"), (2008, 100, 10 ** 9, "held_2008"))
ERA_STORE = release.SOURCE["era_store"]


def buckets(rel):
    t = rel.seasons.table
    listing = rel.store.players["position"]
    pos = np.where(t["pid"] < len(listing), listing[np.minimum(t["pid"], len(listing) - 1)], listing.mean())
    return dict(guard=np.flatnonzero(pos <= GUARD), wing=np.flatnonzero((pos > GUARD) & (pos < BIG)),
                big=np.flatnonzero(pos >= BIG))


def lineups(groups, rng):
    """ROUNDS passes of position-balanced fives; within a pass each bucket is drawn without replacement, cycling."""
    n = sum(len(v) for v in groups.values())
    out = []
    for _ in range(ROUNDS):
        queues = {k: list(rng.permutation(v)) for k, v in groups.items()}
        for _ in range(n // 5):
            five = []
            for kind in PATTERN:
                q = queues[kind]
                while True:
                    if not q:
                        q.extend(rng.permutation(groups[kind]))
                    r = q.pop()
                    if r not in five:
                        five.append(r)
                        break
            out.append(five)
    return np.asarray(out, np.int64)


def points(rel, offense, defense):
    return np.concatenate([rel.season_points(offense[i:i + BATCH], defense[i:i + BATCH], "R")
                           for i in range(0, len(offense), BATCH)])


def ratings(rel, fives, rng):
    """Mean calibrated offense and points allowed of each five against OPPONENTS panel fives per side."""
    defenses, wd = rel.panel_rows["defense"]
    offenses, wo = rel.panel_rows["offense"]
    n = len(fives)
    pick_d = rng.choice(len(defenses), (n, OPPONENTS), p=wd)
    pick_o = rng.choice(len(offenses), (n, OPPONENTS), p=wo)
    off = np.repeat(fives, OPPONENTS, 0)
    offense = points(rel, off, defenses[pick_d.ravel()]).reshape(n, OPPONENTS).mean(1)
    defense = points(rel, offenses[pick_o.ravel()], off).reshape(n, OPPONENTS).mean(1)
    return offense, defense


def fit(fives, y, size):
    """Least squares y = mean + sum of qualities (one column per player-season); per-player SE."""
    n = len(fives)
    X = sparse.csr_matrix((np.ones(5 * n), (np.repeat(np.arange(n), 5), fives.ravel())), shape=(n, size))
    v = lsqr(X, y - y.mean(), atol=1e-10, btol=1e-10, iter_lim=5000)[0]
    resid = y - y.mean() - X @ v
    counts = np.bincount(fives.ravel(), minlength=size)
    return v, np.sqrt(resid.var() / np.maximum(counts, 1)), float(resid.std())


def real_fives(rel, season, lo, hi, rng, count=100):
    """Real offense fives of a season with lo <= possessions < hi (a sample), as player-season rows."""
    g = rel.matchups
    sched = rel.store.schedule().query("season == @season")
    if not len(sched):
        from lineups.features import Store
        sched = Store(ERA_STORE).schedule().query("season == @season")
    rows = np.flatnonzero((np.asarray(g["date"]) >= legacy.day(sched.start.min()))
                          & (np.asarray(g["date"]) < legacy.day(sched.stop.max())))
    fives = np.sort(np.asarray(g["pids"][rows]), 1)
    units, inverse = np.unique(fives, axis=0, return_inverse=True)
    poss = np.bincount(inverse.ravel(), np.asarray(g["possessions"][rows], float), len(units))
    keep = units[(poss >= lo) & (poss < hi)]
    pick = keep[rng.choice(len(keep), min(count, len(keep)), replace=False)]
    return rel.seasons.rows(pick, np.full(pick.shape, season))


def level_and_checks(rel, q, rng):
    """Constants so the 2025-26 panel fives add up on average (possession weights), and held-out checks."""
    anchors, weight = rel.panel_rows["offense"]
    exact = [rel.season_ratings(f, "R") for f in anchors]
    level = {side: float(weight @ (np.array([r[side] for r in exact]) - q[side][anchors].sum(1)))
             for side in ("offense", "defense")}
    checks = {}
    sets = {"anchors_2026": anchors} | {label: real_fives(rel, s, lo, hi, rng) for s, lo, hi, label in HELD}
    for label, fives in sets.items():
        net_x = np.array([rel.season_ratings(f, "R")["margin"] for f in fives]) if label != "anchors_2026" \
            else np.array([r["margin"] for r in exact])
        net_e = level["offense"] - level["defense"] + (q["offense"] - q["defense"])[fives].sum(1)
        gap = net_x - net_e
        checks[label] = dict(lineups=len(fives), corr=float(np.corrcoef(net_e, net_x)[0, 1]),
                             mean_gap=float(gap.mean()), mean_abs_gap=float(np.abs(gap).mean()),
                             p90_abs_gap=float(np.quantile(np.abs(gap), .9)))
    return level, checks


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--level-only", action="store_true", help="reuse the saved fit; recompute level and checks")
    a = p.parse_args()
    torch.set_num_threads(int(os.environ.get("LINEUPS_THREADS", 8)))      # (the refresh: 1)
    OUT.mkdir(parents=True, exist_ok=True)
    saved = dict(np.load(OUT / "values.npz")) if a.level_only else {}
    report, arrays = {}, {}
    for rule in players.RULES:
        tick = time.time()
        rel = release.Release(arms=("R",), rule=rule)
        t = rel.seasons.table
        size = len(t["pid"])
        rng = np.random.default_rng(SEED)
        if a.level_only:
            q = {side: saved[f"{rule}_{side}"].astype(float) for side in ("offense", "defense")}
            se = {side: saved[f"{rule}_{side}_se"] for side in ("offense", "defense")}
            appearances, fit_report = saved[f"{rule}_appearances"], {}
        else:
            fives = lineups(buckets(rel), rng)
            offense, defense = ratings(rel, fives, rng)
            q, se, fit_report = {}, {}, dict(lineups=int(len(fives)), rows=int(len(fives) * OPPONENTS * 2))
            for side, y in (("offense", offense), ("defense", defense)):
                v, s, sd = fit(fives, y, size)
                latest = (t["season"] == rel.seasons.latest) * t["offense_possessions"]
                q[side], se[side] = v - latest @ v / latest.sum(), s
                fit_report[f"{side}_residual_sd"] = sd
            appearances = np.bincount(fives.ravel(), minlength=size)
        level, checks = level_and_checks(rel, q, np.random.default_rng(SEED + 1))
        for side in ("offense", "defense"):
            arrays[f"{rule}_{side}"] = np.asarray(q[side], np.float32)
            arrays[f"{rule}_{side}_se"] = np.asarray(se[side], np.float32)
        arrays[f"{rule}_appearances"] = np.asarray(appearances, np.int32)
        arrays[f"{rule}_level"] = np.array([level["offense"], level["defense"]], np.float32)
        report[rule] = dict(fit_report, level=level, checks=checks, seconds=round(time.time() - tick),
                            median_se={side: float(np.median(se[side])) for side in se})
        print(rule, json.dumps(report[rule]), flush=True)
    np.savez(OUT / "values.npz", pid=t["pid"], season=t["season"], **arrays)
    (OUT / "report.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
