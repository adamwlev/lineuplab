"""Measured combination effects: the nonlinear layer on the release forecast.

Protocol: reports/combination_layer_protocol_2026_10_13.md. Adam, 2026-10-13:
the tool is built around these effects, however small they are.

The network adds up players (reports/synergy_check_2026_10_12.md). The
interaction discovery (reports/interaction_discovery_results_2026_10_13.md)
found player-type combinations whose events differ from what adding up
implies, and that held up on held-out seasons. This layer carries them:

    effect k   a pair feature P_k (pairs of players of two types on one side)
               acting on one event (rim share, three share, turnovers, FTA)
    layer      sum_k beta_k * (P_k - linear projection of P_k on the type counts)

Only the part orthogonal to the type counts is used: what a model that adds up
players cannot express. scripts/combination_layer.py fits beta and the
projections and writes LAYER.

**Points** are accounting on the event changes (``values``), at the rates of
the offense the event belongs to.

**Beyond the measured counts** the forecast holds each type count at its
measured maximum (MEASURED_SHARE of 2022-2026 possessions reach it). The named
alternative K, "combination effects keep adding pair by pair", continues the
pairwise form and goes into the band. (The protocol had these the other way
round; the results report gives the reason for the swap.)

Small guards x rim anchor (H1) is pre-registered for 2026-27 and is not in the
layer. ``h1`` flags it as a labeled note.

Since 2026-10-14 the forecast also carries the learned combinations
(lineups.learned), and the layer is measured on the residuals of network plus
module, so the two do not count the same effect twice.
"""
import json
from functools import cached_property

import numpy as np

from lineups import paths
from lineups.sources import DATA, SOURCE

# Re-measured on top of the learned combinations (Adam, 2026-10-14; scripts/combination_layer.py --learned).
# The 2026-10-13 layer on the network alone: combination_layer_2026_10_13/layer.json.
LAYER = SOURCE["layer"]       # lineups.sources: the 2026-10-14 layer, or the refresh's on the clean data
OFFENSE = ("O_big", "O_small", "O_shooter", "O_nonshooter", "O_passer", "O_creator", "O_slasher", "O_crasher", "O_usage")
DEFENSE = ("D_big", "D_small", "D_rim", "D_hawk", "D_glass")
TYPES = dict(O_big=("height", "hi"), O_small=("height", "lo"), O_shooter=("three_rate", "hi"),
             O_nonshooter=("three_rate", "lo"), O_passer=("assist", "hi"), O_creator=("unassisted", "hi"),
             O_slasher=("rim_rate", "hi"), O_crasher=("crash", "hi"), O_usage=("usage", "hi"),
             D_big=("height", "hi"), D_small=("height", "lo"), D_rim=("block", "hi"), D_hawk=("steal", "hi"),
             D_glass=("drb", "hi"))
LABELS = dict(O_big="big", O_small="small", O_shooter="shooter", O_nonshooter="non-shooter", O_passer="passer",
              O_creator="self-creator", O_slasher="slasher", O_crasher="offensive rebounder", O_usage="high usage",
              D_big="big", D_small="small", D_rim="shot-blocker", D_hawk="ball hawk", D_glass="defensive rebounder")
PLURALS = dict(O_big="bigs", O_small="small players", O_shooter="shooters", O_nonshooter="non-shooters",
               O_passer="passers", O_creator="self-creators", O_slasher="slashers", O_crasher="offensive rebounders",
               O_usage="high-usage players", D_big="bigs", D_small="small defenders", D_rim="shot-blockers",
               D_hawk="ball hawks", D_glass="defensive rebounders")
EVENTS = ("rim_share", "three_share", "tov", "fta")
UNITS = dict(rim_share="pp of shots at the rim", three_share="pp of shots from three", tov="turnovers per 100",
             fta="free-throw attempts per 100")
