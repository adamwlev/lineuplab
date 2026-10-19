"""Out-of-support reasons fire for impossible fixtures and not for a real lineup (needs local caches)."""
import unittest

from lineups import paths


@unittest.skipUnless(paths.STORE.exists() and (paths.STORE / "players.npz").exists() and paths.V16_RUN.exists(),
                     "local caches absent")
class SupportReasons(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.coherence import fixtures
        from lineups.features import Store
        from lineups.support import Support
        cls.support, cls.fx = Support(Store(), "2026q4"), fixtures()

    def describe(self, name):
        pids = self.fx[name]["pids"]
        return self.support.describe(pids, pids)

    def test_real_lineup_is_inside_support(self):
        d = self.describe("highest_exposure_real_2026")
        self.assertEqual(d["reasons"], [])
        self.assertLess(d["offense_percentile"], .5)

    def test_five_goberts_names_every_gap(self):
        reasons = " | ".join(self.describe("five_goberts")["reasons"])
        for phrase in ("offense composition beyond", "defense composition beyond", "no ball handler",
                       "no shooter", "non-spacing bigs", "offense repeats a player"):
            self.assertIn(phrase, reasons)

    def test_five_jokics_have_a_handler(self):
        reasons = " | ".join(self.describe("five_jokics")["reasons"])
        self.assertNotIn("no ball handler", reasons)
        self.assertIn("repeats a player", reasons)


if __name__ == "__main__":
    unittest.main()
