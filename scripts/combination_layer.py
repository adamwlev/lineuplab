"""Fit the combination layer and run its forward check.

Protocol: reports/combination_layer_protocol_2026_10_13.md (committed before this ran).

1. Layer for the tool: 2022-2026 rows without late-game possessions, residuals
   against the network's own forecast, one joint fit per event; pair features
   projected on the involved type counts (only the orthogonal part is used).
2. Forward check: the same fit on 2016-2021, applied to every 2022-2026 row;
   points r^2 (pooled and within-quarter centered) and event squared error,
   network versus network + layer.
3. Shape check: curvature at counts 2 and 3 for same-type pairs.

    PYTHONPATH=.:scripts python -u scripts/combination_layer.py [--learned]

Output: experiments/cache/combination_layer_2026_10_13/ (layer.json, forward.json, report.txt).

--learned (Adam, 2026-10-14) re-measures the layer on top of the learned
combinations (lineups.learned): the residuals are taken against the network
plus SCALE times the module's change, seed means over 17, 23 and 41. The
module forecasts are the forward ones of the screens (2022-2026) and the
confirmation (2015-2021). The forward check adds the module's centered points
change (level on the previous quarter's rows) to the network on both sides.
Output: experiments/cache/combination_layer_2026_10_14_learned/.
"""
import argparse
import json

import numpy as np
import pandas as pd

import interaction_discovery as d
import interaction_discovery_posthoc as post
from lineups import combinations as cb
from lineups import paths
from lineups.evaluate import FIVE
from lineups.sources import SOURCES
from lineups.legacy import DEFENSE

OUT = paths.CACHE / "combination_layer_2026_10_13"
LEARNED_OUT = paths.CACHE / "combination_layer_2026_10_14_learned"
MODULE_ROWS = (paths.CACHE / "nonlinearity_screen_2026_10_13", paths.CACHE / "nonlinearity_confirm_2026_10_14")
FIT, FORWARD_FIT, FORWARD = (2022, 2026), (2016, 2021), (2022, 2026)
NN_ROWS = paths.CACHE / "nn_vs_linear_2026_10_12" / "rows"


def spec_events():
    """{event: [(side, a, b)]} from cb.EFFECTS, checked against the discovery's held-up list."""
    held = json.loads((d.OUT / "result.json").read_text())
    names = {(fam, c["candidate"]) for fam, v in held["families"].items() for c in v["confirmed"]
             if c["label"].startswith("held up")}
    mine = {(e, f"{a} x {b}") for e, _, a, b, _ in cb.EFFECTS}
    if names != mine:
        raise ValueError(f"effects differ from the discovery's held-up list: {names ^ mine}")
    out = {}
    for e, side, a, b, _ in cb.EFFECTS:
        out.setdefault(e, []).append((side, a, b))
    return out


def fit(frame, feats, y, years, keep, events):
    """Joint WLS per event; returns the layer spec (beta, cov, projection) for those rows."""
    out = {}
    for event, pairs in events.items():
        w_all = frame[f"w_{event}"].to_numpy(float)
        s = frame.season.between(*years).to_numpy() & keep & (w_all > 0) & np.isfinite(y[event])
        f = frame[s]
        quarter, game = pd.factorize(f.origin)[0], pd.factorize(f.game_id)[0]
        w = w_all[s]
        types = sorted({t for _, a, b in pairs for t in (a, b)}, key=list(cb.TYPES).index)
        n = np.stack([feats[s][f"n_{t}"].to_numpy(float) for t in types], 1)
        P = np.stack([feats[s][d.name(("offense" if side == "offense" else "defense", a, b))].to_numpy(float)
                      for side, a, b in pairs], 1)
        nc = np.stack([d.centered(n[:, j], quarter, w) for j in range(n.shape[1])], 1)
        Pc = np.stack([d.centered(P[:, j], quarter, w) for j in range(P.shape[1])], 1)
        yc = d.centered(y[event][s], quarter, w)
        X = np.c_[nc, Pc]
        Xw = X * w[:, None]
        B = X.T @ Xw
        beta = np.linalg.solve(B, Xw.T @ yc)
        e = yc - X @ beta
        scores = np.stack([np.bincount(game, Xw[:, j] * e) for j in range(X.shape[1])], 1)
        G = scores.shape[0]
        Binv = np.linalg.inv(B)
        V = Binv @ (scores.T @ scores) @ Binv * G / (G - 1)
        k = len(types)
        # projection of each pair feature on its own side's counts: within-quarter slopes, pooled intercept
        slopes = np.zeros((len(pairs), k))
        for j, (side, _, _) in enumerate(pairs):
            at = np.array([t[0] == side[0].upper() for t in types])
            A = nc[:, at]
            slopes[j, at] = np.linalg.solve(A.T @ (A * w[:, None]), (A * w[:, None]).T @ Pc[:, j])
        intercept = np.average(P, axis=0, weights=w) - slopes @ np.average(n, axis=0, weights=w)
        out[event] = dict(types=types, pairs=[list(p) for p in pairs], beta=beta[k:].tolist(),
                          se=np.sqrt(np.diag(V)[k:]).tolist(), cov=V[k:, k:].tolist(),
                          count_coef=beta[:k].tolist(), slopes=slopes.tolist(), intercept=intercept.tolist(),
                          rows=int(s.sum()), exposure=float(w.sum()))
    return out


