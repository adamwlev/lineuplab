"""Do familiar fives beat the forecast? (post hoc, exploratory; prompted by scripts/era_diagnostics.py)

Familiarity of a five = its possessions together (same five players, either
side) in the five years before the quarter's origin; it uses only data before
the origin, so it is available to a forward forecast. Residual = actual minus
the calibrated neural model alone (seed mean), points per 100, possession
weighted, with season-level SEs.

- 2016-2026: the reference J_POINT_BOTH, checkpoint average (primary benchmark rows);
- 2007-2013: the era backtest R and C (rows cached by scripts/era_diagnostics.py).

Forward correction (a prior-only screen of a familiarity layer): at each
quarter, regress earlier quarters' row residuals on an intercept and
indicators for the defensive five's familiarity bin (new fives are the
baseline), possession weighted; add only the bin effects to the forecast.
Scored on broad offense-five cells (>= 50 possessions per quarter): raw r^2
(pooled, as the scorecard) and centered r^2 (each quarter's mean error
removed), with per-season differences.

    PYTHONPATH=.:scripts python -u scripts/familiarity_check.py
"""
import numpy as np
import pandas as pd

from capacity_score import frames
from era_diagnostics import OUT as ERA_OUT, load
from lineups import evaluate, legacy
from lineups.evaluate import FIVE

LOOKBACK = 5 * 365
BINS, LABELS = [-1, 0, 49, 199, np.inf], ["0", "1-49", "50-199", "200+"]


def familiarity(f, g, start_of):
    """Prior possessions together of each row's offense five and defense five."""
    date = np.asarray(g["date"])
    off_fam, def_fam = np.zeros(len(f)), np.zeros(len(f))
    for tag, idx in f.groupby("origin").groups.items():
        start = start_of(tag)
        prior = np.flatnonzero((date < start) & (date >= start - LOOKBACK))
        n = np.asarray(g["possessions"][prior], float)
        both = np.r_[np.sort(np.asarray(g["pids"][prior]), 1), np.sort(np.asarray(g["defense"][prior]), 1)]
        units, inverse = np.unique(both, axis=0, return_inverse=True)
        total = np.bincount(inverse.ravel(), np.r_[n, n], len(units))
        lookup = pd.Series(total, index=pd.MultiIndex.from_arrays(units.T))
        i = f.index.get_indexer(idx)
        for cols, out in ((FIVE, off_fam), (legacy.DEFENSE, def_fam)):
            five = np.sort(f.loc[idx, cols].to_numpy(), 1)
            out[i] = lookup.reindex(pd.MultiIndex.from_arrays(five.T)).fillna(0.).to_numpy()
    return f.assign(off_fam=pd.cut(off_fam, BINS, labels=LABELS).astype(str),
                    def_fam=pd.cut(def_fam, BINS, labels=LABELS).astype(str), def_fam_poss=def_fam)


def forward_correction(f, forecast):
    """Prior-only familiarity effects added to `forecast`; returns the corrected column."""
    X = np.stack([(f.def_fam == level).to_numpy(float) for level in LABELS[1:]], 1)
    y = (f.actual - f[forecast]).to_numpy(float)
    w = f.possessions.to_numpy(float)
    order = f.origin.drop_duplicates().tolist()
    corrected = f[forecast].to_numpy(float).copy()
    coefficients = []
    for k, tag in enumerate(order):
        here = (f.origin == tag).to_numpy()
        prior = f.origin.isin(order[:k]).to_numpy()
        if not prior.any():
            continue
        A = np.c_[np.ones(prior.sum()), X[prior]] * np.sqrt(w[prior])[:, None]
        beta = np.linalg.lstsq(A, y[prior] * np.sqrt(w[prior]), rcond=None)[0]
        corrected[here] += X[here] @ beta[1:]
        coefficients.append(dict(origin=tag, **dict(zip(LABELS[1:], beta[1:]))))
    return corrected, pd.DataFrame(coefficients)


