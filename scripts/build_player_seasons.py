"""Raw model inputs for every player-season 2002-2026 (docs/CLOSEOUT.md, step 2).

A player-season is the player as of the next season's opening night: the
origin state at that season's first window, which is how the release model
sees active players (season 2026 is origin 2027q1). The convention is the same
for every season. Sources:

    seasons 2002-2012   lineups_store_era, origins 2003q1-2013q1
    seasons 2013-2026   lineups_store_2027q1_library, origins 2014q1-2027q1
                        (origins up to 2026q1 are identical to the v16 store)

Each row holds the raw offensive state, role, rebound prior and n_eff, the
defensive descriptors and both adjusted capability banks read at that origin's
date. Possession counts come from the matchup rows. Standardization happens at
use time with the release normalizer (lineups.players).

season_normalizers.npz holds each season origin's normalizer means, for the
era-relative input rule. They are the stores' saved final-phase normalizers
where those exist. The rest (2003q1-2005q1 and 2014q1) are computed with
lineups.normalizers from the stores' game-level tables, and that recomputation
reproduces a saved normalizer exactly (checked here on 2006q1).

    PYTHONPATH=. python -u scripts/build_player_seasons.py [--era-store DIR --release-store DIR --out DIR]

Output: experiments/cache/player_seasons_2026_10_14/{player_seasons.npz, names.json}, from the stores
rebuilt on the fixed name matching (scripts/rebuild_player_states.py; the defaults). The 2026-10-12
table (player_seasons_2026_10_12) came from lineups_store_era and lineups_store_2027q1_library. Display
names repair mis-decoded UTF-8 (lineups.player_counts.repair).
"""
import argparse
import json
from contextlib import closing
from pathlib import Path

import numpy as np
import pandas as pd

from lineups import db, legacy, normalizers, paths, release, states
from lineups.features import Store
from lineups.schedule import season_labels

OUT = paths.CACHE / "player_seasons_2026_10_14"
ERA = paths.CACHE / "lineups_store_era_names_2026_10_14"
FIRST, LAST = 2002, 2026
LAST_ERA = 2012


def season_counts(g):
    """Possessions and games per (pid, season), offense and defense sides."""
    season = season_labels(pd.to_datetime(np.asarray(g["date"]), unit="D"))
    poss = np.asarray(g["possessions"], float)
    game = np.asarray(g["game_id"])
    frames = []
    for side, column in (("offense", "pids"), ("defense", "defense")):
        pids = np.asarray(g[column])
        frames.append(pd.DataFrame(dict(pid=pids.ravel(), season=np.repeat(season, 5), game=np.repeat(game, 5),
                                        **{f"{side}_possessions": np.repeat(poss, 5)})))
    f = pd.concat(frames, ignore_index=True).fillna(0.)
    out = f.groupby(["pid", "season"]).agg(offense_possessions=("offense_possessions", "sum"),
                                            defense_possessions=("defense_possessions", "sum"),
                                            games=("game", "nunique")).reset_index()
    return out[(out.season >= FIRST) & (out.season <= LAST)]


def lookup(store, tag, pids):
    origin = store.schedule().query("tag == @tag").iloc[0]
    index, day = int(origin.origin_index), legacy.day(origin.start)
    known = np.isin(pids, store.offense_origins["pid"][store.offense_origins["origin_index"] == index])
    if not known.all():
        raise KeyError(f"{tag}: {int((~known).sum())} players without an origin state")
    off = store.offense(pids, origin_index=index)
    column = pids[:, None]
    days = np.full(len(pids), day, np.int64)
    return dict(base=off["base"], role=off["role"], rb_prob=off["rb_prob"], rb_neff=off["rb_neff"],
                defense=store.defense(pids, origin_index=index),
                adjusted_offense=store.capabilities(column, days, "offense")[:, 0],
                adjusted_defense=store.capabilities(column, days, "defense")[:, 0],
                origin_day=days)


MEANS = ("base_mean", "role_mean", "rebound_mean", "defense_mean", "offense_mean", "defense_bank_mean")


