"""Cross-era check (docs/CLOSEOUT.md, step 3; exploratory, decision-relevant).

The tool puts player-seasons from any era into one model. This measures what
that costs on real lineups with outcomes, in two directions:

    A  the release model (R, 2027q1; trained 2021-2026) forecasts 2007-2013
       quarters from era-store origin states; in-era baseline: the era
       backtest R forecasts on the same rows.
    B  the era 2013q4 R fits (trained 2008-2013) forecast 2016-2026 quarters
       from v16 origin states; in-era baseline: the saved v16 reference.

Every forecast is the calibrated neural model alone, mean of three seeds,
against the defenses actually faced. Two input rules, declared before scoring:

    as_was      the players' raw states, standardized by the model's normalizer
    translated  each raw coordinate shifted by (model-origin mean - player-origin
                mean), using the normalizers' means; the ledger's raw anchor
                (base, rebound prior) is shifted the same way

In both, capability banks are read at the player's own origin, and the
environment (budget, renewal, league capture, calibration) is the model's.

Decision rule (docs/CLOSEOUT.md): adopt `translated` if it beats `as_was` on
centered r² in both directions; otherwise `as_was`.

Primary metric: centered r² (within quarter) and within-quarter correlation on
broad offense-five cells (at least 50 possessions), by target season, with the
in-era baseline beside it. Secondary: transport excess error by the offense
five's composition distance from the model's own training support.

    PYTHONPATH=.:scripts python -u scripts/cross_era.py

Output: experiments/cache/cross_era_2026_10_12/.
"""
import json
import os
import time

import numpy as np
import pandas as pd
import torch

import era_run
from era_diagnostics import checkpoint_models
from era_score import league_at
from lineups import evaluate, legacy, paths, release
from lineups.evaluate import FIVE
from lineups.features import Store
from lineups.model import average_ledgers
from lineups.support import Support

OUT = paths.CACHE / "cross_era_2026_10_12"
BASELINES = paths.CACHE / "ensemble_check_2026_10_12"
MEANS = ("base_mean", "role_mean", "rebound_mean", "defense_mean", "offense_mean", "defense_bank_mean")
RULES = ("as_was", "translated")
CHUNK = 20000


def era_calibration(g, tag="2013q4"):
    """Per-seed prior-only affine for the era R fits at one origin (as scripts/era_score.py)."""
    history = {s: [] for s in era_run.SEEDS}
    target = None
    for o in era_run.origins().itertuples():
        if o.tag == tag:
            target = o
            break
        rows = legacy.row_frame(legacy.quarter_rows(o, g), g)
        league = np.full(len(rows), league_at(g, legacy.day(o.start)))
        for s in era_run.SEEDS:
            with np.load(era_run.case_dir(o.tag, "R", s) / "forecast.npz") as z:
                ids, p = z["row"], z["checkpoint_average"].astype(float)
            if not np.array_equal(ids, rows.row.to_numpy()):
                raise ValueError(f"row mismatch {o.tag}/s{s}")
            history[s].append(evaluate.history_cells(rows, p, league, o.stop))
    return {s: evaluate.affine(pd.concat(h, ignore_index=True), target.start) for s, h in history.items()}


def families(g):
    rel = release.Release(arms=("R",))
    era = Store(era_run.STORE)
    era_tag = "2013q4"
    era_index = int(era.schedule().query("tag == @era_tag").iloc[0].origin_index)
    rel_index = int(rel.store.schedule().query("tag == @release.ORIGIN").iloc[0].origin_index)
    calibration = era_calibration(g)
    era_league = league_at(g, legacy.day(era.schedule().query("tag == @era_tag").iloc[0].start))

    def era_calibrate(native):
        return np.mean([era_league + c["intercept"] + c["slope"] * (p - era_league)
                        for c, p in zip(calibration.values(), native)], 0)

    return dict(
        A=dict(models=[rel.models["R"][s] for s in release.SEEDS], store=rel.store, tag=release.ORIGIN,
               normalizer=rel.store.normalizer(release.ORIGIN, "final"), env=rel.store.env(release.ORIGIN, "final"),
               league_capture=float(rel.store.offense_origins["league"][rel_index]),
               calibrate=lambda native: rel.calibrate("R", native),
               targets=(era, era_run.origins().query("season >= 2007")), baseline="era"),
        B=dict(models=[checkpoint_models(era_tag, "R", s) for s in era_run.SEEDS], store=era, tag=era_tag,
               normalizer=era.normalizer(era_tag, "final"), env=era.env(era_tag, "final"),
               league_capture=float(era.offense_origins["league"][era_index]),
               calibrate=era_calibrate,
               targets=(Store(), legacy.origins().query("season >= 2016")), baseline="benchmark"))


