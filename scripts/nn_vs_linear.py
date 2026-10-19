"""How much better than linear is the reference neural model, for points and for events? (exploratory)

Population: the primary benchmark's 44 quarters (2016-2026), reference
J_POINT_BOTH (checkpoint average, mean of seeds 17, 23, 41), neural model alone.

Points, against the registered linear control additive_defense (ridge
player-additive offense and defense, prior-only calibration):
- broad offense-five cells (>= 50 possessions per quarter), as the scorecard;
- every possession: r^2 of points per possession over all possessions in the
  44 quarters. Forecasts are constant within a row, so a model's possession-level
  SSE is the within-row sum of squares (from nba.possessions) plus the
  possession-weighted squared row-mean error.

Events, against a linear model given the same inputs: per origin, weighted
ridge on the prior five years of rows (history-mode inputs, the network's
730-day half-life), lineup features = mean and SD over the five attackers of the
standardized offensive state, the mean of their role and adjusted capability
rows, and the mean and SD of the defenders' descriptors and the mean of their
adjusted capability rows. One linear model per target:
    points, FGA, FTA and turnovers per possession; rim and three-point shares
    of FGA; rim and three-point FG%; offensive-rebound share of live rebounds.
Each target is weighted by its own exposure (possessions, FGA, attempts in the
zone, live rebounds). The network's targets come from its expected ledger,
rebuilt from the saved checkpoints (rebuilt points must match the saved
forecast). Events are native (uncalibrated) for both, so centered r^2 (each
quarter's mean error removed) is the primary event comparison; raw r^2 is shown.
Scored on broad offense-five cells, exposure weighted. Season-level SEs (11).

    PYTHONPATH=.:scripts python -u scripts/nn_vs_linear.py            # build per-origin rows (resumable)
    PYTHONPATH=.:scripts python -u scripts/nn_vs_linear.py --analyze
"""
import argparse
import sys
from contextlib import closing

import numpy as np
import pandas as pd
import torch

from lineups import db, evaluate, history, legacy, paths
from lineups.history import checkpoint_models      # the active cache root's history (lineups.history)
from lineups.evaluate import FIVE
from lineups.features import Store
from lineups.model import average_ledgers
from lineups.train import FitConfig, Rows, game_batches

OUT = paths.CACHE / "nn_vs_linear_2026_10_12"
TARGETS = ("points", "fga", "fta", "tov", "rim_share", "three_share", "rim_fg", "three_fg", "orb_rate")
RIM, THREES = [0], [4, 5]
RIDGE = 1.0


# ---- lineup features and targets ----------------------------------------------
def features(inputs):
    """Linear lineup summaries of exactly the network's inputs."""
    t = lambda k: inputs[k].double()
    parts = [t("msg").mean(1), t("msg").std(1, unbiased=False), t("role").mean(1), t("adjusted_offense").mean(1),
             t("defense").mean(1), t("defense").std(1, unbiased=False), t("adjusted_defense").mean(1)]
    return torch.cat(parts, -1).numpy()


def actual(g, rows):
    take = lambda k: np.asarray(g[k][rows]).astype(float)
    att, mk, rb = take("loc_attempt").sum(1), take("loc_make").sum(1), take("rebound")
    fga_ok = np.asarray(g["fga_observed"][rows])
    loc_ok = fga_ok & np.asarray(g["location_observed"][rows])
    n = take("possessions")
    fga = att.sum(1)
    out = dict(
        points=(take("points"), n), fga=(take("fga").sum(1), n * fga_ok), fta=(take("fta").sum(1), n * np.asarray(g["fta_observed"][rows])),
        tov=(take("turnover").sum(1), n), rim_share=(att[:, RIM].sum(1), fga * loc_ok),
        three_share=(att[:, THREES].sum(1), fga * loc_ok), rim_fg=(mk[:, RIM].sum(1), att[:, RIM].sum(1) * loc_ok),
        three_fg=(mk[:, THREES].sum(1), att[:, THREES].sum(1) * loc_ok), orb_rate=(rb[:, :5].sum(1), rb.sum(1)))
    # (numerator, exposure); the rate is numerator / exposure, zero-exposure rows carry no weight
    return {k: (np.where(e > 0, num, 0.), e) for k, (num, e) in out.items()}


def network_rates(pred):
    s = lambda v: v.double().sum(1).numpy()
    att, mk = pred.expected_attempts.double().sum(1).numpy(), pred.expected_makes.double().sum(1).numpy()
    fga = att.sum(1)
    return dict(points=pred.points100.double().numpy() / 100, fga=s(pred.fga), fta=s(pred.fta), tov=s(pred.turnover),
                rim_share=att[:, RIM].sum(1) / fga, three_share=att[:, THREES].sum(1) / fga,
                rim_fg=mk[:, RIM].sum(1) / att[:, RIM].sum(1), three_fg=mk[:, THREES].sum(1) / att[:, THREES].sum(1),
                orb_rate=s(pred.player_orb) / pred.live.double().numpy())


