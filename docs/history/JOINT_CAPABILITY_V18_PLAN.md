# v18 — clearer capability inputs and role-to-outcome routing

Frozen scientific design, 2026-09-28. Adam approved implementation after reviewing
the arm set and gating/shrinkage discussion. Full production launch is not yet
authorized. Prepared after Adam requested a checkpoint commit,
reflection and a detailed next experiment with a **54-hour total runtime target**.
The v17 review/literature/idea checkpoint is committed as **095183b1**.
This document specifies the experiment, not a completed or launched
campaign. Frozen before scientific pilots. Engineering
findings may require an explicit prelaunch amendment; outer results may not.

## 1. Reflection: what question should we now ask?

The [v17 review](../../reports/joint_capability_v17_codex_review.md) does not say the
contextual model has failed. It preserves a substantial advantage over equally
informed additive on the primary and novel-lineup cohorts. But the new capacity
constraint moved forecasts much less than hoped and did not settle extreme
lineups. Repeated small architecture changes may be attacking the wrong layer.

Our strongest reproducible representation finding remains v16's adjusted
capabilities. They help across many architectures, whereas more attention,
width, phases and ensembling did not establish a comparable benefit. Even so,
adjusted coefficients are noisy estimates, not pure abilities, and adjustment
is worse on some standalone event targets. Raw histories are also not pure
abilities: they mix skill, role, teammates and deployment.

Three questions deserve a coherent campaign:

1. **Which player information do we actually need?** Remove redundant context
   and test selective/reliability-aware adjustment, rather than feed every
   representation everywhere and trust a small NN to disentangle it.
2. **Where should role information act?** Historical usage and teammate context
   may be valuable for allocating actions without deserving an unrestricted
   direct path into shooting conversion. Test that routing explicitly.
3. **What is learned contextual adaptation buying beyond accounting?** Train
   an own-state-plus-opponent control with no learned current-teammate messages,
   retaining the nonlinear action/creation/rebound ledger.

The [literature review](../../reports/literature_review_2026_09_27.md) motivates ability
versus policy and event-based complementarity; it does not validate our proposed
implementation. This campaign is an identifiable **routing/representation test**,
not a claim to recover causal ability or coaching strategy from public PBP.

Prediction, basketball coherence and uncertainty remain co-equal. A simpler,
more coherent model with a modest measured point cost can be valuable. Do not
force the five-center or Jokić/Korver/Westbrook ranking.

## 2. Fixed proposed arm set

Seven new arms;48 origins ×3 seeds17/23/41 = **1,008 cases /2,016 fits**.
All use the stationary renewal ledger and full defensive-volume information.
No attention/depth/flow-round/phase sweep. All seven have point-loss weight.25
and retain four event losses. Reuse completed event-only controls.

| Arm | Change | Main question / comparator |
| --- | --- | --- |
| A_CONTEXT | Remove raw teammate/defender contextual paths, retaining adjusted context and own raw anchors | Does redundant raw context help a point-trained model? versus J_POINT_BOTH |
| A_SELECT | Full raw paths, but a fixed subset of adjusted input channels | Can we omit the adjusted channels whose standalone forecasts were less useful? versus J_POINT_BOTH |
| A_GATE | Full inputs; small learned reliability gates on adjusted coefficient deviations | Can reliability organize information better than concatenation alone? versus J_POINT_BOTH |
| A_CONTEXT_GATE | A_CONTEXT plus the same gates | Do compact context and reliability weighting complement each other? versus A_CONTEXT and A_GATE |
| A_ACCOUNT | Remove learned current-teammate messages on offense; keep own-state learning, defense and mechanical accounting | How much is learned teammate adaptation buying? versus J_POINT_BOTH |
| R_ALLOC | v16 action-allocation architecture with point weight.25 | Matched allocation control; versus J_POINT_BOTH |
| R_ROUTE | R_ALLOC, removing raw role/context's direct shooting-conversion route while retaining adjusted-context and workload routes | Does separating action choice from conversion improve transport? versus R_ALLOC |

