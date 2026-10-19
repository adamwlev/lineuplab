"""Build the input store for the 2026-27 prospective origin (2027q1, opening night 2026-10-20).

No new data: the latest game is 2026-06-13. The new origin's states are the
ported sweeps' states as of opening night (lineups.states), and its
normalizers and environment come from lineups.normalizers on the five-year
prefix before it. Game-level tables are the v16 store's, linked rather than
copied.

Capability library:
- default (the first build, lineups_store_2027q1): the v16 library, linked.
  Origin-mode queries at 2026-10-20 then use its last snapshot (2026-03-02),
  with staleness recomputed.
- --library-extension DIR (lineups_store_2027q1_library): the v16 tables plus
  the snapshots after 2026-03-02 made by scripts/library_extend.py
  (2026-04-01 to 2026-10-20). They are compiled with the legacy
  CapabilityLibrary, so the legacy worktree must be on the path:
  PYTHONPATH=.:../basketball-legacy.

The window's stop date is provisional: windows end when the league's game count
crosses 300, which is known only after the games. Scoring uses the realized
window.

Checks: origins 0-51 of the rebuilt origin tables equal the v16 store exactly;
library tables up to 2026-03-02 equal the v16 tables.

    PYTHONPATH=. python -u scripts/build_prospective_store.py
    PYTHONPATH=.:../basketball-legacy python -u scripts/build_prospective_store.py \
        --library-extension experiments/cache/capability_library_2027q1_extension \
        --out experiments/cache/lineups_store_2027q1_library
"""
import argparse
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from lineups import legacy, normalizers, paths, states

OUT = paths.CACHE / "lineups_store_2027q1"
NEW = dict(season=2027, window=1, start=pd.Timestamp("2026-10-20"), stop=pd.Timestamp("2026-12-01"), n_games=0,
           prior_season_games=0)
LINKED = ("offense_games.npz", "defense_games.npz", "players.npz", "references.json")
LIBRARY = ("library_offense.npz", "library_defense.npz")


def extended_library(out, extension):
    """v16 library tables plus the extension's snapshots, compiled exactly as scripts/export_store.py does."""
    from experiments.joint_capability_v16_features import CapabilityLibrary
    from experiments.joint_capability_v16_library import BANKS, FAMILIES, SCHEMA
    as_day = lambda name: int(np.datetime64(name, "D").astype(np.int64))
    dates = sorted(as_day(p.name) for p in (extension / "chains" / "offense" / "counts" / "snapshots").iterdir())
    for bank in BANKS:
        for family in FAMILIES:
            have = sorted(as_day(p.name) for p in (extension / "chains" / bank / family / "snapshots").iterdir()
                          if (p / "complete.json").exists())
            if have != dates:
                raise ValueError(f"extension chain {bank}/{family} is incomplete")
    (extension / "manifest.json").write_text(json.dumps(dict(schema=SCHEMA, dates=dates, full_coverage=False,
                                                             banks=list(BANKS), families=list(FAMILIES)), indent=1))
    library = CapabilityLibrary(extension, allow_partial=True, required=dates)
    for bank in BANKS:
        with np.load(paths.STORE / f"library_{bank}.npz") as old:
            ids, values, last, offsets = [old["ids"]], [old["values"]], [old["last"]], list(old["offsets"])
            old_dates = old["dates"]
        if not old_dates[-1] < dates[0]:
            raise ValueError("extension overlaps the v16 library")
        for d in dates:
            library.features(np.zeros((1, 5), np.int64), np.array([d]), bank, metadata=False)
            t = library.feature_cache.pop((int(d), bank))
            ids.append(t["ids"]); values.append(t["values"]); last.append(t["last"])
            offsets.append(offsets[-1] + len(t["ids"]))
            library.cache.clear()
        np.savez(out / f"library_{bank}.npz", dates=np.r_[old_dates, dates].astype(np.int64),
                 offsets=np.asarray(offsets, np.int64), ids=np.concatenate(ids), values=np.concatenate(values),
                 last=np.concatenate(last))
    return [str(np.datetime64(d, "D")) for d in dates]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=OUT)
    p.add_argument("--library-extension", type=Path)
    a = p.parse_args()
    build(a.out, a.library_extension)