def measured_max(frame, feats, years):
    s = frame.season.between(*years).to_numpy()
    w = frame.w_points.to_numpy(float)[s]
    out = {}
    for t in cb.TYPES:
        n = feats[s][f"n_{t}"].to_numpy().astype(int)
        share = np.bincount(n, w, 6) / w.sum()
        out[t] = int(np.flatnonzero(share >= cb.MEASURED_SHARE).max())
    return out


def side_flags(feats_tables, frame):
    """[N,5,9] offense and [N,5,5] defense flags per row from the discovery's per-quarter type tables."""
    o = np.zeros((len(frame), 5, len(cb.OFFENSE)), bool)
    de = np.zeros((len(frame), 5, len(cb.DEFENSE)), bool)
    for tag, idx in frame.groupby("origin", sort=False).indices.items():
        t = feats_tables[tag]
        q = frame.iloc[idx]
        o[idx] = t[list(cb.OFFENSE)].reindex(q[FIVE].to_numpy().ravel()).to_numpy().reshape(-1, 5, len(cb.OFFENSE))
        de[idx] = t[list(cb.DEFENSE)].reindex(q[DEFENSE].to_numpy().ravel()).to_numpy().reshape(-1, 5, len(cb.DEFENSE))
    return o, de


def row_values(frame, league):
    """Per-row unit values from the network's forecast rates (rim and three FG%), league constants otherwise."""
    import glob
    nn = pd.concat([pd.read_pickle(p)[["origin", "row", "fga_net", "tov_net", "points_net", "rim_share_net",
                                       "three_share_net", "rim_fg_net", "three_fg_net"]]
                    for p in sorted(glob.glob(str(NN_ROWS / "*.pkl")))], ignore_index=True)
    m = frame[["origin", "row"]].merge(nn, on=["origin", "row"], how="left", validate="one_to_one")
    rim, three = m.rim_share_net.to_numpy(), m.three_share_net.to_numpy()
    other = 1 - rim - three
    att = np.stack([rim, other, three], 1)
    mid_fg = sum(league["makes"][1:4]) / sum(league["attempts"][1:4])
    mk = att * np.stack([m.rim_fg_net.to_numpy(), np.full(len(m), mid_fg), m.three_fg_net.to_numpy()], 1)
    ft = league["ftm"] / league["fta"]
    return cb.values(m.fga_net.to_numpy(), att, mk, (2., 2., 3.), (0,), (2,), ft, m.points_net.to_numpy(),
                     m.tov_net.to_numpy())


def r2(actual, pred, w, quarter=None):
    if quarter is not None:
        actual, pred = d.centered(actual, quarter, w), d.centered(pred, quarter, w)
    mean = np.average(actual, weights=w) if quarter is None else 0.
    return 1 - (w * (actual - pred) ** 2).sum() / (w * (actual - mean) ** 2).sum()


def shape_check(frame, feats, y, years, keep):
    """Curvature at counts 2 and 3 (count dummies, within-quarter centered) for same-type pairs."""
    out = {}
    for event, side, a, b, _ in cb.EFFECTS:
        if a != b:
            continue
        w_all = frame[f"w_{event}"].to_numpy(float)
        s = frame.season.between(*years).to_numpy() & keep & (w_all > 0) & np.isfinite(y[event])
        f = frame[s]
        quarter, game = pd.factorize(f.origin)[0], pd.factorize(f.game_id)[0]
        w = w_all[s]
        n = feats[s][f"n_{a}"].to_numpy().astype(int)
        D = np.stack([(n == 1), (n == 2), (n >= 3)], 1).astype(float)
        X = np.stack([d.centered(D[:, j], quarter, w) for j in range(3)], 1)
        yc = d.centered(y[event][s], quarter, w)
        Xw = X * w[:, None]
        B = X.T @ Xw
        beta = np.linalg.solve(B, Xw.T @ yc)
        e = yc - X @ beta
        scores = np.stack([np.bincount(game, Xw[:, j] * e) for j in range(3)], 1)
        G = scores.shape[0]
        Binv = np.linalg.inv(B)
        V = Binv @ (scores.T @ scores) @ Binv * G / (G - 1)
        c2, c3 = np.array([-2, 1, 0.]), np.array([-3, 0, 1.])      # f(2)-2f(1), f(3)-3f(1)
        k2, k3 = float(c2 @ beta), float(c3 @ beta)
        out[f"{event}:{a}x{b}"] = dict(curv2=k2, se2=float(np.sqrt(c2 @ V @ c2)), curv3=k3, se3=float(np.sqrt(c3 @ V @ c3)),
                                       ratio=k3 / k2 if k2 else np.nan, share3=float(w[n >= 3].sum() / w.sum()))
    return out


