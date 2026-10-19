"""The learned combination module in the release forecast (Adam, 2026-10-14).

Confirmed design (reports/learned_module_confirmation_results_2026_10_14.md,
the screens' ``frozen_fixed`` arm):
- each seed's frozen release network (arm R) carries a held pairwise module
  (lineups.model.PairInteractions, joint hold), trained on top of it for
  EPOCHS on the final training rows (scripts/release_module.py);
- the module's level is its possession-weighted mean effect on the previous
  quarter's real lineups (2026q4, inputs as of the origin). It is removed, so
  the module only moves a lineup relative to the league's current lineups;
- the forecast keeps SCALE of the centered module:
  native = network + SCALE * (network with module - network - level),
  calibrated by the seed's affine and averaged over seeds.

The adjustment is the same for every assumption in the band (like the
combination layer). The network-alone number stays visible.
"""
import json

import numpy as np
import torch

from lineups import paths
from lineups.sources import SOURCE
from lineups.model import PairInteractions, average_ledgers
from lineups.train import game_batches

DIR = SOURCE["modules"]       # lineups.sources
SCALE = .5
EPOCHS = 8
INIT_OFFSET = 1800                    # the module's initial weights: torch.manual_seed(seed + INIT_OFFSET)
FIELDS = ("points", "rim_share", "three_share", "tov", "fta")


def new_module(seed):
    with torch.random.fork_rng():
        torch.manual_seed(seed + INIT_OFFSET)
        return PairInteractions(hold="joint")


def rates(pred):
    """Points/100 and the four event rates per row from a ledger: rim and three shares of FGA, turnovers and
    FTA per possession."""
    att = pred.expected_attempts.double().sum(1).numpy()
    fga = att.sum(1)
    return dict(points=pred.points100.double().numpy(), rim_share=att[:, 0] / fga, three_share=att[:, 4:].sum(1) / fga,
                tov=pred.turnover.double().sum(1).numpy(), fta=pred.fta.double().sum(1).numpy())


def measure_holds(modules, data, rows, normalizer, log=print):
    """Set each held module's output ranges from its unclamped outputs on training rows."""
    offense, defense = [[] for _ in modules], [[] for _ in modules]
    with torch.no_grad():
        for ix in game_batches(data.game, rows):
            inputs, _, _ = data.batch(ix, normalizer)
            for i, held in enumerate(modules):
                o, d = held.eval()(inputs)
                offense[i].append(o)
                defense[i].append(d[:, 0])
    for i, b in enumerate(modules):
        b.bound_outputs(torch.cat(offense[i]), torch.cat(defense[i]))
        log(f"module {i}: player range width {float((b.player_bounds[1] - b.player_bounds[0]).mean()):.3f}, "
            f"lineup {float((b.lineup_bounds[1] - b.lineup_bounds[0]).mean()):.3f}, "
            f"defense {float((b.defense_bounds[1] - b.defense_bounds[0]).mean()):.3f}"
            + (f", radius lineup {float(b.lineup_radius):.2f} defense {float(b.defense_radius):.2f}"
               if b.hold == "joint" else ""))


def ledgers_with(models, module, inputs, env):
    """Checkpoint-mixture ledgers without and with the module (the module is detached again afterwards)."""
    with torch.no_grad():
        off = average_ledgers([m.eval()(inputs, env) for m in models])
        try:
            for m in models:
                m.pairs = module
            on = average_ledgers([m.eval()(inputs, env) for m in models])
        finally:
            for m in models:
                m.pairs = None
    return off, on


def level(models, module, data, rows, normalizer, env, origin_index, possessions):
    """Possession-weighted mean module effect (with minus without) on real rows, per field in FIELDS."""
    sums, total = {k: 0. for k in FIELDS}, 0.
    for ix in game_batches(data.game, rows):
        inputs, _, _ = data.batch(ix, normalizer, origin_index=origin_index)
        off, on = (rates(p) for p in ledgers_with(models, module, inputs, env))
        w = np.asarray(possessions[ix], float)
        for k in FIELDS:
            sums[k] += float(w @ (on[k] - off[k]))
        total += float(w.sum())
    return {k: v / total for k, v in sums.items()}


def path(seed, directory=None):
    return (directory or DIR) / f"module_s{seed}.pt"


def load(seed, directory=None):
    """A seed's trained module (eval mode) and its level, from directory (default DIR)."""
    saved = torch.load(path(seed, directory), map_location="cpu", weights_only=False)
    module = PairInteractions(hold="joint")
    module.load_state_dict(saved["module"])
    return module.eval(), saved["level"]
