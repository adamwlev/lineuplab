"""lineups.history under the main cache serves the saved v16 reference and its league level; the fixture
registry is the same at every root."""
import json
import os
import subprocess
import sys
import unittest

import numpy as np

from lineups import coherence, history, legacy, paths


@unittest.skipUnless((paths.V16_RUN / "origins").exists() and paths.V16_CONTROLS.exists(), "v16 run absent")
class MainCacheHistory(unittest.TestCase):
    def test_world(self):
        self.assertFalse(history.CLEAN)

    def test_native_is_the_saved_reference(self):
        for view in ("direct", "checkpoint_average"):
            ids, p = history.native("2020q1", 17, view)
            ids0, p0 = legacy.native("2020q1", "J_POINT_BOTH", 17, view)
            np.testing.assert_array_equal(ids, ids0)
            np.testing.assert_array_equal(p, p0)

    def test_league_is_the_saved_controls_league(self):
        g = legacy.matchups()
        for o in legacy.origins().iloc[[0, 21, 47]].itertuples():
            saved = legacy.controls(o.tag, 17).league.to_numpy()
            self.assertAlmostEqual(history.league_at(g, legacy.day(o.start)), float(saved[0]), places=9)
            self.assertEqual(np.ptp(saved), 0.)


OLD_EXPORT = paths.ROOT / "experiments" / "cache" / "release_export_2026_10_12"


@unittest.skipUnless(paths.FIXTURES.exists() and (paths.CLEAN / "release_export").exists() and OLD_EXPORT.exists(),
                     "fixture registry or a release export absent")
class Fixtures(unittest.TestCase):
    def test_the_clean_root_reads_the_main_registry(self):
        # the registry is a definition: the same named lineups at either root (the refresh's modules stopped at
        # 2026q4 without it, 2026-10-18), and each pid names the same player in the clean release as in the old
        # one (the registry's own labels differ only in spelling: "Nikola Jokic", "Marcus Morris Sr.")
        code = ("import json; from lineups import coherence, paths; "
                "print(paths.CLEAN_ROOT, json.dumps(coherence.fixtures(), sort_keys=True))")
        out = subprocess.run([sys.executable, "-c", code], env=os.environ | dict(LINEUPS_CACHE=str(paths.CLEAN)),
                             capture_output=True, text=True, cwd=paths.ROOT, check=True).stdout
        world, registry = out.split(" ", 1)
        self.assertEqual(world, "True")
        self.assertEqual(json.loads(registry), coherence.fixtures())
        names = {k: json.loads((root / "meta.json").read_text())["names"]
                 for k, root in (("clean", paths.CLEAN / "release_export"), ("old", OLD_EXPORT))}
        for v in coherence.fixtures().values():
            self.assertEqual([names["clean"][str(p)] for p in v["pids"]], [names["old"][str(p)] for p in v["pids"]])


if __name__ == "__main__":
    unittest.main()
