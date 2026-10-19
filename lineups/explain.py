"""Basketball explanations of a forecast (docs/CLOSEOUT.md, step 5).

Everything here reads the release model's expected ledger (arm R, the mixture
of every checkpoint of every seed). It is accounting on the model's own
numbers, not causal credit (rule of evidence 7).

**Team channels.** The lineup is compared with a reference: the league-average
offense, which is the average-opponent panel's offenses against its defenses.
For a specific opponent, the reference is the same lineup against the
league-average defense, so the channels show what that defense does. Points per
100 telescope into:

    volume       field-goal attempts per possession (turnovers, free-throw trips
                 and offensive rebounds move it)
    shot mix     where the attempts come from
    conversion   make rates by location
    free throws  free throws made

The four parts sum to the native difference. They are scaled by the mean
calibration slope so that they sum to the calibrated difference the tool shows.

**Players.**
- Each player's share of the lineup's opportunities (FGA + 0.44 FTA + TO).
- His "usual" share: the split if every player kept his own dated rate.
- The difference is how far the lineup pushes him out of his usual role.

**Creation.** Assisted-finishing demand against passing supply, per 100
possessions (the creation constraint's own inputs).

``rates`` is the offense's raw ledger per possession; the combination layer
(lineups.combinations) values its event changes at these rates.
"""
from functools import cached_property

import numpy as np
import torch

from lineups.model import SHOT_VALUES, USAGE_WEIGHTS, average_ledgers
from lineups.release import FORECAST, SEEDS

LOCATIONS = ("rim", "paint", "mid-range", "long mid-range", "corner three", "above-break three")
VALUES = np.array(SHOT_VALUES)


def team(ledger, weights=None):
    """Possession ledger per 100 for a batch of rows, averaged with weights (default: the first row)."""
    w = np.array([1.]) if weights is None else np.asarray(weights, float)
    n = len(w)
    avg = lambda x: (w @ x.double().numpy()[:n].reshape(n, -1)).reshape(x.shape[1:]) if x.ndim > 1 else float(w @ x.double().numpy()[:n])
    attempts, makes = avg(ledger.expected_attempts.sum(1)), avg(ledger.expected_makes.sum(1))
    return dict(points=avg(ledger.points100) / 100, fga=avg(ledger.fga.sum(1)), fta=avg(ledger.fta.sum(1)),
                tov=avg(ledger.turnover.sum(1)), ftm=avg((ledger.fta * ledger.ft_make).sum(1)),
                orb=avg(ledger.orb), attempts=attempts, makes=makes)


def channels(lineup, reference, slope):
    """Telescoping decomposition of lineup minus reference points per 100 (calibrated units)."""
    a0, a1 = reference["attempts"], lineup["attempts"]
    m0, m1 = reference["makes"] / a0, lineup["makes"] / a1
    s0, s1 = a0 / a0.sum(), a1 / a1.sum()
    f0, f1 = reference["fga"], lineup["fga"]
    parts = dict(volume=(f1 - f0) * (s0 * m0 * VALUES).sum(), shot_mix=f1 * ((s1 - s0) * m0 * VALUES).sum(),
                 conversion=f1 * (s1 * (m1 - m0) * VALUES).sum(), free_throws=lineup["ftm"] - reference["ftm"])
    return {k: 100 * slope * v for k, v in parts.items()}


def summary(t):
    """Readable team numbers per 100 possessions."""
    share = t["attempts"] / t["attempts"].sum()
    fg = t["makes"] / t["attempts"]
    return dict(fga=100 * t["fga"], fta=100 * t["fta"], turnovers=100 * t["tov"],
                offensive_rebounds=100 * t["orb"], three_share=float(share[4:].sum()), rim_share=float(share[0]),
                rim_fg=float(fg[0]), three_fg=float((t["makes"][4:]).sum() / t["attempts"][4:].sum()))