Core reused controls: J_POINT_BOTH, J_BOTH, J_ACTION_BOTH, O_ORDER,
additive_defense and parent_half_defense; additive offense for orientation.
Reuse exact compatible fits/predictions, never refit those just for completeness.
Other v16/v17 arms remain historical comparators, not a larger automatic serving
ensemble. v17 flow fixtures/diagnostics can be cited without rerunning them.

Why not adopt O_ORDER as every arm's base? Its point advantage is tiny and not
established. Keeping J_POINT_BOTH's ordering isolates input/routing hypotheses,
and R_ALLOC can compare to the already trained event-only J_ACTION_BOTH. O_ORDER
remains a displayed control. No simultaneous ordering change hidden in v18.

## 3. Exact representation contracts

### 3.1 Shared inputs and initialization

Read the immutable dated v16 capability library, matchup labels, parent models,
inner/final normalizers and training contexts already verified for v17. No new
ridge/profile fits, raw-data extraction, input-cache reconstruction or tracking.
Player IDs index strictly dated profiles; they are not NN embeddings/features.

Adjusted offense has97 coordinates: own/influence coefficients32, log-support32,
log-curvature-SD32, log-staleness1. Defense has49:16 of each plus staleness.
Within each16-coordinate block: counts0:3, location3:9, conversion9:15,
recovery15:16. Write named schema masks; never guess flattened positions.

Each inner and final fit starts independently from its proper dated parent,
not from the previous arm or origin, nor from an inner-fit checkpoint. Preserve
prefix loss references, raw anchors and the existing model's per-parameter
initialization convention. Use fixed seed offsets for new modules; adding an
arm must not change another arm's random initialization or minibatch order.

No pretend exact nesting for a path-removal arm: it can change the pretrained
initial function. Record initial point/event/assisted-fraction differences on
inner-training probes before fitting. Parameter-count and initialization
differences belong next to the comparison, not in a footnote after selection.

### 3.2 A_CONTEXT: precisely a contextual-input ablation

Use v16 J_ADJ_CONTEXT's semantics with point weight.25:

- Raw offensive message keeps the receiver's own18 coordinates; raw other-four
  mean and spread are removed.
- Keep four own recent-role coordinates; remove four historical-teammate role
  descriptors from raw role and rebound collector paths.
- Disable raw rebound donor facilitation and raw defensive main/recovery
  adapters. Keep adjusted own/teammate/donor/defense paths, including their
  count and recovery outputs; this is **not** D_SHAPE.
- Keep own raw rate/location/conversion anchors, assist supply, rebound priors,
  league reference and support. Apply the same own-only raw-state convention
  to the frozen assisted-fraction path, as J_ADJ_CONTEXT did. FT conversion
  remains frozen and context-isolated.

This is not a fully adjusted-only player model. Original raw quantities anchor
an event process and include channels the adjusted bank does not supply. Do
not substitute zeros/league rates for missing assist capacity merely to claim
complete replacement. A_CONTEXT is a retrained point-objective test, not a
repeat of v16's event-only scorecard.

### 3.3 A_SELECT: fixed input-family exclusion

Retain adjusted **count** coordinates for both offensive own and influence
blocks; retain adjusted **counts and location** for defense. For excluded
coordinates, mask their coefficient, support and SD inputs to standardized
zero. Retain the bank's shared staleness coordinate. Raw features and all output
channels remain available, so conversion/recovery are still predicted/trained.

This tests excluding entire adjusted input families, not setting conversion
probabilities or rebound effects to zero. Zero standardized inputs mean an
omitted predictor at its training reference, not an assertion that a player's
raw coefficient is zero. Use the same reserved module widths/topology to avoid
mixing feature deletion with a capacity search; report enabled coordinates.
No second subset chosen after results. v16 informed this hypothesis, so reused
historical seasons are not an untouched feature-selection holdout.

### 3.4 A_GATE and A_CONTEXT_GATE: small reliability modulation

