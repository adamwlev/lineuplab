# v16 implementation checkpoint — 2026-09-18

**In progress, not launch acceptance or a v16 model result.** The unchanged
[design v1](../JOINT_CAPABILITY_V16_PLAN.md) remains the experiment authority.
Codex implements directly. No delegation, database access, old-cache rebuild,
production launch, promotion, deployment or commit was performed.

## Implemented so far

- Declarative 22-arm registry, prescribed 48 operational pilots and 3,168-case
  production schedule; this is not yet a runnable training lifecycle.
- Four actor/teammate/defender GLM likelihoods, constrained canonical fitting,
  dated league offsets, strict fit cutoffs, independent held-out likelihoods,
  paired game-bootstrap one-SE penalty-selection primitive, and joint
  constrained-Hessian draws.
- Qualified actor/opponent phase labels and exact possession/matchup/team
  orientation from the immutable local archive.
- All 14 archived point controls, exact broader/legacy populations, additional
  common prior-completed broad-cohort affine calibration, and actual two-team
  game margins rather than pooling the two offenses.
- Nested shifted base-two opponent quadrature, checked against **exact**
  prior-weighted enumeration using all four v15 arms, three seeds and the fixed
  fixture panel at 2016q4, 2021q4, 2025q4 and 2026q4.
- All 22 neural forward paths: supported joint offense, frozen unsupported
  parent outputs, adjusted-input slots, raw/adjusted defense, rank-8 cross,
  typed two-sided attention, capacity-matched pooling, hierarchical allocation,
  tied/separate two-phase renewal. No new NN fitting has occurred.
- Common aggregate/qualified-phase loss primitives, game×off5 pooled point
  auxiliary, and accounting-preserving checkpoint prediction averaging.

Real-checkpoint replay also completed: **88 forward checks** (all 22 arms,
inner/final parents at both early/late cutoffs). Every nested arm matched its
correct dated parent within 1e-4 pts/100, with finite gradients and conserved
usage. J_ADJ_CONTEXT's deliberately nonnested initial differences are saved,
not silently excused as numerical error. Output:
`experiments/cache/joint_capability_2026_09_18_v16_replay_dev2` (current code).
The worst nested point difference was .0000302 pts/100. The earlier dev1
replay is preserved; dev2 follows the WIDE capacity-control correction below.
These checks use zero new heads/adjusted slots and do not substitute for the
dated feature library, NN training pilots or counterfactual acceptance.

## Empirical preparation results

### Controls, not new v16 forecasts

Output: `experiments/cache/joint_capability_2026_09_18_v16_controls_dev1`.
The 48-origin, three-seed replay completed in 88 seconds after input verification.
All primary populations reconcile exactly:

| Population, 2016–2026 | Cells/rows | Possessions |
| --- | ---: | ---: |
| Legacy primary | 5,607 | 726,364 |
| Broad offensive five >=50 | 8,345 | 1,013,999 |
| All matchup groups | 718,526 | 2,760,546 |
| Offensive five <50 | 212,036 | 1,746,547 |
| Defensive five >=50 | 8,340 | 1,010,779 |
| Ten-player unit >=50 | 453 | 32,664 |
| Team-game offense | 28,314 | 2,760,546 |

There are also 14,157 true two-direction game-margin observations. That table
uses **points per game, equal game weights**, conditional on realized rotations
and possession counts; it is not an unconditional rotation forecast.

The archived-inherited view reproduces the original legacy RMSEs exactly.
Under v16's *additional* common prior-only affine procedure:

| Starting control | Legacy RMSE | Legacy r² | Broad RMSE | Broad r² |
| --- | ---: | ---: | ---: | ---: |
| Additive + defense | 10.757068 | .133998 | 11.165936 | .146023 |
| Old HALF + defense | 10.708648 | .141776 | 11.096562 | .156601 |
| v15 MAIN_RB half | 10.718376 | .140216 | 11.110428 | .154492 |

This is a calibration/population foundation, not a new model gain. The older
ensemble remains the important comparator. Controls retain their inherited
calibration paths; new NNs will enter this same additional procedure at native
event-accounted points. Do not label their entire training histories identical.

### Qualified phases

Accepted output: `experiments/cache/joint_capability_2026_09_18_v16_phase_dev2`.
It contains 4,846,590 qualified possessions out of 6,059,380 and 440,850 renewal
entries. FGA, FTA, TO, located attempts/makes and eligible recovery reconcile
**exactly** to independent original labels on the accepted possession mask.
Repeated offensive recoveries each add an entry to phase 1. All unqualified
possessions remain in the original aggregate objective.

