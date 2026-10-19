"""Rung 5 step 3: the ported rebound sweep reproduces rebound_states.npz exactly.

    PYTHONPATH=. python -u scripts/check_rebound_states.py
"""
import numpy as np
import pandas as pd

from lineups import paths, states

if __name__ == "__main__":
    with np.load(states.V3 / "player_game_states_v3.npz") as z:
        offense = {k: z[k] for k in z.files}
    with np.load(states.REBOUND_LABELS) as z:
        labels = {k: z[k] for k in z.files}
    new = states.rebound_sweep(labels, offense, pd.read_csv(paths.SCHEDULE, parse_dates=["start", "stop"]))
    saved = paths.CACHE / "joint_capability_2026_09_15_v14_states" / "rebound_states.npz"
    bad = []
    with np.load(saved) as z:
        for k in z.files:
            same = np.array_equal(z[k], new[k]) and z[k].dtype == new[k].dtype
            print(f"{k:22s} {str(z[k].shape):12s} {z[k].dtype} {'identical' if same else 'DIFFERENT ' + str(new[k].dtype)}")
            if not same:
                bad.append(k)
    print("REBOUND", "IDENTICAL" if not bad else f"DIFFERENT {bad}")
