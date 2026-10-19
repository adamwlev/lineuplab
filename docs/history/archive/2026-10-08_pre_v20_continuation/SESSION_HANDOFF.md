# Current handoff — V20 launched (2026-10-06)

## Authority and exact restart step

Direct implementation only; no delegation. Adam explicitly approved full launch
on2026-10-06. **V20 is running**, detached supervisor PID53523, with three numerical
workers and durable logs. At12:38PDT the first2015q1/P_ADJ seeds17/23/41 were
progressing through inner-fit batches; no failures. Eight reused pilots count as
8/864completed slots;856new cases were queued. Inspect status/logs rather than
launching a second supervisor. [Launch record](reports/joint_capability_v20_launch.md)
records authority and commands; the readiness report remains the prelaunch record.
Do not refit pilots, rebuild inputs, scrape, mutate the database, promote a
scorer or delete historical artifacts.

[Plan](JOINT_CAPABILITY_V20_PLAN.md), [state](JOINT_CAPABILITY_STATE.md),
[product contract](CONTEXTUAL_MODEL.md) §1–2 govern the frozen science.
Three standards remain coequal; no pair chemistry, forced rankings or gates.
Latest checkpoint:3fd8bc28 (complete prelaunch implementation/rehearsal).
Launch documentation updates are uncommitted; never stage generated cache files.

Adam also requested [post-v20 direction notes](MODEL_RESEARCH_ROADMAP.md#post-v20-direction-notes--2026-10-06)
following the Opus 5.5 review. They record candidate diagnostics, defensive
coverage/transport experiments and caveats; no new experiment is frozen or
launched. This documentation-only follow-up does not change v20 or its next step.

Subsequent [bias follow-up](MODEL_RESEARCH_ROADMAP.md#bias-follow-up--exploratory-evidence-2026-10-06)
adds two standalone diagnostic consumers and new derived outputs/logs, no fits or
production changes. Retained NN global FG-conversion mean error nearly cancels,
but final-exposure cohort selection exposes a persistent gap; prior-known exposure
has a smaller gap and first-three-game shooting residuals barely persist. Read
the population/estimand caveats before planning a correction. Files are uncommitted.

## What is ready

- Eight factorial arms: retained P_BASE/P_CONTEXT; six new P_ADJ/P_BOTH/
  S_BASE/S_CONTEXT/S_ADJ/S_BOTH.48quarters, seeds17/23/41.864new-arm slots
  minus8exact reusable pilots =856remaining.2015warmup excluded from primary.
- Full2,032snapshot adjusted-profile library, deep4,562receipt audit,640fit
  synthetic suite, eight NN pilots, compact lifecycle and matched scoring done.
  Original pilots/profiles unchanged. New-case retention saves82.22%.
- Physical checkpoint/seed mixtures, five extra descriptive controls, event/
  role/transfer/context curves, persistence/covariance, fixture discrepancy,
  average-opponent integration and17/44/4registered contrast schemas implemented.
- Three total process slots with prioritized single-writer chronological
  scoring.19post-training analysis/audit stages. Full production-shaped graph
  rehearsal passed using the two pilot dates; all65unit tests pass.
- Completed-source resume and deliberate partial-census interruption replay
  pass. Full-calendar synthetic contrast schemas also pass.
- Sealed readiness status READY_FOR_APPROVAL with zero unresolved prelaunch
  items. It is not full experiment completion or three-pillar model acceptance.

## Batching answer and important limitations

Adam asked whether the expensive deployment-risk census could be batched.
Yes: cache lineup/defender-only work, vectorize input construction, batch the
remaining decoder operations.30measurements over2dates/3seeds show exact count/R
parity; typical64-five decoder time2.8–3.0s→.20–.23s.1024-five end-to-end time
2.00–3.01s per seed. No historical-lineup sampling amendment.

Full one-seed censuses:157,527compositions/7.44min early;314,494/15.01min late.
Independent first/middle/last-block slow replay has zero count error; complete
coverage and historical95th-percentile arithmetic verified. The shared high-R
slice flags6/4,412future compositions early (1supported) and123/7,015late
(77supported). This is not proof of useful error detection; slice power may be
limited. Thresholds use no future outcomes; low support is separate, never a gate.

Late three-seed retained conditional count losses .766840/.764845
(P_BASE/P_CONTEXT) reproduce the known context effect; not a new v20 winner.
All four late pilot candidates still favor legal centers against both Jokić
examples (+5.69to+7.62primary-blend margin). No coherence pass. Cold uncertainty
is unidentified; fixture bands do not certify latent hypothetical quality.

The first graph rehearsal exposed a controls resume bug: v1 overwrote ONLY its
root timing/status file, invalidating that root receipt. Original quarter
receipts, numerical tables and forecasts remain valid. Do not repair or reuse
that broken root. New v20_controls_v2/new output prefix matches62forecast arrays,
all numeric tables and calibration exactly and resumes without writes.
See [downstream evidence](reports/v20_downstream_rehearsal.md).

## Resource budget and paths

Remaining total forecast63.21hcentral/82.42hstress; all-cases96-epoch-cap scenario
256.49h, not a hard upper bound. Includes training44.38/52.69h, exhaustive risk
8.98/14.41h, average-opponent5.86/7.32h and4/8hexplicit allowance for other
scoring/analysis/audits. Already-completed library/pilots excluded.
Required immediate free storage102.97GiB including margins/reserve;
195.06GiBavailable at readiness. Other workloads and later epochs can exceed
timing forecasts. No sampling or historical cleanup required.

All paths below are under experiments/cache/:

- Running production:joint_capability_2026_10_06_v20_prod
- Readiness:v20_prelaunch_readiness_2026_10_06
- Full resource forecast:v20_full_resources_2026_10_06
- Graph rehearsal:v20_pipeline_rehearsal_2026_10_06_v2 and derived siblings
- Census:v20_risk_census_pilot_2026_10_06/{2016q1,2026q4}
- Census resume:v20_risk_resume_rehearsal_2026_10_06
- Control repair replay:v20_controls_resume_rehearsal_2026_10_06
- Existing pilots:v20_nn_pilots_2026_10_06; compact:v20_storage_rehearsal_2026_10_06
- Scoring:v20_pilot_scored_2026_10_06; descriptors:v20_descriptor_library_2026_10_06
- Profile library:v20_library_full_2026_10_04

Logs:v20_implementation_2026_10_04/logs/, especially
pipeline_rehearsal_v2.log, risk_census_<origin>.log, prelaunch_readiness.log,
controls_resume_rehearsal.log, risk_resume_rehearsal.log and full_resources.log.
Readiness check_01.log records65tests. Production manifest now records explicit
full-launch authority. Live log is joint_capability_2026_10_06_v20_prod/logs/launcher.log;
percase epoch/batch logs are under its training_queue/logs/. Run
`bash experiments/run_joint_capability_v20.sh status` for current progress.
All19post-training stages run automatically after training/scoring; the final
scientific interpretation still requires review. No automatic assistant wakeup.

Every native consumer/child uses artifact_retention exec with ledger
completed_resume_retention_2026_09_30; correct basketball25 Python, six numerical
thread limits1. Frozen sources now fingerprinted; any fixes require successor
consumers/new prefixes. Do not edit completed campaign artifacts.

[Previous handoff](docs/archive/2026-10-06_pre_v20_readiness/SESSION_HANDOFF.md)
preserves earlier detailed prerequisites and linked history.

