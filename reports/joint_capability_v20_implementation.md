# V20 implementation checkpoint — updated 2026-10-06

Adam approved implementation of [the detailed plan](../docs/history/JOINT_CAPABILITY_V20_PLAN.md)
while freeing storage, then authorized all prescribed prelaunch steps. Direct
implementation; no delegated work. The full historical profile build, deep audit
and all eight neural pilots are complete. New-case retention has been approved
and verified on disposable copies; see the [storage checkpoint](v20_storage_lifecycle.md).
No full neural launch, original-artifact deletion,
database access or promotion has occurred.
Original producers and completed research outputs remain unchanged.

**Latest:** pilots finished in28.07minutes, all16fits successful, no cap hits,
selected7–23epochs.42receipts verified and selected-inner scores replay exactly.
New production case entry point retires temporary files only after durable
verification and preserves outer forecasts losslessly:2.506→.445GiB on eight
independent copies, all48forecast exports byte-exact.35tests pass. Original pilots
remain intact. [Matched scoring rehearsal](v20_scoring_rehearsal.md) now passes:
four point panels,32native event panels, both conditional checkpoint windows,
report/preview parity and16targeted tests. Adam freed more storage:196.55GiBfree
versus75.32GiBcalendar-scaled case/scoring/stress/reserve estimate, excluding
remaining downstream analyses. Partial training estimate44.38/52.69hcentral/stress.
Full launch remains unauthorized; downstream rehearsal and orchestration remain.
Earlier active/pending descriptions below are the implementation history, not
the current job state. Current operations are in the single handoff.

## Current checkpoint: historical library verified, neural pilots active

The following supersedes earlier launch/pending descriptions in this report;
those sections retain the history of individual prerequisites.

Library `experiments/cache/v20_library_full_2026_10_04` completed all2,032snapshots
in120,389.9seconds (33.44h), eight254-date chains, no failed workers. New derived
audit `experiments/cache/v20_library_audit_2026_10_06` verifies4,562receipts,
384annual candidates including read-only pilot reuse, strict source/fit dates,
annual choices, preceding-snapshot warm starts, player/clock gauges, stored
marginal SDs against joint draws and original-Hessian residuals. All converged;
snapshot max238iterations and max residual9.99985e-9. All2,032selected player
penalties equal the original library. Audit writes new CSVs; original artifacts
are unchanged. It took67seconds, not another profile build.

392matched channel audits (49registered dates ×eight chains, including warmup)
use parent-grain reference **mean-rate** NLL with identical games/exposures:

| Family | Offense relative pooled NLL change | Defense relative pooled NLL change |
| --- | ---: | ---: |
| Counts | −0.01085% | −0.00996% |
| Location | +0.00548% | +0.00745% |
| Conversion | +0.00166% | +0.00137% |
| Recovery | −0.00098% | −0.00094% |

These are descriptive profile-channel audits over the full registered calendar,
not the44quarter primary NN population. Conditional label-splitting constants
remain noncomparable. Tiny NLL changes do not establish better learned lineup
predictions, causal player effects, counterfactual coherence or uncertainty.

`experiments/cache/v20_feature_audit_2026_10_06` passes bothdates ×inner/final.
Original raw prefix objects/loss scales are byte-identical; adjusted normalizers
are recomputed. Historical rows use47distinct snapshots in the early prefix
and63in the late prefix, not final-date backfill. An in-memory .125coefficient
sentinel on each bank changes predictions through the actual trained NN/memo;
raw tensors remain identical. Mismatched profile-normalizer provenance fails.
Sentinel point differences are wiring evidence, not basketball effects.

New `v20_case.py` exports selected-inner and final ledgers, direct and checkpoint
mixtures, reference and conditional environments, and **both** conditional-state
windows. That enables later seed-averaged ledger likelihoods without averaging
nonlinear losses. Case-level receipts resolve the trainer's pending-environment
marker without editing fits. Selected-inner objective is reconstructed from saved
weights at1e-10absolute/1e-12relative tolerance. Near-minimum plateau count/span,
timing, peak RSS and artifact bytes are saved with prefix/source provenance.

Twelve targeted tests pass in3.60seconds (`nn_pilot_tests3.log`), including two
actual toy end-to-end inner/final cases, complete serialization/reuse and selected
mixture replay. Earlier failed logs are preserved: a context-reference ndarray
needed tensor serialization rather than JSON, caught before any real pilot.
No frozen library/replay/trainer producer was modified.
The consolidated27test foundation/case suite also passes in7.62seconds
(`pilot_launch_all_tests.log`).

