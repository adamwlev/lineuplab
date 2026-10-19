# Current handoff — v19 ~65h accepted; integration/storage pending (2026-09-30)

## Authority and state

Adam now accepts roughly65hours for v19 and explicitly defers the proposed
validation optimization. See the [runtime amendment](reports/joint_capability_v19_runtime_authorization.md).
Full frozen v19 launch approval is already recorded, conditional on readiness;
do not ask again unless material scope/runtime changes require a decision.
**No full campaign has launched.** Direct work only,
no delegation. Last commit: **32ab995d**. The new downstream/prelaunch work is
uncommitted; no additional commit was made in this turn.

Read [prelaunch checkpoint](reports/joint_capability_v19_prelaunch.md) for measured
results, exact commands, caveats and remaining work, then the
[frozen plan](JOINT_CAPABILITY_V19_PLAN.md). The earlier
[native implementation report](reports/joint_capability_v19_implementation.md)
is historical; its original pre-cleanup storage failure is not current free space.

All seven native pilots remain complete and unchanged. New scorecards, preview,
opponent integration, uncertainty and fixed-fixture pilots are complete and
independently audited. All bounded jobs have finished; nothing remains running.
No new scientific winner, three-pillar pass or scorer promotion.

## Runtime allowance and remaining storage/integration checks

Native-only remaining projection: **53.19h selected,63.82h at1.2× stress**, with
three busy workers and seven pilots reused (713new cases). This uses row-scaled
concurrent pilot timings and per-arm maximum measured costs, not fixed epoch
knowledge for future fits. Cap scenario227.14h is not the expected run. Downstream
and barriers are still excluded; do not divide again by measured parallel speedup.

Full native artifact estimate47.257GiB; latest free66.107GiB leaves8.850GiB after
the10GiB reserve for all downstream/control/temporary costs, still unmeasured.
Adam superseded the old <=48h reference / <=54h stress targets with acceptance
of roughly65hours. They are no longer launch blockers; the all-in runtime must
still be reported honestly and a materially larger estimate flagged. Storage
and pipeline readiness remain unfinished. Do not alter frozen reports to relabel
their historical HOLD; bind the separate runtime amendment in future readiness.

Three-worker benchmark:40.52s sequential versus15.94s parallel (2.542×), exact
weight parity. Six engineering jobs,2epochs over12complete late game batches.
These are NOT scientific fits. Host has16GiB RAM/10logical CPUs/8performance
cores; prior full-worker peak4.016GiB. Do not assume four full workers are safe.

**Exact speedup deferred by Adam; not a v19 prerequisite:** the fitter evaluates reference
diagnostics every validation epoch even though only conditional scores select
epochs. Saved-model profiling across all7pilots shows exactly unchanged
conditional statistics/RNG without that work. Early C_MARGIN validation7.261s
both views versus.612s conditional. Keep this in the future engineering backlog;
do not implement or benchmark it further for this launch. Any future adoption
requires a NEW versioned fitter and trajectory/selection/resume equivalence.
The current verified fitter and full scientific evaluations remain unchanged.

## Required retention mode

Completed v16–v18 optimizer retirement removed19,420resume payloads from9,792fits.
All weights, averaging checkpoints, predictions, original receipts and frozen
code remain. Read [retention operations](docs/ARTIFACT_RETENTION.md).

Ledger: experiments/cache/completed_resume_retention_2026_09_30.
Plan SHA256:825e76b9b847ab3b3ea046b5b302cac772d093a4c6f32be6e3319be7af826cd2.

Legacy strict verification intentionally rejects retired restarts. Invoke
consumers through `python -u -m experiments.artifact_retention exec --ledger
<ledger> <module> <args>`. Every spawned Python worker must use
`artifact_retention.python_job(ledger,module,*args)`; wrapping its parent does
not propagate in-memory verification. New benchmark exercises this successfully.
No further deletion is authorized.

## Evidence at this checkpoint

Prefixes use experiments/cache/joint_capability_2026_09_30:

