"""PairInteractions and the nonlinearity reward (reports/nonlinearity_screen_protocol_2026_10_13.md)."""
import types
import unittest

import numpy as np
import torch

from lineups.model import PairInteractions, load_legacy
from lineups.train import second_difference
from tests.test_model_parity import load_golden


def with_heights(batch, seed=0):
    g = torch.Generator().manual_seed(seed)
    out = dict(batch)
    out["offense_height"] = torch.randn(len(batch["msg"]), 5, generator=g)
    out["defense_height"] = torch.randn(len(batch["msg"]), 5, generator=g)
    return out


class Pairs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.z, cls.states, batch, cls.env = load_golden()
        cls.batch = with_heights(batch)
        cls.model = load_legacy(cls.states["final"]).eval()

    def test_zero_start_keeps_the_function(self):
        with torch.no_grad():
            before = self.model(self.batch, self.env).points100
            self.model.pairs = PairInteractions()
            after = self.model(self.batch, self.env).points100
            self.model.pairs = None
        torch.testing.assert_close(before, after, rtol=0, atol=0)

    def test_order_free_and_symmetric_on_defense(self):
        torch.manual_seed(3)
        pairs = PairInteractions()
        with torch.no_grad():
            for layer in (pairs.u, pairs.p):
                layer.weight.normal_(0, .3)
            perm = torch.tensor([3, 0, 4, 1, 2])
            shuffled = {k: (v[:, perm] if v.ndim >= 2 and v.shape[1] == 5 else v) for k, v in self.batch.items()}
            off, de = pairs(self.batch)
            off_s, de_s = pairs(shuffled)
        torch.testing.assert_close(off[:, perm], off_s, rtol=1e-5, atol=1e-6)
        torch.testing.assert_close(de, de_s, rtol=1e-5, atol=1e-6)
        self.assertGreater(float(off.abs().mean()), 1e-3)

    def test_held_range_is_tracked_in_training_and_clamps_forecasts(self):
        torch.manual_seed(5)
        held, free = PairInteractions(hold="inputs"), PairInteractions()
        free.load_state_dict({k: v for k, v in held.state_dict().items() if "range" not in k and k != "seen"})
        with torch.no_grad():
            for m in (held, free):
                m.u.weight.copy_(torch.full_like(m.u.weight, .2))
                m.p.weight.copy_(torch.full_like(m.p.weight, .2))
            held.train()
            held(self.batch)
            self.assertTrue(bool(held.seen))
            self.assertTrue((held.offense_range[1] >= held.offense_range[0]).all())
            held.eval()
            free.eval()
            off_h, de_h = held(self.batch)
            off_f, de_f = free(self.batch)
            # on the rows that set the range almost nothing is clamped
            self.assertLess(float((off_h - off_f).abs().mean()), 1e-2)
            held.offense_range.copy_(torch.stack([torch.full((60,), -1e-3), torch.full((60,), 1e-3)]))
            held.defense_range.copy_(torch.stack([torch.full((60,), -1e-3), torch.full((60,), 1e-3)]))
            off_c, de_c = held(self.batch)
            self.assertLess(float(off_c.abs().max()), float(off_f.abs().max()))
            self.assertLess(float(de_c.abs().max()), float(de_f.abs().max()))

    def test_output_hold_bounds_players_and_lineups(self):
        torch.manual_seed(7)
        held, free = PairInteractions(hold="outputs"), PairInteractions()
        free.load_state_dict({k: v for k, v in held.state_dict().items() if "bounds" not in k and k != "measured"})
        with torch.no_grad():
            for m in (held, free):
                m.u.weight.copy_(torch.full_like(m.u.weight, .2))
                m.p.weight.copy_(torch.full_like(m.p.weight, .2))
            held.eval()
            free.eval()
            off_f, de_f = free(self.batch)
            off_h, de_h = held(self.batch)          # not yet measured: unclamped
            torch.testing.assert_close(off_h, off_f, rtol=0, atol=0)
            held.bound_outputs(off_f, de_f[:, 0])
            off_h, de_h = held(self.batch)
            # on the rows that set the range almost nothing moves
            self.assertLess(float((off_h - off_f).abs().mean()), 1e-2)
            tight = torch.stack([torch.full((15,), -1e-3), torch.full((15,), 1e-3)])
            for name in ("player_bounds", "lineup_bounds", "defense_bounds"):
                getattr(held, name).copy_(tight)
            off_c, de_c = held(self.batch)
            self.assertLessEqual(float(off_c.sum(1).abs().max()), 1e-3 + 1e-6)
            self.assertLessEqual(float(off_c.abs().max()), 1e-3 + 1e-6)
            self.assertLessEqual(float(de_c.abs().max()), 1e-3 + 1e-6)
            # scaling keeps each player's share and order does not matter
            perm = torch.tensor([3, 0, 4, 1, 2])
            shuffled = {k: (v[:, perm] if v.ndim >= 2 and v.shape[1] == 5 else v) for k, v in self.batch.items()}
            torch.testing.assert_close(held(shuffled)[0], off_c[:, perm], rtol=1e-5, atol=1e-7)

    def test_joint_hold_keeps_lineups_inside_the_ellipsoid(self):
        torch.manual_seed(9)
        held, free = PairInteractions(hold="joint"), PairInteractions()
        free.load_state_dict({k: v for k, v in held.state_dict().items() if k in free.state_dict()})
        with torch.no_grad():
            for m in (held, free):
                m.u.weight.copy_(torch.full_like(m.u.weight, .2))
                m.p.weight.copy_(torch.full_like(m.p.weight, .2))
            held.eval()
            free.eval()
            off_f, de_f = free(self.batch)
            held.bound_outputs(off_f, de_f[:, 0])
            self.assertGreater(float(held.lineup_radius), 0)
            off_h, de_h = held(self.batch)
            # the rows that set the range: almost nothing moves
            self.assertLess(float((off_h - off_f).abs().mean()), 1e-2)
            distance = lambda t, m: ((t @ m) * t).sum(-1).sqrt()
            # a lineup pushed far out is scaled back onto the ellipsoid, direction kept
            big = 50 * off_f[:4]
            out, _ = held.held_outputs(big, de_f[:4, 0] * 50)
            d = distance(out.sum(1), held.lineup_metric)
            self.assertLessEqual(float(d.max()), float(held.lineup_radius) * (1 + 1e-4))
            channel, _ = held.channel_holds(big, de_f[:4, 0])
            for b in range(len(big)):           # one common scale per lineup, at most 1
                ok = channel[b].abs() > 1e-6
                ratio = out[b][ok] / channel[b][ok]
                self.assertLess(float(ratio.max() - ratio.min()), 1e-4)
                self.assertLessEqual(float(ratio.max()), 1 + 1e-6)
            # zero interaction is never moved
            zero = torch.zeros_like(off_f[:2])
            torch.testing.assert_close(held.held_outputs(zero, torch.zeros_like(de_f[:2, 0]))[0], zero)

    def test_centered_module_is_a_pure_interaction_and_starts_at_zero(self):
        torch.manual_seed(11)
        pure = PairInteractions(centered=True)
        with torch.no_grad():
            before = self.model(self.batch, self.env).points100
            self.model.pairs = pure
            self.model.train()
            after = self.model(self.batch, self.env).points100      # U, P zero: still the parent's function
            self.model.eval()
            self.model.pairs = None
        torch.testing.assert_close(before, after, rtol=0, atol=1e-5)
        with torch.no_grad():
            for layer in (pure.u, pure.p):
                layer.weight.normal_(0, .3)
            pure.train()
            pure(self.batch)                                       # first batch sets the running centers
            self.assertTrue(bool(pure.centers_seen))
            pure.eval()
            s = torch.cat([self.batch["msg"], self.batch["rb_input"][..., -2:], self.batch["offense_height"][..., None]], -1)
            g = pure.center(pure.features(pure.offense_map, s), "offense")
            torch.testing.assert_close(g.reshape(-1, g.shape[-1]).mean(0), torch.zeros(g.shape[-1]), rtol=0, atol=1e-5)
            # order still does not matter
            perm = torch.tensor([3, 0, 4, 1, 2])
            shuffled = {k: (v[:, perm] if v.ndim >= 2 and v.shape[1] == 5 else v) for k, v in self.batch.items()}
            off, de = pure(self.batch)
            off_s, de_s = pure(shuffled)
        torch.testing.assert_close(off[:, perm], off_s, rtol=1e-5, atol=1e-6)
        torch.testing.assert_close(de, de_s, rtol=1e-5, atol=1e-6)

    def test_parameter_groups_cover_every_parameter_once(self):
        self.model.pairs = PairInteractions()
        try:
            groups = self.model.parameter_groups(1e-3, 1e-4, 5., 0.)
            ids = [id(p) for g in groups for p in g["params"]]
            self.assertEqual(sorted(ids), sorted(id(p) for p in self.model.parameters()))
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(groups[1]["lr"], 5e-3)
            self.assertEqual(groups[1]["weight_decay"], 0.)
        finally:
            self.model.pairs = None


