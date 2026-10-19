"""Interaction discovery (protocol: reports/interaction_discovery_protocol_2026_10_13.md; exploratory).

105 player-type combinations x 8 outcome families. Discover on 2016-2021 (BH,
q = .10), confirm the top 5 per family on held-out 2022-2026 (one-sided, Holm),
replicate in 2007-2013. Residuals are against the best additive approximation of
the network's forecast, per family. SEs are cluster-robust by game.

    PYTHONPATH=.:scripts python -u scripts/interaction_discovery.py

Output: experiments/cache/interaction_discovery_2026_10_13/.
"""
import glob
import itertools
import json

import numpy as np
import pandas as pd
from scipy import sparse, stats
from scipy.sparse.linalg import lsqr

import era_run
from lineups import combinations as cb
from lineups import legacy, paths
from lineups.evaluate import FIVE
from lineups.features import Store
from lineups.legacy import DEFENSE

OUT = paths.CACHE / "interaction_discovery_2026_10_13"
SYNERGY = paths.CACHE / "synergy_hypotheses_2026_10_12"
EVENTS = ("three_fg", "rim_fg", "tov", "fta", "orb_rate", "rim_share", "three_share")
FAMILIES = ("points",) + EVENTS
WINDOWS = dict(discovery=(2016, 2021), confirmation=(2022, 2026), replication=(2007, 2013))
OFF, DEF = cb.OFFENSE, cb.DEFENSE
CANDIDATES = ([("offense", a, b) for a, b in itertools.combinations_with_replacement(OFF, 2)]
              + [("defense", a, b) for a, b in itertools.combinations_with_replacement(DEF, 2)]
              + [("matchup", a, b) for a in OFF for b in DEF])
Q, K, HOLM_ALPHA = .10, 5, .05
SHOT_EVENTS = {"three_fg", "rim_fg", "rim_share", "three_share"}


def name(c):
    kind, a, b = c
    return f"{a} x {b}" if kind != "matchup" else f"{a} vs {b}"


# ---- rows, events and additive baselines ------------------------------------------
def project(off, de, target, weight):
    """Weighted least squares of target on intercept + attacker and defender dummies (rows with weight > 0)."""
    keep = weight > 0
    out = np.full(len(target), np.nan)
    if keep.sum() < 50:
        return out
    o, d = off[keep], de[keep]
    ou, oi = np.unique(o, return_inverse=True)
    du, di = np.unique(d, return_inverse=True)
    n = int(keep.sum())
    rows = np.repeat(np.arange(n), 5)
    X = sparse.hstack([sparse.csr_matrix(np.ones((n, 1))),
                       sparse.csr_matrix((np.ones(5 * n), (rows, oi.ravel())), shape=(n, len(ou))),
                       sparse.csr_matrix((np.ones(5 * n), (rows, di.ravel())), shape=(n, len(du)))]).tocsr()
    w = np.sqrt(weight[keep])
    sol = lsqr(sparse.diags(w) @ X, w * target[keep], atol=1e-10, btol=1e-10, iter_lim=20000)[0]
    out[keep] = X @ sol
    return out