# ---- per origin ---------------------------------------------------------------------
def linear_fit(data, store, origin, normalizer, config=FitConfig()):
    """Weighted ridge per target on the prior five years (history-mode inputs)."""
    cutoff = legacy.day(origin.start)
    rows = data.prefix(cutoff, config.lookback_days)
    xtx, xty = {}, {}
    for ix in game_batches(data.game, rows, 8192):
        inputs, _, _ = data.batch(ix, normalizer)
        x = np.c_[np.ones(len(ix)), features(inputs)]
        decay = np.exp2(-(cutoff - data.date[ix]) / config.half_life_days)
        for k, (num, e) in actual(data.g, ix).items():
            w = decay * e
            y = np.divide(num, e, out=np.zeros_like(num), where=e > 0)
            xtx[k] = xtx.get(k, 0.) + (x * w[:, None]).T @ x
            xty[k] = xty.get(k, 0.) + (x * w[:, None]).T @ y
    beta = {}
    for k in TARGETS:
        a = xtx[k].copy()
        a[1:, 1:] += RIDGE * np.eye(len(a) - 1)
        beta[k] = np.linalg.solve(a, xty[k])
    return beta


def build_origin(o, g, data, store, by_game):
    normalizer, env = store.normalizer(o.tag, "final"), store.env(o.tag, "final")
    beta = linear_fit(data, store, o, normalizer)
    rows = np.sort(legacy.quarter_rows(o, g))
    batches = list(game_batches(data.game, rows))
    order = np.argsort(np.concatenate(batches))
    inputs = [data.batch(ix, normalizer, origin_index=int(o.origin_index))[0] for ix in batches]
    lin = {k: np.concatenate([np.c_[np.ones(len(ix)), features(x)] @ beta[k] for ix, x in zip(batches, inputs)])[order]
           for k in TARGETS}
    net = {k: 0. for k in TARGETS}
    for seed in legacy.SEEDS:
        models = checkpoint_models(o.tag, seeds=(seed,))
        with torch.no_grad():
            per = [network_rates(average_ledgers([m.eval()(x, env) for m in models])) for x in inputs]
        cols = {k: np.concatenate([p[k] for p in per])[order] for k in TARGETS}
        ids, saved = history.native(o.tag, seed, "checkpoint_average")
        gap = np.abs(100 * cols["points"] - saved).max()
        if not np.array_equal(ids, rows) or gap > 1e-6:
            raise ValueError(f"rebuilt forecast differs from the saved one: {o.tag}/s{seed} gap={gap}")
        net = {k: net[k] + cols[k] / len(legacy.SEEDS) for k in TARGETS}
    f = legacy.row_frame(rows, g)[["row", "game_id"] + FIVE]
    for k, (num, e) in actual(g, rows).items():
        f[f"{k}_num"], f[f"{k}_exp"] = num, e
        f[f"{k}_net"], f[f"{k}_lin"] = net[k], lin[k]
    return f.assign(origin=o.tag, season=int(o.season))


def build(only=None):
    (OUT / "rows").mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    store, g = Store(), legacy.matchups()
    data = Rows(g, store)
    for o in legacy.origins(2016).itertuples():
        path = OUT / "rows" / f"{o.tag}.pkl"
        if not path.exists() and (not only or o.tag in only):
            build_origin(o, g, data, store, None).to_pickle(path)
            print("built", o.tag, flush=True)


# ---- analysis -------------------------------------------------------------------------
def cell_stats(f, column_of, target):
    """Per-quarter weighted SSE (raw and centered) and SST on broad offense-five cells for one target."""
    out = []
    for (tag, season), q in f.groupby(["origin", "season"], sort=False):
        num, e = q[f"{target}_num"], q[f"{target}_exp"]
        keyed = q[FIVE].assign(num=num, e=e, poss=q.points_exp,
                               **{m: q[c] * e for m, c in column_of.items()})
        c = keyed.groupby(FIVE).sum()
        c = c[(c.poss >= evaluate.MIN_CELL_POSSESSIONS) & (c.e > 0)]
        w, y = c.e.to_numpy(float), (c.num / c.e).to_numpy(float)
        rec = dict(origin=tag, season=season, sst=w @ (y - np.average(y, weights=w)) ** 2, w=w.sum(),
                   sum_y=w @ y, sum_yy=w @ y ** 2)
        for m in column_of:
            err = y - (c[m] / c.e).to_numpy(float)
            rec[f"sse_{m}"], rec[f"ssec_{m}"] = w @ err ** 2, w @ (err - np.average(err, weights=w)) ** 2
        out.append(rec)
    return pd.DataFrame(out)


