# Current handoff — v17 ready, not launched (2026-09-27)

## Authority and current state

Direct implementation only; no delegation. Adam authorized continued work and
checkpoint commits. **No full v17 launch until he approves or runs the supplied
command.** No active training/analysis process. No scraping, database access,
input-cache rebuild, scorer promotion or deployment in this implementation.

Read [launch readiness](reports/joint_capability_v17_launch_readiness.md) for
verified commands, outputs, runtime/storage, caveats and complete evidence.
Scientific design: [frozen v17 plan](JOINT_CAPABILITY_V17_PLAN.md).
All720 production cases /1,440 fits remain unlaunched.

## Completed this checkpoint

- Fixture/mirror/flow-capacity diagnostics: all32 frozen cases at10 dates,
  direct/half, full native per-player/location/renewal/flow ledgers, independent
  permutations, duplicate profiles. No exhaustive synthetic integrations.
- Pooled/quarter/season metrics and five cohorts/allfour views;16 registered
  half RMSE contrasts, season bootstrap/exact swaps/Holm; native event/point
  losses, epochs, residual correlations, seasonal/bias diagnostics.
- Separate direct/half U0/U1 summaries, matched identified populations,
  unchanged real analogues/allmembers, outcome-selected top/bottom10 descriptions
  with their own intervals. Pilot tables successfully run end-to-end.
- Production supervisor: threeCPUworkers/one thread, durable per-case logs,
  chronological scoring, automatic product/coherence/uncertainty/summary/handoff
  stages, receipt-backed resume. Full run is explicit, not triggered by prepare.
- Versioned production case writer uses the unchanged v17 fit/model code.
  Five pilot cases are not relabeled/reused; their campaign receipts differ.
- Source/producer fingerprints frozen in the prepared production manifest.

## Verification

33 launch-gate tests plus2 report-rendering tests passed. All288 dated contexts
and288 reused controls verified. **576** actual production calibration replays
passed (48quarters ×2arms ×3seeds ×2views). Batched early/late average-mode
control replay agrees within4.27e-14pts/100. Allseven architectures passed21
late-date fixture-input probes. Constant U1 replay on2,249 prior pairs matches
both archived point-half and J_BOTH-half fits within4.45e-16 inparameters.

A tiny real-fixture permutation discrepancy required a diagnostic tolerance
adjustment, not a model change. Failed audit1 and summary_dev1 are preserved;
successful counterparts are audit2 and summary_dev2. See readiness report.
Synthetic true-quality uncertainty and basketball rankings remain unvalidated.

Runtime scenarios: reference-like stopping29.24training hours +1–3hours
downstream; doubled training58.49hours +1–3hours. Not confidence limits.
Estimated31.49GiB additional storage,10GiB reserve,122.74GiB physically free at
preflight. No seeds/epochs/design reductions to meet the estimate.

## Current operations

Prepared native prefix:
`experiments/cache/joint_capability_2026_09_27_v17_prod`.
Readiness and source hashes:`preflight.json`, `manifest.json`.

```bash
bash experiments/run_joint_capability_v17.sh status --run-dir experiments/cache/joint_capability_2026_09_27_v17_prod
```

Verified output:ready_not_launched,0/720cases. Report correctly saysNO_ROWS.
Repeated prepare verifies readiness without creating fits. Launch/live-log/
leaderboard/per-case commands are in the readiness report; do not interpret
their existence as authorization to launch.

New modules under `experiments/`:v17_analysis_tools,v17_basketball,v17_summary,
v17_production_audit,v17_production_case,v17_run,v17_handoff; shell wrapper
`run_joint_capability_v17.sh`. No completed producer edited. New tests:
test_v17_analysis,test_v17_run,test_v17_handoff.

Generated artifacts stay out of git. Existing history includes8949128a
(pilot/scoring),91be8b52(core),e9f994ec(design),3fb8f1cb(v16 follow-up).
This checkpoint commits launch integration, tests and documentation.

## Precise next step

Wait for Adam's full-run launch/approval. During a valid run, no tuning or
stopping because interim accuracy disappoints. On failure preserve logs and
receipts, diagnose and version any warranted repair. The same command resumes.

When complete, review the generated `_handoff/HANDOFF.md` and underlying
`_summary`/`_basketball` outputs independently, discuss allthree pillars, and
document a scientific conclusion without automatic promotion. The v16 point
candidate remains retained until that review.

[Previous handoff](docs/archive/2026-09-27_pre_v17_launch/SESSION_HANDOFF.md)
preserves the pre-integration checkpoint.
