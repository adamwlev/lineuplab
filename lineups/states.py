"""Dated offensive player states (refactor rung 5, step 2).

A day-by-day sweep keeps exponentially decayed player counts (half-lives 180
and 730 days) and turns them into the 18-coordinate offensive state with moment
empirical-Bayes shrinkage. Before each day's games, it exports:

* game states: every player appearing that day, as of the start of the day
  (history mode in lineups.features);
* origin states: on each schedule start date, every player seen so far, plus a
  population fallback for players never seen (origin mode).

The x vector adds log1p exposures, missing flags, the offensive-rebound rate,
four recent-minus-long contrasts, four past-teammate context averages and log1p
staleness. Role statistics track each player's possession-weighted share of
the lineup's usage units.

Ported from tag pre-refactor-2026-10-09 (joint_capability_data._eb and
joint_capability_v3_data.pooled_logit_offset, state_from_counts, build_states).
``sweep`` reproduces player_game_states_v3.npz bit for bit
(tests/test_states.py), and accepts any schedule, so origins can be added
before 2014.

Inputs:
    lineups    game x offense-five labels (game_lineups.npz in the v3 run)
    players    player-game box counts (experiments/cache/game_player_stats.pkl)
    schedule   frame with ``start`` dates; its row index is the origin index
"""
import numpy as np
import pandas as pd

from lineups import paths

EPS = 1e-6
V3 = paths.CACHE / "joint_capability_2026_09_09_v3" / "derived"
GAME_LINEUPS = V3 / "game_lineups.npz"
GAME_PLAYERS = paths.CACHE / "game_player_stats.pkl"
FIELDS = ("base", "x", "neff", "last_seen", "role_mean", "role_sd", "role_weight")


def _logit(probability):
    p = np.clip(np.asarray(probability, float), EPS, 1.0 - EPS)
    return np.log(p) - np.log1p(-p)


def _sigmoid(value):
    value = np.asarray(value, float)
    return np.where(value >= 0, 1.0 / (1.0 + np.exp(-value)), np.exp(value) / (1.0 + np.exp(value)))


def eb(num, den, den2, active):
    """Moment empirical-Bayes rates for the current prefix, and effective exposure."""
    good = active & (den > 0)
    if not good.any():
        return np.full_like(den, .5, dtype=float), np.zeros_like(den, dtype=float)
    mu = float(num[good].sum() / den[good].sum())
    raw = np.divide(num, den, out=np.full_like(den, mu), where=den > 0)
    neff = np.divide(den * den, den2, out=np.zeros_like(den), where=den2 > 0)
    var = max(mu * (1 - mu), 1e-9)
    spread = float(np.average((raw[good] - mu) ** 2, weights=den[good]))
    noise = float(np.average(var / np.maximum(neff[good], EPS), weights=den[good]))
    tau2 = max(spread - noise, 1e-12)
    keep = tau2 / (tau2 + var / np.maximum(neff, EPS))
    return mu + keep * (raw - mu), neff


def pooled_logit_offset(c, q, active, buckets):
    """Moment EB logit offset of a player's makes over league rates, pooled over shot buckets."""
    attempts, makes, attempt_q = c[:, 9:15], c[:, 15:21], q[:, 9:15]
    league = (makes[active].sum(axis=0) + 0.5) / (attempts[active].sum(axis=0) + 1.0)
    league = np.clip(league, EPS, 1.0 - EPS)
    use = np.asarray(tuple(buckets), np.int64)
    variance = league[use] * (1.0 - league[use])
    information = (attempts[:, use] * variance).sum(axis=1)
    score = (makes[:, use] - attempts[:, use] * league[use]).sum(axis=1)
    jitter = (attempt_q[:, use] * variance).sum(axis=1)
    raw = np.divide(score, information, out=np.zeros_like(score), where=information > 0)
    sampling = np.divide(jitter, information ** 2, out=np.full_like(jitter, np.inf), where=information > 0)
    mass, mass_q = attempts[:, use].sum(axis=1), attempt_q[:, use].sum(axis=1)
    neff = np.divide(mass ** 2, mass_q, out=np.zeros_like(mass), where=mass_q > 0)
    good = active & (neff > 0) & np.isfinite(sampling)
    tau2 = max(float(np.average(raw[good] ** 2 - sampling[good], weights=neff[good])), 1e-12) if good.any() else 1e-12
    keep = np.divide(tau2, tau2 + sampling, out=np.zeros_like(sampling), where=np.isfinite(sampling))
    return keep * raw, neff, tau2, league


