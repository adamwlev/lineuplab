"""Pilot: can a two-phase fit from scratch replace the v14 parents? (exploratory)

Phase A trains the offense alone (EventModel.offense_only: backbone and
rebound heads, defense and adjusted heads off) with the reference protocol.
Phase B starts from it exactly as the reference starts from a v14 parent
(EventModel.from_offense: zero adjusted and defense heads) and runs the
protocol again. If this matches the reference, offense-side structure and the
2026-27 refresh no longer need the legacy v14 chain.

Compared with the saved reference at the same origin and seed, on identical
rows: outer native event losses and pooled point MSE (as in
scripts/single_stage_check.py, direct view), and half-blend r^2 on broad
cells with the reference's prior-only calibration (checkpoint-average view).

    PYTHONPATH=. python -u scripts/two_phase_check.py --origins 2016q1 2019q3 2022q2 2025q4 --seed 17
"""
import argparse
import json
import time

import numpy as np
import torch

from capacity_screen import score
from coverage_screen import reference_calibration
from lineups import legacy, paths
from lineups.features import Store
from lineups.model import EventModel, load_legacy
from lineups.train import FAMILIES, Rows, evaluate, fit_origin, self_references

OUT = paths.CACHE / "two_phase_check_2026_10_09"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--origins", nargs="+", default=["2016q1", "2019q3", "2022q2", "2025q4"])
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--defense", default="broadcast")
    p.add_argument("--self-references", action="store_true",
                   help="normalize each phase by its own starting model instead of the saved v16 references")
    a = p.parse_args()
    if a.seed != 17:
        raise SystemExit("the comparison uses the reference's seed-17 calibration")
    torch.set_num_threads(1)
    OUT.mkdir(parents=True, exist_ok=True)
    schedule, store = legacy.schedule(), Store()
    g = legacy.matchups()
    data = Rows(g, store)
    for tag in a.origins:
        origin = schedule[schedule.tag == tag].iloc[0]
        inner = schedule[schedule.stop <= origin.start].iloc[-1]
        tick = time.monotonic()
        log = lambda m: print(f"[{tag} {time.monotonic() - tick:6.0f}s] {m}", flush=True)
        log("phase A: offense only")
        reference = self_references(data) if a.self_references else None
        suffix = "_selfref" if a.self_references else ""
        offense = fit_origin(lambda phase: EventModel.offense_only(a.seed), data, store, origin, inner, a.seed, log=log,
                             reference=reference)

        def parent(phase):
            m = EventModel.offense_only(a.seed)
            m.load_state_dict(offense["inner_state" if phase == "inner" else "final_state"])
            return EventModel.from_offense(m, a.seed, a.defense)

        log("phase B: full model")
        full = fit_origin(parent, data, store, origin, inner, a.seed, log=log, reference=reference)
        torch.save(dict(offense_inner=offense["inner_state"], offense_final=offense["final_state"],
                        offense_selected=offense["selected_epoch"], final=full["final_state"],
                        checkpoints=full["checkpoint_states"], selected=full["selected_epoch"]),
                   OUT / f"{tag}_s{a.seed}_{a.defense}{suffix}.pt")
        norm, env = store.normalizer(tag, "final"), store.env(tag, "final")
        outer = data.window(legacy.day(origin.start), legacy.day(origin.stop))
        case = paths.V16_RUN / "origins" / tag / "J_POINT_BOTH" / f"s{a.seed}" / "final"
        reference = load_legacy(torch.load(case / "fit.pt", map_location="cpu", weights_only=False)["state_dict"])
        two_phase = parent("final")
        two_phase.load_state_dict(full["final_state"])
        report = dict(origin=tag, seed=a.seed, defense=a.defense, self_references=a.self_references,
                      offense_epoch=offense["selected_epoch"],
                      selected_epoch=full["selected_epoch"], seconds=time.monotonic() - tick)
        for name, model in (("reference", reference), ("two_phase", two_phase)):
            totals, _, _ = evaluate(model, data, outer, norm, env, origin_index=int(origin.origin_index))
            report[name] = {f: totals[f][0] / totals[f][1] for f in FAMILIES} | {
                "point_mse": totals["point"][0] / totals["point"][1]}
        frame = legacy.row_frame(legacy.quarter_rows(origin, g), g)
        controls = legacy.controls(tag, a.seed)
        calibration = reference_calibration(tag)      # the reference's seed-17 calibration
        assert np.array_equal(frame.row.to_numpy(), full["rows"])
        report["r2_reference"] = score(legacy.native(tag, "J_POINT_BOTH", a.seed, "checkpoint_average")[1], frame,
                                       controls, calibration)
        report["r2_two_phase"] = score(full["checkpoint_average"], frame, controls, calibration)
        log("TWO_PHASE " + json.dumps(report))
        with open(OUT / "results.jsonl", "a") as f:
            f.write(json.dumps(report) + "\n")


if __name__ == "__main__":
    main()
