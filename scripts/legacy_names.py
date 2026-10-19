"""Run a legacy builder (tag pre-refactor-2026-10-09) with the fixed name matching (2026-10-14).

The legacy parsers of the play-by-play text (shot_quality, possession_channels,
joint_capability_v14_data) match each event's actor to the players on the
floor by "first initial. last name" from nba.players
(reports/name_matching_fix_2026_10_14.md). This runner fixes names where the
legacy code reads them, at the database connection, and leaves the legacy
code unchanged:

- connections go through lineups.db (no credentials in code);
- rows with first_name and last_name come back renamed so that the legacy
  formula gives each player's canonical name: the form most of his events
  are printed under, which is his folded legacy name
  (lineups.player_counts.fold) or a learned alias;
- rows with texts come back folded (mis-decoded UTF-8 repaired, accents
  stripped), with each of a player's other forms rewritten to his canonical
  name where he is among the row's ten and no other player there owns that
  form as his canonical name ("j. williams" when Jeenathan Williams is the
  only J. Williams on the floor).

With --ids (2026-10-14, after the re-scrape) names are exact: every linked name
in a segment aligned with its page (lineups.pbp_ids) becomes its player's
token, his canonical name made unique with his Basketball Reference id when
another player shares it ("j. williams-willija06" for Jalen Williams), and
the name rows give the same tokens. Segments whose players are not all known
by id fall back to the rewrite above, then to the first player of the ten
with that canonical name.

--table reads another possession table with nba.possessions' columns in
every legacy query (nba_pages.possessions, rebuilt from the pages by
lineups.page_possessions).

It also maps a player stored under two ids to his page id in every player
column (lineups.pbp_ids.merges: Taylor Hendricks).

With --off nothing is transformed (the parity run: it must reproduce the
original artifact). The working directory becomes --root, so the legacy
relative paths (experiments/cache/...) resolve there and never in the
original cache. Run with the legacy worktree on the path:

    PYTHONPATH=.:../basketball-legacy python -u scripts/legacy_names.py --root DIR [--off] \\
        experiments.shot_quality build
    ... experiments.joint_capability_v14_data main -- extract --output-dir DIR
"""
import argparse
import importlib
import os
import sys
from pathlib import Path

import psycopg2

from lineups import db
from lineups.names import Names

TEN = [f"away_player_{i}_id" for i in range(1, 6)] + [f"home_player_{i}_id" for i in range(1, 6)]
_REAL_CONNECT = psycopg2.connect
TABLE = ["nba.possessions"]          # --table: the possession table the legacy queries read


class Cursor:
    def __init__(self, real, names):
        object.__setattr__(self, "_c", real)
        object.__setattr__(self, "_names", names)
        object.__setattr__(self, "_plan", None)

    def __getattr__(self, k):
        return getattr(self._c, k)

    def __setattr__(self, k, v):
        setattr(self._c, k, v)

    def __enter__(self):
        self._c.__enter__()
        return self

    def __exit__(self, *exc):
        return self._c.__exit__(*exc)

    def execute(self, query, *a, **k):
        object.__setattr__(self, "_plan", None)
        if TABLE[0] != "nba.possessions" and isinstance(query, str):
            query = query.replace("nba.possessions", TABLE[0])
        return self._c.execute(query, *a, **k)

    def _row(self, row):
        if row is None:
            return row
        plan = self._plan
        if plan is None:
            cols = [d[0] for d in (self._c.description or [])]
            names = (cols.index("id"), cols.index("first_name"), cols.index("last_name")) \
                if {"id", "first_name", "last_name"} <= set(cols) else None
            texts = cols.index("texts") if "texts" in cols else None
            ten = [cols.index(c) for c in TEN] if set(TEN) <= set(cols) else None
            poss = cols.index("id") if "id" in cols and texts is not None else None
            merge = [cols.index(c) for c in TEN + ["scorer"] if c in cols] if self._names.merge else []
            if self._names.ids and texts is not None and (poss is None or ten is None):
                raise RuntimeError(f"--ids needs the possession id and the ten with texts; query columns {cols}")
            plan = (names, texts, ten, poss, merge)
            object.__setattr__(self, "_plan", plan)
        names, texts, ten, poss, merge = plan
        if names is None and texts is None and not merge:
            return row
        row = list(row)
        for j in merge:
            row[j] = self._names.merge.get(row[j], row[j])
        if names is not None:
            i, f, l = names
            row[f], row[l] = self._names.name_row(row[i], row[f], row[l])
        if texts is not None and self._names.ids:
            row[texts] = self._names.text_ids(row[texts], [row[j] for j in ten], int(row[poss]))
        elif texts is not None:
            row[texts] = self._names.text(row[texts], None if ten is None else {row[j] for j in ten})
        return tuple(row)

    def fetchone(self):
        return self._row(self._c.fetchone())

    def fetchmany(self, *a, **k):
        return [self._row(r) for r in self._c.fetchmany(*a, **k)]

    def fetchall(self):
        return [self._row(r) for r in self._c.fetchall()]

    def __iter__(self):
        for r in self._c:
            yield self._row(r)


