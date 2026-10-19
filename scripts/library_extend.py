"""Extend the capability library from 2026-03-02 to opening night, 2026-10-20 (legacy code, refactor rung 5).

The v16 library (joint_capability_2026_09_18_v16_library_full1) stops at the
last backtest origin. At 2027q1 the store would therefore query a snapshot 7.5
months old; scripts/library_staleness_check.py measures what that costs
(-0.0067 +- 0.0044 half r^2 at past opening quarters).

This runs the unchanged chain code of tag pre-refactor-2026-10-09
(joint_capability_v16_library.snapshot and .tune) for the snapshot dates that
the legacy calendar requires after 2026-03-02 once origin 2027q1 (start
2026-10-20) is in the schedule: monthly from 2026-04-01 to 2026-10-01, plus
2026-10-20. Each chain warm-starts from the saved 2026-03-02 state. Snapshots
before 2026-10-20 reuse the saved season-2026 penalty. The 2026-10-20 snapshot
gets a new season-2027 selection (validated on 2026q4, trained before
2026-03-02), as the legacy chain would make it.

Run from the legacy worktree, one process per bank and family:

    cd ../basketball-legacy && PYTHONPATH=. python -u ../basketball/scripts/library_extend.py --bank offense --family counts
    ... --check   # rebuild the saved 2026-03-02 snapshot from the 2026-03-01 state and compare
    ... --tune    # only the season-2027 penalty choice, which needs no snapshot, so it can run ahead

Output: experiments/cache/capability_library_2027q1_extension/chains/<bank>/<family>/.

Era mode (--era) adds the monthly snapshots before the v16 library's first
(2009-03-01), from 2001-12-01 to 2009-02-01, for the 2006-2013 era backtest.
Like the saved snapshots before the first registered season opening (2014),
they all use the cold penalty (1000) with no annual tuning. --segment k/n runs
the k-th of n contiguous date blocks. Each block starts without a warm start,
which changes only the starting point of a converged fit.

    ... library_extend.py --era --bank offense --family location --segment 1/3

Output: experiments/cache/capability_library_era_extension/chains/<bank>/<family>/.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.joint_capability_data import source_paths
from experiments.joint_capability_repro import no_database
from experiments.joint_capability_v16_inputs import LeagueOffsets, day
from experiments.joint_capability_v16_library import (BANKS, FAMILIES, date_name, required_dates, selection_event,
                                                      snapshot, tune)
from experiments.joint_capability_v16_storage import load_arrays

FULL = Path("experiments/cache/joint_capability_2026_09_18_v16_library_full1")
OUT = Path("experiments/cache/capability_library_2027q1_extension")
CHECK = Path("experiments/cache/capability_library_2027q1_extension_check")
ERA = Path("experiments/cache/capability_library_era_extension")
ERA_DATES = np.arange(np.datetime64("2001-12"), np.datetime64("2009-03"), dtype="datetime64[M]").astype("datetime64[D]")
COLD = dict(cold=True, penalty=1000.0, reason="no registered season-opening quarter yet", selection_cutoff=None,
            training_cutoff=None, validation=None)        # what the saved pre-2014 snapshots record
LAST_SAVED = "2026-03-02"
NEW_ORIGIN = dict(season=2027, window=1, start=pd.Timestamp("2026-10-20"), stop=pd.Timestamp("2026-12-01"))


def extended_schedule():
    s = pd.read_csv(source_paths()["schedule"], parse_dates=["start", "stop"])
    s = pd.concat([s, pd.DataFrame([NEW_ORIGIN])], ignore_index=True)
    s["tag"] = s.season.astype(str) + "q" + s.window.astype(str)
    s["origin_index"] = np.arange(len(s))
    return s


def new_dates(schedule):
    dates = required_dates(schedule)
    saved = json.loads((FULL / "manifest.json").read_text())["dates"]
    if dates[dates <= day(LAST_SAVED)].tolist() != saved:
        raise ValueError("the extended calendar does not reproduce the saved snapshot dates")
    return dates[dates > day(LAST_SAVED)]


def load_state(bank, family, name):
    with np.load(FULL / "chains" / bank / family / "snapshots" / name / "state.npz") as z:
        return {k: z[k] for k in z.files}


def saved_choice(bank, family, season):
    path = FULL / "chains" / bank / family / "penalties" / str(season) / "selection.json"
    return json.loads(path.read_text()) if path.exists() else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bank", choices=BANKS, required=True)
    p.add_argument("--family", choices=FAMILIES, required=True)
    p.add_argument("--check", action="store_true")
    p.add_argument("--tune", action="store_true")
    p.add_argument("--era", action="store_true")
    p.add_argument("--segment", default="1/1")
    a = p.parse_args()
    if a.era:
        return era(a.bank, a.family, a.segment)
    schedule = extended_schedule()
    g = load_arrays(FULL / "mapped_matchups")
    offsets = LeagueOffsets(g, a.bank, a.family)
    with no_database():
        if a.check:
            cutoff = day(LAST_SAVED)
            choice = saved_choice(a.bank, a.family, selection_event(schedule, cutoff)["season"])
            state = snapshot(g, offsets, a.bank, a.family, cutoff, choice,
                             CHECK / a.bank / a.family / LAST_SAVED, load_state(a.bank, a.family, "2026-03-01"))
            saved = load_state(a.bank, a.family, LAST_SAVED)
            for k in ("ids", "history_ids", "history_last_seen", "last_seen"):
                np.testing.assert_array_equal(state[k], saved[k], err_msg=k)
            for k in ("intercept", "coefficients", "std", "support", "neff", "offset"):
                diff = float(np.max(np.abs(np.asarray(state[k], float) - np.asarray(saved[k], float))))
                print(f"  {k}: max |diff| {diff:.2e}", flush=True)
            print("CHECK_DONE", a.bank, a.family, flush=True)
            return
        out = OUT / "chains" / a.bank / a.family
        if a.tune:
            event = selection_event(schedule, int(new_dates(schedule)[-1]))
            choice = saved_choice(a.bank, a.family, event["season"]) or tune(
                g, offsets, a.bank, a.family, event, out / "penalties" / str(event["season"]))
            print(f"TUNED {a.bank}/{a.family} {event['season']} penalty={choice['penalty']:g}", flush=True)
            return
        previous, choices = load_state(a.bank, a.family, LAST_SAVED), {}
        for cutoff in new_dates(schedule):
            event = selection_event(schedule, int(cutoff))
            season = None if event is None else event["season"]
            if season not in choices:
                choices[season] = saved_choice(a.bank, a.family, season) or tune(
                    g, offsets, a.bank, a.family, event, out / "penalties" / str(season))
            previous = snapshot(g, offsets, a.bank, a.family, int(cutoff), choices[season],
                                out / "snapshots" / date_name(cutoff), previous)
            print(f"EXTENDED {a.bank}/{a.family} {date_name(cutoff)} penalty={choices[season]['penalty']:g}",
                  flush=True)


def era(bank, family, segment):
    k, n = map(int, segment.split("/"))
    dates = np.array_split(ERA_DATES.astype(np.int64), n)[k - 1]
    g = load_arrays(FULL / "mapped_matchups")
    offsets = LeagueOffsets(g, bank, family)
    out, previous = ERA / "chains" / bank / family, None
    with no_database():
        for cutoff in dates:
            previous = snapshot(g, offsets, bank, family, int(cutoff), COLD, out / "snapshots" / date_name(cutoff),
                                previous)
            print(f"ERA {bank}/{family} {date_name(cutoff)} segment {segment}", flush=True)


if __name__ == "__main__":
    main()
