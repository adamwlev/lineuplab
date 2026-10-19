"""The learned combinations in the release (lineups.learned, lineups.release, lineups.band)."""
import unittest

import numpy as np

from lineups import learned, players, release
from lineups.band import Band


class WithLayer(unittest.TestCase):
    by_arm = dict(R=dict(margin=2.), C=dict(margin=1.))
    layer = dict(layer=dict(margin=.5), continued=dict(margin=.8))

    def test_learned_joins_every_assumption_but_n(self):
        v = Band.with_layer(self.by_arm, ["margin"], self.layer, dict(margin=-1.))["margin"]
        want = dict(R=1.5, C=.5, K=1.8, N=2.5)
        self.assertEqual(set(v), set(want))
        for k in want:
            self.assertAlmostEqual(v[k], want[k], places=12)

    def test_without_learned_nothing_changes(self):
        v = Band.with_layer(self.by_arm, ["margin"], self.layer)["margin"]
        self.assertEqual(v, dict(R=2.5, C=1.5, K=2.8))

    def test_reason_only_past_the_threshold(self):
        self.assertEqual(Band.learned_reasons(dict(margin=.9), "margin", "net"), [])
        self.assertTrue(Band.learned_reasons(dict(margin=-1.2), "margin", "net")[0].startswith("assumption N"))


@unittest.skipUnless(all(learned.path(s).exists() for s in release.SEEDS)
                     and (players.TABLE / "player_seasons.npz").exists(), "release modules absent")
class ReleaseLearned(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.coherence import fixtures
        cls.rel = release.Release(arms=("R",))
        fx = fixtures()
        cls.five = {k: cls.rel.seasons.rows(fx[k]["pids"], np.full(5, 2026))
                    for k in ("five_goberts", "legal_pure_centers", "jokic_westbrook")}

    def test_network_alone_is_untouched(self):
        a, b = self.five["jokic_westbrook"], self.five["five_goberts"]
        before = self.rel.season_points([a], [b], "R")
        self.rel.season_learned([a], [b])
        self.assertTrue(all(m.pairs is None for s in release.SEEDS for m in self.rel.models["R"][s]))
        self.assertEqual(float(before[0]), float(self.rel.season_points([a], [b], "R")[0]))

    def test_clone_bigs_offense_not_inflated(self):
        # the confirmation's bar (reports/learned_module_confirmation_protocol_2026_10_14.md): at most +1 per 100
        for k in ("five_goberts", "legal_pure_centers"):
            self.assertLessEqual(self.rel.season_learned_ratings(self.five[k])["offense"], 1., k)

    def test_half_strength_of_the_centered_module(self):
        a, b = self.five["five_goberts"], self.five["jokic_westbrook"]
        got = self.rel.season_learned([a], [b])["points"][0]
        inputs = self.rel.inputs([a], [b])
        want = []
        for seed in release.SEEDS:
            module, level = self.rel.modules[seed]
            off, on = learned.ledgers_with(self.rel.models["R"][seed], module, inputs, self.rel.env)
            slope = self.rel.record["calibration"][f"R_s{seed}"]["slope"]
            want.append(slope * .5 * (float(on.points100[0]) - float(off.points100[0]) - level["points"]))
        self.assertAlmostEqual(got, float(np.mean(want)), places=9)


if __name__ == "__main__":
    unittest.main()