For each player and each of the12 block/family groups (own/influence/defense ×
four families), compute the mean standardized log-support and log-SD within
the family, plus the bank's standardized staleness. Define:

`g = 2 * sigmoid(b + w_n * support + w_s * sd + w_t * staleness)`.

Use one parameter quadruple per block/family: **48 new scalars**. Initialize all
four to zero, so g=1 exactly and A_GATE starts at J_POINT_BOTH. Multiply only
that family's standardized coefficient coordinates by g; keep support/SD/stale
metadata unchanged. Compute teammate/defender means and spreads **after** gating.
No player identity, outcome or current/future support enters the gate.

The gate scales deviations from the training reference; it is not a posterior
probability or a mixture of raw rates and ridge coefficients on incompatible
scales. It may amplify up to2 as well as attenuate. Signs are unconstrained:
report the learned relationship to reliability rather than silently imposing
one. No gate regularization sweep, hard support threshold or coverage gate.
Missing-history players retain the existing prior-state fallback.

Input-dependent gates receive point/event gradients. Do not cache gated features
or adjusted-defender moments outside the forward pass: that would freeze the
learned gate or detach its gradients. Reuse only immutable pre-gate quantities.

### 3.5 A_ACCOUNT: trained accounting comparator

Remove all learned **current-offensive-teammate** information:
raw sender mean/spread, adjusted teammate message, raw/adjusted rebound donors.
Keep raw receiver-only transforms, own raw/adjusted inputs and historical own
profile/role information. Retain opponent-conditioned defensive main/recovery
paths and full adjusted defense. No cross-attention or allocator.

The frozen assisted-fraction computation must also be receiver-only; otherwise
it silently reintroduces current-teammate messages. Historical teammate summaries
may remain as fixed parts of a player's observed history, not recomputed from
the proposed five. List those retained dependencies in the artifact schema.

Action normalization, assist supply/demand, overload and rebound competition/
renewal still combine players nonlinearly. Thus this is **not additive** and
not an exact SPM reproduction. It is a trained comparator, distinct from turning
messages off at inference in a model trained to depend on them. Initial
predictions can differ; record that rather than claim a nested zero residual.

## 4. Role-routing family: a bounded test, not latent causal skill discovery

### R_ALLOC

Reuse the exact v16 J_ACTION_BOTH architecture and initialization, changing only
point weight from0 to.25. Separate action-type shares and actor shares:

`q[i,k] = budget * team_share[k] * actor_share[i,k] / c[k]`,
where `c = (1, .44, 1)` for FGA/FTA/TO. Positive softmax shares conserve the
action budget. Use the existing zero-output-initialized team/actor residual
heads, pooled summaries and relative-load feature. This was tested without
point supervision in v16; it is not a claim that allocation itself is new.

### R_ROUTE

Identical to R_ALLOC except the six shooting-conversion coordinates use a
receiver-only raw residual **before** the diagonal decoder. Evaluate the same
raw message MLP with receiver x_i retained but sender mean/spread set to zero;
evaluate the same role MLP with receiver x_i retained and all eight dedicated
role inputs set to zero. For coordinates9:15 only, use:

`z_conversion = base_conversion + message(x_i, 0, 0) + role_head(x_i, 0_8)`.

Zero is the fixed standardized training reference for an excluded input, not
literal zero basketball ability. This preserves own nonlinear receiver
transforms instead of accidentally deleting them with the context. All other
coordinates use the original full-context state. Raw context can still
influence counts, location and the allocator. Own raw anchors/learned diagonal
calibration remain, and own historical rates can still reflect prior role.

Adjusted own/teammate conversion effects, defensive conversion, and the existing
explicit load/assist-shortage responses remain. Thus historical role can change
conversion **indirectly through assigned workload/creation demand**, but not
through an unconstrained raw-context conversion residual. Frozen FT and assisted
fraction paths are identical to R_ALLOC, not relearned. Recovery is unchanged.
Keep parameter topology identical; report removed input paths and
initial function changes. There is no extra loss or bottleneck in this contrast.

