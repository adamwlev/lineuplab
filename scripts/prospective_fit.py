"""Fit the frozen 2026-27 prospective arms at origin 2027q1.

Protocol: reports/prospective_2027q1_protocol_2026_10_09.md. Arms R (broadcast
defense, the reference architecture) and C (capacity v2), each trained two-phase
from scratch with self-references on the 2027q1 store: phase A trains the
offense alone, phase B starts from it (EventModel.from_offense), and each phase
is normalized by its own starting model. Inner selection validates on 2026q4;
the final refit uses every game before opening night (2026-10-20).

    PYTHONPATH=. python scripts/prospective_fit.py --cases \
        | xargs -P 3 -L 1 sh -c 'PYTHONPATH=. python -u scripts/prospective_fit.py --arm $0 --seed $1'

Output: experiments/cache/prospective_2027q1/<arm>_s<seed>.pt; a finished case is skipped.

--store DIR --out DIR (2026-10-15) fit the same protocol on another store into a new directory: the release
retrained on the clean data (lineups.page_possessions). The frozen record's fits are never touched.
"""
import argparse
import os
import time
from pathlib import Path

import torch

from lineups import legacy, paths
from lineups.features import Store
from lineups.model import EventModel
from lineups.train import Rows, fit_origin, self_references

STORE = paths.CACHE / "lineups_store_2027q1_library"   # library extended to opening night
OUT = paths.CACHE / "prospective_2027q1"
ORIGIN = "2027q1"
ARMS = dict(R="broadcast", C="capacity")
SEEDS = (17, 23, 41)


def path(arm, seed, out=None):
    return (out or OUT) / f"{arm}_s{seed}.pt"


def model(arm, seed, saved):
    """The frozen arm's final model and its checkpoint mixture, from a saved fit."""
    offense = EventModel.offense_only(seed)
    offense.load_state_dict(saved["offense_final"])
    final = EventModel.from_offense(offense, seed, ARMS[arm])
    final.load_state_dict(saved["final"])
    mixture = []
    for state in saved["checkpoints"]:
        m = EventModel.from_offense(offense, seed, ARMS[arm])
        m.load_state_dict(state)
        mixture.append(m.eval())
    return final.eval(), mixture


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--arm", choices=sorted(ARMS))
    p.add_argument("--seed", type=int, choices=SEEDS)
    p.add_argument("--cases", action="store_true", help="print the unfinished arm/seed cases")
    p.add_argument("--store", type=Path, default=STORE)
    p.add_argument("--out", type=Path, default=OUT)
    a = p.parse_args()
    if a.out.resolve() != OUT.resolve() and a.store.resolve() == STORE.resolve():
        p.error("a new --out needs its own --store")
    if a.cases:
        for arm in ARMS:
            for seed in SEEDS:
                if not path(arm, seed, a.out).exists():
                    print(arm, seed)
        return
    out = path(a.arm, a.seed, a.out)
    if out.exists():
        print("done", out)
        return
    torch.set_num_threads(1)
    a.out.mkdir(parents=True, exist_ok=True)
    store = Store(a.store)
    schedule = store.schedule()
    origin = schedule.query("tag == @ORIGIN").iloc[0]
    inner = schedule[schedule.stop <= origin.start].iloc[-1]
    data = Rows(legacy.matchups(), store)
    reference = self_references(data)
    tick = time.monotonic()
    log = lambda m: print(f"[{a.arm}/s{a.seed} {time.monotonic() - tick:6.0f}s] {m}", flush=True)
    log(f"phase A: offense only (inner validation {inner.tag})")
    offense = fit_origin(lambda phase: EventModel.offense_only(a.seed), data, store, origin, inner, a.seed, log=log,
                         reference=reference)

    def parent(phase):
        m = EventModel.offense_only(a.seed)
        m.load_state_dict(offense["inner_state" if phase == "inner" else "final_state"])
        return EventModel.from_offense(m, a.seed, ARMS[a.arm])

    log(f"phase B: full model, {ARMS[a.arm]} defense")
    full = fit_origin(parent, data, store, origin, inner, a.seed, log=log, reference=reference)
    tmp = out.with_suffix(".tmp")
    torch.save(dict(arm=a.arm, defense=ARMS[a.arm], seed=a.seed, origin=ORIGIN, store=str(a.store),
                    offense_inner=offense["inner_state"], offense_final=offense["final_state"],
                    offense_selected=offense["selected_epoch"], offense_references=offense["references"],
                    offense_curves=dict(inner=offense["inner_curve"], final=offense["final_curve"]),
                    final=full["final_state"], checkpoints=full["checkpoint_states"], selected=full["selected_epoch"],
                    references=full["references"], curves=dict(inner=full["inner_curve"], final=full["final_curve"]),
                    seconds=time.monotonic() - tick), tmp)
    os.replace(tmp, out)
    log(f"saved {out}")


if __name__ == "__main__":
    main()
