"""Per-(game, player) event counts from the possession texts.

A port of experiments/game_player_stats.build (tag pre-refactor-2026-10-09),
the source of experiments/cache/game_player_stats.pkl that lineups.states
reads. Each possession's play-by-play text is split into events. Each event's
actor is matched by name to one of the ten players on the floor:

    own_*   the actor's own events (shots by location, makes, free throws,
            turnovers by type, rebounds, assists, steals, blocks, fouls)
    ton_*   his team's offense while he is on the floor
    don_*   the opponent's offense while he defends
    tt_*, ot_*  his team's and the opponent's game totals

**The name fix (2026-10-14).** The legacy matcher compares the text with
"first initial. last name" built from nba.players, lowercased. An event
whose actor is printed differently is silently dropped, and his own counts
miss it. About 34 player-seasons with 600-5,900 possessions came out
nearly empty (Nenê in every season, Vít Krejčí, Vasilije Micić, Hugo
González, D.J. Mbenga and others), so the model saw non-shooters. With
fixed=True:

- names on both sides are folded: mis-decoded UTF-8 repaired, accents
  stripped, spaces collapsed;
- the remaining unmatched names are learned as aliases. An unmatched name
  printed at least ALIAS_MIN times is assigned to the player who is on the
  floor for at least ALIAS_SHARE of its events, when no other player reaches
  ALIAS_RIVAL. The player must also have almost no events under his own name
  in the games where the alias appears (at most ALIAS_OWN per alias event).
  Without that check, events by a player missing from the recorded lineup
  went to a teammate ("d. ewing" to Elton Brand). An alias applies only when
  its player is on the floor.

fixed=False reproduces the legacy file exactly (tests/test_player_counts.py).

**Exact names (ids=True, after the re-scrape).** Every linked name of a
segment aligned with its Basketball Reference page becomes a token unique to
its player (lineups.names, lineups.pbp_ids), so teammates who print the same
("j. williams" for Jalen and Jaylin) are told apart. Other segments fall back
to the name fix. Matching is then exact.

    PYTHONPATH=. python -u -m lineups.player_counts [--ids]    # writes OUT (OUT_IDS)
"""
import json
import re
import time
from pathlib import Path
import unicodedata
from contextlib import closing

import numpy as np
import pandas as pd

from lineups import db, paths

LEGACY = paths.CACHE / "game_player_stats.pkl"
OUT = paths.CACHE / "game_player_stats_2026_10_14.pkl"
OUT_IDS = paths.CACHE / "game_player_stats_ids_2026_10_14.pkl"
AW = [f"away_player_{i}_id" for i in range(1, 6)]
HM = [f"home_player_{i}_id" for i in range(1, 6)]
SUF = re.compile(r"\s+(jr|sr|ii|iii|iv|v)\.?$", re.I)
DIST = re.compile(r"from (\d+) ft")
FT_QUALIFIER = re.compile(r"\b(makes|misses) (?:flagrant|clear path|transition take|away from play) free throw")
PRE = [(" makes 3-pt", "pre", "fg3m"), (" misses 3-pt", "pre", "fg3x"),
       (" makes 2-pt", "pre", "fg2m"), (" misses 2-pt", "pre", "fg2x"),
       (" makes free throw", "pre", "ftm"), (" misses free throw", "pre", "ftx"),
       ("turnover by ", "post", "tov"), ("offensive rebound by ", "post", "orb"),
       ("defensive rebound by ", "post", "drb"), ("(assist by ", "post", "ast"),
       ("steal by ", "post", "stl"), ("block by ", "post", "blk"),
       ("(drawn by ", "post", "fdrawn"), (" foul by ", "post", "fcommit")]