Compare R_ALLOC to the saved J_ACTION_BOTH for the allocation architecture's
point/event objective tradeoff. An eighth R_ROUTE_EVENT arm was considered,
but deferred to protect the54-hour target after checking actual allocator
timings. We therefore **cannot** isolate routing under event-only supervision
in this campaign. Neither current profiles nor this routing uniquely
separates ability from deployment. A multi-timescale latent capability/policy
model remains later work; use precise names rather than claim it implemented.

## 5. Labels and evaluation of role transport

Training uses existing player FGA/FTA/TO, location attempts/makes and rebound
outcomes with their original target-specific masks. No new assisted-make,
potential-assist or shot-quality labels are assumed present. Current event
losses already supervise player allocation; no additional share loss or
outcome-reweighting is introduced in this experiment.

Add a bounded **derived** role evaluation from those same held-out labels:

- Save seed-mean per-player FGA/FTA/TO and location forecasts for the original
  matchup rows, keyed by row/player/date; aggregate to player×quarter and
  player×off5×quarter. Preserve event-mask denominators, not just row counts.
- For action type k, score player allocation conditional on observed team
  count using cross-entropy of `pred_i,k / sum_i pred_i,k`, and compare absolute
  event rates separately. Conditioning is an evaluation estimand, never a
  forecasting input. Report team volume so an allocation score cannot hide
  total-volume error. Score shooter location shares only on observed attempts.
- Report full and novel broad populations plus the existing fixed transfer
  cohort. Join by IDs/date, not player names. Use identical eligible rows across
  compared arms; print every exclusion and event denominator.
- Reuse the frozen transfer registry and archived metadata, not new DB queries.
  The original primary cohort was146 cells /47,419 possessions; verify mappings
  to current targets, report any mismatch instead of silently assuming those
  counts transfer. Retain all/100/200/500 possession sensitivities and >=5 games
  where prescribed by TRANSFER_ROLE_BENCHMARK.md. Count multi-mover cells once.
- The transfer registry is retrospectively defined from appearances, not a
  prospectively known trade list. Never use its future labels as inputs or
  relabel its score as causal adaptation. Do not add outcome-selected "large
  role changes" as a confirmatory cohort during this campaign.

Historical controls may lack player-level exports. Use bounded saved-weight
inference on the same rows for J_POINT_BOTH and J_ACTION_BOTH only, and include
that cost in preflight. Do not refit controls or require exhaustive exports for
every archived model. If a required control export exceeds the analysis budget,
bring the scope back before launch, not silently omit it after training.

## 6. Temporal design, fitting and calibration

Unchanged48 origins,44 primary quarters2016–2026;2015 is calibration warmup.
At origin t, inner training is the prior five-year window before the preceding
quarter; that preceding quarter supplies early stopping. Fresh final fit uses
the appropriate dated parent and all eligible data before t, for the selected
epoch count. Outer quarter t is never used to choose epochs, masks, gate
parameters, initialization or normalizers.

Keep Adam lr.001, weight decay.0001, gradient clipping5, epoch cap96, patience8,
minimum improvement1e-5, existing best-versus-patience semantics and730-day
training recency. Game-preserving batches and shared prefix event/point loss
normalizers remain unchanged. Three seeds17/23/41; no silent seed reduction.
Retain selected final and last-min(5,selected)-checkpoint prediction means.

Primary estimand: possession-weighted off5-quarter offensive ratings against
actual opponents, broad>=50 cells, no profile-support gate. Report all/novel/
recurring/thin/debut and below50 separately. Prior-completed-quarter affine
calibration is common across arms, corrected player-ID schema, nonnegative
slope and original cold-start rules. Never calibrate on the evaluated quarter.
Report direct, half, checkpoint-average and checkpoint-average-half;
**half is primary**, not whichever view wins afterward. Native event/point
losses and quarter-bias decomposition remain separately visible.

