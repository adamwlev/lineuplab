# Current handoff — v19 full pilots running (2026-09-30)

## Current checkpoint

Adam authorized direct implementation of the frozen v19 plan. Commit **b7401231**
records v18 evidence and the v19 plan. All subsequent v19 implementation remains
uncommitted; no new commit or full-production launch was authorized this turn.

Read [the implementation checkpoint](reports/joint_capability_v19_implementation.md)
and [the v19 plan](JOINT_CAPABILITY_V19_PLAN.md).

The native trainer, split scoring and resumability are implemented. **Seven
prescribed full pilots are running**, three CPU workers / one thread each.
This is not the720-case campaign. Full-launch readiness is still incomplete.
The supervisor will stop after seven cases; no production run starts automatically.

## Active process and exact monitoring commands

Pilot root: experiments/cache/joint_capability_2026_09_30_v19_pilot1.
Detached caffeinate supervisor launched with PID67369; live worker PIDs and
success/failure state are in queue/status.json. Verify current state, not a stale
PID. At last check CLOCK/FULL at2016q1 had completed successfully (2/7).
C_FIXED/C_ALLOC/C_MARGIN at2016q1 were active, with CLOCK/FULL at2026q4 pending.

From repository root:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v19_pilot status \
  --out experiments/cache/joint_capability_2026_09_30_v19_pilot1

tail -f experiments/cache/joint_capability_2026_09_30_v19_pilot1.log

tail -f experiments/cache/joint_capability_2026_09_30_v19_pilot1/queue/logs/2016q1_C_CLOCK_s17.log
```

Only if the pilot supervisor is no longer running and the queue needs resume:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v19_pilot run \
  --out experiments/cache/joint_capability_2026_09_30_v19_pilot1 \
  >> experiments/cache/joint_capability_2026_09_30_v19_pilot1.log 2>&1
```

The kernel lock rejects a second supervisor. Completed fits are immutable;
interrupted fits resume their Adam state and epoch journal.

## Verified progress

- Source audit:288/288 dated teachers,48origins,3seeds,599 provenance entries.
- Derived labels:3,056,123 context rows conserve1,592,743 matchup rows /
  6,059,380possessions and every original event/point label exactly.
-120float64 old/new value/loss/gradient comparisons pass at two fixed dates.
- Seven real-input optimizer cases pass exact uninterrupted/resumed three-epoch
  equality. Each used two complete training game batches and a separate prior
  validation batch.27.76s total; maximum ledger error2.20e-7 conditional /
  6.56e-8 reference. Engineering tests, not scientific fits.
-35combined tests pass, including existing persistence/coupling regression tests.
-2016q1 CLOCK and FULL each selected epoch14 after22inner epochs and completed
  fresh14-epoch final fits, both prediction views and checkpoint averages.
  Worker times560.55s/564.12s; artifacts67.68MB/68.24MB. C_FIXED selected36epochs
  and is in its final fit. Inner epochs about16s, final epochs about13s.
  Partial engineering timings, not the campaign estimate; no worker failures.
- Independent numpy/scipy audit of both completed cases passed: all four point
  scores, both reference event readouts and primary conditional state likelihoods.
  Max point identity discrepancy5.68e-14/event-rate4.44e-16. Checkpoint-average
  conditional event likelihood still requires state re-inference for this audit;
  its pooled point MSE was independently verified.
- No new calibrated leaderboard, coherence result or uncertainty claim yet.
  Retain J_POINT_BOTH and all three co-equal product standards.

## New code and outputs

Foundation modules remain as previously recorded. New this continuation:
v19_fit.py, v19_evaluate.py, v19_case.py, v19_micro.py, v19_pilot.py,
v19_point_context.py, v19_control_fit.py, v19_calibration.py,
v19_native_audit.py under experiments/.
New tests: test_v19_fit.py, test_v19_point_context.py, test_v19_calibration.py.

Completed source/label/replay prefixes under experiments/cache/:
joint_capability_2026_09_30_v19_sources2, _v19_labels1,
_v19_replay_smoke1, _v19_replay1, and now _v19_micro1
(all use the same joint_capability_2026_09_30 stem).
Each has a receipt and sibling.log. Full pilots: _v19_pilot1, in progress.
Independent completed-case snapshot audit: _v19_native_audit1 (same date/stem),
receipt and sibling.log. Only the first two completed cases are in that snapshot;
use a new prefix for the remaining cases after they finish.

Logs: v19_training_tests2.log (35 pass), v19_fit_tests1.log,
v19_training_tests1.log, v19_point_context_tests1.log,
v19_calibration_tests1.log, v19_control_sources1.log.
All earlier failed/source diagnostics remain preserved.

**Pilot manifest now binds the fitter/case/model/pilot and all transitive
producers. Do not edit them in place.** New downstream modules can be added
without changing that dependency set; corrections need new versions/prefixes.
Control/calibration modules were added after pilot preparation and are not yet
bound by completed real-data control exports.

## Precise next steps

1. Check pilot logs/status and completed case receipts. Audit native arithmetic,
   epoch selection, source identities, memory/storage and conditional/reference
   outputs. Don't select arms from these pilots.
2. Complete and test real-data point-control export with v19_control_fit.py on
   both pilot dates (CLI --help verified import/source probes only; full export
   not yet run). It reads the same frozen dated teachers/additive models and
   fits only residual tables, no upstream rebuild or NN optimization.
3. Wire v19_calibration.py into original-population reports/preview, with distinct
   histories for reference, conditional_clock and conditional_margin; finish
   fair controls and independently reproduce metrics. Low-level tests already
   cover future leakage, view collisions, blend identities and constant status.
4. Complete average-opponent/fixtures/U0/U1/role/persistence/summary/audit adapters.
   Measure a late-sized downstream bundle and fixed fixtures. No pilot-only
   calibration or conditional-information gain advertised as production gain.
5. Measure one/three-worker throughput, selected/cap projections,1.2x training
   stress, peak memory and disk with10GiB reserve. Physical free space was56GiB
   before pilots. Full conditional ledgers add storage; measure actual artifacts.
6. Only after readiness: provide verified full launch/log/status/report/preview
   commands and wait for Adam's explicit full-launch approval.

### Explicit source gap to disclose before full launch

No saved2014q4 additive snapshot/control exists. This affects **only2015q1's
inner additive warmup diagnostic**. v19_control_fit.py records
NOT_AVAILABLE_PRE_2015_INNER_ONLY and does not substitute the later final fit.
The frozen NN inner teacher exists.2015q1 final/outer additive and all primary
period sources remain required; no original scoring population is removed.
No NN stopping criterion depends on this diagnostic. Source probes verified
2015q1/2015q4/2016q1/2026q4; audit the complete control schedule before launch.

Residual tables use the NN five-year/730-day training weights, fixed500/250
possession shrinkage, and three-year/365-day reference centering. Margins are
centered within clock, missing clock is zero and missing margin inherits clock.
These are point-only nuisance controls, not event-ledger/causal explanations.
All this is documented in the implementation checkpoint; frozen plan unchanged.

## Preserved history and boundaries

Foundation checkpoint archived at
docs/archive/2026-09-30_pre_v19_pilots/, including handoff/state/roadmap/navigation/
implementation report. Earlier planning archive remains intact.
Numerous cache directories are untracked: never blanket-stage or delete them.
No scraping, database mutation, upstream cache/profile rebuild, known-pair terms,
forced fixture ranking, coverage gate, promotion or deployment.