def state_from_counts(c180, q180, c730, q730, active):
    """Anchored state, exposures, offensive-rebound rate and recent-minus-long contrasts."""
    rates180, neff_rates, rates730 = [], [], []
    for num_col, den_col in ((1, 0), (2, 0), (4, 0)):
        r, n = eb(c180[:, num_col], c180[:, den_col], q180[:, den_col], active)
        long, _ = eb(c730[:, num_col], c730[:, den_col], q730[:, den_col], active)
        rates180.append(np.maximum(r, EPS))
        rates730.append(np.maximum(long, EPS))
        neff_rates.append(n)
    mix, mix_n = [], []
    for b in range(6):
        r, n = eb(c180[:, 9 + b], c180[:, 1], q180[:, 1], active)
        mix.append(np.maximum(r, EPS))
        mix_n.append(n)
    mix = np.column_stack(mix)
    mix /= mix.sum(axis=1, keepdims=True)
    two_offset, two_neff, _, league = pooled_logit_offset(c730, q730, active, range(4))
    three_offset, three_neff, _, _ = pooled_logit_offset(c730, q730, active, range(4, 6))
    offsets = np.column_stack([np.repeat(two_offset[:, None], 4, axis=1), np.repeat(three_offset[:, None], 2, axis=1)])
    conversion = _sigmoid(_logit(league)[None, :] + offsets)
    conversion_neff = np.column_stack([np.repeat(two_neff[:, None], 4, axis=1),
                                       np.repeat(three_neff[:, None], 2, axis=1)])
    ft, ft_n = eb(c730[:, 3], c730[:, 2], q730[:, 2], active)
    ast180, ast_n = eb(c180[:, 5], c180[:, 0], q180[:, 0], active)
    ast730, _ = eb(c730[:, 5], c730[:, 0], q730[:, 0], active)
    assisted, assisted_n = eb(c180[:, 8], c180[:, 7], q180[:, 7], active)
    base = np.column_stack([np.log(np.column_stack(rates180)), np.log(mix) - np.log(mix).mean(axis=1, keepdims=True),
                            _logit(conversion), _logit(ft), np.log(np.maximum(ast180, EPS)), _logit(assisted)])
    neff = np.column_stack(neff_rates + mix_n + [conversion_neff[:, b] for b in range(6)] + [ft_n, ast_n, assisted_n])
    orb, _ = eb(c180[:, 6], c180[:, 0], q180[:, 0], active)
    fga180, fta180, to180 = rates180
    fga730, fta730, to730 = rates730
    long_mix = []
    for b in range(6):
        r, _ = eb(c730[:, 9 + b], c730[:, 1], q730[:, 1], active)
        long_mix.append(np.maximum(r, EPS))
    long_mix = np.column_stack(long_mix)
    long_mix /= long_mix.sum(axis=1, keepdims=True)
    contrast = np.column_stack([(fga180 + 0.44 * fta180 + to180) - (fga730 + 0.44 * fta730 + to730),
                                mix[:, 4:6].sum(axis=1) - long_mix[:, 4:6].sum(axis=1), to180 - to730,
                                ast180 - ast730])
    return base, neff, np.asarray(orb), contrast


def load_inputs(lineups_path=GAME_LINEUPS, players_path=GAME_PLAYERS):
    with np.load(lineups_path, allow_pickle=False) as z:
        g = {k: z[k] for k in ("game_id", "pids", "date", "possessions", "loc_attempt", "loc_make", "fga", "fta",
                               "turnover", "fga_observed", "fta_observed")}
    return g, pd.read_pickle(players_path)