def build(out, extension):
    if (out / "manifest.json").exists():
        raise FileExistsError(f"{out} is complete")
    (out / "normalizers").mkdir(parents=True, exist_ok=True)      # an incomplete build is resumed
    base_schedule = pd.read_csv(paths.SCHEDULE, parse_dates=["start", "stop"])
    schedule = pd.concat([base_schedule, pd.DataFrame([NEW])], ignore_index=True)
    schedule.to_csv(out / "schedule.csv", index=False, date_format="%Y-%m-%d")
    new_index = len(schedule) - 1

    origins, (offense, rebound) = states.origin_states(schedule)
    states.write_origins(out, origins)
    with np.load(states.REBOUND_LABELS) as z:
        labels = {k: z[k] for k in z.files}
    for name in LINKED + (() if extension else LIBRARY):
        if not (out / name).is_symlink():
            os.symlink(paths.STORE / name, out / name)
    extension_dates = extended_library(out, extension) if extension else []
    for name in LIBRARY if extension else ():
        with np.load(paths.STORE / name) as old, np.load(out / name) as new:
            n = len(old["dates"])
            if not (np.array_equal(old["dates"], new["dates"][:n]) and np.array_equal(old["offsets"], new["offsets"][:n + 1])):
                raise ValueError(f"{name}: v16 dates/offsets changed")
            for k in ("ids", "values", "last"):
                if not np.array_equal(old[k], new[k][:old["offsets"][-1]]):
                    raise ValueError(f"{name}:{k} differs from the v16 library before the extension")
    for f in (paths.STORE / "normalizers").iterdir():
        if not (out / "normalizers" / f.name).is_symlink():
            os.symlink(f, out / "normalizers" / f.name)

    # Exactness for the 52 v16 origins.
    for name, keys in (("offense_origins.npz", ("origin_index", "pid", "base", "role", "rb_prob", "rb_neff")),
                       ("defense_origins.npz", ("origin_index", "pid", "x"))):
        with np.load(paths.STORE / name) as old, np.load(out / name) as new:
            keep = new["origin_index"] < new_index
            for k in keys:
                if not np.array_equal(old[k], new[k][keep]):
                    raise ValueError(f"{name}:{k} differs from the v16 store for origins 0-51")
            for k in [k for k in old.files if k.startswith("fallback") or k == "league"]:
                if not np.array_equal(old[k], new[k][:new_index]):
                    raise ValueError(f"{name}:{k} fallback differs")

    # Normalizers and environment for the new origin: inner = previous quarter's start (2026q4), final = opening night.
    environment = json.loads((paths.STORE / "environment.json").read_text())
    (out / "environment.json").write_text(json.dumps(environment, indent=1, default=float))
    with np.load(states.GAME_LINEUPS) as z:
        grouped = {k: z[k] for k in z.files}
    from lineups.features import Store
    store = Store(out)
    cutoffs = dict(inner=legacy.day(base_schedule.start.iloc[-1]), final=legacy.day(NEW["start"]))
    for phase, cutoff in cutoffs.items():
        norm = normalizers.lineup_normalizers(grouped, offense, rebound, cutoff)
        norm |= normalizers.matchup_normalizers(legacy.matchups(), store, cutoff)
        np.savez(out / "normalizers" / f"2027q1_{phase}.npz", **norm)
        environment[f"2027q1/{phase}"] = normalizers.environment(grouped, labels["counts"], cutoff)
    (out / "environment.json").write_text(json.dumps(environment, indent=1, default=float))
    # The 2027q1 inner phase has the same cutoff as 2026q4 final: it must reproduce it. Inner-phase
    # rows and queries all predate 2026-03-02, so the library extension cannot change it.
    with np.load(paths.STORE / "normalizers" / "2026q4_final.npz") as old, \
            np.load(out / "normalizers" / "2027q1_inner.npz") as new:
        for k in old.files:
            np.testing.assert_allclose(new[k], old[k], rtol=0, atol=1e-9, err_msg=k)
    (out / "manifest.json").write_text(json.dumps(dict(
        created="2026-10-09", base_store=str(paths.STORE), new_origin=dict(tag="2027q1", index=int(new_index),
                                                                            start="2026-10-20", stop="provisional"),
        latest_game="2026-06-13",
        library_snapshot_for_new_origin=extension_dates[-1] if extension else "2026-03-02 (latest available)",
        library_extension=dict(directory=str(extension), dates=extension_dates) if extension else None,
        checks=["origins 0-51 identical to the v16 store", "2027q1 inner normalizers equal 2026q4 final"]
               + (["library tables before the extension equal the v16 library"] if extension else [])), indent=1))
    print("built", out)


if __name__ == "__main__":
    main()
