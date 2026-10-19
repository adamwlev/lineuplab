"""Players' printed names in the play-by-play text: canonical names, aliases and exact tokens (2026-10-14).

Every reader of nba.possessions texts matches an event's actor to the players
on the floor by "first initial. last name" built from nba.players
(reports/name_matching_fix_2026_10_14.md). Names holds the fixes, applied by
scripts/legacy_names.py where the legacy builders read the database:

- canonical names: each player's form most of his events are printed under
  (his folded legacy name or a learned alias, lineups.player_counts), and
  the rewrite of his other forms where he is on the floor;
- exact tokens (ids=True): the canonical name made unique with the player's
  Basketball Reference id when another player shares it, put in place of
  every linked name of a segment aligned with its page (lineups.pbp_ids);
- merges (ids=True): a player stored under two ids is mapped to his page id
  (pbp_ids.merges), wherever player ids are read.
"""
import json
import re
import unicodedata

import numpy as np

from lineups import db, pbp_ids
from lineups import player_counts as pc


def fold_text(text):
    """Repair and strip accents; keep case and spacing (texts are lowercase already)."""
    if text is None or text.isascii():
        return text
    s = unicodedata.normalize("NFKD", pc.repair(text))
    return "".join(c for c in s if not unicodedata.combining(c))


class Names:
    """Canonical names and alias rewrites from the counts build (lineups.player_counts.OUT).

    A player's canonical name is the form most of his events are printed under: his folded legacy name or
    one of his learned aliases (an empty legacy name never wins). Every other form of his is rewritten to it
    where he is on the floor, unless that form is another player's canonical name (never rewrite a shared
    name such as "j. williams")."""

    def __init__(self, ids=False, anchors=None):
        """ids: exact tokens from the anchors in the directory anchors (default lineups.pbp_ids.OUT)."""
        import pandas as pd
        report = json.loads(pc.OUT.with_suffix(".json").read_text())
        aliases = [(r["name"], int(r["pid"]), int(r["events"])) for r in report["alias_table"] if r["accepted"]]
        with db.connect() as conn, conn.cursor() as cur:
            cur.execute("select id, first_name, last_name from nba.players")
            players = {int(i): (f or "", l or "") for i, f, l in cur.fetchall()}
        folded = {pid: pc.fold(pc.legacy_name(f, l)) for pid, (f, l) in players.items() if f and l.strip()}
        self.canonical = dict(folded)
        aliased = sorted({pid for _, pid, _ in aliases})
        own = [c for c in pd.read_pickle(pc.LEGACY).columns if c.startswith("own_") and c[4:] in {k for _, _, k in pc.PRE}]
        legacy = pd.read_pickle(pc.LEGACY).query("pid in @aliased").groupby("pid")[own].sum().sum(1)
        self.forms = {}
        for pid in aliased:
            forms = {name: events for name, p, events in aliases if p == pid}
            if pid in folded:
                forms[folded[pid]] = forms.get(folded[pid], 0) + int(legacy.get(pid, 0))
            self.canonical[pid] = max(forms, key=forms.get)
            self.forms[pid] = forms
        self.owners = {}
        for pid, c in self.canonical.items():
            self.owners.setdefault(c, set()).add(pid)
        self.rewrites = [(form, pid, self.canonical[pid]) for pid, forms in self.forms.items() for form in forms
                         if form != self.canonical[pid]]
        self.ids, self._anchors, self.merge = ids, None, {}
        self._dir = pbp_ids.OUT if anchors is None else anchors
        if ids:
            with db.connect() as conn, conn.cursor() as cur:
                cur.execute("select id, player_id from nba.players")
                bref_of = {int(i): b for i, b in cur.fetchall()}
            self.token = pbp_ids.tokens(self.canonical, bref_of)
            path = self._dir / "merges.json"
            self.merge = {int(k): v for k, v in json.loads(path.read_text()).items()} if path.exists() else {}
            self.shared = {c: re.compile(r"(?<![a-z])" + re.escape(c) + r"(?![a-z'-])")
                           for c, owners in self.owners.items() if len(owners) > 1}

    def name_row(self, pid, first, last):
        c = (self.token if self.ids else self.canonical).get(int(pid))
        if c is None or c[1:3] != ". ":
            return first, last
        return c[0], c[3:]

    def text(self, text, ten=None):
        """Fold, then rewrite a player's other forms where he is on the floor and nobody else on the floor
        owns that form as his canonical name. Without the ten, only forms nobody owns are rewritten."""
        text = fold_text(text)
        if text is None:
            return text
        for form, pid, canon in self.rewrites:
            if form not in text:
                continue
            owners = self.owners.get(form, set()) - {pid}
            if ten is None:
                ok = not owners
            else:
                ok = pid in ten and not (owners & ten)
            if ok:
                text = text.replace(form, canon)
        return text


    def _load(self):
        """Anchors whose printed name differs from their player's token, and unaligned segments, sorted."""
        a = np.load(self._dir / "anchors.npz", allow_pickle=False)
        u = np.load(self._dir / "unaligned.npz", allow_pickle=False)
        names = a["printed_names"]
        player = a["player"]
        uniq, inv = np.unique(player, return_inverse=True)
        tok = np.array([self.token.get(int(p), "") for p in uniq], dtype=object)[inv]
        need = (tok != "") & (tok != names[a["printed"]].astype(object))
        order = np.lexsort((-a["start"][need].astype(np.int64), a["segment"][need], a["poss"][need]))
        sel = np.flatnonzero(need)[order]
        self._anchors = dict(poss=a["poss"][sel], segment=a["segment"][sel], start=a["start"][sel],
                             end=a["end"][sel], token=tok[sel])
        key = u["poss"].astype(np.int64) * 1024 + u["segment"]
        self._unaligned = np.sort(key)
        self._covered = u["covered"]
        print(f"name ids: {len(sel):,} of {len(player):,} linked names rewritten; "
              f"{len(key):,} segments fall back to names", flush=True)

    def text_ids(self, text, ten, poss):
        """--ids: exact tokens on aligned segments, the name fallback elsewhere (module docstring)."""
        if text is None:
            return text
        if self._anchors is None:
            self._load()
        A = self._anchors
        segs = [pbp_ids.fold_piece(x) for x in text.split("/n")]
        c = np.searchsorted(self._covered, poss)
        if c == len(self._covered) or self._covered[c] != poss:      # no page read: names only
            return "/n".join(self._fallback(x, ten) for x in segs)
        i, j = np.searchsorted(A["poss"], [poss, poss + 1])
        for r in range(i, j):                        # within a segment, rightmost first
            k, s, e = int(A["segment"][r]), int(A["start"][r]), int(A["end"][r])
            segs[k] = segs[k][:s] + A["token"][r] + segs[k][e:]
        U = self._unaligned
        lo, hi = np.searchsorted(U, [poss * 1024, (poss + 1) * 1024])
        for key in U[lo:hi]:
            k = int(key - poss * 1024)
            if k < len(segs):
                segs[k] = self._fallback(segs[k], ten)
        return "/n".join(segs)

    def _fallback(self, seg, ten):
        seg = self.text(seg, set(ten))
        for c, pattern in self.shared.items():
            if c in seg:
                first = next((p for p in ten if self.canonical.get(p) == c), None)
                if first is not None:
                    seg = pattern.sub(self.token[first], seg)
        return seg
