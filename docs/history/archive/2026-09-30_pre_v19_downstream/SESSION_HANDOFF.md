# Current handoff — restart cleanup complete; v19 readiness hold (2026-09-30)

## Authority and current state

Adam most recently said “Ok let’s commit and launch.” Commit authority is now
granted; approval for the full frozen v19 campaign remains recorded once ready.
**It has NOT started.** The readiness review confirms there is still no full
production launcher and reporting/downstream/runtime integration is unfinished.
Do not ask for the same launch approval again unless changing scope.
Direct implementation only; no delegation.

All seven full pilots completed successfully in30m18s. No failures, cap hits or
active processes. New full-pilot saved-output audit and both-date context-control
exports/audits pass. The remaining obstacles are measured all-in storage/runtime
readiness and unfinished scoring/downstream integration—not permission or failed
NN training.

Read [implementation checkpoint](reports/joint_capability_v19_implementation.md)
and [frozen plan](JOINT_CAPABILITY_V19_PLAN.md). Commit b7401231 preserves v18
and the plan. This checkpoint commits the subsequent v19 implementation/tests,
documentation and restart-retention tools plus the sealed retirement ledger.
It is an implementation checkpoint, not a production-ready release.

## Completed restart cleanup — required verification mode

Adam authorized deleting obsolete completed-fit optimizer restart artifacts,
after fixing verification. Maintenance is complete: **19,420 resume_0/1.pt
payloads removed from9,792 completed v16–v18 fits**,12.8308GiB allocated bytes.
Physical free space increased12.7902GiB, from54.2330to67.0232GiB during apply.
No weights, averaging checkpoints, predictions, curves, journals, receipts or
frozen producer source files changed. No v19 files were retired. Deleted optimizer
states are not recoverable from the metadata ledger; no backup was made.

Read [retention operations](docs/ARTIFACT_RETENTION.md) and the
[maintenance report](reports/completed_resume_retention_2026_09_30.md).
Ledger: experiments/cache/completed_resume_retention_2026_09_30.
Plan SHA256:825e76b9b847ab3b3ea046b5b302cac772d093a4c6f32be6e3319be7af826cd2.

**Legacy strict verification still rejects the intentionally absent restarts.**
Use `python -u -m experiments.artifact_retention exec --ledger <ledger> <module>
<args>` for consumers of retired fits. The wrapper changes verification in memory
before importing consumers; it does not change frozen source hashes. Every new
v19 worker must use `artifact_retention.python_job(ledger,module,*args)`; wrapping
only its parent does NOT propagate Python replacements. Bind wrapper code and
ledger hashes into the new launcher and test child-process verification.

21 focused tests pass. Original v16 preview output matches exactly before/after.
Compatibility audit passes288v19teacher fits,7untouched pilot cases and129frozen
code hashes plus existing input receipts. Full retained-artifact audit passed
9,792fits/4,896cases and is logged
at the ledger prefix plus `_audit.log`; apply and compatibility logs use
`_apply.log` and `_compatibility.log`. No model/experiment results changed.

## Storage/runtime readiness — still required before full launch

Verified completed-pilot compressed sizes, actual48-origin row counts and reuse
of seven pilots project **47.257GiB additional native artifacts for713cases**.
The prior measurement55.072GiBfree failed the10GiBreserve before downstream
outputs (2.185GiB shortfall). After authorized cleanup, free67.0232GiB leaves
about9.77GiB after the native estimate and reserve. Downstream analyses, controls,
logs and temporary peaks are still NOT included.20% native-storage sensitivity
56.709GiB is not a bound; comparable v18 analysis directories occupy roughly9GiB.

The original resource report's HOLD_STORAGE is historical and unchanged. Fresh
all-in acceptance remains pending; do not infer READY from cleanup alone. No
further deletion is authorized by this maintenance. Largest measured individual
worker peak RSS4.016GiB; not a simultaneous physical-RAM measurement.

Resource report:
experiments/cache/joint_capability_2026_09_30_v19_resources1/
(summary, per-pilot sizes, exact partitions,713projected cases, COMPLETE receipt,
sibling.log). No full launcher exists yet; authorization does not make it ready.

## Completed verification and outputs

Prefixes below use experiments/cache/joint_capability_2026_09_30:

- _v19_sources2:288teachers,48origins,3seeds,599source/receipt checks.
- _v19_labels1:3,056,123context rows exactly conserve1,592,743matchups /
  6,059,380possessions and all original event/point ledgers.
- _v19_replay1:120float64 value/loss/gradient comparisons pass.
- _v19_micro1:7real optimizer/resume tests pass in27.76s, exact weights.
- _v19_pilot1: all7full cases COMPLETE;1818.10s queue wall time.
 2016q1 C_FIXED selected36epochs/44inner; CLOCK/FULL/ALLOC/MARGIN14/22;
 2026q4 CLOCK/FULL13/21. No cap hits. All required native views saved.
