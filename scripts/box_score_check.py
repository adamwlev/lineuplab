"""Check play-by-play player counts against Basketball Reference box scores (name-matching fix, 2026-10-14).

The cached box-score pages (experiments/cache/bref_raw, the games ingested since
November 2024, 2024-25 and 2025-26) give each player's official FGA, FTA,
turnovers, rebounds, steals and blocks. lineups.player_counts gives the same
events as attributed from the play-by-play text, legacy and fixed. Per
player-season, the ratio counts / box score shows attribution losses:
- a name-matching loss is near 0 for one player and normal for his teammates;
- events by players missing from the recorded five cost every player a little.

    PYTHONPATH=. python -u scripts/box_score_check.py

Output: experiments/cache/names_fix_2026_10_14/box_score_check.csv and a printed summary.
"""
import gzip
from contextlib import closing

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from lineups import db, paths, player_counts
from lineups.bref_pages import PLAYER_HREF

RAW = paths.CACHE / "bref_raw"
OUT = paths.CACHE / "names_fix_2026_10_14" / "box_score_check.csv"
STATS = ("fga", "fta", "tov", "orb", "drb", "stl", "blk")
OWN = dict(fga=("own_fg2m", "own_fg2x", "own_fg3m", "own_fg3x"), fta=("own_ftm", "own_ftx"), tov=("own_tov",),
           orb=("own_orb",), drb=("own_drb",), stl=("own_stl",), blk=("own_blk",))


def box_scores():
    rows = []
    for path in sorted(RAW.glob("boxscores__2*.html.gz")):
        game = path.name.split("__")[1].split(".")[0]
        soup = BeautifulSoup(gzip.open(path, "rt", encoding="utf-8", errors="replace").read(), "html.parser")
        for table in soup.find_all("table"):
            if not table.get("id", "").endswith("game-basic"):
                continue
            for tr in table.select("tbody tr"):
                a = tr.select_one("th[data-stat=player] a[href]")
                m = PLAYER_HREF.search(a.get("href", "")) if a else None
                if not m or tr.select_one("td[data-stat=fga]") is None:
                    continue
                value = lambda k: float(tr.select_one(f"td[data-stat={k}]").get_text(strip=True) or 0)
                rows.append(dict(game=game, bref=m.group(1), **{k: value(k) for k in STATS}))
    return pd.DataFrame(rows)


def main():
    box = box_scores()
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute("select id, game_id, game_date from nba.games")
        games = pd.DataFrame(cur.fetchall(), columns=["game_id", "game", "date"])
        cur.execute("select id, player_id from nba.players")
        ids = dict((b, i) for i, b in cur.fetchall())
    box = box.merge(games, on="game", how="inner")
    box["pid"] = box.bref.map(ids)
    box = box.dropna(subset=["pid"]).astype({"pid": int})
    box["season"] = np.where(pd.to_datetime(box.date).dt.month >= 9, pd.to_datetime(box.date).dt.year + 1,
                             pd.to_datetime(box.date).dt.year)
    out = box.groupby(["pid", "season"])[list(STATS)].sum().add_prefix("box_")
    for label, path in (("legacy", player_counts.LEGACY), ("fixed", player_counts.OUT)):
        gp = pd.read_pickle(path)
        gp = gp[gp.game_id.isin(box.game_id.unique())]
        gp = gp.merge(box[["game_id", "season"]].drop_duplicates(), on="game_id")
        sums = pd.DataFrame({k: gp[list(cols)].sum(1) for k, cols in OWN.items()}).assign(pid=gp.pid, season=gp.season)
        out = out.join(sums.groupby(["pid", "season"]).sum().add_prefix(f"{label}_"), how="left")
    out = out.fillna(0).reset_index()
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute("select id, first_name, last_name from nba.players")
        names = {i: player_counts.repair(f"{f} {l}") for i, f, l in cur.fetchall()}
    out["name"] = out.pid.map(names)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"{box.game.nunique()} games, {len(out)} player-seasons")
    for k in STATS:
        tot = {label: out[f"{label}_{k}"].sum() / out[f"box_{k}"].sum() for label in ("legacy", "fixed")}
        print(f"{k}: play-by-play / box score, all players: legacy {tot['legacy']:.4f}, fixed {tot['fixed']:.4f}")
    big = out[out.box_fga >= 200].copy()
    for label in ("legacy", "fixed"):
        big[f"{label}_ratio"] = big[f"{label}_fga"] / big.box_fga
    print("\nplayer-seasons with 200+ box-score FGA whose play-by-play FGA ratio is below 0.95:")
    for label in ("legacy", "fixed"):
        low = big[big[f"{label}_ratio"] < .95].sort_values(f"{label}_ratio")
        print(f" {label}: {len(low)} of {len(big)}")
        print(low[["name", "season", "box_fga", "legacy_ratio", "fixed_ratio"]].head(15).round(3).to_string(index=False))
    print("\nratio distribution (fixed, 200+ FGA):", big.fixed_ratio.quantile([.01, .05, .5, .95, .99]).round(4).to_dict())


if __name__ == "__main__":
    main()
