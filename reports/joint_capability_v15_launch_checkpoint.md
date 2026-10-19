# v15 opponent-aware experiment — launch checkpoint

2026-09-17. **Launch-ready. Production preflight passed; zero production
training cases launched.** No process is still training. Adam launches the
full campaign with the command below when ready.

## What will train

Four defensive adapters, three matched seeds,48quarter origins:576cases,
each with inner selection and a fresh final fit. The offensive/rebound
RB_RENEW_FAC checkpoints are frozen and reused, not refitted. There are no
player-ID or named-pair parameters in the new adapters.

| Arm | Difference |
| --- | --- |
| D_MAIN | Pooled opposing-player capabilities affect action rates, shot locations and conversion. |
| D_CROSS | Adds attacker-capability-dependent response to that defense. |
| D_MAIN_RB | D_MAIN plus defensive rebound competition in possession renewal. |
| D_CROSS_RB | Both additions. |

The defense never changes a shooter's FT-conversion probability. Every model
still conserves its opportunity budget and recomputes rebound renewal from
its changed attempts/misses. No new game-state input is needed in the product.
The full protocol is `JOINT_CAPABILITY_V15_EXPERIMENT.md`.

## Data and comparisons

New prefix `experiments/cache/joint_capability_2026_09_17_v15_inputs`:
1,592,743ten-player game groups,6,059,380possessions,2,216,895eligible FG
recoveries,668,380dated game-player defensive states. All parent-label rollups
are exact. Independent prefix reconstruction at2016q1 and2026q4 matches all
19features exactly for23sampled players each; cold entrants receive the same
dated league prior and zero history. Profiles include own event rates and
allowed-on-floor rates; they are descriptive and confounded, not identified
individual defensive effects. In particular committed-foul rate uses the
cached total committed-foul count, not a newly reconstructed defensive-only
foul label. We do not claim substitution-level floor truth has been rebuilt.

The primary scorecard remains the same5,607offensive-quarter cells and726,364
possessions. Finer defensive-five/ten-player and complete-game comparisons
are separately named. Actual opponents and their exposure mix are additional
conditioning information; these are not generic unknown-schedule forecasts.

Already completed **control replay**, primary population, NNseed17 only:

| Control | RMSE | r² |
| --- | ---: | ---: |
| Additive offense |10.840994|.120432|
| Additive + shared defensive control |10.786989|.129173|
| Frozen NN offense |10.809132|.125595|
| Frozen NN + same defensive control |10.754040|.134485|
| Frozen HALF |10.782881|.129837|
| Frozen HALF + same defensive control |10.728119|.138653|

These are controls, not new NN wins or promotion decisions. The final campaign
uses matched three-seed means, including the frozen-NN controls. The shared
defensive slope is fitted only from earlier completed A-residual cells and
uses strictly prior centering; no evaluation-window centering or future ratings.
New adapters retain their registered own prior-window point calibration.
The raw shared-D controls preserve their original offensive calibration; they
are not a claim that every possible joint A+D recalibration has been exhausted.
Inspect calibration/bias as well as ranking when judging small point gains.

## Stopping and information boundaries

Maximum96inner epochs, patience8, minimum meaningful improvement1e-5;
selected checkpoint is the actual minimum validation-loss epoch. Final fits
start fresh and run exactly that selected count. The outer evaluation is
never the stopping set. The inner offensive backbone and defensive profiles
also predate validation, so freezing the backbone does not introduce leakage.

Examples:

- 2016q1: validation2015q4,2015-03-05 through2015-06-16; outer evaluation starts
2015-10-27. Inner fit stops before2015-03-05, final before2015-10-27.
- 2026q4: validation2026q3,2026-01-15 through2026-03-01; outer evaluation starts
2026-03-02. Inner fit stops before2026-01-15, final before2026-03-02.

2015is calibration warmup, not part of the primary scorecard. Each log prints
every epoch, selected epoch, per-origin additive/NN/opponent-aware/blend metrics,
and matched cumulative comparisons. Warmup-only status is explicitly labeled,
not displayed as an all-zero/NaN primary leaderboard.

## Pilot and operational evidence

The first eight pilots completed in602seconds, all96-epoch-cap schedules
allowed to stop normally: all four2016q1fits selected epoch12 (20inner epochs),
all four2026q4fits selected epoch4 (12inner epochs). None hit the cap. Their
point-calibration history contains only isolated pilot quarters, so their point
rankings are **not** the campaign comparison; in particular the apparent later
quarter bias must not be read as a complete prequential result.

