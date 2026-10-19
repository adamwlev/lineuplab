"""Build the input store for the 2006-2013 era backtest (protocol: reports/era_backtest_protocol_2026_10_12.md).

- **Schedule.** Quarter windows for the 2002-2013 seasons (lineups.schedule.build).
- **States.** Offense, rebound and defensive states at every origin of that
  schedule, from the ported sweeps (lineups.states).
- **Normalizers and environment.** For each fitted origin (2006-2013) and its
  inner phase (lineups.normalizers). Rows start at FIRST_DAY, the first library
  snapshot.
- **Capability library.** The era snapshots (2001-12-01 to 2009-02-01, from
  scripts/library_extend.py --era) plus the v16 library from 2009-03-01. They
  are compiled with the legacy CapabilityLibrary, so run with
  PYTHONPATH=.:../basketball-legacy.
- **Game-level states and listings.** The v16 store's, linked (they cover every
  game since 2001-10-30).

    PYTHONPATH=.:../basketball-legacy python -u scripts/build_era_store.py

Output: experiments/cache/lineups_store_era (an incomplete build is resumed).
"""
import json
import os

import numpy as np
import pandas as pd

from lineups import legacy, normalizers, paths, schedule as calendar, states

OUT = paths.CACHE / "lineups_store_era"
ERA = paths.CACHE / "capability_library_era_extension"
FIRST_DAY = legacy.day("2001-12-01")
FIRST_FIT_SEASON, LAST_SEASON = 2006, 2013
LINKED = ("offense_games.npz", "defense_games.npz", "players.npz")


def era_library(out):
    """Era snapshot tables followed by the v16 tables, compiled as scripts/export_store.py does."""
    from experiments.joint_capability_v16_features import CapabilityLibrary
    from experiments.joint_capability_v16_library import BANKS, FAMILIES, SCHEMA
    as_day = lambda name: int(np.datetime64(name, "D").astype(np.int64))
    dates = sorted(as_day(p.name) for p in (ERA / "chains" / "offense" / "counts" / "snapshots").iterdir())
    for bank in BANKS:
        for family in FAMILIES:
            have = sorted(as_day(p.name) for p in (ERA / "chains" / bank / family / "snapshots").iterdir()
                          if (p / "complete.json").exists())
            if have != dates or len(dates) != 87:
                raise ValueError(f"era chain {bank}/{family} is incomplete ({len(have)} of 87)")
    (ERA / "manifest.json").write_text(json.dumps(dict(schema=SCHEMA, dates=dates, full_coverage=False,
                                                       banks=list(BANKS), families=list(FAMILIES)), indent=1))
    library = CapabilityLibrary(ERA, allow_partial=True, required=dates)
    for bank in BANKS:
        ids, values, last, offsets = [], [], [], [0]
        for d in dates:
            library.features(np.zeros((1, 5), np.int64), np.array([d]), bank, metadata=False)
            t = library.feature_cache.pop((int(d), bank))
            ids.append(t["ids"]); values.append(t["values"]); last.append(t["last"])
            offsets.append(offsets[-1] + len(t["ids"]))
            library.cache.clear()
        with np.load(paths.STORE / f"library_{bank}.npz") as old:
            if not dates[-1] < old["dates"][0]:
                raise ValueError("era snapshots overlap the v16 library")
            np.savez(out / f"library_{bank}.npz", dates=np.r_[dates, old["dates"]].astype(np.int64),
                     offsets=np.r_[offsets[:-1], offsets[-1] + old["offsets"]].astype(np.int64),
                     ids=np.concatenate(ids + [old["ids"]]), values=np.concatenate(values + [old["values"]]),
                     last=np.concatenate(last + [old["last"]]))
    # The v16 part must read back unchanged.
    for bank in BANKS:
        with np.load(paths.STORE / f"library_{bank}.npz") as old, np.load(out / f"library_{bank}.npz") as new:
            n, k = len(dates), int(new["offsets"][len(dates)])
            assert np.array_equal(new["dates"][n:], old["dates"])
            assert np.array_equal(new["offsets"][n:] - k, old["offsets"])
            for key in ("ids", "values", "last"):
                assert np.array_equal(new[key][k:], old[key]), key


def main():
    if (OUT / "manifest.json").exists():
        raise FileExistsError(f"{OUT} is complete")
    (OUT / "normalizers").mkdir(parents=True, exist_ok=True)
    sched_path = OUT / "schedule.csv"
    if not sched_path.exists():
        calendar.build(2002, LAST_SEASON).to_csv(sched_path, index=False, date_format="%Y-%m-%d")
    schedule = pd.read_csv(sched_path, parse_dates=["start", "stop"])
    print("schedule", len(schedule), "windows", schedule.start.min().date(), schedule.stop.max().date(), flush=True)

    origins, (offense, rebound) = states.origin_states(schedule)
    states.write_origins(OUT, origins)
    with np.load(states.REBOUND_LABELS) as z:
        labels = {k: z[k] for k in z.files}
    for name in LINKED:
        if not (OUT / name).is_symlink():
            os.symlink(paths.STORE / name, OUT / name)
    (OUT / "references.json").write_text("{}")       # era fits normalize by their own starting model
    if not (OUT / "library_offense.npz").exists() or not (OUT / "library_defense.npz").exists():
        era_library(OUT)
    print("library written", flush=True)

    from lineups.features import Store
    (OUT / "environment.json").write_text("{}")
    store = Store(OUT)
    with np.load(states.GAME_LINEUPS) as z:
        grouped = {k: z[k] for k in z.files}
    s = legacy.schedule(sched_path)
    environment = {}
    for origin in s[s.season >= FIRST_FIT_SEASON].itertuples():
        inner = s[s.stop <= origin.start].iloc[-1]
        for phase, cutoff in (("inner", legacy.day(inner.start)), ("final", legacy.day(origin.start))):
            path = OUT / "normalizers" / f"{origin.tag}_{phase}.npz"
            if not path.exists():
                norm = normalizers.lineup_normalizers(grouped, offense, rebound, cutoff, FIRST_DAY)
                norm |= normalizers.matchup_normalizers(legacy.matchups(), store, cutoff, FIRST_DAY)
                np.savez(path, **norm)
            environment[f"{origin.tag}/{phase}"] = normalizers.environment(grouped, labels["counts"], cutoff)
        print("normalizers", origin.tag, flush=True)
    (OUT / "environment.json").write_text(json.dumps(environment, indent=1, default=float))
    (OUT / "manifest.json").write_text(json.dumps(dict(
        created=str(pd.Timestamp.now().date()), seasons=[2002, LAST_SEASON], fitted_origins=f"{FIRST_FIT_SEASON}-{LAST_SEASON}",
        first_day="2001-12-01", library=dict(era=str(ERA), v16=str(paths.STORE)),
        linked=list(LINKED)), indent=1))
    print("built", OUT, flush=True)


if __name__ == "__main__":
    main()