- _v19_native_audit2: all7cases independently checked with numpy/scipy.
  All four game/off5 point scores, both reference event readouts and primary
  conditional state likelihoods pass. Point identity discrepancy<=8.53e-14;
  event-rate<=4.44e-16. Checkpoint-average conditional EVENT audit still needs
  state re-inference; its pooled point score was independently verified.
- _v19_controls_pilot1/{2016q1,2026q4}/s17/: new inner/final point-only context
  controls, no NN refits. Both dates complete. Separate durable logs:
  _v19_controls_2016q1.log and _v19_controls_2026q4.log.
- _v19_control_audit2: both-date cutoff/gauge/baseline replay passes.
  Reference centering error<=8.10e-16; additive archive replay<=2.85e-14.

37tests pass in experiments/cache/v19_preflight_tests1.log.
Current native fit artifacts must remain unchanged. Their manifest binds
fitter/case/model/pilot/transitive producers. Do not modify those files in place.
New downstream modules can be added independently.

### Tiny teacher archive replay discrepancy, explained

The first control audit used1e-8 absolute archival tolerance and failed on
6/15,832early rows. Max difference4.84e-8points/100 early /6.62e-8late.
Read-only probe shows CURRENT canonical, optimized, memoized and exported
teacher predictions agree exactly; even canonical inference differs slightly
from the old archive. No root numerical/runtime cause beyond that localization
was established; do not claim a model change or a precisely identified library bug.

A documented archival replay guard now uses one float32 score-scale epsilon.
Observed discrepancies are<0.00470of that guard. This does NOT alter the
unchanged1e-8 float64 value/objective/gradient replay requirement.
Original forecasts/checkpoints untouched; failed control_audit1 and probe1 logs
preserved. Passing probe: experiments/cache/v19_control_replay_probe2.log.
The audit checks replay/gauges/cutoffs, not an independently refitted nuisance
estimator or calibrated accuracy.

## Exact next steps

1. Recheck physical space and measured all-in estimates after restart cleanup.
   Launch approval is recorded; no full launch occurred during this maintenance.
2. Finish view-qualified original-population reports and case preview using
   v19_calibration.py. Connect completed point-control exports and fair reference/
   conditional_clock/conditional_margin panels. Independently verify arithmetic.
3. Complete average-opponent512 integration plus fixed4096 convergence,
   fixtures/response curves, U0/U1, role/persistence/covariance, summary and audits.
4. Measure a late-sized downstream bundle plus fixed fixtures and one/three CPU
   worker throughput. Establish selected/cap projection,1.2x training stress,
   all-in54h target and total disk with10GiBreserve. The original native-only
   storage check failed before cleanup; new all-in acceptance is still pending.
5. Prepare a frozen full runner with explicit retention-aware child commands,
   reuse seven verified pilots without copying or
   modifying them, verify launch/log/status/report/preview commands, then launch
   under Adam's current authorization if all requirements pass. Otherwise return
   any material scope/runtime/resource decision before launch.

No calibrated v19 scorecard or new coherence/uncertainty claim yet.
J_POINT_BOTH remains reference; pilots are not an arm-selection tournament.

## Known warmup control-source gap

Saved additive controls start2015q1. The2015q1 inner additive diagnostic needs
2014q4 and is explicitly NOT_AVAILABLE_PRE_2015_INNER_ONLY, not replaced by a
future fit. NN inner teacher exists;2015q1 final and all primary-period controls
remain required. No point-population drop or NN stopping change. Audit all other
source dates before full launch and disclose this limitation.

## Files, preserved history and boundaries

The preceding launch check added: v19_resource_review.py, v19_control_audit.py,
v19_control_replay_probe.py and tests/test_v19_preflight.py.
Existing control producer and completed pilot/model code unchanged.
Prior handoff/state/roadmap/navigation/report snapshot preserved in
docs/archive/2026-09-30_pre_v19_launch_check/.

New maintenance files: experiments/artifact_retention.py,
experiments/retention_compatibility_audit.py, tests/test_artifact_retention.py,
docs/ARTIFACT_RETENTION.md and reports/completed_resume_retention_2026_09_30.md.
Earlier v19 implementation is included in this checkpoint, unchanged by maintenance.
Precommit rerun:26v19tests plus21retention/runtime tests pass. Durable logs:
experiments/cache/v19_commit_tests_2026_09_30.log and
experiments/cache/retention_commit_tests_2026_09_30.log. The retirement plan,
authorization and result JSON are explicitly versioned; large run artifacts
and untracked historical caches are not blanket-staged.

No active model jobs, full run, scraping, database mutation, upstream
cache/profile rebuild, scorer promotion or deployment. The only deletions were
the explicitly authorized completed restart payloads above. Many cache directories
are untracked: never blanket-stage. Preserve the three co-equal standards,
original artifacts and all failed logs.

