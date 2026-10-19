# Quarterly point runner — checkpoint 2026-09-07

**Superseded by the completed experiment and correction, 2026-09-08.** Adam's
run completed all48 origins. The offensive-reference bug and full saved-fit
correction are documented in `ASOF_ADDITIVE_REFERENCE_FIX.md` and
`ASOF_ADDITIVE_REFERENCE_RESULTS.md`. Corrected run and high-exposure review
are complete, 530 tests pass, no jobs remain. The original apparent structural
advantage must not be reported as valid. Read the RESULTS document and latest
handoff before launching anything. The warmup/self-run notes below are historical.

The runner is implemented and the two registered real warmup origins are
complete. The prior full suite passed 515 tests; the new live launcher passes
seven additional focused tests and a saved-artifact preview. **No workers or
model jobs were started for the launcher handoff.**
This establishes working point-level integration and restart behavior, not
predictive improvement or a new contextual mechanism. No primary 2016–2026
origin has been evaluated yet. Scorer, page, source caches and database are
unchanged; the three co-equal model standards remain intact.

## Read and resume

`ASOF_POINT_BENCHMARK.md` is the preregistration and is now an **immutable
input to the saved run**. Do not append results to it: its content hash is
pinned, so even an explanatory edit would refuse resume. Record status here
and in `SESSION_HANDOFF.md`. Do not change computational modules between
origins without explicitly dealing with the resulting protocol mismatch.

New output: `experiments/cache/asof_points_2026/`. Its root manifest is
`paused`, with completed origins `[2015q1, 2015q2]`. Each origin has all 5,760
candidate losses, a hashed additive coefficient snapshot, selection metadata,
50-arm cell forecasts, complete player/channel ledgers, both calibrations and
a completion receipt. Fit checkpoints commit before point scoring. Completed
files are verified and reused, not silently overwritten or refitted.

**Latest user direction:** Adam wants the full remaining predictive experiment,
not another small batch, and will launch it himself to avoid assistant usage
while it computes. This supersedes the earlier proposed three-origin batch;
it does not change the scientific protocol or select parameters from results.
Carry numerical warnings into the readout rather than treating another audit
as a prerequisite to running the study. Stop on genuine correctness failures.

The separate `experiments/asof_point_run.py` launcher runs all remaining origins
in one invocation, with a six-hour whole-run safety cap and checkpoint resume.
It does not modify the pinned fitting/scoring modules or invalidate saved fits.
After each completed origin it prints fixed additive/structural/control rows,
possession-weighted MAE, RMSE, bias, correlation, raw r² and differences versus
additive. Cumulative comparisons exclude the 2015 warmup and are labeled partial
until complete. Original tuning warnings remain visible. All 50 arms are saved;
the live table shows nine preselected rows, not the best-looking arm.

Run from Terminal:

```bash
cd /Users/adam/Documents/basketball
nohup /usr/bin/caffeinate -i \
  /Users/adam/miniconda3/envs/basketball25/bin/python -u \
  -m experiments.asof_point_run \
  >> experiments/cache/asof_points_2026/progress.log 2>&1 < /dev/null &
```

Watch the saved live log:

```bash
tail -f /Users/adam/Documents/basketball/experiments/cache/asof_points_2026/progress.log
```

The launch command has NOT been run by the assistant. Ctrl-C on `tail` stops
watching, not computation. Keep the Mac on with its lid open. Do not start
duplicate copies or edit model code/refresh source data during the run. If
interrupted, the same command resumes verified checkpoints. On return, inspect
the manifest and log before starting anything; Adam may have completed the run.
Final CSV reports are under `experiments/cache/asof_points_2026/reports/`.

Never remove `--resume` or overwrite the existing directory.
Missing/corrupt/mismatched inputs stop explicitly. The ignored local
`fit.pkl` snapshots are required for fit-only recovery; all other receipts and
CSVs are inspectable. The empty `.lock` is runtime state, not a research result
to stage in a later commit. Nothing was committed or pushed this continuation.

## Completed runtime and accounting check

| Origin | Forecast cutoff | Cells | Possessions | Whole invocation |
|---|---|---:|---:|---:|
| 2015 Q1 | 2014-10-28 | 139 | 19,151 | 61.59 seconds |
| 2015 Q2 | 2014-12-08 | 128 | 17,229 | 65.01 seconds |