# (event, side, first type, second type, title). Titles follow the joint fit: two pairs that held up alone
# are, once fitted with their neighbours, carried by the two-bigs and small-pair effects
# (reports/combination_layer_results_2026_10_13.md).
EFFECTS_2026_10_13 = (
    ("rim_share", "defense", "D_big", "D_big", "Bigs on defense: rim deterrence saturates"),
    ("rim_share", "defense", "D_big", "D_rim", "Bigs beside shot-blockers: nothing beyond the bigs effect"),
    ("rim_share", "defense", "D_rim", "D_glass", "Shot-blockers beside defensive rebounders: rim deterrence overlaps"),
    ("three_share", "offense", "O_big", "O_crasher", "Bigs beside offensive rebounders: one plays outside"),
    ("three_share", "offense", "O_nonshooter", "O_crasher", "Non-shooters beside offensive rebounders: one plays outside"),
    ("three_share", "offense", "O_crasher", "O_crasher", "Offensive rebounders together: one plays outside"),
    ("tov", "offense", "O_shooter", "O_creator", "Shooters beside self-creators: fewer turnovers"),
    ("tov", "offense", "O_slasher", "O_usage", "Slashers beside high-usage players: fewer turnovers"),
    ("tov", "offense", "O_nonshooter", "O_crasher", "Non-shooters beside offensive rebounders: fewer turnovers"),
    ("fta", "offense", "O_small", "O_small", "Small players together: more free throws drawn"),
    ("fta", "offense", "O_small", "O_passer", "Small players beside passers: more free throws drawn"),
    ("fta", "offense", "O_small", "O_creator", "Small players beside self-creators: nothing beyond the small-player effects"),
    ("fta", "defense", "D_big", "D_big", "Bigs on defense together: more free throws allowed"),
    ("fta", "defense", "D_small", "D_small", "Small defenders together: more free throws allowed"),
)
# The clean data's discovery (the refresh, 2026-10-18; the protocol keeps whatever survives on the clean data,
# reports/refresh_protocol_2026_10_16.md): the three turnover effects did not hold up, and bigs beside defensive
# rebounders did. In the clean joint fit, bigs beside shot-blockers, bigs beside defensive rebounders and small
# players beside self-creators are carried by their neighbours ("nothing beyond ..."), as before.
EFFECTS_CLEAN = tuple(e for e in EFFECTS_2026_10_13 if e[0] != "tov") + (
    ("rim_share", "defense", "D_big", "D_glass", "Bigs beside defensive rebounders: rim deterrence overlaps"),)
# (the title as exported for the refresh; in the joint fit it is carried by its neighbours, -0.11 (0.13), and the
# page shows "nothing beyond the bigs effect")
# The layer is fitted on the clean data at the clean root, and the refresh source serves it.
EFFECTS = EFFECTS_CLEAN if paths.CLEAN_ROOT or DATA == "refresh" else EFFECTS_2026_10_13
MEASURED_SHARE = .005          # a count is measured if at least this share of 2022-2026 possessions reach it
H1_SMALL, H1_ANCHOR, H1_BLOCK = 75, 81, .9   # reports/prospective_h1_small_guards_anchor_2026_10_12.md


def effect_id(event, side, a, b):
    return f"{event}:{a}x{b}"


# ---- player types -------------------------------------------------------------------
def profile(base, rb_prob, defense, height):
    """The quantities the types are defined on, from raw offensive states, rebound prior and defensive descriptors."""
    base, defense = np.asarray(base, float), np.asarray(defense, float)
    e = lambda k: np.exp(np.clip(base[..., k], -12, 4))
    loc = np.exp(base[..., 3:9] - base[..., 3:9].max(-1, keepdims=True))
    loc /= loc.sum(-1, keepdims=True)
    return dict(height=np.asarray(height, float), three_rate=e(0) * loc[..., 4:].sum(-1), assist=e(16),
                unassisted=1 - 1 / (1 + np.exp(-base[..., 17])), rim_rate=e(0) * loc[..., 0],
                crash=np.asarray(rb_prob, float), usage=e(0) + .44 * e(1) + e(2),
                block=defense[..., 1], steal=defense[..., 0], drb=defense[..., 2])