def event_columns(era):
    """Per (origin, row): actual numerator, exposure and forecast rate for each event."""
    if not era:
        frames = []
        for path in sorted(glob.glob(str(paths.CACHE / "nn_vs_linear_2026_10_12" / "rows" / "*.pkl"))):
            f = pd.read_pickle(path)
            cols = {"origin": f.origin, "row": f.row}
            for k in EVENTS:
                cols |= {f"{k}_num": f[f"{k}_num"], f"{k}_exp": f[f"{k}_exp"], f"{k}_fc": f[f"{k}_net"]}
            frames.append(pd.DataFrame(cols))
        return pd.concat(frames, ignore_index=True)
    f = pd.concat([pd.read_pickle(p) for p in sorted(glob.glob(str(paths.CACHE / "era_diagnostics_2026_10_12" / "rows_s17_23" / "*.pkl")))],
                  ignore_index=True)
    obs = f.observed.astype(float).to_numpy()
    att = {z: f[f"att_{z}_actual"].to_numpy(float) * obs for z in ("rim", "paint", "mid", "longmid", "c3", "ab3")}
    mk = {z: f[f"make_{z}_actual"].to_numpy(float) * obs for z in ("rim", "c3", "ab3")}
    ra = {z: f[f"R_att_{z}"].to_numpy(float) for z in ("rim", "paint", "mid", "longmid", "c3", "ab3")}
    rm = {z: f[f"R_make_{z}"].to_numpy(float) for z in ("rim", "c3", "ab3")}
    fga, rfga = sum(att.values()), sum(ra.values())
    n = f.possessions.to_numpy(float)
    cols = dict(origin=f.origin, row=f.row,
                three_fg_num=mk["c3"] + mk["ab3"], three_fg_exp=att["c3"] + att["ab3"],
                three_fg_fc=(rm["c3"] + rm["ab3"]) / (ra["c3"] + ra["ab3"]),
                rim_fg_num=mk["rim"], rim_fg_exp=att["rim"], rim_fg_fc=rm["rim"] / ra["rim"],
                tov_num=f.tov_actual.to_numpy(float), tov_exp=n, tov_fc=f.R_tov.to_numpy(float),
                fta_num=f.fta_actual.to_numpy(float), fta_exp=n, fta_fc=f.R_fta.to_numpy(float),
                orb_rate_num=f.orb_actual.to_numpy(float), orb_rate_exp=(f.orb_actual + f.drb_actual).to_numpy(float),
                orb_rate_fc=(f.R_orb / f.R_live).to_numpy(float),
                rim_share_num=att["rim"], rim_share_exp=fga, rim_share_fc=ra["rim"] / rfga,
                three_share_num=att["c3"] + att["ab3"], three_share_exp=fga, three_share_fc=(ra["c3"] + ra["ab3"]) / rfga)
    return pd.DataFrame(cols)


def residuals(era):
    """Rows with a residual and weight per family (points from the synergy rows; events projected here)."""
    path = OUT / f"residuals_{'era' if era else 'benchmark'}.pkl"
    if path.exists():
        return pd.read_pickle(path)
    rows = pd.read_pickle(SYNERGY / f"rows_{'era' if era else 'benchmark'}.pkl")
    rows = rows[["game_id", "possessions", "row", *FIVE, *DEFENSE, "origin", "season", "res"]]
    rows = rows.merge(event_columns(era), on=["origin", "row"], how="left", validate="one_to_one")
    out = []
    for tag, q in rows.groupby("origin", sort=False):
        q = q.copy()
        off, de = q[FIVE].to_numpy(), q[DEFENSE].to_numpy()
        q["y_points"], q["w_points"] = q.res, q.possessions.astype(float)
        for k in EVENTS:
            exp = q[f"{k}_exp"].fillna(0).to_numpy(float)
            fc = q[f"{k}_fc"].to_numpy(float)
            ok = (exp > 0) & np.isfinite(fc)
            w = np.where(ok, exp, 0.)
            a = project(off, de, np.where(ok, fc, 0.), w)
            rate = np.divide(q[f"{k}_num"].fillna(0).to_numpy(float), exp, out=np.zeros(len(q)), where=exp > 0)
            q[f"y_{k}"], q[f"w_{k}"] = 100 * (rate - a), w
        out.append(q[["game_id", "row", *FIVE, *DEFENSE, "origin", "season"] + [f"{p}_{f}" for f in FAMILIES for p in "yw"]])
        print("residuals", tag, flush=True)
    frame = pd.concat(out, ignore_index=True)
    OUT.mkdir(parents=True, exist_ok=True)
    frame.to_pickle(path)
    return frame


# ---- player types --------------------------------------------------------------------------
def types(store, origin_index, pids):
    """Type flags at one origin; percentiles among ``pids`` (lineups.combinations holds the definitions)."""
    off = store.offense(pids, origin_index=origin_index)
    prof = cb.profile(off["base"], off["rb_prob"], store.defense(pids, origin_index=origin_index),
                      store.players["height"][pids])
    return pd.DataFrame(cb.flags(prof, cb.cutoffs(prof)), index=pids, columns=list(cb.TYPES))


