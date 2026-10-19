"""Secondary benchmark without selected possessions (exploratory).

Coaches keep lineups that start well (scripts/selection_check.py), so a cell's
first possessions are partly selected outcomes. This scores each offense-five x
quarter cell on its possessions after the first EARLY, and compares that with
the primary benchmark on the same models.

* Possessions and forecasts as in selection_check: every possession in the 44
  primary quarters, joined to its row's seed-mean forecasts (prior-only
  calibration, checkpoint-average view of J_POINT_BOTH, and additive_defense).
* Primary cells: all possessions, cells with >= 50 (reproduces the scorecard).
* Late cells: possessions after the first EARLY in the cell, cells with >= 50
  such possessions.
* Metrics pooled over quarters, possession-weighted; r^2 = 1 - SSE/SST.

    PYTHONPATH=. python -u scripts/late_possession_benchmark.py
"""
import numpy as np
import pandas as pd

from lineups import evaluate, legacy, paths
from selection_check import EARLY, POSSESSIONS, forecasts, lineup_key

OUT = paths.CACHE / "late_possession_benchmark_2026_10_09"
MODELS = ("half", "calibrated", "additive_defense", "native")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = forecasts(models=MODELS)
    rows["off"] = lineup_key(rows[evaluate.FIVE].to_numpy())
    rows["def"] = lineup_key(rows[legacy.DEFENSE].to_numpy())
    p = pd.read_pickle(POSSESSIONS)
    p = p[p.game_id.isin(rows.game_id.unique())].reset_index(drop=True)
    away = p[[f"away_player_{i}_id" for i in range(1, 6)]].to_numpy()
    home = p[[f"home_player_{i}_id" for i in range(1, 6)]].to_numpy()
    ball = p.away_team_ball.to_numpy()[:, None]
    p["off"], p["def"] = lineup_key(np.where(ball, away, home)), lineup_key(np.where(ball, home, away))
    p["order"] = np.arange(len(p))
    j = p.merge(rows[["game_id", "off", "def", "origin", "season", *MODELS]], on=["game_id", "off", "def"],
                how="inner").sort_values(["origin", "off", "game_id", "order"])
    j["k"] = j.groupby(["origin", "off"]).cumcount()
    j["points"] = 100. * j.points_scored
    out = []
    for name, use in (("primary", np.ones(len(j), bool)), ("late", (j.k >= EARLY).to_numpy())):
        cells = j[use].groupby(["origin", "off"]).agg(possessions=("points", "size"), actual=("points", "mean"),
                                                      season=("season", "first"),
                                                      **{m: (m, "mean") for m in MODELS})
        cells = cells[cells.possessions >= evaluate.MIN_CELL_POSSESSIONS]
        stats = {m: [] for m in MODELS}
        for _, c in cells.groupby("origin"):
            for m in MODELS:
                stats[m].append(evaluate.sufficient(c.actual, c[m], c.possessions))
        for m in MODELS:
            out.append(dict(benchmark=name, model=m, **evaluate.metrics(evaluate.pooled(stats[m]))))
    table = pd.DataFrame(out)
    table.to_csv(OUT / "metrics.csv", index=False)
    with pd.option_context("display.width", 200, "display.float_format", "{:.6f}".format):
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
