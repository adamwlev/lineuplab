"""Extract a golden J_POINT_BOTH batch from the pre-refactor pipeline.

One-time generator: it imports the old ``experiments`` code, so it only runs at
or before tag ``pre-refactor-2026-10-09``-era code. Its output
(tests/fixtures/reference_<origin>_s<seed>.npz plus .pt) lets the new package
be tested without that code: inputs, environment, saved weights (final and
averaged checkpoints), old-model outputs and the saved production predictions.

    python -u scripts/make_parity_fixture.py --origin 2020q1 --seed 17 --rows 256

It imports the retired ``experiments`` package. To rerun it, create the
legacy worktree and put it on the path after this repository:

    bash scripts/legacy_worktree.sh
    PYTHONPATH=.:../basketball-legacy python -u scripts/make_parity_fixture.py
"""
import argparse
from pathlib import Path

import numpy as np
import torch

RUN = Path("experiments/cache/joint_capability_2026_09_19_v16_fast2_ready")
KEYS = ("points100", "player_points", "fga", "fta", "turnover", "ft_make", "expected_attempts",
        "expected_makes", "usage_budget", "orb", "player_orb", "live", "initial_usage", "renewed_usage",
        "rebound_log_prob")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--origin", default="2020q1")
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--rows", type=int, default=256)
    p.add_argument("--out", type=Path, default=Path("tests/fixtures"))
    a = p.parse_args()
    from experiments.v16_fast2_run import configuration
    from experiments.joint_capability_v16_training_data import TrainingData, split
    from experiments.joint_capability_v16_library import schedule_frame
    from experiments.joint_capability_v13_run import read_pt
    from experiments.joint_capability_v15_fit import parent_fit
    from experiments.joint_capability_v16_model import Model16
    from experiments.joint_capability_v16_loss import average_ledgers

    torch.set_num_threads(1)
    config = configuration(RUN, check=False)
    data = TrainingData(config["training_inputs"], config["capabilities"])
    schedule = schedule_frame()
    o = schedule[schedule.tag == a.origin].iloc[0]
    *_, outer = split(data, o, schedule)
    case = RUN / "origins" / a.origin / "J_POINT_BOTH" / f"s{a.seed}"
    shared = read_pt(RUN / "contexts" / a.origin / f"s{a.seed}" / "final" / "context.pt")["shared"]
    parent, _ = parent_fit(a.origin, a.seed, "final", o.start)
    fit = read_pt(case / "final" / "fit.pt")
    states = [read_pt(case / "final" / f"checkpoint_{e:03d}.pt")["state_dict"] for e in fit["checkpoint_epochs"]]

    # Whole games, so a sample keeps the game/off5 pooling of point rows intact.
    rng = np.random.default_rng(20261009)
    games = np.unique(data.game[outer])
    chosen = []
    for g in rng.permutation(games):
        chosen.extend(outer[data.game[outer] == g])
        if len(chosen) >= a.rows:
            break
    rows = np.sort(np.asarray(chosen, np.int64))
    inputs, labels, phases, weight, parent_key = data.batch(rows, shared, origin=int(o.origin_index))

    old = Model16("J_POINT_BOTH", a.seed, parent).eval()
    out = {}
    with torch.no_grad():
        old.load_state_dict(fit["state_dict"])
        final = old(inputs, shared["environment"])
        mixture = []
        for s in states:
            old.load_state_dict(s)
            mixture.append(old(inputs, shared["environment"]))
        averaged = average_ledgers(mixture)
    for k in KEYS:
        out["old_" + k] = getattr(final, k).numpy()
        out["old_avg_" + k] = getattr(averaged, k).numpy()
    for name in ("primary", "checkpoint_average"):
        with np.load(case / f"{name}.npz") as z:
            pos = np.searchsorted(z["row"], rows)
            assert np.array_equal(z["row"][pos], rows)
            for k in KEYS:
                out[f"saved_{name}_{k}"] = z[k][pos]
    env = shared["environment"]
    np.savez_compressed(
        a.out / f"reference_{a.origin}_s{a.seed}.npz", row=rows,
        **{"input_" + k: v.numpy() for k, v in inputs.items()},
        **{"label_" + k: v.numpy() for k, v in labels.items()},
        weight=weight.numpy(), parent=parent_key.numpy(), game=data.game[rows], date=data.date[rows],
        offense=data.g["pids"][rows], defense=data.g["defense"][rows],
        env_budget=np.float64(env["budget"]), env_eta=np.float64(env["eta"]),
        env_non_rebound=np.float64(env["non_rebound"]), **out)
    torch.save(dict(final=fit["state_dict"], checkpoints=states, checkpoint_epochs=fit["checkpoint_epochs"],
                    selected_epoch=fit["selected_epoch"], origin=a.origin, seed=a.seed,
                    source=str(case)), a.out / f"reference_{a.origin}_s{a.seed}.pt")
    print(f"wrote {len(rows)} rows from {len(np.unique(data.game[rows]))} games; environment {env}")


if __name__ == "__main__":
    main()