def compare(stats, a, b):
    """Pooled raw r^2 (variance around the pooled mean), centered r^2, per-season differences a - b."""
    sst_pooled = stats.sum_yy.sum() - stats.sum_y.sum() ** 2 / stats.w.sum()
    r2 = {m: 1 - stats[f"sse_{m}"].sum() / sst_pooled for m in (a, b)}
    r2c = {m: 1 - stats[f"ssec_{m}"].sum() / stats.sst.sum() for m in (a, b)}
    s = stats.groupby("season").sum()
    s_pooled = s.sum_yy - s.sum_y ** 2 / s.w
    d_raw = (s[f"sse_{b}"] - s[f"sse_{a}"]) / s_pooled
    d_c = (s[f"ssec_{b}"] - s[f"ssec_{a}"]) / s.sst
    se = lambda d: float(d.std(ddof=1) / np.sqrt(len(d)))
    return dict(r2_a=r2[a], r2_b=r2[b], diff=r2[a] - r2[b], se=se(d_raw), t=(r2[a] - r2[b]) / se(d_raw),
                pos=int((d_raw > 0).sum()), r2c_a=r2c[a], r2c_b=r2c[b], diff_c=r2c[a] - r2c[b], se_c=se(d_c),
                t_c=(r2c[a] - r2c[b]) / se(d_c), pos_c=int((d_c > 0).sum()), seasons=len(d_raw))


def possession_level(f):
    """Points per possession over every possession: r^2 of each forecast (per 1, not per 100)."""
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute("select game_id, count(*), sum(points_scored), sum(points_scored * points_scored) "
                    "from nba.possessions group by game_id")
        games = pd.DataFrame(cur.fetchall(), columns=["game_id", "n", "pts", "pts2"]).astype(float)
    games = games.set_index(games.game_id.astype(np.int64))
    out = []
    for season, q in f.groupby("season"):
        gm = games.reindex(q.game_id.unique())
        n_rows = q.points_exp.sum()
        if not np.isclose(gm.n.sum(), n_rows) or not np.isclose(gm.pts.sum(), q.points_num.sum()):
            raise ValueError(f"possession totals do not match rows in {season}")
        sst = gm.pts2.sum() - gm.pts.sum() ** 2 / gm.n.sum()
        ybar = q.points_num / q.points_exp
        within = gm.pts2.sum() - (q.points_exp * ybar ** 2).sum()
        rec = dict(season=season, sst=sst, possessions=n_rows)
        for m in ("calibrated", "additive_defense", "half"):
            rec[m] = within + (q.points_exp * (ybar - q[m] / 100) ** 2).sum()
        out.append(rec)
    return pd.DataFrame(out)


def analyze():
    from capacity_score import frames
    pd.set_option("display.width", 200, "display.precision", 5)
    g = legacy.matchups()
    f = pd.concat([pd.read_pickle(p) for p in sorted((OUT / "rows").glob("*.pkl"))], ignore_index=True)
    bench = frames(lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"), g)
    f = f.merge(bench[["row", "calibrated", "additive_defense", "half"]], on="row", validate="one_to_one")

    print("== Points, broad offense-five cells (points per 100)")
    pts = f.assign(**{f"points_{m}": f[m] / 100 for m in ("calibrated", "additive_defense", "half")})
    s = cell_stats(pts, {"nn": "points_calibrated", "additive": "points_additive_defense", "half": "points_half",
                         "linear": "points_lin"}, "points")
    rows = []
    for a, b in (("nn", "additive"), ("half", "additive"), ("nn", "linear")):
        rows.append(dict(contrast=f"{a} - {b}", **compare(s, a, b)))
    print(pd.DataFrame(rows).to_string(index=False))

    print("\n== Points per possession, every possession")
    p = possession_level(f)
    tot = p.sum()
    for m in ("calibrated", "half", "additive_defense"):
        print(f"{m}: r2 {1 - tot[m] / tot.sst:.5f}")
    d = (p.additive_defense - p.calibrated) / p.sst
    print(f"nn - additive: {(tot.additive_defense - tot.calibrated) / tot.sst:+.5f}, season se {d.std(ddof=1) / np.sqrt(len(d)):.5f}, "
          f"positive {(d > 0).sum()}/{len(d)}; possessions {tot.possessions:,.0f}")

    print("\n== Events, broad offense-five cells: network (native) vs linear on the same inputs")
    rows = []
    for k in TARGETS:
        s = cell_stats(f, {"net": f"{k}_net", "lin": f"{k}_lin"}, k)
        rows.append(dict(target=k, **compare(s, "net", "lin")))
    out = pd.DataFrame(rows)
    print(out.to_string(index=False))
    out.to_csv(OUT / "events.csv", index=False)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--analyze", action="store_true")
    p.add_argument("--only", nargs="+")
    a = p.parse_args()
    analyze() if a.analyze else build(a.only)