Pilot root `experiments/cache/v20_nn_pilots_2026_10_06` now has its frozen
transitive producer/source manifest. Eight registered cases,3workers/1thread;
late S_ADJ/S_BOTH first, plus all six new arms at2016q1/s17. Detached caffeinate
launcher PID47716; supervisor `logs/nn_pilots.log` under implementation root,
per-case epoch logs under pilot `queue/logs`. Initial late-case epochs about
15–17seconds; S5 validation rings about58MiB plain /105MiB FULL at five epochs.
These are early observations, not a full-run time estimate. About54GiB immediately
free at launch; no cleanup or full-campaign launch. Old controls are reused.

Remaining: completed neural pilot review, scoring/report/preview, registered
downstream/uncertainty integration, production-shaped rehearsal and measured
runtime/storage forecasts. No launch command for a full campaign is ready yet.

## Implemented and verified so far

- Declarative eight-cell factorial, six new arms, 17 point/44 event contrasts.
- Joint actor/teammate/defender + clock GLMs for all four families, separate
  opportunity-weighted orthonormal gauges, unknown/unsupported clock zero,
  unpenalized intercept, fixed clock ridge1000 and unchanged player ridge grid.
- In-memory margin collapse of original v19 labels; sparse player design remains
  at parent-matchup grain. Strict-date league offsets and annual tuning.
- Full joint covariance, including player–clock coupling. Exact cached curvature
  and shared factors avoid re-reading every state row for every draw. Dense
  synthetic helper bounded to64players/10,000actors; not the production route.
- Versioned pilot library builder, 97/49-feature adapter, explicit profile
  provenance/normalizer guard, historical lookup and shared unknown-player draws.
- P/S5 training primitives, last-five expected-ledger window, endpoint weights,
  transactional optimizer/RNG/window resume. FULL selects conditional likelihood;
  no-context selects original parent likelihood. Neither sees outer outcomes.
  Selected/final environment evaluation primitives now exist; the full case
  consumer remains pending. Fit payloads retain the pending marker; a future
  case-level evaluation receipt must resolve it without rewriting completed fits.

Twenty-two targeted tests cover gradients/Hessian, zero-clock nesting and splitting
constants, full-vs-Schur covariance, cached-vs-reference draws, future poisoning,
schema/date rejection, unknown/clone sharing, exact old-policy optimization and
selection on a toy fixture, exact S5 inner/final resume, annual-pilot read-only
reuse, chronological calendar resume, low-storage refusal, unchanged raw contexts
and conditional/reference event equivalence. Real saved-control inference replay
also passed (below). The eight full NN pilots remain unrun.

## Completed empirical prerequisite

Frozen source: `experiments/cache/v20_synthetic_full_2026_10_04`.
All640fits converged;128full-joint draws each;488.07seconds wall time.
Maximum original-Hessian solve residual6.83e-15.20replicates per family/scenario.
Derived diagnosis: `experiments/cache/v20_synthetic_review_2026_10_04`.

Prespecified overlapping-deployment scenario2:

| Family | Original coefficient RMSE | Joint-clock RMSE | Original common-environment prediction RMSE | Joint-clock RMSE |
| --- | ---: | ---: | ---: | ---: |
| Counts | .066983 | .065299 | .019868 | .017249 |
| Shot location | .091189 | .090888 | .036801 | .036477 |
| Conversion | .128966 | .128959 | .086244 | .086245 |
| Recovery | .094507 | .094063 | .025345 | .025149 |

Synthetic native-rate/probability errors, **not NBA point r²**. Counts improve
13.2% on novel-composition mean prediction; location0.88%, recovery0.77%.
Conversion is effectively tied: paired difference+0.0000010,95%Monte Carlo
interval[−.000018,.000020]. Other three paired prediction intervals exclude zero.
Strong segregation and hidden-interaction scenarios retain that pattern.
Balanced zero-clock control incurs tiny costs from estimating unnecessary
nuisance (count prediction RMSE+.000048), not an exact-zero empirical effect.

### Recovery-gate investigation

Conversion does not establish improvement. Saved-fit diagnosis finds strong
shrinkage: scenario2 fitted-vs-true player projection slope.139 for conversion,
versus.625 counts,.358 location,.396 recovery. Conversion fitted coefficient RMS
.0275 versus true.1483. Fixed lambda1000 implies prior SD.03162; the generator
deliberately uses scale.15. Bin-specific conversion opportunities carry little
information relative to that penalty.