SHOTK = {"fg3m", "fg3x", "fg2m", "fg2x"}
LOC = ["rim", "paint", "mid", "longmid", "c3", "ab3"]
TOVT = ["badpass", "lostball", "offfoul", "travel"]
FOULT = ["shoot", "pers", "off", "loose"]
OWN = ([k for _, _, k in PRE] + ["shot_ast", "shot_rim", "dist_sum", "dist_n", "loc_n"]
       + ["loc_" + c for c in LOC] + ["tov_" + c for c in TOVT]
       + ["foul_" + c for c in FOULT] + ["fdrawn_shoot"])
TEAM = (["fg3m", "fg3a", "fg2m", "fg2a", "ftm", "fta", "orb", "drb", "tov", "pts", "poss",
         "loc_n"] + ["loc_" + c for c in LOC])
ALIAS_MIN, ALIAS_SHARE, ALIAS_RIVAL, ALIAS_OWN = 20, .95, .85, .1


LOWER_MOJIBAKE = re.compile("[\u00e2-\u00e5\u00c2-\u00c5][\u0080-\u00bf]")


def repair(text):
    """Undo UTF-8 read as Latin-1 ("MiciÄ\\x87" -> "Micić"), also after lowercasing ("jokiä\\x87" -> "jokić");
    other text is unchanged."""
    raised = LOWER_MOJIBAKE.sub(lambda m: m.group(0)[0].upper() + m.group(0)[1], text)
    try:
        return raised.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def fold(name):
    """Lowercase, accents stripped, spaces collapsed."""
    s = unicodedata.normalize("NFKD", repair(name))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def legacy_name(first, last):
    return f"{first[0]}. {SUF.sub('', last.strip())}".lower()


def _classify(seg, key):
    """Shot location bucket from the segment text, or None if unknown."""
    d = DIST.search(seg)
    dist = int(d.group(1)) if d else None
    if key in ("fg3m", "fg3x"):
        if dist is None:
            return None
        return "c3" if dist <= 22 else "ab3"
    if "at rim" in seg:
        return "rim"
    if dist is None:
        return None
    if dist <= 3:
        return "rim"
    if dist <= 9:
        return "paint"
    if dist <= 15:
        return "mid"
    return "longmid"


def read(table="nba.possessions"):
    """nba.players names and every possession's ten players and text (read only), from table
    (nba_pages.possessions: lineups.page_possessions)."""
    with closing(db.connect()) as conn:
        players = pd.read_sql("select id, first_name, last_name from nba.players", conn)
        with conn.cursor() as c:
            c.execute("set max_parallel_workers_per_gather = 4")
        cols = ", ".join("p." + c for c in AW + HM)
        df = pd.read_sql(f"""select p.id, p.game_id, p.away_team_ball, p.points_scored,
                                    {cols}, p.texts from {table} p""", conn)
    return players, df


