# Current research state

As of **2026-09-30**: **v19 production is running**, following completed
implementation, seven unchanged native pilots and full downstream rehearsal.
See [launch report](reports/joint_capability_v19_launch.md) for current operations.
V18's scientific review, role/volume diagnosis and persistence/coupling work
remain the latest completed research conclusions. Retain J_POINT_BOTH; no new
winner, scorer promotion or overall three-pillar pass.

## Active experiment: v19

Frozen five-arm context/capability study: C_FIXED, C_CLOCK, C_FULL, C_ALLOC,
C_MARGIN.48origins, three seeds,720cases/1,440fits; seven compatible pilots
reused and713new cases. Three CPU workers, one thread each. All original
cutoffs, objective, epoch cap96/patience8/min_delta1e-5 and populations unchanged.
Reference forecasts integrate nonlinear physical ledgers over the past-only
context distribution. Actual-context CLOCK/MARGIN panels are diagnostics,
not forecasts made with unknowable future context.

Root: experiments/cache/joint_capability_2026_09_30_v19_prod.
Detached supervisor73644, caffeinate73645. Initial2015q1point-control jobs
finished successfully; three C_FIXED training workers started. Read
[handoff](SESSION_HANDOFF.md) for log/status/report/preview commands.

All-in estimate58.04h,68.71h with1.2× native training stress, under Adam's
[roughly65h runtime acceptance](reports/joint_capability_v19_runtime_authorization.md).
Optional per-epoch validation optimization remains deferred.
Storage projected54.48GiB additional against65.10GiB free at acceptance,
leaving10.63GiB. Reserve10GiB; supervisor stops before a subsequent origin/stage
if free storage is below it. This is tight and compression varies; no new cleanup
is authorized automatically.

Full downstream graph rehearsed in324.39s, no new NN fits.51tests passed.
All1,152 retained-control calibration checks match to2.84e-14points/100.
Independent native/event, context-mixture, point, uncertainty-status and
covariance-accounting audits pass. Pilot accuracy is isolated cold-start
evidence, not production prequential results. The final readiness receipt is
experiments/cache/joint_capability_2026_09_30_v19_launch_readiness1.

After training, automatic stages cover average-opponent integration, all
high-support observed context curves, coefficients/support/saturation, fixed
fixtures, role/transfer/analogue checks, native event audits, candidate U0/U1,
persistence/full covariance, registered17point/28event contrasts and final
supporting tables. Scientific review and human interpretation remain to be
written after completion. No automatic model promotion or assistant wakeup.

Completed v16–v18 optimizer retirement is governed by the separate
[retention ledger](docs/ARTIFACT_RETENTION.md). Original weights/checkpoints,
predictions, receipts and frozen producers remain. Every consumer process needs
the retention wrapper; the v19 shell launcher and children use it. Adam authorized
the post-launch implementation/documentation checkpoint on top of32ab995d;
generated run artifacts remain local and outside that commit.

The [scorecard](MODEL_SCORECARD.md) owns comparable metrics;
the [roadmap](MODEL_RESEARCH_ROADMAP.md) owns priorities;
the [handoff](SESSION_HANDOFF.md) owns operations.

## Retained research models

| Component | Present role |
| --- | --- |
| Additive and additive_defense | Individual-value and equally informed opponent controls |
| Parent_half_defense | Strong earlier contextual comparator |
| J_POINT_BOTH half / checkpoint-average-half | Retained v16 point references; not promoted |
| J_BOTH | Simpler event/mechanism comparator |
| O_ORDER | v17 accounting-order candidate; point performance tied with retained reference |
| R_ALLOC / R_ROUTE | v18 allocation/routing candidates; count/allocation gains, no established incremental primary point gain |
| A_CONTEXT_GATE / A_GATE | v18 compact-context transfer and reliability candidates; descriptive evidence, not selected scorers |
| O_FLOW / O_FLOW_EVENT | Shared-capacity mechanism comparators; no established incremental point win |
| D_SHAPE / O_FLOW_D_SHAPE | Diagnostic evidence; removing defensive volume worsens count/conversion fidelity |
| U1 constant discrepancy | Required uncertainty control; no synthetic-quality validation |
| U2 contextual discrepancy | Earlier research only; no established advantage over U1 |

The NN is profile-based, without known-pair chemistry or player-ID embeddings.
The [existing tool](tool/five.html) still uses its older
[additive-based model](CURRENT_MODEL.md).

## What the completed experiments establish

- Conversion errors repeat weakly: reference random-game correlation .0367,
  chronological .0188. On2,214,552attempts the NN beats dated player50 shooting
  (log loss .657272 vs .658250) in all11seasons; previous-quarter residual updates
  worsen every NN in all11. This is not proof of an exhausted accuracy ceiling.
