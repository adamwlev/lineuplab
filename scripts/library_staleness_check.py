"""How much does a stale capability library cost at a season-opening origin? (exploratory)

The 2027q1 store queries the capability library at its latest snapshot,
2026-03-02, because the library has no later snapshot. Every backtest origin
had a snapshot at its own start. This check imitates the 2027q1 situation at
past opening quarters: the library is cut at the previous season's quarter-4
start (about 7.5 months before opening night), and origin-mode forecasts of the
saved reference (J_POINT_BOTH, seed 17, checkpoint mixture) are compared with
the normal ones on the same outer rows, with the same calibration.

Not imitated: the 2027q1 fit's final-phase training rows after March also see
the stale library (the saved fits trained with monthly snapshots).

    PYTHONPATH=.:scripts python -u scripts/library_staleness_check.py
"""
import copy
import json

import numpy as np
import torch

from capacity_screen import score
from coverage_screen import reference_calibration
from lineups import legacy, paths
from lineups.coherence import checkpoint_models
from lineups.features import Store
from lineups.train import Rows, evaluate

OUT = paths.CACHE / "library_staleness_check_2026_10_09"
SEED = 17


def stale(store, last_day):
    """A store whose library ends at the last snapshot on or before last_day."""
    s = copy.copy(store)
    s.library = {}
    for bank, lib in store.library.items():
        k = int(np.searchsorted(lib["dates"], last_day, side="right"))
        s.library[bank] = dict(lib, dates=lib["dates"][:k], offsets=lib["offsets"][:k + 1])
    return s


def main():
    torch.set_num_threads(1)
    OUT.mkdir(parents=True, exist_ok=True)
    store, g, schedule = Store(), legacy.matchups(), legacy.schedule()
    for o in schedule[(schedule.window == 1) & (schedule.season >= 2016)].itertuples():
        march = schedule[(schedule.season == o.season - 1) & (schedule.window == 4)].iloc[0]
        models = checkpoint_models(o.tag, seeds=(SEED,))
        states = [copy.deepcopy(m.state_dict()) for m in models]   # state_dict() aliases live parameters
        norm, env = store.normalizer(o.tag, "final"), store.env(o.tag, "final")
        rows = legacy.quarter_rows(o, g)
        frame = legacy.row_frame(rows, g)
        controls, calibration = legacy.controls(o.tag, SEED), reference_calibration(o.tag)
        result = dict(origin=o.tag, stale_snapshot=str(march.start.date()))
        native = {}
        for name, s in (("fresh", store), ("stale", stale(store, legacy.day(march.start)))):
            _, ids, native[name] = evaluate(models[0], Rows(g, s), rows, norm, env, origin_index=int(o.origin_index),
                                            checkpoints=states)
            assert np.array_equal(ids, frame.row.to_numpy())
            result[name] = score(native[name], frame, controls, calibration)
        saved = legacy.native(o.tag, "J_POINT_BOTH", SEED, "checkpoint_average")[1]
        result["fresh_vs_saved_max"] = float(np.max(np.abs(native["fresh"] - saved)))
        w = frame.possessions.to_numpy(float)
        d = native["stale"] - native["fresh"]
        result["native_shift_mean"] = float(np.average(d, weights=w))
        result["native_shift_rms"] = float(np.sqrt(np.average(d ** 2, weights=w)))
        print(json.dumps(result), flush=True)
        with open(OUT / "results.jsonl", "a") as f:
            f.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    main()