def learned_changes(frame):
    """Per row of frame: SCALE x the module's seed-mean change in each event rate (x100, as the residuals), and
    in points/100 after removing each fit's level on the previous quarter's rows."""
    from lineups import learned
    parts = []
    for directory in MODULE_ROWS:
        level = pd.read_csv(directory / "prior_level.csv").query("where == 'previous'").set_index(["origin", "seed"]).level
        for tag in sorted(set(frame.origin) & set(level.index.get_level_values(0))):
            per = []
            for seed in (17, 23, 41):
                sfx = "" if seed == 17 else f"_s{seed}"
                ref = pd.read_pickle(directory / f"reference{sfx}_{tag}_rows.pkl").set_index("row")
                arm = pd.read_pickle(directory / f"frozen_fixed{sfx}_{tag}_rows.pkl").set_index("row")
                change = arm[list(learned.FIELDS)] - ref[list(learned.FIELDS)]
                change["points"] -= level[(tag, seed)]
                per.append(change)
            mean = sum(per) / len(per)
            parts.append(mean.assign(origin=tag).reset_index())
    m = frame[["origin", "row"]].merge(pd.concat(parts, ignore_index=True), on=["origin", "row"], how="left",
                                       validate="one_to_one")
    if m[list(learned.FIELDS)].isna().any().any():
        raise ValueError("rows without a module forecast")
    out = {k: learned.SCALE * 100 * m[k].to_numpy(float) for k in cb.EVENTS}
    out["points"] = learned.SCALE * m.points.to_numpy(float)
    return out