def sweep(g, gp, schedule, log=None):
    """The daily state sweep; returns arrays named as player_game_states_v3.npz."""
    game_id, pids = g["game_id"], g["pids"].astype(np.int64)
    dates = g["date"].astype(np.int32)
    possessions = g["possessions"].astype(np.float64)
    max_pid = int(pids.max())
    keys = np.unique(np.column_stack([np.repeat(game_id, 5), pids.ravel()]), axis=0)
    game_date = pd.Series(dates, index=game_id).groupby(level=0).first()
    key_dates = game_date.reindex(keys[:, 0]).to_numpy(np.int32)
    order = np.lexsort((keys[:, 1], key_dates))
    keys, key_dates = keys[order], key_dates[order]

    gp = gp[gp.pid <= max_pid].copy()
    gp["date"] = gp.game_id.map(game_date)
    gp = gp[gp.date.notna()].copy()
    flat = pd.DataFrame({"game_id": np.repeat(game_id, 5), "pid": pids.ravel()})
    for b in range(6):
        flat[f"la{b}"] = g["loc_attempt"][:, :, b].ravel()
        flat[f"lm{b}"] = g["loc_make"][:, :, b].ravel()
    loc = flat.groupby(["game_id", "pid"], as_index=False).sum()
    gp = gp.merge(loc, on=["game_id", "pid"], how="left").fillna(
        {f"la{b}": 0. for b in range(6)} | {f"lm{b}": 0. for b in range(6)})
    gp = gp.sort_values(["date", "game_id", "pid"], kind="mergesort")
    gp_by_date = {int(d): block for d, block in gp.groupby("date", sort=True)}

    n_players, n_count = max_pid + 1, 21
    c180 = np.zeros((n_players, n_count))
    q180, c730, q730 = np.zeros_like(c180), np.zeros_like(c180), np.zeros_like(c180)
    active, last_seen = np.zeros(n_players, bool), np.full(n_players, -1, np.int32)
    ctx_num, ctx_den = np.zeros((n_players, 4)), np.zeros(n_players)
    role_w, role_sum, role_sum2 = np.zeros(n_players), np.zeros(n_players), np.zeros(n_players)
    outputs = {k: [] for k in ("game_id", "pid") + FIELDS}
    origins = {k: [] for k in ("origin_index", "pid") + FIELDS}
    fallback = {k: [] for k in ("origin_index", "base", "x", "neff")}
    group_by_date = {int(d): np.flatnonzero(dates == d) for d in np.unique(dates)}
    key_frame = pd.DataFrame({"game_id": keys[:, 0], "pid": keys[:, 1], "date": key_dates})
    appearances = {int(day): block for day, block in key_frame.groupby("date")}
    origin_day = pd.to_datetime(schedule.start).to_numpy("datetime64[D]").astype(np.int32)
    origin_by_day = {int(d): np.flatnonzero(origin_day == d) for d in np.unique(origin_day)}
    previous = None

    for day in sorted(set(appearances) | set(origin_by_day)):
        if previous is not None:
            f180, f730 = 2 ** (-(day - previous) / 180.), 2 ** (-(day - previous) / 730.)
            c180 *= f180
            q180 *= f180 ** 2
            c730 *= f730
            q730 *= f730 ** 2
            ctx_num *= f180
            ctx_den *= f180
            role_w *= f180
            role_sum *= f180
            role_sum2 *= f180
        base_all, neff_all, orb_all, contrast_all = state_from_counts(c180, q180, c730, q730, active)
        missing = (neff_all <= 0).astype(float)
        context = np.divide(ctx_num, ctx_den[:, None], out=np.zeros_like(ctx_num), where=ctx_den[:, None] > 0)
        stale = np.where(last_seen >= 0, np.maximum(day - last_seen, 0), 3650)
        role_mean = np.divide(role_sum, role_w, out=np.zeros_like(role_sum), where=role_w > 0)
        role_var = np.divide(role_sum2, role_w, out=np.zeros_like(role_sum2), where=role_w > 0) - role_mean ** 2
        role_sd = np.sqrt(np.maximum(role_var, 0.))
        x_all = np.column_stack([base_all, np.log1p(neff_all), missing, orb_all, contrast_all, context,
                                 np.log1p(stale)])

        def export(ids):
            return dict(base=base_all[ids].astype(np.float32), x=x_all[ids].astype(np.float32),
                        neff=neff_all[ids].astype(np.float32), last_seen=last_seen[ids].astype(np.int32),
                        role_mean=role_mean[ids].astype(np.float32), role_sd=role_sd[ids].astype(np.float32),
                        role_weight=role_w[ids].astype(np.float32))

        block = appearances.get(day)
        if block is not None:
            ids = block.pid.to_numpy(np.int64)
            outputs["game_id"].append(block.game_id.to_numpy(np.int64))
            outputs["pid"].append(ids.astype(np.int32))
            for k, v in export(ids).items():
                outputs[k].append(v)
        for origin_index in origin_by_day.get(day, []):
            ids = np.flatnonzero(active)
            origins["origin_index"].append(np.full(len(ids), origin_index, np.int16))
            origins["pid"].append(ids.astype(np.int32))
            for k, v in export(ids).items():
                origins[k].append(v)
            prior = int(np.flatnonzero(~active)[0]) if (~active).any() else 0
            fallback["origin_index"].append(np.array([origin_index], np.int16))
            fallback["base"].append(base_all[prior:prior + 1].astype(np.float32))
            fallback["x"].append(x_all[prior:prior + 1].astype(np.float32))
            fallback["neff"].append(neff_all[prior:prior + 1].astype(np.float32))

        rows = group_by_date.get(day, np.empty(0, np.int64))
        if len(rows):
            unit = pids[rows]
            location = np.exp(base_all[:, 3:9])
            location /= location.sum(1, keepdims=True)
            metrics = np.column_stack([np.exp(base_all[:, 0]) + 0.44 * np.exp(base_all[:, 1]) + np.exp(base_all[:, 2]),
                                       np.exp(base_all[:, 16]), np.exp(base_all[:, 0]) * location[:, 4:6].sum(1),
                                       _sigmoid(base_all[:, 17])])[unit]
            other = (metrics.sum(axis=1, keepdims=True) - metrics) / 4.
            weight = possessions[rows, None, None]
            np.add.at(ctx_num, unit.ravel(), (weight * other).reshape(-1, 4))
            np.add.at(ctx_den, unit.ravel(), np.broadcast_to(possessions[rows, None], unit.shape).ravel())
            observed = g["fga_observed"][rows] & g["fta_observed"][rows]
            components = g["fga"][rows] + 0.44 * g["fta"][rows] + g["turnover"][rows]
            totals = components.sum(1)
            valid = observed & (totals > 0)
            if valid.any():
                shares = components[valid] / totals[valid, None]
                ids = unit[valid].ravel()
                rw = np.broadcast_to(possessions[rows][valid, None], shares.shape).ravel()
                values = shares.ravel()
                np.add.at(role_w, ids, rw)
                np.add.at(role_sum, ids, rw * values)
                np.add.at(role_sum2, ids, rw * values ** 2)

        update = gp_by_date.get(day)
        if update is not None:
            values = np.column_stack([
                update.ton_poss.to_numpy(float),
                (update.own_fg2m + update.own_fg2x + update.own_fg3m + update.own_fg3x).to_numpy(float),
                (update.own_ftm + update.own_ftx).to_numpy(float), update.own_ftm.to_numpy(float),
                update.own_tov.to_numpy(float), update.own_ast.to_numpy(float), update.own_orb.to_numpy(float),
                (update.own_fg2m + update.own_fg3m).to_numpy(float), update.own_shot_ast.to_numpy(float),
                *[update[f"la{b}"].to_numpy(float) for b in range(6)],
                *[update[f"lm{b}"].to_numpy(float) for b in range(6)]])
            daily = pd.DataFrame(values)
            daily["pid"] = update.pid.to_numpy(np.int64)
            daily = daily.groupby("pid", as_index=False).sum()
            ids, values = daily.pid.to_numpy(np.int64), daily.drop(columns="pid").to_numpy()
            for counts in (c180, q180, c730, q730):
                np.add.at(counts, ids, values)
            active[ids] = True
            last_seen[ids] = day
        previous = day
        if log is not None and block is not None and len(outputs["pid"]) % 1000 == 0:
            log(f"states through {np.datetime64(day, 'D')}")

    arrays = {k: np.concatenate(v, axis=0) for k, v in outputs.items()}
    arrays |= {"origin_" + k: np.concatenate(v) for k, v in origins.items()}
    arrays |= {"fallback_" + k: np.concatenate(v) for k, v in fallback.items()}
    return arrays