def transported(fam, store, origin, offense, defense, rule):
    """Inputs for target rows: target-origin states, model normalizer (and translation)."""
    n_model, n_player = fam["normalizer"], store.normalizer(origin.tag, "final")
    n = dict(n_model) | ({k: n_player[k] for k in MEANS} if rule == "translated" else {})
    inputs = store.batch(offense, defense, None, n, origin_index=int(origin.origin_index),
                         query_day=int(n_player["cutoff_day"]))
    if rule == "translated":
        inputs["base"] = inputs["base"] + torch.as_tensor(n_model["base_mean"] - n_player["base_mean"],
                                                          dtype=torch.float32)
        shift = float(n_model["rebound_mean"][0] - n_player["rebound_mean"][0])
        p = inputs["rb_prior"].double().clamp(1e-6, 1 - 1e-6)
        inputs["rb_prior"] = torch.sigmoid(torch.logit(p) + shift).float()
    inputs["league_capture"] = torch.full_like(inputs["league_capture"], fam["league_capture"])
    return inputs


def forecast(fam, inputs):
    natives = []
    with torch.no_grad():
        for models in fam["models"]:
            natives.append(average_ledgers([m(inputs, fam["env"]) for m in models]).points100.numpy())
    return fam["calibrate"](np.asarray(natives, float))


def distance(support, inputs):
    x = inputs["msg"].double().numpy()
    z = np.concatenate([x.mean(1), x.std(1)], -1)
    d = support._distance(z, "offense")
    return d, np.searchsorted(support.reference["offense"]["distance"], d) / len(support.reference["offense"]["distance"])


def build(name, fam, g):
    path = OUT / f"{name}.pkl"
    if path.exists():
        return pd.read_pickle(path)
    support = Support(fam["store"], fam["tag"], g)
    store, schedule = fam["targets"]
    base = pd.read_pickle(BASELINES / f"{fam['baseline']}.pkl")[["origin", "row", "R"]].rename(columns=dict(R="baseline"))
    out = []
    for o in schedule.itertuples():
        tick = time.monotonic()
        f = legacy.row_frame(legacy.quarter_rows(o, g), g)
        offense, defense = f[FIVE].to_numpy(np.int64), f[legacy.DEFENSE].to_numpy(np.int64)
        cols = {r: [] for r in RULES} | {"distance": [], "percentile": []}
        for lo in range(0, len(f), CHUNK):
            sl = slice(lo, lo + CHUNK)
            for rule in RULES:
                inputs = transported(fam, store, o, offense[sl], defense[sl], rule)
                cols[rule].append(forecast(fam, inputs))
                if rule == "as_was":
                    d, pct = distance(support, inputs)
                    cols["distance"].append(d)
                    cols["percentile"].append(pct)
        f = f.assign(origin=o.tag, season=int(o.season), **{k: np.concatenate(v) for k, v in cols.items()})
        f = f.merge(base.query("origin == @o.tag"), on=["origin", "row"], how="left", validate="one_to_one")
        if f.baseline.isna().any():
            raise ValueError(f"baseline rows missing at {o.tag}")
        out.append(f)
        print(f"[{name}] {o.tag}: {len(f)} rows, {time.monotonic() - tick:.0f}s", flush=True)
    frame = pd.concat(out, ignore_index=True)
    frame.to_pickle(path)
    return frame


COLUMNS = ("baseline",) + RULES


