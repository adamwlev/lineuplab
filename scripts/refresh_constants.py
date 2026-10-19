"""The band's constants from their producers' outputs (the refresh, 2026-10-16; reports/refresh_protocol_2026_10_16.md).

- tau2 per side and on the margin: scripts/band_in_support.py (tau.csv, the pooled rows);
- the cross-era variance per side: direction A's pooled excess cell MSE over the in-era baseline, per input rule
  (scripts/cross_era.py, A.pkl), "relative" being the era-relative (translated) rule;
- the cross-era correlation: each rule's within-quarter correlation as a share of the baseline's.

Under the main cache this reproduces lineups.band's constants (to their printed rounding). Run with LINEUPS_CACHE at
the clean root, it writes lineups.sources.SOURCES["refresh"]["band"]; under the main cache it only prints.

    LINEUPS_CACHE=<clean root> PYTHONPATH=.:scripts python -u scripts/refresh_constants.py
"""
import json

import numpy as np
import pandas as pd

import band_in_support
import cross_era
from lineups import paths
from lineups.sources import SOURCES

RULE = dict(relative="translated", as_was="as_was")


def constants():
    tau = pd.read_csv(band_in_support.OUT / "tau.csv").set_index("side")
    per, pooled, cells = cross_era.score(pd.read_pickle(cross_era.OUT / "A.pkl"))
    w = cells.possessions.to_numpy(float)
    mse = {m: float(w @ cells[f"err_{m}"] ** 2 / w.sum()) for m in cross_era.COLUMNS}
    return dict(
        tau2={side: float(tau.loc[side, "tau2"]) for side in ("offense", "defense", "margin")},
        cross_era_variance={k: mse[r] - mse["baseline"] for k, r in RULE.items()},
        cross_era_correlation={k: float(pooled.correlation[r] / pooled.correlation["baseline"]) for k, r in RULE.items()},
        sources=dict(tau=str(band_in_support.OUT / "tau.csv"), cross_era=str(cross_era.OUT / "A.pkl"), cache=str(paths.CACHE)))


def main():
    c = constants()
    print(json.dumps(c, indent=1))
    if not paths.CLEAN_ROOT:
        return
    out = SOURCES["refresh"]["band"]
    if out.exists():
        raise SystemExit(f"{out} exists; constants are not overwritten")
    out.write_text(json.dumps(c, indent=1))
    print("wrote", out)


if __name__ == "__main__":
    main()
