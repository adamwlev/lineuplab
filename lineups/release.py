"""The release model: what the lineup tool shows (docs/CLOSEOUT.md, step 1).

Adam's decision of 2026-10-12: the forecast is the calibrated neural model
alone, reference architecture (arm R, broadcast defense). The capacity-law
model (arm C) is the band's labeled alternative. Both are the frozen 2026-27
prospective fits at origin 2027q1 (scripts/prospective_fit.py):

- three seeds each, every seed the mixture of its last five checkpoints;
- inputs from the 2027q1 store (states through 2026-06-13, library to opening
  night). Since 2026-10-14 the origin states come from the fixed name matching
  (STORE); the frozen record was made with FROZEN_STORE;
- each seed calibrated by its prior-only affine from the freeze record,
  around the record's league level.

Fits are read only and checked against the freeze record's hashes.

An offense-side assumption arm (creation conservation at full strength) was
screened and dropped: real lineups contradict it
(reports/creation_law_screen_2026_10_12.md).

**Inputs.** By player id at the release origin (the frozen store), or by
player-season rows (lineups.players). The two agree exactly for season 2026.
Player-seasons default to the era-relative rule (Adam, 2026-10-12). As-was is
the switchable alternative.

Points per 100 possessions. A seed's native forecast is its checkpoint-mixture
ledger. Its calibrated forecast is league + intercept + slope * (native -
league). The release forecast is the mean of the calibrated seeds.

**League-average opponent.** The panel of real fives from the last season
before the origin with at least PANEL_POSSESSIONS on that side, weighted by
possessions:
- a lineup's offensive rating is its average against the panel's defenses;
- its defensive rating is the panel offenses' average against it.

The neutral defense of lineups.coherence (five identical average defenders) is
kept only to reproduce the freeze's fixture table. It has no offensive
counterpart, and under capacity it is not neutral.

**Learned combinations** (Adam, 2026-10-14; lineups.learned). ``season_learned``
gives the calibrated points the centered module adds at half strength: for
each seed, slope * SCALE * (arm R with its module - arm R - level), then the
seed mean. Points methods stay the network alone; lineups.band adds the
module, like the combination layer, to every assumption.
"""
import hashlib
import json
from functools import cached_property

import numpy as np
import torch

from lineups import learned, legacy, paths
from lineups.coherence import ledgers
from lineups.features import Store
from lineups.model import EventModel, average_ledgers
from lineups.players import PlayerSeasons

FROZEN_FITS = paths.CACHE / "prospective_2027q1"                 # the frozen 2026-27 prospective record: never modified
FROZEN_RECORD = FROZEN_FITS / "freeze" / "record.json"
FROZEN_STORE = paths.CACHE / "lineups_store_2027q1_library"   # the inputs of the frozen record
from lineups.sources import DATA, SOURCE, SOURCES  # noqa: E402  (what the tool shows)
FITS, RECORD, STORE, MATCHUPS = SOURCE["fits"], SOURCE["record"], SOURCE["store"], SOURCE["matchups"]
ORIGIN = "2027q1"
ARMS = dict(R="broadcast", C="capacity")
SEEDS = (17, 23, 41)
FORECAST = "R"
RULE = "relative"                     # default player-season input rule (lineups.players.RULES)
PANEL_SEASON = 2026
PANEL_POSSESSIONS = 100


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def checkpoints(arm, seed, saved):
    """A frozen fit's checkpoint models (built as scripts/prospective_fit.model does)."""
    offense = EventModel.offense_only(seed)
    offense.load_state_dict(saved["offense_final"])
    models = []
    for state in saved["checkpoints"]:
        m = EventModel.from_offense(offense, seed, ARMS[arm])
        m.load_state_dict(state)
        models.append(m.eval())
    return models