Both invocations were capped at 450 seconds. Total: **267 cells / 36,380
possessions**, all retained across all 50 arms, all additive slots supported.
These are warmup cells, not independent factorial experiments or the primary
5,607-cell population. All eight Q1 artifacts stayed byte-identical after Q2
resume; Q1 fitting was not called a second time.

Q1 has no prior point-calibration cells and correctly uses the disclosed raw
identity calibration. Q2 uses exactly **139 prior cells / 19,151 possessions**
for every arm. Each opportunity stream uses its own completed prior forecasts;
the comparison never borrows live offsets for frozen profiles. The shared
league level enters each forecast exactly once. Q1 raw frozen/live profiles
agree; later-year final calibrated Q1 predictions need not agree because
cadence policies have distinct historical calibration inputs.

Maximum source/accounting discrepancies: Q1 **1.14e-13**, Q2 **9.95e-14** in
their stated per100 units. Independent saved-prediction reconstruction errors
are **4.27e-14** and **2.85e-14 points/100**. No row was dropped for these checks.

## Additive numerical audit, unchanged selection policy

Q1: career=10,000, prior=1,000,000, experience=1, delta=10,000,
rho=0.09085073215189737. Its experience penalty is on the low finite edge.
Adjacent grid changes are **0.000576908 / 0.000057735 pts/100**, both below the
registered 0.001 threshold. The original audit nonetheless remains
**provisional**, because its rule also requires no finite boundary. Do not
rename it converged or extrapolate the separate 2026 Q3 sensitivity to it.

Q2: career=10,000, prior=1,000,000, experience=1,000,000, delta=10,000,
rho=1. No finite boundary; both adjacent prediction changes are zero.
Its original audit is **stable / not provisional**.

The first two origins show no material grid-expansion instability under the
registered diagnostic; Q1 retains its finite-edge warning. A subsequent
material boundary would need its own validation-only follow-up before claiming
an adequately tuned full comparison. No test outcome changes any penalty or
bandwidth choice. Reports include the original flags and affected exposures.

## Verification and lead review

The read-only real preflight reproduces all 48 source windows, plus four 2014
inner-validation windows. The source Q1 profile CSV was only a Q1-query extract:
complete preseason snapshots were reconstructed from existing cached history,
preserving later-quarter players. Independent 2015 frozen reproduction retained
all 572 season cells per bandwidth, maximum channel discrepancy 1.43e-14/100.
No source profile/cache was overwritten.

The independent final audit rechecks source/code/epoch hashes; all artifact
hashes; direct raw point aggregation from possession rows; the common cohort;
additive player coefficients read directly from snapshots; structural player
sum plus one intercept; full point-calibration arithmetic; and prior-only
history counts, dates and constrained-WLS optimality conditions. All pass.

Opus's first task wrote four authorized code/test files but hit its 45-turn
cap; the second saved partial runner corrections and hit its 35-turn cap.
Neither had permission denials, extra agents or git mutations. Lead reviewed
actual diffs, finished integration and added regression coverage. Important
repairs included actual gzip bytes, cold-start validation, genuine prior-date
test fixtures, all source input hashes, whole-invocation timing, public-call
locking, closed checkpoint file sets, metadata/fingerprint checks, exact shared
histories and partial-study reporting. Neither worker performed real fits.

Code: `experiments/asof_point_benchmark.py`,
`experiments/asof_point_calibration.py`; their corresponding tests. Existing
fitting, allocation and opportunity estimators are unchanged.

Private verification logs (do not publish worker snapshots):

- `/private/tmp/basketball-quarter-point-full-tests.log` — 515 pass / 30.65s.
- `/private/tmp/basketball-quarter-point-preflight.log`.
- `/private/tmp/basketball-quarter-point-2015q1.log` and `-2015q2.log`.
- `/private/tmp/basketball-quarter-point-independent-audit.py` and `.log` — PASS.
- Worker audit root: `/var/folders/0q/vr0lp8p56s7ddsz7k2d30j100000gn/T/opus-worker-501/`;
  runs `run-nlnkz12h` and `run-lkrhfzhq`.

The user's approval for relevant task/code sharing with Anthropic via the
Claude subscription remains recorded in the handoff. No API fallback was used.

## Still owed

The full quarterly apples-to-apples point comparison; revisiting high-exposure
disagreements under fresher profiles and era controls; named counterfactual
checks under this construction; context-dependent role adaptation; full matchup
defense; and honest latent/OOD uncertainty. Warmup execution does not settle
any of those scientific/product questions.
