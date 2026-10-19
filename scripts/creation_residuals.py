"""Where does the weak-best-passer overprediction come from? (exploratory, post hoc to the confirmatory run)

The confirmatory run's secondary cohorts showed both models overpredict real
offenses whose best passer is below 5 assists per 100 (residual -2.3 +- 0.5,
half blend). This splits that residual into the blend's two halves
(calibrated reference and additive_defense) and grades it by best-passer
assist rate, against all rows. Rows: the 44 primary quarters, actual defenses,
possession-weighted, points per 100; season-level SEs.

    PYTHONPATH=.:scripts python -u scripts/creation_residuals.py
"""
import numpy as np
import pandas as pd

from capacity_score import cohorts, frames
from lineups import db, legacy
from lineups.features import Store

BINS = (0, 3, 4, 5, 6, 8, 10, 15, 100)


def main():
    g, store = legacy.matchups(), Store()
    rows = frames(lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"), g)
    flags = cohorts(rows, store, db.heights())
    from capacity_score import roles
    best = []
    for index, f in rows.groupby("origin_index", sort=False):
        off = f[[f"p{i}" for i in range(5)]].to_numpy()
        r = roles(store, int(index), np.unique(off))
        best.append(pd.Series(r["assist"].reindex(off.ravel()).to_numpy().reshape(off.shape).max(1), index=f.index))
    rows["best_passer"] = pd.concat(best)
    rows["actual"] = 100 * rows.points / rows.possessions
    rows["bin"] = pd.cut(rows.best_passer, BINS)
    out = []
    for name, sub in [("all rows", rows), ("weak best passer", rows[flags.weak_best_passer])] + \
            [(f"best passer {b}", rows[rows.bin == b]) for b in rows.bin.cat.categories]:
        rec = dict(slice=name, possessions=int(sub.possessions.sum()))
        for m in ("half", "calibrated", "additive_defense"):
            per = sub.assign(r=sub.actual - sub[m]).groupby("season").apply(
                lambda s: np.average(s.r, weights=s.possessions), include_groups=False)
            rec[m] = f"{np.average(sub.actual - sub[m], weights=sub.possessions):+.2f} ± {per.std(ddof=1) / np.sqrt(len(per)):.2f}"
        out.append(rec)
    print(pd.DataFrame(out).to_string(index=False))


if __name__ == "__main__":
    main()
