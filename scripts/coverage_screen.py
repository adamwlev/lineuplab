"""Exploratory screen: does an explicit coverage assignment change the defense? (2026-10-09)

Design, fixed before running:

* Arms, each warm-started from the saved J_POINT_BOTH final weights (seed 17)
  at the origin and trained FIT_EPOCHS more epochs on the same final-phase
  rows, objective, optimizer settings and batch order:
    control       the reference, continued unchanged;
    matched       + Coverage(matched=True): per-attacker effects from the
                  defender assigned by sorted listed position;
    matched_help  + Coverage(matched=True, help_term=True): also team help
                  discounted when the helper's assigned attacker is a spacer.
  Coverage starts at exactly zero, so every arm starts at the same function.
* Origins: 2017q2 2018q3 2019q4 2021q2 2022q3 2023q4 2025q2 2026q4.
* Contrast 1 (accuracy, non-inferiority): outer-quarter broad cells (>= 50
  possessions), possession-weighted, actual defenses. Native forecasts get
  the reference's own prior-only calibration at that origin, then the half
  blend with additive_defense. Arm minus control in r^2, mean over origins
  with origin-level SE. Margin: -0.003.
* Contrast 2 (pillar 2): native fixture margins at 2026q4 (legal centers vs
  Jokic/Westbrook and Jokic/Korver, five Goberts vs Jokic/Westbrook) and the
  property suite at 2026q4.
* Also recorded: outer event objective, kappa, spread of coverage effects.

Single seed, warm start, few origins: a screen for direction and magnitude,
not a registered result.

    PYTHONPATH=. python -u scripts/coverage_screen.py --origin 2026q4
    PYTHONPATH=. python -u scripts/coverage_screen.py --summary
"""
import argparse
import copy
import json
import time

import numpy as np
import pandas as pd
import torch

import property_suite
from lineups import evaluate, legacy, paths, properties
from lineups.coherence import fixtures, ledgers, matchup
from lineups.features import Store
from lineups.model import Coverage, load_legacy
from lineups.train import FitConfig, Rows, evaluate as evaluate_rows, train, validation_score

OUT = paths.CACHE / "coverage_screen_2026_10_09"
ORIGINS = ("2017q2", "2018q3", "2019q4", "2021q2", "2022q3", "2023q4", "2025q2", "2026q4")
SEED, FIT_EPOCHS = 17, 4
ARMS = dict(control=None, matched=dict(matched=True, help_term=False), matched_help=dict(matched=True, help_term=True))
FIXTURE_PAIRS = (("legal_pure_centers", "jokic_westbrook"), ("legal_pure_centers", "jokic_korver"),
                 ("five_goberts", "jokic_westbrook"), ("five_jokics", "jokic_westbrook"))


def reference_calibration(tag):
    """The reference's prior-only affine calibration (seed 17, direct) at an origin."""
    g = legacy.matchups()
    history = []
    for o in legacy.origins().itertuples():
        if o.tag == tag:
            return evaluate.affine(pd.concat(history, ignore_index=True) if history else None, o.start)
        rows = legacy.row_frame(legacy.quarter_rows(o, g), g)
        ids, native = legacy.native(o.tag, "J_POINT_BOTH", SEED, "direct")
        league = legacy.controls(o.tag, SEED).league.to_numpy()
        assert np.array_equal(ids, rows.row.to_numpy())
        history.append(evaluate.history_cells(rows, native, league, o.stop))
    raise KeyError(tag)


