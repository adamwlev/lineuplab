"""The possession table rebuilt from the Basketball Reference pages (2026-10-14).

Adam (2026-10-14): "yes continue with the rebuild. clean data is primary ...
you can write to the database."

nba.possessions was written by the original scraper (scrape_br.ipynb) for
every game before November 2024 (reports/rescrape_pilot_2026_10_14.md):

- the first possession of each later quarter starts at the previous quarter's
  last clock (89,733 possessions);
- in 335 games the scraper stopped more than 20 points short, at a
  substitution it could not follow; 17 games have no possessions;
- a technical foul cleared the possession in progress.

This module re-parses every game from its two cached pages with the parser of
record (lineups.bref_pages.parse_game, used since November 2024, with its two
labeled page repairs), checks the score against nba.games, and writes TABLE.
nba.possessions is left as it is.

- **Columns** are those of nba.possessions. Players are ordered within each
  five as lineups.bref_pages orders them. texts are stored in the original
  scraper's form (each event cell's text, stripped and lowercased) for every
  game, the form the readers were written for.
- **Ids** start at ID_START, so a possession id can never be mistaken for one
  of nba.possessions.
- **Sources** (SOURCES, one row a game): "pages", or "stored" when the pages
  are missing or cannot be parsed, or the parse fails the score check. A
  stored game keeps nba.possessions' rows, with the quarter-start clock
  repaired. The reason and any page repairs are recorded.
- **One player, one id:** stored rows map ids through merges() (Taylor
  Hendricks, stored as 2292 before Basketball Reference renamed his id).
- **One transaction:** seasons are parsed and inserted one at a time, and
  nothing is visible until all of them are in.

    PYTHONPATH=. python -u -m lineups.page_possessions --check [--limit N]   # parse and audit, no writes
    PYTHONPATH=. python -u -m lineups.page_possessions --write               # create and fill TABLE, SOURCES

Output: OUT/{check,write}/{games.csv, report.json}.
"""
import argparse
import datetime as dt
import gzip
import json
import time
from contextlib import closing
from multiprocessing import Pool

import numpy as np
import pandas as pd
from psycopg2.extras import execute_values

from lineups import db, paths
from lineups.bref_pages import GameListing, ParseError, _ordered_player_ids, parse_game, validate_score

SCHEMA = "nba_pages"
TABLE = f"{SCHEMA}.possessions"
SOURCES = f"{SCHEMA}.game_sources"
ID_START = 10_000_001
RAW = paths.CACHE / "bref_raw"
OUT = paths.CACHE / "page_possessions_2026_10_14"
MERGES = paths.CACHE / "pbp_ids_2026_10_14_partial" / "merges.json"   # one player under two ids (lineups.pbp_ids)
TEN = [f"away_player_{i}_id" for i in range(1, 6)] + [f"home_player_{i}_id" for i in range(1, 6)]
COLUMNS = ["game_id", "quarter", "time_left_start", "time_left_end", "away_team_ball", "turnover",
           "points_scored", "scorer", *TEN, "texts"]


def use_schema(schema):
    """Write into another schema (a scratch test of the writer)."""
    global SCHEMA, TABLE, SOURCES
    SCHEMA, TABLE, SOURCES = schema, f"{schema}.possessions", f"{schema}.game_sources"


def pages(game):
    return RAW / f"boxscores__{game}.html.html.gz", RAW / f"boxscores__pbp__{game}.html.html.gz"


def games():
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute("""select id, game_id, game_date, away_team, home_team, away_team_points, home_team_points,
                              playoffs from nba.games order by game_date, game_id""")
        return pd.DataFrame(cur.fetchall(), columns=["id", "game", "date", "away", "home", "away_points",
                                                     "home_points", "playoffs"])


def players():
    """{bref id: (id, position, height)}, as lineups.bref_pages orders a five."""
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute("select player_id, id, position, height_inches from nba.players")
        return {b: (i, pos, h) for b, i, pos, h in cur.fetchall()}