class Release:
    def __init__(self, arms=tuple(ARMS), verify=True, rule=RULE, store=None, fits=None, record=None,
                 matchups=None, table=None, modules=None):
        """store, fits, record, matchups: default STORE, FITS, RECORD, MATCHUPS (the frozen record is
        FROZEN_STORE, FROZEN_FITS, FROZEN_RECORD); table, modules: the player-season table and the learned
        modules (default SOURCE's)."""
        store, fits, record = store or STORE, fits or FITS, record or RECORD
        self.rule = rule                       # player-season input rule (lineups.players)
        self.fits, self.matchups_dir = fits, matchups or MATCHUPS
        self.table, self.modules_dir = table or SOURCE["table"], modules or SOURCE["modules"]
        self.record = json.loads(record.read_text())
        if self.record["origin"] != ORIGIN:
            raise ValueError("freeze record is for another origin")
        self.store = Store(store)
        self.league = float(self.record["additive"]["league"])
        self.models = {}
        for arm in arms:
            self.models[arm] = {}
            for seed in SEEDS:
                path = fits / f"{arm}_s{seed}.pt"
                if verify and _sha256(path) != self.record["fits"][f"{arm}_s{seed}"]:
                    raise ValueError(f"{path.name} does not match the freeze record")
                saved = torch.load(path, map_location="cpu", weights_only=False)
                self.models[arm][seed] = checkpoints(arm, seed, saved)
        index = int(self.store.schedule().query("tag == @ORIGIN").iloc[0].origin_index)
        self.league_capture = float(self.store.offense_origins["league"][index])
        self.normalizer = self.store.normalizer(ORIGIN, "final")
        self.env = self.store.env(ORIGIN, "final")

    # ---- forecasts --------------------------------------------------------------
    def native(self, arm, offense, defense):
        """Per-seed native points/100 [S, B]; defense None is the neutral defense."""
        return np.stack([ledgers(self.models[arm][s], self.store, offense, defense, ORIGIN).points100.numpy()
                         for s in SEEDS]).astype(float)

    def calibrate(self, arm, native):
        """Calibrate per-seed native forecasts [S, ...] and average the seeds."""
        out = []
        for seed, p in zip(SEEDS, native):
            c = self.record["calibration"][f"{arm}_s{seed}"]
            out.append(self.league + c["intercept"] + c["slope"] * (p - self.league))
        return np.mean(out, 0)

    def points(self, offense, defense, arm=FORECAST):
        """Calibrated points/100 for [B,5] offense fives against [B,5] defense fives (or None: neutral)."""
        offense = np.asarray(offense, np.int64)
        return self.calibrate(arm, self.native(arm, offense, None if defense is None else np.asarray(defense, np.int64)))

    def ledger(self, offense, defense, arm=FORECAST):
        """The expected ledger: the equal mixture of every checkpoint of every seed."""
        preds = [ledgers(self.models[arm][s], self.store, np.asarray(offense, np.int64),
                         None if defense is None else np.asarray(defense, np.int64), ORIGIN) for s in SEEDS]
        return average_ledgers(preds)

    def matchup(self, team_a, team_b, arm=FORECAST):
        """A's and B's calibrated offense against each other, and the margin (A minus B)."""
        p = self.points([team_a, team_b], [team_b, team_a], arm)
        return dict(a_offense=float(p[0]), b_offense=float(p[1]), margin=float(p[0] - p[1]))

    # ---- league-average opponent ------------------------------------------------
    @cached_property
    def matchups(self):
        """The real game-level lineup rows (lineups.legacy.matchups) of this release's data."""
        return legacy.matchups(self.matchups_dir)

    @cached_property
    def panel(self):
        """{side: (fives [K,5], weights [K])}: real fives of PANEL_SEASON with enough possessions."""
        g = self.matchups
        season = self.store.schedule().query("season == @PANEL_SEASON")
        rows = np.flatnonzero((np.asarray(g["date"]) >= legacy.day(season.start.min()))
                              & (np.asarray(g["date"]) < legacy.day(season.stop.max())))
        possessions = np.asarray(g["possessions"][rows], float)
        out = {}
        for side, column in (("offense", "pids"), ("defense", "defense")):
            fives = np.sort(np.asarray(g[column][rows]), 1)
            units, inverse = np.unique(fives, axis=0, return_inverse=True)
            weight = np.bincount(inverse.ravel(), possessions, len(units))
            keep = weight >= PANEL_POSSESSIONS
            out[side] = (units[keep], weight[keep] / weight[keep].sum())
        return out

    def ratings(self, five, arm=FORECAST):
        """Offensive and defensive rating against the league-average panel, and the margin."""
        five = np.asarray(five, np.int64)
        defenses, wd = self.panel["defense"]
        offenses, wo = self.panel["offense"]
        offense = float(wd @ self.points(np.repeat(five[None], len(defenses), 0), defenses, arm))
        defense = float(wo @ self.points(offenses, np.repeat(five[None], len(offenses), 0), arm))
        return dict(offense=offense, defense=defense, margin=offense - defense)

    # ---- player-season rows (lineups.players) -----------------------------------
    @cached_property
    def seasons(self):
        return PlayerSeasons() if self.table is None else PlayerSeasons(self.table)

    def inputs(self, offense_rows, defense_rows):
        return self.seasons.batch(np.asarray(offense_rows, np.int64), np.asarray(defense_rows, np.int64),
                                  self.normalizer, self.league_capture, self.store, self.rule)

    def season_ledgers(self, arm, inputs):
        """Per-seed checkpoint-mixture ledgers for prepared inputs."""
        with torch.no_grad():
            return [average_ledgers([m(inputs, self.env) for m in self.models[arm][s]]) for s in SEEDS]

    def season_points(self, offense_rows, defense_rows, arm=FORECAST):
        """Calibrated points/100 for [B,5] offense rows against [B,5] defense rows."""
        preds = self.season_ledgers(arm, self.inputs(offense_rows, defense_rows))
        return self.calibrate(arm, np.stack([p.points100.numpy() for p in preds]).astype(float))

    @cached_property
    def panel_rows(self):
        """The average-opponent panel as player-season rows (every panel player played in PANEL_SEASON)."""
        return {side: (self.seasons.rows(fives, np.full(fives.shape, PANEL_SEASON)), w)
                for side, (fives, w) in self.panel.items()}

    def season_ratings(self, rows, arm=FORECAST):
        """Offensive and defensive rating of one five (player-season rows) against the panel."""
        rows = np.asarray(rows, np.int64)
        defenses, wd = self.panel_rows["defense"]
        offenses, wo = self.panel_rows["offense"]
        offense = float(wd @ self.season_points(np.repeat(rows[None], len(defenses), 0), defenses, arm))
        defense = float(wo @ self.season_points(offenses, np.repeat(rows[None], len(offenses), 0), arm))
        return dict(offense=offense, defense=defense, margin=offense - defense)

    # ---- learned combinations (lineups.learned) ---------------------------------
    @cached_property
    def modules(self):
        """{seed: (module, level)}: each seed's learned module on arm R."""
        return {s: learned.load(s, self.modules_dir) for s in SEEDS}

    def learned_native(self, inputs):
        """Per-seed native changes [S, B] per field: SCALE * (with the module - without - level)."""
        out = {k: [] for k in learned.FIELDS}
        for seed in SEEDS:
            module, level = self.modules[seed]
            off, on = (learned.rates(p) for p in learned.ledgers_with(self.models["R"][seed], module, inputs, self.env))
            for k in learned.FIELDS:
                out[k].append(learned.SCALE * (on[k] - off[k] - level[k]))
        return {k: np.stack(v) for k, v in out.items()}

    def season_learned(self, offense_rows, defense_rows):
        """Per row: calibrated points/100 and native event-rate changes from the learned module (seed means)."""
        native = self.learned_native(self.inputs(offense_rows, defense_rows))
        slopes = np.array([self.record["calibration"][f"R_s{s}"]["slope"] for s in SEEDS])
        out = {k: v.mean(0) for k, v in native.items() if k != "points"}
        out["points"] = (slopes[:, None] * native["points"]).mean(0)
        return out

    def season_learned_ratings(self, rows):
        """The learned module's change to one five's offense and defense against the panel, and the margin;
        event changes for its offense (against the panel defenses) and for the panel offenses against it."""
        rows = np.asarray(rows, np.int64)
        defenses, wd = self.panel_rows["defense"]
        offenses, wo = self.panel_rows["offense"]
        own = self.season_learned(np.repeat(rows[None], len(defenses), 0), defenses)
        allowed = self.season_learned(offenses, np.repeat(rows[None], len(offenses), 0))
        offense, defense = float(wd @ own["points"]), float(wo @ allowed["points"])
        events = {side: {k: float(w @ v[k]) for k in learned.FIELDS if k != "points"}
                  for side, v, w in (("offense", own, wd), ("defense", allowed, wo))}
        return dict(offense=offense, defense=defense, margin=offense - defense, events=events)

    def season_learned_matchup(self, a_rows, b_rows):
        """The learned module's change to A's and B's offense against each other, and the margin."""
        p = self.season_learned(np.asarray([a_rows, b_rows], np.int64), np.asarray([b_rows, a_rows], np.int64))
        events = {side: {k: float(p[k][i]) for k in learned.FIELDS if k != "points"}
                  for i, side in enumerate(("a_offense", "b_offense"))}
        return dict(a_offense=float(p["points"][0]), b_offense=float(p["points"][1]),
                    margin=float(p["points"][0] - p["points"][1]), events=events)
