"""The combination layer (lineups.combinations): pair counting, the orthogonal term, values, and lineup properties."""
import unittest

import numpy as np

from lineups import combinations as cb
from lineups import players, release


class PairCounting(unittest.TestCase):
    def test_same_type_and_overlapping_pairs(self):
        # five players; columns: X, Y. Players 0-2 are X, players 2-3 are Y (player 2 is both)
        f = np.zeros((1, 5, 2), bool)
        f[0, [0, 1, 2], 0] = True
        f[0, [2, 3], 1] = True
        n, pairs = cb.pair_features(f, ("X", "Y"), [("X", "X"), ("X", "Y")])
        self.assertEqual(n["X"][0], 3)
        self.assertEqual(pairs[("X", "X")][0], 3)              # C(3, 2)
        self.assertEqual(pairs[("X", "Y")][0], 3 * 2 - 1)      # ordered i != j

    def test_caps_hold_counts_at_the_measured_maximum(self):
        f = np.ones((1, 5, 1), bool)
        n, pairs = cb.pair_features(f, ("X",), [("X", "X")], dict(X=3))
        self.assertEqual(n["X"][0], 3)
        self.assertEqual(pairs[("X", "X")][0], 3)
        _, free = cb.pair_features(f, ("X",), [("X", "X")])
        self.assertEqual(free[("X", "X")][0], 10)


class LayerTerm(unittest.TestCase):
    def spec(self):
        return dict(measured_max={t: 3 for t in cb.TYPES},
                    events=dict(rim_share=dict(types=["D_big"], pairs=[["defense", "D_big", "D_big"]], beta=[.5],
                                               intercept=[.2], slopes=[[.4]])))

    def test_change_is_beta_times_pairs_beyond_the_additive_expectation(self):
        layer = cb.Layer(self.spec())
        o = np.zeros((3, 5, len(cb.OFFENSE)), bool)
        d = np.zeros((3, 5, len(cb.DEFENSE)), bool)
        for b, bigs in enumerate((0, 2, 5)):
            d[b, :bigs, cb.DEFENSE.index("D_big")] = True
        got = layer.deltas(o, d)["rim_share:D_bigxD_big"]
        n = np.array([0, 2, 3.])                                 # capped at 3
        np.testing.assert_allclose(got, .5 * (n * (n - 1) / 2 - .2 - .4 * n))
        free = layer.deltas(o, d, cap=False)["rim_share:D_bigxD_big"]
        self.assertAlmostEqual(free[2], .5 * (10 - .2 - .4 * 5))


class Values(unittest.TestCase):
    def test_accounting(self):
        attempts = np.array([.3, .1, .1, .1, .05, .25])
        makes = attempts * np.array([.65, .42, .42, .4, .38, .36])
        v = cb.values(.88, attempts, makes, (2, 2, 2, 2, 3, 3), (0,), (4, 5), .78, 1.14, .13)
        value = makes / attempts * np.array([2, 2, 2, 2, 3, 3.])
        rest = (attempts[1:] * value[1:]).sum() / attempts[1:].sum()
        self.assertAlmostEqual(v["rim_share"], .88 * (value[0] - rest))
        self.assertAlmostEqual(v["tov"], -1.14 / .87)
        self.assertAlmostEqual(v["fta"], .78 - .5 * (attempts * value).sum() / attempts.sum())
        bad = cb.values(.88, attempts, attempts * np.array([.65, .42, .42, .4, .1, .1]), (2, 2, 2, 2, 3, 3),
                        (0,), (4, 5), .78, 1.0, .13)
        self.assertLess(bad["three_share"], 0)                  # moving shots outside costs a poor shooting five


class OnTheRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rel = release.Release()
        cls.comb = cb.Combinations(cls.rel)
        from lineups.explain import Explainer
        cls.ex = Explainer(cls.rel)
        t = cls.rel.seasons.table
        rng = np.random.default_rng(3)
        cls.fives = [rng.choice(np.flatnonzero(t["season"] == s), 5, replace=False) for s in (2008, 2019, 2026)]

    def test_types_agree_across_rules_for_the_latest_season(self):
        latest = self.rel.seasons.table["season"] == self.rel.seasons.latest
        np.testing.assert_array_equal(self.comb.flags["relative"][latest], self.comb.flags["as_was"][latest])

    def test_layer_ignores_order_and_negates_on_swap(self):
        a, b = self.fives[0], self.fives[1]
        rates = lambda x, y: self.ex.against(x, y)["rates"]
        m = self.comb.matchup(a, b, rates(a, b), rates(b, a))
        swapped = self.comb.matchup(b[::-1], a[::-1], rates(b[::-1], a[::-1]), rates(a[::-1], b[::-1]))
        self.assertAlmostEqual(m["layer"]["margin"], -swapped["layer"]["margin"], 6)
        self.assertAlmostEqual(m["layer"]["a_offense"], swapped["layer"]["b_offense"], 6)

    def test_panel_pairs_are_near_zero(self):
        for means in self.comb.panel.values():
            self.assertLess(abs(sum(means.values())), .5)

    def test_measured_range_never_exceeds_continued_counts(self):
        rows = self.fives[2]
        terms, free = self.comb.terms(rows[None], rows[None]), self.comb.terms(rows[None], rows[None], cap=False)
        for k in terms:
            self.assertLessEqual(float(terms[k][1][0]), float(free[k][1][0]))


if __name__ == "__main__":
    unittest.main()
