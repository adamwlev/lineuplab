"""Model inputs: dated player states, capability banks and prefix normalizers.

Every model input is a per-player lookup. A row's lineup only decides which
players are stacked. There are two lookup modes:

* **history**: the player's state as of a specific game (strictly earlier
  data), used for training rows;
* **origin**: the state frozen at an origin date, used for forecasting a
  later quarter and for hypothetical lineups. Players without history get
  that origin's population fallback state.

The store (``paths.STORE``) holds:

    offense_games.npz    game_id, pid, base[18], role[8], rb_prob, rb_neff, league
    offense_origins.npz  origin_index, pid, base, role, rb_prob, rb_neff;
                         fallback_base[O,18], fallback_role[O,8], fallback_rb_prob[O], league[O]
    defense_games.npz    game_id, pid, x[19]
    defense_origins.npz  origin_index, pid, x[19]; fallback[O,19]
    library_{bank}.npz   dates[D], offsets[D+1], ids, values[...,97|49], last
    normalizers/<tag>_<phase>.npz   prefix-fitted standardization for one origin/phase
    references.json      shared loss normalizers per origin/phase/seed (training)
    environment.json     opportunity budget, renewal and miss constants per origin/phase
    players.npz          optional static listings: pid, height (in), position (1-5)
    schedule.csv         optional origin schedule when it extends the v16 one

With players.npz present, batches also carry standardized listed height and
position for both sides and ``matched``: for each attacker, the defender slot
assigned by sorting both fives on (position, height, pid) and pairing in order.
In one dimension sorted pairing is the minimum-cost assignment; the pid
tie-break keeps the pairing independent of slot order. ``defense_tiebreak``
(a tiny pid-based value) lets models rank defenders without slot-order ties.

``base`` is the 18-coordinate offensive state (see lineups.model). ``role`` is
four recent-minus-long contrasts plus four historical-teammate averages.
``x`` is the 19 defensive descriptors. Capability bank rows are the adjusted
GLM coefficients, log opportunities, log coefficient SD and log staleness.
Staleness is recomputed at query time.
"""
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import torch

from lineups import paths

NEVER_SEEN_STALENESS = 1825
BANK_WIDTH = {"offense": 97, "defense": 49}
HEIGHT_SCALE = (79., 3.5)      # fixed unit conversions, not fitted
POSITION_SCALE = (3., 1.4)
TIEBREAK = 1e-7               # pid-based key that orders otherwise identical defenders


def _keyed(table_keys, wanted):
    """Positions of wanted keys in a sorted key array; -1 where absent."""
    at = np.searchsorted(table_keys, wanted)
    safe = np.minimum(at, len(table_keys) - 1)
    return np.where((at < len(table_keys)) & (table_keys[safe] == wanted), at, -1)