## 7. Registered comparisons and interpretation

Nine mechanism contrasts, all primary half-view broad RMSE:

1. A_CONTEXT − J_POINT_BOTH.
2. A_SELECT − J_POINT_BOTH.
3. A_GATE − J_POINT_BOTH.
4. A_CONTEXT_GATE − A_CONTEXT.
5. A_CONTEXT_GATE − A_GATE.
6. A_ACCOUNT − J_POINT_BOTH.
7. R_ALLOC − J_POINT_BOTH.
8. R_ROUTE − R_ALLOC.
9. R_ALLOC − J_ACTION_BOTH (same allocation architecture, changed objective).

Add each new arm against additive_defense and parent_half_defense: **23 total**.
10,000 paired season-block bootstrap draws, RNG180928, exact2^11 season swaps,
Holm over23. Report deltas, intervals, season wins, leave-one-season-out
sensitivity, and cohort counts. All other views/slices are descriptive.

For those same9 contrasts ×4 event families, report a separate **36-test event
family** with season-block intervals/exact swaps/Holm36, clearly labeled as a
separate family rather than global error control across all findings. Compare
loss/exposure sums; do not average quarter losses equally. Player-role and
transfer diagnostics are descriptive; uncertainty claims receive their own
limitations, not a surprise significance search. No arm selection by an
individual favorable channel.

Interpretation rules:

- Removing inputs and tying prediction with clearer mechanisms is meaningful;
  a small favorable point estimate alone is not equivalence or superiority.
- Gate success requires observed calibration/transport benefits, not attractive
  gate values. Gates are not posterior trust or causal skill estimates.
- A_ACCOUNT tying the full model would narrow the case for learned messages,
  not disprove complementarity: accounting still interacts skills.
- R_ROUTE tests an input pathway; it does not identify pure ability. Positive
  player-share results without better conversion/point/coherence are partial.
- A named synthetic ranking is never an optimizer target or sole acceptance
  rule. Judge each side's offense and defense as well as margin.

## 8. Coherence, product mode and uncertainty

Reuse all32 v17 fixtures at10 dates, including mirrors, clones, creator swaps,
spacing, center/guard, real small-ball, rebound and thin/stale/debut cases.
Export native player/channel/renewal ledgers and calibrated direct/half totals.
For gate arms include family gains and metadata; for allocation arms include
team/actor shares, workload and pre/post-constraint conversion. Test independent
slot permutations and team-swap margin antisymmetry. Preserve the Korver mixed-
era transport caveat; no selective player-profile update to force a conclusion.

Keep frozen two-big/low-creation analogue definitions and all-member tables;
top/bottom outcomes are descriptive with their own verified intervals. Compare
raw/adjusted-context removal sensitivities as diagnostics, not trained controls.
No exhaustive all-fixture×all-reference integration: batch ordered fixture
matchups, as the fast v17 implementation does.

All new direct/half models get512 prior-average-opponent integration, plus the
same first20 cells/date4096 sensitivity. Reuse compatible control results and
record equality of row keys/reference IDs. Primary point comparisons remain
actual-opponent conditional forecasts; average-opponent targets are still
realized outcomes, not neutral-opponent ground truth.

Candidate-specific prior-only U0 for direct/half, plus U1 constant persistent
discrepancy with the original balanced-game pairs. Validate broad and all-off5
summaries, all five slices, and transfer membership where intervals exist.
Compare coverage, width and proper scores on matched identified populations;
cold/not-identified remains explicit. No new U2 architecture, borrowed bands,
coverage gate or inference-time independent feature jitter.

**Mandatory v17 regression:** per-cell FINITE_GAME_BAND is valid; aggregate OK
is a different schema. Validate bounds/coverage/interval-score arithmetic and
test a real historical quarter with nonzero identified rows. Repair this in
new v18 producers; do not edit frozen v17 files. Wider seed spread is not a
hypothetical-quality interval. Honest synthetic latent uncertainty remains open.

