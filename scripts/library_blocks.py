"""Run one capability-library chain in parallel blocks (2026-10-15).

The legacy chain (joint_capability_v16_library.chain, tag pre-refactor-2026-10-09) fits every monthly
snapshot in order, each warm-started from the previous one, and tunes each season's penalty when the season
opens. It runs one process per bank and family, and the two location chains take 15-17 hours alone.

Every snapshot is a fit to the data before its cutoff, with that season's penalty. The tuning uses only
the data, and the last-seen history is recomputed at each cutoff. The warm start only moves the
optimizer's starting point, and every fit converges to the same tolerance (relative objective change
about 1e-11). So a chain can be cut into contiguous blocks at season boundaries, each starting cold, as
scripts/library_extend.py --era does. Each block's snapshots and penalties go to the chain's usual
directories. Afterwards the ordinary `chain` command finds them complete, checks their hashes and writes
the chain's receipt.

Run from the rebuild root (the legacy relative paths resolve there):

    cd ROOT && PYTHONPATH=REPO:LEGACY python -u REPO/scripts/library_blocks.py --out LIBRARY --bank B --family F \
        --block k/n
    ... --check CUTOFF --against OTHER_LIBRARY   # one cold snapshot vs a sequential library's saved one
"""
import argparse
import json
from pathlib import Path

import numpy as np

from experiments.joint_capability_repro import no_database
from experiments.joint_capability_v16_inputs import LeagueOffsets
from experiments.joint_capability_v16_library import (BANKS, FAMILIES, date_name, library_hashes, schedule_frame,
                                                      selection_event, sha256, snapshot, tune)
from experiments.joint_capability_v16_runtime import manifest
from experiments.joint_capability_v16_storage import load_arrays


def blocks(dates, schedule, n):
    """n contiguous blocks of cutoffs, balanced by count. A cut falls where the season's penalty changes, or
    anywhere before the first tuned season (the cold penalty has no tuning directory to share); never inside a
    tuned season, whose single tuning directory would then have two writers."""
    key = [None if (e := selection_event(schedule, c)) is None else e["season"] for c in dates]
    cuts = [i for i in range(1, len(dates)) if key[i] != key[i - 1] or key[i] is None]
    chosen = sorted({min(cuts, key=lambda c: abs(c - len(dates) * j / n)) for j in range(1, n)}) if cuts else []
    edges = [0, *chosen, len(dates)]
    return [dates[a:b] for a, b in zip(edges, edges[1:]) if b > a]


def run(directory, bank, family, k, n):
    meta = json.loads((directory / "manifest.json").read_text())
    if meta["codes"] != library_hashes():
        raise ValueError("capability producer changed; use a new prefix")
    out = directory / "chains" / bank / family
    manifest(out, dict(library=sha256(directory / "manifest.json"), bank=bank, family=family))
    g = load_arrays(directory / "mapped_matchups")
    offsets = LeagueOffsets(g, bank, family)
    schedule = schedule_frame()
    split = blocks(meta["dates"], schedule, n)
    if k > len(split):                         # fewer blocks than asked: too few places to cut
        print(f"BLOCK_DONE {bank}/{family} {k}/{n}: no block (only {len(split)})", flush=True)
        return
    mine = split[k - 1]
    previous, choices = None, {}
    for cutoff in mine:
        event = selection_event(schedule, cutoff)
        season = None if event is None else event["season"]
        if season not in choices:
            choices[season] = tune(g, offsets, bank, family, event, out / "penalties" / str(season))
        previous = snapshot(g, offsets, bank, family, cutoff, choices[season], out / "snapshots" / date_name(cutoff),
                            previous)
        print(f"BLOCK {bank}/{family} {k}/{n} {date_name(cutoff)}", flush=True)
    print(f"BLOCK_DONE {bank}/{family} {k}/{n}: {len(mine)} snapshots {date_name(mine[0])}..{date_name(mine[-1])}",
          flush=True)


def check(directory, bank, family, cutoff, against, into):
    """Fit one snapshot cold and compare with a sequential library's saved state at the same cutoff."""
    g = load_arrays(directory / "mapped_matchups")
    offsets = LeagueOffsets(g, bank, family)
    day = int(np.datetime64(cutoff, "D").astype(np.int64))
    saved_dir = against / "chains" / bank / family / "snapshots" / date_name(day)
    selection = json.loads((saved_dir / "manifest.json").read_text())["selection"]
    state = snapshot(g, offsets, bank, family, day, selection, into / bank / family / date_name(day), None)
    with np.load(saved_dir / "state.npz") as z:
        saved = {k: z[k] for k in z.files}
    for k in ("ids", "history_ids", "history_last_seen", "last_seen"):
        print(f"  {k}: {'equal' if np.array_equal(state[k], saved[k]) else 'DIFFERENT'}", flush=True)
    for k in ("intercept", "coefficients", "std", "support", "neff", "offset"):
        a, b = np.asarray(state[k], float), np.asarray(saved[k], float)
        print(f"  {k}: max |diff| {np.max(np.abs(a - b)):.2e} (scale {np.max(np.abs(b)):.2e})", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True, help="the library directory (prepared)")
    p.add_argument("--bank", choices=BANKS, required=True)
    p.add_argument("--family", choices=FAMILIES, required=True)
    p.add_argument("--block", default="1/1")
    p.add_argument("--check", help="a cutoff date: fit it cold and compare with --against")
    p.add_argument("--against", type=Path)
    p.add_argument("--into", type=Path, help="with --check: where the cold snapshot goes")
    a = p.parse_args()
    with no_database():
        if a.check:
            return check(a.out, a.bank, a.family, a.check, a.against, a.into)
        k, n = map(int, a.block.split("/"))
        run(a.out, a.bank, a.family, k, n)


if __name__ == "__main__":
    main()
