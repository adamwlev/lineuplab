"""Trainer smoke tests on a small real prefix (needs the local store)."""
import unittest

import numpy as np
import torch

from lineups import legacy, paths
from lineups.train import FitConfig, Rows, game_batches, train


@unittest.skipUnless(paths.STORE.exists(), "local lineups store absent")
class TrainSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.features import Store
        cls.store = Store()
        cls.data = Rows(legacy.matchups(), cls.store)
        normalizer = cls.store.normalizer("2020q1", "final")
        cutoff = int(normalizer["cutoff_day"])
        prefix = cls.data.prefix(cutoff, 5 * 365)
        games = np.unique(cls.data.game[prefix])[-40:]
        cls.rows = prefix[np.isin(cls.data.game[prefix], games)]
        cls.normalizer, cls.env = normalizer, cls.store.env("2020q1", "final")
        cls.reference = cls.store.references["2020q1/final/s17"]

    def run_once(self):
        from lineups.model import EventModel
        torch.set_num_threads(1)
        model = EventModel.fresh(17)
        fit = train(model, self.data, self.rows, self.normalizer, self.env, self.reference, 17,
                    FitConfig(batch_rows=512), epochs=2, log=lambda m: None)
        return fit, model

    def test_training_is_deterministic_and_keeps_checkpoints(self):
        a, model_a = self.run_once()
        b, model_b = self.run_once()
        self.assertEqual([r["train"] for r in a["curve"]], [r["train"] for r in b["curve"]])
        self.assertEqual(sorted(a["checkpoints"]), [1, 2])
        for k, v in model_a.state_dict().items():
            self.assertTrue(torch.equal(v, model_b.state_dict()[k]), k)

    def test_constraint_coefficients_stay_in_range(self):
        _, model = self.run_once()
        for p in (model.backbone.k_supply, model.backbone.k_ft, model.backbone.k_load):
            self.assertTrue(((p >= 0) & (p <= 4)).all())

    def test_batches_keep_whole_games(self):
        for ix in game_batches(self.data.game, self.rows, 512, shuffle=True, seed=3):
            games = np.unique(self.data.game[ix])
            whole = np.isin(self.data.game[self.rows], games)
            self.assertEqual(whole.sum(), len(ix))


if __name__ == "__main__":
    unittest.main()
