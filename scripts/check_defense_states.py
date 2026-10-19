"""Rung 5 step 4: the ported defensive sweep reproduces defense_states.npz exactly.

    PYTHONPATH=. python -u scripts/check_defense_states.py
"""
import numpy as np
import pandas as pd

from lineups import paths, states

V15 = paths.CACHE / "joint_capability_2026_09_17_v15_inputs"

if __name__ == "__main__":
    with np.load(V15 / "matchups.npz") as z:
        g = {k: z[k] for k in z.files}
    new = states.defense_sweep(g, pd.read_pickle(states.GAME_PLAYERS), pd.read_csv(paths.SCHEDULE, parse_dates=["start"]))
    bad = []
    with np.load(V15 / "defense_states.npz") as z:
        for k in z.files:
            same = np.array_equal(z[k], new[k]) and z[k].dtype == new[k].dtype
            print(f"{k:18s} {str(z[k].shape):14s} {z[k].dtype} {'identical' if same else 'DIFFERENT ' + str(new[k].dtype)}")
            if not same:
                bad.append(k)
    print("DEFENSE", "IDENTICAL" if not bad else f"DIFFERENT {bad}")