def parse(texts):
    """Events (possession row, actor name, key, value) and the per-possession team matrix."""
    rows, nms, keys, vals = [], [], [], []
    IDX = {k: i for i, k in enumerate(TEAM)}
    S = np.zeros((len(texts), len(TEAM)))

    def emit(i, nm, k, v=1.0):
        rows.append(i); nms.append(nm); keys.append(k); vals.append(v)

    for i, s in enumerate(texts):
        for seg in s.split("/n"):
            seg = FT_QUALIFIER.sub(r"\1 free throw", seg)
            for mark, how, key in PRE:
                j = seg.find(mark)
                if j < 0:
                    continue
                if how == "pre":
                    nm = seg[:j].strip()
                else:
                    nm = seg[j + len(mark):]
                    ks = [k for k in (nm.find("("), nm.find(")"), nm.find(";")) if k >= 0]
                    if ks:
                        nm = nm[:min(ks)]
                    nm = nm.strip()
                if not nm or nm.startswith("team"):
                    continue
                nm = SUF.sub("", nm)
                emit(i, nm, key)
                if key in SHOTK:
                    if "(assist by" in seg:
                        emit(i, nm, "shot_ast")
                    if "at rim" in seg:
                        emit(i, nm, "shot_rim")
                    d = DIST.search(seg)
                    if d:
                        emit(i, nm, "dist_sum", float(d.group(1))); emit(i, nm, "dist_n")
                    loc = _classify(seg, key)
                    if loc:
                        emit(i, nm, "loc_" + loc); emit(i, nm, "loc_n")
                        S[i, IDX["loc_" + loc]] += 1; S[i, IDX["loc_n"]] += 1
                    if key == "fg3m":
                        S[i, IDX["fg3m"]] += 1; S[i, IDX["fg3a"]] += 1
                    elif key == "fg3x":
                        S[i, IDX["fg3a"]] += 1
                    elif key == "fg2m":
                        S[i, IDX["fg2m"]] += 1; S[i, IDX["fg2a"]] += 1
                    elif key == "fg2x":
                        S[i, IDX["fg2a"]] += 1
                elif key == "tov":
                    S[i, IDX["tov"]] += 1
                    for t, pat in (("badpass", "bad pass"), ("lostball", "lost ball"),
                                   ("offfoul", "offensive foul"), ("travel", "traveling")):
                        if pat in seg:
                            emit(i, nm, "tov_" + t); break
                elif key == "fcommit":
                    for t, pat in (("shoot", "shooting foul"), ("off", "offensive foul"),
                                   ("loose", "loose ball foul"), ("pers", "personal foul")):
                        if pat in seg:
                            emit(i, nm, "foul_" + t); break
                elif key == "fdrawn":
                    if "shooting foul" in seg:
                        emit(i, nm, "fdrawn_shoot")
                elif key == "ftm":
                    S[i, IDX["ftm"]] += 1; S[i, IDX["fta"]] += 1
                elif key == "ftx":
                    S[i, IDX["fta"]] += 1
                elif key == "orb":
                    S[i, IDX["orb"]] += 1
                elif key == "drb":
                    S[i, IDX["drb"]] += 1
    return (np.array(rows, np.int64), np.array(nms, dtype=object), np.array(keys, dtype=object),
            np.array(vals, float), S)


def match(ten, rows, nms, name_of):
    """Each event's actor among the ten on the floor (-1: no match), first column first, as the legacy code."""
    lookup = np.full(max(int(ten.max()), max(name_of)) + 1, "", dtype=object)
    for p, nm in name_of.items():
        lookup[p] = nm
    names = lookup[ten]
    who = np.full(len(rows), -1, np.int64)
    for c in range(10):
        hit = (names[rows, c] == nms) & (who < 0)
        who[hit] = ten[rows[hit], c]
    return who


def learn_aliases(ten, rows, nms, who, game):
    """{name: pid} for unmatched names that one on-floor player accounts for (module docstring).
    game: each event's game id."""
    miss = np.flatnonzero(who < 0)
    if not len(miss):
        return {}, pd.DataFrame()
    n = pd.Series(nms[miss]).value_counts()
    common = n[n >= ALIAS_MIN]
    keep = miss[pd.Series(nms[miss]).isin(common.index).to_numpy()]
    pairs = pd.DataFrame(dict(nm=np.repeat(nms[keep], 10), pid=ten[rows[keep]].ravel()))
    share = pairs.groupby(["nm", "pid"]).size().div(common.reindex(pairs.nm.unique()), level="nm").rename("share").reset_index()
    alias_events = pd.DataFrame(dict(nm=nms[keep], game=game[keep]))
    alias_games = alias_events.groupby("nm").game.unique()
    matched = pd.DataFrame(dict(game=game[who >= 0], pid=who[who >= 0])).groupby(["pid", "game"]).size()
    out, table, credited = {}, [], {}
    # largest first; a player's events under an accepted alias count as his own for the smaller names
    for nm in common.index:
        g = share[share.nm == nm].sort_values("share", ascending=False)
        best, rival = g.iloc[0], (g.iloc[1].share if len(g) > 1 else 0.)
        pid = int(best.pid)
        games = alias_games[nm]
        own = int(matched.reindex(pd.MultiIndex.from_product([[pid], games])).fillna(0).sum())
        own += sum(int(c.reindex(games).fillna(0).sum()) for c in credited.get(pid, []))
        ok = best.share >= ALIAS_SHARE and rival < ALIAS_RIVAL and own <= ALIAS_OWN * common[nm]
        table.append(dict(name=nm, events=int(common[nm]), pid=pid, share=float(best.share), rival=float(rival),
                          own=own, accepted=bool(ok)))
        if ok:
            out[nm] = pid
            credited.setdefault(pid, []).append(alias_events[alias_events.nm == nm].groupby("game").size())
    return out, pd.DataFrame(table)


