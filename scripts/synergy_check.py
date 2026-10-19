"""Does the network's non-additive part predict outcomes? (exploratory, 2026-10-12)

For each benchmark quarter (2016-2026), the calibrated network's row forecasts f
(R, three-seed mean; saved by scripts/ensemble_check.py) are projected onto the
most flexible model that is additive across players: one free value per
offensive player and one per defensive player in that quarter,

    f(row) ~ c + sum_{attackers} alpha_j + sum_{defenders} beta_k,

by possession-weighted least squares on the forecasts themselves (no outcomes
are used). The projection a is the best additive approximation of the network.
The remainder i = f - a is whatever the network predicts that no sum of
per-player values can: teammate interactions, offense-defense interactions and
the one-ball accounting.

Then, on broad offense-five cells (at least 50 possessions), within quarter:
- centered r² of f against a: what the non-additive part adds to accuracy;
- a regression of the actual outcome on a and i: whether i carries signal
  (coefficient > 0) and how much of it is real (a coefficient near 1 means its
  full size is borne out);
- the SD of i across cells: how large the network's interactions are.

Season-level SEs, 11 seasons. Ties in the projection (players who always appear
together) are absorbed by the minimum-norm solution and do not change a.

    PYTHONPATH=. python -u scripts/synergy_check.py
"""
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import lsqr

from lineups import evaluate, paths
from lineups.evaluate import FIVE
from lineups.legacy import DEFENSE

ROWS = paths.CACHE / "ensemble_check_2026_10_12" / "benchmark.pkl"
OUT = paths.CACHE / "synergy_check_2026_10_12"


def additive_projection(f):
    """Possession-weighted least-squares fit of f.R on intercept + attacker and defender dummies."""
    off = f[FIVE].to_numpy()
    de = f[DEFENSE].to_numpy()
    ou, oi = np.unique(off, return_inverse=True)
    du, di = np.unique(de, return_inverse=True)
    n = len(f)
    rows = np.repeat(np.arange(n), 5)
    X = sparse.hstack([sparse.csr_matrix(np.ones((n, 1))),
                       sparse.csr_matrix((np.ones(5 * n), (rows, oi.ravel())), shape=(n, len(ou))),
                       sparse.csr_matrix((np.ones(5 * n), (rows, di.ravel())), shape=(n, len(du)))]).tocsr()
    w = np.sqrt(f.possessions.to_numpy(float))
    target = f.R.to_numpy(float)
    sol = lsqr(sparse.diags(w) @ X, w * target, atol=1e-12, btol=1e-12, iter_lim=20000)[0]
    return X @ sol


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f = pd.read_pickle(ROWS)
    f[FIVE] = np.sort(f[FIVE].to_numpy(), 1)
    recs, cells = [], []
    for (tag, season), q in f.groupby(["origin", "season"], sort=False):
        q = q.copy()
        q["A"] = additive_projection(q)
        q["I"] = q.R - q.A
        c = evaluate.cells(q, ["R", "A", "I"])
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS].assign(origin=tag, season=season)
        w, y = c.possessions.to_numpy(float), c.actual.to_numpy(float)
        cen = lambda v: v - np.average(v, weights=w)
        yc, rc, ac, ic = cen(y), cen(c.R.to_numpy()), cen(c.A.to_numpy()), cen(c.I.to_numpy())
        rec = dict(origin=tag, season=season, sst=w @ yc ** 2, sse_R=w @ (yc - rc) ** 2, sse_A=w @ (yc - ac) ** 2,
                   row_share=float(np.average((q.I - np.average(q.I, weights=q.possessions)) ** 2, weights=q.possessions)
                                   / np.average((q.R - np.average(q.R, weights=q.possessions)) ** 2, weights=q.possessions)))
        X = np.c_[ac, ic]
        rec |= dict(xtx=(X * w[:, None]).T @ X, xty=(X * w[:, None]).T @ yc, var_i=float(np.average(ic ** 2, weights=w)))
        recs.append(rec)
        cells.append(c)
        print(tag, f"row variance share of the non-additive part {rec['row_share']:.3f}", flush=True)
    t = pd.DataFrame(recs)
    pd.concat(cells).to_pickle(OUT / "cells.pkl")
    per = t.groupby("season").apply(lambda s: pd.Series(dict(
        r2_R=1 - s.sse_R.sum() / s.sst.sum(), r2_A=1 - s.sse_A.sum() / s.sst.sum(),
        **dict(zip(("coef_a", "coef_i"), np.linalg.solve(sum(s.xtx), sum(s.xty)))))), include_groups=False)
    per["gain"] = per.r2_R - per.r2_A
    pooled_coef = np.linalg.solve(sum(t.xtx), sum(t.xty))
    se = lambda x: x.std(ddof=1) / np.sqrt(len(x))
    lines = [
        "Calibrated network (R) vs its best additive approximation (one value per player, each side), "
        "broad offense-five cells, 2016-2026, centered within quarter.",
        f"centered r²: network {1 - t.sse_R.sum() / t.sst.sum():.4f}, additive part alone {1 - t.sse_A.sum() / t.sst.sum():.4f}",
        f"gain from the non-additive part: {per.gain.mean():+.4f} ± {se(per.gain):.4f} (season mean ± SE), "
        f"{int((per.gain > 0).sum())}/{len(per)} seasons",
        f"regression of actual on [additive, non-additive]: coefficients {pooled_coef[0]:.2f}, {pooled_coef[1]:.2f}; "
        f"non-additive coefficient by season {per.coef_i.mean():.2f} ± {se(per.coef_i):.2f}, "
        f"{int((per.coef_i > 0).sum())}/{len(per)} positive",
        f"size: non-additive part's SD across cells {np.sqrt(t.var_i.mean()):.2f} points per 100; "
        f"share of the network's row-level variance {t.row_share.mean():.3f}",
        "", per.round(4).to_string()]
    text = "\n".join(lines)
    (OUT / "report.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
