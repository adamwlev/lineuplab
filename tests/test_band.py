"""The band widens with named reasons off support and stays narrow on a real lineup (needs local caches)."""
import unittest

import numpy as np

from lineups import players, release
from lineups.band import TAU2              # the active source's constants (19.83 on the old data; refreshed on the clean)


@unittest.skipUnless(release.RECORD.exists() and (players.TABLE / "player_seasons.npz").exists(), "local caches absent")
class BandReasons(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.band import Band
        from lineups.coherence import fixtures
        cls.band, cls.fx = Band(), fixtures()
        seasons = cls.band.seasons
        cls.rows = lambda self, name, season=2026: seasons.rows(self.fx[name]["pids"], np.full(5, season))
        by_name = {}
        for pid, name in seasons.names.items():
            by_name.setdefault(name, []).append(pid)
        cls.celtics_2008 = seasons.rows([by_name[n][0] for n in ("Rajon Rondo", "Ray Allen", "Paul Pierce",
                                                                 "Kevin Garnett", "Kendrick Perkins")], np.full(5, 2008))
        cls.real = cls.band.lineup(cls.rows(cls, "highest_exposure_real_2026"))
        cls.goberts = cls.band.lineup(cls.rows(cls, "five_goberts"))

    def test_real_lineup_has_no_reasons_and_the_in_support_width(self):
        self.assertEqual(self.real["reasons"], [])
        m = self.real["margin"]
        self.assertLess(m["assumption_high"] - m["assumption_low"], 1.)
        self.assertAlmostEqual(m["sd"], np.sqrt(TAU2["margin"]), places=6)    # the in-support width: tau alone

    def test_five_goberts_band_is_wide_and_says_why(self):
        m = self.goberts["margin"]
        self.assertLess(m["low"], m["point"] - 10)
        reasons = " | ".join(self.goberts["reasons"])
        for phrase in ("no ball handler", "no shooter", "non-spacing bigs", "repeats a player",
                       "assumption C, capacity defense"):
            self.assertIn(phrase, reasons)

    def test_five_jokics_have_a_handler(self):
        reasons = " | ".join(self.band.lineup(self.rows("five_jokics"))["reasons"])
        self.assertNotIn("no ball handler", reasons)

    def test_swapping_teams_negates_every_arm(self):
        a, b = self.rows("jokic_westbrook"), self.celtics_2008
        ab, ba = self.band.matchup(a, b), self.band.matchup(b, a)
        for arm in ab["arms"]:
            self.assertAlmostEqual(ab["arms"][arm]["margin"], -ba["arms"][arm]["margin"], places=4)

    def test_cross_era_lineup_is_compared_with_its_own_season(self):
        r = self.band.lineup(self.celtics_2008)
        reasons = " | ".join(r["reasons"])
        self.assertIn("cross-era", reasons)
        self.assertNotIn("composition beyond", reasons)
        self.assertGreater(r["margin"]["sd"], self.real["margin"]["sd"])


if __name__ == "__main__":
    unittest.main()