def main():
    global OUT
    p = argparse.ArgumentParser()
    p.add_argument("--learned", action="store_true", help="re-measure on top of the learned combinations")
    a = p.parse_args()
    if a.learned:
        OUT = LEARNED_OUT
    OUT.mkdir(parents=True, exist_ok=True)
    events = spec_events()
    bench = d.residuals(False)
    feats, tables = d.features(bench, False)
    y = post.network_residuals(bench, False)
    change = learned_changes(bench) if a.learned else None
    if change is not None:
        y = {k: (v - change[k] if k in cb.EVENTS else v) for k, v in y.items()}
    late = post.late_rows()
    keys = ["game_id", *FIVE, *DEFENSE]
    no_late = bench[keys].merge(late, on=keys, how="left").late.fillna(0).to_numpy() == 0
    # the league-average offense of the root's release: the 2026-10-12 export, or the clean release's (2026-10-16)
    export = SOURCES["clean" if paths.CLEAN_ROOT else "names"]["export"]
    league = json.loads((export / "meta.json").read_text())["explain"]["league"]
    lines = []

    # 1. the tool's layer
    mm = measured_max(bench, feats, FIT)
    residual = ("event rate minus the network's own forecast plus half its learned combinations (x100)" if a.learned
                else "event rate minus the network's own forecast (x100)")
    layer = dict(fit=dict(seasons=FIT, rows="game x offense five x defense five, no late-game possessions",
                          residual=residual),
                 measured_max=mm, measured_share=cb.MEASURED_SHARE, events=fit(bench, feats, y, FIT, no_late, events))
    (OUT / "layer.json").write_text(json.dumps(layer, indent=1))
    lines.append(f"Layer fit {FIT}, no late-game rows. Measured maximum counts: {mm}")
    for event, e in layer["events"].items():
        for p, b, s in zip(e["pairs"], e["beta"], e["se"]):
            lines.append(f"  {event:<12} {p[0]:<8} {p[1]} x {p[2]:<14} beta {b:+.3f} ({s:.3f})")

    # 2. forward check
    fwd = cb.Layer(dict(measured_max=mm, events=fit(bench, feats, y, FORWARD_FIT, no_late, events)))
    o, de = side_flags(tables, bench)
    s = bench.season.between(*FORWARD).to_numpy()
    unit = row_values(bench[s], league)
    rows = pd.read_pickle(d.SYNERGY / "rows_benchmark.pkl")[["origin", "row", "actual", "R", "possessions", "season"]]
    m = bench[s][["origin", "row"]].merge(rows, on=["origin", "row"], how="left", validate="one_to_one")
    w, actual, net = m.possessions.to_numpy(float), m.actual.to_numpy(float), m.R.to_numpy(float)
    if change is not None:
        net = net + change["points"][s]
    quarter = pd.factorize(m.origin)[0]
    res = {}
    # declared: pairwise continued (uncapped); the tool's forecast: counts held at the measured maximum (capped)
    for variant, cap in (("continued", False), ("measured_range", True)):
        ev = cb.Layer.by_event(fwd.deltas(o[s], de[s], cap))
        layer_points = sum(ev[k] * unit[k] for k in cb.EVENTS)
        r = dict(events={}, by_season={})
        r["points"] = dict(raw_network=r2(actual, net, w), raw_layer=r2(actual, net + layer_points, w),
                           centered_network=r2(actual, net, w, quarter),
                           centered_layer=r2(actual, net + layer_points, w, quarter),
                           mean_abs_layer=float(np.average(np.abs(layer_points), weights=w)),
                           sd_layer=float(np.sqrt(np.average((layer_points - np.average(layer_points, weights=w)) ** 2, weights=w))),
                           p99_abs_layer=float(np.quantile(np.abs(layer_points), .99)))
        for season in sorted(m.season.unique()):
            at = (m.season == season).to_numpy()
            q = pd.factorize(m.origin[at])[0]
            r["by_season"][int(season)] = dict(
                raw=r2(actual[at], net[at] + layer_points[at], w[at]) - r2(actual[at], net[at], w[at]),
                centered=r2(actual[at], net[at] + layer_points[at], w[at], q) - r2(actual[at], net[at], w[at], q))
        for event in cb.EVENTS:
            ww = bench[s][f"w_{event}"].to_numpy(float)
            yy = y[event][s]
            ok = (ww > 0) & np.isfinite(yy)
            pred = np.broadcast_to(np.asarray(ev[event], float), yy.shape)   # 0 for a family with no held-up effect
            sse0, sse1 = (ww[ok] * yy[ok] ** 2).sum(), (ww[ok] * (yy[ok] - pred[ok]) ** 2).sum()
            per = {}
            for season in sorted(bench[s].season.unique()):
                at = ok & (bench[s].season == season).to_numpy()
                per[int(season)] = float(((ww[at] * (yy[at] - pred[at]) ** 2).sum() - (ww[at] * yy[at] ** 2).sum())
                                         / (ww[at] * yy[at] ** 2).sum())
            r["events"][event] = dict(relative_change=float((sse1 - sse0) / sse0), by_season=per, keep=bool(sse1 <= sse0))
        p = r["points"]
        lines.append(f"\nForward check ({variant}): layer fit {FORWARD_FIT}, applied to {FORWARD} rows (all, possession-weighted)")
        lines.append(f"  points r2 raw {p['raw_network']:.5f} -> {p['raw_layer']:.5f} ({p['raw_layer'] - p['raw_network']:+.5f}); "
                     f"centered {p['centered_network']:.5f} -> {p['centered_layer']:.5f} "
                     f"({p['centered_layer'] - p['centered_network']:+.5f})")
        lines.append(f"  layer size: mean |adjustment| {p['mean_abs_layer']:.3f}, SD {p['sd_layer']:.3f}, "
                     f"99th percentile |adjustment| {p['p99_abs_layer']:.3f} points per 100")
        lines.append("  by season (raw, centered): " + ", ".join(f"{k} {v['raw']:+.5f}/{v['centered']:+.5f}"
                                                                for k, v in r["by_season"].items()))
        for event, v in r["events"].items():
            lines.append(f"  {event:<12} squared error {100 * v['relative_change']:+.3f}% "
                         f"(seasons: {', '.join(f'{100 * x:+.2f}' for x in v['by_season'].values())}) keep={v['keep']}")
        decision = p["raw_layer"] - p["raw_network"] >= -.003
        lines.append(f"  decision: layer {'enters' if decision else 'does not enter'} the printed number "
                     "(rule: raw r2 change >= -0.003)")
        r["decision"] = dict(enters=bool(decision), keep_events=[k for k, v in r["events"].items() if v["keep"]])
        res[variant] = r

    # 3. shape check
    shape = shape_check(bench, feats, y, FIT, no_late)
    lines.append("\nShape check (2022-2026, no late-game rows): curvature f(2)-2f(1) and f(3)-3f(1); pairwise predicts ratio 3")
    for k, v in shape.items():
        lines.append(f"  {k:<26} count 2: {v['curv2']:+.2f} ({v['se2']:.2f})  count 3+: {v['curv3']:+.2f} ({v['se3']:.2f})  "
                     f"ratio {v['ratio']:.1f}  share at 3+: {100 * v['share3']:.1f}%")
    res["shape"] = shape
    (OUT / "forward.json").write_text(json.dumps(res, indent=1))
    text = "\n".join(lines)
    (OUT / "report.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
