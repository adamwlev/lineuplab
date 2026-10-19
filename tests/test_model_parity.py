"""Rung 1: the flat EventModel reproduces the pre-refactor reference exactly.

Run: python -m unittest tests.test_model_parity
"""
from pathlib import Path
import unittest

import numpy as np
import torch

from lineups.model import average_ledgers, load_legacy

FIXTURE = Path(__file__).parent / "fixtures" / "reference_2020q1_s17"
KEYS = ("points100", "player_points", "fga", "fta", "turnover", "ft_make", "expected_attempts",
        "expected_makes", "usage_budget", "orb", "player_orb", "live", "initial_usage", "renewed_usage",
        "rebound_log_prob")


def load_golden():
    z = dict(np.load(FIXTURE.with_suffix(".npz")))
    states = torch.load(FIXTURE.with_suffix(".pt"), map_location="cpu", weights_only=False)
    batch = {k[len("input_"):]: torch.as_tensor(v) for k, v in z.items() if k.startswith("input_")}
    env = dict(budget=float(z["env_budget"]), eta=float(z["env_eta"]), non_rebound=float(z["env_non_rebound"]))
    return z, states, batch, env


def predict(state, batch, env):
    with torch.no_grad():
        return load_legacy(state)(batch, env)


class ModelParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.z, cls.states, cls.batch, cls.env = load_golden()
        cls.final = predict(cls.states["final"], cls.batch, cls.env)
        cls.mixture = average_ledgers([predict(s, cls.batch, cls.env) for s in cls.states["checkpoints"]])

    def close(self, new, expected):
        np.testing.assert_allclose(new, expected, rtol=1e-6, atol=1e-9)

    def test_final_fit_matches_old_model(self):
        for key in KEYS:
            with self.subTest(key=key):
                self.close(getattr(self.final, key).numpy(), self.z["old_" + key])

    def test_checkpoint_mixture_matches_old_and_saved_production(self):
        for key in KEYS:
            with self.subTest(key=key):
                new = getattr(self.mixture, key).numpy()
                self.close(new, self.z["old_avg_" + key])
                self.close(new, self.z["saved_checkpoint_average_" + key])

    def test_final_fit_matches_saved_primary(self):
        for key in KEYS:
            with self.subTest(key=key):
                self.close(getattr(self.final, key).numpy(), self.z["saved_primary_" + key])

    def test_ledger_conserves_opportunities(self):
        p = self.final
        total = p.fga.sum(1) + .44 * p.fta.sum(1) + p.turnover.sum(1)
        torch.testing.assert_close(total, p.usage_budget, rtol=0, atol=3e-6)
        self.assertTrue(torch.isfinite(p.points100).all())

    def test_slot_order_does_not_matter(self):
        model = load_legacy(self.states["final"])
        perm = torch.tensor([3, 0, 4, 1, 2])
        shuffled = {k: (v[:, perm] if v.ndim >= 2 and v.shape[1] == 5 else v) for k, v in self.batch.items()}
        with torch.no_grad():
            b = model(shuffled, self.env)
        torch.testing.assert_close(self.final.points100, b.points100, rtol=1e-5, atol=1e-5)  # float32 sum order
        torch.testing.assert_close(self.final.fga[:, perm], b.fga, rtol=1e-5, atol=1e-6)


if __name__ == "__main__":
    unittest.main()
