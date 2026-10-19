"""Is there room left in the events where the network ties a linear model? (exploratory)

Uses the rows of scripts/nn_vs_linear.py (44 benchmark quarters, broad offense-five
cells). For each target:

1. Ceiling. Split each cell's games by game-id parity; the exposure-weighted
   correlation of the two half-cell rates across cells within each quarter,
   stepped up with Spearman-Brown, estimates the share of within-quarter cell
   variance that is persistent (the centered-r^2 ceiling for any forecast).
2. Share of the ceiling reached by the network and the linear model (centered r^2).
3. Missing order statistics. Regress the network's centered cell residual on
   the attackers' max-minus-mean and min-minus-mean of the matching player rate
   (origin states), within quarter; report the share of residual variance they
   explain, pooled and by season.

    PYTHONPATH=.:scripts python -u scripts/event_headroom.py
"""
import numpy as np
import pandas as pd

from lineups import evaluate, legacy, paths
from lineups.evaluate import FIVE
from lineups.features import Store
from nn_vs_linear import OUT, TARGETS

# matching player state coordinate (lineups.model): 0 FGA, 1 FTA, 2 TO log rates; 3-8 location logits; 9-14 make logits
STATE = dict(fga=[0], fta=[1], tov=[2], rim_share=[3], three_share=[7, 8], rim_fg=[9], three_fg=[13, 14], points=[0, 16],
             orb_rate=None)


def cells(f, target):
    out = []
    for (tag, season), q in f.groupby(["origin", "season"], sort=False):
        num, e = q[f"{target}_num"], q[f"{target}_exp"]
        half = (q.game_id % 2).to_numpy()
        k = q[FIVE].assign(num=num, e=e, poss=q.points_exp, net=q[f"{target}_net"] * e, lin=q[f"{target}_lin"] * e,
                           num0=num * (half == 0), e0=e * (half == 0), num1=num * (half == 1), e1=e * (half == 1))
        c = k.groupby(FIVE).sum().reset_index()
        c = c[(c.poss >= evaluate.MIN_CELL_POSSESSIONS) & (c.e > 0)]
        c = c.assign(origin=tag, season=season, y=c.num / c.e, net=c.net / c.e, lin=c.lin / c.e)
        out.append(c)
    return pd.concat(out, ignore_index=True)


def wcorr(a, b, w):
    a, b = a - np.average(a, weights=w), b - np.average(b, weights=w)
    return (w @ (a * b)) / np.sqrt((w @ a ** 2) * (w @ b ** 2))


def main():
    pd.set_option("display.width", 200, "display.precision", 4)
    f = pd.concat([pd.read_pickle(p) for p in sorted((OUT / "rows").glob("*.pkl"))], ignore_index=True)
    store = Store()
    index = {t: i for t, i in zip(legacy.origins().tag, legacy.origins().origin_index)}
    rows = []
    for target in TARGETS:
        c = cells(f, target)
        rel, sst, sse = [], {m: 0. for m in ("net", "lin")}, 0.
        per_q = []
        for tag, q in c.groupby("origin", sort=False):
            both = q[(q.e0 > 0) & (q.e1 > 0)]
            w = (both.e0 * both.e1 / (both.e0 + both.e1)).to_numpy()
            r = wcorr((both.num0 / both.e0).to_numpy(), (both.num1 / both.e1).to_numpy(), w)
            w_all, y = q.e.to_numpy(), q.y.to_numpy()
            var = w_all @ (y - np.average(y, weights=w_all)) ** 2
            per_q.append(dict(origin=tag, season=q.season.iloc[0], reliability=2 * r / (1 + r), sst=var,
                              **{f"ssec_{m}": w_all @ ((y - q[m]) - np.average(y - q[m], weights=w_all)) ** 2
                                 for m in ("net", "lin")}))
        p = pd.DataFrame(per_q)
        ceiling = float(np.average(p.reliability, weights=p.sst))
        r2 = {m: 1 - p[f"ssec_{m}"].sum() / p.sst.sum() for m in ("net", "lin")}
        rec = dict(target=target, ceiling=ceiling, net=r2["net"], lin=r2["lin"], net_share=r2["net"] / ceiling,
                   lin_share=r2["lin"] / ceiling, unexplained=ceiling - r2["net"])
        # order statistics of the matching player rate among the five attackers
        cols = STATE[target]
        if cols is not None:
            feats = []
            for tag, q in c.groupby("origin", sort=False):
                base = store.offense(q[FIVE].to_numpy(np.int64), origin_index=int(index[tag]))["base"][..., cols].sum(-1)
                d = np.c_[base.max(1) - base.mean(1), base.min(1) - base.mean(1)]
                d = d - np.average(d, axis=0, weights=q.e)
                res = (q.y - q.net).to_numpy()
                res = res - np.average(res, weights=q.e)
                feats.append(pd.DataFrame(dict(season=q.season.to_numpy(), w=q.e.to_numpy(), res=res, mx=d[:, 0], mn=d[:, 1])))
            z = pd.concat(feats, ignore_index=True)
            X, y, w = z[["mx", "mn"]].to_numpy(), z.res.to_numpy(), z.w.to_numpy()
            sw = np.sqrt(w)
            beta = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]
            share = 1 - (w @ (y - X @ beta) ** 2) / (w @ y ** 2)
            by = []
            for s, t in z.groupby("season"):
                Xs, ys, ws = t[["mx", "mn"]].to_numpy(), t.res.to_numpy(), t.w.to_numpy()
                b = np.linalg.lstsq(Xs * np.sqrt(ws)[:, None], ys * np.sqrt(ws), rcond=None)[0]
                by.append(b)
            by = np.array(by)
            rec |= dict(order_stat_share=share, beta_max=beta[0], beta_max_se=by[:, 0].std(ddof=1) / np.sqrt(len(by)),
                        beta_min=beta[1], beta_min_se=by[:, 1].std(ddof=1) / np.sqrt(len(by)))
        rows.append(rec)
    out = pd.DataFrame(rows)
    print(out.to_string(index=False))
    out.to_csv(OUT / "headroom.csv", index=False)


if __name__ == "__main__":
    main()
