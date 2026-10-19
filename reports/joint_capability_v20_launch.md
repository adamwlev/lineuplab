# V20 approved launch — 2026-10-06

Adam explicitly requested: “yes please launch”, following sealed readiness.
Checkpoint3fd8bc28 contains the implementation, tests and prelaunch evidence.
The original plan, readiness report, producer fingerprints and artifacts were
not edited to grant authority. The runner's production manifest records the
explicit approved invocation and binds the existing readiness receipt.

Before launch: all frozen source/receipt hashes verified; readiness had zero
unresolved items;195.12GiBimmediately free versus102.97GiBrequired; production
manifest absent. No previous campaign was resumed or duplicated.

Launched in a detached session with caffeinate and append-safe logs:

```text
supervisor PID53523
root experiments/cache/joint_capability_2026_10_06_v20_prod
command bash experiments/run_joint_capability_v20.sh run --run-dir <root> --approve-full-run
```

At12:38PDT, the supervisor reported TRAINING and three active workers:
2015q1/P_ADJ/s17 PID53527, s23 PID53528, s41 PID53529. The s17inner fit had
completed its first74training batches with finite losses/gradients; no queue
failures. These are launch observations, not continuing liveness guarantees.
Eight reused pilots count as8/864completed case slots;856new cases were queued.
2015is warmup, excluded from the primary leaderboard. No outer result yet.

Remaining forecast:63.21hcentral/82.42hstressed including all analyses, with
substantial epoch/load uncertainty; no hard deadline. The supervisor runs the
19-stage analysis/audit graph automatically after chronological scoring. Final
three-pillar scientific review and interpretation are still required afterward;
there is no automatic scorer promotion or assistant wakeup.

## Monitor the existing run

```bash
tail -f experiments/cache/joint_capability_2026_10_06_v20_prod/logs/launcher.log
bash experiments/run_joint_capability_v20.sh status
bash experiments/run_joint_capability_v20.sh report --sort r2 --slice all --view checkpoint_average_half
```

Detailed epoch/batch logs:training_queue/logs/ within the production root.
Per-case preview and other views are documented in the unchanged
[readiness report](joint_capability_v20_launch_readiness.md).
Do not rerun launch while the supervisor is active. On failure inspect its exact
log and receipts; preserve original artifacts and frozen scientific choices.