- _v19_sources2:288teachers/48origins/3seeds,599checks.
- _v19_labels1:3,056,123states conserve1,592,743matchups/6,059,380possessions.
- _v19_replay1:120float64 value/loss/gradient checks.
- _v19_micro1:7exact optimizer/resume checks.
- _v19_pilot1:7full native cases,30m18s; no failures/cap hits.
- _v19_native_audit2: original native point/reference-event/primary-state audit.
- _v19_controls_pilot1 and _v19_control_audit2: fair point controls, both dates.
- _v19_pilot_scored1: separate reference/CLOCK/MARGIN panels; calibrated cold-start
  pilots, not production prequential results or arm-selection evidence.
- _v19_scoring_audit1: all5panels,3,820sufficient rows, exact calibration replay.
- _v19_average_pilot1/{2016q1,2026q4}: all187/206broad cells,512opponents and fixed
  first20at4096;154.65s/51.61s. Max half sensitivity.14948/.03458points per100.
- _v19_uncertainty_pilot1:13.53s; own-candidate U0/U1,80/95levels, weighted proper
  scores, frozen transfer labels. All pilot U1 NOT_IDENTIFIED; no invented history.
- _v19_basketball_pilot2/2026q4:21registered fixtures+3defensive references,
  576directed pairs/model across6models;5.04s. Context curves and native ledgers.
- _v19_downstream_audit1: preview parity, opponent means, uncertainty statuses,
  exact fixture mixtures and both-direction margins pass.
- _v19_average_event_audit2: all7checkpoint-average conditional event likelihoods
  now audited by saved-state replay + independent numpy/scipy arithmetic.
  Max event error3.59e-13. This closes the old native-audit missing-event item.
- _v19_parallel1: one/three-worker benchmark and exact final-weight equality.
- _v19_validation_profile1: saved-weight timing probe, no fitter changes.
- _v19_prelaunch_resources1: per-case native timing projection; explicit HOLD.

Durable sibling logs; average logs use _early.log/_late.log.
43v19tests pass in experiments/cache/v19_prelaunch_tests2.log.
Verified pilot report/preview commands are in the prelaunch report.

Preserved failures: basketball_pilot1 JSON serialization (fixed in newprefix2);
average_event_audit1 archival1e-8point mismatch. Audit2 current canonical/factory
paths agree exactly; tiny archive drift is explicitly guarded by one float32
scale epsilon, same policy as control replay. Max archived point drift1.0431e-7,
max any-field guard fraction.13044. The root cause is not established; no
float64 objective/value/gradient tolerance was relaxed and no artifact changed.

## Exact next steps

1. Retain the verified fitter; defer the optional validation optimization per
   Adam's runtime amendment. Preserve all arms/seeds and the scientific protocol.
2. Finish event/conversion, observed-role/transfer, two-big analogues, persistence,
   full covariance, high-support context curves and registered scientific summary.
   Exported transfer interval labels are not a completed role/transport analysis.
3. Measure complete late downstream bundle, all-in selected/cap/stress runtime,
   controls/derived storage and temporary peaks with10GiB reserve.
4. Build frozen full launcher with retention-aware children, explicit compatible
   pilot reuse, chronological calibration barriers and all stages. Verify retained
   controls' production calibration parity. No full launcher exists yet.
5. Under the updated roughly65h allowance, if resource/integration checks pass,
   verify launch/log/status/report/preview
   commands and use recorded launch approval. Otherwise obtain the material
   runtime/scope decision; do not silently remove arms/seeds/analyses.

All original producers/outputs remain unchanged. New completed downstream
producer hashes are frozen too: do not modify them in place to change completed
artifacts. New correction modules/output prefixes when required.
No known-pair chemistry or forced basketball rankings. J_POINT_BOTH remains the
research reference. Finite-game bands do not certify synthetic latent quality.
2015warmup/2016–2026primary and original transfer population remain unchanged.
Missing2014q4 additive inner diagnostic retains its explicit unavailable status.

[Previous operational checkpoint](docs/archive/2026-09-30_pre_v19_downstream/SESSION_HANDOFF.md)
preserves the cleanup/native-only state.
