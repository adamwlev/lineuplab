"""Export the pre-refactor input caches into the lineups.features store.

One-time, uses the old ``experiments`` code (tag pre-refactor-2026-10-09) only to
compile capability-library tables and to cross-check batches. Writes
``paths.STORE`` and verifies new batch assembly against the old pipeline on
outer (origin) rows and on training (history) rows.

    PYTHONPATH=. python -u scripts/export_store.py

It imports the retired ``experiments`` package. To rerun it, create the
legacy worktree and put it on the path after this repository:

    bash scripts/legacy_worktree.sh
    PYTHONPATH=.:../basketball-legacy python -u scripts/export_store.py

**From a rebuild's artifacts (2026-10-14, --from-artifacts --out DIR).** The
same tables from the v3, v14 and v15 states and the library under
paths.CACHE (set LINEUPS_CACHE to a rebuild root's cache, and run from that
root so the legacy relative paths resolve there). Normalizers and the
environment are recomputed with lineups.normalizers for every origin from
2015q1, since a rebuild has no legacy run contexts. references.json is
empty: fits on a rebuilt store use lineups.train.self_references.
--from-artifacts on the original cache reproduces lineups_store_v16
(compare_store).
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from lineups import legacy, normalizers, paths, states
from lineups.features import Store

V3 = paths.CACHE / "joint_capability_2026_09_09_v3/derived/player_game_states_v3.npz"
REBOUND = paths.CACHE / "joint_capability_2026_09_15_v14_states/rebound_states.npz"
DEFENSE = paths.CACHE / "joint_capability_2026_09_17_v15_inputs/defense_states.npz"
ROLE = slice(55, 63)


def offense_tables(out):
    with np.load(V3) as z:
        s = {k: z[k] for k in z.files}
    with np.load(REBOUND) as z:
        r = {k: z[k] for k in z.files}
    for a, b in (("pid", "pid"), ("game_id", "game_id"), ("origin_pid", "origin_pid"),
                 ("origin_origin_index", "origin_origin_index"), ("fallback_origin_index", "fallback_origin_index")):
        if not np.array_equal(s[a], r[b]):
            raise ValueError(f"rebound/offense state misalignment: {a}")
    order = np.lexsort((s["pid"].astype(np.int64), s["game_id"]))
    np.savez(out / "offense_games.npz", game_id=s["game_id"][order].astype(np.int64),
             pid=s["pid"][order].astype(np.int64), base=s["base"][order], role=s["x"][order][:, ROLE],
             rb_prob=r["prob"][order], rb_neff=r["neff"][order], league=r["game_league_capture"][order],
             last_seen=s["last_seen"][order])
    o = np.lexsort((s["origin_pid"].astype(np.int64), s["origin_origin_index"]))
    fb = np.argsort(s["fallback_origin_index"])
    if not np.array_equal(s["fallback_origin_index"][fb], np.arange(len(fb))):
        raise ValueError("fallback states must cover origins 0..O-1")
    np.savez(out / "offense_origins.npz", origin_index=s["origin_origin_index"][o].astype(np.int64),
             pid=s["origin_pid"][o].astype(np.int64), base=s["origin_base"][o], role=s["origin_x"][o][:, ROLE],
             rb_prob=r["origin_prob"][o], rb_neff=r["origin_neff"][o],
             fallback_base=s["fallback_base"][fb], fallback_role=s["fallback_x"][fb][:, ROLE],
             fallback_rb_prob=r["fallback_prob"], league=r["league_capture"], origin_tags=s["origin_tags"])


def defense_tables(out):
    with np.load(DEFENSE) as z:
        d = {k: z[k] for k in z.files}
    order = np.lexsort((d["pid"], d["game_id"]))
    np.savez(out / "defense_games.npz", game_id=d["game_id"][order], pid=d["pid"][order], x=d["x"][order],
             last_seen=d["last_seen"][order], features=d["features"])
    o = np.lexsort((d["origin_pid"], d["origin_index"]))
    np.savez(out / "defense_origins.npz", origin_index=d["origin_index"][o].astype(np.int64),
             pid=d["origin_pid"][o], x=d["origin_x"][o], fallback=d["fallback"], origin_date=d["origin_date"])


def library_tables(out, library):
    for bank in ("offense", "defense"):
        dates = np.asarray(library.required, np.int64)
        ids, values, last, offsets = [], [], [], [0]
        tick = time.monotonic()
        for i, d in enumerate(dates):
            library.features(np.zeros((1, 5), np.int64), np.array([d]), bank, metadata=False)
            t = library.feature_cache.pop((int(d), bank))
            ids.append(t["ids"]); values.append(t["values"]); last.append(t["last"])
            offsets.append(offsets[-1] + len(t["ids"]))
            library.cache.clear()
            if (i + 1) % 50 == 0:
                print(f"LIBRARY {bank} {i + 1}/{len(dates)} {time.monotonic() - tick:.0f}s", flush=True)
        np.savez(out / f"library_{bank}.npz", dates=dates, offsets=np.asarray(offsets, np.int64),
                 ids=np.concatenate(ids), values=np.concatenate(values), last=np.concatenate(last))


def context_tables(out, run, schedule):
    (out / "normalizers").mkdir(exist_ok=True)
    env, refs = {}, {}
    for o in schedule.itertuples():
        for phase in ("inner", "final"):
            saved = {}
            for seed in (17, 23, 41):
                c = torch.load(run / "contexts" / o.tag / f"s{seed}" / phase / "context.pt", map_location="cpu",
                               weights_only=False)
                s, ps = c["shared"], c["shared"]["parent_shared"]
                norm = dict(cutoff_day=np.int64(s["cutoff_day"]), base_mean=ps["base_mean"], base_sd=ps["base_sd"],
                            role_mean=ps["mean"][ROLE], role_scale=ps["scale"][ROLE],
                            rebound_mean=ps["new_moments"]["rebound"]["mean"],
                            rebound_scale=ps["new_moments"]["rebound"]["scale"],
                            defense_mean=s["defense_norm"]["mean"], defense_scale=s["defense_norm"]["scale"],
                            offense_mean=s["adjusted_norm"]["banks"]["offense"]["mean"],
                            offense_scale=s["adjusted_norm"]["banks"]["offense"]["scale"],
                            defense_bank_mean=s["adjusted_norm"]["banks"]["defense"]["mean"],
                            defense_bank_scale=s["adjusted_norm"]["banks"]["defense"]["scale"])
                for k, v in saved.items():
                    if not np.array_equal(v, norm[k]):
                        raise ValueError(f"normalizer {k} differs across seeds at {o.tag}/{phase}")
                saved = norm
                refs[f"{o.tag}/{phase}/s{seed}"] = json.loads(json.dumps(c["reference"], default=float))
                e = {k: v for k, v in s["environment"].items()}
                key = f"{o.tag}/{phase}"
                if key in env and env[key] != e:
                    raise ValueError(f"environment differs across seeds at {key}")
                env[key] = e
            np.savez(out / "normalizers" / f"{o.tag}_{phase}.npz", **saved)
    (out / "environment.json").write_text(json.dumps(env, indent=1, default=float))
    (out / "references.json").write_text(json.dumps(refs, indent=1, default=float))


def recomputed_contexts(out, schedule):
    """Normalizers and environment of every origin and phase from lineups.normalizers; empty references."""
    (out / "normalizers").mkdir(exist_ok=True)
    with np.load(states.GAME_LINEUPS) as z:
        grouped = {k: z[k] for k in z.files}
    with np.load(V3) as z:
        offense = {k: z[k] for k in ("game_id", "pid", "base", "x")}
    with np.load(REBOUND) as z:
        rebound = {k: z[k] for k in ("game_id", "pid", "prob", "neff")}
    with np.load(states.REBOUND_LABELS) as z:
        counts = z["counts"]
    full = legacy.schedule()
    (out / "references.json").write_text("{}")
    (out / "environment.json").write_text("{}")
    store, matchups, env = Store(out), legacy.matchups(), {}
    for o in schedule.itertuples():
        inner = full[full.stop <= o.start].iloc[-1]
        for phase, cutoff in (("inner", legacy.day(inner.start)), ("final", legacy.day(o.start))):
            norm = normalizers.lineup_normalizers(grouped, offense, rebound, cutoff)
            norm |= normalizers.matchup_normalizers(matchups, store, cutoff)
            np.savez(out / "normalizers" / f"{o.tag}_{phase}.npz", **norm)
            env[f"{o.tag}/{phase}"] = dict(normalizers.environment(grouped, counts, cutoff),
                                           cutoff=str(np.datetime64(cutoff, "D")))
        print(f"CONTEXT {o.tag}", flush=True)
    (out / "environment.json").write_text(json.dumps(env, indent=1, default=float))


def compare_store(new, old=None):
    """Differences between a store and the saved v16 store: exact for tables; normalizers to float32
    precision (rtol 2e-7: the recomputation differs from the saved values by one float32 unit in 4 of 96
    files); the environment's three constants to 1e-9. Returns the mismatches (empty when they agree)."""
    old = Path(old or paths.CACHE / "lineups_store_v16")
    bad = []
    for name in ("offense_games.npz", "offense_origins.npz", "defense_games.npz", "defense_origins.npz",
                 "library_offense.npz", "library_defense.npz"):
        with np.load(old / name) as a, np.load(new / name) as b:
            bad += [f"{name}:{k}" for k in a.files if k not in b.files or not np.array_equal(a[k], b[k])]
    for f in sorted((old / "normalizers").iterdir()):
        with np.load(f) as a, np.load(new / "normalizers" / f.name) as b:
            bad += [f"normalizers/{f.name}:{k}" for k in a.files if not np.allclose(a[k], b[k], rtol=2e-7, atol=1e-9)]
    ea, eb = (json.loads((d / "environment.json").read_text()) for d in (old, new))
    bad += [f"environment {k}:{c}" for k in ea for c in ("budget", "eta", "non_rebound") if abs(ea[k][c] - eb[k][c]) > 1e-9]
    return bad