def assemble(df, S, rows, who, keys, vals):
    """The legacy per-(game, player) table from matched events and the team matrix."""
    IDX = {k: i for i, k in enumerate(TEAM)}
    n = len(df)
    ab = df["away_team_ball"].values
    awayA, homeA = df[AW].values.astype(np.int64), df[HM].values.astype(np.int64)
    off5 = np.where(ab[:, None], awayA, homeA)
    def5 = np.where(ab[:, None], homeA, awayA)
    gid = df["game_id"].values.astype(np.int64)
    S = S.copy()
    S[:, IDX["pts"]] = df["points_scored"].values
    S[:, IDX["poss"]] = 1.0
    ok = who >= 0
    own = (pd.DataFrame({"game_id": gid[rows[ok]], "pid": who[ok], "k": keys[ok], "v": vals[ok]})
           .groupby(["game_id", "pid", "k"])["v"].sum().unstack("k", fill_value=0.0)
           .reindex(columns=OWN, fill_value=0.0))
    own.columns = ["own_" + c for c in own.columns]

    def accum(idx5, prefix):
        g = np.repeat(gid, 5); p = idx5.ravel()
        d = {prefix + c: np.repeat(S[:, IDX[c]], 5) for c in TEAM}
        return pd.DataFrame({"game_id": g, "pid": p, **d}).groupby(["game_id", "pid"]).sum()

    gp = own.join(accum(off5, "ton_"), how="outer").join(accum(def5, "don_"), how="outer").fillna(0.0)
    side = ab.astype(int)
    tt = pd.DataFrame({"game_id": gid, "side": side, **{c: S[:, IDX[c]] for c in TEAM}}).groupby(["game_id", "side"]).sum()
    roster = pd.DataFrame({
        "game_id": np.concatenate([np.repeat(gid, 5), np.repeat(gid, 5)]),
        "pid": np.concatenate([awayA.ravel(), homeA.ravel()]),
        "side": np.concatenate([np.ones(n * 5, int), np.zeros(n * 5, int)]),
    }).drop_duplicates()
    ow = roster.merge(tt, on=["game_id", "side"], how="left").set_index(["game_id", "pid"])[TEAM]
    op = (roster.assign(side=1 - roster["side"]).merge(tt, on=["game_id", "side"], how="left")
          .set_index(["game_id", "pid"])[TEAM])
    gp = gp.join(ow.add_prefix("tt_"), how="left").join(op.add_prefix("ot_"), how="left")
    gp = gp.fillna(0.0).reset_index()
    gp["pid"] = gp["pid"].astype(np.int32)
    gp["game_id"] = gp["game_id"].astype(np.int32)
    return gp