## 9. Runtime budget:54 hours total, not54 hours of training

Measured v17:25.27 supervisor hours;24.60 training-queue hours and66.33 accumulated
fit worker-hours. Five-arm averages are misleading: event-only stopping took
longer. Measured per144-case worker-hours: O_ORDER11.70, D_SHAPE11.96,
O_FLOW13.06, O_FLOW_D_SHAPE13.24, O_FLOW_EVENT16.37.

The144 archived J_ACTION_BOTH versus J_BOTH final fits supply a more relevant
allocator cost: median matched **per-epoch ratio1.612**, interquartile1.528–1.740.
Total historical worker-hours23.90 versus15.04 with similar median selected
epochs12 versus12.5. Sources: v16 fast2_ready per-case fit_summary.json and v17
_summary/training_cases.csv; v17 queue summaries distinguish wall from worker
time. This is why the initially considered eighth event-only fit was removed.

Budget scenarios, **not measured v18 timings or confidence bounds**:

| Component | Reference assumption |
| --- | ---: |
| A_CONTEXT, A_SELECT, A_ACCOUNT | 3 ×11.70 worker-hours |
| A_GATE, A_CONTEXT_GATE | 2 ×12.29 worker-hours (5% overhead allowance) |
| R_ALLOC | 18.84 worker-hours (1.61× O_ORDER) |
| R_ROUTE | 20.72 worker-hours (additional10% for receiver-only evaluations) |
| Total fitting | about99.2 worker-hours |
| Three workers plus observed scheduling overhead | about36.8 wall hours |
| Bounded preparation/pilots | up to1.5 wall hours initially budgeted |
| All exports/scoring/analysis/final verification | 4 wall hours budgeted |
| Contingency to54-hour target | about11.7 wall hours |

Thus the working reference is about42.3 hours including pilot/analysis allowance,
with a20% training-time stress scenario about49.7 hours. These are not promises
that seven arms always finish in that time.54 hours is2.14× the
measured25.27-hour v17 run; the user’s approximate2.3× is not permission to
spend58 hours. Human implementation/discussion time is outside compute runtime.
No unnecessary full-prefix input validation rebuild: reuse receipt-verified
contexts and audit changed paths only, with final source integrity checks.

Preflight must replace multipliers with measurements:

1.12 inner-training batches per arm at2016q1 and2026q4, seed17; finite gradients,
   serialization and cache parity, no outer-error-based arm choice.
2. One complete inner/final pilot per arm at2016q1/seed17, with export/scoring;
   at most two additional late-origin fits, R_ALLOC and R_ROUTE, only if
   the microbenchmarks leave late-size/epoch timing unresolved. Budget them.
3. Compare3-worker throughput/memory to the measured v17 setup, one BLAS/torch
   thread per worker. Project case-level overhead as well as epoch computation.
4. Estimate all derived stages, particularly control player-level replay,
   average-opponent integration and uncertainty; verify physical free disk and
   projected artifacts plus10GiB reserve before launch.

Launch only with a written reference projection<=48 hours **including** spent
pilots and downstream work, and an explicit+20% training-time stress scenario
within54 hours. If that fails, optimize without changing math, or discuss scope
with Adam. First deferrable arm is A_CONTEXT_GATE (its ingredients remain);
R_ROUTE_EVENT is already deferred, not spare capacity to restore automatically.
Any further reduction needs Adam's agreement, an amendment and re-enumerated contrasts
before production; no automatic omission or performance-based screening.

54 hours is a planning target, not a process kill timer. Do not truncate valid
fits or alter stopping mid-run to hit it. Report updated ETA/slippage and ask
before material expansion. No indefinite monitoring loop needed: detached
runner and durable progress logs continue without an assistant turn.

## 10. Implementation order and acceptance tests

**A. Protocol and input routing.** New v18 protocol/model files; immutable source
references and an explicit field-to-path table. Reuse existing engines without
editing their frozen producers. Create schemas for masks/gates/role exports.

