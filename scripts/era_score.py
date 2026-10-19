"""Score the era backtest (protocol: reports/era_backtest_protocol_2026_10_12.md). Frozen with the protocol.

Forecasts: each arm's checkpoint-average native forecast, calibrated per seed
by the prior-only affine on earlier era quarters' broad cells, then averaged
over the seeds complete for both arms at every origin. League is the decayed
league scoring rate before each origin (365-day half-life). The neural model
is used alone; there is no additive control in this era.

Scored quarters: 2007q1-2013q4 (2006 is calibration warmup).

Primary:
1. Big-defense gradient. For each model, the possession-weighted residual
   (actual - forecast, points per 100) on rows whose defense has three or more
   bigs (listed height 82+ in) minus that on rows with at most one big. A model
   that is right about big defenses has a gradient near zero. Reported: each
   model's gradient and C - R, with season-level SEs (7 seasons).
2. Accuracy non-inferiority, C vs R, on broad offense-five cells (>= 50
   possessions per quarter):
   - raw r^2 as in the main scorecard (pooled sufficient statistics, variance
     around the pooled mean);
   - centered r^2, within quarter: 1 - sum of SSE after removing each quarter's
     mean error, over the sum of within-quarter variances.
   Season SE from per-season differences. Non-inferior if difference - 1.943 x
   SE > -0.003 (t, 6 df).

Secondary: residuals by defensive big count (0, 1, 2, 3+); per-season tables.

    PYTHONPATH=. python -u scripts/era_score.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from era_run import ARMS, OUT as RUN, SEEDS, case_dir, origins  # noqa: E402

from lineups import db, evaluate, legacy  # noqa: E402
from lineups.history import league_at  # noqa: E402,F401  (re-exported for the era scripts)

OUT = RUN / "score"
BIG = 82
FIRST_SCORED = 2007
T_6DF = 1.943


def native(tag, arm, seed):
    with np.load(case_dir(tag, arm, seed) / "forecast.npz") as z:
        return z["row"].copy(), z["checkpoint_average"].astype(float)


def r2s(cells, column):
    w, y = cells.possessions.to_numpy(float), cells.actual.to_numpy(float)
    e = y - cells[column].to_numpy(float)
    sst = w @ (y - np.average(y, weights=w)) ** 2
    return dict(sse=float(w @ e ** 2), sse_c=float(w @ (e - np.average(e, weights=w)) ** 2), sst=float(sst))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    g, heights = legacy.matchups(), db.heights()
    era = origins()
    seeds = [s for s in SEEDS if all((case_dir(t, a, s) / "complete.json").exists() for t in era.tag for a in ARMS)]
    if not seeds:
        raise SystemExit("no seed is complete for both arms at every origin")
    print("seeds", seeds, flush=True)
    history = {(a, s): [] for a in ARMS for s in seeds}
    rows_out, cell_stats = [], []
    for o in era.itertuples():
        rows = legacy.row_frame(legacy.quarter_rows(o, g), g)
        league = np.full(len(rows), league_at(g, legacy.day(o.start)))
        calibrated = {a: [] for a in ARMS}
        for a in ARMS:
            for s in seeds:
                ids, p = native(o.tag, a, s)
                if not np.array_equal(ids, rows.row.to_numpy()):
                    raise ValueError(f"row mismatch {o.tag}/{a}/s{s}")
                h = pd.concat(history[(a, s)], ignore_index=True) if history[(a, s)] else None
                calibrated[a].append(evaluate.calibrate(evaluate.affine(h, o.start), p, league))
                history[(a, s)].append(evaluate.history_cells(rows, p, league, o.stop))
        if o.season < FIRST_SCORED:
            continue
        f = rows.assign(R=np.mean(calibrated["R"], 0), C=np.mean(calibrated["C"], 0), season=int(o.season),
                        origin=o.tag)
        dh = heights.reindex(f[legacy.DEFENSE].to_numpy().ravel()).to_numpy().reshape(-1, 5)
        f["def_bigs"] = (dh >= BIG).sum(1)
        rows_out.append(f[["season", "origin", "possessions", "points", "R", "C", "def_bigs"]])
        c = evaluate.cells(f, ["R", "C"])
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        for a in ARMS:
            cell_stats.append(dict(origin=o.tag, season=int(o.season), arm=a, **r2s(c, a),
                                   **evaluate.sufficient(c.actual, c[a], c.possessions)))
    rows = pd.concat(rows_out, ignore_index=True)
    rows["actual"] = 100 * rows.points / rows.possessions
    cs = pd.DataFrame(cell_stats)

    # 1. Big-defense gradient.
    def residual(f, a):
        return np.average(f.actual - f[a], weights=f.possessions)
    group = np.select([rows.def_bigs <= 1, rows.def_bigs >= 3], ["0-1", "3+"], "2")
    per_season = []
    for season, f in rows.groupby("season"):
        gs = group[rows.season.to_numpy() == season]
        rec = dict(season=season)
        for a in ARMS:
            rec[a] = residual(f[gs == "3+"], a) - residual(f[gs == "0-1"], a)
        rec["C-R"] = rec["C"] - rec["R"]
        per_season.append(rec)
    ps = pd.DataFrame(per_season)
    gradient = {k: dict(estimate=float(residual(rows[group == "3+"], k) - residual(rows[group == "0-1"], k)),
                        season_se=float(ps[k].std(ddof=1) / np.sqrt(len(ps)))) for k in ARMS}
    gradient["C-R"] = dict(estimate=gradient["C"]["estimate"] - gradient["R"]["estimate"],
                           season_se=float(ps["C-R"].std(ddof=1) / np.sqrt(len(ps))))
    by_bigs = []
    for b, f in rows.groupby(rows.def_bigs.clip(upper=3)):
        per = f.groupby("season").apply(lambda s: pd.Series({a: residual(s, a) for a in ARMS}), include_groups=False)
        by_bigs.append(dict(def_bigs="3+" if b == 3 else str(b), possessions=float(f.possessions.sum()),
                            **{a: float(residual(f, a)) for a in ARMS},
                            **{f"{a}_se": float(per[a].std(ddof=1) / np.sqrt(len(per))) for a in ARMS}))

    # 2. Accuracy.
    def scores(t):
        return dict(r2=evaluate.metrics(evaluate.pooled(t))["r2"], centered_r2=1 - t.sse_c.sum() / t.sst.sum())
    pooled = {a: scores(cs[cs.arm == a]) for a in ARMS}
    season = pd.DataFrame([dict(season=s, arm=a, **scores(t)) for (s, a), t in cs.groupby(["season", "arm"])])
    wide = season.pivot(index="season", columns="arm", values=["r2", "centered_r2"])
    accuracy = {}
    for k in ("r2", "centered_r2"):
        d = wide[k]["C"] - wide[k]["R"]
        est = pooled["C"][k] - pooled["R"][k]
        se = float(d.std(ddof=1) / np.sqrt(len(d)))
        accuracy[k] = dict(R=pooled["R"][k], C=pooled["C"][k], difference=est, season_se=se,
                           lower=est - T_6DF * se, non_inferior=bool(est - T_6DF * se > -0.003),
                           per_season={int(s): float(v) for s, v in d.items()}, seasons_positive=int((d > 0).sum()))
    result = dict(seeds=seeds, scored_quarters=int(cs.origin.nunique()), cells=int(cs[cs.arm == "R"].n.sum()),
                  big_defense_gradient=gradient, gradient_per_season=ps.to_dict("records"),
                  residual_by_defensive_bigs=by_bigs, accuracy=accuracy)
    (OUT / "result.json").write_text(json.dumps(result, indent=1, default=float))
    print(json.dumps(result, indent=1, default=float))


if __name__ == "__main__":
    main()
