"""Scoring lineup forecasts: prior-only calibration, blends, cohorts and metrics.

Conventions of the primary benchmark (see MODEL_SCORECARD.md):

* Forecast rows are game x offense five x defense five; predictions are
  points per 100 possessions conditional on the defense actually faced.
* Each forecast gets its own affine calibration toward observed points,
  fitted only on earlier completed quarters (broad offense-five cells with at
  least 50 possessions), weighted by possessions, with a nonnegative slope.
  Fewer than 30 history cells: identity (cold start).
* ``half`` = 0.5 x calibrated additive_defense + 0.5 x calibrated model.
* Seeds are averaged per row before scoring.
* Cells: rows pooled to offense-five within the quarter, possession-weighted;
  the broad cohort keeps cells with at least 50 possessions.
* Metrics pool possession-weighted sufficient statistics over quarters;
  r^2 = 1 - SSE/SST around the pooled mean (not squared correlation).
"""
import numpy as np
import pandas as pd

FIVE = [f"p{i}" for i in range(5)]
MIN_CELL_POSSESSIONS = 50
MIN_HISTORY_CELLS = 30


def affine(history, start, column="forecast"):
    """Possession-weighted least squares of (actual - league) on (forecast - league)."""
    if history is None or history.empty:
        return dict(intercept=0., slope=1., n_cells=0, cold_start=True)
    h = history[pd.to_datetime(history.window_stop) <= pd.Timestamp(start)]
    if len(h) < MIN_HISTORY_CELLS:
        return dict(intercept=0., slope=1., n_cells=len(h), cold_start=True)
    w = h.possessions.to_numpy(float)
    x = (h[column] - h.league).to_numpy(float)
    y = (h.actual - h.league).to_numpy(float)
    if not np.isfinite(np.r_[x, y, w]).all() or np.any(w <= 0):
        raise ValueError("invalid calibration history")
    xm, ym = np.average(x, weights=w), np.average(y, weights=w)
    den = w @ (x - xm) ** 2
    slope = max(float(w @ ((x - xm) * (y - ym)) / den), 0.) if den > 1e-12 else 0.
    return dict(intercept=float(ym - slope * xm), slope=slope, n_cells=len(h), cold_start=False)


def calibrate(parameters, native, league):
    league = np.asarray(league)
    return league + parameters["intercept"] + parameters["slope"] * (np.asarray(native) - league)


def cells(rows, columns, keys=FIVE):
    """Pool row predictions to cells, possession-weighted; actual is points per 100."""
    f = rows[keys + ["possessions", "points"]].copy()
    for name in columns:
        f[name] = np.asarray(rows[name], float) * rows.possessions.to_numpy(float)
    f = f.groupby(keys, as_index=False, sort=True).sum()
    f["actual"] = 100 * f.points / f.possessions
    for name in columns:
        f[name] /= f.possessions
    return f


def history_cells(rows, native, league, stop):
    """One quarter's broad cells for later calibration of this forecast."""
    f = cells(rows.assign(forecast=np.asarray(native), league=np.asarray(league)), ["forecast", "league"])
    f = f[f.possessions >= MIN_CELL_POSSESSIONS].copy()
    f["window_stop"] = str(pd.Timestamp(stop).date())
    return f


def sufficient(actual, prediction, weight):
    y, p, w = (np.asarray(v, float) for v in (actual, prediction, weight))
    if not np.isfinite(np.r_[y, p, w]).all() or np.any(w <= 0):
        raise ValueError("nonfinite or nonpositive scoring rows")
    return dict(n=len(w), weight=float(w.sum()), wy=float(w @ y), wp=float(w @ p), wyy=float(w @ (y * y)),
                wpp=float(w @ (p * p)), wyp=float(w @ (y * p)), se=float(w @ ((p - y) ** 2)),
                ae=float(w @ np.abs(p - y)), error=float(w @ (p - y)))


def metrics(s):
    """RMSE, MAE, r^2, correlation and bias from pooled sufficient statistics."""
    w = s["weight"]
    vy = s["wyy"] / w - (s["wy"] / w) ** 2
    vp = s["wpp"] / w - (s["wp"] / w) ** 2
    return dict(cells=int(s["n"]), weight=w, rmse=float(np.sqrt(s["se"] / w)), mae=s["ae"] / w,
                r2=1 - s["se"] / w / vy, corr=(s["wyp"] / w - s["wy"] * s["wp"] / w ** 2) / np.sqrt(vy * vp),
                bias=s["error"] / w)


def pooled(stats):
    """Sum a list/frame of sufficient-statistic dicts."""
    frame = pd.DataFrame(list(stats)) if not isinstance(stats, pd.DataFrame) else stats
    return frame[["n", "weight", "wy", "wp", "wyy", "wpp", "wyp", "se", "ae", "error"]].sum().to_dict()


