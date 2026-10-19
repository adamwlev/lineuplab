"""Why the capacity law did not help in 2006-2013 (post hoc, exploratory; not the registered result).

Reads the era backtest's saved fits and forecasts (scripts/era_run.py); never
writes into its output. For every scored quarter (2007-2013) and each seed
complete for both arms:

- the calibrated forecast exactly as scripts/era_score.py builds it;
- the checkpoint-mixture event ledger, re-run from the saved checkpoints, and
  the same ledger with every defensive path off (offense against a neutral
  defense). The rebuilt points must match the saved forecast;
- row composition: defensive and offensive bigs (82 in or taller), offensive
  shooters and the best passer from origin-dated states, and how familiar the
  defensive five is (possessions in the five years before the origin; first
  game in the quarter or not).

Per-origin rows are cached in OUT/rows_s<seeds>/<tag>.pkl (resumable).

    PYTHONPATH=. python -u scripts/era_diagnostics.py [--seeds 17 23]            # build rows
    PYTHONPATH=. python -u scripts/era_diagnostics.py [--seeds 17 23] --analyze  # tables
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

sys.path.insert(0, str(Path(__file__).parent))
from era_run import ARMS, SEEDS, STORE, EraRows, case_dir, origins  # noqa: E402
from era_score import BIG, FIRST_SCORED, league_at, native  # noqa: E402

from lineups import db, evaluate, legacy, paths  # noqa: E402
from lineups.evaluate import FIVE  # noqa: E402
from lineups.features import Store  # noqa: E402
from lineups.model import EventModel, average_ledgers  # noqa: E402
from lineups.train import game_batches  # noqa: E402

OUT = paths.CACHE / "era_diagnostics_2026_10_12"
LOCATIONS = ("rim", "paint", "mid", "longmid", "c3", "ab3")
VALUES = np.array([2., 2., 2., 2., 3., 3.])
SHOOTER = 3.      # 3PA per 100 own opportunities: a perimeter threat
LOOKBACK = 5 * 365


def checkpoint_models(tag, arm, seed):
    fit = torch.load(case_dir(tag, arm, seed) / "fit.pt", map_location="cpu", weights_only=False)
    offense = EventModel.offense_only(seed)
    offense.load_state_dict(fit["offense_final"])
    models = []
    for state in fit["checkpoints"]:
        m = EventModel.from_offense(offense, seed, ARMS[arm])
        m.load_state_dict(state)
        models.append(m.eval())
    return models


def team(pred):
    """Per-possession team ledger from a (mixture) prediction."""
    s = lambda v: v.double().sum(1).numpy()
    attempts, makes = pred.expected_attempts.double().sum(1).numpy(), pred.expected_makes.double().sum(1).numpy()
    out = dict(points=pred.points100.double().numpy() / 100, fga=s(pred.fga), fta=s(pred.fta), tov=s(pred.turnover),
               ftm=s(pred.fta * pred.ft_make), orb=s(pred.player_orb), live=pred.live.double().numpy())
    out |= {f"att_{x}": attempts[:, i] for i, x in enumerate(LOCATIONS)}
    out |= {f"make_{x}": makes[:, i] for i, x in enumerate(LOCATIONS)}
    return out


def ledgers(models, inputs, env, defense_off=False):
    with torch.no_grad():
        preds = []
        for m in models:
            m.defense_off = defense_off
            preds.append(m(inputs, env))
            m.defense_off = False
    return average_ledgers(preds)


def build_origin(o, data, store, g, seeds, arms=ARMS):
    rows = np.sort(legacy.quarter_rows(o, g))
    normalizer, env = store.normalizer(o.tag, "final"), store.env(o.tag, "final")
    batches = list(game_batches(data.game, rows))
    inputs = [data.batch(ix, normalizer, origin_index=int(o.origin_index))[0] for ix in batches]
    order = np.argsort(np.concatenate(batches))
    frame = {}
    for arm in arms:
        acc = None
        for seed in seeds:
            models = checkpoint_models(o.tag, arm, seed)
            on = [team(ledgers(models, x, env)) for x in inputs]
            off = [ledgers(models, x, env, defense_off=True).points100.double().numpy() / 100 for x in inputs]
            cols = {k: np.concatenate([b[k] for b in on])[order] for k in on[0]}
            cols["points_neutral"] = np.concatenate(off)[order]
            ids, saved = native(o.tag, arm, seed)
            gap = np.abs(100 * cols["points"] - saved).max()
            if not np.array_equal(ids, rows) or gap > 1e-6:
                raise ValueError(f"rebuilt forecast differs from the saved one: {o.tag}/{arm}/s{seed} gap={gap}")
            acc = cols if acc is None else {k: acc[k] + cols[k] for k in acc}
        frame |= {f"{arm}_{k}": v / len(seeds) for k, v in acc.items()}
    return pd.DataFrame(frame).assign(row=rows)


def actual_ledger(g, rows):
    take = lambda k: np.asarray(g[k][rows]).astype(float)
    att, mk, rb = take("loc_attempt").sum(1), take("loc_make").sum(1), take("rebound")
    out = dict(possessions=take("possessions"), points_actual=take("points"), fga=take("fga").sum(1),
               fta=take("fta").sum(1), tov=take("turnover").sum(1), orb=rb[:, :5].sum(1), drb=rb[:, 5],
               observed=(np.asarray(g["fga_observed"][rows]) & np.asarray(g["fta_observed"][rows])
                         & np.asarray(g["location_observed"][rows])))
    # Made free throws: points minus field-goal points.
    out["ftm"] = out["points_actual"] - mk @ VALUES
    out |= {f"att_{x}": att[:, i] for i, x in enumerate(LOCATIONS)}
    out |= {f"make_{x}": mk[:, i] for i, x in enumerate(LOCATIONS)}
    return pd.DataFrame({k + ("" if k in ("possessions", "points_actual", "observed") else "_actual"): v
                         for k, v in out.items()})


def composition(o, rows, g, store, heights):
    off, de = np.asarray(g["pids"][rows]).astype(np.int64), np.asarray(g["defense"][rows]).astype(np.int64)
    h = lambda p: heights.reindex(p.ravel()).to_numpy().reshape(-1, 5)
    base = store.offense(off, origin_index=int(o.origin_index))["base"].astype(float)
    loc = np.exp(base[..., 3:9] - base[..., 3:9].max(-1, keepdims=True))
    loc /= loc.sum(-1, keepdims=True)
    three = 100 * np.exp(np.clip(base[..., 0], -12, 4)) * loc[..., 4:].sum(-1)
    assist = 100 * np.exp(np.clip(base[..., 16], -12, 4))
    off_h, def_h = h(off), h(de)
    # Familiarity of the exact defensive five before the origin, and its first game in the quarter.
    start = legacy.day(o.start)
    date = np.asarray(g["date"])
    prior = np.flatnonzero((date < start) & (date >= start - LOOKBACK))
    key = lambda fives: pd.Series([tuple(r) for r in np.sort(fives, 1)])
    prior_poss = pd.Series(np.asarray(g["possessions"][prior], float)).groupby(key(np.asarray(g["defense"][prior]))).sum()
    k = key(de)
    games = pd.DataFrame(dict(k=k, game=np.asarray(g["game_id"][rows]), date=date[rows]))
    first_game = games.sort_values(["date", "game"], kind="stable").groupby("k").game.transform("first")
    return pd.DataFrame(dict(
        def_bigs=(def_h >= BIG).sum(1), off_bigs=(off_h >= BIG).sum(1),
        def_height=def_h.mean(1), off_height=off_h.mean(1),
        off_shooters=(three >= SHOOTER).sum(1), off_nonspacing_bigs=((off_h >= BIG) & (three < 1.)).sum(1),
        off_best_passer=assist.max(1),
        def_prior_poss=k.map(prior_poss).fillna(0.).to_numpy(),
        def_first_game=(games.game.to_numpy() == first_game.to_numpy())))


def build(seeds, only=None, arms=ARMS):
    """Per-origin rows; --arms R (2026-10-16, the refresh) builds arm R only: the discovery replication reads
    only R's columns."""
    folder = OUT / ("rows_s" + "_".join(map(str, seeds)))
    folder.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    store = Store(STORE)
    g = legacy.matchups()
    data = EraRows(g, store)
    heights = db.heights()
    era = origins(store)
    history = {(a, s): [] for a in arms for s in seeds}
    for o in era.itertuples():
        rows = np.sort(legacy.quarter_rows(o, g))
        league = np.full(len(rows), league_at(g, legacy.day(o.start)))
        calibrated = {a: [] for a in arms}
        for a in arms:
            for s in seeds:
                ids, p = native(o.tag, a, s)
                h = pd.concat(history[(a, s)], ignore_index=True) if history[(a, s)] else None
                calibrated[a].append(evaluate.calibrate(evaluate.affine(h, o.start), p, league))
                frame = legacy.row_frame(ids, g)
                history[(a, s)].append(evaluate.history_cells(frame, p, league, o.stop))
        path = folder / f"{o.tag}.pkl"
        if o.season < FIRST_SCORED or path.exists() or (only and o.tag not in only):
            continue
        f = legacy.row_frame(rows, g)[["row", "game_id", "date"] + FIVE + legacy.DEFENSE]
        f = f.assign(season=int(o.season), origin=o.tag, league=league,
                     **{a: np.mean(calibrated[a], 0) for a in arms})
        f = pd.concat([f.reset_index(drop=True), actual_ledger(g, rows),
                       composition(o, rows, g, store, heights),
                       build_origin(o, data, store, g, seeds, arms).drop(columns="row")], axis=1)
        f.to_pickle(path)
        print("built", o.tag, len(f), flush=True)


