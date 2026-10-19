"""Each stored event's players by id, from the Basketball Reference pages (2026-10-14).

nba.possessions keeps each possession's play-by-play as lowercased text, so
every reader matches an event's actor to the players on the floor by printed
name (lineups.player_counts). Teammates who print the same name cannot be
told apart: "j. williams" is Jalen or Jaylin at Oklahoma City, "j. green" is
Jalen or Jeff at Houston, "m. morris" is either twin. The pages
(scripts/rescrape_pages.py) link every printed name to its player.

**Alignment.** A game's stored segments (each possession's texts split on
"/n", in possession order) are aligned with the page's event rows by
difflib on folded text: mis-decoded UTF-8 repaired, accents stripped. A
segment that equals its row takes the row's linked players, in order, with
their positions in the folded segment. A segment that differs (the page was
edited after the original scrape) takes, in order, the next differing row
that is at least EDITED similar and whose linked names it contains.

    PYTHONPATH=. python -u -m lineups.pbp_ids [--games N]

Output: OUT/{anchors.npz, unaligned.npz, games.csv, splits.csv, merges.json, report.json}.
- anchors.npz: one row per linked name of an aligned segment: possession id,
  segment number, start and end in the folded segment, the player
  (nba.players id; -1 if not in nba.players), the printed name (a code
  into printed_names) and whether the row is a substitution, technical or
  ejection (bench).
- unaligned.npz: (possession id, segment) of every segment whose players are
  not all known by id: no page, no aligned row, or a name printed without a
  link (a coach's technical, for example). Readers fall back to name
  matching there, and everywhere in possessions outside covered (the
  possessions of games whose page was read).
- splits.csv: (page player, stored player, events): linked names whose page
  player is absent from the possession's stored ten while a stored player
  there prints the same name. Many events for one pair mean one player
  stored under two ids (Basketball Reference renamed Taylor Hendricks
  hendrita01 -> hendrta01 between the scrapes).
- merges.json: {stored id: page id} for those players (merges()); readers
  with exact names map the stored id to the page id everywhere.
"""
import argparse
import difflib
import gzip
import json
import re
import time
import unicodedata
from contextlib import closing
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

from lineups import db, paths
from lineups.bref_pages import PLAYER_HREF
from lineups.player_counts import repair

PAGES = paths.CACHE / "bref_raw"
NAME = re.compile(r"(?<![a-z])[a-z]\. [a-z]")
BENCH = re.compile(r"enters the game for|technical|ejected")   # rows whose players need not be on the floor
MERGE_MIN = 20             # events for a split pair to be merged (see merges)
EDITED = .8                 # least difflib similarity for a differing segment to take a page row's players
OUT = paths.CACHE / "pbp_ids_2026_10_14"


def fold_piece(text):
    """Repair, strip accents and lowercase, keeping spacing (texts are lowercase already)."""
    if text.isascii():
        return text.lower()
    s = unicodedata.normalize("NFKD", repair(text))
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def page_path(game):
    return PAGES / f"boxscores__pbp__{game}.html.html.gz"


def _pieces(el):
    out = [(el.text, None)] if el.text else []
    for child in el:
        m = PLAYER_HREF.search(child.get("href", "")) if child.tag == "a" else None
        if m:
            out.append((child.text_content(), m.group(1)))
        else:
            out.extend(_pieces(child))
        if child.tail:
            out.append((child.tail, None))
    return out


def _text(pieces, modern):
    """The cell text and the linked players' spans in it. Legacy scrape: the text nodes joined as they are,
    then stripped. Since November 2024 (lineups.ingest): each node stripped, joined by single spaces."""
    if modern:
        pieces = [(t.strip(), ref) for t, ref in pieces if t.strip()]
    spans, parts, at = [], [], 0
    for t, ref in pieces:
        if modern and parts:
            parts.append(" ")
            at += 1
        if ref is not None:
            spans.append((at, at + len(t), ref))
        parts.append(t)
        at += len(t)
    full = "".join(parts)
    lead = len(full) - len(full.lstrip())
    return full.strip(), [(s - lead, e - lead, ref) for s, e, ref in spans]


