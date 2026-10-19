"""Do a lineup's early possessions beat the forecast by more than its later ones? (exploratory)

Coaches keep lineups that start well and pull lineups that start badly. If so,
a lineup-quarter's first possessions should outscore the forecast by more than
its later possessions, even though the forecast for a given game and opposing
five does not depend on possession order.

Possessions: every possession in the 44 primary quarters (2016-2026), joined
to its game x offense five x defense five row and that row's seed-mean
reference forecast (half blend, prior-only calibration). Cell = offense five x
quarter. Possessions in a cell are ordered by date and in-game order; "early"
is the first 25. Residual = 100 x points - forecast (points per 100).
Uncertainty: season-level standard errors over 11 seasons.

    PYTHONPATH=. python -u scripts/selection_check.py
"""
import numpy as np
import pandas as pd

from lineups import legacy, paths
from lineups.evaluate import FIVE, calibrated_rows

EARLY = 25
POSSESSIONS = paths.CACHE / "possessions_ba7aeb377198.pkl"
OUT = paths.CACHE / "selection_check_2026_10_09"


def forecasts(models=("half", "additive_defense")):
    g = legacy.matchups()
    frames = []
    for o, f in calibrated_rows(legacy.origins(), lambda o: legacy.row_frame(legacy.quarter_rows(o, g), g),
                                lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"),
                                lambda o, s: legacy.controls(o.tag, s)[["row", "league", "additive_defense"]],
                                legacy.SEEDS):
        frames.append(f[["game_id", "possessions", "points", *models] + FIVE + legacy.DEFENSE]
                      .assign(origin=o.tag, season=int(o.season)))
    return pd.concat(frames, ignore_index=True)


def lineup_key(players):
    s = np.sort(players, 1).astype(np.int64)
    return s @ (np.int64(4096) ** np.arange(5, dtype=np.int64))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = forecasts()
    rows["off"] = lineup_key(rows[FIVE].to_numpy())
    rows["def"] = lineup_key(rows[legacy.DEFENSE].to_numpy())
    p = pd.read_pickle(POSSESSIONS)
    p = p[p.game_id.isin(rows.game_id.unique())].reset_index(drop=True)
    away = p[[f"away_player_{i}_id" for i in range(1, 6)]].to_numpy()
    home = p[[f"home_player_{i}_id" for i in range(1, 6)]].to_numpy()
    ball = p.away_team_ball.to_numpy()[:, None]
    p["off"] = lineup_key(np.where(ball, away, home))
    p["def"] = lineup_key(np.where(ball, home, away))
    p["order"] = np.arange(len(p))
    joined = p.merge(rows[["game_id", "off", "def", "half", "additive_defense", "origin", "season", "possessions",
                           "points"]], on=["game_id", "off", "def"], how="inner")
    check = joined.groupby(["game_id", "off", "def"]).agg(n=("order", "size"), pts=("points_scored", "sum"),
                                                         row_n=("possessions", "first"), row_pts=("points", "first"))
    print(f"possessions joined {len(joined):,} of {len(p):,}; rows where possession counts match "
          f"{(check.n == check.row_n).mean():.4f}, points match {(check.pts == check.row_pts).mean():.4f}")
    joined = joined.sort_values(["origin", "off", "game_id", "order"])
    joined["k"] = joined.groupby(["origin", "off"]).cumcount()
    joined["cell_n"] = joined.groupby(["origin", "off"]).k.transform("size")
    joined["early"] = joined.k < EARLY
    joined["resid"] = 100 * joined.points_scored - joined.half
    joined["resid_additive"] = 100 * joined.points_scored - joined.additive_defense
    joined["size"] = pd.cut(joined.cell_n, [EARLY, 50, 100, 200, np.inf], right=False,
                            labels=["25-49", "50-99", "100-199", "200+"])
    out = []
    for size, g in joined[joined.cell_n > EARLY].groupby("size", observed=True):
        per = g.groupby(["season", "early"])[["resid", "resid_additive"]].mean().unstack("early")
        gap = per[("resid", True)] - per[("resid", False)]
        gap_add = per[("resid_additive", True)] - per[("resid_additive", False)]
        raw = g.groupby(["season", "early"]).points_scored.mean().unstack("early")
        raw_gap = 100 * (raw[True] - raw[False])
        out.append(dict(cell_size=size, cells=g.groupby(["origin", "off"]).ngroups, possessions=len(g),
                        raw_gap=raw_gap.mean(), resid_gap=gap.mean(), se=gap.std(ddof=1) / np.sqrt(len(gap)),
                        seasons_positive=f"{int((gap > 0).sum())}/{len(gap)}", resid_gap_additive=gap_add.mean()))
    table = pd.DataFrame(out)
    table.to_csv(OUT / "early_late.csv", index=False)
    with pd.option_context("display.width", 200, "display.float_format", "{:.3f}".format):
        print("\n== First 25 possessions minus later possessions, points per 100 (season means)")
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