def parse_one(args):
    """(rows, stats) for one game from its pages; rows are empty when it falls back."""
    row, people = args
    stats = dict(game=row["game"], id=int(row["id"]), source="pages", reason="", repairs="", possessions=0,
                 points=0, official=int(row["away_points"] + row["home_points"]), technical=0)
    box, pbp = pages(row["game"])
    try:
        parsed = parse_game(gzip.open(box, "rt", encoding="utf-8").read(),
                            gzip.open(pbp, "rt", encoding="utf-8").read(), repair=True)
        listing = GameListing(row["game"], row["date"], row["away"], row["home"], int(row["away_points"]),
                              int(row["home_points"]), bool(row["playoffs"]))
        validate_score(listing, parsed)
        unknown = sorted((set(parsed.away_roster) | set(parsed.home_roster)) - set(people))
        if unknown:
            raise ParseError(f"players missing from nba.players: {unknown}")
        out = [(int(row["id"]), p.quarter, p.time_left_start, p.time_left_end, p.away_team_ball, p.turnover,
                p.points_scored, people[p.scorer_bref_id][0] if p.scorer_bref_id else None,
                *_ordered_player_ids(p.away_players, people), *_ordered_player_ids(p.home_players, people),
                p.cell_texts) for p in parsed.possessions]
    except (OSError, ParseError, ValueError, KeyError) as exc:
        stats.update(source="stored", reason=f"{type(exc).__name__}: {exc}"[:300])
        return [], stats
    stats.update(possessions=len(out), points=sum(r[6] for r in out),
                 technical=sum(parsed.technical_points or (0, 0)), repairs=" | ".join(parsed.repairs)[:1000])
    return out, stats


def merges():
    """{stored id: page id}: a player the old scraper stored under an id Basketball Reference has since
    renamed (Taylor Hendricks), detected from the pages by lineups.pbp_ids. Pages-derived games carry the
    page id, so stored games must too."""
    return {int(k): int(v) for k, v in json.loads(MERGES.read_text()).items()} if MERGES.exists() else {}


def stored_rows(game_ids):
    """nba.possessions rows of these games (internal ids) in their order, the quarter-start clock repaired
    (a quarter's possession that ends later than it starts starts at the period's full clock) and player ids
    merged (merges())."""
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute(f"select {', '.join(COLUMNS)} from nba.possessions where game_id = any(%s) order by game_id, id",
                    (list(map(int, game_ids)),))
        rows = [list(r) for r in cur.fetchall()]
    merge = merges()
    for r in rows:
        if r[2] < r[3]:
            r[2] = 720.0 if r[1] <= 4 else 300.0
        for j in range(7, 18):                       # scorer and the ten
            r[j] = merge.get(r[j], r[j])
    return [tuple(r) for r in rows]


def build(check=True, processes=6, limit=None, log=print):
    """Per-game stats; with check=False also writes TABLE and SOURCES, a season at a time in one transaction."""
    t0 = time.time()
    g = games()
    have = g[[all(x.exists() for x in pages(n)) for n in g.game]]
    if limit:
        have = have.iloc[np.unique(np.linspace(0, len(have) - 1, limit).round().astype(int))]
    people = players()
    log(f"[{time.time() - t0:.0f}s] {len(g):,} games; {len(have):,} with both pages")
    todo = have if limit else g
    season = pd.to_datetime(todo.date).dt.year + (pd.to_datetime(todo.date).dt.month >= 9)
    conn = None if check else closing(db.connect())
    stats, written = [], 0
    with Pool(processes) as pool, (conn if conn is not None else _nothing()) as c:
        cur = None if c is None else c.cursor()
        if cur is not None:
            create(cur)
        for s in sorted(season.unique()):
            chunk = todo[(season == s).to_numpy()]
            jobs = [(x, people) for x in chunk.to_dict("records") if x["id"] in set(have.id)]
            by_game, chunk_stats = {}, []
            for r, st in pool.imap(parse_one, jobs, chunksize=4):
                if r:
                    by_game[st["id"]] = r
                chunk_stats.append(st)
            done = {st["id"] for st in chunk_stats}
            chunk_stats += [dict(game=x.game, id=int(x.id), source="stored", reason="pages not downloaded", repairs="",
                                 possessions=0, points=0, official=int(x.away_points + x.home_points), technical=0)
                            for x in chunk.itertuples() if int(x.id) not in done]
            fallback = [st["id"] for st in chunk_stats if st["source"] == "stored"]
            for r in stored_rows(fallback) if fallback else []:
                by_game.setdefault(r[0], []).append(r)
            for st in chunk_stats:
                if st["source"] == "stored":
                    rows = by_game.get(st["id"], [])
                    st.update(possessions=len(rows), points=sum(r[6] for r in rows))
            rows = [r for gid in chunk.id if gid in by_game for r in by_game[gid]]
            if cur is not None:
                insert(cur, rows, chunk_stats)
            written += len(rows)
            stats += chunk_stats
            log(f"[{time.time() - t0:.0f}s] season {s}: {len(chunk):,} games, {len(rows):,} possessions, "
                f"{len(fallback)} fall back; {written:,} so far")
        if cur is not None:
            cur.execute(f"alter table {TABLE} add primary key (id)")
            cur.execute(f"create index on {TABLE} (game_id)")
            c.commit()
            log(f"wrote {TABLE}: {written:,} possessions; {SOURCES}: {len(stats):,} games")
    return pd.DataFrame(stats)


