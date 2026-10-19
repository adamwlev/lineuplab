# V19 prelaunch checkpoint — downstream pilots and runtime risk

September 30, 2026. Follow-up to commit `32ab995d` and the
[native implementation checkpoint](joint_capability_v19_implementation.md).
This work is uncommitted. **The full campaign has not launched.** Adam's launch
approval remains recorded, subject to readiness and the frozen runtime protocol.

## Completed in this checkpoint

New modules, separate output namespaces, unchanged native pilots and frozen
producers. No scraping, database access, input rebuild, model promotion or
deployment. No delegated work.

| Component | Verified result |
| --- | --- |
| Reference and actual-context scorecards | Five pilot panels; 3,820 sufficient-statistic rows independently reproduced |
| Prior-only calibration | Environment and estimator-qualified histories; equally informed conditional controls; independent centered regression replay |
| Read-only case preview | Matches completed scorecards in all five panels; production refuses missing earlier calibration history |
| Exact context × sampled-opponent integration | All eligible broad cells; 512 opponents, 4,096 on the fixed first 20 lexicographic cells |
| Early average-opponent pilot | 187 cells, nine models, one seed; 154.65 seconds; 1.87 GiB peak process RSS |
| Late average-opponent pilot | 206 cells, six models, one seed; 51.61 seconds |
| Finite-game/persistent discrepancy outputs | Candidate-specific U0/U1; nominal 80/95; possession-weighted and unweighted summaries; original transfer registry |
| Uncertainty pilot | Both dates in 13.53 seconds; no invented histories; U1 correctly NOT_IDENTIFIED |
| Late basketball fixture batch | 21 registered fixtures plus three existing defensive references; 576 directed matchups/model, six models, 5.04 seconds |
| Fixture context curves | All 31 CLOCK states, including zero-weight support; MARGIN path tested on all 186 states; exact whole-ledger reference mixture |
| Downstream arithmetic audit | Preview, opponent means, uncertainty status, fixture mixtures and both-direction margins pass |
| Checkpoint-average conditional event audit | All seven cases replayed; independent numpy/scipy event rates agree within 3.59e-13 |
| One/three-worker training benchmark | Identical bounded workload: 40.52s sequential, 15.94s parallel; 2.542× throughput; weights exactly identical |
| Current v19 unit tests | 43 pass in 2.00 seconds; durable log below |

The uncertainty adapter reports broad, novel, thin, debut and the immutable
primary transfer cohort (146 cells / 47,419 possessions over the full history).
U1's paired-game eligibility remains narrower than broad U0; it must not be
presented as coverage of every lineup. Conditional residual variance is a
separate diagnostic and never supplies reference-model interval histories.

The actual fixture pilot is late C_CLOCK/C_FULL plus retained controls. C_FIXED,
C_ALLOC and C_MARGIN fixture paths have synthetic ledger/permutation tests, but
were not substituted into an unregistered late trained pilot. This is not a
completed three-seed or ten-date scientific coherence assessment.

## Pilot point readouts — not model selection

Each date is an **isolated one-seed calibration cold start**, including the
retained NN controls. Do not pool dates with different arm rosters, compare them
to fully prequential historical leaderboard numbers, select arms, or interpret
these few cells as confirmation of a new winner.

Reference half, original broad off5 >=50 population:

| Origin | Cells / possessions | C_CLOCK r² | C_FULL r² | J_POINT_BOTH r² | Additive defense r² |
| --- | --- | ---: | ---: | ---: | ---: |
| 2016q1 | 187 / 23,039 | .10822 | .10777 | .10868 | .04884 |
| 2026q4 | 206 / 24,528 | .11354 | .11388 | .10207 | .07276 |

Conditional CLOCK and conditional MARGIN have distinct panels and control
information sets. They use realized future game context and are **not** product
forecast leaderboards. Half blending there uses the correspondingly calibrated
context-aware additive arm, not the unconditioned baseline.

Opponent sensitivity: maximum absolute 512–4096 difference across the fixed
20-cell samples and models was .19537 direct / .14948 half points per100 early,
.08454 direct / .03458 half late. 4,096 is a convergence sensitivity, not exact
truth. Realized scores are not observed neutral-opponent counterfactual outcomes.

Prediction, basketball coherence and honest uncertainty retain equal standing.
No ranking was enforced, no known-pair chemistry introduced, and neither finite
game coverage nor context curves establish hypothetical latent-quality coverage.

## Runtime/storage warning

Native projection uses exact scheduled inner/final/outer row counts and the
maximum pilot-scaled cost for each arm, keeping its observed epoch counts.
It reuses all seven pilots without copying. This is an estimate, not an upper
confidence bound: future epoch choices and machine load may differ substantially.

| Remaining native workload | Estimated hours with three busy workers |
| --- | ---: |
| C_FIXED | 14.72 |
| C_CLOCK | 7.58 |
| C_FULL | 7.63 |
| C_ALLOC | 13.39 |
| C_MARGIN | 9.87 |
| Total, 713 new cases | **53.19** |
| 1.2× native stress | **63.82** |
| All cases at 96 inner +96 final epochs | 227.14; cap scenario, not expectation |

These times already derive from concurrent pilots. **Do not divide them again
by the measured 2.542× benchmark speedup.** Downstream work, scheduling barriers,
remaining control exports and complete verification are not included. Thus the
unoptimized campaign currently misses the <=48h reference / <=54h stress target
even before the all-in estimate is finished.

