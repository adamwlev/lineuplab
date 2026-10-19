# Current research state

As of **2026-09-27**. This is the canonical present-state page, not a journal.
[Scorecard](MODEL_SCORECARD.md) owns numerical comparisons;
[NEURAL_MODEL.md](NEURAL_MODEL.md) owns the implemented architecture;
[roadmap](MODEL_RESEARCH_ROADMAP.md) owns priorities.

## Status

- **v15 complete and independently reviewed:** 576 cases, four arms, three
  seeds, 48 quarterly origins. The primary analysis excludes 2015 warmup.
  Source/tests/review committed as **e438a4a**.
- **v16 training and all post-training analyses COMPLETE (September 27).**
  Root and all stage receipts verified; no campaign remains active.
  The optimized post-training analysis completed
  the full prediction audit, ensemble/reliability supplements, all 48 average-
  opponent quarters and all 10 fixture origins. All sampled-reference shift
  checks passed. Stage 5 saved 15 quarters, then rejected a falsely converged
  U2 optimizer result in 2018q4. A bounded failed-fit restart preserves the
  likelihood, penalties and gradient threshold; 180 accepted historical fits
  replay within 1.55e-8 in parameters. Fourteen tests pass.
  The new derived continuation `...2026_09_27_v16_uncertainty_repaired`
  reuses completed outputs without editing the failed source or frozen producers.
  All 48 uncertainty quarters and finalization finished. The final Markdown
  formatting failure was resolved by installing tabulate==0.9.0 in basketball25;
  resumed finalization took 6.55 seconds, with no numerical recomputation.
  All 20 final provenance files and reused sources were verified.
  [Numerical repair](reports/joint_capability_v16_uncertainty_solver_repair.md).
  [Current handoff and live logs](SESSION_HANDOFF.md).
  All 3,168 native cases / 6,336 inner-final fits remain intact.
  The earlier player-ID/prediction-column collision was repaired in derived
  scoring; old uncorrected leaderboards must not be used. Neural training was
  unaffected. Human interpretation across all three standards is still pending.
- **v16 optimization accepted and launched:** Adam stopped the
  first production campaign after four completed cases to address excessive
  runtime. Original cases, partial epoch journals and all producer fingerprints
  are preserved. Versioned equivalent-computation optimizations remove repeated
  work on disabled banks and reuse fixed input summaries, without changing the
  22-arm scientific protocol. Matched warmed CPU speedups: RAW **2.35×**, BOTH
  **1.34×**, ALL_BOTH **1.86×**; not a whole-campaign ETA. All-arm early/late
  forward/loss/gradient/update checks are exact; a full RAW training replay
  preserves stopping, weights and forecasts exactly. 104 tests and storage/RAM
  preflight pass. Three workers/seeds retained. See the
  [runtime review](reports/joint_capability_v16_speed_review.md).
  Accepted destination: `...2026_09_19_v16_fast2_ready`; wrapper:
  `bash experiments/run_v16_fast2_ready.sh run`. Adam has restarted full
  training, now completed; do not launch another supervisor. The [current handoff](SESSION_HANDOFF.md)
  has operational commands and the report-validity warning.
  Original library (2,032 snapshots), 44 smoke cases and eight audited pilots
  are retained; no input rebuild. Earlier hashfix/fast/fast2 launch routes are
  historical and must not be used for the optimized restart.
- **Local GPU benchmark complete; retain three CPU workers.** On real saved
  training batches, warmed M1 Pro MPS was only 1.07–1.18× faster than one CPU
  worker for simple arms. Measured three-worker CPU throughput was 2.10–2.35×
  projected sequential single-GPU throughput for those workloads. All four
  combined-arm MPS attempts failed with nonfinite gradients. Original CPU
  producers/precision are unchanged; no new predictive or OOD claim. See
  [benchmark report](reports/joint_capability_v16_local_gpu_benchmark.md).
- **No research scorer promoted.** The existing
  [published-page source](tool/five.html) still uses the older
  [additive-based model](CURRENT_MODEL.md).
- Current session: completed repaired uncertainty and finalization; all three
  seeds and original artifacts retained. Corrected point validation, prediction
  audit and statistical supplements are complete; human review remains. See
  [handoff](SESSION_HANDOFF.md).

## What we retain

