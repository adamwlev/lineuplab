"""Exploratory screen: does reading specific teammates (best passer, best shooter) change the offense?

Design, fixed before running:

* Both arms are warm-started from the version-2 capacity screen's final
  weights (seed 17) at each of its eight origins and trained FIT_EPOCHS more
  epochs on the same rows, objective and batch order:
    control   the capacity model, continued;
    creation  + lineups.model.Creation (zero at the start, so both arms start
              at the same function).
* Accuracy: outer broad cells, direct view, half blend, the reference's
  prior-only calibration and an oracle in-quarter affine (as
  scripts/capacity_screen.py). Arm minus control, mean over origins.
* Offense coherence: native offense against a neutral defense for five
  Goberts, legal centers, Jokic/Westbrook and the real Minnesota five; native
  fixture margins; the property suite at 2026q4.
* Real low-creation cells: outer rows whose best passer is below 5 assists per
  100, residual of the half blend (prior calibration).

    PYTHONPATH=. python -u scripts/creation_screen.py
"""
import copy
import json
import time

import numpy as np
import pandas as pd
import torch

import property_suite
from capacity_screen import V14, oracle, score
from coverage_screen import FIT_EPOCHS, FIXTURE_PAIRS, ORIGINS, SEED, reference_calibration
from creation_analogues import LOW_CREATION_AST, roles
from lineups import evaluate, legacy, paths, properties
from lineups.coherence import fixtures, ledgers, matchup
from lineups.features import Store
from lineups.model import Creation, EventModel
from lineups.train import Rows, evaluate as evaluate_rows, train

SOURCE = paths.CACHE / "capacity_v2_screen_2026_10_09"
OUT = paths.CACHE / "creation_screen_2026_10_09"
NEUTRAL = ("five_goberts", "legal_pure_centers", "jokic_westbrook", "highest_exposure_real_2026")


def capacity_model(tag):
    parent = torch.load(V14 / "origins" / tag / "RB_RENEW_FAC" / f"s{SEED}" / "final.pt", map_location="cpu",
                        weights_only=False)["state_dict"]
    model = EventModel.from_parent(parent, SEED, defense="capacity")
    model.load_state_dict(torch.load(SOURCE / f"{tag}.pt", map_location="cpu", weights_only=False)["final"])
    return model


def run(tag, store, g, data, fx, log):
    origin = legacy.schedule().query("tag == @tag").iloc[0]
    normalizer, env = store.normalizer(tag, "final"), store.env(tag, "final")
    reference = store.references[f"{tag}/final/s{SEED}"]
    fit_rows = data.prefix(legacy.day(origin.start), 5 * 365)
    outer = data.window(legacy.day(origin.start), legacy.day(origin.stop))
    frame = legacy.row_frame(outer, g)
    controls = legacy.controls(tag, SEED)
    calibration = reference_calibration(tag)
    assist = roles(store, int(origin.origin_index), np.unique(frame[evaluate.FIVE].to_numpy()))["assist"]
    weak = assist.reindex(frame[evaluate.FIVE].to_numpy().ravel()).to_numpy().reshape(-1, 5).max(1) < LOW_CREATION_AST
    result = {}
    for arm in ("control", "creation"):
        model = copy.deepcopy(capacity_model(tag))
        if arm == "creation":
            with torch.random.fork_rng():
                torch.manual_seed(SEED + 1800)
                model.creation = Creation()
        train(model, data, fit_rows, normalizer, env, reference, SEED, epochs=FIT_EPOCHS, log=log)
        _, rows, native = evaluate_rows(model, data, outer, normalizer, env, origin_index=int(origin.origin_index))
        assert np.array_equal(rows, frame.row.to_numpy())
        league = controls.league.to_numpy()
        half = .5 * controls.additive_defense.to_numpy() + .5 * evaluate.calibrate(calibration, native, league)
        actual = 100 * frame.points / frame.possessions
        w = frame.possessions.to_numpy()
        rec = dict(prior=score(native, frame, controls, calibration),
                   oracle=score(native, frame, controls, oracle(native, frame, league)),
                   weak_passer_residual=float(np.average((actual - half)[weak], weights=w[weak])),
                   weak_passer_possessions=int(w[weak].sum()))
        neutral = ledgers(model, store, np.array([fx[k]["pids"] for k in NEUTRAL]), None, tag).points100.numpy()
        rec["neutral_offense"] = dict(zip(NEUTRAL, map(float, neutral)))
        rec["fixtures"] = {f"{a}|{b}": matchup(model, store, fx[a]["pids"], fx[b]["pids"], tag)["margin"]
                           for a, b in FIXTURE_PAIRS}
        if tag == "2026q4":
            offense = property_suite.real_fives(tag, g, evaluate.FIVE)
            defense = property_suite.real_fives(tag, g, legacy.DEFENSE)
            suite = properties.run(lambda o, d, m=model: ledgers(m, store, o, d, tag), store, tag, offense, defense,
                                   offense[:40])
            rec["properties"] = properties.summarize(suite).pass_rate.to_dict()
        result[arm] = rec
        log(f"{arm}: {json.dumps({k: v for k, v in rec.items() if k != 'properties'})}")
    return result


def main():
    torch.set_num_threads(1)
    OUT.mkdir(parents=True, exist_ok=True)
    store, g, fx = Store(), legacy.matchups(), fixtures()
    data = Rows(g, store)
    results = {}
    for tag in ORIGINS:
        tick = time.monotonic()
        results[tag] = run(tag, store, g, data, fx, lambda m: print(f"[{tag} {time.monotonic() - tick:6.0f}s] {m}",
                                                                     flush=True))
        (OUT / "results.json").write_text(json.dumps(results, indent=1, default=float))
    rows = []
    for tag, r in results.items():
        for arm, rec in r.items():
            rows.append(dict(origin=tag, arm=arm, half_prior=rec["prior"]["half"], half_oracle=rec["oracle"]["half"],
                             weak=rec["weak_passer_residual"], **{f"neutral_{k[:12]}": v for k, v in
                                                                 rec["neutral_offense"].items()},
                             **{k.split("|")[0][:12] + "|" + k.split("|")[1][6:]: v
                                for k, v in rec["fixtures"].items()}))
    f = pd.DataFrame(rows)
    with pd.option_context("display.width", 260, "display.float_format", "{:.4f}".format):
        print(f.to_string(index=False))
        c, x = f[f.arm == "control"].set_index("origin"), f[f.arm == "creation"].set_index("origin")
        for col in [k for k in f.columns if k not in ("origin", "arm")]:
            d = x[col] - c[col]
            print(f"creation - control {col}: {d.mean():+.4f}  SE {d.std(ddof=1) / np.sqrt(len(d)):.4f}  "
                  f"positive {int((d > 0).sum())}/{len(d)}")
        if "2026q4" in results:
            print(pd.DataFrame({a: rec["properties"] for a, rec in results["2026q4"].items()}).round(3).to_string())


if __name__ == "__main__":
    main()
