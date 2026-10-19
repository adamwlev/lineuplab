"""The additive control, additive_defense, for any offense and defense fives at an origin.

It is the pillar-1 comparator and the other half of the reference's half blend.
Ported from tag pre-refactor-2026-10-09; each step names its legacy source.

1. Snapshot. Ridge coefficients fitted on every possession before the origin
   (asof_additive_tuning.fit_origin, still run from the old code by
   scripts/additive_origin_fit.py). Each player has an offensive and a
   defensive identity (theta), a carried season effect (delta, scaled by rho)
   and experience-bin effects (eta).
2. Player parts in points per 100: base, carry and experience. A player the
   snapshot never saw contributes zero (asof_point_calibration.additive_offense_score,
   onfloor_defense.additive_defense_score).
3. Centering. Each part minus its mean over the players seen before the origin,
   weighted by possessions x 2^(-age/365 days) (asof_additive_reference,
   joint_capability_v15_controls.centered). An unseen player counts as that
   average player.
4. Offense: league + a + b x offense score, with (a, b >= 0) from possession-weighted
   least squares of actual - league on earlier completed cells
   (asof_point_calibration.fit_point_calibration).
5. Defense: k x defense score, where k is the weighted slope through the origin of
   actual - offense on the defense score over earlier cells, clipped to [0, 2]
   (joint_capability_v15_controls.slope).
6. additive_defense = league + c0 + c1 (offense + defense - league), with (c0, c1 >= 0)
   from weighted least squares on earlier completed offense-five cells with at
   least 50 possessions (joint_capability_v16_controls.affine).

The calibration histories of steps 4-6 are the saved 2015-2026 cell tables, so
they cover any origin up to 2027q1. Their cohort rules are not ported; origins
before 2015 or after 2027q1 need them.
"""
import pickle
from functools import lru_cache

import numpy as np
import pandas as pd
from scipy.optimize import lsq_linear

from lineups import legacy, paths
from lineups.evaluate import FIVE

FITS = (paths.CACHE / "asof_points_2026" / "origins", paths.CACHE / "additive_origin_fits_2026_10_09")
CENTERED = paths.CACHE / "asof_points_centered_2026" / "origins"
BINS = np.array([0, 1, 2, 3, 4, 6, 8, 10, 13, 99])     # experience years (aging_curve.BINS)
N_BINS = len(BINS) - 1
PARTS = ("base", "carry", "experience")
HALF_LIFE = 365.
MIN_CELLS, MIN_POSSESSIONS = 30, 50


class _Legacy:
    """Stand-in for pickled pre-refactor classes (the snapshot's PlayerMap); its fields are not read."""

    def __init__(self, *args, **kwargs):
        pass


class _Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        return _Legacy if module.startswith("experiments") else super().find_class(module, name)


def snapshot(origin_tag):
    for directory in FITS:
        path = directory / origin_tag / "fit.pkl"
        if path.exists():
            with path.open("rb") as f:
                return _Unpickler(f).load()["snapshot"]
    raise FileNotFoundError(f"no additive fit for {origin_tag}; run scripts/additive_origin_fit.py")


def player_parts(snap, fives, season, side):
    """Known mask and per-player parts (points/100) for [..., 5] player ids on one side."""
    ids = np.asarray(snap["sorted_ids"], np.int64)
    n = len(ids) + 1                                     # slot 0 is the unseen-player bucket
    half = slice(0, n) if side == "offense" else slice(n, 2 * n)
    theta = np.asarray(snap["theta"], float)[half]
    delta = np.asarray(snap["delta"], float)[half]
    eta = np.asarray(snap["eta"], float)[:N_BINS] if side == "offense" else np.asarray(snap["eta"], float)[N_BINS:]
    reference = np.asarray(snap["reference_year"], float)
    fives = np.asarray(fives, np.int64)
    position = np.clip(np.searchsorted(ids, fives), 0, len(ids) - 1)
    known = ids[position] == fives
    slot = np.where(known, position + 1, 0)
    years = float(season) - reference[slot]
    graded = known & np.isfinite(years)
    bucket = np.clip(np.digitize(np.where(graded, years, 0.), BINS) - 1, 0, N_BINS - 1)
    parts = dict(base=100. * np.where(known, theta[slot], 0.),
                 carry=100. * np.where(known, float(snap["rho"]) * delta[slot], 0.),
                 experience=100. * np.where(graded, eta[bucket], 0.))
    return known, parts


# ---- calibrations (steps 4-6) -----------------------------------------------------
def _completed(history, start):
    return history[pd.to_datetime(history.window_stop).to_numpy() <= pd.Timestamp(start)]


def point_calibration(history, start):
    """(a, b >= 0) for league + a + b x score; identity below MIN_CELLS cells."""
    h = _completed(history, start)
    if len(h) < MIN_CELLS:
        return dict(a=0., b=1., n_cells=len(h))
    w = np.sqrt(h.possessions.to_numpy(float))
    design = np.column_stack([np.ones(len(h)), h.score.to_numpy(float)]) * w[:, None]
    fit = lsq_linear(design, (h.actual - h.league).to_numpy(float) * w, bounds=([-np.inf, 0.], [np.inf, np.inf]),
                     method="trf")
    return dict(a=float(fit.x[0]), b=float(fit.x[1]), n_cells=len(h))