The first development output, `..._v16_phase_dev1`, is preserved, **not accepted
for phase training**. Its overly broad exclusion of FT-rebound records retained
almost exclusively made FTs (initial phase: 425,774 makes / 430,316 attempts).
That was a label-selection failure, found before NN fitting. The corrected
parser recognizes numbered nonfinal-FT dead-ball team boards and terminal
defensive boards after a final FT. Neither is an eligible FG renewal. It still
rejects unresolved offensive FT recoveries, floor changes, unknown actors,
ambiguous restarts and incomplete sequences. Corrected initial-phase FT totals
are 518,979 / 664,332 (78.1%); phase-1 totals are 48,409 / 65,250 (74.2%).

Whole-possession qualification is still selective; it is not a missing-at-random
claim. TIED and PHASE get the identical extra supervision, and aggregate
training stays complete. These masks must be frozen and reported by cohort
before the neural pilots. Phase-entry exposure and the .44 usage convention
remain an approximation, not an exact FT-sequence simulator.

The control replay uses dev1's independently verified **orientation alignment**,
not its rejected phase labels. The phase-qualification correction does not
change possession keys, opponents, points, counts or team orientation.

### Opponent integration

Output: `experiments/cache/joint_capability_2026_09_18_v16_integration_dev1`.
All 252 fixture/model/seed cases completed, each against exact summation over
the finite prior defensive-five distribution. Eight fixed shifts were checked
at each nested resolution; errors below are maximum across shifts and cases.

| Reference sample size | Worst native error, pts/100 | Worst inherited-calibrated error |
| ---: | ---: | ---: |
| 128 | .499979 | .376099 |
| 256 | .308056 | .237503 |
| 512 | .312805 | .239001 |
| 1,024 | .229745 | .175539 |
| 2,048 | .097715 | .074081 |
| 4,096 | .054880 | .041771 |

Thus 4,096 passes the registered .10 threshold for **these archived models and
fixtures**. New v16 fixtures must be checked independently and use exact fallback
where required. The bounded 512-reference broad average-mode task is approximate;
its mandatory 4,096-reference sensitivity remains important. Conditional actual-
opponent point accuracy is unaffected by this quadrature approximation.

### Adjusted-profile feasibility

The fixed-lambda diagnostic **completed** in
`experiments/cache/joint_capability_2026_09_18_v16_profile_dev2`.
It fitted all four families at 2016q1 and 2026q4 in each bank, replayed serialized
coefficients and obtained 32 joint curvature draws per fit: **16 fits and 512
joint draws**. These are **not**
the annual penalty-selected monthly feature library or the 48 NN pilots.

All 16 fits improved held-out family likelihood against their dated league-only
baseline at these two cutoffs. That is a weak
baseline, **not** proof of improvement over existing raw profiles or additive
points. The matched-timescale raw-profile comparison is still required.

| Bank / family | Early NLL difference vs league | Late NLL difference vs league |
| --- | ---: | ---: |
| Offense / counts | -.00138744 | -.00240380 |
| Offense / location | -.02478964 | -.03643950 |
| Offense / conversion | -.00108209 | -.00151022 |
| Offense / recovery | -.00577089 | -.00904899 |
| Defense / counts | -.00203588 | -.00292414 |
| Defense / location | -.04218239 | -.04610765 |
| Defense / conversion | -.00099028 | -.00115469 |
| Defense / recovery | -.01097784 | -.01303277 |

Each entry uses its family's opportunity denominator; magnitudes are not
comparable across likelihood families. Counts use actor/channel exposures.
Maximum projected gradient was 1.94e-9 (registered tolerance 1e-5); maximum
exposure-weighted gauge error was 1.66e-17. Total wall time was 2,578 seconds
(43 minutes), of which fitted optimization took 338 seconds. Peak reported
process memory was 2.19 GiB. Most preparation time was spent on covariance
draws, not coefficient fitting. This is not a full-library runtime estimate:
annual selection and monthly histories have not yet been executed.

The first diagnostic, `..._v16_profile_dev1`, is preserved as a failed numerical
check: L-BFGS stopped on likelihood precision at a projected gradient of
2.2e-4, above the registered 1e-5 requirement. A same-objective constrained
Newton-CG refinement now satisfies that criterion without relaxing it. The
500 nonlinear-iteration cap includes refinement steps; linear-system residuals
are separately checked. Fit/replay tests never accept the optimizer's success
code alone.

An optional constrained Jacobi preconditioner was then benchmarked on the
four completed late offensive-bank fits, two right-hand sides each:
`experiments/cache/joint_capability_2026_09_18_v16_curvature_dev1`.
Linear solves were approximately 1.2–1.8 times faster, with relative solution
differences below 7.1e-9. This solves the **same full Hessian system**; its
diagonal is not substituted for the covariance, and no prior, ridge, draw count
or convergence tolerance changed. It is not yet wired into joint-draw export.
That improvement alone does not settle full-library cost; batched solves or
other same-system optimizations may still be worthwhile before preparation.