def type_tables(era):
    store = Store(era_run.STORE) if era else Store()
    schedule = (era_run.origins() if era else legacy.origins()).set_index("tag")
    return store, schedule


def features(frame, era):
    """Type counts and the 105 pair features per row; also the per-quarter type tables."""
    store, schedule = type_tables(era)
    parts, tables = [], {}
    for tag, q in frame.groupby("origin", sort=False):
        pids = np.unique(np.r_[q[FIVE].to_numpy().ravel(), q[DEFENSE].to_numpy().ravel()])
        t = types(store, int(schedule.loc[tag, "origin_index"]), pids)
        tables[tag] = t
        o = {k: t[k].reindex(q[FIVE].to_numpy().ravel()).to_numpy().reshape(-1, 5) for k in OFF}
        d = {k: t[k].reindex(q[DEFENSE].to_numpy().ravel()).to_numpy().reshape(-1, 5) for k in DEF}
        cols = {f"n_{k}": v.sum(1).astype(float) for k, v in (o | d).items()}
        for c in CANDIDATES:
            kind, a, b = c
            if kind == "matchup":
                cols[name(c)] = cols[f"n_{a}"] * cols[f"n_{b}"]
                continue
            side = o if kind == "offense" else d
            na, nb = cols[f"n_{a}"], cols[f"n_{b}"]
            cols[name(c)] = na * (na - 1) / 2 if a == b else na * nb - (side[a] & side[b]).sum(1)
        parts.append(pd.DataFrame(cols, index=q.index))
    return pd.concat(parts), tables


# ---- estimation -----------------------------------------------------------------------------
def centered(x, quarter, w):
    m = np.bincount(quarter, w * x) / np.maximum(np.bincount(quarter, w), 1e-12)
    return x - m[quarter]


def estimate(y, w, X, quarter, game):
    """WLS of y on X (columns already centered within quarter); cluster-robust SE of the last coefficient."""
    Xw = X * w[:, None]
    B = X.T @ Xw
    if np.linalg.matrix_rank(B) < B.shape[0]:
        return np.nan, np.nan
    b = np.linalg.solve(B, Xw.T @ y)
    e = y - X @ b
    scores = np.stack([np.bincount(game, Xw[:, j] * e) for j in range(X.shape[1])], 1)
    G = scores.shape[0]
    Binv = np.linalg.inv(B)
    V = Binv @ (scores.T @ scores) @ Binv * G / max(G - 1, 1)
    return float(b[-1]), float(np.sqrt(V[-1, -1]))


def window_data(frame, feats, family, years):
    s = frame.season.between(*years).to_numpy() & (frame[f"w_{family}"].to_numpy() > 0) & np.isfinite(frame[f"y_{family}"].to_numpy())
    f = frame[s]
    quarter = pd.factorize(f.origin)[0]
    game = pd.factorize(f.game_id)[0]
    w = f[f"w_{family}"].to_numpy(float)
    return dict(y=centered(f[f"y_{family}"].to_numpy(float), quarter, w), w=w, quarter=quarter, game=game,
                feats=feats[s], season=f.season.to_numpy())


def test(d, c, by_season=False):
    kind, a, b = c
    mains = [f"n_{a}"] if (a == b and kind != "matchup") else [f"n_{a}", f"n_{b}"]
    cols = mains + [name(c)]
    X = np.stack([centered(d["feats"][k].to_numpy(float), d["quarter"], d["w"]) for k in cols], 1)
    coef, se = estimate(d["y"], d["w"], X, d["quarter"], d["game"])
    out = dict(coef=coef, se=se, exposure=float((d["w"] * (d["feats"][name(c)].to_numpy() > 0)).sum()))
    if by_season:
        signs = {}
        for s in np.unique(d["season"]):
            m = d["season"] == s
            signs[int(s)] = estimate(d["y"][m], d["w"][m], X[m], d["quarter"][m], d["game"][m])[0]
        out["by_season"] = signs
    return out


