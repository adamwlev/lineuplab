"""Synergy hypotheses H1-H5 (protocol: reports/synergy_hypotheses_protocol_2026_10_12.md; exploratory).

Residual = actual points per 100 minus the best additive approximation of the
calibrated network's forecast (one value per player per side, fitted within the
quarter to the forecasts; scripts/synergy_check.py). Each hypothesis regresses
the residual on two main effects and their interaction, centered within
quarter, possession-weighted. It reports the coefficient by season (mean ± season
SE) and the pooled coefficient. Profiles are prior-only origin states; percentile
thresholds are taken among the players appearing in the quarter's rows.

    PYTHONPATH=.:scripts python -u scripts/synergy_hypotheses.py

Output: experiments/cache/synergy_hypotheses_2026_10_12/ (possession cache, tables, report.txt).
"""
import json
from contextlib import closing

import numpy as np
import pandas as pd
from scipy import stats

import era_run
from lineups import db, legacy, paths
from lineups.evaluate import FIVE
from lineups.features import Store
from lineups.legacy import DEFENSE
from lineups.schedule import season_labels
from synergy_check import additive_projection

OUT = paths.CACHE / "synergy_hypotheses_2026_10_12"
ROWS = paths.CACHE / "ensemble_check_2026_10_12"
SHRINK, MIN_PRIOR_POSSESSIONS, PRIOR_SEASONS = 300., 500., 3
SMALL, TALL = 75, 81
PREDICTED = dict(H1=-1, H2=1, H3=1, H4=-1, H5=1)


# ---- possessions and transition profiles (H3) -------------------------------------
def possessions():
    path = OUT / "possessions.pkl"
    if path.exists():
        return pd.read_pickle(path)
    ids = [f"{side}_player_{i}_id" for side in ("away", "home") for i in range(1, 6)]
    query = f"""select p.game_id, p.quarter, p.time_left_start, p.id, p.away_team_ball, p.turnover,
                       p.points_scored, p.scorer, {", ".join("p." + c for c in ids)},
                       coalesce(position('steal by' in p.texts) > 0, false) as steal, g.game_date
                from {paths.POSSESSIONS_TABLE} p join nba.games g on g.id = p.game_id
                order by p.game_id, p.quarter, p.time_left_start desc, p.id"""
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute(query)
        cols = [d[0] for d in cur.description]
        frame = pd.DataFrame(cur.fetchall(), columns=cols)
    prev = frame.shift(1)
    same = (prev.game_id == frame.game_id) & (prev.quarter == frame.quarter)
    frame["post_steal"] = (same & prev.turnover.fillna(False).astype(bool) & prev.steal.fillna(False).astype(bool)
                           & (prev.away_team_ball != frame.away_team_ball)).to_numpy()
    away = frame[[f"away_player_{i}_id" for i in range(1, 6)]].to_numpy()
    home = frame[[f"home_player_{i}_id" for i in range(1, 6)]].to_numpy()
    offense = np.where(frame.away_team_ball.to_numpy()[:, None], away, home)
    out = pd.DataFrame(np.sort(offense, 1), columns=FIVE)
    out["date"] = pd.to_datetime(frame.game_date).to_numpy()
    out["season"] = season_labels(out.date)
    out["points"] = frame.points_scored.fillna(0).to_numpy(float)
    out["scorer"] = frame.scorer.fillna(-1).to_numpy(np.int64)
    out["post_steal"] = frame.post_steal.to_numpy()
    out["game_id"] = frame.game_id.to_numpy()
    OUT.mkdir(parents=True, exist_ok=True)
    out.to_pickle(path)
    return out


