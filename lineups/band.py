"""The uncertainty band and its reasons (docs/CLOSEOUT.md, step 4).

The point is the release forecast (arm R) plus, when given, the learned
combinations (lineups.learned, half strength) and the measured combination
effects (lineups.combinations). The band is the union over named assumptions
of each assumption's interval:

    interval(a) = point(a) +- Z * sqrt(model error variance)

**Assumption arms** (lineups.release):
- R, the reference;
- C, capacity defense: rim protection reads the two best inside defenders, and
  each attacker is matched with one defender.

They nearly agree on real lineups and differ where the data cannot choose, so
their spread is assumption-based and labeled as such. With the combination
layer, both arms carry it, and a third value K is arm R with the layer's
alternative: combination effects keep adding pair by pair past the measured
counts. With the learned combinations, every value carries them, and N is the
forecast without them: players add up apart from the measured effects. An
offense-side
creation-conservation arm was screened and dropped, because real lineups
contradict it (reports/creation_law_screen_2026_10_12.md).

**Model error variance** has two parts:
- TAU: the persistent discrepancy between a real lineup's rating and the
  forecast. It is estimated on 2016-2026 from split halves
  (scripts/band_in_support.py): about 3.2 per side and 4.5 on the margin, in
  points per 100.
- CROSS_ERA_VARIANCE: the excess error when the release model forecasts
  another era's lineups, which is the tool's direction (scripts/cross_era.py,
  direction A). It is about 4.0 (points per 100)² per side under the
  era-relative input rule and 5.3 as-was. It is scaled by the share of the
  five's player-seasons from before the release's training seasons.

Z = 1.28: an 80% band. Finite-game coverage on real lineups checks the
in-support part only. Nothing validates the assumption part; it states what
follows if each named assumption holds.

**Reasons.**
- Composition and role limits (lineups.support), with each player compared
  against his own season's players.
- Repeated players.
- Thin player data.
- Cross-era use.
- The capacity assumption, when it moves the margin by more than
  SPREAD_REASON points, with its mechanism.
- Combination effects carried past the measured counts.
- The learned combinations, when they move the margin by more than
  SPREAD_REASON points.
"""
import json

from lineups.combinations import PLURALS
import numpy as np
from lineups.release import ORIGIN, Release
from lineups.sources import SOURCE
from lineups.support import Support

ARMS = ("R", "C")
Z = 1.28
TAU2 = dict(offense=10.25, defense=10.45, margin=19.83)    # scripts/band_in_support.py, 2016-2026
CROSS_ERA_VARIANCE = dict(relative=4.0, as_was=5.3)      # scripts/cross_era.py, direction A, per side
CROSS_ERA_CORRELATION = dict(relative=.88, as_was=.84)    # share of in-era within-quarter correlation
if SOURCE["band"] is not None:                            # the refresh's, on the clean data (lineups.sources;
    _refreshed = json.loads(SOURCE["band"].read_text())   # scripts/refresh_constants.py)
    TAU2, CROSS_ERA_VARIANCE, CROSS_ERA_CORRELATION = (_refreshed[k] for k in ("tau2", "cross_era_variance",
                                                                               "cross_era_correlation"))
FIRST_TRAINING_SEASON = 2022                              # release rows start 2021-10-20
THIN_POSSESSIONS = 500
SPREAD_REASON = 1.


