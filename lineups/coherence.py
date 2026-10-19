"""Hypothetical matchups: score any lineups against each other at an origin.

Players are looked up in origin mode: states frozen at the origin date, and
the population fallback for players without history. Repeated players (clones)
share one state. A matchup is scored in both directions, so the margin is
antisymmetric by construction. Native points are pre-calibration; the scorecard's
calibration and additive blend are separate steps (lineups.evaluate).

A neutral defense is five identical average defenders: zero standardized
defensive inputs, so every defensive effect is exactly zero.

Fixture lineups (named players, pids, scoring origin) come from the v16
registry in the frozen run manifest, in the main cache whatever the cache root
(paths.FIXTURES).
"""
import json

import numpy as np
import torch

from lineups import legacy, paths
from lineups.model import average_ledgers


def fixtures(manifest=paths.FIXTURES):
    """Registered named lineups: {name: dict(names, pids, scoring_origin)}."""
    registry = json.loads(paths.Path(manifest).read_text())["fixtures"]
    return {k: dict(names=v["names"], pids=list(map(int, v["pids"])), origin=v["scoring_origin"])
            for k, v in registry.items()}


def checkpoint_models(origin_tag, arm="J_POINT_BOTH", seeds=legacy.SEEDS, run=paths.V16_RUN):
    """Every saved checkpoint of a pre-refactor arm at one origin, across seeds (a mixture)."""
    from lineups.model import load_legacy
    models = []
    for seed in seeds:
        case = run / "origins" / origin_tag / arm / f"s{seed}" / "final"
        fit = torch.load(case / "fit.pt", map_location="cpu", weights_only=False)
        for epoch in fit["checkpoint_epochs"]:
            state = torch.load(case / f"checkpoint_{epoch:03d}.pt", map_location="cpu", weights_only=False)
            models.append(load_legacy(state["state_dict"]))
    return models


def batch(store, offense, defense, origin_tag):
    """Origin-mode model inputs for B lineups; offense/defense are [B,5] player ids."""
    origin = store.schedule().query("tag == @origin_tag").iloc[0]
    normalizer = store.normalizer(origin_tag, "final")
    offense, defense = np.asarray(offense, np.int64), np.asarray(defense, np.int64)
    return store.batch(offense, defense, np.full(len(offense), normalizer["cutoff_day"]), normalizer,
                       origin_index=int(origin.origin_index))


def neutral(inputs):
    return inputs | dict(defense=torch.zeros_like(inputs["defense"]),
                         adjusted_defense=torch.zeros_like(inputs["adjusted_defense"]))


def ledgers(models, store, offense, defense, origin_tag):
    """Expected ledgers for B offense fives; defense None means the neutral defense.

    models: one model, or a list of checkpoint models (their mixture).
    """
    inputs = batch(store, offense, offense if defense is None else defense, origin_tag)
    if defense is None:
        inputs = neutral(inputs)
    env = store.env(origin_tag, "final")
    models = models if isinstance(models, (list, tuple)) else [models]
    with torch.no_grad():
        preds = [m.eval()(inputs, env) for m in models]
    return preds[0] if len(preds) == 1 else average_ledgers(preds)


def ledger(models, store, offense, defense, origin_tag):
    """Expected ledger for one offense five against one defense five."""
    return ledgers(models, store, [offense], [defense], origin_tag)


def matchup(models, store, team_a, team_b, origin_tag):
    """Both directions and the native margin (A's offense minus B's offense, points/100)."""
    a = ledger(models, store, team_a, team_b, origin_tag)
    b = ledger(models, store, team_b, team_a, origin_tag)
    return dict(a_offense=float(a.points100[0]), b_offense=float(b.points100[0]),
                margin=float(a.points100[0] - b.points100[0]), a=a, b=b)
