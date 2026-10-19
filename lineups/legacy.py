"""Readers for pre-refactor artifacts (tag pre-refactor-2026-10-09).

These read files only; nothing here imports the old ``experiments`` code.
"""
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from lineups import paths
from lineups.evaluate import FIVE

DEFENSE = [f"d{i}" for i in range(5)]
SEEDS = (17, 23, 41)


def schedule(path=paths.SCHEDULE):
    s = pd.read_csv(path, parse_dates=["start", "stop"])
    s["tag"] = s.season.astype(str) + "q" + s.window.astype(str)
    s["origin_index"] = np.arange(len(s))
    return s


def origins(first_season=2015):
    return schedule().query("season >= @first_season").reset_index(drop=True)


def day(value):
    return int(np.datetime64(value, "D").astype(np.int64))


@lru_cache(maxsize=1)
def matchups(directory=paths.V16_INPUTS):
    """Game x offense five x defense five labels (memory-mapped)."""
    directory = Path(directory) / "matchups"
    names = json.loads((directory / "arrays.json").read_text())
    return {k: np.load(directory / (k + ".npy"), mmap_mode="r", allow_pickle=False) for k in names}


def quarter_rows(origin, g=None):
    g = matchups() if g is None else g
    return np.flatnonzero((g["date"] >= day(origin.start)) & (g["date"] < day(origin.stop)))


def row_frame(rows, g=None):
    g = matchups() if g is None else g
    f = pd.DataFrame({k: np.asarray(g[k][rows]) for k in ("game_id", "date", "possessions", "points")})
    f["row"] = rows
    f[FIVE] = np.asarray(g["pids"][rows])
    f[DEFENSE] = np.asarray(g["defense"][rows])
    return f


def controls(origin_tag, seed, directory=paths.V16_CONTROLS):
    """Calibrated additive controls and the dated league reference, per row."""
    with np.load(Path(directory) / origin_tag / f"s{seed}" / "groups.npz") as z:
        frame = pd.DataFrame(z["prediction"], columns=z["models"].tolist())
        frame["row"] = z["row"]
        frame["league"] = z["league"]
    return frame


def native(origin_tag, arm, seed, view="direct", run=paths.V16_RUN):
    """Saved per-row native points/100: 'direct' (final fit) or 'checkpoint_average'."""
    name = "primary" if view == "direct" else "checkpoint_average"
    with np.load(Path(run) / "origins" / origin_tag / arm / f"s{seed}" / f"{name}.npz") as z:
        return z["row"].copy(), z["points100"].astype(float)
