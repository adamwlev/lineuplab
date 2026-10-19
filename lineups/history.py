"""The release's history: forecasts and fits at each 2015-2026 quarter origin (2026-10-16).

The active cache root (lineups.paths) picks the history, so a producer that reads it here writes results that
match its root's data:
- the main cache: the saved v16 reference for arm R (J_POINT_BOTH, warm-started from v14 parents) and the
  confirmatory capacity run for arm C, both trained on the old data;
- the clean root (LINEUPS_CACHE = paths.CLEAN): the refresh on the clean data, two-phase from scratch exactly as
  the release fits (scripts/era_run.py --campaign history; reports/refresh_protocol_2026_10_16.md).

The dated league level is the same in both (league_at); on the old data it equals the saved controls' league.
"""
import numpy as np
import torch

from lineups import legacy, paths

CLEAN = paths.CLEAN_ROOT
RUN = paths.CACHE / "history_2026_10_16"                   # the clean root's history
CAPACITY = paths.CACHE / "capacity_v2_run_2026_10_09"      # the main cache's arm C
DEFENSE = dict(R="broadcast", C="capacity")


def case_dir(tag, arm, seed):
    """A clean-root history fit (scripts/era_run.py --campaign history)."""
    return RUN / "origins" / tag / arm / f"s{seed}"


def native(tag, seed, view="checkpoint_average", arm="R"):
    """Per-row native points/100 at one origin: 'direct' (the final fit) or 'checkpoint_average'."""
    if CLEAN:
        path = case_dir(tag, arm, seed) / "forecast.npz"
    elif arm == "R":
        return legacy.native(tag, "J_POINT_BOTH", seed, view)
    else:
        path = CAPACITY / "origins" / tag / f"s{seed}" / "forecast.npz"
    with np.load(path) as z:
        return z["row"].copy(), z[view].astype(float)


def league_at(g, cutoff):
    """Possession-weighted points/100 of the matchups before cutoff (a day number), one-year half-life."""
    d = np.asarray(g["date"])
    rows = np.flatnonzero(d < cutoff)
    w = np.exp2(-(cutoff - d[rows]) / 365.)
    return float(100 * (w @ np.asarray(g["points"][rows], float)) / (w @ np.asarray(g["possessions"][rows], float)))


def _clean_fit(tag, arm, seed):
    from lineups.model import EventModel
    fit = torch.load(case_dir(tag, arm, seed) / "fit.pt", map_location="cpu", weights_only=False)
    offense = EventModel.offense_only(seed)
    offense.load_state_dict(fit["offense_final"])

    def build(state):
        m = EventModel.from_offense(offense, seed, DEFENSE[arm])
        m.load_state_dict(state)
        return m.eval()
    return fit, build


def final_model(tag, seed, arm="R"):
    """The arm's final fit at one origin (the 'direct' view), in eval mode."""
    if CLEAN:
        fit, build = _clean_fit(tag, arm, seed)
        return build(fit["final"])
    if arm != "R":
        raise NotImplementedError("the main cache's arm C fits are read through scripts/capacity_run.py")
    from lineups.model import load_legacy
    state = torch.load(paths.V16_RUN / "origins" / tag / "J_POINT_BOTH" / f"s{seed}" / "final" / "fit.pt",
                       map_location="cpu", weights_only=False)["state_dict"]
    return load_legacy(state)


def final_references(tag, seed, store, arm="R"):
    """The loss references the arm's final fit trained with; a module trained on top uses the same."""
    if CLEAN:
        return torch.load(case_dir(tag, arm, seed) / "fit.pt", map_location="cpu", weights_only=False)["references"]["final"]
    return store.references[f"{tag}/final/s{seed}"]


def checkpoint_models(tag, seeds=legacy.SEEDS, arm="R"):
    """Every saved checkpoint of the arm at one origin, across seeds (the checkpoint-average mixture)."""
    if not CLEAN:
        if arm != "R":
            raise NotImplementedError("the main cache's arm C fits are read through scripts/capacity_run.py")
        from lineups.coherence import checkpoint_models as legacy_models
        return legacy_models(tag, seeds=seeds)
    models = []
    for seed in seeds:
        fit, build = _clean_fit(tag, arm, seed)
        models += [build(state) for state in fit["checkpoints"]]
    return models
