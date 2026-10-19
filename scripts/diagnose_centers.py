"""Saved-weight diagnosis of the five-center coherence failure (exploratory).

Reference J_POINT_BOTH at 2026q4: all three seeds' checkpoint mixtures (14
states). Native points/100 before calibration. Path switches are accounting on
saved weights, not causal effects and not refits.

Sections:
  1. team and per-player ledgers, against a neutral defense and in the matchups;
  2. defensive effect vectors, against the distribution of real defensive fives;
  3. tanh saturation and input outlyingness for fixtures versus real lineups;
  4. per-attacker defensive effect for the Jokic lineups attacking the centers,
     split by effect group (actions, location, conversion, recovery);
  5. center ladder: replace Jokic-lineup players by centers one at a time;
  6. all five centers in at once versus five single swaps, from real defenses.

Output: experiments/cache/diagnose_centers_2026_10_09/ (tables as CSV, summary JSON).
"""
import json

import numpy as np
import pandas as pd
import torch

import property_suite
from lineups import legacy, paths, properties
from lineups.coherence import batch, checkpoint_models, fixtures, ledgers, neutral
from lineups.features import Store
from lineups.model import average_ledgers, centered, moments

ORIGIN = "2026q4"
OUT = paths.CACHE / "diagnose_centers_2026_10_09"
LOCATIONS = ("rim", "paint", "mid", "longmid", "c3", "ab3")
EFFECTS = ("fga", "fta", "tov") + tuple(f"loc_{x}" for x in LOCATIONS) + tuple(f"make_{x}" for x in LOCATIONS)
GROUPS = dict(actions=slice(0, 3), location=slice(3, 9), conversion=slice(9, 15))
LINEUPS = ("legal_pure_centers", "five_goberts", "five_jokics", "jokic_westbrook", "jokic_korver",
           "highest_exposure_real_2026", "small_guards", "limited_centers")


class Mask:
    """Temporarily scale defensive effects: keep[16] multiplies the 15 effects and recovery."""

    def __init__(self, models, keep):
        self.models, self.keep = models, torch.as_tensor(keep, dtype=torch.float32)

    def __enter__(self):
        for m in self.models:
            main, adjusted, keep = m.defense.forward, m.adjusted.defense_effect, self.keep
            m.defense.forward = lambda d, main=main: (lambda e, r: (e * keep[:15], r * keep[15]))(*main(d))
            m.adjusted.defense_effect = lambda a, adjusted=adjusted: adjusted(a) * keep
        return self

    def __exit__(self, *exc):
        for m in self.models:
            del m.defense.forward, m.adjusted.defense_effect


def predict(models, inputs, env):
    with torch.no_grad():
        return average_ledgers([m.eval()(inputs, env) for m in models])


def team_table(pred, labels):
    loc = pred.expected_attempts.sum(1)            # [B,6] team attempts per starting possession
    makes = pred.expected_makes.sum(1)
    fga = loc.sum(1)
    three = loc[:, 4:].sum(1)
    efg = (makes.sum(1) + .5 * makes[:, 4:].sum(1)) / fga
    return pd.DataFrame(dict(
        lineup=labels, points=pred.points100.numpy(), fga=100 * fga.numpy(), fta=100 * pred.fta.sum(1).numpy(),
        tov=100 * pred.turnover.sum(1).numpy(), rim_share=(loc[:, 0] / fga).numpy(), three_share=(three / fga).numpy(),
        rim_make=(makes[:, 0] / loc[:, 0]).numpy(), three_make=(makes[:, 4:].sum(1) / three).numpy(), efg=efg.numpy(),
        renewed=100 * pred.renewed_usage.numpy(), initial=100 * pred.initial_usage.numpy()))


def player_table(pred, inputs, names, label):
    rows = []
    own_make = torch.sigmoid(inputs["base"][..., 9:15])
    own_loc = torch.softmax(inputs["base"][..., 3:9], -1)
    for i, name in enumerate(names):
        att = pred.expected_attempts[0, i]
        rows.append(dict(lineup=label, player=name, points=100 * float(pred.player_points[0, i]),
                         fga=100 * float(pred.fga[0, i]), fta=100 * float(pred.fta[0, i]),
                         tov=100 * float(pred.turnover[0, i]), rim_share=float(att[0] / att.sum()),
                         own_rim_share=float(own_loc[0, i, 0]), three_share=float(att[4:].sum() / att.sum()),
                         own_three_share=float(own_loc[0, i, 4:].sum()), rim_make=float(pred.make[0, i, 0]),
                         own_rim_make=float(own_make[0, i, 0]), ab3_make=float(pred.make[0, i, 5]),
                         own_ab3_make=float(own_make[0, i, 5])))
    return rows