def accuracy(f, columns):
    """Per-season raw and centered r^2 on broad offense-five cells, and pooled values."""
    stats = []
    for (tag, season), q in f.groupby(["origin", "season"], sort=False):
        c = evaluate.cells(q, columns)
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        w, y = c.possessions.to_numpy(float), c.actual.to_numpy(float)
        for m in columns:
            e = y - c[m].to_numpy(float)
            stats.append(dict(origin=tag, season=season, model=m, sse_c=w @ (e - np.average(e, weights=w)) ** 2,
                              sst_c=w @ (y - np.average(y, weights=w)) ** 2,
                              **evaluate.sufficient(c.actual, c[m], c.possessions)))
    s = pd.DataFrame(stats)
    out = {}
    for m, t in s.groupby("model"):
        out[m] = dict(r2=evaluate.metrics(evaluate.pooled(t))["r2"], centered=1 - t.sse_c.sum() / t.sst_c.sum())
    per = s.groupby(["season", "model"]).apply(
        lambda t: pd.Series(dict(r2=evaluate.metrics(evaluate.pooled(t))["r2"], centered=1 - t.sse_c.sum() / t.sst_c.sum())),
        include_groups=False).unstack("model")
    return out, per


def report(name, f, base):
    f = f.copy()
    f["corrected"], coef = forward_correction(f, base)
    pooled, per = accuracy(f, [base, "corrected"])
    print(f"\n== forward familiarity correction, {name} ({base})")
    print("last coefficients:", coef.iloc[-1].to_dict())
    for k in ("r2", "centered"):
        d = per[k]["corrected"] - per[k][base]
        print(f"{k}: {pooled[base][k]:.4f} -> {pooled['corrected'][k]:.4f} (diff {pooled['corrected'][k] - pooled[base][k]:+.4f}); "
              f"per season mean {d.mean():+.4f} se {d.std(ddof=1) / np.sqrt(len(d)):.4f}, positive {(d > 0).sum()}/{len(d)}")
    return coef


def table(f, residuals):
    out = []
    for side in ("off_fam", "def_fam"):
        for level, s in f.groupby(side):
            rec = dict(side=side, level=level, possessions=float(s.possessions.sum()))
            for r in residuals:
                per = s.groupby("season").apply(lambda t: np.average(t[r], weights=t.possessions), include_groups=False)
                rec[r] = float(np.average(s[r], weights=s.possessions))
                rec[r + "_se"] = float(per.std(ddof=1) / np.sqrt(len(per)))
            out.append(rec)
    return pd.DataFrame(out)


def main():
    pd.set_option("display.width", 200, "display.precision", 2)
    g = legacy.matchups()
    starts = {o.tag: legacy.day(o.start) for o in legacy.origins().itertuples()}
    bench = frames(lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"), g)
    bench["actual"] = 100 * bench.points / bench.possessions
    bench["res_R"] = bench.actual - bench.calibrated
    bench = familiarity(bench, g, starts.get)
    print("== 2016-2026, reference, calibrated NN alone\n", table(bench, ["res_R"]).to_string(index=False))

    from era_run import origins
    era_starts = {o.tag: legacy.day(o.start) for o in origins().itertuples()}
    era = load([17, 23])
    era = familiarity(era.rename(columns={}), g, era_starts.get)
    print("\n== 2007-2013, era R and C, calibrated NN alone\n", table(era, ["res_R", "res_C"]).to_string(index=False))
    out = ERA_OUT / "familiarity"
    out.mkdir(parents=True, exist_ok=True)
    table(bench, ["res_R"]).to_csv(out / "benchmark_2016_2026.csv", index=False)
    table(era, ["res_R", "res_C"]).to_csv(out / "era_2007_2013.csv", index=False)
    era = era.rename(columns={"points_actual": "points"})
    report("2016-2026 benchmark", bench, "calibrated").to_csv(out / "coefficients_benchmark.csv", index=False)
    for arm in ("R", "C"):
        report("2007-2013 era", era, arm).to_csv(out / f"coefficients_era_{arm}.csv", index=False)


if __name__ == "__main__":
    main()