REBOUND_LABELS = paths.CACHE / "joint_capability_2026_09_15_v14_labels" / "rebound_labels.npz"


def rebound_sweep(labels, offense, schedule):
    """Offensive-rebound capture states (half-life 180 days), aligned with the offensive states.

    labels: rebound_labels.npz arrays (game_id, pids, date, counts[:, 6]);
    offense: arrays from ``sweep`` (keys pid, game_id, origin_pid, origin_origin_index).
    Ported from joint_capability_v14_data.build_states; reproduces rebound_states.npz.
    """
    s = {k: offense[k] for k in ("pid", "game_id", "origin_pid", "origin_origin_index", "fallback_origin_index")}
    origin_days = np.array([np.datetime64(x, "D").astype(int) for x in pd.to_datetime(schedule.start)])
    dates, pids = labels["date"], labels["pids"]
    n = int(max(pids.max(), s["pid"].max())) + 1
    num, den, den2, last = np.zeros(n), np.zeros(n), np.zeros(n), np.full(n, -1, np.int32)
    league_num = league_den = 0.
    previous = None
    group_order = np.argsort(dates, kind="stable")
    unique, starts = np.unique(dates[group_order], return_index=True)
    by_day = {int(d): ix for d, ix in zip(unique, np.split(group_order, starts[1:]))}
    game_dates = dict(zip(labels["game_id"], dates))
    state_day = np.array([game_dates[int(k)] for k in s["game_id"]])
    state_order = np.argsort(state_day, kind="stable")
    ud, st = np.unique(state_day[state_order], return_index=True)
    states_by_day = {int(d): ix for d, ix in zip(ud, np.split(state_order, st[1:]))}
    f32 = lambda size: np.zeros(size, np.float32)
    out = dict(prob=f32(len(s["pid"])), neff=f32(len(s["pid"])), last_seen=np.full(len(s["pid"]), -1, np.int32),
               numerator=f32(len(s["pid"])), denominator=f32(len(s["pid"])), denominator2=f32(len(s["pid"])),
               origin_prob=f32(len(s["origin_pid"])), origin_neff=f32(len(s["origin_pid"])),
               origin_last_seen=np.full(len(s["origin_pid"]), -1, np.int32), origin_numerator=f32(len(s["origin_pid"])),
               origin_denominator=f32(len(s["origin_pid"])), origin_denominator2=f32(len(s["origin_pid"])),
               fallback_prob=np.zeros(len(schedule)), league_capture=np.zeros(len(schedule)),
               game_league_capture=f32(len(s["pid"])))
    for d in sorted(set(by_day) | set(map(int, origin_days))):
        if previous is not None:
            decay = 2 ** (-(d - previous) / 180.)
            num *= decay
            den *= decay
            den2 *= decay ** 2
            league_num *= decay
            league_den *= decay
        mu = league_num / league_den if league_den > 0 else .25
        p = (num + 50 * mu / 5) / (den + 50)
        eff = np.divide(den ** 2, den2, out=np.zeros(n), where=den2 > 0)
        if d in states_by_day:
            ix = states_by_day[d]
            ids = s["pid"][ix]
            out["prob"][ix], out["neff"][ix], out["last_seen"][ix] = p[ids], eff[ids], last[ids]
            out["numerator"][ix], out["denominator"][ix], out["denominator2"][ix] = num[ids], den[ids], den2[ids]
            out["game_league_capture"][ix] = mu
        for oi in np.flatnonzero(origin_days == d):
            ix = np.flatnonzero(s["origin_origin_index"] == oi)
            ids = s["origin_pid"][ix]
            out["origin_prob"][ix], out["origin_neff"][ix], out["origin_last_seen"][ix] = p[ids], eff[ids], last[ids]
            out["origin_numerator"][ix], out["origin_denominator"][ix] = num[ids], den[ids]
            out["origin_denominator2"][ix] = den2[ids]
            out["league_capture"][oi], out["fallback_prob"][oi] = mu, mu / 5
        if d in by_day:
            ix = by_day[d]
            live = labels["counts"][ix].sum(1)
            ids = pids[ix].ravel()
            exposure = np.repeat(live, 5)
            np.add.at(num, ids, labels["counts"][ix, :5].ravel())
            np.add.at(den, ids, exposure)
            np.add.at(den2, ids, exposure)
            last[np.unique(ids[exposure > 0])] = d
            league_num += labels["counts"][ix, :5].sum()
            league_den += live.sum()
        previous = d
    if (out["last_seen"] >= state_day).any():
        raise AssertionError("same- or future-day data leaked into rebound states")
    return s | out | dict(date=state_day, origin_date=origin_days)


