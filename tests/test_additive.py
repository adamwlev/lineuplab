"""Rung 5: the ported additive control reproduces the saved per-row additive_defense (needs local caches)."""
import json
import unittest

import numpy as np
import pandas as pd

from lineups import additive, legacy, paths


@unittest.skipUnless(additive.CENTERED.exists() and paths.V16_CONTROLS.exists(), "local caches absent")
class AdditiveParity(unittest.TestCase):
    def test_parameters_and_rows(self):
        g = legacy.matchups()
        for tag in ("2016q1", "2026q4"):
            a = additive.Additive(tag)
            ref = json.loads((additive.CENTERED / tag / "reference.json").read_text())
            v15 = json.loads((paths.V15_ARCHIVE / "controls" / f"{tag}.json").read_text())
            cal = pd.read_csv(additive.CENTERED / tag / "calibration.csv").query("arm == 'additive|base'").iloc[0]
            v16 = json.loads((paths.V16_CONTROLS / tag / "s17" / "calibration.json").read_text())
            v16 = v16["calibration"]["additive_defense"]
            with self.subTest(origin=tag, step="centering"):
                self.assertAlmostEqual(a.league, ref["league_points100"], delta=1e-9)
                for p in additive.PARTS:
                    self.assertAlmostEqual(a.means["offense"][p], ref["player_means"][p], delta=1e-12)
                    self.assertAlmostEqual(a.means["defense"][p], v15["reference"]["player_means"][p], delta=1e-12)
            with self.subTest(origin=tag, step="calibrations"):
                self.assertAlmostEqual(a.offense_calibration["a"], cal.a, delta=1e-10)
                self.assertAlmostEqual(a.offense_calibration["b"], cal.b, delta=1e-10)
                self.assertAlmostEqual(a.defense_calibration["slope"], v15["calibration"]["slope"], delta=1e-12)
                self.assertAlmostEqual(a.blend["intercept"], v16["intercept"], delta=1e-12)
                self.assertAlmostEqual(a.blend["slope"], v16["slope"], delta=1e-12)
            with self.subTest(origin=tag, step="rows"):
                saved = legacy.controls(tag, 17)
                rows = saved.row.to_numpy()
                points = a.points(np.asarray(g["pids"][rows]), np.asarray(g["defense"][rows]))
                np.testing.assert_allclose(points, saved.additive_defense.to_numpy(), rtol=0, atol=1e-9)

    def test_order_and_neutral_defense(self):
        a = additive.Additive("2026q4")
        g = legacy.matchups()
        rows = np.arange(100)
        offense, defense = np.asarray(g["pids"][rows]), np.asarray(g["defense"][rows])
        np.testing.assert_allclose(a.points(offense[:, ::-1], defense[:, [2, 0, 4, 1, 3]]), a.points(offense, defense),
                                   rtol=0, atol=1e-10)
        # An all-unseen defense is the exposure-weighted average defense, i.e. the league-average defense.
        np.testing.assert_allclose(a.points(offense, np.full_like(defense, -1)), a.points(offense), rtol=0, atol=1e-12)


if __name__ == "__main__":
    unittest.main()