def defense_parts(models, inputs):
    """Pre-activation and bounded defensive effects (model mean), plus hidden-unit saturation."""
    pre_main, pre_adj, effect, hidden = [], [], [], []
    with torch.no_grad():
        for m in models:
            d = inputs["defense"]
            z = torch.cat([d.mean(1), d.var(1, unbiased=False).clamp(min=1e-12).sqrt()], -1)
            za = moments(inputs["adjusted_defense"])[:, 0]
            pm = torch.cat([centered(m.defense.main, z), centered(m.defense.recovery, z)], -1)
            pa = centered(m.adjusted.defense, za)
            pre_main.append(pm)
            pre_adj.append(pa)
            effect.append(torch.tanh(pm) + torch.tanh(pa))
            hidden.append(torch.cat([torch.tanh(m.defense.main[0](z)), torch.tanh(m.adjusted.defense[0](za))], -1))
    mean = lambda xs: torch.stack(xs).mean(0).numpy()
    saturated = (torch.stack(hidden).abs() > .95).float().mean((0, 2)).numpy()
    return dict(pre_main=mean(pre_main), pre_adjusted=mean(pre_adj), effect=mean(effect), saturated=saturated,
                z=torch.cat([inputs["defense"].mean(1), inputs["defense"].std(1, unbiased=False)], -1).numpy())