DEFENSE_FEATURES = ("steal", "block", "drb", "foul", "allowed_to", "allowed_fta",
                    *[f"location_{i}" for i in range(6)], *[f"conversion_{i}" for i in range(6)], "log_exposure")
DEFENSE_PRIOR = np.array([.015, .01, .03, .035, .14, .22, .35, .15, .12, .20, .02, .16, .6, .4, .4, .4, .36, .36])


def defensive_game_counts(g, gp):
    """Per player-game defensive numerators and denominators (own events and on-floor opponent outcomes)."""
    own = ["own_stl", "own_blk", "own_drb", "own_fcommit", "don_poss"]
    gp = gp.groupby(["game_id", "pid"], as_index=False)[own].sum()
    keys = np.unique(np.c_[np.repeat(g["game_id"], 5), g["defense"].ravel()], axis=0)
    queries = np.unique(np.r_[keys, np.c_[np.repeat(g["game_id"], 5), g["pids"].ravel()]], axis=0)
    factor = int(queries[:, 1].max()) + 1
    qcode = queries[:, 0] * factor + queries[:, 1]
    dcode = g["game_id"][:, None] * factor + g["defense"]
    ix = np.searchsorted(qcode, dcode)
    if not np.array_equal(qcode[ix], dcode):
        raise ValueError("game player map")
    num, den = np.zeros((len(queries), 18)), np.zeros((len(queries), 18))
    ref = gp.set_index(["game_id", "pid"]).reindex(pd.MultiIndex.from_arrays(queries.T))
    if ref.isna().any().any():
        raise ValueError("missing game-player statistics")
    num[:, :4] = ref[own[:4]].to_numpy()
    den[:, :4] = ref.don_poss.to_numpy()[:, None]
    n, mask = g["possessions"], g["fga_observed"] & g["location_observed"]
    nums = np.c_[g["turnover"].sum(1), g["fta"].sum(1) * g["fta_observed"], g["loc_attempt"].sum(1) * mask[:, None],
                 g["loc_make"].sum(1) * mask[:, None]]
    dens = np.c_[n, n * g["fta_observed"], np.repeat((g["loc_attempt"].sum((1, 2)) * mask)[:, None], 6, axis=1),
                 g["loc_attempt"].sum(1) * mask[:, None]]
    for s in range(5):
        np.add.at(num[:, 4:], ix[:, s], nums)
        np.add.at(den[:, 4:], ix[:, s], dens)
    dates = pd.Series(g["date"], index=g["game_id"]).groupby(level=0).first()
    return queries, dates.reindex(queries[:, 0]).to_numpy(np.int32), num, den


