# v16 runtime and dated-library checkpoint — 2026-09-18

**Implementation progress, not launch acceptance or a predictive v16 result.**
The [22-arm design](../docs/history/JOINT_CAPABILITY_V16_PLAN.md) is unchanged. The
[foundation checkpoint](joint_capability_v16_implementation_notes.md) records
the earlier phase labels, control replay and forward/integration checks.
The [handoff](../docs/history/SESSION_HANDOFF.md) owns current process state and restart order.

## Operational addendum: three CPU workers

Adam explicitly asked to explore three simultaneous training processes on
2026-09-18. This supersedes the plan's **operational** single-process default,
not its scientific design. No agents, GPU migration, smaller data, fewer seeds,
different losses, penalty floors or result-dependent elimination are involved.

Machine: MacBookPro18,3, eight performance plus two efficiency cores, 16 GiB
RAM; approximately 185 GiB disk free after these diagnostics. Each worker uses
one PyTorch/BLAS thread. Three is the launch target, pending adjusted-library
memory and the full-stopping operational pilots.

### Measured throughput, not a whole-campaign estimate

Both checks compare the same six jobs: three repeats each of J_RAW and
J_ALL_RAW, seed17. They have **no validation, outer forecasts or accuracy-based
selection**. Timing checkpoints are explicitly nonreusable as campaign fits.

| Workload | One worker | Two workers | Three workers | Three-worker speedup |
| --- | ---: | ---: | ---: | ---: |
| Four real game-complete batches, 24 fixed steps/job | 84.20 s | 51.02 s | 37.26 s | 2.26× |
| Full five-year prefix, one fixed epoch/job | 323.99 s | Not repeated | 141.81 s | 2.28× |

Every corresponding final parameter is **exactly identical** across schedules.
The full-prefix experiment uses 346,149 matchup rows / 1,337,350 possessions
strictly before 2026q4. Complete-prefix reference preparation took 18.45 seconds
once, outside the timed six-job queues. Shared references are not recomputed
for each arm. The RAW epoch took roughly 16–26 seconds; the integrated ALL_RAW
epoch took 70–89 seconds. These are one-epoch timings, not selected fit lengths.

Maximum worker RSS in the three-worker full-prefix check was 2.16 GiB.
Three times that maximum is **6.48 GiB**, a conservative worker-only estimate,
not a measured simultaneous system peak. Adjusted-feature working sets,
inference, OS memory and full-stopping trajectories remain acceptance items.
An independent bounded GLM preparation process ran during the timing checks;
these are practical on-machine observations, not isolated hardware benchmarks.

Outputs, all under `experiments/cache/joint_capability_2026_09_18_`:

- `v16_perf_packet_dev1`, `v16_parallel_dev1`: short-batch packets/results.
- `v16_fullprefix_packet_dev1`, `v16_fullprefix_parallel_dev1`: complete-prefix
  packets/results, per-worker epoch logs and exact parameter comparisons.
- `v16_bridge_dev1`: four real inner/final data bridges at 2016q1/2026q4.
  Defensive prefix means/scales match archived v15 exactly. Maximum nested
  parent difference is .00003557 pts/100. Label/exposure checks passed.

## Implemented since the foundation checkpoint

- A dated monthly/exact-origin capability-library builder, annual prior-quarter
  four-lambda selection with paired bootstrap one-SE choice, causal warm starts,
  coordinate opportunity/Kish support, matched raw references, marginal
  uncertainty and joint draws. Full calendar: **254 snapshots × eight chains
  = 2,032 snapshot fits**, plus annual tuning candidates. Coverage is
  2009-03-01 through 2026-03-02, exactly the needed historical prefixes.
- Exact-date feature lookup, prefix-only normalization, explicit cold/stale
  handling and shared unknown-player/clone draws. A partial library cannot
  silently forward-fill a missing month or become production training data.
- Read-only numeric memory-mapped views of existing group/phase inputs.
  `v16_training_inputs_dev2` is accepted. Preserve failed `dev1`: its attempted
  numeric export of text defensive-feature names raised a dtype error. The
  accepted layout leaves the smaller original defensive NPZ intact.
- Common loss references, game-complete deterministic training, strict inner
  selection, fresh dated final initialization, transactional two-slot resume,
  bounded checkpoint retention, and complete-ledger last-five averages.
  Interrupted synthetic training resumes identically. Completed shared contexts
  are lock-free reads, so parallel arms do not spuriously acquire writer locks.
- A native per-case fit stage and a 1–3 process fail-stop queue with separate
  logs/receipts. **Shared contexts must finish before dependent parallel jobs;
  calibrated reports must advance chronologically after native fits.**
- ADJUSTED_CHANNEL accounting from each complete offensive-bank GLM, with
  normalized action proportions and stationary renewal applied once.
- U0 and U1/U2 likelihood/fitting primitives with strict prior cutoffs and
  synthetic identification/failure checks. Real pair construction, prior-only
  noise forecasting, descriptors and validation reports are **not finished**.

For U2's remaining numerical conventions: equal weight per pair; summed NLL
plus lambda/2 times squared standardized slopes; unpenalized bias/log-variance
intercepts; strongest lambda on a numerical 1e-10 tie; lambda 10 cold selection
when the earlier calibration-training subset lacks 30 pairs/two seasons.
These are pre-pilot conventions, not choices based on observed U results.

## Selected-penalty diagnostic and numerical correction

