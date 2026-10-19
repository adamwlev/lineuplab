"""How much do seed and variant ensembles add? (exploratory, 2026-10-12)

The calibrated neural model alone, broad offense-five cells (at least 50
possessions), points per 100, raw and centered (within-quarter) r². Each seed is
calibrated by its own prior-only affine, as in the scorecards. Columns:

    R17, R23, R41   reference architecture, one seed (each a five-checkpoint mixture)
    R               the three-seed mean (the reported forecast)
    C               capacity v2, three-seed mean
    RC              the mean of R and C (a two-variant ensemble)

Benchmark 2016-2026: the history of the active cache root (lineups.history): the saved v16 reference and the
confirmatory capacity run under the main cache, the 2026-10-16 refits under the clean root.
Era 2007-2013: the era backtest fits (R and C, two-phase from scratch).

    PYTHONPATH=.:scripts python -u scripts/ensemble_check.py
"""
import numpy as np
import pandas as pd

import era_run
from era_score import FIRST_SCORED
from lineups import evaluate, history, legacy, paths
from lineups.history import league_at

OUT = paths.CACHE / "ensemble_check_2026_10_12"
SEEDS = legacy.SEEDS


def forecast(path, view="checkpoint_average"):
    with np.load(path) as z:
        return z["row"].copy(), z[view].astype(float)


def sources(era):
    if era:
        return dict(R=lambda o, s: forecast(era_run.case_dir(o.tag, "R", s) / "forecast.npz"),
                    C=lambda o, s: forecast(era_run.case_dir(o.tag, "C", s) / "forecast.npz"))
    return dict(R=lambda o, s: history.native(o.tag, s, "checkpoint_average", "R"),     # lineups.history: the root's
                C=lambda o, s: history.native(o.tag, s, "checkpoint_average", "C"))     # 2015-2026 history


def rows(era, arms=("R", "C")):
    """Benchmark rows; arms=("R",) (2026-10-16, the refresh's era rows) leaves out C and RC."""
    g = legacy.matchups()
    schedule = era_run.origins() if era else legacy.origins()
    first = FIRST_SCORED if era else 2016
    native = {a: f for a, f in sources(era).items() if a in arms}
    history = {(a, s): [] for a in native for s in SEEDS}
    out = []
    for o in schedule.itertuples():
        f = legacy.row_frame(legacy.quarter_rows(o, g), g)
        league = np.full(len(f), league_at(g, legacy.day(o.start)))      # = the saved controls' league
        cal = {}
        for a, get in native.items():
            for s in SEEDS:
                ids, p = get(o, s)
                if not np.array_equal(ids, f.row.to_numpy()):
                    raise ValueError(f"row mismatch {o.tag}/{a}/s{s}")
                h = pd.concat(history[(a, s)], ignore_index=True) if history[(a, s)] else None
                cal[(a, s)] = evaluate.calibrate(evaluate.affine(h, o.start), p, league)
                history[(a, s)].append(evaluate.history_cells(f, p, league, o.stop))
        if o.season < first:
            continue
        cols = {f"R{s}": cal[("R", s)] for s in SEEDS}
        cols["R"] = np.mean([cal[("R", s)] for s in SEEDS], 0)
        if "C" in native:
            cols["C"] = np.mean([cal[("C", s)] for s in SEEDS], 0)
            cols["RC"] = .5 * (cols["R"] + cols["C"])
        out.append(f.assign(origin=o.tag, season=int(o.season), **cols))
    return pd.concat(out, ignore_index=True)


COLUMNS = ["R17", "R23", "R41", "R", "C", "RC"]


def season_scores(frame):
    """Per-season raw r² (pooled sufficient statistics, as the scorecards) and centered r² (within quarter)."""
    recs = []
    for (tag, season), f in frame.groupby(["origin", "season"], sort=False):
        c = evaluate.cells(f, [m for m in COLUMNS if m in f])      # the era rows may hold arm R alone
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        w, y = c.possessions.to_numpy(float), c.actual.to_numpy(float)
        sst = w @ (y - np.average(y, weights=w)) ** 2
        for m in [m for m in COLUMNS if m in c]:
            e = y - c[m].to_numpy(float)
            recs.append(dict(season=season, model=m, sse_c=w @ (e - np.average(e, weights=w)) ** 2, sst=sst,
                             **evaluate.sufficient(y, c[m], w)))
    t = pd.DataFrame(recs)
    raw = lambda g: evaluate.metrics(evaluate.pooled(g))["r2"]
    centered = lambda g: 1 - g.sse_c.sum() / g.sst.sum()
    per = pd.DataFrame({k: t.groupby(["season", "model"]).apply(f, include_groups=False)
                        for k, f in (("raw", raw), ("centered", centered))})
    pooled = pd.DataFrame({k: t.groupby("model").apply(f, include_groups=False)
                           for k, f in (("raw", raw), ("centered", centered))})
    return per, pooled


def report(name, frame):
    per, pooled = season_scores(frame)
    print(f"\n== {name}: pooled r² (calibrated network alone)")
    print(pooled.loc[[m for m in COLUMNS if m in pooled.index]].round(5).to_string())
    for a, b in [(a, b) for a, b in (("R", "R17"), ("R", "R23"), ("R", "R41"), ("RC", "R"), ("C", "R"))
                 if a in pooled.index]:
        for kind in ("raw", "centered"):
            d = per[kind].unstack()[a] - per[kind].unstack()[b]
            print(f"{a} - {b:3s} {kind:8s}: {pooled.loc[a, kind] - pooled.loc[b, kind]:+.5f} "
                  f"(season mean {d.mean():+.5f} ± {d.std(ddof=1) / np.sqrt(len(d)):.5f}, {int((d > 0).sum())}/{len(d)} seasons)")
    single = pooled.loc[["R17", "R23", "R41"]]
    print(f"mean single seed: raw {single.raw.mean():.5f}, centered {single.centered.mean():.5f}")


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--era-arms", nargs="+", choices=("R", "C"), default=["R", "C"],
                   help="arms of the era rows (R alone for the refresh on the clean data)")
    a = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for era in (False, True):
        name = "era 2007-2013" if era else "benchmark 2016-2026"
        path = OUT / f"{'era' if era else 'benchmark'}.pkl"
        if not path.exists():
            rows(era, tuple(a.era_arms) if era else ("R", "C")).to_pickle(path)
        frame = pd.read_pickle(path)
        report(name, frame)


if __name__ == "__main__":
    main()
