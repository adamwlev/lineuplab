"""Out-of-support reasons for hypothetical lineups (pillar 3).

A forecast for a lineup unlike anything the model trained on is extrapolation,
and the band must say so in basketball terms. ``Support`` compares a lineup
with the real fives that played in an origin's training window (the five years
before it), all looked up with origin-dated states:

    defensive composition  Mahalanobis distance of the defenders' standardized
                           descriptor mean and SD (the broadcast defense's own
                           input) from the real defensive fives
    offensive composition  the same for the attackers' standardized states
    no ball handler        best passer's assist rate below every real five's
    no shooter             most frequent shooter's 3PA rate below every real five's
    non-spacing bigs       more non-spacing bigs (listed height >= 82 in, < 1
                           3PA per 100) than any real five
    repeated player        the same player more than once

"Beyond observed" means beyond the largest value among real fives with at least
MIN_POSSESSIONS possessions in the window, so a reason fires only where no
trained lineup reaches. Distances are reported as percentiles of the real fives.
"""
import numpy as np

from lineups import legacy
from lineups.features import HEIGHT_SCALE

MIN_POSSESSIONS = 25
BIG_INCHES, NON_SHOOTER = 82, 1.
LOOKBACK_DAYS = 5 * 365


def _inverse_covariance(x, ridge=1e-3):
    return np.linalg.inv(np.cov(x, rowvar=False) + ridge * np.eye(x.shape[1]))


class Support:
    def __init__(self, store, origin_tag, g=None):
        g = legacy.matchups() if g is None else g
        origin = store.schedule().query("tag == @origin_tag").iloc[0]
        start = legacy.day(origin.start)
        rows = np.flatnonzero((np.asarray(g["date"]) < start) & (np.asarray(g["date"]) >= start - LOOKBACK_DAYS))
        self.store, self.tag, self.origin_index = store, origin_tag, int(origin.origin_index)
        self.normalizer = store.normalizer(origin_tag, "final")
        possessions = np.asarray(g["possessions"][rows])
        self.real = {}
        for side, column in (("offense", "pids"), ("defense", "defense")):
            fives = np.sort(np.asarray(g[column][rows]), 1)
            units, inverse = np.unique(fives, axis=0, return_inverse=True)
            weight = np.bincount(inverse.ravel(), possessions, len(units))
            self.real[side] = units[weight >= MIN_POSSESSIONS]
        self.reference = {}
        for side in ("offense", "defense"):
            z = self._composition(self.real[side], side)
            self.reference[side] = dict(mean=z.mean(0), inverse=_inverse_covariance(z))
            self.reference[side]["distance"] = np.sort(self._distance(z, side))
        roles = self.roles(self.real["offense"])
        self.limits = dict(best_passer=roles["best_passer"].min(), best_shooter=roles["best_shooter"].min(),
                           nonspacing_bigs=roles["nonspacing_bigs"].max())

    # ---- lineup features --------------------------------------------------------
    def _composition(self, fives, side, values=None):
        """[mean, SD] over the five of standardized states; values: raw states [B,5,F] instead of a lookup."""
        n = self.normalizer
        if side == "offense":
            base = self.store.offense(fives, origin_index=self.origin_index)["base"] if values is None else values
            x = (base - n["base_mean"]) / np.maximum(n["base_sd"], 1e-6)
        else:
            raw = self.store.defense(fives, origin_index=self.origin_index) if values is None else values
            x = (raw - n["defense_mean"]) / n["defense_scale"]
        return np.concatenate([x.mean(1), x.std(1)], -1).astype(float)

    def _distance(self, z, side):
        r = self.reference[side]
        d = z - r["mean"]
        return np.sqrt(np.einsum("...i,ij,...j->...", d, r["inverse"], d))

    def roles(self, fives, base=None):
        if base is None:
            base = self.store.offense(fives, origin_index=self.origin_index)["base"]
        base = np.asarray(base, float)
        loc = np.exp(base[..., 3:9] - base[..., 3:9].max(-1, keepdims=True))
        loc /= loc.sum(-1, keepdims=True)
        three = 100 * np.exp(np.clip(base[..., 0], -12, 4)) * loc[..., 4:].sum(-1)
        assist = 100 * np.exp(np.clip(base[..., 16], -12, 4))
        players = self.store.players
        height = (players["height"][fives] if players is not None
                  else np.full(np.shape(fives), HEIGHT_SCALE[0]))
        return dict(best_passer=assist.max(-1), best_shooter=three.max(-1),
                    nonspacing_bigs=((height >= BIG_INCHES) & (three < NON_SHOOTER)).sum(-1))

    # ---- report -----------------------------------------------------------------
    def describe(self, offense, defense, offense_base=None, defense_states=None):
        """Distances, role values and the reasons that fire for one matchup.

        offense_base [5,18] and defense_states [5,19] replace the origin lookup
        (player-seasons from other origins, already expressed in this origin's terms).
        """
        offense, defense = np.asarray([offense], np.int64), np.asarray([defense], np.int64)
        given = dict(offense=None if offense_base is None else np.asarray(offense_base)[None],
                     defense=None if defense_states is None else np.asarray(defense_states)[None])
        out, reasons = {}, []
        for side, five in (("offense", offense), ("defense", defense)):
            d = float(self._distance(self._composition(five, side, given[side]), side)[0])
            real = self.reference[side]["distance"]
            out[f"{side}_distance"] = d
            out[f"{side}_percentile"] = float(np.searchsorted(real, d) / len(real))
            if d > real[-1]:
                reasons.append(f"{side} composition beyond every trained lineup (distance {d:.1f}, max {real[-1]:.1f})")
        r = {k: float(v[0]) for k, v in self.roles(offense, given["offense"]).items()}
        out.update(r)
        if r["best_passer"] < self.limits["best_passer"]:
            reasons.append(f"no ball handler: best passer {r['best_passer']:.1f} assists/100, "
                           f"below every trained lineup ({self.limits['best_passer']:.1f})")
        if r["best_shooter"] < self.limits["best_shooter"]:
            reasons.append(f"no shooter: best 3PA rate {r['best_shooter']:.1f}/100, below every trained lineup")
        if r["nonspacing_bigs"] > self.limits["nonspacing_bigs"]:
            reasons.append(f"{int(r['nonspacing_bigs'])} non-spacing bigs, more than any trained lineup "
                           f"({int(self.limits['nonspacing_bigs'])})")
        for side, five in (("offense", offense[0]), ("defense", defense[0])):
            if len(set(five.tolist())) < 5:
                reasons.append(f"{side} repeats a player")
        out["reasons"] = reasons
        return out
