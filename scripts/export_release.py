"""Export the release model for the browser tool (docs/CLOSEOUT.md, step 6).

Writes experiments/cache/release_export_2026_10_12/:

    weights.bin   float32, every checkpoint of arms R and C x seeds 17, 23, 41,
                  then the learned module of each seed (lineups.learned);
                  meta.json gives each tensor's offset and shape
    players.bin   float32 [player-seasons, 193]: base 18, role 8, rb_prob,
                  rb_neff, defensive descriptors 19, offensive bank 97,
                  defensive bank 49
    meta.json     everything else the page needs: normalizer, environment,
                  calibration, listings, names, defaults, season normalizer
                  means (era-relative rule), season means (composition
                  reasons), the average-opponent panel, support statistics,
                  band constants and the league-average offense for the
                  explanations, and the combination layer (type flags per
                  player-season and rule, the fitted layer, evidence per effect),
                  the learned combinations (scale, fields, each seed's level), and
                  overall quality (scripts/player_values.py: the linear approximation's
                  offense and points allowed per player-season and input rule, and its level)

tool/lineup_model.js reads these; tests/test_tool_parity.py checks it against
lineups.release, lineups.band and lineups.explain.

    PYTHONPATH=. python -u scripts/export_release.py
"""
import json

import numpy as np
import pandas as pd

from lineups import band, explain, features, learned, model, paths, release
from lineups import combinations as cb
from lineups.players import MEANS, RAW

OUT = release.SOURCE["export"]                 # the release's (lineups.release.DATA)
WIDTHS = dict(base=18, role=8, rb_prob=1, rb_neff=1, defense=19, adjusted_offense=97, adjusted_defense=49)


def tensors(rel):
    chunks, models, offset = [], [], 0
    for arm in release.ARMS:
        for seed in release.SEEDS:
            for i, m in enumerate(rel.models[arm][seed]):
                params = {}
                for name, value in m.state_dict().items():
                    v = value.detach().double().numpy().astype(np.float32)
                    params[name] = [offset, list(v.shape)]
                    chunks.append(v.ravel())
                    offset += v.size
                models.append(dict(arm=arm, seed=seed, checkpoint=i, params=params))
    modules = []
    for seed in release.SEEDS:
        module, level = rel.modules[seed]
        params = {}
        for name, value in module.state_dict().items():
            v = value.detach().double().numpy().astype(np.float32).reshape(-1 if value.ndim else 1)
            params[name] = [offset, list(value.shape)]
            chunks.append(v.ravel())
            offset += v.size
        modules.append(dict(seed=seed, params=params, level=level))
    return np.concatenate(chunks), models, modules


def players_matrix(seasons):
    t = seasons.table
    cols, layout, at = [], {}, 0
    for k in RAW:
        v = t[k].reshape(len(t["pid"]), -1).astype(np.float32)
        assert v.shape[1] == WIDTHS[k], k
        layout[k] = [at, v.shape[1]]
        cols.append(v)
        at += v.shape[1]
    return np.concatenate(cols, 1), layout


def combinations(rel, league):
    """Type flags as bits (types in cb.TYPES order, then H1 small and anchor), the layer and the evidence."""
    comb = cb.Combinations(rel)
    small, anchor = len(cb.TYPES), len(cb.TYPES) + 1
    flags = {}
    for rule in ("relative", "as_was"):
        bits = comb.flags[rule].astype(np.int64) @ (1 << np.arange(len(cb.TYPES)))
        bits |= comb.h1["small"].astype(np.int64) << small
        bits |= comb.h1["anchor"][rule].astype(np.int64) << anchor
        flags[rule] = bits.tolist()
    discovery = cb.LAYER.parents[1] / "interaction_discovery_2026_10_13"
    held = json.loads((discovery / "result.json").read_text())["families"]
    post = pd.read_csv(discovery / "posthoc.csv").set_index(["family", "candidate"])
    unit = cb.team_values(league)
    effects = []
    for event, side, a, b, title in cb.EFFECTS:
        spec = comb.layer.spec["events"][event]
        k = [tuple(x) for x in spec["pairs"]].index((side, a, b))
        found = next(c for c in held[event]["confirmed"] if c["candidate"] == f"{a} x {b}")
        conf, repl = found["confirmation"], found["replication"]
        effects.append(dict(
            id=cb.effect_id(event, side, a, b), event=event, side=side, a=a, b=b, title=title,
            beta=spec["beta"][k], se=spec["se"][k], points_per_pairing=spec["beta"][k] * float(unit[event]),
            label=found["label"], confirmation=dict(coef=conf["coef"], se=conf["se"], seasons=conf["seasons_same_sign"]),
            replication=dict(coef=repl["coef"], se=repl["se"]),
            without_late=post.loc[(event, f"{a} x {b}"), "no_late_confirmation"]))
    return dict(types=list(cb.TYPES), offense=list(cb.OFFENSE), defense=list(cb.DEFENSE), labels=cb.LABELS,
                plurals=cb.PLURALS, units=cb.UNITS, effects=effects, flags=flags, h1_bits=dict(small=small, anchor=anchor),
                layer=dict(events=comb.layer.spec["events"], measured_max=comb.layer.measured_max,
                           measured_share=cb.MEASURED_SHARE, fit=comb.layer.spec["fit"]))