- Shared CLOCK sensitivity reduces broad FTA bias +1.890→−.025 attempts/100,
  transfer +4.296→+.961; remaining opportunity error is more persistent than
  shooting conversion. Channel errors offset substantially: within-origin
  component covariance diagonals19.235, cross terms−8.703, total10.532.
  Reference half advantage over additive survives common target adjustment.
  Original leaderboard, counterfactual means and interval claims are unchanged.
- The separate observed-role library includes907 large FGA-share changes among
  12,290 supported player-quarters. Reference share MAE4.367pp versus prior6.396pp;
  R_ALLOC4.314pp. On2,139 original role-change cells, reference half r².18102
  versus additive defense.16671; allocators do not improve its point result.
  Conversion dominates absolute accounting residuals, but includes shooting
  noise; FGA/FTA errors offset and component attribution depends on order.
  Role-slice finite95% reference coverage is92.80% cell/93.09% weighted.
  Outcome-selected diagnostics do not certify prospective or synthetic quality.
- v18 confirms useful learned teammate information beyond mechanical accounting:
  A_ACCOUNT worsens counts/location/conversion in all11 seasons, event Holm.03516.
  R_ALLOC improves counts in all11, Holm.03516, but transfer turnover shares and
  team FTA volume remain problematic. Routing alone does not improve transport.
- Primary half r²: A_GATE.162629, R_ROUTE.162308, reference.162915. Checkpoint-half
  R_ROUTE.163469 is descriptive; its same-view reference RMSE interval crosses0.
- Fixed transfer cohort remains146cells/47,419possessions. A_CONTEXT_GATE leads
  descriptively (half RMSE6.6488 vs reference6.6745); no transfer-selected promotion.
- V18 fixes the U0 summary status contract. Reference broad nominal95% coverage
  is93.47% by cell/93.19% weighted, debut90.49% weighted. All eleven candidates
  still favor legal centers against both Jokić fixtures; no solved OOD mean/band.
- v16 adjusted profiles consistently helped RAW/BOTH comparisons. More attention,
  width, phases and multi-NN ensembles did not establish a compelling advantage.
- v17 is a near-tie in primary prediction: O_ORDER half r².163049 versus
  J_POINT_BOTH.162915, additive_defense.146023, parent_half_defense.156601.
  Same8,345 broad cells /1,013,999 possessions,44 primary quarters.
  O_ORDER versus J_POINT_BOTH RMSE−.000887[−.004135,.002210].
- D_SHAPE count and conversion losses worsen11/11 seasons; point totals alone
  would hide that cost. Flow does not establish an event-wide improvement.
- Flow lowers center offense somewhat but all seven models still favor the
  legal-center fixture against both Jokić fixtures. Two-big observed bias remains
  about+3pts/100. No forced rankings and no complete coherence pass.
- Average-opponent half r²: O_ORDER.148764, J_POINT_BOTH.148368,
  integrated additive_defense.132160. Small new differences, not neutral-opponent
  counterfactual ground truth.
- Corrected broad U0 coverage is about93–94% at nominal95%; U1 proper scores
  are very close. These do not certify hypothetical latent-quality intervals.
- Reliability estimates are noise sensitivities, not theoretical r² ceilings.
  Reused historical seasons are development evidence, not fresh confirmation.

## Evidence and next decision

V16:3,168cases/6,336fits and corrected analyses preserved.
V17:720cases,25.27supervisor hours, independent review complete.
V18:1,008cases/2,016fits,41.188supervisor hours, independent review and separate
role/volume/persistence studies complete. Original reports/frozen plans remain
unchanged, including their original launch and historical HOLD statements.

V19 foundation/native evidence is in the
[implementation report](reports/joint_capability_v19_implementation.md),
[prelaunch checkpoint](reports/joint_capability_v19_prelaunch.md) and new
[launch report](reports/joint_capability_v19_launch.md).
All288teachers, context-label reconciliation and120float64 value/loss/gradient
checks passed. Seven full pilots had no failures/cap hits. New diagnostic
precision handling concerns mixed-float32 phase-point re-association only,
not changed training or weakened float64 objective proofs.

Next: allow the frozen campaign to finish, investigate correctness/resource
failures without result-driven protocol changes, then write
reports/joint_capability_v19_review.md and evaluate all three standards.
Compare reference versus equally informed actual-context evidence; preserve
the missing2014q4 additive-inner warmup diagnostic and original primary/transfer
cohorts. Finite-game intervals and seed variation do not certify hypothetical
latent quality. No forced basketball rankings or known-pair chemistry.

[Previous state](docs/archive/2026-09-30_pre_v19_launch/JOINT_CAPABILITY_STATE.md)
preserves full historical operations and earlier archive links.