# ---- analysis -----------------------------------------------------------------
def load(seeds):
    folder = OUT / ("rows_s" + "_".join(map(str, seeds)))
    f = pd.concat([pd.read_pickle(p) for p in sorted(folder.glob("*.pkl"))], ignore_index=True)
    f["actual"] = 100 * f.points_actual / f.possessions
    for a in ARMS:
        f[f"res_{a}"] = f.actual - f[a]
        f[f"def_effect_{a}"] = 100 * (f[f"{a}_points"] - f[f"{a}_points_neutral"])
        f[f"offense_{a}"] = 100 * f[f"{a}_points_neutral"]
    f["bigs3"] = np.select([f.def_bigs <= 1, f.def_bigs == 2], ["0-1", "2"], "3+")
    return f


def wmean(f, column):
    return float(np.average(f[column], weights=f.possessions))


def by(f, keys, columns):
    """Possession-weighted means with season-level SEs for each group."""
    out = []
    for key, s in f.groupby(keys):
        rec = dict(zip(keys if isinstance(keys, list) else [keys], key if isinstance(key, tuple) else (key,)))
        rec["possessions"] = float(s.possessions.sum())
        for c in columns:
            per = s.groupby("season").apply(lambda t: wmean(t, c), include_groups=False)
            rec[c] = wmean(s, c)
            rec[c + "_se"] = float(per.std(ddof=1) / np.sqrt(len(per))) if len(per) > 1 else np.nan
        out.append(rec)
    return pd.DataFrame(out)


