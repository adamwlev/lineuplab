"""The ported schedule builder reproduces the saved 2014-2026 quarter windows (needs local caches)."""
import unittest

import pandas as pd

from lineups import paths, schedule


class SeasonLabels(unittest.TestCase):
    def test_bubble_and_august(self):
        labels = schedule.season_labels(["2019-10-22", "2020-03-11", "2020-08-14", "2020-10-11", "2020-12-22",
                                         "2021-07-20", "2021-10-19"])
        self.assertEqual(labels.tolist(), [2020, 2020, 2020, 2020, 2021, 2021, 2022])


@unittest.skipUnless(schedule.POSSESSIONS.exists() and paths.SCHEDULE.exists(), "local caches absent")
class ScheduleParity(unittest.TestCase):
    def test_rebuilds_saved_schedule(self):
        saved = pd.read_csv(paths.SCHEDULE, parse_dates=["start", "stop"])
        rebuilt = schedule.build(int(saved.season.min()), int(saved.season.max()))
        cols = list(saved.columns)
        pd.testing.assert_frame_equal(rebuilt[cols].reset_index(drop=True), saved[cols].reset_index(drop=True),
                                      check_dtype=False)


if __name__ == "__main__":
    unittest.main()
