"""Two-phase fit: phase B starts exactly at the phase-A offense function (needs local caches)."""
import unittest

import numpy as np
import torch

from lineups import paths


@unittest.skipUnless(paths.STORE.exists() and (paths.STORE / "players.npz").exists() and paths.V16_RUN.exists(),
                     "local caches absent")
class TwoPhase(unittest.TestCase):
    def test_phase_b_starts_at_phase_a(self):
        from lineups.coherence import batch, fixtures
        from lineups.features import Store
        from lineups.model import EventModel
        store, fx = Store(), fixtures()
        inputs = batch(store, np.array([fx["jokic_westbrook"]["pids"]]), np.array([fx["legal_pure_centers"]["pids"]]),
                       "2026q4")
        env = store.env("2026q4", "final")
        offense = EventModel.offense_only(17)
        torch.manual_seed(5)
        with torch.no_grad():
            for p in list(offense.backbone.parameters()) + list(offense.rebound.parameters()):
                p.add_(.05 * torch.randn_like(p))
            offense.parent.load_state_dict(offense.backbone.state_dict())
            a = offense.eval()(inputs, env).points100
            for defense in ("broadcast", "capacity"):
                b = EventModel.from_offense(offense, 17, defense).eval()(inputs, env).points100
                torch.testing.assert_close(a, b, rtol=0, atol=0)
        self.assertFalse(any(p.requires_grad for p in offense.defense.parameters()))


@unittest.skipUnless(paths.STORE.exists() and paths.V16_RUN.exists(), "local caches absent")
class CreationHead(unittest.TestCase):
    def test_zero_start_and_slot_order(self):
        import copy
        from lineups.coherence import batch, fixtures
        from lineups.features import Store
        from lineups.model import Creation, load_legacy
        store, fx = Store(), fixtures()
        case = paths.V16_RUN / "origins" / "2026q4" / "J_POINT_BOTH" / "s17" / "final"
        reference = load_legacy(torch.load(case / "fit.pt", map_location="cpu", weights_only=False)["state_dict"])
        model = copy.deepcopy(reference)
        model.creation = Creation()
        env = store.env("2026q4", "final")
        offense = np.array([fx[k]["pids"] for k in ("jokic_westbrook", "five_goberts", "small_guards")])
        defense = offense[[1, 2, 0]]
        with torch.no_grad():
            torch.testing.assert_close(model(batch(store, offense, defense, "2026q4"), env).points100,
                                       reference(batch(store, offense, defense, "2026q4"), env).points100,
                                       rtol=0, atol=0)
            for p in model.creation.parameters():
                p.add_(.3 * torch.randn_like(p))
            rng = np.random.default_rng(4)
            shuffle = lambda x: np.array([rng.permutation(r) for r in x])
            a = model(batch(store, offense, defense, "2026q4"), env).points100
            b = model(batch(store, shuffle(offense), shuffle(defense), "2026q4"), env).points100
        torch.testing.assert_close(a, b, rtol=1e-5, atol=1e-4)


if __name__ == "__main__":
    unittest.main()