def gradient(f, column, mask=None):
    """3+ minus 0-1 defensive bigs, overall and its season SE."""
    f = f if mask is None else f[mask]
    g = lambda t: wmean(t[t.bigs3 == "3+"], column) - wmean(t[t.bigs3 == "0-1"], column)
    per = f.groupby("season").apply(g, include_groups=False)
    return float(g(f)), float(per.std(ddof=1) / np.sqrt(len(per)))


def channels(f, arm):
    """Accounting decomposition of actual minus native forecast points per 100 (observed rows only).

    volume (FGA per possession), shot mix, conversion by location and free
    throws, in that order (telescoping, so the parts sum to the total)."""
    f = f[f.observed]
    n = f.possessions.to_numpy(float)
    act = lambda k: float(f[f"{k}_actual"].sum() / n.sum())
    pred = lambda k: float((f[f"{arm}_{k}"] * n).sum() / n.sum())
    F0, F1 = pred("fga"), act("fga")
    a0 = np.array([pred(f"att_{x}") for x in LOCATIONS]); a1 = np.array([act(f"att_{x}") for x in LOCATIONS])
    m0 = np.array([pred(f"make_{x}") for x in LOCATIONS]) / a0; m1 = np.array([act(f"make_{x}") for x in LOCATIONS]) / a1
    s0, s1 = a0 / a0.sum(), a1 / a1.sum()
    T0, T1 = pred("ftm"), act("ftm")
    parts = dict(volume=(F1 - F0) * (s0 * m0 * VALUES).sum(), mix=F1 * ((s1 - s0) * m0 * VALUES).sum(),
                 conversion=F1 * (s1 * (m1 - m0) * VALUES).sum(), free_throws=T1 - T0)
    rec = {k: 100 * v for k, v in parts.items()}
    rec["total"] = sum(rec.values())
    rec["check"] = 100 * (float(f.points_actual.sum() / n.sum()) - pred("points")) - rec["total"]
    orb0, live0 = pred("orb"), pred("live")
    rec |= dict(tov_actual=100 * act("tov"), tov_pred=100 * pred("tov"), fta_actual=100 * act("fta"),
                fta_pred=100 * pred("fta"), orb_pct_actual=act("orb") / (act("orb") + act("drb")),
                orb_pct_pred=orb0 / live0)
    rec |= {f"share_{x}_diff": 100 * (s1[i] - s0[i]) for i, x in enumerate(LOCATIONS)}
    rec |= {f"fg_{x}_diff": 100 * (m1[i] - m0[i]) for i, x in enumerate(LOCATIONS)}
    return rec