## Implementation choices to freeze before pilots

- The canonical gauge uses summed decayed family opportunity exposure per
  player/block, shared across outputs in that family; location also removes
  its class gauge. Ridge is on orthonormal canonical coordinates. Validation
  uses the *training* coefficients/gauge and an origin-frozen league baseline.
- A snapshot library has **not yet been built**. It must cover every historical
  row's own date, not substitute the audited outer-cutoff coefficients into
  earlier NN training rows. Annual penalty choices, monthly/as-of snapshots,
  per-coordinate opportunity support and covariance exports remain to wire.
- Reserved adjusted schema: 97 offensive coordinates (own + influence
  coefficients, log opportunities and log curvature standard deviations,
  plus staleness); 49 defensive coordinates. Bank masks are applied after
  normalization. Centered `g(z)-g(0)` paths cannot turn a disabled bank into
  an added intercept. The exporter/normalizers still need implementation.
- Attention: two typed five-player sets, width32, four heads, two residual
  blocks with width64 tanh feed-forwards and no positional encoding. Direct
  own-token messages are masked; two-hop return paths remain ordinary graph
  propagation. WIDE uses the identical typed input projections and a width99
  pooled head, chosen **only** by parameter count: 23,779 versus attention's
  23,856. Active RAW counts are 19,107 versus 19,184; both differences are under
  0.5%. The first local draft matched nominal counts but fed raw concatenated
  inputs directly into WIDE, giving it many more inactive zero-bank columns.
  That was a capacity-control confound, corrected before any NN fits. The
  same width and reserved schema now work for RAW and BOTH.
- Supported offensive event channels and recovery train jointly. FT% and
  assisted-fraction outputs use a separate frozen parent path; assist supply
  remains the dated raw own-skill input. Changing shared hidden weights cannot
  silently train unsupported outputs. The nonnested J_ADJ_CONTEXT removal is
  applied to its frozen assisted-context path too, with its initial change to
  be disclosed. It retains own receiver/style/recent-role information.
- The existing defensive adapter remains after the offensive constraint path,
  preserving the F_DEF/v15 freeze comparison. New own/teammate/attention and
  phase event residuals enter before the creation/load constraints. No point
  residual or hidden additive mixture is introduced.
- New adjusted, attention, allocation and phase corrections use bounded tanh
  residuals. All new output heads start at zero. Complete expected events—not
  independent channel probabilities—are mixed for checkpoint averages.
- Parameter reports distinguish nominal, trainable, enabled-module and
  structurally active coordinates. The last excludes disabled banks, masked
  input columns, unsupported decoder outputs and exactly canceled biases; it
  is not a claim about the network's functional rank or gradient at an optimum.

## Remaining before a launch command

1. Extend the completed profile feasibility and real-parent replay work with
   matched-timescale raw-vs-adjusted comparisons, per-coordinate support
   diagnostics and full-library cost estimates.
2. Implement the strictly dated reusable capability library, annual tuning,
   matched raw references, normalizers, shared-player covariance queries and
   deterministic cold/stale behavior. No shortcut assigning future-fitted
   capabilities back to training rows.
3. Wire verified parent initialization, shared prefix loss references, training,
   stopping/fresh final optimization, checkpoint retention and exact resume.
4. Implement complete fixed fixtures, non-NN adjusted-channel scoring,
   U0/U1/U2, expanded novelty/support cohorts and statistical analyses.
5. Implement the lifecycle CLI, live scorecards, independent auditor and durable
   one-command post-fit completion. Freeze its manifest, complete all-arm smoke
   and the prescribed 48 full-stopping operational pilots.
6. Measure complete runtime/storage and pass preflight, then provide verified
   background-launch, live-log, status and leaderboard commands. **Do not launch
   production without Adam's separate request.**

No scorer or three-pillar conclusion changes at this implementation checkpoint.

## Verification and development-only limitations

All **40 v16 tests** pass (`v16_development/logs/foundation_tests_07.log`).
The frozen-producer audit verified all **256** source hashes from v13/v14/v15.
All bounded preparation jobs have completed; no neural campaign is running.

These preparation CLIs are not the final immutable run lifecycle. Before reuse
in that lifecycle, fix the profile audit's missing root completion guard and
the phase builder's redundant manifest write on completed reuse. Do not rerun a
completed development directory to inspect it: read its receipts and reports.
The protocol dictionary also needs JSON-normalized tuple fields before a
round-tripped manifest comparison. None of those behaviors changes the completed
scientific outputs above; they are explicit pre-freeze integration work.
