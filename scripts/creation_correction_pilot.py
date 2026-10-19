"""Pilot: a forward-fitted creation correction (exploratory).

Forward residuals of both blend halves grow as a lineup's best passer gets
weaker (scripts/creation_residuals.py). In-sample fits cannot see this:
creation-poor lineups get minutes when they happen to work. The correction is
therefore fitted the way calibration is, on earlier quarters' forward
residuals only:

    corrected = forecast + c x max(0, log A0 - log best passer),   A0 = 10 assists per 100

At each origin, c comes from a possession-weighted least-squares fit of
residual on [1, x] over earlier quarters (2015 onward): all rows (default), or
with --cells the scored population (offense-five cells with at least 50
possessions per quarter, x pooled like the forecasts). Only the
slope is applied, so the level calibration is untouched. The best passer is
the lineup's highest origin-dated assist rate.

Scored on the primary benchmark (44 quarters, broad offense-five cells,
seed-mean J_POINT_BOTH checkpoint average). Forecasts corrected: the half
blend, and each half separately before blending.

    PYTHONPATH=.:scripts python -u scripts/creation_correction_pilot.py
"""
import numpy as np
import pandas as pd

from capacity_score import frames, roles
from lineups import evaluate, legacy, paths
from lineups.features import Store

OUT = paths.CACHE / "creation_correction_pilot_2026_10_12"
A0 = 10.


def best_passer(rows, store):
    out = []
    for index, f in rows.groupby("origin_index", sort=False):
        off = f[evaluate.FIVE].to_numpy()
        r = roles(store, int(index), np.unique(off))
        out.append(pd.Series(r["assist"].reindex(off.ravel()).to_numpy().reshape(off.shape).max(1), index=f.index))
    return pd.concat(out)


def slope(history, column):
    w, x = history.possessions.to_numpy(float), history.x.to_numpy(float)
    y = (100 * history.points / history.possessions - history[column]).to_numpy(float)   # actual - forecast
    design = np.column_stack([np.ones_like(x), x]) * np.sqrt(w)[:, None]
    return float(np.linalg.lstsq(design, y * np.sqrt(w), rcond=None)[0][1])


def broad_cells(rows):
    out = []
    for index, f in rows.groupby("origin_index", sort=False):
        c = evaluate.cells(f, ["half", "calibrated", "additive_defense", "x", "best"])
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        out.append(c.assign(origin_index=index))
    return pd.concat(out, ignore_index=True)


def main(on_cells=False):
    OUT.mkdir(parents=True, exist_ok=True)
    g, store = legacy.matchups(), Store()
    rows = frames(lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"), g)
    # frames() yields primary origins only; prepend 2015 for the first fits' history.
    warm = []
    for o, f in evaluate.calibrated_rows(legacy.origins(), lambda o: legacy.row_frame(legacy.quarter_rows(o, g), g),
                                         lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"),
                                         lambda o, s: legacy.controls(o.tag, s)[["row", "league", "additive_defense"]],
                                         legacy.SEEDS, first_primary_season=2015):
        if o.season == 2015:
            f["origin"], f["season"], f["origin_index"] = o.tag, int(o.season), int(o.origin_index)
            warm.append(f)
    rows = pd.concat(warm + [rows], ignore_index=True)
    rows["best"] = best_passer(rows, store)
    rows["x"] = np.maximum(0., np.log(A0) - np.log(np.maximum(rows.best, 1e-3)))
    records, slopes = [], []
    origins = legacy.origins()
    fit_rows = broad_cells(rows) if on_cells else rows
    if on_cells:
        bins = pd.cut(fit_rows.best, (0, 4, 5, 6, 8, 10, 15, 100))
        print("broad-cell residuals by best passer (all quarters, half / calibrated / additive):")
        for b, f in fit_rows.groupby(bins, observed=True):
            print(f"  {b}: cells {len(f)}, " + ", ".join(
                f"{m} {np.average(f.actual - f[m], weights=f.possessions):+.2f}"
                for m in ("half", "calibrated", "additive_defense")))
    for o in origins.itertuples():
        if o.season < 2016:
            continue
        history = fit_rows[fit_rows.origin_index < o.origin_index]
        now = rows[rows.origin_index == o.origin_index].copy()
        c = {m: slope(history, m) for m in ("half", "calibrated", "additive_defense")}
        slopes.append(dict(origin=o.tag, **c))
        now["half_corrected"] = now.half + c["half"] * now.x
        now["halves_corrected"] = .5 * (now.calibrated + c["calibrated"] * now.x) + \
            .5 * (now.additive_defense + c["additive_defense"] * now.x)
        models = ["half", "half_corrected", "halves_corrected", "calibrated", "additive_defense"]
        cells = evaluate.cells(now, models)
        cells = cells[cells.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        for m in models:
            records.append(dict(origin=o.tag, season=int(o.season), model=m,
                                **evaluate.sufficient(cells.actual, cells[m], cells.possessions)))
    rec = pd.DataFrame(records)
    suffix = "_cells" if on_cells else ""
    rec.to_csv(OUT / f"sufficient{suffix}.csv", index=False)
    pd.DataFrame(slopes).to_csv(OUT / f"slopes{suffix}.csv", index=False)
    pooled = {m: evaluate.metrics(evaluate.pooled(f))["r2"] for m, f in rec.groupby("model")}
    print("pooled r2:", {k: round(v, 6) for k, v in pooled.items()})
    season = rec.groupby(["season", "model"]).apply(lambda f: evaluate.metrics(evaluate.pooled(f))["r2"],
                                                     include_groups=False).unstack()
    for m in ("half_corrected", "halves_corrected"):
        d = season[m] - season["half"]
        print(f"{m} - half: pooled {pooled[m] - pooled['half']:+.5f}; per season mean {d.mean():+.5f} "
              f"se {d.std(ddof=1) / np.sqrt(len(d)):.5f}; positive {(d > 0).sum()}/{len(d)}")
        print("  ", " ".join(f"{s}:{v:+.4f}" for s, v in d.items()))
    s = pd.DataFrame(slopes)
    print("slopes (points per unit log shortfall), first / last origin:")
    print(s.iloc[[0, len(s) // 2, -1]].round(3).to_string(index=False))


if __name__ == "__main__":
    import sys
    main(on_cells="--cells" in sys.argv)
