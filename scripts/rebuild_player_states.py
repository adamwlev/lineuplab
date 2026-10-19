"""Rebuild the stores' origin states from the fixed name matching (2026-10-14).

lineups.player_counts fixed the matching of play-by-play names to players
(experiments/cache/game_player_stats_2026_10_14.pkl). This rebuilds what the
tool reads from those counts. For each source store (the era store and the
2027q1 library store):
1. check: the origin states rebuilt from the legacy counts equal the store's
   saved ones, so the shared code (lineups.states.origin_states) is exact;
2. write a new store that links every file of the source except
   offense_origins.npz and defense_origins.npz, which come from the fixed
   counts. It reports how far each player's states moved.

The source stores, the frozen fits and the prospective record are not
touched. Not rebuilt here: the rebound labels, the per-slot training labels
and the capability library, which come from the legacy pipeline and match
names the same way (reports/name_matching_fix_2026_10_14.md).

    PYTHONPATH=. python -u scripts/rebuild_player_states.py
    PYTHONPATH=. python -u scripts/build_player_seasons.py \\
        --era-store experiments/cache/lineups_store_era_names_2026_10_14 \\
        --release-store experiments/cache/lineups_store_2027q1_library_names_2026_10_14 \\
        --out experiments/cache/player_seasons_2026_10_14
"""
import json
import os

import numpy as np
import pandas as pd

from lineups import paths, player_counts, release, states

SOURCES = (paths.CACHE / "lineups_store_era", release.FROZEN_STORE)
SUFFIX = "_names_2026_10_14"
REBUILT = ("offense_origins.npz", "defense_origins.npz")


def main():
    for source in SOURCES:
        out = source.parent / (source.name + SUFFIX)
        out.mkdir(exist_ok=True)
        schedule = pd.read_csv(source / "schedule.csv", parse_dates=["start", "stop"])
        legacy_origins, _ = states.origin_states(schedule)
        for name, side in zip(REBUILT, ("offense", "defense")):
            with np.load(source / name) as saved:
                for k, v in legacy_origins[side].items():
                    if not np.array_equal(saved[k], v):
                        raise ValueError(f"{source.name}/{name}:{k}: rebuilt legacy states differ from the saved ones")
        print(source.name, "legacy origin states reproduced exactly", flush=True)
        fixed, _ = states.origin_states(schedule, players_path=player_counts.OUT)
        for entry in source.iterdir():
            if entry.name not in REBUILT and entry.name != "manifest.json" and not (out / entry.name).exists():
                os.symlink(entry.resolve(), out / entry.name)
        states.write_origins(out, fixed)
        o0, o1 = legacy_origins["offense"], fixed["offense"]
        assert np.array_equal(o0["pid"], o1["pid"]) and np.array_equal(o0["origin_index"], o1["origin_index"])
        move = np.abs(np.asarray(o1["base"], float) - np.asarray(o0["base"], float)).max(1)
        big = pd.Series(move, index=o1["pid"]).groupby(level=0).max().sort_values(ascending=False)
        manifest = json.loads((source / "manifest.json").read_text()) if (source / "manifest.json").exists() else {}
        manifest |= dict(names_fix=dict(source=str(source), counts=str(player_counts.OUT), rebuilt=list(REBUILT),
                                        largest_base_moves={str(int(k)): float(v) for k, v in big.head(30).items()}))
        (out / "manifest.json").write_text(json.dumps(manifest, indent=1, default=str))
        print(out.name, "written; players whose base state moved > 0.5:", int((big > .5).sum()), "> 0.05:",
              int((big > .05).sum()), "of", len(big), flush=True)


if __name__ == "__main__":
    main()