def cutoffs(prof, at=None):
    """{quantity: (20th, 80th percentile)} over the players selected by ``at`` (default all)."""
    pick = (lambda v: v) if at is None else (lambda v: v[at])
    return {k: (float(np.quantile(pick(v), .2)), float(np.quantile(pick(v), .8))) for k, v in prof.items()}


def flags(prof, cut, names=OFFENSE + DEFENSE):
    """Boolean type flags [..., len(names)] for a profile, against cutoffs."""
    out = []
    for t in names:
        q, side = TYPES[t]
        lo, hi = cut[q]
        out.append(prof[q] >= hi if side == "hi" else prof[q] <= lo)
    return np.stack(out, -1)


# ---- pair features ----------------------------------------------------------------------
def pair_features(side_flags, names, pairs, measured_max=None):
    """Counts {type: [B]} and pair features {(a, b): [B]} for one side's flags [B,5,T].

    With measured_max, each count is capped at its measured maximum (the forecast).
    """
    side_flags = np.asarray(side_flags, bool)
    index = {t: i for i, t in enumerate(names)}
    n = {t: side_flags[..., index[t]].sum(-1).astype(float) for t in names}
    capped = n if measured_max is None else {t: np.minimum(v, measured_max[t]) for t, v in n.items()}
    out = {}
    for a, b in pairs:
        na, nb = capped[a], capped[b]
        if a == b:
            out[(a, b)] = na * (na - 1) / 2
        else:
            overlap = (side_flags[..., index[a]] & side_flags[..., index[b]]).sum(-1).astype(float)
            out[(a, b)] = na * nb - np.minimum(overlap, np.minimum(na, nb))
    return capped, out


# ---- points ------------------------------------------------------------------------------------
def values(fga, attempts, makes, shot_values, rim, three, ft, points, tov):
    """Points per 100 of one unit of each event (vectorized over leading dims).

    fga, ft (FT%), points and tov are per possession; attempts and makes are per
    zone [..., Z]; rim and three index the zones.
    - rim share, three share: one pp of FGA moved in from the other zones in
      proportion to their shares, at the lineup's make rates;
    - turnover: one per 100 costs the points of a non-turnover possession;
    - FTA: one per 100 is worth FT% minus half the points of a field-goal
      attempt (a trip of about two attempts replaces a shot).
    """
    attempts, makes = np.asarray(attempts, float), np.asarray(makes, float)
    share = attempts / attempts.sum(-1, keepdims=True)
    value = makes / np.maximum(attempts, 1e-12) * np.asarray(shot_values, float)
    per_fga = (share * value).sum(-1)

    def moved(zones):
        inside = np.zeros(share.shape[-1], bool)
        inside[list(zones)] = True
        s_in = share[..., inside].sum(-1)
        v_in = (share[..., inside] * value[..., inside]).sum(-1) / np.maximum(s_in, 1e-12)
        v_out = (share[..., ~inside] * value[..., ~inside]).sum(-1) / np.maximum(1 - s_in, 1e-12)
        return np.asarray(fga, float) * (v_in - v_out)

    return dict(rim_share=moved(rim), three_share=moved(three),
                tov=-np.asarray(points, float) / (1 - np.asarray(tov, float)),
                fta=np.asarray(ft, float) - .5 * per_fga)


def team_values(t):
    """``values`` for an explanation ledger (lineups.explain.team)."""
    from lineups.explain import VALUES
    return values(t["fga"], t["attempts"], t["makes"], VALUES, (0,), (4, 5), t["ftm"] / t["fta"], t["points"], t["tov"])