def novel_offense(rows, cutoff_day, g):
    """Offense five never seen in any matchup row dated before the cutoff."""
    prior = np.asarray(g["pids"][np.flatnonzero(np.asarray(g["date"]) < cutoff_day)])
    seen = set(map(tuple, prior))
    return np.array([t not in seen for t in map(tuple, rows[FIVE].to_numpy())])


MODELS = ("native", "calibrated", "half", "additive_defense")


def calibrated_rows(origin_frame, rows_of, native_of, controls_of, seeds, *, first_primary_season=2016):
    """Per-row forecasts over consecutive origins with strictly prior calibration.

    rows_of(origin) -> row frame (row, possessions, points, p0..p4, ...)
    native_of(origin, seed) -> (row ids, native points/100)
    controls_of(origin, seed) -> frame with row, league, additive_defense
    Yields (origin, frame) for primary origins; frame adds the seed-mean columns
    native / calibrated / half / additive_defense. Earlier origins only feed calibration.
    """
    history = {seed: [] for seed in seeds}
    for o in origin_frame.itertuples():
        rows = rows_of(o)
        per_seed = []
        for seed in seeds:
            ids, p0 = native_of(o, seed)
            ctrl = controls_of(o, seed)
            if not (np.array_equal(ids, rows.row.to_numpy()) and np.array_equal(ctrl.row.to_numpy(), ids)):
                raise ValueError(f"row mismatch at {o.tag}/s{seed}")
            parameters = affine(pd.concat(history[seed], ignore_index=True) if history[seed] else None, o.start)
            calibrated = calibrate(parameters, p0, ctrl.league)
            per_seed.append(dict(native=p0, calibrated=calibrated,
                                 half=.5 * ctrl.additive_defense.to_numpy() + .5 * calibrated,
                                 additive_defense=ctrl.additive_defense.to_numpy()))
            history[seed].append(history_cells(rows, p0, ctrl.league, o.stop))
        if o.season >= first_primary_season:
            yield o, rows.assign(**{k: np.mean([s[k] for s in per_seed], axis=0) for k in MODELS})


def rolling_scorecard(origin_frame, rows_of, native_of, controls_of, seeds, *, first_primary_season=2016,
                      novel_of=None):
    """Score one forecast over consecutive origins with strictly prior calibration.

    Arguments as calibrated_rows; novel_of(origin, rows) -> boolean per row (optional).
    Returns per-origin sufficient statistics for models
    native / calibrated / half / additive_defense, slices all and (optionally) novel.
    """
    records = []
    for o, frame in calibrated_rows(origin_frame, rows_of, native_of, controls_of, seeds,
                                    first_primary_season=first_primary_season):
        if novel_of is not None:
            frame["novel"] = novel_of(o, frame)
        models = list(MODELS)
        c = cells(frame, models + (["novel"] if novel_of is not None else []))
        c = c[c.possessions >= MIN_CELL_POSSESSIONS]
        slices = {"all": c}
        if novel_of is not None:
            slices["novel"] = c[c.novel > .5]
        for name, s in slices.items():
            for m in models:
                records.append(dict(origin=o.tag, season=int(o.season), slice=name, model=m,
                                    **sufficient(s.actual, s[m], s.possessions)))
    return pd.DataFrame(records)


def summarize(records):
    out = []
    for (slice_, model), g in records.groupby(["slice", "model"], sort=False):
        out.append(dict(slice=slice_, model=model, origins=g.origin.nunique(), **metrics(pooled(g))))
    return pd.DataFrame(out)


def _legacy_cli():
    import argparse
    from lineups import legacy
    p = argparse.ArgumentParser(description="Re-score a pre-refactor arm from its saved native predictions")
    p.add_argument("--arm", default="J_POINT_BOTH")
    p.add_argument("--view", choices=["direct", "checkpoint_average"], default="checkpoint_average")
    p.add_argument("--novel", action="store_true")
    a = p.parse_args()
    g = legacy.matchups()
    rows_of = lambda o: legacy.row_frame(legacy.quarter_rows(o, g), g)
    native_of = lambda o, s: legacy.native(o.tag, a.arm, s, a.view)
    controls_of = lambda o, s: legacy.controls(o.tag, s)[["row", "league", "additive_defense"]]
    novel_of = (lambda o, f: novel_offense(f, legacy.day(o.start), g)) if a.novel else None
    records = rolling_scorecard(legacy.origins(), rows_of, native_of, controls_of, legacy.SEEDS, novel_of=novel_of)
    with pd.option_context("display.float_format", "{:.6f}".format, "display.width", 160):
        print(summarize(records).to_string(index=False))


if __name__ == "__main__":
    _legacy_cli()
