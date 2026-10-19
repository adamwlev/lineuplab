"""Exact player ids for the stored play-by-play text (lineups.pbp_ids, lineups.names)."""
import gzip
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from lineups import pbp_ids
from lineups.names import Names

ROW = ('<tr><td>11:44.0</td><td class="">{away}</td><td></td><td>0-0</td><td></td>'
       '<td class="">{home}</td></tr>')
LINK = '<a href="/players/{i}/{ref}.html">{name}</a>'
SHOT = "j. williams makes 2-pt jump shot from 9 ft (assist by j. williams)"


def page(rows):
    body = "".join(ROW.format(away=a, home=h) for a, h in rows)
    return f'<html><body><table id="pbp"><tr><th colspan="6">1st Q</th></tr>{body}</table></body></html>'


def link(ref, name):
    return LINK.format(i=ref[0], ref=ref, name=name)


class PageText(unittest.TestCase):
    def test_spans_in_both_stored_forms(self):
        html = page([(f"Turnover by {link('castlst01', 'S. Castle')} (lost ball; steal by {link('townska01', 'K. Towns')})", "")])
        (pieces,) = pbp_ids.page_events(html)
        for modern, text in ((False, "turnover by s. castle (lost ball; steal by k. towns)"),
                             (True, "turnover by s. castle (lost ball; steal by k. towns )")):
            got, spans = pbp_ids._text(pieces, modern)
            self.assertEqual(got, text)
            self.assertEqual([(got[s:e], ref) for s, e, ref in spans], [("s. castle", "castlst01"), ("k. towns", "townska01")])

    def test_accents_are_folded_and_home_cells_read(self):
        (pieces,) = pbp_ids.page_events(page([("", f"{link('krejcvi01', 'V. Krejčí')} makes 2-pt layup at rim")]))
        text, spans = pbp_ids._text(pieces, False)
        self.assertEqual(text, "v. krejci makes 2-pt layup at rim")
        self.assertEqual(spans, [(0, 9, "krejcvi01")])


class Align(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        rows = [(f"{link('willija06', 'J. Williams')} makes 2-pt jump shot from 9 ft (assist by {link('willija07', 'J. Williams')})", ""),
                ("", f"Defensive rebound by {link('greenja05', 'J. Green')}"),
                (f"Technical foul by {link('willija06', 'J. Williams')}", ""),
                (f"{link('greenje02', 'J. Green')} misses 3-pt jump shot from 25 ft", "")]
        self.path = Path(self.dir.name) / "g.html.gz"
        with gzip.open(self.path, "wt", encoding="utf-8") as f:
            f.write(page(rows))

    def tearDown(self):
        self.dir.cleanup()

    def test_equal_edited_unlinked_and_missing(self):
        texts = ["j. williams makes 2-pt jump shot from 9 ft (assist by j. williams)/ndefensive rebound by j. green",
                 "technical foul by j. williams/nj. green misses 3-pt jump shot from 24 ft",   # page edited: 25 ft
                 "flagrant foul by d. rivers"]                                                  # no page row
        with mock.patch.object(pbp_ids, "page_path", return_value=self.path):
            anchors, unaligned, stats = pbp_ids.align_game(("g", np.array([1, 2, 3]), texts))
        self.assertEqual([a[6] for a in anchors], [False, False, False, True, False])     # the technical
        self.assertEqual([(a[0], a[1], a[4]) for a in anchors],
                         [(1, 0, "willija06"), (1, 0, "willija07"), (1, 1, "greenja05"), (2, 0, "willija06"), (2, 1, "greenje02")])
        self.assertEqual(stats["equal"], 3)
        self.assertEqual(stats["edited"], 1)
        self.assertIn((3, 0), unaligned)
        seg = texts[0].split("/n")[0]
        self.assertEqual([seg[a[2]:a[3]] for a in anchors[:2]], ["j. williams", "j. williams"])
        self.assertEqual(anchors[1][2], seg.rindex("j. williams"))
        with mock.patch.object(pbp_ids, "page_path", return_value=Path(self.dir.name) / "none.gz"):
            _, unaligned, stats = pbp_ids.align_game(("g", np.array([1]), texts[:1]))
        self.assertFalse(stats["page"])
        self.assertEqual(unaligned, [])

    def test_unlinked_name_falls_back(self):
        self.assertTrue(pbp_ids._unlinked("technical foul by d. rivers", []))
        self.assertFalse(pbp_ids._unlinked("defensive rebound by team", []))
        self.assertFalse(pbp_ids._unlinked("defensive rebound by j. green", [(21, 29, "greenja05")]))


class Tokens(unittest.TestCase):
    def test_shared_canonical_names_get_the_bref_id(self):
        canonical = {1: "j. williams", 2: "j. williams", 3: "k. bryant"}
        self.assertEqual(pbp_ids.tokens(canonical, {1: "willija06", 2: "willija07", 3: "bryanko01"}),
                         {1: "j. williams-willija06", 2: "j. williams-willija07", 3: "k. bryant"})


class TextIds(unittest.TestCase):
    """Names.text_ids on hand-made anchors: exact tokens where aligned, the name fallback elsewhere."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        d = Path(self.dir.name)
        printed = np.array(["j. williams", "k. bryant"])
        # possession 10, segment 0: shooter Jalen (1), assist Jaylin (2); Bryant (3) needs no rewrite
        assist = SHOT.rindex("j. williams")
        np.savez(d / "anchors.npz", poss=np.array([10, 10, 10]), segment=np.array([0, 0, 1], np.int16),
                 start=np.array([0, assist, 21], np.int16), end=np.array([11, assist + 11, 30], np.int16),
                 player=np.array([1, 2, 3], np.int32), printed=np.array([0, 0, 1], np.int32), printed_names=printed)
        np.savez(d / "unaligned.npz", poss=np.array([11]), segment=np.array([0], np.int16), covered=np.array([10, 11, 12]))
        n = Names.__new__(Names)
        n.canonical = {1: "j. williams", 2: "j. williams", 3: "k. bryant"}
        n.owners = {"j. williams": {1, 2}, "k. bryant": {3}}
        n.rewrites, n.forms = [], {}
        n.token = pbp_ids.tokens(n.canonical, {1: "willija06", 2: "willija07", 3: "bryanko01"})
        n.shared = {"j. williams": re.compile(r"(?<![a-z])j\. williams(?![a-z'-])")}
        n.ids, n._anchors, n._dir = True, None, d
        self.names = n

    def tearDown(self):
        self.dir.cleanup()

    def test_rewrite(self):
        text = SHOT + "/ndefensive rebound by k. bryant"
        self.assertEqual(self.names.text_ids(text, [3, 1, 2], 10),
                         "j. williams-willija06 makes 2-pt jump shot from 9 ft (assist by j. williams-willija07)"
                         "/ndefensive rebound by k. bryant")
        # unaligned: the first of the ten with that canonical name, and never inside a longer name
        self.assertEqual(self.names.text_ids("j. williams misses 3-pt jump shot from 24 ft (block by j. williamson)",
                                             [3, 2, 1], 11),
                         "j. williams-willija07 misses 3-pt jump shot from 24 ft (block by j. williamson)")
        # aligned with nothing to rewrite: untouched apart from folding
        self.assertEqual(self.names.text_ids("j. williams makes free throw 1 of 2", [1, 2], 12),
                         "j. williams makes free throw 1 of 2")
        # no page read for its game: names only, every segment
        self.assertEqual(self.names.text_ids("j. williams makes free throw 1 of 2", [2, 1], 13),
                         "j. williams-willija07 makes free throw 1 of 2")


if __name__ == "__main__":
    unittest.main()
