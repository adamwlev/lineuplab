"""Rung 5 step 2: the ported state sweep reproduces player_game_states_v3.npz exactly.

    PYTHONPATH=. python -u scripts/check_states.py
"""
import time

import numpy as np
import pandas as pd

from lineups import paths, states

if __name__ == "__main__":
    tick = time.monotonic()
    g, gp = states.load_inputs()
    schedule = pd.read_csv(paths.SCHEDULE, parse_dates=["start", "stop"])
    new = states.sweep(g, gp, schedule, log=lambda m: print(f"[{time.monotonic() - tick:5.0f}s] {m}", flush=True))
    with np.load(states.V3 / "player_game_states_v3.npz") as z:
        bad = []
        for k in z.files:
            if k == "origin_tags":
                continue
            same = np.array_equal(z[k], new[k]) and z[k].dtype == new[k].dtype
            print(f"{k:22s} {str(z[k].shape):14s} {'identical' if same else 'DIFFERENT'}", flush=True)
            if not same:
                bad.append(k)
    print("STATES", "IDENTICAL" if not bad else f"DIFFERENT {bad}", f"{time.monotonic() - tick:.0f}s")
