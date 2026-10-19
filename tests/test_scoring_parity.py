"""Rung 2: the new scorer reproduces the published v16 reference scorecard.

Needs the local v16 caches; skipped elsewhere. About 40 s per view.
Run: python -m unittest tests.test_scoring_parity
"""
import unittest

from lineups import legacy, paths
from lineups.evaluate import novel_offense, rolling_scorecard, summarize

PUBLISHED = {  # MODEL_SCORECARD.md, broad cohort, 44 quarters 2016-2026
    ("checkpoint_average", "all", "half"): dict(rmse=11.054459, r2=.162989, mae=8.306363, cells=8345),
    ("checkpoint_average", "all", "calibrated"): dict(r2=.161482),
    ("checkpoint_average", "all", "additive_defense"): dict(rmse=11.165936, r2=.146023),
    ("checkpoint_average", "novel", "half"): dict(rmse=12.056185, r2=.144502, cells=3489),
    ("checkpoint_average", "novel", "additive_defense"): dict(rmse=12.238726, r2=.118400),
    ("direct", "all", "half"): dict(rmse=11.054951, r2=.162915, mae=8.299892),
    ("direct", "all", "calibrated"): dict(rmse=11.061484, r2=.161925),
}


@unittest.skipUnless(paths.V16_RUN.exists() and paths.V16_CONTROLS.exists(), "local v16 caches absent")
class ScoringParity(unittest.TestCase):
    def test_reference_scorecard(self):
        g = legacy.matchups()
        for view in ("checkpoint_average", "direct"):
            records = rolling_scorecard(
                legacy.origins(), lambda o: legacy.row_frame(legacy.quarter_rows(o, g), g),
                lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, view),
                lambda o, s: legacy.controls(o.tag, s)[["row", "league", "additive_defense"]],
                legacy.SEEDS, novel_of=lambda o, f: novel_offense(f, legacy.day(o.start), g))
            table = summarize(records).set_index(["slice", "model"])
            for (v, slice_, model), expected in PUBLISHED.items():
                if v != view:
                    continue
                for key, value in expected.items():
                    with self.subTest(view=view, slice=slice_, model=model, metric=key):
                        self.assertAlmostEqual(table.loc[(slice_, model), key], value, places=6)


if __name__ == "__main__":
    unittest.main()