def score(frame):
    """Per-season centered r², within-quarter correlation and cell distances."""
    recs, cell_frames = [], []
    for (tag, season), f in frame.groupby(["origin", "season"], sort=False):
        c = evaluate.cells(f, list(COLUMNS) + ["distance", "percentile"])
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS].assign(origin=tag, season=season)
        w, y = c.possessions.to_numpy(float), c.actual.to_numpy(float)
        yc = y - np.average(y, weights=w)
        for m in COLUMNS:
            p = c[m].to_numpy(float)
            e = y - p
            ec, pc = e - np.average(e, weights=w), p - np.average(p, weights=w)
            recs.append(dict(origin=tag, season=season, model=m, sse_c=w @ ec ** 2, sst=w @ yc ** 2,
                             syp=w @ (yc * pc), spp=w @ pc ** 2))
            c[f"err_{m}"] = ec
        cell_frames.append(c)
    t = pd.DataFrame(recs)
    agg = lambda g: pd.Series(dict(centered_r2=1 - g.sse_c.sum() / g.sst.sum(),
                                   correlation=g.syp.sum() / np.sqrt(g.sst.sum() * g.spp.sum())))
    per = t.groupby(["season", "model"]).apply(agg, include_groups=False).unstack("model")
    pooled = t.groupby("model").apply(agg, include_groups=False)
    return per, pooled, pd.concat(cell_frames, ignore_index=True)


def report(name, frame):
    per, pooled, cells = score(frame)
    lines = [f"== {name}: pooled", pooled.round(4).to_string(), "", "per season, centered r²",
             per["centered_r2"].round(4).to_string(), "", "per season, within-quarter correlation",
             per["correlation"].round(4).to_string(), ""]
    result = dict(pooled=pooled.to_dict(), per_season={k: per[k].to_dict() for k in ("centered_r2", "correlation")})
    contrasts = {}
    for a, b in (("as_was", "baseline"), ("translated", "baseline"), ("translated", "as_was")):
        d = per["centered_r2"][a] - per["centered_r2"][b]
        se = d.std(ddof=1) / np.sqrt(len(d))
        contrasts[f"{a}-{b}"] = dict(estimate=float(pooled.centered_r2[a] - pooled.centered_r2[b]),
                                     season_mean=float(d.mean()), season_se=float(se), positive=int((d > 0).sum()),
                                     seasons=len(d))
        lines.append(f"centered r² {a} - {b}: {pooled.centered_r2[a] - pooled.centered_r2[b]:+.4f} "
                     f"(season mean {d.mean():+.4f} ± {se:.4f}, {int((d > 0).sum())}/{len(d)})")
    result["contrasts"] = contrasts
    bins = pd.cut(cells.percentile, [-1, .5, .9, .99, 1.0 - 1e-12, 2], labels=["<50%", "50-90%", "90-99%", "99%-max",
                                                                              "beyond max"])
    rows = []
    for b, c in cells.groupby(bins, observed=True):
        w = c.possessions.to_numpy(float)
        mse = {m: float(w @ c[f"err_{m}"] ** 2 / w.sum()) for m in COLUMNS}
        rows.append(dict(distance=str(b), cells=len(c), possessions=float(w.sum()), **{f"mse_{m}": v for m, v in mse.items()},
                         **{f"excess_{r}": mse[r] - mse["baseline"] for r in RULES}))
    by_distance = pd.DataFrame(rows)
    result["by_distance"] = by_distance.to_dict("records")
    lines += ["", "cell MSE (within-quarter centered) by offense composition distance from the model's support",
              by_distance.round(2).to_string(index=False)]
    text = "\n".join(lines)
    print(text, flush=True)
    return result, text


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(int(os.environ.get("LINEUPS_THREADS", 8)))      # (the refresh on the laptop: 1)
    g = legacy.matchups()
    results, texts = {}, []
    for name, fam in families(g).items():
        frame = build(name, fam, g)
        results[name], text = report(name, frame)
        texts.append(text)
    decision = all(results[k]["contrasts"]["translated-as_was"]["estimate"] > 0 for k in results)
    results["decision"] = "translated" if decision else "as_was"
    (OUT / "result.json").write_text(json.dumps(results, indent=1, default=float))
    (OUT / "report.txt").write_text("\n\n".join(texts) + f"\n\ndecision: {results['decision']}\n")
    print("decision:", results["decision"])


if __name__ == "__main__":
    main()