def computed_normalizer(store, cutoff, first_day=legacy.day("2001-12-01")):
    """Final-phase normalizer at a cutoff day, from the store's game-level tables and library."""
    with np.load(states.GAME_LINEUPS) as z:
        grouped = {k: z[k] for k in z.files}
    og = store.offense_games
    x = np.zeros((len(og["pid"]), 63), np.float32)
    x[:, 55:63] = og["role"]
    offense = dict(game_id=og["game_id"], pid=og["pid"], base=og["base"], x=x)
    rebound = dict(game_id=og["game_id"], pid=og["pid"], prob=og["rb_prob"], neff=og["rb_neff"])
    out = normalizers.lineup_normalizers(grouped, offense, rebound, cutoff, first_day)
    return out | normalizers.matchup_normalizers(legacy.matchups(), store, cutoff, first_day)


def season_normalizers(stores):
    era = stores["era"]
    start = lambda store, tag: legacy.day(store.schedule().query("tag == @tag").iloc[0].start)
    check = computed_normalizer(era, start(era, "2006q1"))
    for k in MEANS:
        if not np.array_equal(np.asarray(check[k], np.float64), np.asarray(era.normalizer("2006q1", "final")[k], np.float64)):
            raise ValueError(f"recomputed normalizer differs from the saved one: {k}")
    out = {}
    for season in range(FIRST, LAST + 1):
        tag = f"{season + 1}q1"
        source = stores["era" if season <= LAST_ERA else "release"]
        path = source.directory / "normalizers" / f"{tag}_final.npz"
        # The era store's library and game tables cover every prefix; its schedule stops at 2013.
        n = source.normalizer(tag, "final") if path.exists() else computed_normalizer(era, start(source, tag))
        out |= {f"{season}_{k}": np.asarray(n[k], np.float32) for k in MEANS}
        print("normalizer", season, tag, "saved" if path.exists() else "computed", flush=True)
    return out


def names():
    from lineups.player_counts import repair
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute("select id, first_name, last_name from nba.players order by id")
        return {int(i): " ".join(repair(x) for x in (f, l) if x) for i, f, l in cur.fetchall()}


def main():
    global OUT
    p = argparse.ArgumentParser()
    p.add_argument("--era-store", type=Path, default=ERA)
    p.add_argument("--release-store", type=Path, default=release.STORE)
    p.add_argument("--out", type=Path, default=OUT)
    a = p.parse_args()
    OUT = a.out
    OUT.mkdir(parents=True, exist_ok=True)
    counts = season_counts(legacy.matchups())
    stores = dict(era=Store(a.era_store), release=Store(a.release_store))
    parts = []
    for season, block in counts.groupby("season"):
        source = "era" if season <= LAST_ERA else "release"
        tag = f"{season + 1}q1"
        pids = block.pid.to_numpy(np.int64)
        raw = lookup(stores[source], tag, pids)
        parts.append(dict(raw, pid=pids, season=np.full(len(pids), season, np.int32),
                          source=np.full(len(pids), source, "U8"), origin=np.full(len(pids), tag, "U8"),
                          offense_possessions=block.offense_possessions.to_numpy(),
                          defense_possessions=block.defense_possessions.to_numpy(),
                          games=block.games.to_numpy(np.int32)))
        print(season, source, tag, len(pids), flush=True)
    table = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
    np.savez(OUT / "player_seasons.npz", **table)
    np.savez(OUT / "season_normalizers.npz", **season_normalizers(stores))
    roster = names()
    missing = sorted(set(table["pid"].tolist()) - set(roster))
    (OUT / "names.json").write_text(json.dumps({str(k): roster.get(k, f"player {k}")
                                                for k in sorted(set(table["pid"].tolist()))}, indent=0))
    print(f"{len(table['pid'])} player-seasons, {len(set(table['pid'].tolist()))} players, "
          f"{len(missing)} without a name", flush=True)


if __name__ == "__main__":
    main()