The bounded throughput benchmark used two epochs over twelve complete game
batches (48,955 late-origin matchup rows), C_CLOCK/C_FULL/C_MARGIN. It is not
another scientific fit or a replacement full-case runtime measurement. Every
child used the retention wrapper; exact weight parity also exercises that path.

Host readout: ten logical CPUs, eight performance cores, **16 GiB physical RAM**.
The earlier full-pilot individual peak was4.016GiB. A fourth full-size worker is
not justified merely by a small benchmark's memory footprint. Process RSS maxima
do not measure simultaneous physical RAM or memory pressure.

Latest physical free space: **66.11 GiB**. Existing native estimate: **47.26 GiB**
additional, leaving **8.85 GiB** after the required10GiB reserve for all remaining
derived/control/temporary outputs. The all-in storage check remains unfinished;
neither the old native-only failure nor current free space alone decides readiness.

### Exact optimization opportunity found, not yet implemented

The current inner epoch computes both actual-context validation and exact
reference-environment validation. Only actual-context validation determines
stopping/epoch selection. Timing all seven saved pilot models showed:

- Conditional selection statistics were exactly identical with and without the
  separate reference diagnostic; RNG state was unchanged.
- Early C_MARGIN validation: median7.261s for both views versus .612s for the
  selection view, saving6.649s per validation pass on one worker.
- Late CLOCK/FULL save about1.44/1.38s per pass.

Next engineering option: a **new versioned fitter**, retaining conditional
validation every epoch and full reference evaluation of selected/averaged final
models. Preserve original producer files and pilot artifacts. Prove trajectory,
selection and resume equivalence before using it. This profile alone does not
prove a full-run speedup or authorize omitting scientific reference analyses.
If exact optimization still misses the target, return an explicit runtime/scope
choice to Adam; do not silently remove seeds, arms or analyses.

## Preserved failures and numerical caveats

- `_v19_basketball_pilot1`: stopped exporting a numpy-valued context reference to
  JSON. Fixed serialization, added a test, used fresh `_v19_basketball_pilot2`.
  No completed output or native model was changed.
- `_v19_average_event_audit1`: an archival point comparison at1e-8 failed by
 4.62e-8 points/100. The second audit additionally compares the current original
  construction path against the new saved-model factory: outputs agree exactly.
  Across seven cases the maximum archived point discrepancy is1.0431e-7.
  All exported-field differences are below0.131of one float32 scale epsilon.
  The audit explicitly uses the same archival mixed-precision guard as the
  earlier control replay; the1e-8 float64 value/objective/gradient requirement is
  unchanged. Independent conditional event-rate errors are <=3.59e-13. The
  precise cause of the tiny archive/runtime drift is not established.

## Evidence and verified inspection commands

All new prefixes below begin
`experiments/cache/joint_capability_2026_09_30`:

- `_v19_pilot_scored1`: reference/conditional panels, per-case histories and metrics.
- `_v19_scoring_audit1`: independent point/calibration/source audit.
- `_v19_average_pilot1/{2016q1,2026q4}`: opponent integrations and sensitivities.
- `_v19_uncertainty_pilot1`: U0/U1, per-cell bands, transfer flags and conditional variance.
- `_v19_basketball_pilot2/2026q4`: fixture pairs, native ledgers, context curves/support, mirrors.
- `_v19_downstream_audit1`: independent arithmetic/status/preview checks.
- `_v19_average_event_audit2`: closes the remaining native event-audit gap.
- `_v19_parallel1`: six bounded training jobs, one/three-worker queues, exact weight parity.
- `_v19_validation_profile1`: unmodified saved-model validation timing comparison.
- `_v19_prelaunch_resources1`: per-case native projection and explicit readiness hold.

Each has a sibling `.log`, except average pilots use `_early.log` / `_late.log`,
and scoring preparation has its own `_prepare.log`. Tests:
`experiments/cache/v19_prelaunch_tests2.log`. All launched jobs at this checkpoint
are complete; no full train or background analysis remains active.

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v19_report report \
  --out experiments/cache/joint_capability_2026_09_30_v19_pilot_scored1 \
  --origin 2026q4 --environment reference --view half --sort r2 --slice all
```

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v19_case_preview \
  --scoring experiments/cache/joint_capability_2026_09_30_v19_pilot_scored1 \
  --origin 2026q4 --arm C_CLOCK
```

These are completed **pilot** inspection commands, not production launch commands.

## Remaining readiness work

1. Implement/test exact validation speedup in a new producer, then recompute the
   selected/stress budget. Do not invalidate frozen originals or infer all-in
   acceptance from native timing alone.
2. Finish event/conversion, observed role/transfer, two-big analogues, persistence/
   full covariance, high-support context curves and registered summary adapters.
   Existing point/uncertainty transfer labels are not the completed role analysis.
3. Measure the complete late-sized analysis bundle, total derived/control disk,
   temporary peaks and all-in reserve. Report memory-pressure limitations.
4. Integrate a frozen retention-aware full production launcher, chronological
   calibration barriers, verified seven-pilot reuse and all child jobs. Add
   production calibration parity checks against retained controls.
5. Verify launch/live-log/status/report/preview commands and launch only when
   readiness passes under Adam's recorded approval. If target scope/runtime still
   conflicts, resolve that choice before launching. No verified full command yet.
