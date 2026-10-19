"""Fit the as-of additive model at one origin with the legacy code (refactor rung 5, additive controls).

additive_defense starts from a ridge snapshot per origin fitted by the legacy
`asof_additive_tuning.fit_origin` (asof_points_2026/origins/<tag>/fit.pkl). The
scoring, centering and calibrations on top of it are ported in
lineups/additive.py; the fit itself still runs from the pre-refactor tag, with
the exact inputs and settings of the saved run (`asof_point_benchmark`).

A new origin (2027q1) is appended to the rebuilt schedule by its start date
only; the plan reads only the target start, never its stop.

Run from the legacy worktree (scripts/legacy_worktree.sh):

    cd ../basketball-legacy && OMP_NUM_THREADS=2 PYTHONPATH=. python -u \
        ../basketball/scripts/additive_origin_fit.py --tag 2026q1 --check   # must equal the saved fit
    ... --tag 2027q1 --start 2026-10-20                                     # the prospective origin
"""
import argparse
import json
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.asof_additive_tuning import choose_window_plan, fit_origin
from experiments.asof_point_benchmark import (DEBUT_POLICY, EXPANSION_ROUNDS, MIN_PROFILE_POSS, build_schedule,
                                              load_sources)

SAVED = Path("experiments/cache/asof_points_2026/origins")
OUT = Path("experiments/cache/additive_origin_fits_2026_10_09")
ARRAYS = ("sorted_ids", "reference_year", "theta", "eta", "delta", "debut_source")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    parser.add_argument("--start", help="start date for an origin not in the saved schedule")
    parser.add_argument("--check", action="store_true", help="compare with the saved fit instead of writing")
    args = parser.parse_args()
    season, window = int(args.tag[:4]), int(args.tag[5])
    t0 = time.time()
    sources = load_sources()
    schedule = build_schedule(sources)
    if not ((schedule.season == season) & (schedule.window == window)).any():
        if not args.start:
            raise ValueError(f"{args.tag} is not in the schedule; pass --start")
        start = pd.Timestamp(args.start)
        schedule = pd.concat([schedule, pd.DataFrame([dict(season=season, window=window, start=start,
                                                           stop=start + pd.Timedelta(days=42))])],
                             ignore_index=True)
    plan = choose_window_plan(schedule, season, window)
    print("plan", {k: str(v) for k, v in plan.items()}, flush=True)
    result = fit_origin(sources.possessions, sources.gp, sources.roster, sources.debut, plan,
                        expansion_rounds=EXPANSION_ROUNDS, min_profile_poss=MIN_PROFILE_POSS,
                        debut_policy=DEBUT_POLICY)
    print("choice", result["choice"], f"{time.time() - t0:.0f}s", flush=True)
    snapshot = result["snapshot"]
    if args.check:
        with (SAVED / args.tag / "fit.pkl").open("rb") as f:
            saved = pickle.load(f)
        # Penalties must be identical; the validation MSE and coefficients may differ in the last digits
        # (BLAS threading changes summation order).
        penalties = ("career", "prior", "experience", "delta", "round")
        assert all(saved["choice"][k] == result["choice"][k] for k in penalties), (saved["choice"], result["choice"])
        assert all(abs(saved["choice"][k] - result["choice"][k]) < 1e-9 for k in ("mse", "rho"))
        for k in ARRAYS:
            old, new = np.asarray(saved["snapshot"][k]), np.asarray(snapshot[k])
            if old.dtype.kind not in "fiu":
                np.testing.assert_array_equal(new, old, err_msg=k)
                continue
            diff = float(np.nanmax(np.abs(old.astype(float) - new.astype(float)))) if old.size else 0.
            print(f"  {k}: max |diff| {diff:.2e}", flush=True)
            np.testing.assert_allclose(new, old, rtol=0, atol=1e-8, err_msg=k)       # NaN positions must match
        assert pd.Timestamp(saved["snapshot"]["as_of"]) == pd.Timestamp(snapshot["as_of"])
        print("CHECK_OK", args.tag, "same penalties; snapshot within 1e-8 of the saved fit", flush=True)
        return
    out = OUT / args.tag
    out.mkdir(parents=True, exist_ok=False)
    with (out / "fit.pkl").open("wb") as f:
        pickle.dump(dict(snapshot=snapshot, plan=result["plan"], choice=result["choice"], audit=result["audit"],
                         data_epoch=sources.epoch), f)
    (out / "fit.json").write_text(json.dumps(dict(
        tag=args.tag, plan={k: str(v) for k, v in plan.items()}, choice=result["choice"],
        timings=result["timings"], data_epoch=sources.epoch, snapshot_as_of=str(snapshot["as_of"]),
        producer="scripts/additive_origin_fit.py on tag pre-refactor-2026-10-09"), indent=1, default=str))
    print("SAVED", out, flush=True)


if __name__ == "__main__":
    main()