def player_values(seasons):
    """Per input rule: offense and points-allowed values per player-season row (scripts/player_values.py)."""
    import player_values as pv
    with np.load(pv.OUT / "values.npz") as z:
        v = {k: z[k] for k in z.files}
    if not (np.array_equal(v["pid"], seasons.table["pid"]) and np.array_equal(v["season"], seasons.table["season"])):
        raise ValueError("player values do not match the player-season table")
    report = json.loads((pv.OUT / "report.json").read_text())
    return dict(definition="overall quality: each player-season's coefficient in the least-squares linear "
                           "approximation of the network's ratings (scripts/player_values.py)",
                rules={rule: dict(offense=np.round(v[f"{rule}_offense"], 3).tolist(),
                                  defense=np.round(v[f"{rule}_defense"], 3).tolist(),
                                  level=v[f"{rule}_level"].tolist()) for rule in ("relative", "as_was")},
                check={rule: r["checks"] for rule, r in report.items()})


def listify(d):
    return {k: (np.asarray(v).tolist() if not isinstance(v, (int, float, str)) else v) for k, v in d.items()}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rel = release.Release()
    b = band.Band(rel)
    ex = explain.Explainer(rel)
    seasons = rel.seasons
    t = seasons.table

    weights, models, modules = tensors(rel)
    weights.tofile(OUT / "weights.bin")
    matrix, layout = players_matrix(seasons)
    np.ascontiguousarray(matrix).tofile(OUT / "players.bin")

    pids = sorted(set(t["pid"].tolist()))
    listing = rel.store.players
    sup = b.support
    meta = dict(
        origin=release.ORIGIN, seeds=list(release.SEEDS), arms=release.ARMS, forecast=release.FORECAST,
        default_rule=release.RULE, models=models, weights_floats=int(weights.size),
        normalizer=listify(rel.normalizer), env=rel.env, league=rel.league, league_capture=rel.league_capture,
        calibration={k: dict(intercept=v["intercept"], slope=v["slope"]) for k, v in rel.record["calibration"].items()},
        players=dict(count=int(len(t["pid"])), width=int(matrix.shape[1]), layout=layout, pid=t["pid"].tolist(),
                     season=t["season"].tolist(), offense_possessions=np.round(t["offense_possessions"]).tolist(),
                     defense_possessions=np.round(t["defense_possessions"]).tolist(), games=t["games"].tolist()),
        names={str(p): seasons.names[p] for p in pids},
        listings={str(p): [float(listing["height"][p]), float(listing["position"][p])] for p in pids},
        defaults={str(p): s for p, s in seasons.defaults.items()},
        latest_season=seasons.latest,
        season_normalizer=dict(first=seasons.first, means={k: seasons.season_normalizer[k].tolist() for k in MEANS}),
        season_means={str(s): [m[0].tolist(), m[1].tolist()] for s, m in seasons.season_means.items()},
        panel={side: dict(rows=rows.tolist(), weights=w.tolist()) for side, (rows, w) in rel.panel_rows.items()},
        support=dict(limits={k: float(v) for k, v in sup.limits.items()}, big_inches=82, non_shooter=1.,
                     **{side: dict(mean=sup.reference[side]["mean"].tolist(), inverse=sup.reference[side]["inverse"].tolist(),
                                   distance=sup.reference[side]["distance"].tolist()) for side in ("offense", "defense")}),
        band=dict(arms=list(band.ARMS), z=band.Z, tau2=band.TAU2, cross_era_variance=band.CROSS_ERA_VARIANCE,
                  cross_era_correlation=band.CROSS_ERA_CORRELATION, first_training_season=band.FIRST_TRAINING_SEASON,
                  thin_possessions=band.THIN_POSSESSIONS, spread_reason=band.SPREAD_REASON),
        explain=dict(slope=ex.slope, league={k: (v.tolist() if isinstance(v, np.ndarray) else v)
                                             for k, v in ex.league.items()}, locations=list(explain.LOCATIONS)),
        combinations=combinations(rel, ex.league),
        learned=dict(scale=learned.SCALE, fields=list(learned.FIELDS), modules=modules),
        values=player_values(seasons),
        constants=dict(shot_values=list(model.SHOT_VALUES), usage_weights=list(model.USAGE_WEIGHTS),
                       height_scale=list(features.HEIGHT_SCALE), position_scale=list(features.POSITION_SCALE),
                       tiebreak=features.TIEBREAK))
    (OUT / "meta.json").write_text(json.dumps(meta, separators=(",", ":")))
    sizes = {p.name: round(p.stat().st_size / 1e6, 2) for p in OUT.iterdir()}
    print(f"{len(models)} models, {weights.size} weights, {matrix.shape} player matrix; MB: {sizes}")


if __name__ == "__main__":
    main()