def bh(p, q):
    p = np.asarray(p)
    order = np.argsort(p)
    ranked = p[order] * len(p) / (np.arange(len(p)) + 1)
    passed = np.zeros(len(p), bool)
    below = np.flatnonzero(ranked <= q)
    if len(below):
        passed[order[:below.max() + 1]] = True
    return passed


# ---- within-player checks --------------------------------------------------------------------
def within_player(frame, tables, era, c, event, years):
    """The first type's own event rate with vs without a teammate of the second type (and the reverse)."""
    g = legacy.matchups()
    kind, a, b = c
    f = frame[frame.season.between(*years)]
    rows = f.row.to_numpy()
    pids = np.asarray(g["pids"][rows])
    att, mk = np.asarray(g["loc_attempt"][rows]), np.asarray(g["loc_make"][rows])
    ok = np.asarray(g["location_observed"][rows]) & np.asarray(g["fga_observed"][rows])
    if event == "three_fg":
        num, den = mk[..., 4:].sum(-1), att[..., 4:].sum(-1)
    elif event == "rim_fg":
        num, den = mk[..., 0], att[..., 0]
    elif event == "three_share":
        num, den = att[..., 4:].sum(-1), att.sum(-1)
    else:
        num, den = att[..., 0], att.sum(-1)
    den = den * ok[:, None]
    out = {}
    for first, second in ((a, b), (b, a)) if a != b else ((a, b),):
        t1 = np.zeros(pids.shape, bool)
        t2 = np.zeros(pids.shape, bool)
        for tag in f.origin.unique():
            m = (f.origin == tag).to_numpy()
            t = tables[tag]
            t1[m] = t[first].reindex(pids[m].ravel()).to_numpy().reshape(-1, 5)
            t2[m] = t[second].reindex(pids[m].ravel()).to_numpy().reshape(-1, 5)
        partners = t2.sum(1, keepdims=True) - (t1 & t2)            # teammates of the second type, excluding self
        sel = t1 & (den > 0)
        r, s = np.nonzero(sel)
        rate = 100 * num[r, s] / den[r, s]
        w = den[r, s].astype(float)
        x = (partners[r, 0] > 0).astype(float) if partners.shape[1] == 1 else (partners[r, s] > 0).astype(float)
        key = pd.factorize(pd.Series(pids[r, s]).astype(str) + "|" + f.origin.to_numpy()[r])[0]
        game = pd.factorize(f.game_id.to_numpy()[r])[0]
        yc, xc = centered(rate, key, w), centered(x, key, w)
        coef, se = estimate(yc, w, xc[:, None], key, game)
        out[f"{first} own {event}, with vs without {second}"] = dict(coef=coef, se=se, n=int(len(r)),
                                                                     share_with=float(np.average(x, weights=w)))
    return out


