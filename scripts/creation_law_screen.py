"""Assumption O, creation conservation: in-range cost and fixtures (docs/CLOSEOUT.md, step 4b; exploratory).

O is the reference model with its creation constraint at declared full
strength. When a lineup's demand for assisted finishing exceeds its passing
supply, each assisted attempt's make odds scale by supply / demand (k_supply = 1;
the fitted strengths are about 0.1). The direction and the strength are declared.
Nothing is fitted, and every other weight is the reference's.

In range: every saved reference fit at the 48 benchmark origins (three seeds,
five checkpoints) is rerun with k_supply = 1. Each seed is calibrated by its own
prior-only affine, as the scorecard does, and scored on 2016-2026 broad cells
against the reference itself (rebuilt, and checked equal to the saved
forecasts).

Fixtures: the release model (2027q1) with k_supply = 1 against the average-opponent
panel.

    PYTHONPATH=.:scripts python -u scripts/creation_law_screen.py
"""
import copy
import json

import numpy as np
import pandas as pd
import torch

from lineups import evaluate, legacy, paths, release
from lineups.coherence import checkpoint_models, fixtures
from lineups.evaluate import FIVE
from lineups.features import Store
from lineups.model import average_ledgers
from lineups.train import Rows, game_batches

OUT = paths.CACHE / "creation_law_screen_2026_10_12"
K_SUPPLY = 1.
ARMS = ("R", "O")
FIXTURES = ("five_goberts", "legal_pure_centers", "limited_centers", "five_jokics", "jokic_westbrook",
            "jokic_korver", "small_guards", "highest_exposure_real_2026")


def declare(models, k=K_SUPPLY):
    """Copies of the checkpoint models with the creation strength set to k."""
    out = []
    for m in models:
        c = copy.deepcopy(m)
        with torch.no_grad():
            c.backbone.k_supply.fill_(k)
        out.append(c.eval())
    return out


def origin_rows(o, g, data, store):
    path = OUT / "rows" / f"{o.tag}.pkl"
    if path.exists():
        return pd.read_pickle(path)
    normalizer, env = store.normalizer(o.tag, "final"), store.env(o.tag, "final")
    rows = np.sort(legacy.quarter_rows(o, g))
    batches = list(game_batches(data.game, rows))
    order = np.argsort(np.concatenate(batches))
    inputs = [data.batch(ix, normalizer, origin_index=int(o.origin_index))[0] for ix in batches]
    f = legacy.row_frame(rows, g)
    for seed in legacy.SEEDS:
        models = checkpoint_models(o.tag, seeds=(seed,))
        for arm, ms in (("R", models), ("O", declare(models))):
            with torch.no_grad():
                p = np.concatenate([average_ledgers([m(x, env) for m in ms]).points100.numpy() for x in inputs])[order]
            f[f"{arm}{seed}"] = p.astype(float)
        ids, saved = legacy.native(o.tag, "J_POINT_BOTH", seed, "checkpoint_average")
        # 1e-5: multithreaded float32 sums move single rows by ~1e-6 (one thread matches to 1e-7).
        if not np.array_equal(ids, rows) or np.abs(f[f"R{seed}"] - saved).max() > 1e-5:
            raise ValueError(f"rebuilt reference differs from the saved forecast at {o.tag}/s{seed}")
    path.parent.mkdir(parents=True, exist_ok=True)
    f.to_pickle(path)
    return f


def accuracy(g):
    data, store = Rows(g, Store()), Store()
    history = {(a, s): [] for a in ARMS for s in legacy.SEEDS}
    recs = []
    for o in legacy.origins().itertuples():
        f = origin_rows(o, g, data, store)
        league = legacy.controls(o.tag, legacy.SEEDS[0]).league.to_numpy()
        cal = {}
        for a in ARMS:
            for s in legacy.SEEDS:
                h = pd.concat(history[(a, s)], ignore_index=True) if history[(a, s)] else None
                cal[(a, s)] = evaluate.calibrate(evaluate.affine(h, o.start), f[f"{a}{s}"], league)
                history[(a, s)].append(evaluate.history_cells(f, f[f"{a}{s}"].to_numpy(), league, o.stop))
        print(o.tag, flush=True)
        if o.season < 2016:
            continue
        f = f.assign(**{a: np.mean([cal[(a, s)] for s in legacy.SEEDS], 0) for a in ARMS})
        c = evaluate.cells(f, list(ARMS))
        c = c[c.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        w, y = c.possessions.to_numpy(float), c.actual.to_numpy(float)
        for a in ARMS:
            e = y - c[a].to_numpy(float)
            recs.append(dict(season=int(o.season), arm=a, sse_c=w @ (e - np.average(e, weights=w)) ** 2,
                             sst=w @ (y - np.average(y, weights=w)) ** 2, moved=float(w @ (np.abs(c.O - c.R) > .1) / w.sum()),
                             **evaluate.sufficient(y, c[a], w)))
    t = pd.DataFrame(recs)
    raw = lambda x: evaluate.metrics(evaluate.pooled(x))["r2"]
    centered = lambda x: 1 - x.sse_c.sum() / x.sst.sum()
    out = {}
    for name, fn in (("raw", raw), ("centered", centered)):
        per = t.groupby(["season", "arm"]).apply(fn, include_groups=False).unstack("arm")
        d = per.O - per.R
        out[name] = dict(R=float(fn(t[t.arm == "R"])), O=float(fn(t[t.arm == "O"])),
                         difference=float(fn(t[t.arm == "O"]) - fn(t[t.arm == "R"])),
                         season_se=float(d.std(ddof=1) / np.sqrt(len(d))), seasons_positive=int((d > 0).sum()))
    out["cells_moved_over_0.1"] = float(t[t.arm == "O"].moved.mean())
    return out


def fixture_table():
    rel, fx = release.Release(arms=("R",)), fixtures()
    rows = []
    for name in FIXTURES:
        rec = dict(fixture=name)
        for arm in ARMS:
            saved = rel.models["R"]
            if arm == "O":
                rel.models["R"] = {s: declare(ms) for s, ms in saved.items()}
            r = rel.ratings(fx[name]["pids"])
            rel.models["R"] = saved
            rec |= {f"{arm}_{k}": v for k, v in r.items()}
        rows.append(rec)
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(8)
    table = fixture_table()
    table.to_csv(OUT / "fixtures.csv", index=False)
    print(table.round(1).to_string(index=False), flush=True)
    result = accuracy(legacy.matchups())
    (OUT / "result.json").write_text(json.dumps(result, indent=1))
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
