"""Freeze record for the 2026-27 prospective test (origin 2027q1); run after scripts/prospective_fit.py.

Protocol: reports/prospective_2027q1_protocol_2026_10_09.md. Everything here
uses data dated before opening night (2026-10-20); nothing reads a 2026-27 game.

Records:
- calibrations at 2027q1 (one per arm and seed): the prior-only affine on the
  architecture's 2015-2026 checkpoint-average history cells (R: saved
  J_POINT_BOTH; C: the confirmatory capacity run), with league from arm A;
- arm A (additive_defense) at 2027q1: snapshot, centering and calibrations;
- fixtures: every registered lineup against the league-average defense, and
  the named matchups, for R, C and A (native, calibrated, half);
- the property suite for R and C on the real fives of 2026q4 (at least 50
  possessions), looked up with 2027q1 states;
- out-of-support reasons for the named matchups;
- hashes of the code commit, the store manifest, every fit and the additive snapshot.

    PYTHONPATH=. python -u scripts/prospective_freeze.py

Output: experiments/cache/prospective_2027q1/freeze/ (refuses to overwrite).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

sys.path.insert(0, str(Path(__file__).parent))
from capacity_run import case_dir  # noqa: E402
from prospective_fit import ARMS, ORIGIN, OUT, SEEDS, STORE, model, path  # noqa: E402
from property_suite import real_fives  # noqa: E402

from lineups import additive, evaluate, legacy, properties  # noqa: E402
from lineups.coherence import fixtures, ledgers  # noqa: E402
from lineups.evaluate import FIVE  # noqa: E402
from lineups.features import Store  # noqa: E402
from lineups.support import Support  # noqa: E402

FREEZE = OUT / "freeze"
PAIRS = (("legal_pure_centers", "jokic_westbrook"), ("legal_pure_centers", "jokic_korver"),
         ("five_goberts", "jokic_westbrook"), ("five_jokics", "jokic_westbrook"), ("limited_centers", "jokic_westbrook"),
         ("small_guards", "jokic_westbrook"), ("highest_exposure_real_2026", "jokic_westbrook"),
         ("rebound_same_four_Rudy_Gobert", "highest_exposure_real_2026"))
HISTORY = dict(R=lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"),
               C=lambda o, s: _capacity_native(o.tag, s))


def _capacity_native(tag, seed):
    with np.load(case_dir(tag, seed) / "forecast.npz") as z:
        return z["row"].copy(), z["checkpoint_average"].astype(float)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def calibrations(start, g):
    """Prior-only affine on every 2015-2026 quarter's broad cells, per arm and seed."""
    history = {(arm, seed): [] for arm in ARMS for seed in SEEDS}
    for o in legacy.origins().itertuples():
        rows = legacy.row_frame(legacy.quarter_rows(o, g), g)
        for (arm, seed), cells in history.items():
            ids, native = HISTORY[arm](o, seed)
            league = legacy.controls(o.tag, seed)
            if not (np.array_equal(ids, rows.row.to_numpy()) and np.array_equal(league.row.to_numpy(), ids)):
                raise ValueError(f"row mismatch at {o.tag}/{arm}/s{seed}")
            cells.append(evaluate.history_cells(rows, native, league.league, o.stop))
    return {f"{arm}_s{seed}": evaluate.affine(pd.concat(cells, ignore_index=True), start)
            for (arm, seed), cells in history.items()}


