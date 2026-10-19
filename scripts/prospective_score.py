"""Score the frozen 2026-27 prospective test (protocol: reports/prospective_2027q1_protocol_2026_10_09.md).

Written and committed before any 2026-27 game was played; it is not revised
after outcomes are seen.

Input: matchup rows (game x offense five x defense five) from the refreshed
data, as a table with columns game_id, date (days since 1970-01-01), p0..p4,
d0..d4 (store player ids), possessions and points. Players unknown to the
2027q1 store get its population fallback (neural arms) or count as the average
player (arm A).

Forecasts per row: A = lineups.additive at 2027q1; for R and C, each seed's
checkpoint mixture in origin mode, calibrated with its frozen affine, then
averaged over seeds; half = 0.5 A + 0.5 calibrated.

Populations, each pooled to offense-five cells with at least 50 possessions:
- primary: the 2027q1 window (rows before the stop date of the realized
  window, which ends when the league's game count crosses 300);
- whole season: every quarter window of 2026-27, cells per window.

Metrics per population and forecast:
- centered r^2 (primary), after removing the forecast's possession-weighted
  mean error;
- raw r^2 and mean bias.

Contrasts, with 95% intervals from a game-level block bootstrap (1,000
resamples of games within the population):
- primary, the neural model alone: R calibrated - A, and C calibrated -
  R calibrated;
- secondary, the half blends: R half - A, and C half - R half.

    PYTHONPATH=.:scripts python -u scripts/prospective_score.py --rows ROWS.csv.gz --stop YYYY-MM-DD
    PYTHONPATH=.:scripts python -u scripts/prospective_score.py --dry-run   # backtest check at 2026q4
"""
import argparse
import json

import numpy as np
import pandas as pd
import torch

from lineups import evaluate
from lineups.evaluate import FIVE

DEFENSE = [f"d{i}" for i in range(5)]
MIN_POSSESSIONS = 50
# Primary: the neural model alone (calibrated); secondary: the half blends.
CONTRASTS = (("R_calibrated", "A"), ("C_calibrated", "R_calibrated"), ("R_half", "A"), ("C_half", "R_half"))
BOOTSTRAP, SEED = 1000, 20261020


def metrics(cells, forecast, weight=None):
    """Raw r^2, centered r^2 and bias (forecast - actual) on possession-weighted cells."""
    w = cells.possessions.to_numpy(float) if weight is None else weight
    y, p = cells.actual.to_numpy(float), cells[forecast].to_numpy(float)
    sst = w @ (y - np.average(y, weights=w)) ** 2
    e = y - p
    bias = np.average(e, weights=w)
    return dict(r2=1 - (w @ e ** 2) / sst, centered_r2=1 - (w @ (e - bias) ** 2) / sst, bias=-bias)


def cells(rows, forecasts, window):
    """Offense-five cells per window with at least MIN_POSSESSIONS possessions."""
    f = rows.assign(window=window, **forecasts)
    c = evaluate.cells(f, list(forecasts), keys=["window"] + FIVE)
    return c[c.possessions >= MIN_POSSESSIONS]


def _mse(c, forecast):
    w, e = c.possessions.to_numpy(float), (c.actual - c[forecast]).to_numpy(float)
    mean = np.average(e, weights=w)
    return np.average(e ** 2, weights=w), np.average((e - mean) ** 2, weights=w)


def contrasts(rows, forecasts, window, resamples=BOOTSTRAP):
    """Point metrics and game-bootstrap intervals for the contrasts.

    The cells are those of the observed population. A resample reweights their rows by how
    often each game is drawn. A contrast's interval comes from the resampled difference in
    (centered) mean squared error divided by the observed outcome variance, so the point
    estimate equals the r^2 difference. A difference of r^2 values recomputed per resample
    would instead shrink toward zero, because resampling adds outcome noise to the variance in
    the denominator.
    """
    c = cells(rows, forecasts, window)
    point = {m: metrics(c, m) for m in forecasts}
    result = dict(cells=len(c), possessions=float(c.possessions.sum()), metrics=point, contrasts={})
    w, y = c.possessions.to_numpy(float), c.actual.to_numpy(float)
    variance = np.average((y - np.average(y, weights=w)) ** 2, weights=w)
    keys = c[["window"] + FIVE]
    inside = rows.assign(window=window).merge(keys, on=["window"] + FIVE, how="left", indicator=True)["_merge"]
    inside = (inside == "both").to_numpy()
    rows, window = rows[inside].reset_index(drop=True), window[inside]
    forecasts = {k: v[inside] for k, v in forecasts.items()}
    games = np.unique(rows.game_id)
    position = np.searchsorted(games, rows.game_id.to_numpy())
    pairs = [(a, b) for a, b in CONTRASTS if a in forecasts and b in forecasts]
    draws = {(a, b): [] for a, b in pairs}
    rng = np.random.default_rng(SEED)
    for _ in range(resamples):
        weight = np.bincount(rng.integers(0, len(games), len(games)), minlength=len(games))[position].astype(float)
        keep = weight > 0
        boot = rows[keep].assign(possessions=rows.possessions[keep] * weight[keep],
                                 points=rows.points[keep] * weight[keep])
        f = boot.assign(window=window[keep], **{k: v[keep] for k, v in forecasts.items()})
        b = evaluate.cells(f, list(forecasts), keys=["window"] + FIVE)
        mse = {m: _mse(b, m) for m in {x for pair in pairs for x in pair}}
        for a, z in pairs:
            draws[(a, z)].append([(mse[z][0] - mse[a][0]) / variance, (mse[z][1] - mse[a][1]) / variance])
    for a, z in pairs:
        d = np.asarray(draws[(a, z)]) if resamples else np.empty((0, 2))
        result["contrasts"][f"{a} - {z}"] = {
            k: dict(estimate=point[a][k] - point[z][k],
                    low=float(np.percentile(d[:, i], 2.5)) if resamples else None,
                    high=float(np.percentile(d[:, i], 97.5)) if resamples else None)
            for i, k in enumerate(("r2", "centered_r2"))}
    return result


