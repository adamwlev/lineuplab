"""Post hoc: the neural model alone (calibrated) vs the half blend, reference and capacity (exploratory).

Prompted by Adam (2026-10-12): pillar-2 fixes are easier through the neural model
alone, and the additive half need not be permanent. Primary-benchmark
population (44 quarters, broad offense-five cells), seed-mean checkpoint
average, prior-only calibration. Per-season differences, raw and centered r^2
(centered removes each forecast's possession-weighted mean error per quarter).

    PYTHONPATH=.:scripts python -u scripts/nn_alone_check.py
"""
import numpy as np
import pandas as pd

from capacity_score import capacity_native, frames
from lineups import evaluate, legacy


def quarter_metrics(rows, label):
    out = []
    for (tag, season), f in rows.groupby(["origin", "season"], sort=False):
        c = evaluate.cells(f, ["half", "calibrated", "additive_defense"])
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        w, y = c.possessions.to_numpy(float), c.actual.to_numpy(float)
        sst = w @ (y - np.average(y, weights=w)) ** 2
        for m in ("half", "calibrated", "additive_defense"):
            e = y - c[m].to_numpy(float)
            out.append(dict(origin=tag, season=season, model=f"{label}_{m}", sse=w @ e ** 2,
                            sse_c=w @ (e - np.average(e, weights=w)) ** 2, sst=sst,
                            **evaluate.sufficient(c.actual, c[m], c.possessions)))
    return out


def main():
    g = legacy.matchups()
    rows = quarter_metrics(frames(lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"), g), "R")
    rows += quarter_metrics(frames(capacity_native("checkpoint_average"), g), "C")
    q = pd.DataFrame(rows)
    pooled = {m: evaluate.metrics(evaluate.pooled(f))["r2"] for m, f in q.groupby("model")}
    print("pooled r2:", {k: round(v, 5) for k, v in sorted(pooled.items())})
    q["r2"], q["r2_c"] = 1 - q.sse / q.sst, 1 - q.sse_c / q.sst
    wide = q.pivot_table(index=["origin", "season"], columns="model", values=["r2", "r2_c"])
    pairs = [("R_calibrated", "R_half"), ("C_calibrated", "R_half"), ("C_calibrated", "R_calibrated"),
             ("C_half", "R_half"), ("R_calibrated", "R_additive_defense"), ("C_calibrated", "R_additive_defense")]
    for kind in ("r2", "r2_c"):
        print(f"\n== per-quarter {kind}")
        for a, b in pairs:
            d = wide[kind][a] - wide[kind][b]
            s = d.groupby(level="season").mean()
            o1 = d[[t.endswith("q1") for t in d.index.get_level_values(0)]]
            print(f"{a} - {b}: quarters mean {d.mean():+.4f} (sd {d.std():.4f}, + {(d > 0).sum()}/44); "
                  f"seasons + {(s > 0).sum()}/11, se {s.std(ddof=1) / np.sqrt(11):.4f}; "
                  f"opening quarters mean {o1.mean():+.4f} sd {o1.std():.4f} + {(o1 > 0).sum()}/11")


if __name__ == "__main__":
    main()
