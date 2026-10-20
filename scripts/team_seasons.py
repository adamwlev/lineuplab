"""Every team-season's roster and most-used five, for the tool's best-five search (Adam, 2026-10-19).

From the clean possession table (paths.CLEAN's possessions pickle, which is nba_pages.possessions), with each
game's teams from nba.games. A player belongs to a team-season when he was on the floor for it. The roster is
his 13 player-seasons with the most possessions for that team (offense and defense), among the player-seasons
the tool has with at least the band's thin-data offensive possessions. A traded player counts on each team he
played for, with his whole season's estimates. The most-used five is the five that played the most possessions
for the team that season.

    PYTHONPATH=. python -u scripts/team_seasons.py OUT_DIR

Writes OUT_DIR/team_seasons.json (tool/build_lineups.py puts it in the page).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import psycopg2

from lineups import paths
from lineups.db import dsn
from lineups.sources import SOURCE

ROSTER = 13                                  # an NBA active roster


def season_of(dates):
    d = pd.to_datetime(dates)
    return np.where(d.dt.month >= 8, d.dt.year + 1, d.dt.year).astype(np.int16)


def main():
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=False)
    meta = json.loads((SOURCE["export"] / "meta.json").read_text())
    P = meta["players"]
    thin = meta["band"]["thin_possessions"]
    eligible = {(p, s) for p, s, o in zip(P["pid"], P["season"], P["offense_possessions"]) if o >= thin}
    known = set(zip(P["pid"], P["season"]))
    pos = pd.read_pickle(paths.CLEAN / "possessions_ba7aeb377198.pkl")
    with psycopg2.connect(dsn()) as conn:
        games = pd.read_sql("select id as game_id, away_team, home_team from nba.games", conn)
    pos = pos.merge(games, on="game_id", how="left", validate="many_to_one")
    assert pos.away_team.notna().all(), "a possession's game is missing from nba.games"
    pos["season"] = season_of(pos.game_date)
    teams = sorted(set(pos.away_team) | set(pos.home_team))
    code = {t: i for i, t in enumerate(teams)}
    counts, fives = [], []
    for side in ("away", "home"):
        cols = [f"{side}_player_{k}_id" for k in range(1, 6)]
        ids = pos[cols].to_numpy(np.int64)
        team = pos[f"{side}_team"].map(code).to_numpy(np.int64)
        key = pos.season.to_numpy(np.int64) * 100 + team                   # team-season
        counts.append(pd.DataFrame({"key": np.repeat(key, 5), "pid": ids.ravel()}))
        s = np.sort(ids, axis=1)
        five = ((s[:, 0] * 4096 + s[:, 1]) * 4096 + s[:, 2]) * 4096 + s[:, 3]   # four 12-bit ids, then the fifth
        fives.append(pd.DataFrame({"key": key, "five": five, "last": s[:, 4]}))
    on_floor = pd.concat(counts).groupby(["key", "pid"]).size().rename("possessions").reset_index()
    used = pd.concat(fives).groupby(["key", "five", "last"]).size().rename("possessions").reset_index()
    top = used.sort_values("possessions", ascending=False).drop_duplicates("key").set_index("key")
    out = []
    for key, g in on_floor.groupby("key"):
        season, team = int(key // 100), teams[int(key % 100)]
        g = g.sort_values("possessions", ascending=False)
        keep = [(int(p), int(n)) for p, n in zip(g.pid, g.possessions) if (int(p), season) in eligible][:ROSTER]
        t = top.loc[key]
        f = int(t.five)
        best = [f >> 36 & 4095, f >> 24 & 4095, f >> 12 & 4095, f & 4095, int(t["last"])]
        out.append(dict(season=season, team=team, roster=keep,
                        thin=sum((int(p), season) in known and (int(p), season) not in eligible for p in g.pid),
                        most_used=dict(five=best, possessions=int(t.possessions),
                                       known=all((p, season) in known for p in best))))
    out.sort(key=lambda x: (-x["season"], x["team"]))
    doc = dict(source="paths.CLEAN possessions (nba_pages.possessions) and nba.games", roster_size=ROSTER,
               thin_possessions=thin, team_seasons=out)
    (out_dir / "team_seasons.json").write_text(json.dumps(doc, ensure_ascii=False) + "\n")
    sizes = [len(x["roster"]) for x in out]
    print(f"{len(out)} team-seasons, {min(x['season'] for x in out)}-{max(x['season'] for x in out)}; roster sizes "
          f"{min(sizes)}-{max(sizes)}; most-used fives in the tool: {sum(x['most_used']['known'] for x in out)}")
    gsw = next(x for x in out if x["season"] == 2017 and x["team"] == "Golden State Warriors")
    print("2016-17 Warriors:", [meta["names"][str(p)] for p, _ in gsw["roster"]],
          "| most used:", [meta["names"][str(p)] for p in gsw["most_used"]["five"]], gsw["most_used"]["possessions"])


if __name__ == "__main__":
    main()
