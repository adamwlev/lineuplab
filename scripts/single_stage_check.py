"""Rung 4b: does single-stage training from scratch match the two-stage reference?

The reference (J_POINT_BOTH) starts each origin from a separately trained v14
offense. Here EventModel.fresh(seed) trains in one stage, with the same
objective, protocol and inputs. On the outer quarter it compares, on
identical rows, the event-family NLL and the native point MSE (pooled by game
and offense five) with the reference's saved predictions, recomputed through
the same evaluator. This is exploratory: a few origins and one seed, not a
registered benchmark.

    PYTHONPATH=. python -u scripts/single_stage_check.py --origins 2016q1 2019q3 2022q2 2025q4 --seed 17
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from lineups import legacy, paths
from lineups.features import Store
from lineups.model import EventModel, load_legacy
from lineups.train import FAMILIES, Rows, evaluate, fit_origin


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--origins", nargs="+", default=["2016q1", "2019q3", "2022q2", "2025q4"])
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--out", default=str(paths.CACHE / "lineups_single_stage_2026_10_09"))
    a = p.parse_args()
    torch.set_num_threads(1)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    schedule = legacy.schedule()
    store = Store()
    data = Rows(legacy.matchups(), store)
    day = lambda d: int(np.datetime64(d, "D").astype(np.int64))
    for tag in a.origins:
        origin = schedule[schedule.tag == tag].iloc[0]
        inner = schedule[schedule.stop <= origin.start].iloc[-1]
        tick = time.monotonic()
        log = lambda m: print(f"[{tag} {time.monotonic() - tick:6.0f}s] {m}", flush=True)
        result = fit_origin(lambda phase: EventModel.fresh(a.seed), data, store, origin, inner, a.seed, log=log)
        outer = data.window(day(origin.start), day(origin.stop))
        norm, env = store.normalizer(tag, "final"), store.env(tag, "final")
        case = paths.V16_RUN / "origins" / tag / "J_POINT_BOTH" / f"s{a.seed}" / "final"
        reference = load_legacy(torch.load(case / "fit.pt", map_location="cpu", weights_only=False)["state_dict"])
        fresh = EventModel.fresh(a.seed)
        fresh.load_state_dict(result["final_state"])
        report = dict(origin=tag, seed=a.seed, selected_epoch=result["selected_epoch"],
                      seconds=time.monotonic() - tick)
        for name, model in (("reference", reference), ("single_stage", fresh)):
            totals, rows, points = evaluate(model, data, outer, norm, env, origin_index=int(origin.origin_index))
            report[name] = {f: totals[f][0] / totals[f][1] for f in FAMILIES} | {
                "point_mse": totals["point"][0] / totals["point"][1]}
            np.save(out / f"{tag}_s{a.seed}_{name}_direct.npy", points)
        np.save(out / f"{tag}_s{a.seed}_rows.npy", rows)
        torch.save(dict(final=result["final_state"], checkpoints=result["checkpoint_states"],
                        selected_epoch=result["selected_epoch"], inner_curve=result["inner_curve"],
                        final_curve=result["final_curve"]), out / f"{tag}_s{a.seed}_fit.pt")
        np.save(out / f"{tag}_s{a.seed}_single_stage_checkpoint_average.npy", result["checkpoint_average"])
        print("SINGLE_STAGE", json.dumps(report), flush=True)
        with open(out / "results.jsonl", "a") as f:
            f.write(json.dumps(report) + "\n")


if __name__ == "__main__":
    main()
