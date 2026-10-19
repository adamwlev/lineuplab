# v16 launch implementation — 2026-09-18 checkpoint

The 22-arm design is unchanged. This is an implementation/verification record,
**not a new neural accuracy result or a claim that preflight already passed**.
The [handoff](../docs/history/SESSION_HANDOFF.md) gives the live background-state paths.

## Completed implementation

- Chronological common prior-affine calibration, native/late-checkpoint views,
  explicit 50/50 A+D blends, expanded populations, seeded predictions and
  read-only sortable/sliceable leaderboards. No current-quarter calibration.
- Deterministic complete-GLM `ADJUSTED_CHANNEL`, with one normalized action
  budget and renewal, its own event likelihoods and equally calibrated half.
- Fixed fixtures, actual dated defenses, both scoring directions, per-player
  phase/action/collector ledgers, intervention order dependence and shared
  bank-at-a-time coefficient-draw sensitivities.
- Separate average-opponent task: fixed three-model set, shared 512-reference
  approximation, 4,096-reference sensitivity, pooled/season/paired tables.
- U0 finite-game intervals for every new forecast; fixed U1/U2 models with
  disjoint whole-game halves, strictly prior noise forecasts, support/transfer
  validation and alternative-split diagnostics. Hypothetical bands disclose
  extrapolation and finite horizons; they do not certify latent-mean coverage.
- Factual cohort channel tests and adjusted-vs-matched-cadence own-only profile
  diagnostics. Full named-contrast/Holm families, retained controls, native
  sensitivity, bias decomposition, selected-epoch/cap reports and a quantitative
  three-pillar matrix. Original reports/protocols remain untouched.
- CLI lifecycle, durable worker/epoch/report logs, fail-stop three-process
  scheduling, direct worker interruption, independent replay/cutoff/ledger/
  calibration audits, resource preflight and preparation-only continuation.

Implementation choices were written before NN pilots in
[the conventions](joint_capability_v16_implementation_conventions.md).
All new derived outputs use new prefixes. No database access, scraping, old
input rebuild, scorer promotion or deployment occurred.

## Verification completed before the long acceptance sequence

Local artifacts below share prefix
`experiments/cache/joint_capability_2026_09_18_`.

| Check | Verified result | Artifact |
| --- | --- | --- |
| Numerical/runtime foundations | Six identical one-epoch full-prefix jobs: 324.0 seconds serial vs 141.8 with three workers; no parameter differences | `v16_fullprefix_parallel_dev1` |
| Exact location covariance computation | 32 same-seed draws in 135.5 seconds; relative difference 4.92e-9; maximum original-Hessian residual 9.95e-9; peak RSS 2.89 GiB | `v16_location_draws_dev1` |
| Compiled dated lookup | Bit-for-bit values/metadata; ~4.32× lookup speed, not a claim of 4.32× training speed | `v16_feature_lookup_dev1` |
| Real arbitrary-lineup scoring bridge | 32 rows at each of 2016q1/2026q4; exact input equality; additive/A+D error <=1.42e-14; neural error <=1.29e-5 points/100; archived wrapper exact | `v16_scoring_bridge_final` |
| Uncertainty assumptions | True tau²=4 recovered ~4.12 with ~95.5% finite coverage; correlated noise falsely appears persistent (~8.9); opposite role drift lowers coverage to ~80.4% | `v16_uncertainty_simulation_dev1` |
| Source tests | 81 pass, including real-shaped chronological reports, finite/variance pipeline interrupt/resume, direct/averaged ledgers and commit guards | `v16_development/logs/foundation_tests_24.log` |

The bridge uses explicitly partial diagnostic snapshots/identity adjusted
normalizers and **does not train a model**. It checks input/scoring equivalence;
it cannot substitute for full-history pilots. All original v13–v15 producer
hashes were checked unchanged (102 unique files across their manifests), as
were the active historical preparation's frozen producers.

## Automated acceptance, then the requested commit

At the interactive checkpoint, full historical capability preparation was
still running: 254 dates × eight bank/family chains, with annual tuning and
32 joint draws. Full history is necessary for each training row's own dated
features; the two audited origin snapshots are not a shortcut.

`v16_prelaunch2` automatically waits for that library, runs the prescribed
44 one-epoch smoke cases and 48 full-stopping pilots, independently audits
them, and estimates RAM/disk/runtime before declaring preflight PASS. Pilots
are operational, not an accuracy tournament. The full 3,168-case run is a
separate launch action; the preparation supervisor has no production command.

Adam also requested a commit after readiness. A separate guarded continuation
commits only explicit reviewed paths after actual acceptance, requiring the
expected source hashes, unchanged baseline HEAD and empty index. It refuses
unexpected edits or failures; it never stages generated caches or resets user
work. Its actual SHA/status and verified commands are written to the new
prelaunch artifact directory. Do not infer completion from this static report.

Read `v16_prelaunch2/status.json`, `commit_status.json`, `commit_result.json`
and, after success, `READY_HANDOFF.md`. `logs/prelaunch.log` and the individual
stage/worker logs retain failures. The intentionally stopped `v16_prelaunch1`
remains preserved; it never started NN fits.

No model has earned a new predictive/coherence/uncertainty conclusion yet.
The next scientific task after Adam launches production is the complete fixed
comparison and three-pillar review, not an architecture change based on pilots.