def main():
    FREEZE.mkdir(parents=True, exist_ok=False)
    store, g, fx = Store(STORE), legacy.matchups(), fixtures()
    schedule = store.schedule()
    origin = schedule.query("tag == @ORIGIN").iloc[0]
    control = additive.Additive(ORIGIN, schedule=schedule)
    league = control.league
    record = dict(origin=ORIGIN, start=str(origin.start.date()),
                  commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
                  fit_launch_commit=(OUT / "launch_commit.txt").read_text().strip(),
                  dirty=bool(subprocess.run(["git", "status", "--porcelain", "lineups", "scripts"], capture_output=True,
                                            text=True).stdout.strip()),
                  store_manifest=sha256(STORE / "manifest.json"),
                  fits={f"{arm}_s{seed}": sha256(path(arm, seed)) for arm in ARMS for seed in SEEDS},
                  additive=dict(snapshot=sha256(additive.FITS[1] / ORIGIN / "fit.pkl"), league=league,
                                means=control.means, offense_calibration=control.offense_calibration,
                                defense_calibration=control.defense_calibration, blend=control.blend),
                  calibration=calibrations(origin.start, g), selected_epochs={})
    print("calibrations", json.dumps(record["calibration"], indent=1), flush=True)
    models = {}
    for arm in ARMS:
        models[arm] = {}
        for seed in SEEDS:
            saved = torch.load(path(arm, seed), map_location="cpu", weights_only=False)
            models[arm][seed] = model(arm, seed, saved)[1]
            record["selected_epochs"][f"{arm}_s{seed}"] = dict(offense=saved["offense_selected"],
                                                              full=saved["selected"])

    def forecast(arm, offense, defense):
        """Seed-mean calibrated points/100 and the native three-seed mixture, for [B,5] fives."""
        calibrated, native = [], []
        for seed in SEEDS:
            p = ledgers(models[arm][seed], store, offense, defense, ORIGIN).points100.numpy().astype(float)
            native.append(p)
            calibrated.append(evaluate.calibrate(record["calibration"][f"{arm}_s{seed}"], p, league))
        return np.mean(native, 0), np.mean(calibrated, 0)

    # Fixtures against the league-average defense.
    names = sorted(fx)
    offense = np.array([fx[n]["pids"] for n in names], np.int64)
    table = pd.DataFrame(dict(fixture=names, players=[", ".join(fx[n]["names"]) for n in names]))
    table["A"] = control.points(offense)
    for arm in ARMS:
        table[f"{arm}_native"], table[f"{arm}_calibrated"] = forecast(arm, offense, None)
        table[f"{arm}_half"] = .5 * table.A + .5 * table[f"{arm}_calibrated"]
    table.to_csv(FREEZE / "fixtures_vs_average.csv", index=False)

    # Named matchups: margins (A's offense minus B's offense), both directions.
    support, rows = Support(store, ORIGIN), []
    for a, b in PAIRS:
        pa, pb = np.array([fx[a]["pids"]]), np.array([fx[b]["pids"]])
        rec = dict(a=a, b=b, A=float(control.points(pa, pb)[0] - control.points(pb, pa)[0]))
        for arm in ARMS:
            (na, ca), (nb, cb) = forecast(arm, pa, pb), forecast(arm, pb, pa)
            rec[f"{arm}_native"] = float(na[0] - nb[0])
            rec[f"{arm}_calibrated"] = float(ca[0] - cb[0])
            rec[f"{arm}_half"] = float(.5 * rec["A"] + .5 * (ca[0] - cb[0]))
        reasons = support.describe(fx[a]["pids"], fx[b]["pids"])["reasons"]
        reasons += [f"opponent: {r}" for r in support.describe(fx[b]["pids"], fx[a]["pids"])["reasons"]
                    if not r.startswith("defense")]
        rec["reasons"] = "; ".join(reasons) or "within observed support"
        rows.append(rec)
    matchups = pd.DataFrame(rows)
    matchups.to_csv(FREEZE / "matchups.csv", index=False)

    # Property suite on 2026q4's real fives, looked up at 2027q1.
    base_offense, base_defense = real_fives("2026q4", g, FIVE), real_fives("2026q4", g, legacy.DEFENSE)
    summaries = []
    for arm in ARMS:
        mixture = [m for seed in SEEDS for m in models[arm][seed]]
        frame = properties.run(lambda o, d: ledgers(mixture, store, o, d, ORIGIN), store, ORIGIN, base_offense,
                               base_defense, base_offense[:40])
        frame.to_csv(FREEZE / f"properties_{arm}.csv", index=False)
        summaries.append(properties.summarize(frame).assign(arm=arm))
    props = pd.concat(summaries)
    props.to_csv(FREEZE / "properties_summary.csv")

    record["files"] = {p.name: sha256(p) for p in sorted(FREEZE.iterdir())}
    (FREEZE / "record.json").write_text(json.dumps(record, indent=1, default=float))
    with pd.option_context("display.width", 250, "display.max_colwidth", 120, "display.float_format", "{:+.2f}".format):
        print(table.drop(columns="players").to_string(index=False))
        print(matchups.to_string(index=False))
        print(props.to_string())
    print("FROZEN", FREEZE, "record sha256", sha256(FREEZE / "record.json"))


if __name__ == "__main__":
    main()
