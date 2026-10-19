"""Prototype of the assumption-based band for hypothetical matchups (exploratory).

For each matchup at 2026q4: the native margin from the reference (three-seed
checkpoint mixture) and from the capacity-law assumption model (seed-17
checkpoint mixture from the latest capacity screen), their spread, and the
out-of-support reasons from lineups.support. Native points per 100, before
calibration. The spread is assumption-based: both models fit observed lineups
about equally well, so their disagreement is not estimated from data.

    PYTHONPATH=. python -u scripts/assumption_band.py
"""
import pandas as pd
import torch

from capacity_screen import OUT as CAPACITY, V14
from coverage_screen import SEED
from lineups.coherence import checkpoint_models, fixtures, matchup
from lineups.features import Store
from lineups.model import EventModel
from lineups.support import Support

ORIGIN = "2026q4"
PAIRS = (("legal_pure_centers", "jokic_westbrook"), ("legal_pure_centers", "jokic_korver"),
         ("five_goberts", "jokic_westbrook"), ("five_jokics", "jokic_westbrook"), ("limited_centers", "jokic_westbrook"),
         ("small_guards", "jokic_westbrook"), ("highest_exposure_real_2026", "jokic_westbrook"),
         ("rebound_same_four_Rudy_Gobert", "highest_exposure_real_2026"))


def capacity_models(tag=ORIGIN):
    saved = torch.load(CAPACITY / f"{tag}.pt", map_location="cpu", weights_only=False)
    parent = torch.load(V14 / "origins" / tag / "RB_RENEW_FAC" / f"s{SEED}" / "final.pt", map_location="cpu",
                        weights_only=False)["state_dict"]
    models = []
    for state in saved["checkpoints"]:
        m = EventModel.from_parent(parent, SEED, defense="capacity")
        m.load_state_dict(state)
        models.append(m.eval())
    return models


def main():
    store, fx = Store(), fixtures()
    support = Support(store, ORIGIN)
    families = dict(reference=checkpoint_models(ORIGIN), capacity=capacity_models())
    rows = []
    for a, b in PAIRS:
        rec = dict(a=a, b=b)
        for name, models in families.items():
            rec[name] = matchup(models, store, fx[a]["pids"], fx[b]["pids"], ORIGIN)["margin"]
        rec["low"], rec["high"] = min(rec["reference"], rec["capacity"]), max(rec["reference"], rec["capacity"])
        reasons = support.describe(fx[a]["pids"], fx[b]["pids"])["reasons"]
        reasons += [f"opponent: {r}" for r in support.describe(fx[b]["pids"], fx[a]["pids"])["reasons"]
                    if not r.startswith("defense")]
        rec["reasons"] = "; ".join(reasons) or "within observed support"
        rows.append(rec)
    with pd.option_context("display.width", 250, "display.max_colwidth", 200, "display.float_format", "{:+.1f}".format):
        print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
