"""Property-suite mechanics on synthetic roles and a stub predictor (no caches needed)."""
import unittest
from types import SimpleNamespace

import numpy as np
import pandas as pd
import torch

from lineups import properties


def table():
    """Ten players: 1-5 shooters with rising usage, 6-10 non-shooters; 1 and 6 are passers."""
    pids = np.arange(1, 11)
    return pd.DataFrame(dict(three_rate=[8, 6, 6, 5, 7, 0, 0, .5, .2, 0],
                             assist_rate=[12, 3, 2, 2, 2, 9, 1, 1, 1, 1],
                             usage=[.30, .18, .20, .22, .24, .29, .17, .21, .23, .25],
                             height=[75, 78, 79, 80, 77, 84, 83, 82, 85, 81],
                             block=np.linspace(0, 1, 10), drb=np.linspace(0, 1, 10)), index=pids)


def stub(value, spacing_sign):
    """Additive points; each player's rim make moves with the number of non-shooting teammates."""
    roles = table()

    def predict(offense, defense):
        offense = torch.as_tensor(np.asarray(offense))
        v = torch.as_tensor(value)[offense - 1]
        non = torch.as_tensor((roles.three_rate.to_numpy() < 1).astype(float))[offense - 1]
        rim = .6 + spacing_sign * .01 * (non.sum(1, keepdim=True) - non)
        make = torch.cat([rim[..., None], torch.full((*offense.shape, 5), .4, dtype=torch.float64)], -1)
        attempts = torch.ones_like(make)
        return SimpleNamespace(points100=v.sum(1), make=make, expected_attempts=attempts,
                               expected_makes=attempts * make, turnover=.02 * torch.ones_like(v),
                               rebound_log_prob=torch.full((len(v), 6), np.log(1 / 6)))
    return predict


class Properties(unittest.TestCase):
    def setUp(self):
        self.lineups = np.array([[1, 2, 3, 4, 5], [1, 2, 6, 7, 8]])

    def test_spacing_swap_uses_nearest_usage_non_shooter(self):
        cases = [c for c in properties.offense_cases(self.lineups, table()) if c[0] == "spacing"]
        kind, i, five, swapped, slot = cases[0]
        self.assertEqual(five[slot], 1)                 # top shooter
        self.assertEqual(swapped[slot], 6)              # non-shooter nearest usage .30 -> .29
        self.assertEqual(sorted(set(swapped) - set(five)), [6])

    def test_additive_model_has_no_synergy_and_is_order_free(self):
        predict = stub(np.arange(1., 11.), spacing_sign=-1)
        rows = pd.DataFrame(properties.run_offense(predict, self.lineups, table()))
        clone = rows[rows.property == "clone_synergy"]
        self.assertEqual(len(clone), 6)
        np.testing.assert_allclose(clone.violation, 0, atol=1e-12)   # additive: joint gain = sum of singles
        perm = properties.run_permutation(predict, self.lineups, self.lineups)
        self.assertTrue(all(r["violation"] < 1e-12 for r in perm))

    def test_synergy_layout(self):
        five = np.array([1, 2, 3, 4, 5])
        rows = properties.synergy_cases(five, [4, 3], [9, 8])
        np.testing.assert_array_equal(np.array(rows), [[1, 2, 3, 4, 5], [1, 2, 3, 4, 9], [1, 2, 3, 8, 5],
                                                       [1, 2, 3, 8, 9]])
        metric = np.array([[0., -1., -2., -2.5]])        # joint -2.5 against singles summing to -3
        np.testing.assert_allclose(properties.synergy(metric, 2), [[.5]])

    def test_spacing_direction(self):
        good = pd.DataFrame(properties.run_offense(stub(np.ones(10), -1), self.lineups, table()))
        bad = pd.DataFrame(properties.run_offense(stub(np.ones(10), +1), self.lineups, table()))
        self.assertTrue((good[good.property == "spacing_rim"].violation < 0).all())
        self.assertTrue((bad[bad.property == "spacing_rim"].violation > 0).all())


if __name__ == "__main__":
    unittest.main()
