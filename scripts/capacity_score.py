"""Score the confirmatory capacity run against the reference (frozen with the protocol).

Protocol: reports/capacity_confirmatory_protocol_2026_10_09.md. Writes
experiments/cache/capacity_v2_run_2026_10_09/score/ and prints the decision
quantities.

    PYTHONPATH=. python -u scripts/capacity_score.py
    PYTHONPATH=. python -u scripts/capacity_score.py --dry-run   # reference vs itself: every delta must be 0
"""
import argparse
import json

import numpy as np
import pandas as pd
import torch

import property_suite
from capacity_run import OUT, V14, case_dir
from creation_analogues import LOW_CREATION_AST, roles
from defense_analogues import BIG_INCHES
from lineups import db, evaluate, legacy, properties
from lineups.coherence import checkpoint_models, fixtures, ledgers, matchup
from lineups.features import Store
from lineups.model import EventModel

T_10 = 1.812
MARGIN = -.003
PROPERTY_ORIGINS = ("2024q4", "2025q4", "2026q2", "2026q4")
COUNTED = ("spacing_rim", "handler_conversion", "handler_teammate_turnovers", "clone_synergy", "rim_synergy",
           "rebound_synergy", "permutation")
PAIRS = (("legal_pure_centers", "jokic_westbrook"), ("legal_pure_centers", "jokic_korver"),
         ("five_goberts", "jokic_westbrook"))


def capacity_native(view):
    def native(o, seed):
        with np.load(case_dir(o.tag, seed) / "forecast.npz") as z:
            return z["row"].copy(), z[view].astype(float)
    return native


def capacity_models(tag):
    models = []
    for seed in legacy.SEEDS:
        parent = torch.load(V14 / "origins" / tag / "RB_RENEW_FAC" / f"s{seed}" / "final.pt", map_location="cpu",
                            weights_only=False)["state_dict"]
        for state in torch.load(case_dir(tag, seed) / "fit.pt", map_location="cpu", weights_only=False)["checkpoints"]:
            m = EventModel.from_parent(parent, seed, defense="capacity")
            m.load_state_dict(state)
            models.append(m.eval())
    return models


def frames(native_of, g):
    out = []
    for o, f in evaluate.calibrated_rows(legacy.origins(), lambda o: legacy.row_frame(legacy.quarter_rows(o, g), g),
                                         native_of,
                                         lambda o, s: legacy.controls(o.tag, s)[["row", "league", "additive_defense"]],
                                         legacy.SEEDS):
        f["origin"], f["season"], f["origin_index"] = o.tag, int(o.season), int(o.origin_index)
        f["novel"] = evaluate.novel_offense(f, legacy.day(o.start), g)
        out.append(f)
    return pd.concat(out, ignore_index=True)


def accuracy(rows):
    """Pooled and per-season r^2 (broad cells per quarter), all and novel slices."""
    stats = []
    for (tag, season), f in rows.groupby(["origin", "season"], sort=False):
        c = evaluate.cells(f, list(evaluate.MODELS) + ["novel"])
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        for name, s in (("all", c), ("novel", c[c.novel > .5])):
            for m in evaluate.MODELS:
                stats.append(dict(origin=tag, season=season, slice=name, model=m,
                                  **evaluate.sufficient(s.actual, s[m], s.possessions)))
    return pd.DataFrame(stats)


def r2(stats, by=()):
    keys = list(by) + ["slice", "model"]
    return stats.groupby(keys).apply(lambda g: evaluate.metrics(evaluate.pooled(g))["r2"], include_groups=False)


def cohorts(rows, store, heights):
    """Row-level cohort flags from origin-dated roles and listed heights."""
    flags = []
    for index, f in rows.groupby("origin_index", sort=False):
        off, dfn = f[evaluate.FIVE].to_numpy(), f[legacy.DEFENSE].to_numpy()
        r = roles(store, int(index), np.unique(off))
        look = lambda col: r[col].reindex(off.ravel()).to_numpy().reshape(off.shape)
        h_off = heights.reindex(off.ravel()).to_numpy().reshape(off.shape)
        h_def = heights.reindex(dfn.ravel()).to_numpy().reshape(dfn.shape)
        flags.append(pd.DataFrame(dict(
            two_nonspacing_bigs=((h_off >= BIG_INCHES) & (look("three") < 1)).sum(1) >= 2,
            weak_best_passer=look("assist").max(1) < LOW_CREATION_AST,
            defense_two_bigs=(h_def >= BIG_INCHES).sum(1) >= 2), index=f.index))
    return pd.concat(flags)


def residual_bias(rows, flags):
    actual = 100 * rows.points / rows.possessions
    out = []
    for cohort in flags.columns:
        sub = rows[flags[cohort]]
        resid = actual[flags[cohort]] - sub.half
        per = pd.DataFrame(dict(r=resid, w=sub.possessions, season=sub.season)).groupby("season").apply(
            lambda s: np.average(s.r, weights=s.w), include_groups=False)
        out.append(dict(cohort=cohort, possessions=int(sub.possessions.sum()),
                        residual=float(np.average(resid, weights=sub.possessions)),
                        se=float(per.std(ddof=1) / np.sqrt(len(per)))))
    return pd.DataFrame(out)