def mahalanobis(reference, points, ridge=1e-3):
    mu = reference.mean(0)
    cov = np.cov(reference, rowvar=False) + ridge * np.eye(reference.shape[1])
    inv = np.linalg.inv(cov)
    d = lambda x: np.sqrt(np.einsum("...i,ij,...j->...", x - mu, inv, x - mu))
    return d(reference), d(points)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    store, fx = Store(), fixtures()
    env = store.env(ORIGIN, "final")
    models = checkpoint_models(ORIGIN)
    summary = dict(origin=ORIGIN, states=len(models))
    print(f"{len(models)} checkpoint states at {ORIGIN}")

    # 1. Ledgers: each lineup against the neutral defense, and the four center matchups.
    off = [fx[k]["pids"] for k in LINEUPS]
    vs_neutral = team_table(predict(models, neutral(batch(store, off, off, ORIGIN)), env), list(LINEUPS))
    pairs = [("legal_pure_centers", "jokic_westbrook"), ("legal_pure_centers", "jokic_korver"),
             ("five_goberts", "jokic_westbrook"), ("five_jokics", "jokic_westbrook")]
    a = [fx[x]["pids"] for x, _ in pairs]
    b = [fx[y]["pids"] for _, y in pairs]
    forward = predict(models, batch(store, a, b, ORIGIN), env)
    reverse = predict(models, batch(store, b, a, ORIGIN), env)
    matchups = pd.DataFrame(dict(a=[x for x, _ in pairs], b=[y for _, y in pairs],
                                 a_offense=forward.points100.numpy(), b_offense=reverse.points100.numpy()))
    matchups["margin"] = matchups.a_offense - matchups.b_offense
    neutral_points = vs_neutral.set_index("lineup").points
    matchups["a_vs_neutral"] = matchups.a.map(neutral_points)
    matchups["b_vs_neutral"] = matchups.b.map(neutral_points)
    matchups["neutral_margin"] = matchups.a_vs_neutral - matchups.b_vs_neutral
    print("\n== Team offense against a neutral defense (native pts/100 starting possessions)")
    print(vs_neutral.round(3).to_string(index=False))
    real_offense = property_suite.real_fives(ORIGIN, legacy.matchups(), legacy.FIVE)
    real_points = ledgers(models, store, real_offense, None, ORIGIN).points100.numpy()
    vs_neutral["real_percentile"] = [(real_points < v).mean() for v in vs_neutral.points]
    print(f"real {ORIGIN} offense fives with >= 50 possessions: {len(real_points)}, median "
          f"{np.median(real_points):.2f}, p10 {np.quantile(real_points, .1):.2f}; percentiles:",
          ", ".join(f"{k} {v:.2f}" for k, v in zip(vs_neutral.lineup, vs_neutral.real_percentile)))
    print("\n== Matchups (native, both directions)")
    print(matchups.round(3).to_string(index=False))

    players = []
    for k in ("legal_pure_centers", "five_goberts", "five_jokics", "jokic_westbrook", "highest_exposure_real_2026"):
        one = batch(store, [fx[k]["pids"]], [fx[k]["pids"]], ORIGIN)
        players += player_table(predict(models, neutral(one), env), one, fx[k]["names"], k)
    players = pd.DataFrame(players)
    print("\n== Players against a neutral defense (own_* = player's dated own rate)")
    print(players.round(3).to_string(index=False))

    # 2-3. Defensive effects and saturation versus the real 2026q4 defensive fives.
    g = legacy.matchups()
    rows = legacy.quarter_rows(legacy.schedule().query("tag == @ORIGIN").iloc[0], g)
    real_off, real_def = np.asarray(g["pids"][rows]), np.asarray(g["defense"][rows])
    real = defense_parts(models, batch(store, real_off, real_def, ORIGIN))
    fixture_def = defense_parts(models, batch(store, off, off, ORIGIN))
    names = list(EFFECTS) + ["recovery"]
    table = []
    for i, lineup in enumerate(LINEUPS):
        for j, effect in enumerate(names):
            table.append(dict(lineup=lineup, effect=effect, value=fixture_def["effect"][i, j],
                              pre_main=fixture_def["pre_main"][i, j], pre_adjusted=fixture_def["pre_adjusted"][i, j],
                              real_p01=np.quantile(real["effect"][:, j], .01),
                              real_p50=np.quantile(real["effect"][:, j], .5),
                              real_p99=np.quantile(real["effect"][:, j], .99),
                              percentile=(real["effect"][:, j] < fixture_def["effect"][i, j]).mean()))
    effects = pd.DataFrame(table)
    wide = effects.pivot(index="effect", columns="lineup", values="value").loc[names]
    wide["real_p01"] = effects.groupby("effect").real_p01.first().loc[names]
    wide["real_p50"] = effects.groupby("effect").real_p50.first().loc[names]
    wide["real_p99"] = effects.groupby("effect").real_p99.first().loc[names]
    print("\n== Defensive effect as defender (log-rate / logit shifts; model mean), with real 2026q4 range")
    print(wide.round(3).to_string())

    dist_real, dist_fix = mahalanobis(real["z"], fixture_def["z"])
    outlying = pd.DataFrame(dict(lineup=LINEUPS, mahalanobis=dist_fix,
                                 real_percentile=[(dist_real < d).mean() for d in dist_fix],
                                 hidden_saturated=fixture_def["saturated"]))
    print(f"\n== Defensive input distance (38-dim mean/sd); real 2026q4 rows: median "
          f"{np.median(dist_real):.2f}, p99 {np.quantile(dist_real, .99):.2f}, max {dist_real.max():.2f}; "
          f"real hidden saturation {real['saturated'].mean():.3f}")
    print(outlying.round(3).to_string(index=False))
    zs = (fixture_def["z"] - real["z"].mean(0)) / real["z"].std(0)
    feature_names = ["steal", "block", "drb", "foul", "allowed_to", "allowed_fta"] + \
        [f"allowed_loc_{x}" for x in LOCATIONS] + [f"allowed_make_{x}" for x in LOCATIONS] + ["log_exposure"]
    z_names = [f"mean_{x}" for x in feature_names] + [f"sd_{x}" for x in feature_names]
    i = LINEUPS.index("legal_pure_centers")
    top = np.argsort(-np.abs(zs[i]))[:10]
    print("legal_pure_centers most extreme defensive inputs (z vs real fives):",
          ", ".join(f"{z_names[t]} {zs[i, t]:+.1f}" for t in top))

    # 4. Per-attacker defensive effect, by effect group, for the Jokic lineups attacking the centers.
    attack = []
    for victim in ("jokic_westbrook", "jokic_korver"):
        one = batch(store, [fx[victim]["pids"]], [fx["legal_pure_centers"]["pids"]], ORIGIN)
        base = predict(models, neutral(one), env)
        full = predict(models, one, env)
        parts = {"none": base, "all": full}
        for group, cut in list(GROUPS.items()) + [("recovery", slice(15, 16))]:
            keep = np.zeros(16, np.float32)
            keep[cut] = 1
            with Mask(models, keep):
                parts[group] = predict(models, one, env)
        for i, name in enumerate(fx[victim]["names"]):
            rec = dict(offense=victim, player=name)
            for group, pred in parts.items():
                rec[group] = 100 * float(pred.player_points[0, i])
            rec["three_share_none"] = float(base.expected_attempts[0, i, 4:].sum() / base.expected_attempts[0, i].sum())
            rec["three_share_all"] = float(full.expected_attempts[0, i, 4:].sum() / full.expected_attempts[0, i].sum())
            rec["ab3_make_none"], rec["ab3_make_all"] = float(base.make[0, i, 5]), float(full.make[0, i, 5])
            rec["rim_make_none"], rec["rim_make_all"] = float(base.make[0, i, 0]), float(full.make[0, i, 0])
            attack.append(rec)
        attack.append(dict(offense=victim, player="TEAM", **{k: float(v.points100[0]) for k, v in parts.items()}))
    attack = pd.DataFrame(attack)
    for k in ("all",) + tuple(GROUPS) + ("recovery",):
        attack[f"d_{k}"] = attack[k] - attack["none"]
    print("\n== Jokic lineups attacking the five centers: points by attacker, defense switched on by group")
    print(attack[["offense", "player", "none", "d_all", "d_actions", "d_location", "d_conversion", "d_recovery",
                  "three_share_none", "three_share_all", "ab3_make_none", "ab3_make_all",
                  "rim_make_none", "rim_make_all"]].round(3).to_string(index=False))

    # 5. Center ladder: Jokic/Westbrook lineup with k players replaced by centers (most perimeter first).
    # Descriptive only: each step replaces a different player, so step increments are not the marginal
    # effect of one more center (lineups.properties measures that as synergy).
    jw = fx["jokic_westbrook"]
    centers = fx["legal_pure_centers"]
    order = [4, 1, 3, 2, 0]   # Westbrook, Murray, Porter, Gordon, Jokic
    ladder_pids, ladder_names = [], []
    pids, names_now = list(jw["pids"]), list(jw["names"])
    ladder_pids.append(list(pids))
    ladder_names.append("+".join(n.split()[-1] for n in names_now))
    for k, slot in enumerate(order):
        pids[slot], names_now[slot] = centers["pids"][k], centers["names"][k]
        ladder_pids.append(list(pids))
        ladder_names.append("+".join(n.split()[-1] for n in names_now))
    lb = batch(store, ladder_pids, ladder_pids, ORIGIN)
    lad = team_table(predict(models, neutral(lb), env), ladder_names)
    lad.insert(1, "centers", range(6))
    ld = defense_parts(models, lb)
    lad["def_fga"], lad["def_tov"], lad["def_make_rim"], lad["def_make_ab3"] = (
        ld["effect"][:, 0], ld["effect"][:, 2], ld["effect"][:, 9], ld["effect"][:, 14])
    print("\n== Center ladder (offense vs neutral; defensive effects as defender)")
    print(lad.round(3).to_string(index=False))

    # 6. Synergy at the extreme: the 40 most-used real defenses without these centers, all five centers in
    #    together versus the five single swaps (shortest defender first) added up, against the Jokic lineups.
    predict_fn = lambda o, d: ledgers(models, store, o, d, ORIGIN)
    real_defenses = [d for d in property_suite.real_fives(ORIGIN, g, legacy.DEFENSE)[:40]
                     if not np.isin(d, centers["pids"]).any()]
    heights = properties.roles(store, ORIGIN, np.ravel(real_defenses)).height
    extreme = []
    for d in real_defenses:
        stacks = properties.synergy_cases(d, np.argsort(heights.reindex(d).fillna(0).to_numpy()),
                                          list(centers["pids"]))
        for victim in ("jokic_westbrook", "jokic_korver"):
            p = properties.predict_all(predict_fn, np.tile(fx[victim]["pids"], (len(stacks), 1)), np.array(stacks))
            every = np.ones((len(stacks), 5))
            rec = dict(offense=victim)
            for key, v in (("points", p["points100"]), ("rim_make", properties.weighted_make(p, every, slice(0, 1))),
                           ("three_make", properties.weighted_make(p, every, slice(4, 6)))):
                rec[f"{key}_joint"], rec[f"{key}_singles"] = v[-1] - v[0], (v[1:6] - v[0]).sum()
            extreme.append(rec)
    extreme = pd.DataFrame(extreme)
    print(f"\n== Five centers in at once versus five single swaps, {len(real_defenses)} real base defenses (mean)")
    print(extreme.groupby("offense").mean().round(4).to_string())

    for name, frame in dict(teams=vs_neutral, matchups=matchups, players=players, effects=effects,
                            outlying=outlying, attackers=attack, ladder=lad, extreme=extreme).items():
        frame.to_csv(OUT / f"{name}.csv", index=False)
    summary["real_rows"] = int(len(rows))
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
