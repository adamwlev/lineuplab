"""The record of a retrained release (2026-10-15): hashes of its fits, and the calibration it carries.

The release retrained on the clean data (lineups.page_possessions; scripts/prospective_fit.py --store --out,
run with LINEUPS_CACHE at the rebuild root) is not a freeze. lineups.release reads this record as it reads
the freeze record:

- fits: sha256 of every arm/seed fit in the directory, so the release refuses a changed file;
- calibration: --calibration carried (2026-10-15) takes it from the frozen record (release.FROZEN_RECORD):
  each seed's prior-only affine on the architecture's 2015-2026 history cells (scripts/prospective_freeze.py),
  fitted with reference fits on the old data. --calibration history (2026-10-16, the refresh:
  reports/refresh_protocol_2026_10_16.md) fits the same affine on the history of the active cache root
  (lineups.history): on the clean root, the 2015-2026 refits on the clean data. Under the main cache it
  reproduces the frozen record's calibration;
- league: the level the calibration pulls toward (league + intercept + slope x (native - league)). Carried, it
  is the frozen record's (the additive control's league on the old data); with --calibration history it is
  the same dated league average (lineups.history.league_at, equal to the frozen value on the old data) on
  this root's matchups;
- selected epochs, the store and its manifest hash, and the code commit.

    LINEUPS_CACHE=ROOT/experiments/cache PYTHONPATH=. python -u scripts/release_record.py

Output: <fits>/<--name> (default release_record.json), where fits is the retrained directory (default paths.CACHE/prospective_2027q1
under LINEUPS_CACHE, which must not be the frozen record's).
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from lineups import evaluate, history, legacy, paths, release


def calibrations(start, g=None):
    """Prior-only affine at start on every 2015-2026 quarter's broad cells, per arm and seed (lineups.history)."""
    g = legacy.matchups() if g is None else g
    cells = {(arm, seed): [] for arm in release.ARMS for seed in release.SEEDS}
    for o in legacy.origins().itertuples():
        rows = legacy.row_frame(legacy.quarter_rows(o, g), g)
        league = np.full(len(rows), history.league_at(g, legacy.day(o.start)))
        for (arm, seed), c in cells.items():
            ids, native = history.native(o.tag, seed, "checkpoint_average", arm)
            if not np.array_equal(ids, rows.row.to_numpy()):
                raise ValueError(f"row mismatch at {o.tag}/{arm}/s{seed}")
            c.append(evaluate.history_cells(rows, native, league, o.stop))
    return {f"{arm}_s{seed}": evaluate.affine(pd.concat(c, ignore_index=True), start) for (arm, seed), c in cells.items()}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fits", type=Path, default=paths.CACHE / "prospective_2027q1")
    p.add_argument("--store", type=Path, default=paths.CACHE / "lineups_store_2027q1_library")
    p.add_argument("--calibration", choices=("carried", "history"), default="carried")
    p.add_argument("--name", default="release_record.json",
                   help="record file in --fits (the refresh: release_record_refresh.json, beside the carried one)")
    a = p.parse_args()
    frozen_fits = Path(__file__).resolve().parents[1] / "experiments" / "cache" / "prospective_2027q1"
    if a.fits.resolve() == frozen_fits.resolve():
        p.error("that is the frozen record's directory")
    if (a.fits / a.name).exists():                       # a record is never overwritten; a rerun skips it
        print("exists", a.fits / a.name)
        return
    frozen = json.loads((frozen_fits / "freeze" / "record.json").read_text())
    fits, epochs = {}, {}
    for arm in release.ARMS:
        for seed in release.SEEDS:
            path = a.fits / f"{arm}_s{seed}.pt"
            fits[f"{arm}_s{seed}"] = release._sha256(path)
            saved = torch.load(path, map_location="cpu", weights_only=False)
            if str(Path(saved["store"]).resolve()) != str(a.store.resolve()):
                raise ValueError(f"{path.name} was fitted on {saved['store']}, not {a.store}")
            epochs[f"{arm}_s{seed}"] = dict(offense=int(saved["offense_selected"]), full=int(saved["selected"]))
    record = dict(
        origin=release.ORIGIN, start=frozen["start"], kind="retrained release (not a freeze)",
        commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        store=str(a.store), store_manifest=release._sha256(a.store / "manifest.json"), fits=fits,
        selected_epochs=epochs, additive=dict(league=frozen["additive"]["league"]))
    if a.calibration == "carried":
        record.update(calibration=frozen["calibration"],
                      carried="calibration and league from the frozen record (prior-only affine on the "
                              "architecture's 2015-2026 history, old data)")
    else:
        g = legacy.matchups()
        record.update(calibration=calibrations(frozen["start"], g),
                      additive=dict(league=history.league_at(g, legacy.day(frozen["start"]))),
                      history=dict(clean=history.CLEAN, run=str(history.RUN if history.CLEAN else paths.V16_RUN)),
                      carried="nothing: calibration and league fitted on this cache root's 2015-2026 history and "
                              "matchups (lineups.history)")
    (a.fits / a.name).write_text(json.dumps(record, indent=1))
    print("wrote", a.fits / a.name)


if __name__ == "__main__":
    main()
