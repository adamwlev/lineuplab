"""Is defense sub-additive in bigs? A forward additive check across eras (exploratory).

The capacity-law assumption model says a third, fourth or fifth big adds less
defense than additive models credit. The 2016-2026 window has almost no
three-big lineups; 2003-2011 has about ten times more. This checks the premise
with a model simple enough to fit in every season:

* Season t is forecast by a ridge additive model (offense and defense player
  effects, points per 100 possessions) fitted on season t-1 possessions only.
  Players unseen in t-1 count as average. RIDGE is fixed, not tuned on these
  residuals.
* Roles come from season t-1 player-game stats (experiments/cache/
  game_player_stats.pkl) and listed height: big = 82 in or taller; shooter =
  at least 4 3PA per 100 on-floor possessions; non-spacing = under 1.
* Residual = actual - forecast per possession. Grouped by the number of bigs
  on defense (and by spacing on offense), possession-weighted, with
  season-level standard errors, separately for 2003-2011 and 2016-2026.

Sub-additive defense predicts positive residuals that grow with the number of
defensive bigs beyond two. Selection on the outcome (big lineups are kept when
they work) biases the residuals the other way, so a positive result is the
informative one.

    PYTHONPATH=. python -u scripts/era_additive_analogues.py
"""
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.linear_model import Ridge

from lineups import db, paths, schedule

POSSESSIONS = paths.CACHE / "possessions_ba7aeb377198.pkl"
BOX = paths.CACHE / "game_player_stats.pkl"
OUT = paths.CACHE / "era_additive_analogues_2026_10_09"
RIDGE = 3000.
BIG, SHOOTER, NON_SHOOTER = 82, 4., 1.
ERAS = {"2003-2011": (2003, 2011), "2012-2015": (2012, 2015), "2016-2026": (2016, 2026)}


def season_of(dates):
    return schedule.season_labels(dates)


def box_roles(dates):
    """Per player-season 3PA and assists per 100 on-floor possessions (at least 200 possessions)."""
    f = pd.read_pickle(BOX)[["game_id", "pid", "own_fg3m", "own_fg3x", "own_ast", "ton_poss"]]
    f["season"] = f.game_id.map(dates)
    t = f.groupby(["pid", "season"])[["own_fg3m", "own_fg3x", "own_ast", "ton_poss"]].sum()
    t = t[t.ton_poss >= 200]
    return pd.DataFrame(dict(three=100 * (t.own_fg3m + t.own_fg3x) / t.ton_poss,
                             assist=100 * t.own_ast / t.ton_poss))


def design(p, players):
    """Sparse rows: offense players (+1 in offense block), defense players (+1 in defense block)."""
    index = {pid: i for i, pid in enumerate(players)}
    n = len(players)
    rows, cols = [], []
    for block, cols_names in ((0, [f"o{i}" for i in range(5)]), (n, [f"d{i}" for i in range(5)])):
        for c in cols_names:
            ids = p[c].map(index)
            ok = ids.notna().to_numpy()
            rows.append(np.flatnonzero(ok))
            cols.append(block + ids[ok].astype(int).to_numpy())
    r, c = np.concatenate(rows), np.concatenate(cols)
    return sparse.csr_matrix((np.ones(len(r)), (r, c)), shape=(len(p), 2 * n))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p = pd.read_pickle(POSSESSIONS)
    dates = pd.Series(season_of(p.game_date), index=p.game_id).groupby(level=0).first()
    away = p[[f"away_player_{i}_id" for i in range(1, 6)]].to_numpy()
    home = p[[f"home_player_{i}_id" for i in range(1, 6)]].to_numpy()
    ball = p.away_team_ball.to_numpy()[:, None]
    off, dfn = np.where(ball, away, home), np.where(ball, home, away)
    p = pd.DataFrame({**{f"o{i}": off[:, i] for i in range(5)}, **{f"d{i}": dfn[:, i] for i in range(5)},
                      "points": 100. * p.points_scored.to_numpy(), "season": season_of(p.game_date)})
    heights = db.heights()
    roles = box_roles(dates)
    out = []
    for season in range(2003, 2027):
        train, test = p[p.season == season - 1], p[p.season == season].copy()
        players = np.unique(train[[f"{s}{i}" for s in "od" for i in range(5)]].to_numpy())
        model = Ridge(alpha=RIDGE).fit(design(train, players), train.points)
        test["forecast"] = model.predict(design(test, players))
        prior = roles.xs(season - 1, level="season") if season - 1 in roles.index.get_level_values(1) else roles.iloc[:0]
        look = lambda col, table, side: table.reindex(test[[f"{side}{i}" for i in range(5)]].to_numpy().ravel())[col] \
            .to_numpy().reshape(-1, 5) if col != "height" else \
            heights.reindex(test[[f"{side}{i}" for i in range(5)]].to_numpy().ravel()).to_numpy().reshape(-1, 5)
        h_def, h_off = look("height", None, "d"), look("height", None, "o")
        three_off = look("three", prior, "o")
        three_def = look("three", prior, "d")
        test["def_bigs"] = (h_def >= BIG).sum(1)
        test["def_nonspacing_bigs"] = ((h_def >= BIG) & (three_def < NON_SHOOTER)).sum(1)
        test["off_shooters"] = (three_off >= SHOOTER).sum(1)
        test["off_bigs"] = (h_off >= BIG).sum(1)
        test["resid"] = test.points - test.forecast
        test["season"] = season
        out.append(test[["season", "def_bigs", "def_nonspacing_bigs", "off_shooters", "off_bigs", "resid", "points",
                         "forecast"]])
        print(season, len(test), f"mean resid {test.resid.mean():+.2f}", flush=True)
    r = pd.concat(out, ignore_index=True)
    r["era"] = pd.cut(r.season, [2002, 2011, 2015, 2026], labels=list(ERAS))
    r.to_csv(OUT / "possessions.csv.gz", index=False)

    def table(by):
        rows = []
        for key, g in r.groupby(["era"] + by, observed=True):
            per = g.groupby("season").resid.mean()
            rows.append(dict(zip(["era"] + by, key if isinstance(key, tuple) else (key,)), possessions=len(g),
                             share=len(g) / (r.era == key[0]).sum(), actual=g.points.mean(), resid=g.resid.mean(),
                             se=per.std(ddof=1) / np.sqrt(len(per)) if len(per) > 1 else np.nan,
                             seasons_positive=f"{int((per > 0).sum())}/{len(per)}"))
        return pd.DataFrame(rows)

    with pd.option_context("display.width", 200, "display.float_format", "{:.3f}".format):
        for by in (["def_bigs"], ["def_nonspacing_bigs"], ["off_bigs"]):
            t = table(by)
            t.to_csv(OUT / f"by_{by[0]}.csv", index=False)
            print(f"\n== residual (actual - forward additive forecast) by {by}")
            print(t.to_string(index=False))
        r["def_bigs3"] = r.def_bigs.clip(upper=3)
        r["spread"] = r.off_shooters >= 3
        t = table(["def_bigs3", "spread"])
        t.to_csv(OUT / "by_def_bigs_spread.csv", index=False)
        print("\n== by defensive bigs (3 = three or more) and offensive spacing (3+ shooters)")
        print(t.to_string(index=False))


if __name__ == "__main__":
    main()