def defense_profile(numerator, denominator, league_num, league_den):
    prior = np.divide(league_num, league_den, out=DEFENSE_PRIOR.copy(), where=league_den > 0)
    rates = (numerator + 1000. * prior) / (denominator + 1000.)
    return np.c_[rates, np.log1p(denominator[:, 4])].astype(np.float32), prior


def defense_sweep(g, gp, schedule):
    """Dated defensive descriptors (half-life 365 days), queried before each day's games.

    g: game x offense five x defense five matchup arrays; gp: player-game box counts.
    Ported from joint_capability_v15_data.build_states; reproduces defense_states.npz.
    """
    keys, dates, nums, dens = defensive_game_counts(g, gp)
    maxpid = int(max(g["pids"].max(), g["defense"].max())) + 1
    n, d = np.zeros((maxpid, 18)), np.zeros((maxpid, 18))
    seen, active = np.full(maxpid, -1, np.int32), np.zeros(maxpid, bool)
    x, last = np.zeros((len(keys), 19), np.float32), np.full(len(keys), -1, np.int32)
    odates = pd.to_datetime(schedule.start).to_numpy("datetime64[D]").astype(np.int32)
    days = np.union1d(dates, odates)
    byday = np.argsort(dates, kind="stable")
    sdates = dates[byday]
    origins, fallbacks = [], {}
    previous = int(days[0])
    for day in days:
        decay = np.exp2(-(int(day) - previous) / 365.)
        n *= decay
        d *= decay
        previous = int(day)
        league_num, league_den = n.sum(0), d.sum(0)
        for oi in np.flatnonzero(odates == day):
            ids = np.flatnonzero(active)
            ox, prior = defense_profile(n[ids], d[ids], league_num, league_den)
            origins.append((int(oi), ids.copy(), ox, seen[ids].copy()))
            fallbacks[int(oi)] = np.r_[prior, 0.].astype(np.float32)
        lo, hi = np.searchsorted(sdates, [day, day + 1])
        ix = byday[lo:hi]
        if len(ix):
            pids = keys[ix, 1]
            x[ix], _ = defense_profile(n[pids], d[pids], league_num, league_den)
            last[ix] = seen[pids]
            np.add.at(n, pids, nums[ix])
            np.add.at(d, pids, dens[ix])
            observed = dens[ix, 4] > 0
            seen[pids[observed]] = day
            active[pids[observed]] = True
    origin_index = np.concatenate([np.full(len(ids), oi, np.int32) for oi, ids, _, _ in origins])
    origin_last = np.concatenate([v for _, _, _, v in origins])
    if (last >= dates).any() or (origin_last >= odates[origin_index]).any():
        raise ValueError("future defensive state")
    return dict(game_id=keys[:, 0], pid=keys[:, 1], date=dates, x=x, last_seen=last, origin_index=origin_index,
                origin_pid=np.concatenate([ids for _, ids, _, _ in origins]),
                origin_x=np.concatenate([v for _, _, v, _ in origins]), origin_last_seen=origin_last,
                origin_date=odates, fallback=np.stack([fallbacks[i] for i in range(len(schedule))]),
                features=np.asarray(DEFENSE_FEATURES))