def page_events(html):
    """Each event row's folded text pieces: (text, bref id or None), in page order."""
    import lxml.html
    tree = lxml.html.fromstring(html)
    tables = tree.xpath('//table[@id="pbp"]')
    if not tables:
        raise ValueError("no play-by-play table")
    events = []
    for tr in tables[0].iter("tr"):
        tds = tr.findall("td")
        if len(tds) != 6:
            continue
        td = tds[1] if tds[1].text_content().strip() else tds[5]
        pieces = [(fold_piece(t), ref) for t, ref in _pieces(td)]
        if "".join(t for t, _ in pieces).strip():
            events.append(pieces)
    return events


def stored_form(events, segments):
    """The page's events as stored, in whichever form (legacy or since November 2024) matches more segments:
    [(text, spans)]."""
    forms = [[_text(e, modern) for e in events] for modern in (False, True)]
    present = set(segments)
    return max(forms, key=lambda f: sum(t in present for t, _ in f))


def _locate(segment, page_text, spans):
    """The spans' names found in order in a differing stored segment, or None."""
    out, cursor = [], 0
    for s, e, ref in spans:
        name = page_text[s:e]
        j = segment.find(name, cursor)
        if j < 0 or not name:
            return None
        out.append((j, j + len(name), ref))
        cursor = j + len(name)
    return out


def _unlinked(segment, spans):
    """Whether the segment still prints a name ("x. name") outside its linked spans."""
    rest = list(segment)
    for a, b, _ in spans:
        rest[a:b] = " " * (b - a)
    return NAME.search("".join(rest)) is not None


def align_game(args):
    """(anchors, unaligned, stats) for one game.

    anchors: (possession id, segment, start, end, bref id, printed name, bench row) per linked name of an
    aligned segment; a bench row is a substitution, technical or ejection, whose players need not be on the
    floor at the possession's end. unaligned: (possession id, segment) for every segment of a game with a page
    whose players are not all known by id: no aligned row, or a printed name without a link."""
    game, poss_ids, texts = args
    stats = dict(game=game, segments=0, equal=0, edited=0, unmatched=0, unlinked=0, anchors=0, page=True)
    segs = [(pid, k, fold_piece(x)) for pid, t in zip(poss_ids, texts) for k, x in enumerate(t.split("/n")) if x]
    stats["segments"] = len(segs)
    try:
        pieces = page_events(gzip.open(page_path(game), "rt", encoding="utf-8").read())
    except (OSError, ValueError):
        stats["page"] = False                       # not covered: readers use names throughout
        stats["unmatched"] = len(segs)
        return [], [], stats
    a = [x for _, _, x in segs]
    events = stored_form(pieces, a)
    b = [t for t, _ in events]
    anchors, unaligned = [], []

    def take(i, spans):
        pid, k, seg = segs[i]
        if _unlinked(seg, spans):
            stats["unlinked"] += 1
            unaligned.append((pid, k))
        bench = BENCH.search(seg) is not None
        anchors.extend((pid, k, x, y, ref, seg[x:y], bench) for x, y, ref in spans)

    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                take(i, events[j][1])
            stats["equal"] += i2 - i1
        elif tag == "replace":
            # pair in order each differing segment with the next similar row whose names it contains
            j = j1
            for i in range(i1, i2):
                for jj in range(j, j2):
                    found = _locate(segs[i][2], *events[jj])
                    if found is not None and difflib.SequenceMatcher(None, segs[i][2], b[jj]).ratio() >= EDITED:
                        take(i, found)
                        stats["edited"] += 1
                        j = jj + 1
                        break
                else:
                    stats["unmatched"] += 1
                    unaligned.append(segs[i][:2])
        else:
            stats["unmatched"] += i2 - i1
            unaligned.extend(x[:2] for x in segs[i1:i2])
    stats["anchors"] = len(anchors)
    return anchors, unaligned, stats


