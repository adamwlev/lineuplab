"""The release model reproduces the frozen 2027q1 record and keeps the matchup symmetries (needs local caches)."""
import unittest

import numpy as np

from lineups import release


@unittest.skipUnless(release.FROZEN_RECORD.exists() and release.FROZEN_STORE.exists(), "local caches absent")
class ReleaseModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.coherence import fixtures
        cls.release, cls.fx = release.Release(store=release.FROZEN_STORE, fits=release.FROZEN_FITS,
                                              record=release.FROZEN_RECORD), fixtures()

    def test_reproduces_frozen_fixture_table(self):
        import pandas as pd
        frozen = pd.read_csv(release.FROZEN_FITS / "freeze" / "fixtures_vs_average.csv")
        offense = np.array([self.fx[n]["pids"] for n in frozen.fixture])
        for arm in release.ARMS:
            native = self.release.native(arm, offense, None)
            np.testing.assert_allclose(native.mean(0), frozen[f"{arm}_native"], atol=1e-9)
            np.testing.assert_allclose(self.release.calibrate(arm, native), frozen[f"{arm}_calibrated"], atol=1e-9)

    def test_swapping_teams_negates_the_margin(self):
        a, b = self.fx["five_goberts"]["pids"], self.fx["jokic_westbrook"]["pids"]
        for arm in release.ARMS:
            self.assertAlmostEqual(self.release.matchup(a, b, arm)["margin"],
                                   -self.release.matchup(b, a, arm)["margin"], places=5)

    def test_lineup_order_does_not_matter(self):
        a, b = self.fx["highest_exposure_real_2026"]["pids"], self.fx["jokic_westbrook"]["pids"]
        for arm in release.ARMS:
            forward = self.release.matchup(a, b, arm)
            shuffled = self.release.matchup(a[::-1], [b[i] for i in (2, 0, 4, 1, 3)], arm)
            self.assertAlmostEqual(forward["a_offense"], shuffled["a_offense"], places=4)
            self.assertAlmostEqual(forward["b_offense"], shuffled["b_offense"], places=4)

    def test_player_season_rows_equal_the_store_for_the_latest_season(self):
        current = release.Release()                  # the tool's store: the table is built from it
        five = self.fx["highest_exposure_real_2026"]["pids"]
        rows = current.seasons.rows(five, np.full(5, 2026))
        for arm in ("R", "C"):
            self.assertEqual(current.ratings(five, arm), current.season_ratings(rows, arm))

    def test_ratings_average_the_panel(self):
        five = self.fx["highest_exposure_real_2026"]["pids"]
        defenses, weights = self.release.panel["defense"]
        self.assertGreater(len(defenses), 100)
        self.assertAlmostEqual(weights.sum(), 1.)
        direct = weights @ self.release.points(np.repeat([five], len(defenses), 0), defenses)
        self.assertAlmostEqual(self.release.ratings(five)["offense"], direct, places=10)


if __name__ == "__main__":
    unittest.main()