Nominal95% coefficient bands cover only about40% of known truths, even in the
balanced zero-clock control. Substantial shrinkage bias/prior mismatch, not a
calibrated frequentist confidence claim. Full-Hessian draws include nuisance
variance but do not repair mean bias. Schur/solver tests pass; **that numerical
fact does not rescue coverage**. Hidden interactions add misspecification.

Lead decision: proceed to bounded real profile pilots with these limitations
recorded. Three mechanisms recover better; conversion unresolved, not a win.
Do not tune the frozen generator, lambdas or arm grid after seeing results.
NBA profiles select player ridge on strictly prior quarters, rather than using
synthetic fixed1000 throughout. Reason to measure pilots, not evidence of future
improvement. U0/U1 and transport-discrepancy evaluation remain necessary; profile
draws are not latent-quality intervals.

## Real-source arithmetic audit

`experiments/cache/v20_profile_source_audit_2026_10_04` passes16comparisons:
two dates ×two banks ×four families;512deterministically spaced parent rows per
date. State-to-parent target/opportunity reconciliation; zero-clock support,
gradient, Hessian and parameter-independent NLL constants match at floating-point
precision. Arithmetic audit, not an accuracy result. Original point-accounting
exceptions unchanged. Calendar confirms254snapshots/384annual candidate fits.

## Completed real profile pilots and independent review

Source: `experiments/cache/v20_profile_pilots_2026_10_04`.
Derived review: `experiments/cache/v20_profile_review_2026_10_04`.
All122completion receipts verified. All96fits converge:16new snapshots,
16fixed-old-penalty diagnostic snapshots and64annual candidate fits.
Eight chains,3CPU workers/1thread,71.54minutes wall time. Maximum289iterations
of500; maximum projected gradient9.95683e-6 (<1e-5); largest joint-draw
original-Hessian residual9.97912e-9 (<2e-8). No tolerance changes.

All16chosen player penalties match the original library: counts/location/
recovery10, conversion100 at2016q1 and1000 at2026q4. Twelve selections remain
on the grid's low edge, including their original controls. No expansion,
new penalty sweep or outer-result selection was introduced.

Matched old/new **parent-grain reference mean-rate** held-out likelihoods:

| Family | Relative NLL change range across two dates/two banks | Coefficient RMS change | Mean marginal-SD ratio |
| --- | ---: | ---: | ---: |
| Counts | −.07919% to +.00906% | .00844–.01737 | .99744–.99981 |
| Location | +.00331% to +.02220% | .00121–.00523 | .99814–1.00096 |
| Conversion | +.000016% to +.001043% | .00029–.00111 | .99903–1.00035 |
| Recovery | −.01078% to +.00519% | .00085–.00301 | .99840–1.00344 |

Negative NLL change is better. Near ties, not a standalone profile predictive
breakthrough, neural r² result or reason to revise the factorial. Counts move
most. Joint clock uncertainty does not substantially widen these marginal SDs.
Actual-clock conditional NLL uses different label-splitting constants; the
review exports it separately and never directly contrasts it with parent NLL.
Clock-integrated **mean-rate** likelihood is not a mixture-density likelihood.
Fixed-old-penalty comparisons are exported, not turned into new production arms.

Numerical prerequisite passed; basketball coherence and hypothetical-quality
uncertainty are not established by these pilots. Synthetic undercoverage and
causal-identification limitations remain unchanged.

## Historical build and storage gate

`v20_calendar.py` adds the full254-date/eight-chain builder as a separate
consumer, leaving completed pilot producers untouched. It references mapped
inputs, uses strict chronological warm starts and can reuse64verified annual
pilot candidate fits read-only. It does not reuse cold-start pilot snapshots as
if their warm-start provenance matched. Queued workers use the retention wrapper.
Resumption, per-chain receipts/progress, fail-stop execution and storage checks
are implemented; no full neural auto-launch is possible.

Original full-calendar file sizes scaled by the larger of early/late measured
snapshot size ratios and matched annual-fit sizes project **16.993GiB** of new
profile artifacts. This is not a measured completed-library footprint. Add25%
size stress,3GiB temporary worker headroom and10GiB reserve: **34.241GiB free**
required before an empty build. Actual free space11.12GiB; preparation refused
before creating the proposed library directory. Target35GiB free (about24GiB
more), or an approved alternate output volume. No deletion performed.
This estimate excludes all later neural/analysis artifacts; their forecast
requires the neural pilots. This was the initial storage-blocked checkpoint.

### Capacity clarification and profile-only launch

