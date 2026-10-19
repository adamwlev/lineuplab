"""Explanations are accounting on the release forecast: channels sum to the rating gap (needs local caches)."""
import unittest

import numpy as np

from lineups import players, release


@unittest.skipUnless(release.RECORD.exists() and (players.TABLE / "player_seasons.npz").exists(), "local caches absent")
class Explanations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.coherence import fixtures
        from lineups.explain import Explainer
        cls.release = release.Release(arms=("R",))
        cls.explainer, cls.fx = Explainer(cls.release), fixtures()

    def rows(self, name):
        return self.release.seasons.rows(self.fx[name]["pids"], np.full(5, 2026))

    def test_channels_sum_to_the_gap_from_the_league_average_offense(self):
        native = 100 * self.explainer.league["points"]
        cal = self.release.record["calibration"]
        league = np.mean([self.release.league + cal[f"R_s{s}"]["intercept"]
                          + cal[f"R_s{s}"]["slope"] * (native - self.release.league) for s in release.SEEDS])
        for name in ("five_goberts", "jokic_westbrook"):
            e = self.explainer.lineup(self.rows(name))
            gap = self.release.season_ratings(self.rows(name))["offense"] - league
            self.assertAlmostEqual(sum(e["channels"].values()), gap, delta=.05)

    def test_clones_share_usage_equally(self):
        e = self.explainer.lineup(self.rows("five_goberts"))
        for p in e["players"]:
            self.assertAlmostEqual(p["usage_share"], .2, places=6)
            self.assertAlmostEqual(p["usual_share"], .2, places=6)


if __name__ == "__main__":
    unittest.main()
