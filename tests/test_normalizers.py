"""Rung 5 step 5: ported normalizers and environment reproduce the saved store (needs local caches)."""
import unittest

import numpy as np

from lineups import legacy, paths, states


@unittest.skipUnless(paths.STORE.exists() and states.GAME_LINEUPS.exists() and states.REBOUND_LABELS.exists(),
                     "local caches absent")
class NormalizerParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.features import Store
        cls.store = Store()
        with np.load(states.GAME_LINEUPS) as z:
            cls.grouped = {k: z[k] for k in z.files}
        with np.load(states.V3 / "player_game_states_v3.npz") as z:
            cls.offense = {k: z[k] for k in ("game_id", "pid", "base", "x")}
        with np.load(paths.CACHE / "joint_capability_2026_09_15_v14_states" / "rebound_states.npz") as z:
            cls.rebound = {k: z[k] for k in ("game_id", "pid", "prob", "neff")}
        with np.load(states.REBOUND_LABELS) as z:
            cls.counts = z["counts"]
        cls.schedule = legacy.schedule()

    def cutoff(self, tag, phase):
        o = self.schedule.query("tag == @tag").iloc[0]
        if phase == "final":
            return legacy.day(o.start)
        return legacy.day(self.schedule[self.schedule.stop <= o.start].iloc[-1].start)

    def test_normalizers_and_environment(self):
        from lineups import normalizers
        for tag, phase in (("2015q1", "inner"), ("2020q1", "final"), ("2026q4", "final")):
            cutoff = self.cutoff(tag, phase)
            saved = self.store.normalizer(tag, phase)
            new = normalizers.lineup_normalizers(self.grouped, self.offense, self.rebound, cutoff)
            new |= normalizers.matchup_normalizers(legacy.matchups(), self.store, cutoff)
            for key, value in saved.items():
                with self.subTest(origin=tag, phase=phase, key=key):
                    np.testing.assert_allclose(new[key], value, rtol=0, atol=1e-9)
            env, saved_env = normalizers.environment(self.grouped, self.counts, cutoff), self.store.env(tag, phase)
            for key in ("budget", "eta", "non_rebound"):
                with self.subTest(origin=tag, phase=phase, key=key):
                    self.assertAlmostEqual(env[key], saved_env[key], places=12)


if __name__ == "__main__":
    unittest.main()


V14 = paths.CACHE / "joint_capability_2026_09_15_v14_prod" / "origins" / "2015q1" / "RB_RENEW_FAC" / "s17" / "inner.pt"


@unittest.skipUnless(paths.STORE.exists() and V14.exists(), "local caches absent")
class ReferenceParity(unittest.TestCase):
    def test_references_from_the_zero_head_start(self):
        import torch
        from lineups.features import Store
        from lineups.model import EventModel
        from lineups.train import FitConfig, Rows, references
        store = Store()
        data = Rows(legacy.matchups(), store)
        schedule = legacy.schedule()
        origin = schedule.query("tag == '2015q1'").iloc[0]
        inner = schedule[schedule.stop <= origin.start].iloc[-1]
        rows = data.prefix(legacy.day(inner.start), FitConfig().lookback_days)
        parent = torch.load(V14, map_location="cpu", weights_only=False)["state_dict"]
        new = references(EventModel.from_parent(parent, 17), data, rows, store.normalizer("2015q1", "inner"),
                         store.env("2015q1", "inner"))
        saved = store.references["2015q1/inner/s17"]
        for f in ("counts", "location", "conversion", "recovery"):
            self.assertAlmostEqual(new["reference"]["event"][f], saved["reference"]["event"][f], places=10)
            self.assertEqual(new["exposure"]["event"][f], saved["exposure"]["event"][f])
        self.assertAlmostEqual(new["reference"]["point"], saved["reference"]["point"], places=7)