class Store:
    def __init__(self, directory=None):
        self.directory = Path(directory or paths.STORE)
        load = lambda name: dict(np.load(self.directory / name, allow_pickle=False))
        self.offense_games = load("offense_games.npz")
        self.offense_origins = load("offense_origins.npz")
        self.defense_games = load("defense_games.npz")
        self.defense_origins = load("defense_origins.npz")
        self.library = {bank: load(f"library_{bank}.npz") for bank in BANK_WIDTH}
        self.environment = json.loads((self.directory / "environment.json").read_text())
        self.references = json.loads((self.directory / "references.json").read_text())
        factor = int(max(self.offense_games["pid"].max(), self.defense_games["pid"].max())) + 1
        self._factor = factor
        self.players = None
        if (self.directory / "players.npz").exists():
            listing = load("players.npz")
            size = max(factor, int(listing["pid"].max()) + 1)
            height = np.full(size, np.mean(listing["height"]), np.float64)
            position = np.full(size, np.mean(listing["position"]), np.float64)
            height[listing["pid"]], position[listing["pid"]] = listing["height"], listing["position"]
            self.players = dict(height=height, position=position)
        self._off_key = self.offense_games["game_id"] * factor + self.offense_games["pid"]
        self._def_key = self.defense_games["game_id"] * factor + self.defense_games["pid"]
        for name, key in (("offense_games", self._off_key), ("defense_games", self._def_key)):
            if np.any(np.diff(key) <= 0):
                raise ValueError(f"{name} must be sorted by (game_id, pid) without duplicates")

    def schedule(self):
        """The store's own origin schedule (schedule.csv) if it has one, else the v16 schedule."""
        from lineups import legacy
        own = self.directory / "schedule.csv"
        return legacy.schedule(own) if own.exists() else legacy.schedule()

    @lru_cache(maxsize=None)
    def normalizer(self, tag, phase):
        with np.load(self.directory / "normalizers" / f"{tag}_{phase}.npz") as z:
            return {k: z[k] for k in z.files}

    # ---- per-player lookups -------------------------------------------------
    def _game_rows(self, keys, game_ids, pids):
        at = _keyed(keys, np.asarray(game_ids, np.int64)[:, None] * self._factor + np.asarray(pids, np.int64))
        if np.any(at < 0):
            raise KeyError(f"{int((at < 0).sum())} player-game states missing")
        return at

    def _origin_rows(self, table, origin_index, pids):
        select = np.flatnonzero(table["origin_index"] == origin_index)
        at = _keyed(table["pid"][select], np.asarray(pids, np.int64))
        return np.where(at >= 0, select[np.maximum(at, 0)], -1)

    def offense(self, pids, *, game_ids=None, origin_index=None):
        if (game_ids is None) == (origin_index is None):
            raise ValueError("give game_ids (history) or origin_index (origin), not both")
        if game_ids is not None:
            t, at = self.offense_games, self._game_rows(self._off_key, game_ids, pids)
            league = t["league"][at[:, 0]]
            return dict(base=t["base"][at], role=t["role"][at], rb_prob=t["rb_prob"][at],
                        rb_neff=t["rb_neff"][at], league=league)
        t = self.offense_origins
        at = self._origin_rows(t, origin_index, pids)
        known = at >= 0
        take = np.maximum(at, 0)
        pick = lambda k, fallback: np.where(known[..., None] if t[k].ndim > 1 else known, t[k][take], fallback)
        return dict(base=pick("base", t["fallback_base"][origin_index]),
                    role=pick("role", t["fallback_role"][origin_index]),
                    rb_prob=pick("rb_prob", t["fallback_rb_prob"][origin_index]).astype(np.float32),
                    rb_neff=np.where(known, t["rb_neff"][take], 0.).astype(np.float32),
                    league=np.full(len(pids), t["league"][origin_index], np.float32))

    def defense(self, pids, *, game_ids=None, origin_index=None):
        if game_ids is not None:
            return self.defense_games["x"][self._game_rows(self._def_key, game_ids, pids)]
        t = self.defense_origins
        at = self._origin_rows(t, origin_index, pids)
        return np.where((at >= 0)[..., None], t["x"][np.maximum(at, 0)], t["fallback"][origin_index])

    def capabilities(self, pids, dates, bank):
        """Adjusted capability rows from the latest snapshot on or before each date."""
        lib = self.library[bank]
        pids = np.asarray(pids, np.int64)
        dates = np.asarray(dates, np.int64)
        snapshot = np.searchsorted(lib["dates"], dates, side="right") - 1
        if np.any(snapshot < 0):
            raise ValueError("date precedes capability library coverage")
        out = np.empty((*pids.shape, BANK_WIDTH[bank]), np.float32)
        last = np.full(pids.shape, -1, np.int64)
        for s in np.unique(snapshot):
            rows = np.flatnonzero(snapshot == s)
            lo, hi = lib["offsets"][s], lib["offsets"][s + 1]
            ids = lib["ids"][lo:hi]
            at = _keyed(ids, pids[rows])
            at = np.where(at >= 0, at, 0)   # row 0 is the never-seen sentinel
            out[rows] = lib["values"][lo:hi][at]
            last[rows] = lib["last"][lo:hi][at]
        stale = np.where(last >= 0, dates[:, None] - last, NEVER_SEEN_STALENESS)
        out[..., -1] = np.log1p(stale)
        return out

    # ---- batch assembly -----------------------------------------------------
    def batch(self, offense, defense, dates, normalizer, *, game_ids=None, origin_index=None, query_day=None):
        """Standardized model inputs for B lineups (offense/defense: [B,5] player ids).

        In origin mode, capability banks are read at the normalizer's cutoff unless
        ``query_day`` names another date. That is for states from one origin
        standardized by another origin's normalizer (cross-era transport).
        """
        mode = dict(game_ids=game_ids) if game_ids is not None else dict(origin_index=origin_index)
        if game_ids is not None:
            query = np.asarray(dates, np.int64)
        else:
            query = np.full(len(offense), normalizer["cutoff_day"] if query_day is None else query_day, np.int64)
        raw = self.offense(offense, **mode) | dict(defense=self.defense(defense, **mode),
                                                   adjusted_offense=self.capabilities(offense, query, "offense"),
                                                   adjusted_defense=self.capabilities(defense, query, "defense"))
        out = standardize(raw, normalizer)
        if self.players is not None:
            out.update(self.listings(offense, defense))
        return out

    def listings(self, offense, defense):
        """Standardized height/position for both sides and the sorted-position assignment."""
        offense, defense = np.asarray(offense, np.int64), np.asarray(defense, np.int64)
        known = lambda table: (lambda pids: np.where(pids < len(table), table[np.minimum(pids, len(table) - 1)],
                                                     table.mean()))
        h, p = known(self.players["height"]), known(self.players["position"])
        key = lambda pids: p(pids) * 1e4 + h(pids) * 10 + pids * 1e-5
        rank_o = np.argsort(key(offense), axis=1, kind="stable")
        rank_d = np.argsort(key(defense), axis=1, kind="stable")
        matched = np.empty_like(rank_o)
        np.put_along_axis(matched, rank_o, rank_d, axis=1)
        scale = lambda x, c: torch.as_tensor(((x - c[0]) / c[1]).astype(np.float32))
        return dict(offense_height=scale(h(offense), HEIGHT_SCALE), defense_height=scale(h(defense), HEIGHT_SCALE),
                    offense_position=scale(p(offense), POSITION_SCALE),
                    defense_position=scale(p(defense), POSITION_SCALE), matched=torch.as_tensor(matched),
                    defense_tiebreak=torch.as_tensor((defense * TIEBREAK).astype(np.float32)))

    def env(self, tag, phase):
        e = self.environment[f"{tag}/{phase}"]
        return dict(budget=e["budget"], eta=e["eta"], non_rebound=e["non_rebound"])


