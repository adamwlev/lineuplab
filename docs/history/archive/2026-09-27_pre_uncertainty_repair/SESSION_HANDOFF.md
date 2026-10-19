# Current handoff — optimized v16 analysis running without timeouts (2026-09-26)

## Current decision

Adam explicitly removed the hard runtime limit and authorized background launch.
**The optimized analysis is running**, with no overall or per-stage timeouts.
Supervisor PID **99000**, initial prediction-audit worker **99002**. Both the
progress and queue files confirm unlimited execution. Do not launch a duplicate.
Implement directly; no
delegation, NN refits, original-artifact edits, promotion, deployment or commit.

- Active destination: `experiments/cache/joint_capability_2026_09_26_v16_analysis24`.
- Corrected source: `experiments/cache/joint_capability_2026_09_26_v16_repaired`.
- Original trained source: `experiments/cache/joint_capability_2026_09_19_v16_fast2_ready`.
- Old exhaustive analysis PID96909 and supplement supervisor PID97047, plus
  caffeinate helpers, were stopped and verified absent. Do not restart them.
  Their last-written WAITING/RUNNING status files are stale.
- `progress.json` records the active stage; initial checkpoint: prediction audit.
  The supervisor continues automatically through the finite prescribed analyses,
  stopping on errors. No assistant automatic wakeup is promised.
- No commits made; pre-existing edits and all original feedback preserved.

## What is complete

All 3,168 native cases / 6,336 inner-final fit directories remain intact.
All 48 corrected scoring origins and full repair point validation completed.
Repaired point/event/profile/channel reports are reused through read-only links.
Five completed average-opponent origins are reused; 14 old exhaustive fixture
cases remain preserved in the stopped repair but are not mixed with sampled ones.

Calibration repair separates the forecast column from player ID p0; no NN
training changed. The old contaminated rankings must not be used. Independent
full prediction audit and remaining three-pillar analysis are still pending.

[Repair protocol](reports/joint_capability_v16_repair_protocol.md).
[Bounded numerical amendment](reports/joint_capability_v16_analysis24_protocol.md).
[Implementation and measured verification](reports/joint_capability_v16_analysis24_implementation.md).
[Execution-only no-timeout override](reports/joint_capability_v16_no_timeout.md).

## Verified implementation

- 23 tests pass (regression grouping/chronology, ensemble parity, grouped
  sensitivities, clones/unseen IDs, common-reference escalation, receipt resume,
  deadline cleanup and missing-receipt failure).
- Full 157,079-opponent Cleveland sensitivity: **9.29 seconds**, maximum
  difference from the saved exhaustive result **5.59e-8 PPP100**.
- Early/late 512-reference equivalence includes nonlinear spot checks;
  repeated/never-seen player feature lookups match exactly.
- Final late J_ALL_BOTH three-seed throughput: **92.04s serial / 35.56s parallel
  = 2.588x** including loading. Peak worker RSS **2.10 GB**; physical RAM
  **17,179,869,184 bytes (16 GiB)**. Three workers accepted.
- Serial and parallel primary/player/sensitivity/quadrature outputs match exactly.
- Original and repaired producer fingerprints verified unchanged.
- Durable preflight: ready directory `logs/preflight.log`,
  `preflight/equivalence.csv`, `preflight/acceptance.json`.
- Test log: `experiments/cache/v16_analysis24_verification_2026_09_26/logs/tests.log`.
- No-timeout launcher plus regression suite: **26 tests pass**; log
  `experiments/cache/v16_analysis24_verification_2026_09_26/logs/no_timeout_tests.log`.
  New orchestration is `experiments/v16_analysis_continue.py`; the original
  bounded producers/protocol and accepted preflight remain unchanged.
- Earlier `...analysis24_dev1` pilot is historical and no longer matches final
  source fingerprints; preserve it, do not run/resume it.

## Execution design and limits

All 22 arms, three seeds, 48 origins and registered predictive populations stay.
Player-regrouped input gradients preserve the linearized sensitivity calculation.
Common 4,096-reference quadrature plus three shifted point-only replicates;
whole-origin escalation to 16,384 at >.05 PPP100 point/swap discrepancy. Keep
unresolved flags. Sixteen predetermined exact-reference audits. All 32 fixtures
remain, with matched checkpoint-average point predictions for ensemble mixtures.

Fixture workers are split by origin AND seed; the heaviest origins start first.
Numerical selection waits for every arm and all seeds. Original 512/4096
average-opponent task is unchanged. U0/U1/U2 estimands and game/season
resampling remain; synthetic descriptors use the selected numerical reference.

Prediction audit gates nine frozen ensemble methods and reliability separately
from fixtures. Final completion requires all stages; partial origins are never
silently pooled as complete evidence. At Adam's request, the 24-hour target is
only a planning goal, **not a stopping rule or proven ETA**. The active launcher
has no stage cutoffs or wall alarm; it retains failure stops, owned-worker
cleanup and resumable receipts. `execution/manifest.json` fingerprints this
orchestration-only override. Human final interpretation remains necessary.

## Verified commands (from repository root)

Already launched through detached Python subprocess with caffeinate. Equivalent
command below is for reference only; **do not run while the supervisor is active**:

```bash
nohup /usr/bin/caffeinate -i /Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_analysis_continue --workers 3 >> experiments/cache/joint_capability_2026_09_26_v16_analysis24/logs/launcher.log 2>&1 < /dev/null &
```

Overall live log:

```bash
tail -F experiments/cache/joint_capability_2026_09_26_v16_analysis24/logs/run.log
```

Read-only stage/case progress (tested):

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_analysis24 status
```

Verbose worker outputs are under `queues/<stage>/logs/`. For example:

```bash
tail -F experiments/cache/joint_capability_2026_09_26_v16_analysis24/queues/fixtures_4096/logs/fixtures_2026q4_s17_n4096.log
```

Repaired point leaderboard remains available independently:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_repair report --sort r2 --slice all --view half
```

Do not edit fingerprinted producers/protocols. Root `HANDOFF.md` and
`inventory.json` will record completion/deferral; an output receipt is not a
claim of basketball truth or validated hypothetical-lineup latent uncertainty.

## History

[Checkpoint before the bounded amendment](docs/archive/2026-09-26_pre_analysis24/SESSION_HANDOFF.md)
preserves the stopped exhaustive pipeline, repair diagnostics and previous commands.