`v16_library_dev1` is a **two-cutoff diagnostic**, not the full historical
library. Four offensive chains completed. Its late defensive-count fit reached
iteration 500 with projected gradient .00664, failing the registered 1e-5
tolerance despite a tiny objective change. The fail-stop queue stopped starting
new chains while letting its existing defensive-location job finish.
That job subsequently completed successfully. The queue ended after 62.0 minutes
with five successful chains, one failed chain and two unstarted chains; no job
remains active. No nonconverged snapshot was accepted; incomplete/rejected
artifacts remain.

The old solver spent its entire budget on L-BFGS, leaving no room for its
existing Newton refinement. The new separate `v16_solver.py` switches at
relative-objective stabilization (L-BFGS ftol1e-10), reserves up to eight
refinement iterations, and still enforces **both original convergence tests
and the same total 500-iteration cap**. Counts/conversion/recovery use exact
constrained factors; location uses full-Hessian preconditioned CG. There is
no likelihood, constraint, lambda, draw-count or stopping-standard change.

On the exact failed late defensive-count case, with the same earlier warm
start, it converged in **282 iterations / 74.5 seconds**, projected gradient
8.33e-11. This correction is saved separately in `v16_solver_dev1`; it does
not rewrite or relabel the failed source snapshot. Synthetic solutions match
the reference objective and predictions. The full library still needs this
solver integrated under a **new prefix**. The old audit has now exited.

### Joint covariance draw acceleration

The independent-output counts/conversion Hessians and coupled collector-recovery
Hessian admit exact smaller dense factors. Reusing them across 32 right-hand
sides preserves all within-fit player/block covariance and the original RNG
sequence; it is not independent jitter, extra ridge, or diagonal covariance.
The large cross-category location Hessian remains matrix-free.

| Late offensive-bank family | Existing PCG, 32 draws | Shared exact factors, 32 draws |
| --- | ---: | ---: |
| Counts, lambda10 | 324.6 s | 11.82 s |
| Conversion, lambda1000 | 104.3 s | 19.49 s |
| Recovery, lambda10 | 68.8 s | 5.69 s |

Largest sampled-parameter difference versus the saved 32 reference draws:
1.63e-8; relative draw errors below 4.7e-9. Direct residuals are below 2.4e-14.
These are timings from different bounded queue loads, not precise speedup
guarantees. `v16_fast_draws_dev1` retains every comparison. The smaller
`v16_direct_curvature_dev1`, `v16_direct_conversion_dev1`, and
`v16_direct_recovery_dev1` are preceding four-RHS factorization checks.
The accelerated exporter is implemented separately in `v16_draws.py`, not yet
substituted into an active/frozen library producer.

### Raw-versus-adjusted evidence so far

Held-out following-quarter NLL difference, adjusted minus matched monthly
own-only empirical-Bayes raw summaries; lower is better. These are **channel
diagnostics, not NN/additive point comparisons**, and the raw summaries are
not an exact copy of the older two-point conversion representation.

| Offensive bank | 2016q1 | 2026q4 |
| --- | ---: | ---: |
| Action counts | −.00038808 | −.00091790 |
| Location | +.00599038 | +.00343405 |
| Conversion | +.00025806 | +.00102571 |
| Recovery | +.00566648 | +.00384049 |

Both count/location/recovery dates selected lambda 10 at the registered lower
boundary; conversion selected 100 early and 1000 late. These are prior-validation
choices, not outer-result selections. Report the boundaries; do not floor or
expand the grid. Early defensive counts/location improve slightly versus their
matched raw references (−.00041050 / −.00176522); late defensive location also
improves (−.00069085). The defensive audit is still partial.

Thus adjusted profiles do **not** automatically improve channel prediction.
The raw anchors and J_RAW/ALL_RAW comparisons remain essential. Do not remove
an arm or tune a representation in response to these diagnostics. The neural
augmentation, transfer/coherence and uncertainty questions remain untested.

## Remaining acceptance work

1. The old bounded audit has ended partial; integrate verified hybrid fitting and
   exact-factor draws with new code hashes/prefix. Audit missing defensive
   families and the revised numerical path. Schedule the two expensive location
   chains early when preparing a full library; do not change dates or science.
2. Prepare the **complete** dated library; estimate its remaining location cost
   explicitly. No NN pilot can use the two-cutoff audit as its history.
3. Finish the frozen fixture/descriptor registry, real U1/U2 pairs and strictly
   prior noise forecasts, common chronological NN calibration, statistical and
   cohort reporting, and final independent auditor/lifecycle CLI.
4. Freeze the complete campaign before meaningful NN pilot forecasts. Run the
   all-arm smoke and all 48 prescribed full-stopping operational pilots, then
   measured runtime/storage/memory acceptance. No claim of a precise production
   duration from these one-epoch checks.
5. Supply verified full launch/log/status/leaderboard commands only after that
   preflight. Production still requires Adam's separate authorization.

All three standards remain co-equal. No full campaign, database operation,
scraping, old input rebuild, scorer promotion or deployment occurred. Adam later
authorized a checkpoint commit of source/tests/docs, excluding generated caches.
**64 tests passed** in `v16_development/logs/foundation_tests_11.log` (the full
directory prefix is given above). Checkpoint audit `v16_checkpoint_dev2`
verified all **256 original v13–v15 source hashes** and **2,287 derived-artifact
hash checks** across 549 receipts at audit time. Receipt validity does not
make the partial library complete or the rejected phase_dev1 scientifically
usable. The exact preceding handoff/report are preserved in
`docs/archive/2026-09-18_v16_foundation/`.