def player_seasons(poss):
    """Per (pid, season): on-floor offensive possessions and own points, after a steal and otherwise."""
    pids = poss[FIVE].to_numpy().ravel()
    n = len(poss)
    flag = np.repeat(poss.post_steal.to_numpy(), 5)
    own = np.repeat(poss.scorer.to_numpy(), 5) == pids
    pts = np.where(own, np.repeat(poss.points.to_numpy(), 5), 0.)
    f = pd.DataFrame(dict(pid=pids, season=np.repeat(poss.season.to_numpy(), 5), ps=flag, pts=pts))
    g = f.groupby(["pid", "season", "ps"]).agg(n=("pts", "size"), pts=("pts", "sum")).unstack("ps", fill_value=0)
    g.columns = [f"{a}_{'ps' if b else 'other'}" for a, b in g.columns]
    return g.reset_index()


def finisher_lift(seasons, season):
    """Shrunk transition lift from the PRIOR_SEASONS seasons before `season`."""
    s = seasons[(seasons.season < season) & (seasons.season >= season - PRIOR_SEASONS)]
    g = s.groupby("pid")[["n_ps", "pts_ps", "n_other", "pts_other"]].sum()
    lift = g.pts_ps / g.n_ps.clip(lower=1) - g.pts_other / g.n_other.clip(lower=1)
    shrunk = lift * g.n_ps / (g.n_ps + SHRINK)
    return shrunk[(g.n_ps + g.n_other) >= MIN_PRIOR_POSSESSIONS]


# ---- player profiles -----------------------------------------------------------
def profiles(store, origin_index, pids):
    off = store.offense(pids, origin_index=origin_index)["base"].astype(float)
    de = store.defense(pids, origin_index=origin_index).astype(float)
    e = lambda k: np.exp(np.clip(off[:, k], -12, 4))
    loc = np.exp(off[:, 3:9] - off[:, 3:9].max(1, keepdims=True))
    loc /= loc.sum(1, keepdims=True)
    height = store.players["height"][pids]
    return pd.DataFrame(dict(pid=pids, height=height, usage=e(0) + .44 * e(1) + e(2), three_share=loc[:, 4:].sum(1),
                             rim_share=loc[:, 0], three_rate=e(0) * loc[:, 4:].sum(1), assist=e(16),
                             assisted=1 / (1 + np.exp(-off[:, 17])), steal=de[:, 0], block=de[:, 1])).set_index("pid")


def flags(p, lift):
    q = lambda col, x: p[col].quantile(x)
    out = pd.DataFrame(index=p.index)
    out["small"] = p.height <= SMALL
    out["anchor"] = (p.height >= TALL) & (p.block >= q("block", .9))
    out["specialist"] = (p.three_share >= q("three_share", .75)) & (p.assisted >= q("assisted", .75)) & (p.assist <= q("assist", .5))
    out["playmaker"] = p.assist >= q("assist", .9)
    out["ball_dominant"] = p.usage >= q("usage", .9)
    out["rim_runner"] = (p.height >= TALL) & (p.three_share <= q("three_share", .1)) & (p.rim_share >= q("rim_share", .75))
    out["shooter"] = p.three_rate >= q("three_rate", .6)
    known = lift.reindex(p.index)
    eligible = known.dropna()
    out["finisher"] = known >= (eligible.quantile(.9) if len(eligible) else np.inf)
    out["steal"] = p.steal
    return out