The patched runner repeated these pilots under a fresh prefix. Only operational
changes were made: avoid empty primary warmup readouts, and resume fixture
generation if interruption occurs after the last fit. The old producer versions
are archived in `...v15_prelaunch_producers`; first-pilot artifacts are intact.
Training/model/input/protocol code did not change. No design was selected or
retuned from pilot outcomes.

Final verification:

- All eight repeat pilots completed in534seconds at
  `experiments/cache/joint_capability_2026_09_17_v15_pilot_final`.
- All16inner/final fitted parameter dictionaries are **bit-identical** to
  the first pilots; selected epochs are unchanged.
- 46focused tests pass, including exact epoch resume, warmup-only display and
  recovery of missing fixture reports after fits complete.
- Independent audit verifies all54pilot scorecards, fit/source receipts,
  selected minima, fixed final epoch counts, strict dates, shared defensive
  corrections and prior-only calibration/bands. Receipt:
  `experiments/cache/joint_capability_2026_09_17_v15_independent_acceptance.json`;
  log `/tmp/basketball-v15-independent-launch-audit-2026-09-17.log`.
- Pilot acceptance passed and production preflight verified all288saved
  parent inner/final checkpoints across48origins and3seeds, plus their
  control cells/calibrations. Production status is`NOT_STARTED`.
- All90v14producer and38input hashes remain unchanged. Original run outputs
  and the first pilot/failed diagnostic prefixes are preserved.

Estimate **10–15hours**, possibly longer if other quarters select many more
epochs; the ceiling is96, not the pilots'4/12selected epochs. Allow15–20GiB
headroom. The eight-case pilot is62MiB and the new shared inputs81MiB;
rough linear campaign storage is several GiB, with conservative headroom for
longer training. The machine had195GiB free at verification.

The first pilots' maximum zero-adapter replay and permutation discrepancies
were3.815e-5points/100 (float32 arithmetic); FT-conversion change was exactly0.
612two-lineup/reference probes were produced for2026q4.128vs256prior-opponent
marginalization differed by at most.169raw points/100 in that panel. This is
quadrature sensitivity, not uncertainty about true lineup strength.

Basketball coherence is **not solved**: in these pilots CROSS versions still
put five Goberts above the conventional high-exposure five on raw offense.
Defensive functionality does not excuse this. Latent/OOD uncertainty also
remains unvalidated; the automatic outputs separate finite-game residual bands
and seed disagreement from that unmet standard. No scorer is being promoted.

See `reports/joint_capability_v15_companion_review.md` for the bounded Cleveland
action-allocation and persistent-error diagnoses completed alongside this build.

## Launch and monitoring (use after final acceptance)

Run from the repository root. No surrounding quotation marks around commands.
Production preflight creates the log directory before the background launch.

```bash
cd /Users/adam/Documents/basketball
nohup /usr/bin/caffeinate -i bash experiments/run_joint_capability_v15.sh run --run-dir experiments/cache/joint_capability_2026_09_17_v15_prod >> experiments/cache/joint_capability_2026_09_17_v15_prod/logs/launcher.log 2>&1 < /dev/null &
echo "Launcher PID: $!"
```

Live durable log:

```bash
tail -F /Users/adam/Documents/basketball/experiments/cache/joint_capability_2026_09_17_v15_prod/logs/train.log
```

Status and leaderboard, from the repository root:

```bash
bash experiments/run_joint_capability_v15.sh status --run-dir experiments/cache/joint_capability_2026_09_17_v15_prod
bash experiments/run_joint_capability_v15.sh report --run-dir experiments/cache/joint_capability_2026_09_17_v15_prod --sort rmse --slice all
```

`--slice novel` or `recurring`; `--sort mae`, `raw_r2`, or `corr` also work.
The report command is read-only. Do not start a second process on this prefix;
the runner enforces an exclusive lock. To resume after a real interruption,
use the same launch command: optimizer/RNG checkpoints and verified completed
fits are reused. Producers/input changes are rejected, not silently mixed.

## Automatic outputs and follow-up

Per-case inner/final weights/curves, provenance, event/point ledgers,
matched offensive cells, all matchup-group forecasts and mechanism checks;
per-origin fixed basketball matchup/reference panels; design-level scorecards,
novel/recurring slices, season contrasts, finite-game intervals/coverage,
event readouts and defensive-five/ten-player/game populations.

After the full run, independently inspect receipts, exact populations,
additive-defense versus profile-defense versus cross-response, defensive
recovery, calibrated/raw/event differences, seed consistency, repeated/transfer
cases and support/coherence limits. Historical seasons have been inspected many
times: small improvements are research evidence, not fresh confirmatory proof.
No scraping, DB writes, existing-cache rebuild, deployment, promotion or commit.