**B. Correctness before expensive fitting.** Tests must establish:

- Baseline mode reproduces J_POINT_BOTH; allocation mode with point weight0
  reproduces J_ACTION_BOTH. A_GATE at g=1 reproduces its ungated counterpart.
- Excluded inputs have zero influence on the specified paths; changing them
  cannot enter through cached defender summaries, rebound donor branches or
  frozen assisted-fraction paths. Distinguish fixed own historical context
  from proposed-current-teammate information.
- R_ROUTE blocks the direct raw conversion path but preserves indirect changes
  through workload/shortage. Hold assigned actions/constraints fixed when
  testing path isolation; don't demand the whole model ignore roles.
- Gates get finite, nonzero gradients away from degenerate all-zero adjusted
  heads; metadata and feature-family indexing are correct for both banks.
- Slow reference and optimized cached forward/loss/gradients agree on all arms,
  including gated reaggregation and the arm-specific frozen nuisance outputs.
- Probabilities normalize, FGA+.44FTA+TO conserves action mass, rebound renewal
  terminates, and points match the2/3/1 ledger. No extra point residual head.
- Slot permutations, duplicate profiles, unseen players, zero/support extremes,
  frozen FT output and independent team-swap behavior remain valid.
- Prefix input dates/normalizers/parents/epoch-selection and calibration windows
  stay disjoint from outer evaluation. Reject receipt/config mismatches on resume.
- U0 writer/summary contract is tested end-to-end on a real identified quarter;
  U1 cold start is allowed. No acceptance solely from file existence.

**C. Bounded pilots and full runtime gate.** Do the measurements above; report
timings and quantitative parity. No broad pilot accuracy tournament, no new
hyperparameter search and no48-origin sweep labeled a smoke test.

**D. Production runner.** Three independent CPU workers; retain chronological
calibration. A small ready queue may keep workers occupied across adjacent
origins once dependencies are prepared, while scoring waits for complete prior
origins. Treat that only as an optional mathematically identical scheduling
optimization with its own tests, not a prerequisite or a changed data cutoff.
Durable per-case epoch/batch logs plus supervisor stage/case counters, ETA ranges,
view/slice/sort leaderboard, and receipt-backed resume. Don't poll constantly.

**E. Automatic analysis and independent review.** All specified scorecards,
23 point contrasts,36 event contrasts, player allocation diagnostics, transfer
cohort, average mode, fixtures, U0/U1 and final handoff run automatically.
Independent review recomputes headline metrics from forecasts and verifies
source immutability. Training completion alone is not campaign completion.

Suggested module boundary: joint_capability_v18_protocol/model, v18_fit/case,
v18_run/report, v18_role_analysis, v18_summary, versioned uncertainty adapter.
Avoid wholesale rewriting of the mature loss/ledger/runtime infrastructure.
Bounded helpers may be reused by import if their frozen behavior fits exactly.

## 11. Deliverables and authority

Before launch: implementation receipt, tests, arm/parameter table, frozen code
and data hashes, measured runtime/storage scenarios, verified background-launch,
live-log/status/leaderboard commands. Do not publish speculative runnable
commands before the scripts exist. Full launch requires Adam's explicit approval.

At completion: original native fits and loss curves; chronological predictions;
all-view/slice/season point and event tables; registered contrasts; role/transfer
outputs; full fixture ledgers and real analogues; direct/half U0/U1 tables with
valid statuses; runtime/failure record; independent review and one current
handoff/state/scorecard. Preserve original artifacts; new output namespaces only.

Not included: scraping, database mutation, upstream input reconstruction,
tracking access, cross-team possession-entry labels, full adjusted-only decoder,
new assisted-shot supervision, multi-timescale state fitting, learned blend
selection, new U2 architecture, serving integration, promotion or deployment.
Read-only database access is not intrinsically forbidden, but this design does
not need it. Reopen any excluded work explicitly instead of slipping it into
the54-hour campaign. All implementation is direct, no agent delegation.
