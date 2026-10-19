"""Name matching for the per-player event counts (lineups.player_counts)."""
import unittest

import numpy as np

from lineups import player_counts as pc


class Names(unittest.TestCase):
    def test_fold_repairs_and_strips(self):
        self.assertEqual(pc.fold("MiciÄ\x87"), "micic")                  # mis-decoded in nba.players
        self.assertEqual(pc.fold("n. jokiä\x87"), "n. jokic")            # mis-decoded, then lowercased, in the text
        self.assertEqual(pc.fold("v. krejčí"), "v. krejci")
        self.assertEqual(pc.fold("h. gonzález  peña"), "h. gonzalez pena")
        self.assertEqual(pc.fold("plain name"), "plain name")

    def test_legacy_name(self):
        self.assertEqual(pc.legacy_name("Gary", "Payton II"), "g. payton")
        self.assertEqual(pc.legacy_name("Vit", "Krejci"), "v. krejci")


class Aliases(unittest.TestCase):
    """Player 7 is on the floor for every possession; the other nine slots rotate through a pool."""

    def setUp(self):
        rng = np.random.default_rng(0)
        n = 60
        others = np.stack([rng.choice(np.arange(20, 60), 9, replace=False) for _ in range(n)])
        self.ten = np.c_[np.full(n, 7), others]
        self.game = np.repeat(np.arange(n // 2), 2)
        self.rows = np.arange(n)

    def test_alias_goes_to_the_player_always_on_the_floor(self):
        nms = np.array(["b. smith"] * 60, dtype=object)
        found, _ = pc.learn_aliases(self.ten, self.rows, nms, np.full(60, -1), self.game)
        self.assertEqual(found, {"b. smith": 7})

    def test_teammate_with_his_own_events_is_refused(self):
        # "d. ewing" acts while missing from the recorded lineup; player 7 is on the floor every time,
        # but he has events under his own name in those games, so the name is not his
        nms = np.array(["d. ewing", "a. seven"] * 30, dtype=object)
        who = np.where(nms == "a. seven", 7, -1)
        found, table = pc.learn_aliases(self.ten, self.rows, nms, who, self.game)
        self.assertEqual(found, {})
        self.assertEqual(int(table.pid.iloc[0]), 7)
        self.assertGreater(int(table.own.iloc[0]), 0)

    def test_events_under_an_accepted_alias_count_as_his_own(self):
        # player 7 is printed "b. smith" (large) and, in the same games, "j. reese" appears (small):
        # the small name must not go to 7 as well
        nms = np.array(["b. smith"] * 40 + ["j. reese"] * 20, dtype=object)
        found, _ = pc.learn_aliases(self.ten, self.rows, nms, np.full(60, -1), np.r_[np.arange(40) % 20, np.arange(20)])
        self.assertEqual(found, {"b. smith": 7})


if __name__ == "__main__":
    unittest.main()