| Component | Present role |
| --- | --- |
| Corrected additive offense `A` | Required individual-value baseline; not the legacy page's full chemistry/gate stack |
| v14 `RB_RENEW_FAC` offense `N` | Neural backbone with teammate context, dated role features, creation/load constraints and rebound renewal |
| Shared additive defensive adjustment `D` | Equally informed actual-opponent control, with a prior-centered sign convention |
| `N+D` | Best novel-lineup RMSE among the listed v15 forecasts |
| `.5(A+N)+D` | Essential opponent-aware combined control |
| v15 `D_MAIN_RB` | Simple defensive mechanism candidate; its half blend has the smallest primary point error, but no established increment over the combined control |
| v15 `D_CROSS_RB` | Channel-mechanism challenger, not the point winner |
| v14 `ROLE_SL`, `RB_RENEW_FAC_SHIFT` | Retained offensive/role controls; evidence is in the v14 and transfer reviews |

“Retained” means useful for research comparisons, not production acceptance.
The primary contextual NN has no known-pair chemistry or player-ID embeddings.

## Three co-equal standards

**Prediction:** actual-opponent information improves the comparisons, but the
new adapter's small point advantage over old HALF+D is not established.
Calibration explains most of that small headline difference. Original and
post-hoc-calibrated results must remain separate.

**Basketball coherence:** learned opponent/rebound responses are encouraging;
five-center offense and role/action allocation remain unresolved. Named cases
are hypotheses, not rankings to impose. Good defense cannot rescue an
implausible offensive prediction.

**Uncertainty:** held-out finite-game bands are reasonably calibrated.
That does not validate latent lineup-quality uncertainty, extreme hypothetical
lineups, or cross-era transport. Numerical opponent-integration error is also
not a statistical confidence interval.

The authority for these standards is
[CONTEXTUAL_MODEL.md §2](CONTEXTUAL_MODEL.md#2-three-co-equal-acceptance-standards).
The completed [v15 review](reports/joint_capability_v15_codex_review.md) gives
the supporting evidence and limitations.

## Interpretation boundaries

The main scorecard is possession-weighted **offensive-lineup-quarter** error
on 44 quarters / 5,607 matched cells / 726,364 possessions. It inherits an old
profile-support intersection: “all” does not mean all possessions or all
>=50-possession lineups. The separately labeled broader cohort has 8,345 cells.
Opponent-aware scores condition on the actual opposing fives encountered;
they do not validate a forecast against an unknown future schedule or the
tool's average-opponent rating. See [scorecard](MODEL_SCORECARD.md) for details.

These historical seasons have been repeatedly inspected during development;
they are not a fresh confirmatory holdout.

## Active campaign and post-training repair

[v16](JOINT_CAPABILITY_V16_PLAN.md) combines controlled tests of strictly dated
adjusted capability profiles, jointly adapted offense/defense, two-sided
attention versus matched capacity, action allocation, and separate post-rebound
offense. Fair calibration, broader evaluation, stable average-opponent
integration and persistent-discrepancy uncertainty are required companions.

The authorized optimized training and corrected point reconstruction are complete.
The old repair/supplement supervisors are stopped. A new bounded analysis path
has finished its prediction audit, supplements and fixtures. Its separate numerical
uncertainty-repair continuation and finalization are complete. No relaunch needed.
See the [current handoff](SESSION_HANDOFF.md)
for repaired status/report/log commands, not the old training launcher. The
[canonical backlog](MODEL_RESEARCH_ROADMAP.md) records deferred questions;
the v16 plan alone specifies its experiment.

## Operations

Run from `/Users/adam/Documents/basketball`. These commands were verified
2026-09-18 and **only read existing outputs**:

```bash
bash experiments/run_joint_capability_v15.sh status --run-dir experiments/cache/joint_capability_2026_09_17_v15_prod
bash experiments/run_joint_capability_v15.sh report --run-dir experiments/cache/joint_capability_2026_09_17_v15_prod --sort rmse --slice all
```

Report options: `--sort rmse|mae|raw_r2|corr`;
`--slice all|novel|recurring`. Do not run an old `run` command just to inspect
the leaderboard.

Completed training log:

```bash
tail -n 80 experiments/cache/joint_capability_2026_09_17_v15_prod/logs/train.log
```

Independent derived review:
`experiments/cache/joint_capability_2026_09_18_v15_codex_review`
(`review.log`, `receipt.json`).
Broader-population review:
`experiments/cache/joint_capability_2026_09_18_v15_group_review_v3`
(`analysis.log`, `receipt.json`).

These are local artifacts, not bundled data for a fresh clone. The earlier
[v2–v10 state synthesis](docs/archive/2026-09-18_pre_cleanup/JOINT_CAPABILITY_STATE.md)
is historical; its broad “closed” and ceiling claims are not current rules.