def build(fixed=True, log=print, data=None, ids=False, anchors=None):
    """(table, report). data: (players, possessions) as from read(), to reuse one read. ids: exact names
    (module docstring; fixed is then ignored), from the lineups.pbp_ids output in anchors (default its OUT)."""
    t0 = time.time()
    players, df = data if data is not None else read()
    log(f"[{time.time() - t0:.0f}s] {len(df):,} possessions")
    ab = df["away_team_ball"].values
    awayA, homeA = df[AW].values.astype(np.int64), df[HM].values.astype(np.int64)
    ten = np.concatenate([np.where(ab[:, None], awayA, homeA), np.where(ab[:, None], homeA, awayA)], axis=1)
    texts = df["texts"].values
    if ids:
        from lineups.names import Names
        names = Names(ids=True, anchors=anchors)
        if names.merge:                              # one player stored under two ids
            lut = np.arange(max(int(df[AW + HM].to_numpy().max()), max(names.merge)) + 1)
            lut[list(names.merge)] = list(names.merge.values())
            df = df.copy()
            df[AW + HM] = lut[df[AW + HM].to_numpy(np.int64)]
            ab = df["away_team_ball"].values
            awayA, homeA = df[AW].values.astype(np.int64), df[HM].values.astype(np.int64)
            ten = np.concatenate([np.where(ab[:, None], awayA, homeA), np.where(ab[:, None], homeA, awayA)], axis=1)
        texts = [names.text_ids(t, list(r), int(i)) for t, r, i in zip(df["texts"].fillna(""), ten, df["id"])]
    rows, nms, keys, vals, S = parse(texts)
    log(f"[{time.time() - t0:.0f}s] parsed {len(rows):,} events")
    legacy = {int(i): legacy_name(f, l) for i, f, l in players[["id", "first_name", "last_name"]].itertuples(index=False)}
    report = dict(events=int(len(rows)))
    if ids:
        before = match(ten, rows, nms, legacy)
        who = match(ten, rows, nms, names.token)
        report.update(matched_legacy=float((before >= 0).mean()), matched=float((who >= 0).mean()),
                      tokens=int(sum(t != names.canonical[p] for p, t in names.token.items())))
    elif not fixed:
        who = match(ten, rows, nms, legacy)
        report["matched"] = float((who >= 0).mean())
    else:
        before = match(ten, rows, nms, legacy)
        folded = {i: fold(n) for i, n in legacy.items()}
        codes, unique = pd.factorize(nms)
        nms = np.array([fold(x) for x in unique], dtype=object)[codes]
        who = match(ten, rows, nms, folded)
        aliases, table = learn_aliases(ten, rows, nms, who, df["game_id"].values[rows])
        miss = np.flatnonzero(who < 0)
        target = np.array([aliases.get(x, -1) for x in nms[miss]], np.int64)
        on = (ten[rows[miss]] == target[:, None]).any(1) & (target >= 0)
        who[miss[on]] = target[on]
        report.update(matched_legacy=float((before >= 0).mean()), matched=float((who >= 0).mean()),
                      aliases=len(aliases), alias_events=int(on.sum()), alias_table=table.to_dict("records"),
                      gained={int(p): int(c) for p, c in pd.Series(who[before < 0]).value_counts().items() if p >= 0})
    log(f"[{time.time() - t0:.0f}s] matched {report['matched']:.3%}"
        + (f" (legacy {report['matched_legacy']:.3%}; {report['tokens']} unique tokens)" if ids
           else f" (legacy {report['matched_legacy']:.3%}; {report['aliases']} aliases)" if fixed else ""))
    return assemble(df, S, rows, who, keys, vals), report


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--ids", action="store_true", help="exact names from the pages")
    p.add_argument("--anchors", type=Path, help="with --ids: the lineups.pbp_ids output directory")
    p.add_argument("--out", type=Path, help="output pickle (default OUT, or OUT_IDS with --ids)")
    p.add_argument("--table", default="nba.possessions", help="possession table (nba_pages.possessions)")
    a = p.parse_args()
    out = a.out or (OUT_IDS if a.ids else OUT)
    gp, report = build(fixed=True, ids=a.ids, anchors=a.anchors, data=read(a.table) if a.table != "nba.possessions" else None)
    gp.to_pickle(out)
    out.with_suffix(".json").write_text(json.dumps(report, indent=1, default=float))
    print(f"wrote {out} rows={len(gp):,}")


if __name__ == "__main__":
    main()
