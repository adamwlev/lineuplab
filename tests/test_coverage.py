"""Optional coverage defense: exact nesting at initialization and slot-order invariance (needs local caches)."""
import copy
import unittest

import numpy as np
import torch

from lineups import paths


@unittest.skipUnless(paths.STORE.exists() and (paths.STORE / "players.npz").exists() and paths.V16_RUN.exists(),
                     "local caches absent")
class CoverageDefense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.coherence import fixtures
        from lineups.features import Store
        from lineups.model import load_legacy
        cls.store, fx = Store(), fixtures()
        case = paths.V16_RUN / "origins" / "2026q4" / "J_POINT_BOTH" / "s17" / "final"
        cls.reference = load_legacy(torch.load(case / "fit.pt", map_location="cpu", weights_only=False)["state_dict"])
        names = ("legal_pure_centers", "jokic_westbrook", "small_guards", "highest_exposure_real_2026")
        cls.offense = np.array([fx[k]["pids"] for k in names])
        cls.defense = cls.offense[[1, 0, 3, 2]]
        cls.env = cls.store.env("2026q4", "final")

    def batch(self, offense, defense):
        from lineups.coherence import batch
        return batch(self.store, offense, defense, "2026q4")

    def with_coverage(self, seed=0):
        from lineups.model import Coverage
        model = copy.deepcopy(self.reference)
        torch.manual_seed(seed)
        model.coverage = Coverage(matched=True, help_term=True)
        return model.eval()

    def test_starts_exactly_at_the_reference(self):
        inputs = self.batch(self.offense, self.defense)
        with torch.no_grad():
            a = self.reference(inputs, self.env).points100
            b = self.with_coverage()(inputs, self.env).points100
        torch.testing.assert_close(a, b, rtol=0, atol=0)

    def test_slot_order_does_not_matter(self):
        model = self.with_coverage()
        with torch.no_grad():
            for p in model.coverage.parameters():
                p.add_(.3 * torch.randn_like(p))
            model.project()
            rng = np.random.default_rng(1)
            shuffle = lambda x: np.array([rng.permutation(r) for r in x])
            a = model(self.batch(self.offense, self.defense), self.env).points100
            b = model(self.batch(shuffle(self.offense), shuffle(self.defense)), self.env).points100
            self.assertGreater(float((a - self.reference(self.batch(self.offense, self.defense), self.env)
                                      .points100).abs().max()), .1)          # coverage is active
        torch.testing.assert_close(a, b, rtol=1e-5, atol=1e-4)


if __name__ == "__main__":
    unittest.main()


V14 = paths.CACHE / "joint_capability_2026_09_15_v14_prod" / "origins" / "2026q4" / "RB_RENEW_FAC" / "s17" / "final.pt"


@unittest.skipUnless(paths.STORE.exists() and (paths.STORE / "players.npz").exists() and V14.exists(),
                     "local caches absent")
class CapacityDefenseModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.coherence import fixtures
        from lineups.features import Store
        from lineups.model import EventModel
        cls.store, fx = Store(), fixtures()
        parent = torch.load(V14, map_location="cpu", weights_only=False)["state_dict"]
        cls.broadcast = EventModel.from_parent(parent, 17).eval()
        cls.capacity = EventModel.from_parent(parent, 17, defense="capacity").eval()
        cls.fx = fx
        cls.env = cls.store.env("2026q4", "final")

    def batch(self, offense, defense):
        from lineups.coherence import batch
        return batch(self.store, np.asarray(offense), np.asarray(defense), "2026q4")

    def test_starts_at_the_parent_like_the_reference(self):
        inputs = self.batch([self.fx["jokic_westbrook"]["pids"]], [self.fx["legal_pure_centers"]["pids"]])
        with torch.no_grad():
            torch.testing.assert_close(self.capacity(inputs, self.env).points100,
                                       self.broadcast(inputs, self.env).points100, rtol=0, atol=0)

    def perturbed(self):
        model = copy.deepcopy(self.capacity)
        torch.manual_seed(3)
        with torch.no_grad():
            for p in model.defense.parameters():
                p.add_(.3 * torch.randn_like(p))
        return model

    def test_slot_order_does_not_matter(self):
        model = self.perturbed()
        offense = np.array([self.fx[k]["pids"] for k in ("jokic_westbrook", "small_guards")])
        defense = np.array([self.fx[k]["pids"] for k in ("legal_pure_centers", "highest_exposure_real_2026")])
        rng = np.random.default_rng(2)
        shuffle = lambda x: np.array([rng.permutation(r) for r in x])
        with torch.no_grad():
            a = model(self.batch(offense, defense), self.env).points100
            b = model(self.batch(shuffle(offense), shuffle(defense)), self.env).points100
        torch.testing.assert_close(a, b, rtol=1e-5, atol=1e-4)

    def test_tied_unknown_defenders_do_not_depend_on_order(self):
        model = self.perturbed()
        unknown = [10**6 + 1, 10**6 + 2, 10**6 + 3]          # identical fallback states, different ids
        offense = [self.fx["jokic_westbrook"]["pids"]]
        defense = self.fx["small_guards"]["pids"][:2] + unknown
        with torch.no_grad():
            a = model(self.batch(offense, [defense]), self.env).points100
            b = model(self.batch(offense, [defense[::-1]]), self.env).points100
        torch.testing.assert_close(a, b, rtol=1e-5, atol=1e-4)

    def test_inside_reads_only_the_top_two(self):
        model = self.perturbed()
        gobert = self.fx["five_goberts"]["pids"][0]
        guards = self.fx["small_guards"]["pids"]
        two = self.batch([guards], [[gobert, gobert] + guards[:3]])
        five = self.batch([guards], [[gobert] * 5])
        with torch.no_grad():
            e2, r2 = model.defense(two)
            e5, r5 = model.defense(five)
        from lineups.model import INSIDE
        torch.testing.assert_close(e2[..., list(INSIDE)], e5[..., list(INSIDE)])
        torch.testing.assert_close(r2, r5)
