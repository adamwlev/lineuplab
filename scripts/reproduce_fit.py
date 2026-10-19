"""Rung 4a: refit one saved reference case with lineups.train and compare.

Initializes from the same v14 parents the production run used, so a faithful
trainer should reproduce the selected epoch, the final weights and the outer
forecasts of experiments/cache/joint_capability_2026_09_19_v16_fast2_ready.

    PYTHONPATH=. python -u scripts/reproduce_fit.py --origin 2020q1 --seed 17
"""
import argparse
import json
import time

import numpy as np
import torch

from lineups import legacy, paths
from lineups.features import Store
from lineups.model import EventModel, from_legacy_state
from lineups.train import Rows, fit_origin

V14 = paths.CACHE / "joint_capability_2026_09_15_v14_prod"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--origin", default="2020q1")
    p.add_argument("--seed", type=int, default=17)
    a = p.parse_args()
    torch.set_num_threads(1)
    schedule = legacy.schedule()
    origin = schedule[schedule.tag == a.origin].iloc[0]
    inner = schedule[schedule.stop <= origin.start].iloc[-1]
    store = Store()
    data = Rows(legacy.matchups(), store)
    parent = lambda phase: torch.load(V14 / "origins" / a.origin / "RB_RENEW_FAC" / f"s{a.seed}" / f"{phase}.pt",
                                      map_location="cpu", weights_only=False)["state_dict"]
    tick = time.monotonic()
    result = fit_origin(lambda phase: EventModel.from_parent(parent(phase), a.seed), data, store, origin, inner, a.seed,
                        log=lambda m: print(f"[{time.monotonic() - tick:7.0f}s] {m}", flush=True))
    case = paths.V16_RUN / "origins" / a.origin / "J_POINT_BOTH" / f"s{a.seed}"
    summary = json.loads((case / "fit_summary.json").read_text())
    saved = torch.load(case / "final" / "fit.pt", map_location="cpu", weights_only=False)
    expected = from_legacy_state(saved["state_dict"])
    weight_diff = max(float((result["final_state"][k] - v).abs().max()) for k, v in expected.items())
    report = dict(selected_new=result["selected_epoch"], selected_saved=summary["selected_epoch"],
                  max_weight_diff=weight_diff, seconds=time.monotonic() - tick)
    for view, name in (("direct", "primary"), ("checkpoint_average", "checkpoint_average")):
        rows, saved_points = legacy.native(a.origin, "J_POINT_BOTH", a.seed, view)
        assert np.array_equal(rows, result["rows"])
        diff = result[view] - saved_points
        report[f"{view}_max_abs_diff"] = float(np.abs(diff).max())
        report[f"{view}_rms_diff"] = float(np.sqrt(np.mean(diff ** 2)))
    print("REPRODUCE", json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