# ---- origin states of a store (scripts/build_prospective_store.py, build_era_store.py) -------------
ROLE = slice(55, 63)                     # the role columns of the x vector
MATCHUPS = paths.CACHE / "joint_capability_2026_09_17_v15_inputs" / "matchups.npz"


def origin_states(schedule, players_path=GAME_PLAYERS):
    """A store's offense_origins.npz and defense_origins.npz contents for a schedule, from the three sweeps.

    players_path: the per-(game, player) counts (lineups.player_counts); the default is the legacy file."""
    g, gp = load_inputs(players_path=players_path)
    offense = sweep(g, gp, schedule)
    with np.load(REBOUND_LABELS) as z:
        labels = {k: z[k] for k in z.files}
    rebound = rebound_sweep(labels, offense, schedule)
    with np.load(MATCHUPS) as z:
        matchups = {k: z[k] for k in z.files}
    defense = defense_sweep(matchups, gp, schedule)
    o = np.lexsort((offense["origin_pid"].astype(np.int64), offense["origin_origin_index"]))
    fb = np.argsort(offense["fallback_origin_index"])
    d = np.lexsort((defense["origin_pid"], defense["origin_index"]))
    origins = dict(
        offense=dict(origin_index=offense["origin_origin_index"][o].astype(np.int64),
                     pid=offense["origin_pid"][o].astype(np.int64), base=offense["origin_base"][o],
                     role=offense["origin_x"][o][:, ROLE], rb_prob=rebound["origin_prob"][o],
                     rb_neff=rebound["origin_neff"][o], fallback_base=offense["fallback_base"][fb],
                     fallback_role=offense["fallback_x"][fb][:, ROLE], fallback_rb_prob=rebound["fallback_prob"],
                     league=rebound["league_capture"],
                     origin_tags=(schedule.season.astype(str) + "q" + schedule.window.astype(str)).to_numpy(dtype="U8")),
        defense=dict(origin_index=defense["origin_index"][d].astype(np.int64), pid=defense["origin_pid"][d],
                     x=defense["origin_x"][d], fallback=defense["fallback"], origin_date=defense["origin_date"]))
    return origins, (offense, rebound)


def write_origins(out, origins):
    np.savez(out / "offense_origins.npz", **origins["offense"])
    np.savez(out / "defense_origins.npz", **origins["defense"])
