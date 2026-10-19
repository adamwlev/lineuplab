"""Compare two rebuilds of the legacy data chain, artifact by artifact (2026-10-14).

    PYTHONPATH=. python -u scripts/compare_rebuilds.py ROOT_A ROOT_B [--stages text v3 v14 v15 v16]

ROOT_A and ROOT_B are roots written by scripts/rebuild_legacy_chain.sh (or the original cache, given as
experiments/cache/..: pass "original"). For every numeric array of every artifact, it prints whether the two
are equal and, if not, how many rows differ and the totals. Exact equality is the parity check (fix off
against the original); for a fix, the differing rows are what the fix changed.
"""
import argparse
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

from lineups import paths

STAGES = {
    "text": ["shot_events2_ba7aeb377198.pkl", "possession_channels_ba7aeb377198_5.npz"],
    "v3": ["joint_capability_2026_09_09_v3/derived/game_lineups.npz",
           "joint_capability_2026_09_09_v3/derived/player_game_states_v3.npz"],
    "v14": ["joint_capability_2026_09_15_v14_labels/rebound_labels.npz",
            "joint_capability_2026_09_15_v14_states/rebound_states.npz"],
    "v15": ["joint_capability_2026_09_17_v15_inputs/matchups.npz",
            "joint_capability_2026_09_17_v15_inputs/defense_states.npz"],
    "v16": ["joint_capability_2026_09_18_v16_phase_dev2/phase_labels.npz",
            "joint_capability_2026_09_18_v16_training_inputs_dev2/matchups"],
}


def cache(root):
    return paths.CACHE if root == "original" else Path(root) / "experiments" / "cache"


def arrays(path):
    """{name: array} of an npz, a pickled DataFrame (numeric columns) or a directory of .npy files."""
    if path.is_dir():
        return {f.stem: np.load(f, mmap_mode="r") for f in sorted(path.glob("*.npy"))}
    if path.suffix == ".npz":
        z = np.load(path, allow_pickle=False)
        return {k: z[k] for k in z.files}
    frame = pd.read_pickle(path)
    return {c: frame[c].to_numpy() for c in frame.columns if frame[c].dtype.kind in "biuf"}


def compare(a, b):
    out = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            out.append(f"  {k:<26} only in {'B' if k not in a else 'A'}")
            continue
        x, y = np.asarray(a[k]), np.asarray(b[k])
        if x.shape != y.shape:
            out.append(f"  {k:<26} shape {x.shape} vs {y.shape}")
            continue
        if x.dtype.kind not in "biuf":
            out.append(f"  {k:<26} {'equal' if np.array_equal(x, y) else 'differs'} (non-numeric)")
            continue
        same = (x == y) | (np.isnan(x) & np.isnan(y)) if x.dtype.kind == "f" else (x == y)
        rows = ~same.reshape(len(x), -1).all(1) if x.ndim > 1 else ~same
        if not rows.any():
            out.append(f"  {k:<26} equal")
        else:
            out.append(f"  {k:<26} {int(rows.sum()):>9,} of {len(x):,} rows differ; "
                       f"total {np.nansum(x.astype(float)):,.1f} -> {np.nansum(y.astype(float)):,.1f}")
    return out


EXTRACT = "joint_capability_2026_09_15_v14_extract"


def extract(a, b):
    """v14 extract (the raw texts and names, json lines): counts of differing records."""
    ra, rb = a / EXTRACT / "raw.jsonl.gz", b / EXTRACT / "raw.jsonl.gz"
    if not (ra.exists() and rb.exists()):
        return ["  v14 extract: missing"]
    n = diff = 0
    with gzip.open(ra, "rt") as fa, gzip.open(rb, "rt") as fb:
        for la, lb in zip(fa, fb):
            n += 1
            diff += la != lb
    pa = json.loads((a / EXTRACT / "players.json").read_text())
    pb = json.loads((b / EXTRACT / "players.json").read_text())
    names = sum(pa.get(k) != pb.get(k) for k in set(pa) | set(pb))
    return [f"  raw.jsonl.gz: {diff:,} of {n:,} records differ; players.json: {names} names differ"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("a")
    p.add_argument("b")
    p.add_argument("--stages", nargs="+", default=list(STAGES))
    x = p.parse_args()
    ca, cb = cache(x.a), cache(x.b)
    for stage in x.stages:
        print(f"== {stage}")
        if stage == "text":
            print(" v14 extract")
            print("\n".join(extract(ca, cb)), flush=True)
        for f in STAGES[stage]:
            pa, pb = ca / f, cb / f
            if not (pa.exists() and pb.exists()):
                print(f" {f}: missing in {'A' if not pa.exists() else 'B'}")
                continue
            print(f" {f}")
            print("\n".join(compare(arrays(pa), arrays(pb))), flush=True)


if __name__ == "__main__":
    main()
