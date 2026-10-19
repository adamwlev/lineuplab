# Current research state

As of **2026-10-06**: **v19 training, all post-training analyses and independent
scientific review are complete**. Read the [v19 review](reports/joint_capability_v19_review.md).
Retain J_POINT_BOTH: no new incremental point winner, scorer promotion or overall
three-pillar pass. V19 completion is committed as **8e8b325f**. Adam approved
implementation of [v20](JOINT_CAPABILITY_V20_PLAN.md); its bounded profile pilots
are complete and independently reviewed. The full historical profile library
and its deep audit are complete. All eight bounded neural pilots finished in
28.07minutes. New-case storage lifecycle passes exact replay with82.22% smaller
artifacts; original pilots unchanged. Matched pilot scoring and independent
point/event audits now pass. No full NN campaign has launched.

## Active implementation: v20

Context-adjusted capability profiles × no/FULL decoder context × current/S5
checkpoint selection: eight comparison cells, two reused controls and six new
neural arms (864case slots before pilot reuse). Primary checkpoint-average-half
is common across cells; direct/half views remain visible. A new254-date/eight-chain
profile library is required, with strict historical lookup and joint player/clock
covariance. Raw state inputs and original artifacts remain unchanged.

Synthetic recoverability, original transfer/coherence checks and a small nested
role/clock-deployment discrepancy experiment are part of the design, not merely
more point metrics. Adam freed additional space:196.55GiB immediately free.
Pilot-measured remaining training estimate44.38hcentral/52.69htraining-stress,
excluding downstream work; no full-launch readiness or authorization yet.
[Implementation checkpoint](reports/joint_capability_v20_implementation.md): joint
GLM/covariance/library and P/S5 trainer primitives implemented;22targeted tests
pass. Synthetic640fits complete: overlapping-deployment prediction errors improve
13.2% counts,0.88% location,0.77% recovery; conversion tied. Severe fixed-ridge
shrinkage yields only~40%nominal95coefficient coverage; not an uncertainty pass.
Real-source16panel arithmetic audit passes. Two-date profile pilots finished in
71.5minutes:96/96fits converged, all16penalties unchanged, matched mean-rate NLL
differences under0.08%. No standalone predictive breakthrough claimed.
Independent profile-pilot review verifies122receipts. Full chronological library
`experiments/cache/v20_library_full_2026_10_04` completed in33.44h:2,032snapshots.
New deep audit verifies4,562receipts and384annual candidates; all snapshots
converge, max238iterations, max joint-draw residual1.0e-8. All2,032player penalties
match the original library. Matched reference profile NLL changes remain tiny;
not a new neural predictive result. Raw inputs remain unchanged and real
feature sentinels pass through both adjusted banks and the memoized NN.
New case consumer exports selected-inner/final, direct/averaged and
reference/conditional ledgers, including state-level mixtures. Twelve targeted
case/fit/evaluation/selection tests pass. Eight prescribed neural pilots completed
at `experiments/cache/v20_nn_pilots_2026_10_06`:16fits, selected7–23epochs,
no cap hits/errors, exact selected-score replay. New production-case lifecycle
rehearsed on copies:2.506→.445GiB,48forecast exports byte-exact;35tests pass.
[Retention evidence](reports/v20_storage_lifecycle.md) is followed by the
[matched-scoring rehearsal](reports/v20_scoring_rehearsal.md): all four pilot
panels pass independent point arithmetic and32native event panels pass, including
conditional averaged states. Core report/preview verified;16targeted tests pass.
Calendar-scaled cases+scorecards+stress/temporary/reserve total75.32GiB, below
current196.55GiBfree. Remaining downstream analysis/storage/time and full-run
orchestration are open. No automatic cleanup or full NN launch.
Saved P_BASE/P_CONTEXT replay passes at both pilot dates (four cases, zero refits):
current-evaluator outputs bit-exact; archived drift below the existing float32
guard, maximum~1.07e-7points/100. All original artifacts preserved.
No historical cleanup authorized. Operational commands and current job: [handoff](SESSION_HANDOFF.md).

## Latest completed experiment: v19

Five frozen context/capability arms: C_FIXED, C_CLOCK, C_FULL, C_ALLOC, C_MARGIN.
720 cases / 1,440 fits, 48 origins, three seeds. Training/scoring49.24h;
average-opponent integration2.39h; repaired post-training continuation1.61h.
Original root: experiments/cache/joint_capability_2026_09_30_v19_prod.
Its RUNNING status is stale. Do not restart the original supervisor.
Completed continuation: experiments/cache/joint_capability_2026_10_03_v19_posttrain1.
Independent derived review: experiments/cache/joint_capability_2026_10_04_v19_review2.

Primary remains8,345cells/1,013,999possessions,44quarters2016–2026.
Half r²: J_POINT_BOTH.162915, C_FIXED.162937, C_CLOCK.159471, C_FULL.159127,
C_ALLOC.158154, C_MARGIN.156975; additive_defense.146023. Joint context arms
recover substantially with checkpoint averaging, but not past the same-view
reference. No registered incremental point contrast establishes an improvement.

C_FULL improves actual-context counts/location/conversion/recovery in11/11seasons,
Holm.027344 each against C_CLOCK. Shared situation matters beyond counts; better
conditional event prediction does not establish better common-environment player
values. Margin-conditioned accuracy is not a product forecast or causal effect.
Transfer/role-change point results do not improve. All9models still favor legal
centers against both Jokić fixtures; new joint arms increase center FTA.

Primary-only reference half U0 nominal95 coverage93.47%cell/93.19%weighted.
C_FULL93.68%/93.20% with wider bands, slightly worse interval score.
Automated pooled uncertainty included2015warmup; use review2's primary-only
re-pooling for comparison with previous reviews. Original bands/tables unchanged.
U1 has no new advantage; hypothetical latent-quality coverage remains unvalidated.

The [accounting repair](reports/joint_capability_v19_accounting_repair.md)
preserves frozen labels/targets and adds an explicit observed-accounting
component for3mismatched input rows, none in primary evaluation.
Independent native audit720cases, point audit144panels/5,472calibration checks
and review270metric rows pass. Original code, plans and outputs remain intact.

See [handoff](SESSION_HANDOFF.md) for current operations and dirty work.
The [scorecard](MODEL_SCORECARD.md) owns comparable metrics; the
[roadmap](MODEL_RESEARCH_ROADMAP.md) owns priorities.
Mandatory native-consumer [retention wrapper](docs/ARTIFACT_RETENTION.md)
continues to apply to retired v16–v18 optimizer restarts. V20 implementation and
bounded pilots are now authorized. No cleanup or full NN launch is authorized.

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
| C_FIXED / C_CLOCK / C_FULL | v19 context controls; C_FULL adds conditional event fidelity, no new reference-point or three-pillar winner |
| C_ALLOC / C_MARGIN | v19 allocation and endogenous-margin sensitivities; no established incremental reference gain |
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

V19 and its [independent review](reports/joint_capability_v19_review.md) are now
complete and committed. Next: finish the
[v20 plan's](JOINT_CAPABILITY_V20_PLAN.md) downstream implementation/rehearsal
using the new storage interface; finalize downstream resources and orchestration
before requesting full NN launch approval.
Preserve the missing2014q4 additive-inner warmup diagnostic and all original
primary/transfer cohorts. Finite-game intervals and seed variation do not certify
hypothetical latent quality. No forced rankings or known-pair chemistry.

[Previous state](docs/archive/2026-10-04_pre_v19_review/JOINT_CAPABILITY_STATE.md)
preserves full historical operations and earlier archive links.