Adam subsequently freed storage and reported over100GB available in Settings.
The filesystem showed21.04GiB free; independent `diskutil` confirmed22.6GB.
Read-only native Foundation queries reconciled the figures: macOS reported
112,228,577,710bytes available for user-requested work, including reclaimable
space, versus24,407,191,552bytes immediately free at the later query. These
are different capacity concepts, not GB/GiB rounding or a failed cleanup.
Apple recommends its important-usage capacity API for user-requested storage:
[Checking Volume Storage Capacity](https://developer.apple.com/documentation/foundation/checking-volume-storage-capacity).

New `v20_storage.py` uses this OS estimate for the full-budget preflight,
conservatively falling back to filesystem free bytes if the API fails. The
calendar retains the **13GiB immediate-free floor between fits**. It can stop
resumably if automatic reclamation does not keep up; availability is an OS
estimate, not a reservation. No manual cache purge, snapshot deletion, dummy
file allocation or relaxation of fit/curvature criteria. No original completed
producer was edited. Capacity policy/helper hashes are recorded in the new
library manifest and the measured values in `capacity_at_prepare.json`.

Preparation passed at104.52GiB available /22.73GiB immediately free. Launched
`experiments/cache/v20_library_full_2026_10_04`, detached caffeinate PID13402,
three CPU workers/one thread. Durable supervisor log `calendar_build.log` under
implementation logs; verbose chain logs under the library `queue/logs/`.
This job builds historical profiles only, never neural fits automatically.
New storage tests check the two distinct capacity quantities, conservative API
fallback and retained immediate reserve; all five storage/calendar tests pass.
The full22-test suite passes in5.41seconds (`storage_prelaunch_all_tests.log`).

## Production-source control replay

`v20_case_inputs.py` retains the exact original raw/parent/loss context and
recomputes **only** adjusted normalization for a changed bank.
`v20_evaluate.py` gives both decoder choices the same conditional/reference
output interface. No-context forecasts repeat across actual state labels with
the original parent constants; checkpoint forecasts mix complete ledgers.
Conditional state exports are available for seed-mixture event comparisons.

Real replay: `experiments/cache/v20_control_replay_2026_10_04_v4`.
P_BASE/P_CONTEXT,2016q1/2026q4,seed17; **four cases, zero refits**.
Selected inner objectives and full outer direct/averaged ledgers replayed;
FULL includes conditional and reference environments. New interfaces match the
unchanged current evaluators bit-for-bit. Inner objective checks retain strict
1e-10 absolute/1e-12 relative tolerance. Archived predictions have small mixed-
precision runtime drift, at most about1.07e-7 points/100, within the existing
v19 float32 scale guard. No changed weights, objectives or selection rules.

Preserved failed replay outputs/logs without suffix and `_v2`/`_v3` document
an initially over-strict archive comparison. The previously documented v19
canonical/fast/memo replay probe localized this same runtime issue; current
unchanged-evaluator parity remains exact. This guard applies to archived neural
inference, **not** float64 solver/objective/gradient tests. A toy conditional-
equivalence test also needed valid integer trial labels: splitting a single
attempt into two half-attempts engages the unchanged binomial clamp differently.
Real labels and production likelihoods were not changed.

Archived controls lack inner averaging weights; replay covers their selected
inner endpoints and final archived averaging windows. It does not claim full
real optimizer-trajectory retraining. Toy optimization/resume parity covers
the training primitive separately.

## Operations and remaining work

Logs: `experiments/cache/v20_implementation_2026_10_04/logs/`.
Synthetic: `synthetic_full.log`; source audit: `source_audit.log`; tests:
`foundation_tests.log`, `curvature_tests.log`, `fit_library_tests.log`,
and the consolidated `all_tests.log`. Current20-test suite: `prelaunch_tests.log`
(3.37seconds); profile review: `profile_review.log`; storage refusal:
`calendar_readiness.log`; real replay: `control_replay4.log` (68.4seconds).

Completed: bounded real profile pilot. Active: full historical profile library,
not the neural campaign. Current job/commands are in the single handoff.
Supervisor log: `profile_pilots.log`; worker logs: pilot `queue/logs/`.
Use `python -u -m experiments.v20_profile_pilot status --out <pilot-root>` with
the repository interpreter. No automatic full-library or NN launch follows.
Queue/status commands implemented; full v20 launcher not implemented or approved.
The new pilots occupy about469MiB on disk. All original outputs remain intact.

Still required: full historical build and resulting library
audits; source sentinel and large-memory S5 checks;
eight full NN pilots; case/scoring/report/preview/queue integration; registered
coherence, transport, uncertainty and independent audits; production-shaped
rehearsal and measured launch/storage forecast. No full training command until
those readiness steps pass.
