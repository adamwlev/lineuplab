"""Observed analogues for creation, and selection by composition (exploratory).

1. Does the reference over-forecast offenses without a ball handler? Rows are
   grouped by the lineup's best passer (highest prior assist rate per 100,
   origin-dated) and by the number of handlers (assist rate >= 6 per 100).
2. Is the early-possession excess (scripts/selection_check.py) larger for
   unusual offenses (two or more non-spacing bigs, or best passer below 5)?
   If coaches keep unusual lineups mainly when they start well, it should be.

Same rows, forecasts, weighting and season-level SEs as the other analogue
scripts. Thresholds fixed before looking at residuals.

    PYTHONPATH=. python -u scripts/creation_analogues.py
"""
import numpy as np
import pandas as pd

from defense_analogues import BIG_INCHES, SHOOTER_3PA, stratum_table
from lineups import db, legacy, paths
from lineups.evaluate import FIVE, MODELS, calibrated_rows
from lineups.features import Store
from selection_check import EARLY, POSSESSIONS, lineup_key

OUT = paths.CACHE / "creation_analogues_2026_10_09"
HANDLER_AST = 6.
LOW_CREATION_AST = 5.


def roles(store, origin_index, pids):
    base = store.offense(pids, origin_index=origin_index)["base"].astype(float)
    loc = np.exp(base[:, 3:9] - base[:, 3:9].max(1, keepdims=True))
    loc /= loc.sum(1, keepdims=True)
    three = 100 * np.exp(np.clip(base[:, 0], -12, 4)) * loc[:, 4:].sum(1)
    assist = 100 * np.exp(np.clip(base[:, 16], -12, 4))
    return pd.DataFrame(dict(three=three, assist=assist), index=pids)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    store, g = Store(), legacy.matchups()
    height = db.heights()
    frames = []
    for o, f in calibrated_rows(legacy.origins(), lambda o: legacy.row_frame(legacy.quarter_rows(o, g), g),
                                lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"),
                                lambda o, s: legacy.controls(o.tag, s)[["row", "league", "additive_defense"]],
                                legacy.SEEDS):
        off = f[FIVE].to_numpy()
        r = roles(store, int(o.origin_index), np.unique(off))
        look = lambda col: r[col].reindex(off.ravel()).to_numpy().reshape(off.shape)
        h = height.reindex(off.ravel()).to_numpy().reshape(off.shape)
        f["best_passer"] = look("assist").max(1)
        f["handlers"] = (look("assist") >= HANDLER_AST).sum(1)
        f["nonspacing_bigs"] = ((h >= BIG_INCHES) & (look("three") < 1)).sum(1)
        f["shooters"] = (look("three") >= SHOOTER_3PA).sum(1)
        f["season"], f["origin"] = int(o.season), o.tag
        actual = 100 * f.points / f.possessions
        for m in MODELS:
            f[f"r_{m}"] = actual - f[m]
        frames.append(f)
    rows = pd.concat(frames, ignore_index=True)
    rows["best_passer_bin"] = pd.cut(rows.best_passer, [0, 4, 5, 6, 8, 10, np.inf], right=False)
    rows["handlers_bin"] = rows.handlers.clip(upper=3)
    with pd.option_context("display.width", 220, "display.float_format", "{:.3f}".format):
        for by in (["best_passer_bin"], ["handlers_bin"]):
            t = stratum_table(rows.assign(**{by[0]: rows[by[0]].astype(str)}), by)
            t.to_csv(OUT / f"by_{by[0]}.csv", index=False)
            print("\n== residual (actual - forecast) by", by)
            print(t[[c for c in t.columns if not c.endswith("additive_defense")]].to_string(index=False))

    # Selection by composition: early-minus-late residual gap for unusual versus ordinary offenses.
    rows["off"] = lineup_key(rows[FIVE].to_numpy())
    rows["def"] = lineup_key(rows[legacy.DEFENSE].to_numpy())
    p = pd.read_pickle(POSSESSIONS)
    p = p[p.game_id.isin(rows.game_id.unique())].reset_index(drop=True)
    away = p[[f"away_player_{i}_id" for i in range(1, 6)]].to_numpy()
    home = p[[f"home_player_{i}_id" for i in range(1, 6)]].to_numpy()
    ball = p.away_team_ball.to_numpy()[:, None]
    p["off"], p["def"] = lineup_key(np.where(ball, away, home)), lineup_key(np.where(ball, home, away))
    p["order"] = np.arange(len(p))
    j = p.merge(rows[["game_id", "off", "def", "half", "origin", "season", "best_passer", "nonspacing_bigs"]],
                on=["game_id", "off", "def"], how="inner").sort_values(["origin", "off", "game_id", "order"])
    j["k"] = j.groupby(["origin", "off"]).cumcount()
    j["n"] = j.groupby(["origin", "off"]).k.transform("size")
    j = j[(j.n > EARLY) & (j.n < 200)]
    j["early"] = j.k < EARLY
    j["resid"] = 100 * j.points_scored - j.half
    j["unusual"] = (j.nonspacing_bigs >= 2) | (j.best_passer < LOW_CREATION_AST)
    out = []
    for unusual, s in j.groupby("unusual"):
        per = s.groupby(["season", "early"]).resid.mean().unstack("early")
        gap = (per[True] - per[False]).dropna()
        out.append(dict(unusual=unusual, cells=s.groupby(["origin", "off"]).ngroups, possessions=len(s),
                        gap=gap.mean(), se=gap.std(ddof=1) / np.sqrt(len(gap)), seasons=len(gap),
                        positive=int((gap > 0).sum())))
    t = pd.DataFrame(out)
    t.to_csv(OUT / "selection_by_composition.csv", index=False)
    print("\n== Early-minus-late residual gap, cells of 26-199 possessions, by composition")
    print(t.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
