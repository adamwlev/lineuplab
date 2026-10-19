"""Compare capability-library snapshots of two library directories (name-matching fix, 2026-10-14).

    PYTHONPATH=. python scripts/library_parity.py ORIGINAL REBUILT [--dates N]

For every bank/family chain and each of the first N snapshot dates present in REBUILT, every array in
state.npz and joint_draws.npz must be equal. Prints the worst absolute difference per chain.
"""
import argparse
from pathlib import Path

import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument("original", type=Path)
    p.add_argument("rebuilt", type=Path)
    p.add_argument("--dates", type=int, default=3)
    a = p.parse_args()
    ok = True
    for chain in sorted((a.rebuilt / "chains").glob("*/*")):
        dates = sorted(d.name for d in (chain / "snapshots").iterdir() if (d / "complete.json").exists())[:a.dates]
        worst, exact = 0., True
        for d in dates:
            for f in ("state.npz", "joint_draws.npz"):
                x = np.load(a.original / "chains" / chain.parent.name / chain.name / "snapshots" / d / f)
                y = np.load(chain / "snapshots" / d / f)
                for k in x.files:
                    if not np.array_equal(x[k], y[k]):
                        exact = False
                        if x[k].dtype.kind in "fi":
                            worst = max(worst, float(np.abs(x[k].astype(float) - y[k].astype(float)).max()))
        ok &= exact
        print(f"{chain.parent.name}/{chain.name}: {len(dates)} snapshots {dates[:1]}..{dates[-1:]} "
              f"{'exact' if exact else f'DIFFER (worst {worst:.3g})'}")
    print("ALL EXACT" if ok else "NOT EXACT")


if __name__ == "__main__":
    main()