# ---- rows ---------------------------------------------------------------------------
def quarter_rows(era):
    f = pd.read_pickle(ROWS / ("era.pkl" if era else "benchmark.pkl"))
    f[FIVE] = np.sort(f[FIVE].to_numpy(), 1)
    f[DEFENSE] = np.sort(f[DEFENSE].to_numpy(), 1)
    store = Store(era_run.STORE) if era else Store()
    schedule = (era_run.origins() if era else legacy.origins()).set_index("tag")
    seasons = player_seasons(possessions())
    out = []
    for tag, q in f.groupby("origin", sort=False):
        q = q.copy()
        q["A"] = additive_projection(q)
        q["actual"] = 100 * q.points / q.possessions
        q["res"] = q.actual - q.A
        pids = np.unique(np.r_[q[FIVE].to_numpy().ravel(), q[DEFENSE].to_numpy().ravel()])
        fl = flags(profiles(store, int(schedule.loc[tag, "origin_index"]), pids), finisher_lift(seasons, int(q.season.iloc[0])))
        off = {k: fl[k].reindex(q[FIVE].to_numpy().ravel()).to_numpy().reshape(-1, 5) for k in fl}
        de = {k: fl[k].reindex(q[DEFENSE].to_numpy().ravel()).to_numpy().reshape(-1, 5) for k in fl}
        q["n_small"] = de["small"].sum(1)
        q["anchor"] = de["anchor"].any(1).astype(float)
        q["n_spec"] = off["specialist"].sum(1)
        q["playmaker"] = off["playmaker"].any(1).astype(float)
        q["n_fin"] = off["finisher"].astype(float).sum(1)
        sp = off["steal"].astype(float).sum(1)
        w = q.possessions.to_numpy(float)
        q["steal_pressure"] = (sp - np.average(sp, weights=w)) / np.sqrt(np.average((sp - np.average(sp, weights=w)) ** 2, weights=w))
        q["n_bd"] = off["ball_dominant"].sum(1)
        q["rim_runner"] = off["rim_runner"].any(1).astype(float)
        q["n_shoot"] = off["shooter"].sum(1)
        out.append(q)
        print(tag, flush=True)
    return pd.concat(out, ignore_index=True)


# ---- tests ----------------------------------------------------------------------------
def design(f, h):
    """Columns (main effects..., tested term) for hypothesis h; the residual sign is points allowed for H1."""
    if h == "H1":
        return dict(n_small=f.n_small, anchor=f.anchor, interaction=f.n_small * f.anchor)
    if h == "H2":
        return dict(n_spec=f.n_spec, playmaker=f.playmaker, interaction=f.n_spec * f.playmaker)
    if h == "H3":
        return dict(n_fin=f.n_fin, steal_pressure=f.steal_pressure, interaction=f.n_fin * f.steal_pressure)
    if h == "H4":
        return dict(any_bd=(f.n_bd >= 1).astype(float), interaction=(f.n_bd >= 2).astype(float))
    if h == "H5":
        return dict(rim_runner=f.rim_runner, n_shoot=f.n_shoot, interaction=f.rim_runner * f.n_shoot)


def fit(f, h):
    X = pd.DataFrame(design(f, h))
    w = f.possessions.to_numpy(float)
    cols = list(X.columns)
    data = pd.concat([X, f[["res", "origin", "possessions"]]], axis=1)
    for c in cols + ["res"]:
        data[c] = data[c] - data.groupby("origin")[c].transform(lambda s: np.average(s, weights=data.loc[s.index, "possessions"]))
    A = data[cols].to_numpy(float)
    return np.linalg.lstsq(A * np.sqrt(w)[:, None], data.res.to_numpy() * np.sqrt(w), rcond=None)[0][-1]


def test(f, h):
    per = {s: fit(g, h) for s, g in f.groupby("season")}
    v = np.array(list(per.values()))
    t = v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))
    return dict(pooled=float(fit(f, h)), season_mean=float(v.mean()), season_se=float(v.std(ddof=1) / np.sqrt(len(v))),
                p=float(2 * stats.t.sf(abs(t), len(v) - 1)), predicted_sign=int((np.sign(v) == PREDICTED[h]).sum()),
                seasons=len(v), per_season={int(k): float(x) for k, x in per.items()})