def tokens(canonical, bref_of):
    """pid -> the name the readers should match: his canonical name (scripts/legacy_names.py), made unique
    with his Basketball Reference id when another player has the same canonical name."""
    owners = pd.Series(list(canonical.values())).value_counts()
    return {pid: c if owners[c] == 1 else f"{c}-{bref_of[pid]}" for pid, c in canonical.items()}


def rewrite(texts, spans, token):
    """texts with each linked name replaced by its player's token. spans: [(segment, start, end, pid)] of
    one possession, positions in the folded segment. Segments with a span come back folded."""
    segs = texts.split("/n")
    by = {}
    for k, s, e, p in spans:
        by.setdefault(int(k), []).append((int(s), int(e), int(p)))
    for k, sp in by.items():
        seg = fold_piece(segs[k])
        for s, e, p in sorted(sp, reverse=True):
            if p in token:
                seg = seg[:s] + token[p] + seg[e:]
        segs[k] = seg
    return "/n".join(segs)


TEN = [f"away_player_{i}_id" for i in range(1, 6)] + [f"home_player_{i}_id" for i in range(1, 6)]


def read(season=None, games=None, table="nba.possessions"):
    """nba.players (id, bref id, folded legacy name) and possessions (game, id, the ten, texts) of one season
    or of the listed games, from table (nba_pages.possessions: lineups.page_possessions)."""
    from lineups.player_counts import fold, legacy_name
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute("select id, player_id, first_name, last_name from nba.players")
        players = pd.DataFrame(cur.fetchall(), columns=["id", "bref", "first", "last"])
        if games is not None:
            where, arg = "where g.game_id = any(%s)", (list(games),)
        else:
            where, arg = "where g.game_date >= %s and g.game_date < %s", (f"{season - 1}-09-01", f"{season}-09-01")
        cols = ", ".join("p." + c for c in TEN)
        cur.execute(f"""select g.game_id, p.id, {cols}, p.texts from {table} p join nba.games g on g.id = p.game_id
                        {where} order by g.game_date, g.game_id, p.id""", arg)
        df = pd.DataFrame(cur.fetchall(), columns=["game", "pid", *TEN, "texts"])
    df["texts"] = df.texts.fillna("")
    players["name"] = [fold(legacy_name(f, l)) if f and l and l.strip() else "" for f, l in zip(players["first"], players["last"])]
    return players, df


def _absent(arr, poss_ids, ten, names):
    """Linked players of event rows (not bench rows) absent from their possession's stored ten, and for each the
    stored players of that ten who print the same name: (count, [(page player, stored player)])."""
    row = pd.Series(np.arange(len(poss_ids)), index=poss_ids)
    r = row.reindex(arr["poss"]).to_numpy()
    off = ~(ten[r] == arr["player"][:, None]).any(1) & ~arr["bench"]
    pairs = []
    for k in np.flatnonzero(off & (arr["player"] >= 0)):
        printed = arr["printed_names"][arr["printed"][k]]
        for q in ten[r[k]]:
            if names.get(int(q)) == printed:
                pairs.append((int(arr["player"][k]), int(q)))
    return int(off.sum()), pairs