def from_artifacts(out):
    """The store from the artifacts under paths.CACHE (module docstring)."""
    from experiments.joint_capability_v16_features import CapabilityLibrary
    torch.set_num_threads(1)
    out.mkdir(parents=True, exist_ok=False)
    tick = time.monotonic()
    offense_tables(out); defense_tables(out)
    print(f"STATES written {time.monotonic() - tick:.0f}s", flush=True)
    library_tables(out, CapabilityLibrary(paths.V16_LIBRARY))     # the compiler TrainingData wraps, without its v9 inputs
    print(f"LIBRARY written {time.monotonic() - tick:.0f}s", flush=True)
    recomputed_contexts(out, legacy.origins())
    manifest = dict(created=time.strftime("%Y-%m-%d"), source_tag="pre-refactor-2026-10-09 (library compiler)",
                    cache=str(paths.CACHE),
                    sources=[str(p) for p in (V3, REBOUND, DEFENSE, paths.V16_INPUTS, paths.V16_LIBRARY)],
                    contexts="normalizers and environment recomputed by lineups.normalizers; references empty")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print("EXPORT_COMPLETE", json.dumps(manifest), flush=True)


def verify(store, data, run, schedule):
    from experiments.joint_capability_v16_training_data import split
    from experiments.joint_capability_v13_run import read_pt
    worst = 0.
    rng = np.random.default_rng(1)
    history_fixture = None
    for tag in ("2016q1", "2020q1", "2026q4"):
        o = schedule[schedule.tag == tag].iloc[0]
        inner, itr, val, ftr, outer = split(data, o, schedule)
        for phase, rows, origin in (("final", np.sort(rng.choice(outer, 3000, replace=False)), int(o.origin_index)),
                                    ("final", np.sort(rng.choice(ftr, 3000, replace=False)), None),
                                    ("inner", np.sort(rng.choice(val, 2000, replace=False)), int(inner.origin_index))):
            shared = read_pt(run / "contexts" / tag / "s17" / phase / "context.pt")["shared"]
            old, *_ = data.batch(rows, shared, origin=origin)
            g = data.g
            mode = dict(game_ids=g["game_id"][rows]) if origin is None else dict(origin_index=origin)
            new = store.batch(g["pids"][rows], g["defense"][rows], g["date"][rows], store.normalizer(tag, phase), **mode)
            for k, v in old.items():
                if not torch.equal(v, new[k]):
                    diff = float((v.double() - new[k].double()).abs().max())
                    worst = max(worst, diff)
                    if diff > 1e-6:
                        raise AssertionError(f"{tag}/{phase}/{'origin' if origin is not None else 'history'} {k}: {diff}")
            print(f"VERIFY {tag} {phase} {'origin' if origin is not None else 'history'} rows={len(rows)} exact", flush=True)
            if tag == "2020q1" and origin is None:
                history_fixture = dict(rows=rows[:200], game_id=g["game_id"][rows[:200]], date=g["date"][rows[:200]],
                                       offense=g["pids"][rows[:200]], defense=g["defense"][rows[:200]],
                                       **{"input_" + k: v[:200].numpy() for k, v in old.items()})
    np.savez_compressed("tests/fixtures/history_2020q1_final.npz", **history_fixture)
    return worst


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from-artifacts", action="store_true", help="rebuild mode (module docstring)")
    p.add_argument("--out", type=Path, help="with --from-artifacts: the new store directory")
    p.add_argument("--compare", type=Path, help="compare this store with lineups_store_v16 and exit")
    a = p.parse_args()
    if a.compare:
        bad = compare_store(a.compare)
        print("store equals lineups_store_v16" if not bad else f"{len(bad)} differences: {bad[:20]}")
        return
    if a.from_artifacts:
        return from_artifacts(a.out)
    from experiments.v16_fast2_run import configuration
    from experiments.joint_capability_v16_training_data import TrainingData
    from experiments.joint_capability_v16_library import schedule_frame
    torch.set_num_threads(1)
    out = paths.STORE
    out.mkdir(parents=True, exist_ok=False)
    tick = time.monotonic()
    offense_tables(out); defense_tables(out)
    print(f"STATES written {time.monotonic() - tick:.0f}s", flush=True)
    config = configuration(paths.V16_RUN, check=False)
    data = TrainingData(config["training_inputs"], config["capabilities"])
    library_tables(out, data.library)
    schedule = schedule_frame().query("season >= 2015")
    context_tables(out, paths.V16_RUN, schedule)
    print(f"STORE written {time.monotonic() - tick:.0f}s", flush=True)
    worst = verify(Store(out), data, paths.V16_RUN, schedule_frame())
    manifest = dict(created="2026-10-09", source_tag="pre-refactor-2026-10-09",
                    sources=[str(p) for p in (V3, REBOUND, DEFENSE, config["capabilities"], paths.V16_RUN / "contexts")],
                    verification=f"batches identical to old TrainingData.batch on sampled outer/training/inner rows "
                                 f"of 2016q1, 2020q1, 2026q4 (max abs diff {worst})")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print("EXPORT_COMPLETE", json.dumps(manifest), flush=True)


if __name__ == "__main__":
    main()