class Connection:
    def __init__(self, real, names):
        object.__setattr__(self, "_real", real)
        object.__setattr__(self, "_names", names)

    def __getattr__(self, k):
        return getattr(self._real, k)

    def __setattr__(self, k, v):
        setattr(self._real, k, v)

    def __enter__(self):
        self._real.__enter__()
        return self

    def __exit__(self, *exc):
        return self._real.__exit__(*exc)

    def cursor(self, *a, **k):
        return Cursor(self._real.cursor(*a, **k), self._names)


def install(fixed, ids=False, anchors=None):
    names = Names(ids, anchors) if fixed else None

    def connect(*a, **k):
        k = {key: v for key, v in k.items() if key not in ("dsn", "dbname", "user", "password", "host", "port")}
        real = _REAL_CONNECT(db.dsn(), **k)
        return Connection(real, names) if fixed else real

    psycopg2.connect = connect
    return names


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True, help="working directory for the legacy relative paths")
    p.add_argument("--off", action="store_true", help="no name fix (parity run)")
    p.add_argument("--ids", action="store_true", help="exact names from the pages (lineups.pbp_ids)")
    p.add_argument("--anchors", type=Path, help="with --ids: the lineups.pbp_ids output directory (default OUT)")
    p.add_argument("--table", default="nba.possessions",
                   help="possession table the legacy queries read (nba_pages.possessions: lineups.page_possessions)")
    p.add_argument("module")
    p.add_argument("function")
    p.add_argument("args", nargs=argparse.REMAINDER)
    a = p.parse_args()
    if a.off and a.ids:
        p.error("--off and --ids exclude each other")
    TABLE[0] = a.table
    names = install(not a.off, a.ids, a.anchors)
    if names is not None:
        print(f"name fix: {len(names.canonical)} canonical names, {len(names.rewrites)} alias rewrites"
              + (f"; ids: {sum(t != names.canonical[p] for p, t in names.token.items())} tokens" if a.ids else ""),
              flush=True)
    os.makedirs(os.path.join(a.root, "experiments", "cache"), exist_ok=True)
    os.chdir(a.root)
    fn = getattr(importlib.import_module(a.module), a.function)
    args = a.args[1:] if a.args[:1] == ["--"] else a.args
    if a.function == "main":
        import inspect
        if inspect.signature(fn).parameters:
            out = fn(args)
        else:                                       # a main that parses sys.argv itself
            sys.argv = [a.module] + args
            out = fn()
    else:
        out = fn(*args)
    print("done", a.module, a.function, flush=True)
    return out


if __name__ == "__main__":
    sys.exit(0 if main() is None or True else 1)