class Band:
    def __init__(self, release=None):
        self.release = release or Release()
        self.seasons = self.release.seasons
        self.support = Support(self.release.store, ORIGIN, self.release.matchups)
        self.cross_era = CROSS_ERA_VARIANCE[self.release.rule]

    # ---- pieces -----------------------------------------------------------------
    def cross_era_share(self, rows):
        return float(np.mean(self.seasons.table["season"][np.asarray(rows)] < FIRST_TRAINING_SEASON))

    def player_reasons(self, rows, label):
        t, reasons = self.seasons.table, []
        rows = np.asarray(rows)
        pids = t["pid"][rows]
        if len(set(pids.tolist())) < 5:
            reasons.append(f"{label} repeats a player")
        for r in rows:
            if t["offense_possessions"][r] < THIN_POSSESSIONS:
                reasons.append(f"thin player data: {self.seasons.names[int(t['pid'][r])]} played "
                               f"{int(t['offense_possessions'][r])} offensive possessions in {int(t['season'][r])}")
        old = sorted({int(s) for s in t["season"][rows] if s < FIRST_TRAINING_SEASON})
        if old:
            reasons.append(f"cross-era: {label} uses {', '.join(map(str, old))} player-seasons in a model trained on "
                           f"{FIRST_TRAINING_SEASON}-{self.seasons.latest}; across eras the model ranks real lineups "
                           f"with about {CROSS_ERA_CORRELATION[self.release.rule]:.0%} of its in-era correlation, "
                           f"and levels across eras are not validated")
        return reasons

    def composition_reasons(self, offense_rows, defense_rows):
        base, _ = self.seasons.relative(offense_rows)
        _, states = self.seasons.relative(defense_rows)
        pid = self.seasons.table["pid"]
        d = self.support.describe(pid[np.asarray(offense_rows)], pid[np.asarray(defense_rows)],
                                  offense_base=base, defense_states=states)
        return [r for r in d["reasons"] if "repeats a player" not in r], d

    # ---- the band -----------------------------------------------------------------
    @staticmethod
    def with_layer(by_arm, keys, layer, learned=None):
        """{key: {assumption: value}}: the arms with the combination layer and the learned combinations; K, arm R
        with the layer's continued alternative; N, arm R with the layer but without the learned combinations."""
        add = lambda k: learned[k] if learned is not None else 0.
        values = {k: {a: by_arm[a][k] + add(k) for a in ARMS} for k in keys}
        if layer is not None:
            values = {k: {**{a: v + layer["layer"][k] for a, v in values[k].items()},
                          "K": by_arm["R"][k] + layer["continued"][k] + add(k)} for k in keys}
        if learned is not None:
            for k in keys:
                values[k]["N"] = by_arm["R"][k] + (layer["layer"][k] if layer is not None else 0.)
        return values

    @staticmethod
    def learned_reasons(learned, key, label):
        if learned is None or abs(learned[key]) <= SPREAD_REASON:
            return []
        return [f"assumption N: the learned combinations move the {label} {learned[key]:+.1f}. They are learned from "
                "real lineups at half strength and are not validated one by one; without them the players add up, "
                "apart from the measured combination effects."]

    @staticmethod
    def combination_reasons(layer, key, label):
        if layer is None or not layer["beyond"]:
            return []
        past = "; ".join(f"{b['count']} {PLURALS[b['type']]} on {b['side']} (measured up to {b['measured']})"
                         for b in layer["beyond"])
        moved = layer["continued"][key] - layer["layer"][key]
        return [f"assumption K: combination effects are held at the most players of a type measured together: "
                f"{past}. If they keep adding pair by pair, the {label} moves {moved:+.1f}."]

    def interval(self, values, variance):
        sd = float(np.sqrt(variance))
        lo, hi = min(values.values()), max(values.values())
        return dict(point=values["R"], low=lo - Z * sd, high=hi + Z * sd, sd=sd,
                    assumption_low=lo, assumption_high=hi)

    def lineup(self, rows, layer=None, learned=None):
        """One five against the league-average panel: offense, defense and margin with bands and reasons.

        layer: lineups.combinations.Combinations.lineup output, added to every assumption.
        learned: lineups.release.Release.season_learned_ratings output, added to every assumption but N.
        """
        rows = np.asarray(rows, np.int64)
        by_arm = {a: self.release.season_ratings(rows, a) for a in ARMS}
        share = self.cross_era_share(rows)
        variance = dict(offense=TAU2["offense"] + self.cross_era * share,
                        defense=TAU2["defense"] + self.cross_era * share,
                        margin=TAU2["margin"] + 2 * self.cross_era * share)
        values = self.with_layer(by_arm, variance, layer, learned)
        out = {k: self.interval(values[k], variance[k]) for k in variance}
        out["arms"] = by_arm
        composition, detail = self.composition_reasons(rows, rows)
        reasons = composition + self.player_reasons(rows, "the lineup")
        reasons += self.assumption_reasons({a: by_arm[a]["margin"] for a in ARMS})
        reasons += self.combination_reasons(layer, "margin", "net")
        reasons += self.learned_reasons(learned, "margin", "net")
        out["reasons"], out["support"] = reasons, detail
        return out

    def matchup(self, a_rows, b_rows, layer=None, learned=None):
        """Team A against team B: each offense, the margin (A minus B), bands and reasons."""
        a_rows, b_rows = np.asarray(a_rows, np.int64), np.asarray(b_rows, np.int64)
        by_arm = {}
        for arm in ARMS:
            p = self.release.season_points([a_rows, b_rows], [b_rows, a_rows], arm)
            by_arm[arm] = dict(a_offense=float(p[0]), b_offense=float(p[1]), margin=float(p[0] - p[1]))
        sa, sb = self.cross_era_share(a_rows), self.cross_era_share(b_rows)
        side = TAU2["offense"] + TAU2["defense"]
        variance = dict(a_offense=side + self.cross_era * (sa + sb), b_offense=side + self.cross_era * (sa + sb),
                        margin=2 * TAU2["margin"] + 2 * self.cross_era * (sa + sb))
        values = self.with_layer(by_arm, variance, layer, learned)
        out = {k: self.interval(values[k], variance[k]) for k in variance}
        out["arms"] = by_arm
        reasons = []
        for label, mine, theirs in (("team A", a_rows, b_rows), ("team B", b_rows, a_rows)):
            composition, _ = self.composition_reasons(mine, theirs)
            reasons += [f"{label}: {r}" for r in composition if not r.startswith("defense")]
            reasons += self.player_reasons(mine, label)
        reasons += self.assumption_reasons({a: by_arm[a]["margin"] for a in ARMS})
        reasons += self.combination_reasons(layer, "margin", "margin")
        reasons += self.learned_reasons(learned, "margin", "margin")
        out["reasons"] = reasons
        return out

    def assumption_reasons(self, margins):
        moved = margins["C"] - margins["R"]
        if abs(moved) <= SPREAD_REASON:
            return []
        return [f"assumption C, capacity defense, moves the margin {moved:+.1f}: rim protection counts only the two "
                "best inside defenders, and each attacker is matched with one defender. The era backtest found "
                "real big defenses did better than this assumes, so it is a labeled alternative, not the forecast."]