def frozen_forecasts(rows):
    """A, R and C forecasts per row from the frozen 2027q1 arms and their recorded calibrations."""
    from prospective_fit import ARMS, OUT, SEEDS, STORE, model, path
    from lineups import additive
    from lineups.coherence import ledgers
    from lineups.features import Store
    record = json.loads((OUT / "freeze" / "record.json").read_text())
    store = Store(STORE)
    offense, defense = rows[FIVE].to_numpy(np.int64), rows[DEFENSE].to_numpy(np.int64)
    control = additive.Additive("2027q1", schedule=store.schedule())
    out = dict(A=control.points(offense, defense))
    for arm in ARMS:
        calibrated = []
        for seed in SEEDS:
            saved = torch.load(path(arm, seed), map_location="cpu", weights_only=False)
            mixture = model(arm, seed, saved)[1]
            native = np.concatenate([ledgers(mixture, store, offense[i:i + 4096], defense[i:i + 4096], "2027q1")
                                     .points100.numpy().astype(float) for i in range(0, len(rows), 4096)])
            calibrated.append(evaluate.calibrate(record["calibration"][f"{arm}_s{seed}"], native, control.league))
        out[f"{arm}_calibrated"] = np.mean(calibrated, 0)
        out[f"{arm}_half"] = .5 * out["A"] + .5 * out[f"{arm}_calibrated"]
    return out


def dry_run():
    """Backtest check: the saved reference (as R) and additive_defense at 2026q4 reproduce the scorecard values."""
    from lineups import legacy
    g = legacy.matchups()
    rows_of = lambda o: legacy.row_frame(legacy.quarter_rows(o, g), g)
    native_of = lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average")
    controls_of = lambda o, s: legacy.controls(o.tag, s)[["row", "league", "additive_defense"]]
    for o, f in evaluate.calibrated_rows(legacy.origins(), rows_of, native_of, controls_of, legacy.SEEDS):
        if o.tag != "2026q4":
            continue
        forecasts = dict(A=f.additive_defense.to_numpy(), R_calibrated=f.calibrated.to_numpy(), R_half=f.half.to_numpy())
        result = contrasts(f, forecasts, np.zeros(len(f), int), resamples=200)
        print(json.dumps(result, indent=1, default=float))
        expected = dict(R_calibrated=.1104, R_half=.0972, A=.0728)   # per-quarter raw r^2 from the rolling scorecard
        for k, v in expected.items():
            assert abs(result["metrics"][k]["r2"] - v) < 5e-5, (k, result["metrics"][k]["r2"])
        print("DRY_RUN_OK")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rows", help="refreshed 2026-27 matchup rows (csv)")
    p.add_argument("--stop", help="realized stop date of the 2027q1 window (first day after it)")
    p.add_argument("--windows", help="csv of 2026-27 quarter windows (season, window, start, stop) for the whole season")
    p.add_argument("--out")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    if a.dry_run:
        return dry_run()
    rows = pd.read_csv(a.rows)
    forecasts = frozen_forecasts(rows)
    stop = int(np.datetime64(a.stop, "D").astype(np.int64))
    primary = rows.date.to_numpy() < stop
    report = dict(primary=contrasts(rows[primary].reset_index(drop=True), {k: v[primary] for k, v in forecasts.items()},
                                    np.zeros(int(primary.sum()), int)))
    if a.windows:
        w = pd.read_csv(a.windows, parse_dates=["start", "stop"])
        window = np.full(len(rows), -1)
        for i, r in enumerate(w.itertuples()):
            inside = (rows.date >= np.datetime64(r.start, "D").astype(np.int64)) & \
                     (rows.date < np.datetime64(r.stop, "D").astype(np.int64))
            window[inside.to_numpy()] = i
        keep = window >= 0
        report["whole_season"] = contrasts(rows[keep].reset_index(drop=True), {k: v[keep] for k, v in forecasts.items()},
                                           window[keep])
    text = json.dumps(report, indent=1, default=float)
    print(text)
    if a.out:
        open(a.out, "w").write(text)


if __name__ == "__main__":
    main()
