# Joint capability v11 operational handoff

Completed and reviewed 2026-09-13. Read
`reports/joint_capability_v11_review.md` for scientific interpretation.

## State and provenance

- Frozen production prefix:
  `experiments/cache/joint_capability_2026_09_13_v11_prod_final/`
- Post-run interval-summary correction prefix:
  `experiments/cache/joint_capability_2026_09_13_v11_postrun/`
- Protocol: `SOL_JOINT_CAPABILITY_DAY5_PLAN.md`
- Production exit: 0; SUCCESS present; 96/96 reference-origins; 48 origins.
- Primary: 44 origins, 5,607 cells / 726,364 possessions per reference.
- Descriptive: 48 origins, 6,179 cells / 803,447 possessions per reference.
- 248,889,082 frozen forward lineup evaluations; 916.037 summed origin seconds.
- K counts: 256 at 25 cells, 512 at 25, 1024 at 46; 13 limited flags.
- Zero optimizer fits, zero epochs, no new calibration fit, no scorer promotion.
- No scraper, network fetch, database access/mutation, cache rebuild or deployment.

Independent verification is in
`reports/joint_capability_v11_verification.log`: 96 receipts, six source hashes,
five frozen code hashes, 290 full gzip/CRC reads, exact decomposition and HALF
identities. Production log and command/exit/PID receipts live under the source
prefix's `logs/` directory. Nothing is running.

## Result

VALUE_SWAP fails its registered recurring-RMSE contrast versus HALF:
+.00538 [-.02784,+.03860] for EXPOSURE and +.01675 [-.02290,+.05641] for
UNIFORM. CONTEXT_RELEASE is tied overall and modestly improves novel RMSE under
EXPOSURE (-.00720 [-.01352,-.00089], 8/11 seasons), but its extracted interaction
is basketball-incoherent as a transferable mechanism: +4.77 for five Goberts,
+1.66 for limited centers and -7.57 for five Jokics. No arm is promoted.

The completed source's original interval summary has an object-boolean reduction
bug; it prints near-zero coverage. Row forecasts and interval radii are valid.
The source is preserved untouched. Use
`experiments/cache/joint_capability_2026_09_13_v11_postrun/corrected_interval_summary.csv`.
The correction's manifest hashes its input and states its limited scope.

## Verification and tests

- Pre-run focused suite: 6/6 passed.
- Post-run focused suite: 7/7 passed.
- Report smoke and production preflight passed.
- The final full suite ran 750 tests in 34.584 seconds: 749 pass and one fails,
  solely because the four new v11/postrun Python producers are untracked. Day5
  prohibited staging and commits. Re-run after staging only if Adam authorizes
  a commit; do not alter tests to suppress the reproducibility guard.

Durable logs:

- `reports/joint_capability_v11_pilot_final.log`
- `reports/joint_capability_v11_preflight.log`
- `reports/joint_capability_v11_test_suite.log`
- `reports/joint_capability_v11_report_smoke.log`
- `reports/joint_capability_v11_postrun.log`
- `reports/joint_capability_v11_postrun_tests.log`
- `reports/joint_capability_v11_verification.log`
- `reports/joint_capability_v11_final_test_suite.log`

## Remaining work

Discuss and pre-register, but do not silently launch, a jointly adapted
additive-plus-identity-free-context residual model. The residual must be trained
against the combined value surface and constrained from relearning player value.
This directly answers the limitation Adam identified before v11. Actual-opponent
defense remains the strongest separate product workstream. Latent-mean OOD
uncertainty remains incomplete.

No commit, staging or cleanup was authorized. Multiple incomplete/superseded
pilot/preflight prefixes created during implementation remain untracked and
preserved. `git status --short` is authoritative for the complete change list.