class _nothing:
    def __enter__(self):
        return None

    def __exit__(self, *exc):
        return False


def create(cur):
    """SCHEMA, TABLE (nba.possessions' columns, ids from ID_START) and SOURCES; never over an existing table."""
    cur.execute(f"create schema if not exists {SCHEMA}")
    cur.execute(f"select to_regclass('{TABLE}')")
    if cur.fetchone()[0] is not None:
        raise RuntimeError(f"{TABLE} exists; it is never overwritten")
    cur.execute(f"create sequence {SCHEMA}.possessions_id_seq start {ID_START}")
    cur.execute(f"create table {TABLE} (like nba.possessions including constraints)")
    cur.execute(f"alter table {TABLE} alter column id set default nextval('{SCHEMA}.possessions_id_seq')")
    cur.execute(f"alter sequence {SCHEMA}.possessions_id_seq owned by {TABLE}.id")
    cur.execute(f"""create table {SOURCES} (game_id integer primary key, source text not null, reason text not null,
                    repairs text not null, possessions integer not null, points integer not null,
                    official integer not null)""")


def insert(cur, rows, stats):
    """One season's possessions (games by date, each game's in order, so ids follow the play) and sources."""
    execute_values(cur, f"insert into {TABLE} ({', '.join(COLUMNS)}) values %s", rows, page_size=2000)
    execute_values(cur, f"insert into {SOURCES} values %s",
                   [(int(r["id"]), r["source"], r["reason"] or "", r["repairs"] or "", int(r["possessions"]),
                     int(r["points"]), int(r["official"])) for r in stats])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="parse and audit only (no database writes)")
    p.add_argument("--write", action="store_true", help="create and fill TABLE and SOURCES")
    p.add_argument("--limit", type=int, help="with --check: this many games with pages, evenly spaced")
    p.add_argument("--processes", type=int, default=6)
    p.add_argument("--schema", default=SCHEMA, help="target schema; with --limit only a scratch schema")
    a = p.parse_args()
    if a.check == a.write:
        p.error("choose one of --check and --write")
    if a.write and a.limit and a.schema == SCHEMA:
        p.error("a partial write goes to a scratch --schema, never to the table of record")
    use_schema(a.schema)
    stats = build(check=a.check, processes=a.processes, limit=a.limit)
    out = OUT / ("check" if a.check else "write" if a.schema == "nba_pages" else f"write_{a.schema}")
    out.mkdir(parents=True, exist_ok=True)
    stats.to_csv(out / "games.csv", index=False)
    pg = stats[stats.source == "pages"]
    report = dict(written_at=dt.datetime.now().isoformat(timespec="seconds"), games=len(stats),
                  from_pages=int(len(pg)), stored=int((stats.source == "stored").sum()),
                  reasons=stats.loc[stats.source == "stored", "reason"].str.split(":").str[0].value_counts().to_dict(),
                  with_repairs=int((pg.repairs.fillna("") != "").sum()),
                  possessions=int(stats.possessions.sum()), points=int(stats.points.sum()),
                  official=int(stats.official.sum()), technical_from_pages=int(pg.technical.sum()))
    (out / "report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