def main(dry_run):
    score_dir = OUT / ("score_dry_run" if dry_run else "score")
    score_dir.mkdir(parents=True, exist_ok=True)
    store, g, fx = Store(), legacy.matchups(), fixtures()
    reference_native = lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average")
    arms = dict(reference=reference_native,
                capacity=reference_native if dry_run else capacity_native("checkpoint_average"))
    arm_models = dict(reference=checkpoint_models,
                      capacity=checkpoint_models if dry_run else capacity_models)
    if not dry_run:
        missing = [c for c in __import__("capacity_run").cases() if not (case_dir(*c) / "complete.json").exists()]
        if missing:
            raise SystemExit(f"{len(missing)} fits incomplete, e.g. {missing[:3]}")
    result = {}

    # 1. Accuracy.
    rows = {name: frames(native_of, g) for name, native_of in arms.items()}
    acc = {name: accuracy(r) for name, r in rows.items()}
    pooled = {name: r2(a) for name, a in acc.items()}
    season = {name: r2(a, ["season"]) for name, a in acc.items()}
    d_pool = pooled["capacity"][("all", "half")] - pooled["reference"][("all", "half")]
    d_season = (season["capacity"].xs(("all", "half"), level=("slice", "model"))
                - season["reference"].xs(("all", "half"), level=("slice", "model")))
    se = float(d_season.std(ddof=1) / np.sqrt(len(d_season)))
    result["accuracy"] = dict(
        reference_r2=float(pooled["reference"][("all", "half")]), capacity_r2=float(pooled["capacity"][("all", "half")]),
        delta=float(d_pool), season_se=se, lower_bound=float(d_pool - T_10 * se),
        non_inferior=bool(d_pool - T_10 * se > MARGIN), seasons_positive=int((d_season > 0).sum()),
        per_season=d_season.round(6).to_dict(),
        secondary={f"{s}/{m}": dict(reference=float(pooled["reference"][(s, m)]),
                                    capacity=float(pooled["capacity"][(s, m)]))
                   for s in ("all", "novel") for m in evaluate.MODELS})
    print(json.dumps(result["accuracy"], indent=1), flush=True)

    # 2. Fixtures at every primary origin (three-seed checkpoint mixtures).
    margins = []
    for o in legacy.origins().query("season >= 2016").itertuples():
        for name, make in arm_models.items():
            models = make(o.tag)
            for a, b in PAIRS:
                margins.append(dict(origin=o.tag, model=name, pair=f"{a}|{b}",
                                    margin=matchup(models, store, fx[a]["pids"], fx[b]["pids"], o.tag)["margin"]))
        print("fixtures", o.tag, flush=True)
    margins = pd.DataFrame(margins)
    margins.to_csv(score_dir / "fixtures.csv", index=False)
    wide = margins.pivot_table(index=["pair", "origin"], columns="model", values="margin")
    change = (wide.capacity - wide.reference).groupby(level="pair")
    result["fixtures"] = {pair: dict(mean_change=float(c.mean()), share_lower=float((c < 0).mean()),
                                     capacity_lose_share=float((wide.loc[pair].capacity < 0).mean()),
                                     reference_lose_share=float((wide.loc[pair].reference < 0).mean()))
                          for pair, c in change}

    # 3. Property suite.
    suites = []
    for tag in PROPERTY_ORIGINS:
        offense = property_suite.real_fives(tag, g, evaluate.FIVE)
        defense = property_suite.real_fives(tag, g, legacy.DEFENSE)
        for name, make in arm_models.items():
            models = make(tag)
            frame = properties.run(lambda o, d, m=models: ledgers(m, store, o, d, tag), store, tag, offense, defense,
                                   offense[:40])
            frame.to_csv(score_dir / f"properties_{tag}_{name}.csv", index=False)
            suites.append(properties.summarize(frame).pass_rate.rename("pass_rate").reset_index()
                          .rename(columns={"index": "property"}).assign(origin=tag, model=name))
        print("properties", tag, flush=True)
    suites = pd.concat(suites)
    suites.to_csv(score_dir / "properties.csv", index=False)
    mean_pass = suites.groupby(["property", "model"]).pass_rate.mean().unstack("model")
    worse = mean_pass.loc[list(COUNTED)].pipe(lambda m: m.reference - m.capacity)
    result["properties"] = dict(mean_pass=mean_pass.round(4).to_dict(), counted_worse_by_over_05=int((worse > .05).sum()))
    legal = result["fixtures"]["legal_pure_centers|jokic_westbrook"]
    result["pillar2_gain"] = bool(legal["share_lower"] >= .75 and -legal["mean_change"] >= 2
                                  and result["properties"]["counted_worse_by_over_05"] <= 1)

    # Secondary: residual bias on real unusual cells.
    heights = db.heights()
    flags = cohorts(rows["reference"], store, heights)
    result["unusual_cells"] = {name: residual_bias(r, flags.loc[r.index]).round(4).to_dict("records")
                               for name, r in rows.items()}

    (score_dir / "result.json").write_text(json.dumps(result, indent=1, default=float))
    print(json.dumps({k: v for k, v in result.items() if k != "accuracy"}, indent=1, default=float))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    main(p.parse_args().dry_run)