def group_table(f, h):
    c = f.copy()
    c["res_c"] = c.res - c.groupby("origin").res.transform(lambda s: np.average(s, weights=c.loc[s.index, "possessions"]))
    keys = dict(H1=[c.n_small.clip(upper=2), c.anchor], H2=[c.n_spec.clip(upper=2), c.playmaker],
                H3=[c.n_fin.clip(upper=1), pd.qcut(c.steal_pressure, 3, labels=["low", "mid", "high"])],
                H4=[c.n_bd.clip(upper=2)], H5=[c.rim_runner, c.n_shoot.clip(lower=1, upper=3)])[h]
    return c.groupby(keys, observed=True).apply(lambda g: pd.Series(dict(
        possessions=g.possessions.sum(), residual=np.average(g.res_c, weights=g.possessions))), include_groups=False)


def transition_mechanism(f_quarters):
    """Secondary H3: post-steal and other points per possession of offense fives, by finisher count (2016-2026)."""
    poss = possessions()
    sched = legacy.origins()
    poss = poss[(poss.date >= sched.start.min()) & (poss.date < sched.stop.max())].copy()
    poss["origin"] = pd.cut(poss.date, bins=list(sched.start) + [sched.stop.max()], right=False, labels=list(sched.tag)).astype(str)
    fin = f_quarters.groupby(["origin", *FIVE]).n_fin.first()
    poss = poss.join(fin, on=["origin", *FIVE], how="inner")
    rows = []
    for k, g in poss.groupby(poss.n_fin.clip(upper=2)):
        ps, other = g[g.post_steal], g[~g.post_steal]
        rows.append(dict(finishers=int(k), post_steal_possessions=len(ps), post_steal_ppp=ps.points.mean(),
                         other_ppp=other.points.mean(), lift=ps.points.mean() - other.points.mean()))
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results, lines = {}, []
    frames = {}
    for era in (False, True):
        name = "replication 2007-2013" if era else "primary 2016-2026"
        path = OUT / f"rows_{'era' if era else 'benchmark'}.pkl"
        frames[era] = pd.read_pickle(path) if path.exists() else quarter_rows(era)
        frames[era].to_pickle(path)
        results[name] = {h: test(frames[era], h) for h in PREDICTED}
    primary = results["primary 2016-2026"]
    order = sorted(PREDICTED, key=lambda h: primary[h]["p"])
    holm = {}
    running = 0.
    for i, h in enumerate(order):
        running = max(running, min(1., (len(order) - i) * primary[h]["p"]))
        holm[h] = running
    for h in PREDICTED:
        p, r = primary[h], results["replication 2007-2013"][h]
        sign_ok = np.sign(p["pooled"]) == PREDICTED[h]
        verdict = ("supported" if sign_ok and holm[h] < .05 and np.sign(r["pooled"]) == PREDICTED[h]
                   else "suggestive" if sign_ok and p["p"] < .05 else "no evidence at this power")
        primary[h]["holm"], primary[h]["verdict"] = holm[h], verdict
        lines.append(f"{h}: interaction {p['pooled']:+.2f} pts/100 (season mean {p['season_mean']:+.2f} ± {p['season_se']:.2f}, "
                     f"p {p['p']:.3f}, Holm {holm[h]:.3f}, predicted sign in {p['predicted_sign']}/{p['seasons']} seasons); "
                     f"replication {r['pooled']:+.2f} ({r['season_mean']:+.2f} ± {r['season_se']:.2f}, {r['predicted_sign']}/{r['seasons']}) -> {verdict}")
    for era in (False, True):
        lines.append(f"\n== group residuals, {'2007-2013' if era else '2016-2026'} (points per 100, within quarter)")
        for h in PREDICTED:
            lines.append(f"-- {h}\n" + group_table(frames[era], h).round(2).to_string())
    mech = transition_mechanism(frames[False])
    lines.append("\n== H3 mechanism, 2016-2026: points per possession after a steal vs otherwise, by finishers in the five\n"
                 + mech.round(3).to_string(index=False))
    text = "\n".join(lines)
    (OUT / "report.txt").write_text(text)
    (OUT / "result.json").write_text(json.dumps(results, indent=1, default=float))
    print(text)


if __name__ == "__main__":
    main()
