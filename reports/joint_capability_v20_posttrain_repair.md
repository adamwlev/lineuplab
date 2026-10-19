# V20 post-training path repair — 2026-10-08

## Outcome and scope

All864native cases and48scored origins completed before this failure. The
training/scoring queue took175,980.76seconds (48.88hours). Controls, events,
diagnostics, roles and observed-context stages completed. Stage6/19 average
opponent integration failed on the first three jobs, before inference/output.

Adam authorized repair and continuation. No neural refits, rescoring, changed
estimands, new samples, altered tolerances, artifact deletion or scorer promotion.
All original frozen producers, manifests and completed outputs remain unchanged.

## Cause

The production scoring manifest explicitly stores `compact: null`; a separate
compact source directory is an optional pilot-rehearsal feature. Both
`v20_average.py` and `v20_basketball.py` used
`c.get('compact', c['native'])` in the output/source disjointness check. Because
the key exists, this returns None instead of the default. `Path(None)` fails.
The rehearsal had a populated compact path, so it did not exercise this state.
The same expression appears in the optional pilot-only predict replay utility.

Versioned `_v2` copies use `c.get('compact') or c['native']`. Nothing else in
these consumers changes. AST regression checks the complete modules against
that one-expression replacement. Production still uses the original forecast
loader's existing compact/native handling; no source-selection logic changes.
The pilot replay remains pilot-only and is not part of the continuation graph.

## Recovery and verification

-70v20unit tests pass, including5new regression tests. They cover absent/null/
 populated compact paths, output-overlap rejection, preserved replay restriction,
 numerical-code identity and unchanged remaining graph arguments.
-Preflight validates original frozen code/receipt hashes, the training queue,
 reference and conditional scoring receipts for all48origins, and every completed
 first-five-stage output/queue receipt.
-Continuation reuses those first five stages without launching their consumers.
 Remaining14stages use fresh output roots. Only average/basketball module names
 change; fixed fixtures,512/4096opponent draws, exhaustive risk census, population,
 calibration and downstream independent audits are preserved.
-Three workers, one numerical thread each, mandatory retention wrapper,
 no-database guard,13GiBreserve, source/continuation writer locks, append-safe
 logs and completed-child receipts preserve bounded, resumable execution.
-Tests: `experiments/cache/v20_posttrain_repair_2026_10_08/logs/tests.log`.
 Preflight: same directory, `preflight.log`. Shell syntax and git whitespace pass.
-Initial live verification: all three2015q1/q2/q3workers passed startup.
 2015q1/P_BASE/s17 completed160,768integration pairs over two checkpoints;
 P_CONTEXT was progressing through its checkpoints. This verifies repaired
 production startup, not completion of all remaining analysis or all three pillars.

## Operations

Original failed run/status/logs are retained under
`experiments/cache/joint_capability_2026_10_06_v20_prod`.
Do not restart the original supervisor. New continuation:
`experiments/cache/joint_capability_2026_10_08_v20_posttrain1`.
Its manifest records every reused/new root, source receipt and successor code hash.
Outputs use this prefix plus `_average`, `_basketball`, `_risk`, etc.

Detached continuation PID65142, launched with explicit user authority. Shell
background attempts did not persist; neither was alive before the successful
new-session subprocess launch. No duplicate supervisors were left running.

```bash
bash experiments/run_v20_posttrain_continue.sh status
tail -f experiments/cache/joint_capability_2026_10_08_v20_posttrain1/logs/launcher.log
```

The original leaderboard command still reads unchanged scoring outputs:

```bash
bash experiments/run_joint_capability_v20.sh report --sort r2 --slice all --view checkpoint_average_half
```

If interrupted, diagnose first, then resume with
`bash experiments/run_v20_posttrain_continue.sh run` (detach for long execution).
`check` verifies prerequisites without starting numerical jobs. Receipt verification
prevents changing this continuation's implementation in place once launched.

Prelaunch post-training forecast18.84hcentral/29.73hstressed is a planning
estimate, not a newly measured ETA. Five quick stages are already completed.
Final stage status READY_FOR_SCIENTIFIC_REVIEW means arithmetic audits complete;
scientific interpretation, three-pillar conclusions and a documented review remain.