def run(tag):
    torch.set_num_threads(1)
    OUT.mkdir(parents=True, exist_ok=True)
    tick = time.monotonic()
    log = lambda m: print(f"[{tag} {time.monotonic() - tick:6.0f}s] {m}", flush=True)
    store, g = Store(), legacy.matchups()
    data = Rows(g, store)
    origin = legacy.schedule().query("tag == @tag").iloc[0]
    normalizer, env = store.normalizer(tag, "final"), store.env(tag, "final")
    reference = store.references[f"{tag}/final/s{SEED}"]
    fit_rows = data.prefix(legacy.day(origin.start), FitConfig().lookback_days)
    outer = data.window(legacy.day(origin.start), legacy.day(origin.stop))
    case = paths.V16_RUN / "origins" / tag / "J_POINT_BOTH" / f"s{SEED}" / "final"
    saved = load_legacy(torch.load(case / "fit.pt", map_location="cpu", weights_only=False)["state_dict"])
    frame = legacy.row_frame(outer, g)
    controls = legacy.controls(tag, SEED)
    assert np.array_equal(controls.row.to_numpy(), frame.row.to_numpy())
    calibration = reference_calibration(tag)
    fx = fixtures()
    result = dict(origin=tag, calibration=calibration, arms={})
    for arm, coverage in ARMS.items():
        model = copy.deepcopy(saved)
        if coverage is not None:
            with torch.random.fork_rng():
                torch.manual_seed(SEED + 1700)
                model.coverage = Coverage(**coverage)
        log(f"{arm}: training {FIT_EPOCHS} epochs on {len(fit_rows):,} rows")
        train(model, data, fit_rows, normalizer, env, reference, SEED, epochs=FIT_EPOCHS, log=log)
        totals, rows, native = evaluate_rows(model, data, outer, normalizer, env, origin_index=int(origin.origin_index))
        assert np.array_equal(rows, frame.row.to_numpy())
        league = controls.league.to_numpy()
        calibrated = evaluate.calibrate(calibration, native, league)
        f = frame.assign(native=native, calibrated=calibrated,
                         half=.5 * controls.additive_defense.to_numpy() + .5 * calibrated)
        cells = evaluate.cells(f, ["native", "calibrated", "half"])
        cells = cells[cells.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        stats = {m: evaluate.sufficient(cells.actual, cells[m], cells.possessions) for m in ("calibrated", "half")}
        rec = dict(event_objective=validation_score(totals, reference, FitConfig()),
                   stats=stats, metrics={m: evaluate.metrics(s) for m, s in stats.items()})
        np.savez(OUT / f"{tag}_{arm}.npz", row=rows, native=native)
        torch.save(model.state_dict(), OUT / f"{tag}_{arm}.pt")
        if model.coverage is not None and model.coverage.has_help:
            rec["kappa"] = float(model.coverage.kappa())
        rec["fixtures"] = {f"{a}|{b}": {k: v for k, v in matchup(model, store, fx[a]["pids"], fx[b]["pids"], tag).items()
                                        if k in ("a_offense", "b_offense", "margin")} for a, b in FIXTURE_PAIRS}
        if tag == "2026q4":
            offense = property_suite.real_fives(tag, g, evaluate.FIVE)
            defense = property_suite.real_fives(tag, g, legacy.DEFENSE)
            predict = lambda o, d, m=model: ledgers(m, store, o, d, tag)
            suite = properties.run(predict, store, tag, offense, defense, offense[:40])
            suite.to_csv(OUT / f"{tag}_{arm}_properties.csv", index=False)
            rec["properties"] = properties.summarize(suite).pass_rate.to_dict()
        result["arms"][arm] = rec
        log(f"{arm}: r2 half {rec['metrics']['half']['r2']:.6f} calibrated {rec['metrics']['calibrated']['r2']:.6f} "
            f"event {rec['event_objective']:.6f} centers-vs-westbrook "
            f"{rec['fixtures']['legal_pure_centers|jokic_westbrook']['margin']:+.2f}")
    (OUT / f"{tag}.json").write_text(json.dumps(result, indent=1, default=float))
    log("done")


def summary():
    results = [json.loads((OUT / f"{t}.json").read_text()) for t in ORIGINS if (OUT / f"{t}.json").exists()]
    rows = []
    for r in results:
        for arm, rec in r["arms"].items():
            rows.append(dict(origin=r["origin"], arm=arm, r2_half=rec["metrics"]["half"]["r2"],
                             r2_cal=rec["metrics"]["calibrated"]["r2"], event=rec["event_objective"],
                             kappa=rec.get("kappa", np.nan),
                             **{k: v["margin"] for k, v in rec["fixtures"].items()}))
    f = pd.DataFrame(rows)
    base = f[f.arm == "control"].set_index("origin")
    with pd.option_context("display.width", 220, "display.float_format", "{:.5f}".format):
        print(f.to_string(index=False))
        for arm in ARMS:
            if arm == "control":
                continue
            d = f[f.arm == arm].set_index("origin")
            for col in ("r2_half", "r2_cal", "event"):
                diff = d[col] - base[col]
                print(f"{arm} - control {col}: mean {diff.mean():+.6f}  SE {diff.std(ddof=1) / np.sqrt(len(diff)):.6f}"
                      f"  positive {int((diff > 0).sum())}/{len(diff)}")
        for r in results:
            if r["origin"] == "2026q4":
                print(pd.DataFrame({a: rec.get("properties", {}) for a, rec in r["arms"].items()}).round(3).to_string())


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--origin")
    p.add_argument("--summary", action="store_true")
    a = p.parse_args()
    summary() if a.summary else run(a.origin)
