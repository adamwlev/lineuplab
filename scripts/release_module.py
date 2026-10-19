"""Fit the learned combination module on the release networks (Adam, 2026-10-14).

The confirmed design (lineups.learned): each seed's frozen release network
(arm R, experiments/cache/prospective_2027q1, read only and checked against
the freeze record) carries a held pairwise module trained on top for
lineups.learned.EPOCHS on the final training rows, with the fit's own final
loss references, as in scripts/nonlinearity_screen.py (fixed_fit). The
module's output ranges are measured on those rows. Then its level on the
previous quarter's real rows (2026q4, inputs as of the origin).

    PYTHONPATH=. python -u scripts/release_module.py --seed 17      (one process per seed)

Output: experiments/cache/release_module_2027q1/module_s<seed>.pt (module state, level, training record).
"""
import argparse
import os
import time

import numpy as np
import torch

from lineups import learned, legacy, release
from lineups.features import Store
from lineups.train import FitConfig, Rows, train


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, choices=release.SEEDS, required=True)
    a = p.parse_args()
    out = learned.path(a.seed, release.SOURCE["modules"])
    if out.exists():
        print("done", out)
        return
    torch.set_num_threads(1)
    release.SOURCE["modules"].mkdir(parents=True, exist_ok=True)
    tick = time.monotonic()
    log = lambda m: print(f"[module s{a.seed} {time.monotonic() - tick:6.0f}s] {m}", flush=True)

    record = __import__("json").loads(release.RECORD.read_text())
    fit = release.FITS / f"R_s{a.seed}.pt"         # the release's fits (release.FITS, RECORD, STORE)
    if release._sha256(fit) != record["fits"][f"R_s{a.seed}"]:
        raise ValueError(f"{fit.name} does not match the release record")
    saved = torch.load(fit, map_location="cpu", weights_only=False)
    import prospective_fit
    final, mixture = prospective_fit.model("R", a.seed, saved)

    store = Store(release.STORE)
    schedule = store.schedule()
    origin = schedule.query("tag == @release.ORIGIN").iloc[0]
    previous = schedule[schedule.stop <= origin.start].iloc[-1]
    g = legacy.matchups(release.MATCHUPS)
    data = Rows(g, store)
    normalizer, env = store.normalizer(release.ORIGIN, "final"), store.env(release.ORIGIN, "final")
    rows = data.prefix(int(np.datetime64(origin.start, "D").astype(np.int64)), FitConfig().lookback_days)

    final.train()
    for q in final.parameters():
        q.requires_grad_(False)
    frozen = {k: v.clone() for k, v in final.state_dict().items()}
    final.pairs = learned.new_module(a.seed)
    log(f"train {learned.EPOCHS} epochs on {len(rows):,} rows before {origin.start}")
    train(final, data, rows, normalizer, env, saved["references"]["final"], a.seed, FitConfig(),
          epochs=learned.EPOCHS, log=log)
    state = final.state_dict()
    moved = [k for k in frozen if not torch.equal(frozen[k], state[k])]
    if moved:
        raise ValueError(f"frozen network weights moved: {moved[:5]}")
    module = final.pairs
    final.pairs = None
    learned.measure_holds([module], data, rows, normalizer, log)
    module.eval()

    before = np.sort(legacy.quarter_rows(previous, g))
    lv = learned.level(mixture, module, data, before, normalizer, env, int(origin.origin_index), g["possessions"])
    log(f"level on {previous.tag} ({len(before):,} rows): " + ", ".join(f"{k} {v:+.4f}" for k, v in lv.items()))
    tmp = out.with_suffix(".tmp")
    torch.save(dict(seed=a.seed, origin=release.ORIGIN, network=fit.name, network_sha256=record["fits"][f"R_s{a.seed}"],
                    epochs=learned.EPOCHS, training_rows=len(rows), level_quarter=previous.tag, level_rows=len(before),
                    level=lv, module=module.state_dict(), seconds=time.monotonic() - tick), tmp)
    os.replace(tmp, out)
    log(f"saved {out}")


if __name__ == "__main__":
    main()
