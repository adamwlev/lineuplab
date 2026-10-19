"""Rung 3: lineups.features rebuilds the exact model inputs of the old pipeline.

Needs the local store (experiments/cache/lineups_store_v16); skipped elsewhere.
Run: python -m unittest tests.test_feature_parity
"""
from pathlib import Path
import unittest

import numpy as np

from lineups import paths

FIXTURES = Path(__file__).parent / "fixtures"


@unittest.skipUnless(paths.STORE.exists(), "local lineups store absent")
class FeatureParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.features import Store
        cls.store = Store()

    def check(self, fixture, new):
        """Every input of the old pipeline is reproduced exactly; newer optional inputs may be added."""
        old = [k[len("input_"):] for k in fixture.files if k.startswith("input_")]
        self.assertTrue(old)
        for key in old:
            with self.subTest(key=key):
                np.testing.assert_array_equal(new[key].numpy(), fixture["input_" + key])

    def test_origin_mode_reference_batch(self):
        z = np.load(FIXTURES / "reference_2020q1_s17.npz")
        from lineups.legacy import origins
        origin = origins().query("tag == '2020q1'").iloc[0]
        new = self.store.batch(z["offense"], z["defense"], z["date"], self.store.normalizer("2020q1", "final"),
                               origin_index=int(origin.origin_index))
        self.check(z, new)

    def test_history_mode_training_batch(self):
        z = np.load(FIXTURES / "history_2020q1_final.npz")
        new = self.store.batch(z["offense"], z["defense"], z["date"], self.store.normalizer("2020q1", "final"),
                               game_ids=z["game_id"])
        self.check(z, new)

    def test_assignment_pairs_sorted_positions_and_ignores_slot_order(self):
        if self.store.players is None:
            self.skipTest("players.npz absent")
        offense = np.array([[10, 20, 30, 40, 50]])
        defense = np.array([[60, 70, 80, 90, 100]])
        a = self.store.listings(offense, defense)
        matched = a["matched"][0].numpy()
        self.assertEqual(sorted(matched), list(range(5)))              # one defender per attacker
        players = self.store.players
        key = lambda pid: (players["position"][pid], players["height"][pid], pid)
        attackers = sorted(range(5), key=lambda i: key(offense[0, i]))
        self.assertEqual([key(defense[0, matched[i]]) for i in attackers],
                         sorted(key(d) for d in defense[0]))           # sorted attackers get sorted defenders
        perm_o, perm_d = np.array([3, 0, 4, 1, 2]), np.array([2, 4, 0, 3, 1])
        b = self.store.listings(offense[:, perm_o], defense[:, perm_d])
        pairs = lambda o, d, m: sorted(zip(o[0], d[0][m]))
        self.assertEqual(pairs(offense, defense, matched),
                         pairs(offense[:, perm_o], defense[:, perm_d], b["matched"][0].numpy()))

    def test_origin_mode_query_day_moves_only_the_capability_banks(self):
        z = np.load(FIXTURES / "reference_2020q1_s17.npz")
        from lineups.legacy import origins
        origin = int(origins().query("tag == '2020q1'").iloc[0].origin_index)
        n = self.store.normalizer("2020q1", "final")
        args = (z["offense"], z["defense"], z["date"], n)
        default = self.store.batch(*args, origin_index=origin)
        same = self.store.batch(*args, origin_index=origin, query_day=int(n["cutoff_day"]))
        earlier = self.store.batch(*args, origin_index=origin, query_day=int(n["cutoff_day"]) - 400)
        for key, value in default.items():
            self.assertTrue(np.array_equal(value.numpy(), same[key].numpy()), key)
            moved = not np.array_equal(value.numpy(), earlier[key].numpy())
            self.assertEqual(moved, key in ("adjusted_offense", "adjusted_defense"), key)

    def test_unknown_player_gets_origin_fallback(self):
        unknown = np.array([[10**9] * 5])
        out = self.store.offense(unknown, origin_index=20)
        np.testing.assert_array_equal(out["base"][0, 0], self.store.offense_origins["fallback_base"][20])
        self.assertTrue(np.all(out["rb_neff"] == 0))


if __name__ == "__main__":
    unittest.main()
