"""Confirmatory run: one CapacityDefense (version 2) fit per origin and seed.

Protocol: reports/capacity_confirmatory_protocol_2026_10_09.md. Resumable: a
case with complete.json is skipped.

    PYTHONPATH=. python -u scripts/capacity_run.py --origin 2020q1 --seed 17
    PYTHONPATH=. python -u scripts/capacity_run.py --cases    # print every origin,seed pair
"""
import argparse
import json
import subprocess
import time

import numpy as np
import torch

from lineups import legacy, paths
from lineups.features import Store
from lineups.model import EventModel
from lineups.train import Rows, fit_origin

OUT = paths.CACHE / "capacity_v2_run_2026_10_09"
V14 = paths.CACHE / "joint_capability_2026_09_15_v14_prod"


def case_dir(tag, seed):
    return OUT / "origins" / tag / f"s{seed}"


def run(tag, seed):
    case = case_dir(tag, seed)
    if (case / "complete.json").exists():
        print(f"{tag}/s{seed} already complete", flush=True)
        return
    torch.set_num_threads(1)
    case.mkdir(parents=True, exist_ok=True)
    tick = time.monotonic()
    log = lambda m: print(f"[{tag}/s{seed} {time.monotonic() - tick:6.0f}s] {m}", flush=True)
    store, g = Store(), legacy.matchups()
    schedule = legacy.schedule()
    origin = schedule[schedule.tag == tag].iloc[0]
    inner = schedule[schedule.stop <= origin.start].iloc[-1]
    parent = lambda phase: torch.load(V14 / "origins" / tag / "RB_RENEW_FAC" / f"s{seed}" / f"{phase}.pt",
                                      map_location="cpu", weights_only=False)["state_dict"]
    fit = fit_origin(lambda phase: EventModel.from_parent(parent(phase), seed, defense="capacity"),
                     Rows(g, store), store, origin, inner, seed, log=log)
    np.savez(case / "forecast.npz", row=fit["rows"], direct=fit["direct"], checkpoint_average=fit["checkpoint_average"])
    torch.save(dict(final=fit["final_state"], checkpoints=fit["checkpoint_states"]), case / "fit.pt")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=paths.ROOT).stdout.strip()
    (case / "complete.json").write_text(json.dumps(dict(
        origin=tag, seed=seed, selected_epoch=fit["selected_epoch"], inner_curve=fit["inner_curve"],
        final_curve=fit["final_curve"], seconds=time.monotonic() - tick, commit=commit), indent=1))
    log(f"done selected_epoch={fit['selected_epoch']}")


def cases():
    return [(t, s) for t in legacy.origins().tag for s in legacy.SEEDS]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--origin")
    p.add_argument("--seed", type=int)
    p.add_argument("--cases", action="store_true")
    a = p.parse_args()
    if a.cases:
        print("\n".join(f"{t} {s}" for t, s in cases() if not (case_dir(t, s) / "complete.json").exists()))
    else:
        run(a.origin, a.seed)