class SecondDifference(unittest.TestCase):
    def batch(self, n=40):
        g = torch.Generator().manual_seed(1)
        return dict(msg=torch.randn(n, 5, 3, generator=g), defense=torch.randn(n, 5, 2, generator=g))

    def check(self, f, expect_zero):
        x = self.batch()
        model = lambda inputs, env: types.SimpleNamespace(points100=f(inputs))
        rng = np.random.default_rng(0)
        m = 30
        pick = rng.choice(40, m, replace=False)
        i = rng.integers(0, 5, m)
        j = (i + rng.integers(1, 5, m)) % 5
        donors = tuple((rng.integers(0, 40, m), rng.integers(0, 5, m)) for _ in range(2))
        side = rng.random(m) < .5
        d = second_difference(model, x, None, pick, side, (i, j), donors, f(x)[torch.as_tensor(pick)])
        if expect_zero:
            torch.testing.assert_close(d, torch.zeros_like(d), rtol=0, atol=1e-5)
        else:
            self.assertGreater(float(d.abs().max()), 1e-2)

    def test_zero_for_a_model_that_adds_up_players(self):
        self.check(lambda b: b["msg"].sum((1, 2)) - 2 * b["defense"][..., 0].sum(1), True)

    def test_nonzero_with_an_interaction(self):
        self.check(lambda b: b["msg"][..., 0].sum(1) ** 2 + b["defense"][..., 1].sum(1) ** 2, False)


if __name__ == "__main__":
    unittest.main()