# ---- main ------------------------------------------------------------------------------------
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bench, era = residuals(False), residuals(True)
    fb, tables_b = features(bench, False)
    fe, tables_e = features(era, True)
    results, lines = {}, []
    sanity = None
    for family in FAMILIES:
        disc = window_data(bench, fb, family, WINDOWS["discovery"])
        conf = window_data(bench, fb, family, WINDOWS["confirmation"])
        repl = window_data(era, fe, family, WINDOWS["replication"])
        rows = []
        for c in CANDIDATES:
            r = test(disc, c)
            r["p"] = float(2 * stats.norm.sf(abs(r["coef"] / r["se"]))) if np.isfinite(r["se"]) and r["se"] > 0 else np.nan
            rows.append(dict(candidate=name(c), kind=c[0], **r))
        t = pd.DataFrame(rows)
        t["p_filled"] = t.p.fillna(1.)
        t["bh"] = bh(t.p_filled.to_numpy(), Q)
        t["rank"] = t.p_filled.rank(method="first").astype(int)
        t["mde"] = 2.8 * t.se
        if family == "points":
            sanity = t[t.candidate == "D_small x D_rim"].iloc[0].to_dict()
        chosen = t[t.bh].sort_values("p").head(K)
        confirmed = []
        for _, r in chosen.iterrows():
            c = next(x for x in CANDIDATES if name(x) == r.candidate)
            sign = np.sign(r.coef)
            cr = test(conf, c, by_season=True)
            cr["p_one"] = float(stats.norm.sf(sign * cr["coef"] / cr["se"]))
            cr["seasons_same_sign"] = int(sum(np.sign(v) == sign for v in cr["by_season"].values()))
            rr = test(repl, c)
            rr["p_one"] = float(stats.norm.sf(sign * rr["coef"] / rr["se"])) if np.isfinite(rr["se"]) and rr["se"] > 0 else np.nan
            confirmed.append(dict(candidate=r.candidate, kind=r.kind, discovery=dict(coef=r.coef, se=r.se, p=r.p),
                                  confirmation=cr, replication=rr))
        order = sorted(range(len(confirmed)), key=lambda i: confirmed[i]["confirmation"]["p_one"])
        running = 0.
        for j, i in enumerate(order):
            running = max(running, min(1., (len(order) - j) * confirmed[i]["confirmation"]["p_one"]))
            c = confirmed[i]
            c["holm"] = running
            held = c["holm"] < HOLM_ALPHA
            rp = c["replication"]["p_one"]
            rsign = np.sign(c["replication"]["coef"]) == np.sign(c["discovery"]["coef"])
            c["label"] = ("held up across eras" if held and rp < .05 else "held up (era: same sign)" if held and rsign
                          else "held up (era: reverses)" if held else "discovery-only")
        for c in confirmed:
            kind, a, b = next(x for x in CANDIDATES if name(x) == c["candidate"])
            if c["label"].startswith("held up") and kind == "offense" and family in SHOT_EVENTS:
                c["within_player"] = {"2016-2026": within_player(bench, tables_b, False, (kind, a, b), family, (2016, 2026))}
        t.drop(columns="p_filled").to_csv(OUT / f"discovery_{family}.csv", index=False)
        results[family] = dict(n_bh=int(t.bh.sum()), mde_discovery=float(t.mde.median()),
                               mde_confirmation=float(np.median([c["confirmation"]["se"] * 2.8 for c in confirmed])) if confirmed else None,
                               confirmed=confirmed, top10=t.sort_values("p_filled").head(10)[["candidate", "coef", "se", "p", "bh"]].to_dict("records"))
        lines.append(f"\n== {family}: {int(t.bh.sum())} of {len(t)} pass BH (q={Q}) in discovery; median MDE {t.mde.median():.2f}")
        for c in confirmed:
            d, cf, rp = c["discovery"], c["confirmation"], c["replication"]
            lines.append(f"  {c['candidate']:<28} disc {d['coef']:+.2f} ({d['se']:.2f}, p {d['p']:.4f}) | conf {cf['coef']:+.2f} "
                         f"({cf['se']:.2f}, one-sided p {cf['p_one']:.4f}, Holm {c['holm']:.3f}, {cf['seasons_same_sign']}/5 seasons) | "
                         f"era {rp['coef']:+.2f} ({rp['se']:.2f}, p {rp['p_one']:.4f}) -> {c['label']}")
            for k, v in c.get("within_player", {}).get("2016-2026", {}).items():
                lines.append(f"      within-player: {k}: {v['coef']:+.2f} ({v['se']:.2f}), n={v['n']}, share with {v['share_with']:.2f}")
    lines.insert(0, f"Sanity check, points, D_small x D_rim in discovery: coef {sanity['coef']:+.2f} (SE {sanity['se']:.2f}), "
                    f"p {sanity['p']:.4f}, rank {sanity['rank']} of {len(CANDIDATES)}, BH {'pass' if sanity['bh'] else 'fail'}")
    text = "\n".join(lines)
    (OUT / "report.txt").write_text(text)
    (OUT / "result.json").write_text(json.dumps(dict(sanity=sanity, families=results), indent=1, default=float))
    print(text)


if __name__ == "__main__":
    main()
