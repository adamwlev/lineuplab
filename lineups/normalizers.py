"""Prefix-fitted input normalizers and environment constants (refactor rung 5, step 5).

For a cutoff day (an origin's start for the final phase, the previous quarter's
start for the inner phase), every normalizer is a possession-weighted moment
over the five-year training prefix [cutoff - 5 years, cutoff), with row weight
possessions x 2^(-age/730 days):

    base_mean, base_sd        18 offensive state coordinates     game x offense-five rows
    role_mean, role_scale     role inputs x[..., 55:63]          game x offense-five rows
    rebound_mean, _scale      [logit capture prior, log1p neff]  game x offense-five rows
    defense_mean, _scale      19 defensive descriptors           game x offense x defense rows
    offense_mean, _scale      offensive capability bank (97)     game x offense x defense rows
    defense_bank_mean, _scale defensive capability bank (49)     game x offense x defense rows

The environment uses every earlier row with weight 2^(-age/365 days):
budget (FGA + .44 FTA + TO per possession), the offensive-rebound reference,
eta (eligible live misses per cached field-goal miss) and non_rebound =
budget - offensive-rebound reference.

Ported from tag pre-refactor-2026-10-09 (v3 standardization_and_reference,
v8 state_moments, v14 extend_shared and environment, v16 make_shared and
fit_normalizers). tests/test_normalizers.py reproduces the saved store.
Team baselines and additive offsets are not ported: they fed only the legacy
readout offset, which the forward pass ignores.
"""
import numpy as np

LOOKBACK_DAYS = 5 * 365
CHUNK = 50000


def _moments(values, weights, floor):
    """values [N,5,F], weights [N]; mean and sd over rows and the five players."""
    total = weights.sum() * 5
    mean = (values * weights[:, None, None]).sum((0, 1)) / total
    var = (values ** 2 * weights[:, None, None]).sum((0, 1)) / total - mean ** 2
    return mean, np.sqrt(np.maximum(var, floor))


def prefix(dates, cutoff, first_day=None):
    """Rows in [cutoff - 5 years, cutoff), and on or after first_day if given (era stores start their library later)."""
    start = cutoff - LOOKBACK_DAYS if first_day is None else max(cutoff - LOOKBACK_DAYS, first_day)
    return np.flatnonzero((dates < cutoff) & (dates >= start))


def lineup_normalizers(grouped, offense, rebound, cutoff, first_day=None):
    """Base, role and rebound moments over game x offense-five rows (cached v3 grouping).

    offense / rebound: game-level arrays from lineups.states (game_id, pid, base, x; prob, neff).
    """
    rows = prefix(grouped["date"], cutoff, first_day)
    factor = int(offense["pid"].max()) + 1
    key = offense["game_id"].astype(np.int64) * factor + offense["pid"]
    order = np.argsort(key)
    at = order[np.searchsorted(key[order], grouped["game_id"][rows, None].astype(np.int64) * factor
                               + grouped["pids"][rows])]
    w = np.exp2(-(cutoff - grouped["date"][rows]) / 730.) * grouped["possessions"][rows]
    base = offense["base"][at].astype(np.float64)
    x = offense["x"][at].astype(np.float64)
    total = w.sum() * 5
    base_mean = (base * w[:, None, None]).sum((0, 1)) / total
    base_sd = np.sqrt(np.maximum(((base - base_mean) ** 2 * w[:, None, None]).sum((0, 1)) / total, 1e-12))
    x_mean = (x * w[:, None, None]).sum((0, 1)) / total
    x_sd = np.sqrt(np.maximum(((x - x_mean) ** 2 * w[:, None, None]).sum((0, 1)) / total, 1e-6))
    rkey = rebound["game_id"].astype(np.int64) * factor + rebound["pid"]
    rorder = np.argsort(rkey)
    rat = rorder[np.searchsorted(rkey[rorder], grouped["game_id"][rows, None].astype(np.int64) * factor
                                 + grouped["pids"][rows])]
    p = np.clip(rebound["prob"][rat], 1e-6, 1 - 1e-6)
    extra = np.stack([np.log(p) - np.log1p(-p), np.log1p(rebound["neff"][rat])], -1).astype(np.float64)
    rebound_mean, rebound_scale = _moments(extra, w, 1e-12)
    return dict(cutoff_day=np.int64(cutoff), base_mean=base_mean.astype(np.float32), base_sd=base_sd.astype(np.float32),
                role_mean=x_mean[55:63].astype(np.float32), role_scale=x_sd[55:63].astype(np.float32),
                rebound_mean=rebound_mean, rebound_scale=rebound_scale)


def matchup_normalizers(matchups, store, cutoff, first_day=None):
    """Defensive descriptor and capability-bank moments over game x offense x defense rows."""
    dates = np.asarray(matchups["date"])
    rows = prefix(dates, cutoff, first_day)
    sums = {k: [0., 0.] for k in ("defense", "offense", "defense_bank")}
    total = 0.
    for start in range(0, len(rows), CHUNK):
        ix = rows[start:start + CHUNK]
        game, d = np.asarray(matchups["game_id"][ix]), dates[ix]
        offense, defense = np.asarray(matchups["pids"][ix]), np.asarray(matchups["defense"][ix])
        w = np.asarray(matchups["possessions"][ix]) * np.exp2(-(cutoff - d) / 730.)
        values = dict(defense=store.defense(defense, game_ids=game),
                      offense=store.capabilities(offense, d, "offense"),
                      defense_bank=store.capabilities(defense, d, "defense"))
        for k, v in values.items():
            v = v.astype(np.float64)
            sums[k][0] = sums[k][0] + (v * w[:, None, None]).sum((0, 1))
            sums[k][1] = sums[k][1] + (v * v * w[:, None, None]).sum((0, 1))
        total += 5 * w.sum()
    out = {}
    for k, (first, second) in sums.items():
        mean = first / total
        out[f"{k}_mean"] = mean.astype(np.float32)
        out[f"{k}_scale"] = np.sqrt(np.maximum(second / total - mean ** 2, 1e-8)).astype(np.float32)
    return out


def environment(grouped, rebound_counts, cutoff):
    """Opportunity budget and renewal constants from every earlier row (half-life 365 days)."""
    rows = np.flatnonzero(grouped["date"] < cutoff)
    w = np.exp2(-(cutoff - grouped["date"][rows]) / 365.)
    possessions = grouped["possessions"][rows]
    events = grouped["fga"][rows].sum(1) + .44 * grouped["fta"][rows].sum(1) + grouped["turnover"][rows].sum(1)
    budget = float(np.sum(w * possessions * events / possessions) / np.sum(w * possessions))
    den = float(w @ possessions)
    orb = float(w @ rebound_counts[rows, :5].sum(1) / den)
    observed = grouped["fga_observed"][rows] & grouped["location_observed"][rows]
    misses = (grouped["loc_attempt"][rows] - grouped["loc_make"][rows]).sum((1, 2))
    live = rebound_counts[rows].sum(1)
    live_total, miss_total = float(w[observed] @ live[observed]), float(w[observed] @ misses[observed])
    eta = live_total / miss_total if miss_total else 0.
    return dict(budget=budget, eta=eta, non_rebound=budget - orb)
