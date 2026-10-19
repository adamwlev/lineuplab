"""In-support band: persistent forecast error on real lineups (docs/CLOSEOUT.md, step 4a; exploratory).

For each cell (a five on offense, on defense, or both for the margin, in one
quarter), the quarter's games are split by game-id parity. Each half's
residual is actual minus forecast, points per 100, against the opponents
actually faced. The shared part of the two halves' residuals estimates tau²,
the variance of a lineup's persistent discrepancy from the forecast; the rest
is finite-game noise:

    tau² = weighted covariance of (e1, e2) across cells, centered within quarter,
    weights n1 n2 / (n1 + n2)

This is the v16 U1 working model (docs/history/JOINT_CAPABILITY_V16_PLAN.md
section 9). Tau includes in-quarter context the forecast cannot see, so it is
the right width for "how far is this lineup's rating from the forecast" on
observed-like lineups. It does not validate anything off support.

Forecast: the calibrated network alone (R, three-seed mean) on the 2016-2026
benchmark rows saved by scripts/ensemble_check.py. Cells need at least
MIN_HALF possessions in each half.

    PYTHONPATH=. python -u scripts/band_in_support.py
"""
import numpy as np
import pandas as pd

from lineups import paths
from lineups.evaluate import FIVE
from lineups.legacy import DEFENSE

ROWS = paths.CACHE / "ensemble_check_2026_10_12" / "benchmark.pkl"
OUT = paths.CACHE / "band_in_support_2026_10_12"
MIN_HALF = 25


def halves(f, keys, sign):
    """Per (origin, five, half): possessions, actual and forecast per 100 (sign -1: points allowed)."""
    g = f.assign(half=f.game_id % 2, fp=f.R * f.possessions)
    g = g.groupby(["origin", "season", *keys, "half"], as_index=False)[["possessions", "points", "fp"]].sum()
    g["e"] = 100 * g.points / g.possessions - g.fp / g.possessions
    g["e"] *= sign
    wide = g.pivot_table(index=["origin", "season", *keys], columns="half", values=["possessions", "e"])
    wide.columns = [f"{a}{b}" for a, b in wide.columns]
    wide = wide.dropna()
    wide = wide[(wide.possessions0 >= MIN_HALF) & (wide.possessions1 >= MIN_HALF)].reset_index()
    if keys != FIVE:
        wide = wide.rename(columns=dict(zip(keys, FIVE)))
    return wide


def tau2(c):
    w = c.n0 * c.n1 / (c.n0 + c.n1)
    out = []
    for _, q in c.assign(w=w).groupby("origin"):
        m0, m1 = np.average(q.e0, weights=q.w), np.average(q.e1, weights=q.w)
        out.append(dict(num=float(q.w @ ((q.e0 - m0) * (q.e1 - m1))), den=float(q.w.sum()),
                        noise=float(q.w @ (((q.e0 - m0) ** 2 + (q.e1 - m1) ** 2) / 2)), season=int(q.season.iloc[0])))
    t = pd.DataFrame(out)
    per = t.groupby("season").apply(lambda s: s.num.sum() / s.den.sum(), include_groups=False)
    return dict(tau2=t.num.sum() / t.den.sum(), tau=np.sqrt(max(t.num.sum() / t.den.sum(), 0)),
                season_se=float(per.std(ddof=1) / np.sqrt(len(per))), cells=len(c))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f = pd.read_pickle(ROWS)
    f[FIVE] = np.sort(f[FIVE].to_numpy(), 1)
    f[DEFENSE] = np.sort(f[DEFENSE].to_numpy(), 1)
    off = halves(f, FIVE, 1.).rename(columns=dict(possessions0="n0", possessions1="n1"))
    de = halves(f, DEFENSE, -1.).rename(columns=dict(possessions0="n0", possessions1="n1"))
    both = off.merge(de, on=["origin", "season", *FIVE], suffixes=("_o", "_d"))
    margin = both.assign(e0=both.e0_o + both.e0_d, e1=both.e1_o + both.e1_d,
                         n0=2 / (1 / both.n0_o + 1 / both.n0_d), n1=2 / (1 / both.n1_o + 1 / both.n1_d))
    rows = []
    for name, c in (("offense", off), ("defense", de), ("margin", margin)):
        r = tau2(c)
        rows.append(dict(side=name, **r))
        for lo, hi in ((25, 50), (50, 100), (100, 10 ** 6)):
            s = c[(np.minimum(c.n0, c.n1) >= lo) & (np.minimum(c.n0, c.n1) < hi)]
            rows.append(dict(side=f"{name}, half {lo}-{hi}", **tau2(s)))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "tau.csv", index=False)
    print("Residuals are signed so positive is good for the five: defense = forecast minus actual points allowed; margin = offense + defense.")
    print(t.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
