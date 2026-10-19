"""The coherence tools reproduce saved v16 fixture matchups (needs local caches)."""
import unittest

import torch

from lineups import paths


@unittest.skipUnless(paths.STORE.exists() and paths.V16_RUN.exists(), "local caches absent")
class CoherenceParity(unittest.TestCase):
    def test_centers_against_jokic_westbrook(self):
        from lineups.coherence import fixtures, matchup
        from lineups.features import Store
        from lineups.model import load_legacy
        store, fx = Store(), fixtures()
        case = paths.V16_RUN / "origins" / "2026q4" / "J_POINT_BOTH" / "s17" / "final"
        fit = torch.load(case / "fit.pt", map_location="cpu", weights_only=False)
        direct = load_legacy(fit["state_dict"])
        result = matchup(direct, store, fx["legal_pure_centers"]["pids"], fx["jokic_westbrook"]["pids"], "2026q4")
        self.assertAlmostEqual(result["a_offense"], 123.873560, places=4)   # saved v16 follow-up, seed 17
        self.assertAlmostEqual(result["b_offense"], 116.173684, places=4)
        states = [torch.load(case / f"checkpoint_{e:03d}.pt", map_location="cpu", weights_only=False)["state_dict"]
                  for e in fit["checkpoint_epochs"]]
        mixture = [load_legacy(s) for s in states]
        result = matchup(mixture, store, fx["legal_pure_centers"]["pids"], fx["jokic_westbrook"]["pids"], "2026q4")
        self.assertAlmostEqual(result["a_offense"], 121.215703, places=4)
        self.assertAlmostEqual(result["b_offense"], 115.624016, places=4)


if __name__ == "__main__":
    unittest.main()
