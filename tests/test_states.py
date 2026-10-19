"""Rung 5 step 2: the ported state sweep reproduces the saved v3 states bit for bit (about 50 s; needs caches)."""
import unittest

import numpy as np
import pandas as pd

from lineups import paths, states


@unittest.skipUnless(states.GAME_LINEUPS.exists() and states.GAME_PLAYERS.exists(), "local caches absent")
class StateSweepParity(unittest.TestCase):
    def test_sweep_matches_saved_states(self):
        g, gp = states.load_inputs()
        new = states.sweep(g, gp, pd.read_csv(paths.SCHEDULE, parse_dates=["start", "stop"]))
        with np.load(states.V3 / "player_game_states_v3.npz") as z:
            for key in z.files:
                if key == "origin_tags":
                    continue
                with self.subTest(key=key):
                    self.assertEqual(z[key].dtype, new[key].dtype)
                    np.testing.assert_array_equal(z[key], new[key])


if __name__ == "__main__":
    unittest.main()


V15 = paths.CACHE / "joint_capability_2026_09_17_v15_inputs"
V14_STATES = paths.CACHE / "joint_capability_2026_09_15_v14_states" / "rebound_states.npz"


@unittest.skipUnless(states.REBOUND_LABELS.exists() and V14_STATES.exists() and (V15 / "matchups.npz").exists(),
                     "local caches absent")
class ReboundAndDefenseParity(unittest.TestCase):
    def compare(self, saved, new):
        with np.load(saved) as z:
            for key in z.files:
                with self.subTest(key=key):
                    self.assertEqual(z[key].dtype, new[key].dtype)
                    np.testing.assert_array_equal(z[key], new[key])

    def test_rebound_states(self):
        with np.load(states.V3 / "player_game_states_v3.npz") as z:
            offense = {k: z[k] for k in z.files}
        with np.load(states.REBOUND_LABELS) as z:
            labels = {k: z[k] for k in z.files}
        schedule = pd.read_csv(paths.SCHEDULE, parse_dates=["start", "stop"])
        self.compare(V14_STATES, states.rebound_sweep(labels, offense, schedule))

    def test_defense_states(self):
        with np.load(V15 / "matchups.npz") as z:
            g = {k: z[k] for k in z.files}
        schedule = pd.read_csv(paths.SCHEDULE, parse_dates=["start", "stop"])
        self.compare(V15 / "defense_states.npz", states.defense_sweep(g, pd.read_pickle(states.GAME_PLAYERS), schedule))
