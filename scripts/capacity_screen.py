"""Exploratory screen: the capacity-law defense as an assumption model (2026-10-09).

Design, fixed before running:

* Arm: EventModel.from_parent(v14 parent, seed 17, defense="capacity"), fitted
  with the full reference protocol (lineups.train.fit_origin: inner epoch
  selection, fresh final fit, last five checkpoints).
* Comparator: the saved J_POINT_BOTH fit for the same origin and seed, which
  lineups.train reproduces exactly (reports/refactor_parity_2026_10_09.md).
* Origins: 2017q2 2018q3 2019q4 2021q2 2022q3 2023q4 2025q2 2026q4.
* Contrast 1 (accuracy, non-inferiority margin -0.003 r^2): outer broad cells,
  checkpoint-average view, half blend with additive_defense. Calibration is
  approximated in two ways, both reported: (a) the reference's prior-only
  affine applied to both models; (b) each model's own in-quarter affine
  (an oracle, the same for both).
* Contrast 2 (pillar 2): native fixture margins at 2026q4 and the property
  suite at 2026q4, checkpoint mixtures.

Single seed and eight origins: a screen, not a registered result. Versions 2
and 3 of CapacityDefense are post-hoc revisions (see its docstring), each run
with the same design.

    PYTHONPATH=. python -u scripts/capacity_screen.py --origin 2026q4
    PYTHONPATH=. python -u scripts/capacity_screen.py --summary
"""
import argparse
import json
import time

import numpy as np
import pandas as pd
import torch

import property_suite
from coverage_screen import FIXTURE_PAIRS, ORIGINS, SEED, reference_calibration
from lineups import evaluate, legacy, paths, properties
from lineups.coherence import checkpoint_models, fixtures, ledgers, matchup
from lineups.features import Store
from lineups.model import EventModel, load_legacy
from lineups.train import Rows, fit_origin

# Version 1 (commit 6f5e7b67) wrote capacity_screen_2026_10_09; version 2 (the current
# CapacityDefense) wrote here; version 3 (listings only in the assignment, not kept) wrote
# capacity_v3_screen_2026_10_09.
OUT = paths.CACHE / "capacity_v2_screen_2026_10_09"
V14 = paths.CACHE / "joint_capability_2026_09_15_v14_prod"


def oracle(native, frame, league):
    """In-quarter affine on broad cells (the same oracle for every model)."""
    f = frame.assign(forecast=native, league=league)
    cells = evaluate.cells(f, ["forecast", "league"])
    cells = cells[cells.possessions >= evaluate.MIN_CELL_POSSESSIONS].assign(window_stop="1900-01-01")
    return evaluate.affine(cells, "2100-01-01")


def score(native, frame, controls, calibration):
    league = controls.league.to_numpy()
    calibrated = evaluate.calibrate(calibration, native, league)
    f = frame.assign(half=.5 * controls.additive_defense.to_numpy() + .5 * calibrated, calibrated=calibrated)
    cells = evaluate.cells(f, ["half", "calibrated"])
    cells = cells[cells.possessions >= evaluate.MIN_CELL_POSSESSIONS]
    return {m: evaluate.metrics(evaluate.sufficient(cells.actual, cells[m], cells.possessions))["r2"]
            for m in ("half", "calibrated")}