class Explainer:
    def __init__(self, release):
        self.release = release
        self.slope = float(np.mean([release.record["calibration"][f"{FORECAST}_s{s}"]["slope"] for s in SEEDS]))

    def ledger(self, offense_rows, defense_rows, arm=FORECAST):
        inputs = self.release.inputs(offense_rows, defense_rows)
        return average_ledgers(self.release.season_ledgers(arm, inputs)), inputs

    def creation(self, rows, arm=FORECAST):
        """Assisted-finishing demand and passing supply per 100 vs the panel defenses: each seed's checkpoint
        mean, then the seed mean (the release's mixture)."""
        defenses, w = self.release.panel_rows["defense"]
        inputs = self.release.inputs(np.repeat(np.asarray(rows)[None], len(defenses), 0), defenses)
        demand, supply = [], []
        with torch.no_grad():
            for s in SEEDS:
                d, u = [], []
                for m in self.release.models[arm][s]:
                    phase = m(inputs, self.release.env).phase
                    d.append(w @ phase.demand.double().sum(1).numpy())
                    u.append(w @ phase.supply.double().sum(1).numpy())
                demand.append(np.mean(d))
                supply.append(np.mean(u))
        return 100 * float(np.mean(demand)), 100 * float(np.mean(supply))

    @cached_property
    def league(self):
        """The league-average offense: panel offenses against panel defenses."""
        offenses, wo = self.release.panel_rows["offense"]
        defenses, wd = self.release.panel_rows["defense"]
        total, block = None, 16
        for lo in range(0, len(offenses), block):
            o = offenses[lo:lo + block]
            led, _ = self.ledger(np.repeat(o, len(defenses), 0), np.tile(defenses, (len(o), 1)))
            t = team(led, np.outer(wo[lo:lo + block], wd).ravel())
            total = t if total is None else {k: total[k] + v for k, v in t.items()}
        return total

    def players(self, ledger, inputs, weights, rows):
        n = len(weights)
        avg = lambda x: weights @ x.double().numpy()[:n]
        load = avg(ledger.fga + USAGE_WEIGHTS[1] * ledger.fta + ledger.turnover)
        base = inputs["base"].double().numpy()[0]
        own = np.exp(np.clip(base[:, :3], -12, 4)) @ np.array(USAGE_WEIGHTS)
        usual = own / own.sum()
        attempts = (weights[:, None, None] * ledger.expected_attempts.double().numpy()[:n]).sum(0)
        points = avg(ledger.player_points)
        t = self.release.seasons.table
        out = []
        for i, r in enumerate(np.asarray(rows)):
            out.append(dict(player=self.release.seasons.names[int(t["pid"][r])], season=int(t["season"][r]),
                            usage_share=float(load[i] / load.sum()), usual_share=float(usual[i]),
                            points=100 * float(points[i]), threes=100 * float(attempts[i, 4:].sum()),
                            rim_attempts=100 * float(attempts[i, 0])))
        return out

    def lineup(self, rows):
        """Explanation of one five against the league-average defense."""
        rows = np.asarray(rows, np.int64)
        defenses, w = self.release.panel_rows["defense"]
        led, inputs = self.ledger(np.repeat(rows[None], len(defenses), 0), defenses)
        mine = team(led, w)
        demand, supply = self.creation(rows)
        return dict(team=summary(mine), league=summary(self.league), channels=channels(mine, self.league, self.slope),
                    players=self.players(led, inputs, w, rows), creation=dict(demand=demand, supply=supply), rates=mine)

    def against(self, rows, opponent_rows):
        """What a specific defense does to this offense, relative to the league-average defense."""
        rows, opponent_rows = np.asarray(rows, np.int64), np.asarray(opponent_rows, np.int64)
        defenses, w = self.release.panel_rows["defense"]
        base_led, _ = self.ledger(np.repeat(rows[None], len(defenses), 0), defenses)
        led, inputs = self.ledger(rows[None], opponent_rows[None])
        mine, average = team(led), team(base_led, w)
        return dict(team=summary(mine), average_defense=summary(average), channels=channels(mine, average, self.slope),
                    players=self.players(led, inputs, np.array([1.]), rows), rates=mine)