def defense_slope(history, start):
    h = _completed(history, start)
    if h.empty:
        return dict(slope=1., n_cells=0)
    d, w, y = h.defense_raw.to_numpy(), h.possessions.to_numpy(), (h.actual - h.additive).to_numpy()
    denominator = float(w @ (d * d))
    return dict(slope=float(np.clip(w @ (d * y) / denominator, 0, 2)) if denominator > 0 else 1., n_cells=len(h))


def affine(history, start):
    """(intercept, slope >= 0) for league + intercept + slope x (forecast - league)."""
    h = _completed(history, start)
    if len(h) < MIN_CELLS:
        return dict(intercept=0., slope=1., n_cells=len(h))
    w, x, y = h.possessions.to_numpy(float), (h.forecast - h.league).to_numpy(float), (h.actual - h.league).to_numpy(float)
    xm, ym = np.average(x, weights=w), np.average(y, weights=w)
    den = w @ (x - xm) ** 2
    slope = max(float(w @ ((x - xm) * (y - ym)) / den), 0.) if den > 1e-12 else 0.
    return dict(intercept=float(ym - slope * xm), slope=slope, n_cells=len(h))


@lru_cache(maxsize=1)
def offense_history():
    """Saved centered-additive cells for every 2015-2026 origin (the step-4 cohort)."""
    frames = [pd.read_csv(CENTERED / tag / "cells.csv.gz").query("arm == 'additive|base'")
              for tag in legacy.origins().tag]
    return pd.concat(frames, ignore_index=True)[["window_stop", "score", "actual", "league", "possessions"]]


@lru_cache(maxsize=1)
def defense_history():
    """Saved v15 control cells (the step-5 cohort)."""
    cells = pd.read_csv(paths.V15_ARCHIVE / "controls" / "cells.csv.gz")
    return cells[["window_stop", "defense_raw", "actual", "additive", "possessions"]]


@lru_cache(maxsize=1)
def blend_history(seed=17):
    """Offense-five cells with >= 50 possessions per 2015-2026 origin, with the step-5 forecast (step-6 cohort)."""
    g, frames = legacy.matchups(), []
    for origin in legacy.origins().itertuples():
        with np.load(paths.V16_CONTROLS / origin.tag / f"s{seed}" / "groups.npz") as z:
            rows = z["row"]
            forecast = z["inherited"][:, z["models"].tolist().index("additive_defense")]
            league = z["league"]
        f = pd.DataFrame(np.asarray(g["pids"][rows]), columns=FIVE)
        w = np.asarray(g["possessions"][rows], float)
        f["possessions"], f["points"], f["forecast"], f["league"] = w, np.asarray(g["points"][rows]), forecast * w, league * w
        f = f.groupby(FIVE, as_index=False, sort=True).sum()
        f["actual"] = 100 * f.points / f.possessions
        f["forecast"] /= f.possessions
        f["league"] /= f.possessions
        f["window_stop"] = str(origin.stop.date())
        frames.append(f[f.possessions >= MIN_POSSESSIONS])
    return pd.concat(frames, ignore_index=True)


# ---- the control at one origin ---------------------------------------------------------
class Additive:
    """additive_defense at one origin; ``schedule`` must contain the origin's tag (Store.schedule() for 2027q1)."""

    def __init__(self, origin_tag, schedule=None, g=None):
        schedule = legacy.schedule() if schedule is None else schedule
        origin = schedule.query("tag == @origin_tag").iloc[0]
        self.tag, self.season, self.start = origin_tag, int(origin.season), pd.Timestamp(origin.start)
        self.snapshot = snapshot(origin_tag)
        g = legacy.matchups() if g is None else g
        cutoff = legacy.day(self.start)
        prior = np.flatnonzero(np.asarray(g["date"]) < cutoff)
        w = np.exp2(-(cutoff - np.asarray(g["date"][prior], float)) / HALF_LIFE)
        possessions = w * np.asarray(g["possessions"][prior], float)
        self.league = float(100 * (w @ np.asarray(g["points"][prior], float)) / possessions.sum())
        self.means = {}
        for side, key in (("offense", "pids"), ("defense", "defense")):
            exposure = np.bincount(np.asarray(g[key][prior]).ravel(), weights=np.repeat(possessions, 5))
            ids = np.flatnonzero(exposure)
            known, parts = player_parts(self.snapshot, ids[:, None], self.season, side)
            if not known.all():
                raise ValueError(f"{origin_tag}: a prior {side} player is missing from the snapshot")
            self.means[side] = {p: float(np.average(parts[p][:, 0], weights=exposure[ids])) for p in PARTS}
        self.offense_calibration = point_calibration(offense_history(), self.start)
        self.defense_calibration = defense_slope(defense_history(), self.start)
        self.blend = affine(blend_history(), self.start)

    def score(self, fives, side):
        """Centered score: the sum of the five players' centered parts (points/100)."""
        known, parts = player_parts(self.snapshot, fives, self.season, side)
        centered = sum(np.where(known, parts[p] - self.means[side][p], 0.) for p in PARTS)
        return centered.sum(-1)

    def points(self, offense, defense=None):
        """additive_defense points/100 for [B,5] offenses against [B,5] defenses (None: league-average defense)."""
        c = self.offense_calibration
        forecast = self.league + c["a"] + c["b"] * self.score(offense, "offense")
        if defense is not None:
            forecast = forecast + self.defense_calibration["slope"] * self.score(defense, "defense")
        return self.league + self.blend["intercept"] + self.blend["slope"] * (forecast - self.league)