def run(tag):
    torch.set_num_threads(1)
    OUT.mkdir(parents=True, exist_ok=True)
    tick = time.monotonic()
    log = lambda m: print(f"[{tag} {time.monotonic() - tick:6.0f}s] {m}", flush=True)
    store, g = Store(), legacy.matchups()
    data = Rows(g, store)
    schedule = legacy.schedule()
    origin = schedule[schedule.tag == tag].iloc[0]
    inner = schedule[schedule.stop <= origin.start].iloc[-1]
    parent = lambda phase: torch.load(V14 / "origins" / tag / "RB_RENEW_FAC" / f"s{SEED}" / f"{phase}.pt",
                                      map_location="cpu", weights_only=False)["state_dict"]
    fit = fit_origin(lambda phase: EventModel.from_parent(parent(phase), SEED, defense="capacity"), data, store,
                     origin, inner, SEED, log=log)
    torch.save(dict(final=fit["final_state"], checkpoints=fit["checkpoint_states"], selected=fit["selected_epoch"]),
               OUT / f"{tag}.pt")
    frame = legacy.row_frame(legacy.quarter_rows(origin, g), g)
    controls = legacy.controls(tag, SEED)
    assert np.array_equal(frame.row.to_numpy(), fit["rows"]) and np.array_equal(controls.row.to_numpy(), fit["rows"])
    calibration = reference_calibration(tag)
    result = dict(origin=tag, selected_epoch=fit["selected_epoch"],
                  reference_selected=json.loads((paths.V16_RUN / "origins" / tag / "J_POINT_BOTH" / f"s{SEED}" /
                                                 "fit_summary.json").read_text())["selected_epoch"], models={})
    league = controls.league.to_numpy()
    for name, native in (("capacity", fit["checkpoint_average"]),
                         ("reference", legacy.native(tag, "J_POINT_BOTH", SEED, "checkpoint_average")[1])):
        result["models"][name] = dict(prior=score(native, frame, controls, calibration),
                                      oracle=score(native, frame, controls, oracle(native, frame, league)))
    def mixture(states):
        models = []
        for s in states:
            m = EventModel.from_parent(parent("final"), SEED, defense="capacity")
            m.load_state_dict(s)
            models.append(m.eval())
        return models
    capacity_models = mixture(fit["checkpoint_states"])
    reference_models = checkpoint_models(tag, seeds=(SEED,))
    fx = fixtures()
    for name, models in (("capacity", capacity_models), ("reference", reference_models)):
        result["models"][name]["fixtures"] = {
            f"{a}|{b}": matchup(models, store, fx[a]["pids"], fx[b]["pids"], tag)["margin"] for a, b in FIXTURE_PAIRS}
        if tag == "2026q4":
            offense = property_suite.real_fives(tag, g, evaluate.FIVE)
            defense = property_suite.real_fives(tag, g, legacy.DEFENSE)
            suite = properties.run(lambda o, d, m=models: ledgers(m, store, o, d, tag), store, tag, offense, defense,
                                   offense[:40])
            suite.to_csv(OUT / f"{tag}_{name}_properties.csv", index=False)
            result["models"][name]["properties"] = properties.summarize(suite).pass_rate.to_dict()
        log(f"{name}: {json.dumps({k: v for k, v in result['models'][name].items() if k != 'properties'})}")
    (OUT / f"{tag}.json").write_text(json.dumps(result, indent=1, default=float))
    log("done")


def summary():
    results = [json.loads((OUT / f"{t}.json").read_text()) for t in ORIGINS if (OUT / f"{t}.json").exists()]
    rows = []
    for r in results:
        for name, rec in r["models"].items():
            rows.append(dict(origin=r["origin"], model=name, epoch=r["selected_epoch" if name == "capacity"
                                                                   else "reference_selected"],
                             **{f"{k}_{m}": v for k in ("prior", "oracle") for m, v in rec[k].items()},
                             **{k.split("|")[0][:12] + "|" + k.split("|")[1][6:]: v for k, v in rec["fixtures"].items()}))
    f = pd.DataFrame(rows)
    with pd.option_context("display.width", 240, "display.float_format", "{:.5f}".format):
        print(f.to_string(index=False))
        cap, ref = f[f.model == "capacity"].set_index("origin"), f[f.model == "reference"].set_index("origin")
        for col in ("prior_half", "prior_calibrated", "oracle_half", "oracle_calibrated"):
            d = cap[col] - ref[col]
            print(f"capacity - reference {col}: {d.mean():+.6f}  SE {d.std(ddof=1) / np.sqrt(len(d)):.6f}  "
                  f"positive {int((d > 0).sum())}/{len(d)}")
        for r in results:
            if r["origin"] == "2026q4":
                print(pd.DataFrame({n: rec.get("properties", {}) for n, rec in r["models"].items()}).round(3).to_string())


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--origin")
    p.add_argument("--summary", action="store_true")
    a = p.parse_args()
    summary() if a.summary else run(a.origin)