# ---- the layer ----------------------------------------------------------------------------
class Layer:
    """The fitted layer (scripts/combination_layer.py) applied to type flags."""

    def __init__(self, spec=None):
        self.spec = json.loads(LAYER.read_text()) if spec is None else spec
        self.measured_max = {t: int(v) for t, v in self.spec["measured_max"].items()}

    def terms(self, offense_flags, defense_flags, cap=True):
        """{effect id: (beta, pairs [B], expected pairs [B])} from [B,5,9] offense and [B,5,5] defense flags.

        Expected pairs: the linear projection on the type counts, i.e. what adding up players implies.
        """
        out = {}
        for event, e in self.spec["events"].items():
            for side, names, side_flags in (("offense", OFFENSE, offense_flags), ("defense", DEFENSE, defense_flags)):
                pairs = [tuple(p[1:]) for p in e["pairs"] if p[0] == side]
                if not pairs:
                    continue
                n, feats = pair_features(side_flags, names, pairs, self.measured_max if cap else None)
                for k, p in enumerate(e["pairs"]):
                    if p[0] != side:
                        continue
                    expected = e["intercept"][k] + sum(e["slopes"][k][j] * n[t] for j, t in enumerate(e["types"]) if t in n)
                    out[effect_id(event, side, *p[1:])] = (e["beta"][k], feats[tuple(p[1:])], expected)
        return out

    def deltas(self, offense_flags, defense_flags, cap=True):
        """{effect id: [B] event change}."""
        return {k: b * (P - x) for k, (b, P, x) in self.terms(offense_flags, defense_flags, cap).items()}

    @staticmethod
    def by_event(deltas):
        out = {e: 0. for e in EVENTS}
        for k, v in deltas.items():
            out[k.split(":")[0]] = out[k.split(":")[0]] + v
        return out


def points(deltas, unit_values):
    """{effect id: points per 100} from event changes and per-unit values."""
    return {k: v * unit_values[k.split(":")[0]] for k, v in deltas.items()}


def is_offense(effect):
    return effect.split(":")[1].startswith("O")


