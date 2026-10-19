"""Seasons and quarter-season forecast windows (refactor rung 5, step 1).

A season is labeled by the year it ends; games after August belong to the next
season, except in 2020, when the bubble ran into October. Each season is cut
into SLICES windows with online-observable starts: a window starts the day after
the league's cumulative game count crosses each multiple of 1200 / SLICES. The
last window ends the day after the season's final game.

Ported from tag pre-refactor-2026-10-09 (asof_additive.season_labels,
asof_state.rolling_windows). ``build(2014, 2026)`` reproduces
experiments/cache/asof_points_2026/schedule.csv exactly (tests/test_schedule.py).
"""
import numpy as np
import pandas as pd

from lineups import paths

SLICES = 4
POSSESSIONS = paths.CACHE / "possessions_ba7aeb377198.pkl"


def season_labels(dates):
    dates = pd.to_datetime(pd.Series(dates))
    year, month = dates.dt.year.to_numpy(), dates.dt.month.to_numpy()
    return np.where(month > np.where(year == 2020, 11, 8), year + 1, year).astype(np.int32)


def windows(games, slices=SLICES):
    """games: one row per game with game_date and season. Returns season, window, start, stop and counts."""
    rows, step = [], 1200 // slices
    g = games.assign(game_date=pd.to_datetime(games.game_date).dt.normalize())
    for season, block in g.groupby("season", sort=True):
        by_day = block.groupby("game_date").size().sort_index()
        cum = by_day.cumsum()
        starts = [by_day.index[0]]
        for threshold in range(step, step * slices, step):
            crossed = cum[cum >= threshold]
            if crossed.empty:
                break
            candidate = crossed.index[0] + pd.Timedelta(days=1)
            if by_day.index[-1] >= candidate > starts[-1]:
                starts.append(candidate)
        stops = starts[1:] + [by_day.index[-1] + pd.Timedelta(days=1)]
        for window, (start, stop) in enumerate(zip(starts, stops), 1):
            rows.append(dict(season=int(season), window=window, start=start, stop=stop,
                             n_games=int(((block.game_date >= start) & (block.game_date < stop)).sum()),
                             prior_season_games=int((block.game_date < start).sum())))
    return pd.DataFrame(rows)


def games(possessions=None):
    p = pd.read_pickle(POSSESSIONS) if possessions is None else possessions
    g = p[["game_id", "game_date"]].drop_duplicates("game_id")
    return g.assign(season=season_labels(g.game_date))


def build(first_season, last_season, possessions=None):
    g = games(possessions)
    g = g[(g.season >= first_season) & (g.season <= last_season)]
    return windows(g).sort_values(["start", "season", "window"]).reset_index(drop=True)