def analyze(seeds):
    f = load(seeds)
    folder = OUT / ("tables_s" + "_".join(map(str, seeds)))
    folder.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 220, "display.max_columns", 40, "display.precision", 2)
    res = ["res_R", "res_C"]
    tables = {}
    tables["by_def_bigs"] = by(f.assign(db=f.def_bigs.clip(upper=3)), "db", res + ["def_effect_R", "def_effect_C"])
    tables["grid_off_bigs"] = by(f.assign(ob=np.select([f.off_bigs <= 1, f.off_bigs == 2], ["0-1", "2"], "3+")),
                                 ["bigs3", "ob"], res)
    tables["grid_shooters"] = by(f.assign(sh=f.off_shooters.clip(upper=3)), ["bigs3", "sh"], res)
    fam = pd.cut(f.def_prior_poss, [-1, 0, 199, np.inf], labels=["new", "1-199", "200+"])
    tables["familiarity"] = by(f.assign(fam=fam.astype(str)), ["bigs3", "fam"], res)
    tables["first_game"] = by(f, ["bigs3", "def_first_game"], res)
    grads = {}
    for a in ARMS:
        grads[f"{a} all"] = gradient(f, f"res_{a}")
        grads[f"{a} first game only"] = gradient(f, f"res_{a}", f.def_first_game)
        grads[f"{a} later games"] = gradient(f, f"res_{a}", ~f.def_first_game)
        grads[f"{a} new five (0 prior poss)"] = gradient(f, f"res_{a}", f.def_prior_poss == 0)
        grads[f"{a} model defense effect"] = gradient(f, f"def_effect_{a}")
    f["CmR"] = f.C - f.R
    grads["C-R forecast"] = gradient(f, "CmR")
    tables["gradients"] = pd.DataFrame([dict(what=k, estimate=v[0], season_se=v[1]) for k, v in grads.items()])

    # Dispersion: does the residual follow the model's own defense effect within quarter?
    disp = []
    for a in ARMS:
        x = f[[f"def_effect_{a}", f"offense_{a}"]].copy()
        x = x - x.groupby(f.origin).transform("mean")
        y = f[f"res_{a}"] - f[f"res_{a}"].groupby(f.origin).transform("mean")
        w = f.possessions.to_numpy(float)
        X = np.c_[x.to_numpy(float), np.ones(len(x))]
        sw = np.sqrt(w)[:, None]
        beta = np.linalg.lstsq(X * sw, y.to_numpy(float) * sw[:, 0], rcond=None)[0]
        per = []
        for season, idx in f.groupby("season").groups.items():
            i = f.index.get_indexer(idx)
            per.append(np.linalg.lstsq(X[i] * sw[i], y.to_numpy(float)[i] * sw[i, 0], rcond=None)[0][:2])
        per = np.array(per)
        adjusted = f[f"res_{a}"] - beta[0] * f[f"def_effect_{a}"] - beta[1] * f[f"offense_{a}"]
        g = gradient(f.assign(adj=adjusted), "adj")
        disp.append(dict(arm=a, defense_slope=beta[0], defense_slope_se=per[:, 0].std(ddof=1) / np.sqrt(len(per)),
                         offense_slope=beta[1], offense_slope_se=per[:, 1].std(ddof=1) / np.sqrt(len(per)),
                         gradient_after=g[0], gradient_after_se=g[1]))
    tables["dispersion"] = pd.DataFrame(disp)

    rows = []
    for grp, s in f.groupby("bigs3"):
        for a in ARMS:
            rows.append(dict(bigs=grp, arm=a, **channels(s, a)))
    ch = pd.DataFrame(rows)
    tables["channels"] = ch
    for name, t in tables.items():
        t.to_csv(folder / f"{name}.csv", index=False)
        print(f"\n== {name}\n{t.to_string(index=False)}", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", type=int, nargs="+", default=None)
    p.add_argument("--only", nargs="+", default=None)
    p.add_argument("--analyze", action="store_true", help="tables from the cached rows")
    p.add_argument("--arms", nargs="+", choices=list(ARMS), default=list(ARMS))   # R first, as the saved rows
    a = p.parse_args()
    seeds = a.seeds or [s for s in SEEDS if all((case_dir(t, arm, s) / "complete.json").exists()
                                               for t in origins().tag for arm in a.arms)]
    print("seeds", seeds, flush=True)
    analyze(seeds) if a.analyze else build(seeds, a.only, tuple(a.arms))