def standardize(raw, normalizer):
    """Model inputs from raw per-player rows.

    raw: base [B,5,18], role [B,5,8], rb_prob and rb_neff [B,5], league [B],
    defense [B,5,19], adjusted_offense [B,5,97] and adjusted_defense [B,5,49].
    """
    n = normalizer
    msg = (raw["base"] - n["base_mean"]) / np.maximum(n["base_sd"], 1e-6)
    role = (raw["role"] - n["role_mean"]) / n["role_scale"]
    p = np.clip(raw["rb_prob"], 1e-6, 1 - 1e-6)
    extra = np.stack([np.log(p) - np.log1p(-p), np.log1p(raw["rb_neff"])], -1)
    extra = (extra - n["rebound_mean"]) / n["rebound_scale"]
    arrays = dict(base=raw["base"], msg=msg, role=role,
                  rb_input=np.concatenate([msg, role, extra], -1), rb_prior=raw["rb_prob"],
                  league_capture=raw["league"],
                  defense=(raw["defense"] - n["defense_mean"]) / n["defense_scale"],
                  adjusted_offense=(raw["adjusted_offense"] - n["offense_mean"]) / n["offense_scale"],
                  adjusted_defense=(raw["adjusted_defense"] - n["defense_bank_mean"]) / n["defense_bank_scale"])
    return {k: torch.as_tensor(np.asarray(v, np.float32)) for k, v in arrays.items()}
