"""Player-seasons for the tool (docs/CLOSEOUT.md, step 2).

A player-season is the player as of the next season's opening night
(scripts/build_player_seasons.py): raw offensive state, role, rebound prior,
defensive descriptors and adjusted capability banks, read at that origin. The
release model standardizes them with its own normalizer and runs them in its
own environment (league capture, budget, renewal). Two input rules
(scripts/cross_era.py, reports/cross_era_2026_10_12.md):

    as_was    the raw states, standardized by the model's normalizer
    relative  each raw coordinate shifted by (model normalizer mean - the
              player's season-origin normalizer mean), so a player is placed
              relative to his own league; the raw anchors the ledger reads
              (base, rebound prior and n_eff) shift the same way

Defaults: a player who played in the latest season defaults to it. Anyone else
defaults to the season with the most possessions on the floor.
"""
import json
from functools import cached_property

import numpy as np

from lineups import paths
from lineups.sources import SOURCE
from lineups.features import standardize

TABLE = SOURCE["table"]       # lineups.sources (player_seasons_2026_10_14: fixed name matching; 2026_10_12 before)
RAW = ("base", "role", "rb_prob", "rb_neff", "defense", "adjusted_offense", "adjusted_defense")
MEANS = ("base_mean", "role_mean", "rebound_mean", "defense_mean", "offense_mean", "defense_bank_mean")
RULES = ("as_was", "relative")


class PlayerSeasons:
    def __init__(self, directory=TABLE):
        with np.load(directory / "player_seasons.npz") as z:
            self.table = {k: z[k] for k in z.files}
        self.names = {int(k): v for k, v in json.loads((directory / "names.json").read_text()).items()}
        self.key = self.table["pid"].astype(np.int64) * 10000 + self.table["season"]
        if np.any(np.diff(np.sort(self.key)) == 0):
            raise ValueError("duplicate player-season")
        self._order = np.argsort(self.key)
        self.latest = int(self.table["season"].max())
        with np.load(directory / "season_normalizers.npz") as z:
            seasons = sorted({int(k.split("_")[0]) for k in z.files})
            self.first = seasons[0]
            self.season_normalizer = {k: np.stack([z[f"{s}_{k}"] for s in seasons]) for k in MEANS}

    def rows(self, pids, seasons):
        """Table rows for player ids and seasons (any matching shapes)."""
        wanted = np.asarray(pids, np.int64) * 10000 + np.asarray(seasons, np.int64)
        at = np.searchsorted(self.key[self._order], wanted)
        at = np.minimum(at, len(self.key) - 1)
        found = self.key[self._order][at] == wanted
        if not found.all():
            raise KeyError(f"{int((~found).sum())} player-seasons not in the table")
        return self._order[at]

    @cached_property
    def defaults(self):
        """{pid: default season}."""
        t = self.table
        on_floor = t["offense_possessions"] + t["defense_possessions"]
        out = {}
        for i in np.lexsort((on_floor, t["pid"])):
            out[int(t["pid"][i])] = int(t["season"][i])          # most possessions wins (sorted last)
        for i in np.flatnonzero(t["season"] == self.latest):
            out[int(t["pid"][i])] = self.latest
        return out

    @cached_property
    def season_means(self):
        """{season: (offensive state mean [18], defensive descriptor mean [19])}, possession-weighted."""
        t, out = self.table, {}
        for season in np.unique(t["season"]):
            at = t["season"] == season
            out[int(season)] = (np.average(t["base"][at], axis=0, weights=t["offense_possessions"][at]),
                                np.average(t["defense"][at], axis=0, weights=t["defense_possessions"][at]))
        return out

    def relative(self, rows, season=None):
        """Raw offensive and defensive states of table rows, re-centered from each player's season onto one season.

        Used for composition reasons only: it compares a five with its own era's
        players. The forecast uses the states as they were.
        """
        rows = np.asarray(rows, np.int64)
        target = self.season_means[self.latest if season is None else season]
        own = [self.season_means[int(s)] for s in self.table["season"][rows].ravel()]
        shift_o = np.stack([target[0] - o for o, _ in own]).reshape(*rows.shape, -1)
        shift_d = np.stack([target[1] - d for _, d in own]).reshape(*rows.shape, -1)
        return self.table["base"][rows] + shift_o, self.table["defense"][rows] + shift_d

    def raw(self, rows, league_capture, normalizer=None, rule="as_was"):
        """Raw per-player inputs for [B,5] table rows, in the model's environment."""
        if rule not in RULES:
            raise ValueError(f"unknown input rule {rule}")
        rows = np.asarray(rows, np.int64)
        raw = {k: self.table[k][rows] for k in RAW}
        if rule == "relative":
            own = {k: v[self.table["season"][rows] - self.first] for k, v in self.season_normalizer.items()}
            shift = {k: np.asarray(normalizer[k], np.float32) - own[k] for k in MEANS}
            raw["base"] = raw["base"] + shift["base_mean"]
            raw["role"] = raw["role"] + shift["role_mean"]
            p = np.clip(raw["rb_prob"].astype(np.float64), 1e-6, 1 - 1e-6)
            logit = np.log(p) - np.log1p(-p) + shift["rebound_mean"][..., 0]
            raw["rb_prob"] = (1 / (1 + np.exp(-logit))).astype(np.float32)
            raw["rb_neff"] = np.expm1(np.log1p(raw["rb_neff"]) + shift["rebound_mean"][..., 1]).astype(np.float32)
            raw["defense"] = raw["defense"] + shift["defense_mean"]
            raw["adjusted_offense"] = raw["adjusted_offense"] + shift["offense_mean"]
            raw["adjusted_defense"] = raw["adjusted_defense"] + shift["defense_bank_mean"]
        raw["league"] = np.full(len(rows), league_capture, np.float32)
        return raw

    def batch(self, offense_rows, defense_rows, normalizer, league_capture, store, rule="as_was"):
        """Standardized model inputs for [B,5] offense and defense table rows.

        ``store`` supplies the static listings (height, position, assignment).
        """
        off = self.raw(offense_rows, league_capture, normalizer, rule)
        de = self.raw(defense_rows, league_capture, normalizer, rule)
        raw = {k: off[k] for k in ("base", "role", "rb_prob", "rb_neff", "league", "adjusted_offense")}
        raw |= dict(defense=de["defense"], adjusted_defense=de["adjusted_defense"])
        out = standardize(raw, normalizer)
        if store.players is not None:
            pid = self.table["pid"].astype(np.int64)
            out.update(store.listings(pid[np.asarray(offense_rows)], pid[np.asarray(defense_rows)]))
        return out