def build(games=None, processes=4, log=print, table="nba.possessions"):
    """Anchors and unaligned segments of every possession (or of the listed games), read a season at a time,
    and the identity check: page players absent from the stored ten while a stored player of that ten prints
    the same name (one player stored under two ids, when Basketball Reference renamed his id)."""
    t0 = time.time()
    parts, unaligned, stats, unknown, absent, pairs, covered = [], [], [], set(), 0, [], []
    chunks = [dict(games=games)] if games is not None else [dict(season=s) for s in range(2002, 2027)]
    with Pool(processes) as pool:
        for chunk in chunks:
            players, df = read(**chunk, table=table)
            pid_of = dict(zip(players.bref, players.id))
            names = dict(zip(players.id, players.name))
            jobs = [(g, d.pid.to_numpy(), d.texts.to_list()) for g, d in df.groupby("game", sort=False)]
            poss_ids, ten = df.pid.to_numpy(), df[TEN].to_numpy(np.int64)
            del df
            rows = []
            for (g, ids, _), (r, u, st) in zip(jobs, pool.imap(align_game, jobs, chunksize=8)):
                rows.extend(r)
                unaligned.extend(u)
                stats.append(st)
                if st["page"]:
                    covered.append(ids)
            printed, code = np.unique(np.array([x[5] for x in rows], dtype=str), return_inverse=True)
            arr = dict(poss=np.array([x[0] for x in rows], np.int64), segment=np.array([x[1] for x in rows], np.int16),
                       start=np.array([x[2] for x in rows], np.int16), end=np.array([x[3] for x in rows], np.int16),
                       player=np.array([pid_of.get(x[4], -1) for x in rows], np.int32), printed=code.astype(np.int32),
                       printed_names=printed, bench=np.array([x[6] for x in rows], bool))
            unknown |= {x[4] for x in rows if x[4] not in pid_of}
            del rows
            n, pr = _absent(arr, poss_ids, ten, names)
            absent += n
            pairs.extend(pr)
            parts.append(arr)
            log(f"[{time.time() - t0:.0f}s] {chunk.get('season', 'listed games')}: {len(jobs):,} games; "
                f"{sum(len(a['poss']) for a in parts):,} anchors, {len(unaligned):,} unaligned segments so far")
    vocab = np.unique(np.concatenate([a["printed_names"] for a in parts]))
    out = {k: np.concatenate([a[k] for a in parts]) for k in ("poss", "segment", "start", "end", "player", "bench")}
    out["printed"] = np.concatenate([np.searchsorted(vocab, a["printed_names"])[a["printed"]] for a in parts]).astype(np.int32)
    out["printed_names"] = vocab
    un = dict(poss=np.array([x[0] for x in unaligned], np.int64), segment=np.array([x[1] for x in unaligned], np.int16),
              covered=np.sort(np.concatenate(covered)) if covered else np.zeros(0, np.int64))
    splits = (pd.DataFrame(pairs, columns=["page_player", "stored_player"]).value_counts().rename("events").reset_index()
              if pairs else pd.DataFrame(columns=["page_player", "stored_player", "events"]))
    return out, un, pd.DataFrame(stats), dict(unknown_players=sorted(unknown), absent=absent, splits=splits)


def merges(splits, anchors):
    """{stored id: page id} for one player stored under two ids: at least MERGE_MIN events of the page player
    in slots the stored player holds, while the stored player's own id is linked on no page."""
    linked = set(np.unique(anchors["player"]).tolist())
    keep = splits[(splits.events >= MERGE_MIN) & ~splits.stored_player.isin(linked)]
    return {int(a): int(b) for a, b in zip(keep.stored_player, keep.page_player)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--games", type=int, help="only games with a cached page, at most this many (a check)")
    p.add_argument("--processes", type=int, default=4)
    p.add_argument("--out", default=str(OUT))
    p.add_argument("--table", default="nba.possessions", help="possession table (nba_pages.possessions)")
    a = p.parse_args()
    games = None
    if a.games:
        games = sorted(f.name.split("__")[2].split(".")[0] for f in PAGES.glob("boxscores__pbp__*.html.gz"))[:a.games]
    anchors, unaligned, stats, extra = build(games, a.processes, table=a.table)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / "anchors.npz", **anchors)
    np.savez_compressed(out / "unaligned.npz", **unaligned)
    stats.to_csv(out / "games.csv", index=False)
    tot = stats[["segments", "equal", "edited", "unmatched", "unlinked", "anchors"]].sum()
    extra["splits"].to_csv(out / "splits.csv", index=False)
    merged = merges(extra["splits"], anchors)
    (out / "merges.json").write_text(json.dumps({str(k): v for k, v in merged.items()}))
    report = dict(games=len(stats), games_without_page=int((~stats.page).sum()),
                  **{k: int(v) for k, v in tot.items()}, unknown_players=extra["unknown_players"],
                  anchors_absent_from_ten=extra["absent"], splits=extra["splits"].head(50).to_dict("records"),
                  merges=merged)
    (out / "report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report))


if __name__ == "__main__":
    main()