# ---- the release tool ----------------------------------------------------------------------
class Combinations:
    """Type flags for player-seasons and the layer for one lineup or one matchup.

    Types follow the input rule: era-relative compares a player-season with its own
    season's players, as-was with the latest season's.

    The forecast holds each type count at its measured maximum ("layer"); the
    band's alternative K continues pair by pair ("continued").
    """

    def __init__(self, release, layer=None):
        self.release = release
        self.layer = layer or Layer()
        t = release.seasons.table
        height = release.store.players["height"][t["pid"]]
        prof = profile(t["base"], t["rb_prob"], t["defense"], height)
        season = t["season"]
        latest = cutoffs(prof, season == release.seasons.latest)
        self.flags = {"as_was": flags(prof, latest), "relative": np.zeros((len(season), len(TYPES)), bool)}
        block90 = {}
        for s in np.unique(season):
            at = season == s
            self.flags["relative"][at] = flags({k: v[at] for k, v in prof.items()}, cutoffs(prof, at))
            block90[int(s)] = float(np.quantile(prof["block"][at], H1_BLOCK))
        latest90 = block90[release.seasons.latest]
        self.h1 = dict(small=height <= H1_SMALL,
                       anchor={"relative": (height >= H1_ANCHOR) & (prof["block"] >= np.array([block90[int(s)] for s in season])),
                               "as_was": (height >= H1_ANCHOR) & (prof["block"] >= latest90)})

    def side_flags(self, rows):
        f = self.flags[self.release.rule][np.asarray(rows, np.int64)]
        return f[..., :len(OFFENSE)], f[..., len(OFFENSE):]

    def terms(self, offense_rows, defense_rows, cap=True):
        """Layer terms for [B,5] offense rows against [B,5] defense rows."""
        o, _ = self.side_flags(offense_rows)
        _, d = self.side_flags(defense_rows)
        return self.layer.terms(o, d, cap)

    @cached_property
    def panel(self):
        """{(side, cap): {effect: mean event change}}: the panel offenses' own offense pairs, the panel defenses' defense pairs."""
        out = {}
        for side, (rows, w) in self.release.panel_rows.items():
            for cap in (True, False):
                terms = self.terms(rows, rows, cap)
                out[(side, cap)] = {k: float(w @ (b * (P - x))) for k, (b, P, x) in terms.items()
                                    if is_offense(k) == (side == "offense")}
        return out

    @staticmethod
    def _effects(terms, unit_values, keep):
        """Effects acting on one offense, largest points first. keep(effect id) selects them."""
        titles = {effect_id(e, s, a, b): (title, s) for e, s, a, b, title in EFFECTS}
        out = []
        for k, (b, P, x) in terms.items():
            if not keep(k):
                continue
            P, x = float(np.asarray(P).ravel()[0]), float(np.asarray(x).ravel()[0])
            change = b * (P - x)
            title, side = titles[k]
            event = k.split(":")[0]
            out.append(dict(id=k, title=title, side=side, event=event, pairs=P, expected=x, change=change,
                            points=change * float(unit_values[event])))
        return sorted(out, key=lambda e: -abs(e["points"]))

    def lineup(self, rows, rates, league_rates):
        """The layer for one five against the league-average panel.

        rates: the five's offense against the panel defenses (explain ledger);
        league_rates: the league-average offense. Effects of the five's offense
        pairs are valued at its rates, of its defense pairs at the league's; the
        panel's own pairs add their average.
        """
        rows = np.asarray(rows, np.int64)[None]
        v_own, v_league = team_values(rates), team_values(league_rates)
        out = {}
        for cap, key in ((True, "layer"), (False, "continued")):
            terms = self.terms(rows, rows, cap)
            off = self._effects(terms, v_own, is_offense)
            de = self._effects(terms, v_league, lambda k: not is_offense(k))
            off_panel = sum(points(self.panel[("defense", cap)], v_own).values())
            def_panel = sum(points(self.panel[("offense", cap)], v_league).values())
            offense = sum(e["points"] for e in off) + off_panel
            defense = sum(e["points"] for e in de) + def_panel
            out[key] = dict(offense=float(offense), defense=float(defense), margin=float(offense - defense))
            if cap:
                out["effects"] = dict(offense=off, defense=de)
                out["opponent"] = dict(offense=float(off_panel), defense=float(def_panel))
        out["beyond"] = self.beyond(rows[0], rows[0])
        out["notes"] = self.notes(rows[0], "the lineup")
        return out

    def matchup(self, a_rows, b_rows, a_rates, b_rates):
        """The layer for A against B: each offense's own pairs plus the other defense's, at that offense's rates."""
        a_rows, b_rows = np.asarray(a_rows, np.int64)[None], np.asarray(b_rows, np.int64)[None]
        va, vb = team_values(a_rates), team_values(b_rates)
        out = {}
        for cap, key in ((True, "layer"), (False, "continued")):
            ea = self._effects(self.terms(a_rows, b_rows, cap), va, lambda k: True)
            eb = self._effects(self.terms(b_rows, a_rows, cap), vb, lambda k: True)
            a, b = sum(e["points"] for e in ea), sum(e["points"] for e in eb)
            out[key] = dict(a_offense=float(a), b_offense=float(b), margin=float(a - b))
            if cap:
                out["effects"] = dict(a_offense=ea, b_offense=eb)
        out["beyond"] = self.beyond(a_rows[0], b_rows[0]) + self.beyond(b_rows[0], a_rows[0])
        out["notes"] = self.notes(a_rows[0], "team A") + self.notes(b_rows[0], "team B")
        return out

    def beyond(self, offense_rows, defense_rows):
        """Type counts past the measured maximum, for the effects that read them."""
        o, _ = self.side_flags(np.asarray(offense_rows)[None])
        _, d = self.side_flags(np.asarray(defense_rows)[None])
        used = {t for e in self.layer.spec["events"].values() for p in e["pairs"] for t in p[1:]}
        out = []
        for names, f, side in ((OFFENSE, o[0], "offense"), (DEFENSE, d[0], "defense")):
            for j, t in enumerate(names):
                n = int(f[:, j].sum())
                if t in used and n > self.layer.measured_max[t]:
                    out.append(dict(type=t, side=side, count=n, measured=self.layer.measured_max[t]))
        return out

    def notes(self, rows, label):
        """Labeled notes that are not in the number (H1, pre-registered for 2026-27)."""
        rows = np.asarray(rows, np.int64)
        small = int(self.h1["small"][rows].sum())
        if not small:
            return []
        anchor = bool(self.h1["anchor"][self.release.rule][rows].any())
        return [dict(id="h1", label=label, small=small, anchor=anchor)]
