"""Backtest fits from scratch: the era backtest, and the 2015-2026 history on the clean data.

One fit per origin, arm (R broadcast, C capacity v2) and seed. Each is two-phase
from scratch with self-references, exactly as the 2027q1 prospective arms:
- phase A trains the offense alone;
- phase B starts the full model from it.
Forecasts for the origin's quarter are saved in the direct and
checkpoint-average views.

Campaigns (--campaign):
- era (protocol: reports/era_backtest_protocol_2026_10_12.md): origins 2006q1-2013q4 on
  lineups_store_era; training rows start at the store's first library snapshot (2001-12-01).
- history (Adam, 2026-10-16: "refresh all the components that produce numbers for the tool"): origins
  2015q1-2026q4 on lineups_store_v16 with the reference's five-year lookback, run with LINEUPS_CACHE at the
  clean root (paths.CLEAN). It replaces the saved v16 reference (warm-started from v14 parents on the old
  data) and the capacity confirmatory run as the release's history: calibration, band, benchmark.

    PYTHONPATH=. python scripts/era_run.py --cases | xargs -P 9 -L 1 sh -c \
        'PYTHONPATH=. python -u scripts/era_run.py --origin $0 --arm $1 --seed $2'

Cases are listed seed by seed (17 first). A case with complete.json is skipped.
Output: <cache>/era_backtest_2026_10_12/ or <cache>/history_2026_10_16/, then origins/<tag>/<arm>/s<seed>/.
"""
import argparse
import json
import subprocess
import time

import numpy as np
import torch

from lineups import legacy, paths
from lineups.features import Store
from lineups.model import EventModel
from lineups.train import Rows, fit_origin, self_references

CAMPAIGNS = dict(era=dict(store=paths.CACHE / "lineups_store_era", out=paths.CACHE / "era_backtest_2026_10_12",
                          seasons=(2006, 2013)),
                 history=dict(store=paths.CACHE / "lineups_store_v16", out=paths.CACHE / "history_2026_10_16",
                              seasons=(2015, 2026)))
STORE, OUT = CAMPAIGNS["era"]["store"], CAMPAIGNS["era"]["out"]
ARMS = dict(R="broadcast", C="capacity")
SEEDS = (17, 23, 41)
FIRST_DAY = legacy.day("2001-12-01")


class EraRows(Rows):
    """Training prefixes never reach before the first library snapshot."""

    def prefix(self, cutoff_day, lookback_days):
        return np.flatnonzero((self.date < cutoff_day) & (self.date >= max(cutoff_day - lookback_days, FIRST_DAY)))


def origins(store=None, campaign="era"):
    c = CAMPAIGNS[campaign]
    s = (store or Store(c["store"])).schedule()
    return s[(s.season >= c["seasons"][0]) & (s.season <= c["seasons"][1])]


def case_dir(tag, arm, seed, campaign="era"):
    return CAMPAIGNS[campaign]["out"] / "origins" / tag / arm / f"s{seed}"


def run(tag, arm, seed, campaign="era"):
    case = case_dir(tag, arm, seed, campaign)
    if (case / "complete.json").exists():
        print(f"{tag}/{arm}/s{seed} already complete", flush=True)
        return
    torch.set_num_threads(1)
    case.mkdir(parents=True, exist_ok=True)
    store = Store(CAMPAIGNS[campaign]["store"])
    schedule = store.schedule()
    origin = schedule[schedule.tag == tag].iloc[0]
    inner = schedule[schedule.stop <= origin.start].iloc[-1]
    data = (EraRows if campaign == "era" else Rows)(legacy.matchups(), store)
    reference = self_references(data)
    tick = time.monotonic()
    log = lambda m: print(f"[{tag}/{arm}/s{seed} {time.monotonic() - tick:6.0f}s] {m}", flush=True)
    offense = fit_origin(lambda phase: EventModel.offense_only(seed), data, store, origin, inner, seed, log=log,
                         reference=reference)

    def parent(phase):
        m = EventModel.offense_only(seed)
        m.load_state_dict(offense["inner_state" if phase == "inner" else "final_state"])
        return EventModel.from_offense(m, seed, ARMS[arm])

    full = fit_origin(parent, data, store, origin, inner, seed, log=log, reference=reference)
    np.savez(case / "forecast.npz", row=full["rows"], direct=full["direct"], checkpoint_average=full["checkpoint_average"])
    torch.save(dict(offense_final=offense["final_state"], final=full["final_state"], checkpoints=full["checkpoint_states"],
                    offense_references=offense["references"], references=full["references"]),     # (2026-10-16) for
               case / "fit.pt")                                                                  # modules on top
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=paths.ROOT).stdout.strip()
    (case / "complete.json").write_text(json.dumps(dict(
        origin=tag, arm=arm, seed=seed, campaign=campaign, store=str(store.directory),
        offense_epoch=offense["selected_epoch"], selected_epoch=full["selected_epoch"],
        inner_curve=full["inner_curve"], final_curve=full["final_curve"], seconds=time.monotonic() - tick,
        commit=commit), indent=1))
    log(f"done offense_epoch={offense['selected_epoch']} selected_epoch={full['selected_epoch']}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--origin")
    p.add_argument("--arm", choices=sorted(ARMS))
    p.add_argument("--seed", type=int)
    p.add_argument("--cases", action="store_true")
    p.add_argument("--campaign", choices=sorted(CAMPAIGNS), default="era")
    a = p.parse_args()
    if a.cases:
        tags = origins(campaign=a.campaign).tag.tolist()
        print("\n".join(f"{t} {arm} {s}" for s in SEEDS for t in tags for arm in ARMS
                        if not (case_dir(t, arm, s, a.campaign) / "complete.json").exists()))
    else:
        run(a.origin, a.arm, a.seed, a.campaign)
