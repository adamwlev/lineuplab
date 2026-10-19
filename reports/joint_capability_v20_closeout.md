# V20 closeout and next-decision notes — 2026-10-09

Adam requested that the analysis, loose ends and implementation be documented
and committed. This record closes the completed research campaign; it does not
authorize a next training run, data refresh, deletion, promotion or deployment.

## What is closed

| Work | Final disposition |
| --- | --- |
| Training and point scoring | All 864 native case slots and 48 origins complete; no retraining needed |
| Post-training failure | Null optional compact-path bug repaired in versioned consumers; original producers/logs retained |
| Automated analyses | All 19 stages complete: five reused, 14 in the continuation; all arithmetic audits pass |
| Scientific review | [Full review](joint_capability_v20_scientific_review.md) covers prediction, coherence, uncertainty, event losses, role/transfer cohorts, bias, seed/epoch behavior, risk and average-opponent integration |
| Independent checking | 192 point metric rows reproduced; exact populations/targets/weights checked; 73 v20 tests pass |
| Earlier bias investigation | Scripts, quantitative findings, input provenance and methodological limitations preserved; no correction fitted |
| External perspective | Adam's [Opus 5.5 review](../docs/history/OPUS_55_review_100626.md) preserved unchanged as advisory evidence; responses and qualifications in the roadmap |
| Restart documentation | Current handoff/state/scorecard/backlog synchronized; stale v19 README and v14/v15 architecture entry point corrected |
| Historical pending tasks | Old v16 repair, reliability and multi-model ensemble checklists retired from the active backlog; exact text archived and completed evidence linked |
| Git checkpoint | Source, tests, reports, current guidance, historical snapshots and compact evidence included; bulk cache artifacts excluded |

The original production root still says FAILED_REVIEW_REQUIRED, and the
continuation says READY_FOR_SCIENTIFIC_REVIEW. Both are accurate immutable records
of their own scope. This subsequent scientific review closes the campaign; there
is no missing training job, audit or automatic stage to restart.

## Judgment and rationale

**Keep P_BASE/J_POINT_BOTH as the research reference, not a publicly promoted
product.** The primary blend's r² .162989 exceeds additive_defense .146023;
novel-lineup r² is .144502 versus .118400. The NN remains useful. V20 does not
establish that its new profile adjustment or selection rule improves that
reference. It also does not remove the unresolved product limitations.

Three distinctions should survive this checkpoint:

1. **Adjusted profiles are not a single yes/no idea.** V16's original
   lineup-adjusted banks helped. V20's additional clock adjustment did not
   demonstrate an incremental benefit. We should retain the former without
   repeatedly tuning the latter until it wins. This is not proof that all game
   situation adjustment, or observational identification, is exhausted.
2. **Event fidelity is real progress but not sufficient evidence of transport.**
   Context improves conditional event forecasts, and S5 improves some count losses.
   Yet neither makes unusual combinations reliably more coherent. We should
   report those narrower wins, not call the entire campaign either a breakthrough
   or a failure. The permission to accept a small r² cost remains active when a
   meaningful coherence/uncertainty gain is demonstrated; this campaign did not
   demonstrate that trade.
3. **A precise calculation can answer a weak question.** The exhaustive risk
   threshold took 8.49 hours and yielded four supported primary tail observations.
   Better batching solved runtime mechanics, not inferential power. Future
   diagnostics need a relevant population and plausible sample size before a
   large inference pass, with choices fixed without outcome-selected thresholds.

I am most interested in whether **defensive coverage and possession renewal
reward size/recovery without sufficient costs for perimeter coverage and primary
creation**. The retained model already includes creation penalties and reports
role stretch; the question is whether they constrain the relevant computations
at the right stage. The current defense broadcasts channel-specific effects,
and renewal can magnify differences. These are architectural clues, not proof
of the cause. Equal logit shifts are not equal point effects. We must inspect
the actual computation before building around a story.

The evidence does not support simply blaming the additive half: pure NN also
favors the five centers. It does not support chasing hot shooting residuals:
their repeatability is weak. It does not support declaring an accuracy ceiling:
game-split reliability is assumption-dependent. It does not support solving OOD
by widening all bands indiscriminately: proper scores and observed coverage must
improve, and latent synthetic quality remains unverifiable from these fixtures.

## Proposed next sequence — not a frozen experiment

1. Agree a bounded saved-weight diagnosis, before another fit. Use existing
   diverse fixtures and supported real analogues; separate offensive and defensive
   point ledgers, FTA, opportunity allocation, conversion/location and recovery.
   Check saturation and controlled generic capability perturbations. Include both
   matchup directions and pure NN/additive/blend; avoid selecting cases solely by
   a desired ranking. Code interventions locate sensitivity, not causal effects.
2. If that identifies a defensible failure domain, freeze a small structural
   experiment: retained baseline, flexible attacker-specific defense control,
   and a constrained shared-capacity/assignment candidate. Isolate assignment
   value from merely adding flexibility. Preserve exact baseline initialization
   explicitly; uniform Sinkhorn weights do not automatically reproduce nonlinear
   mean/SD pooling. Account for help and switching rather than treating strict
   one-to-one coverage as basketball truth.
3. Predeclare forward unfamiliar-composition tests and realistic support
   populations, retaining the old benchmark for continuity. Earlier-era height
   analogues are leads, not equivalent roles or measured five-center ground truth.
   Specify acceptable predictive tradeoffs, mechanism checks and uncertainty
   comparisons before fits. No fixture labels or named-player bonuses.
4. Keep a private tool/export workstream separate from new model research if
   Adam chooses it. The tool can expose retained forecasts, additive comparison,
   mechanism explanations and limitations without claiming a three-pillar pass.
   Public promotion and newly acquired data need separate authority.

No arm roster, exact predictive tolerance, refit budget or launch date has been
agreed for the next experiment. This deliberately remains a decision boundary,
not an incomplete v20 deliverable or permission for automatic implementation.

## Open questions and deferred work

| Item | Why it remains open / next condition |
| --- | --- |
| Five-center mean and free throws | All eight arms remain incoherent; diagnose coverage/renewal before another generic feature sweep |
| Hypothetical latent-quality intervals | Finite-game coverage and wider fixture bands cannot certify them; observed composition holdouts and named assumptions needed |
| Risk reference population | Four supported primary tail cells are underpowered; predefine a relevant prior cohort or continuous descriptor/noise test |
| Dated role adaptation and injury/transaction cases | Current libraries are retrospective; genuine event identification and prospective information contracts still needed |
| Cross-era player transport | Korver override does not transport all banks consistently; no strong cross-era chemistry claim |
| Rebound facilitation | Distinguish collector skill from improving teammates' boards; no required Adams/Robinson ranking |
| True FT trips, possession entry, tracking | Potentially valuable new targets/inputs; feasibility, temporal safety and acquisition scope not authorized here |
| Selection/cohort bias | October 6 diagnostics establish associations, not optional-stopping causation; no future-exposure bonus or universal bias offset |
| Prospective validation | Reused seasons are development evidence; freeze future update/selection rules before evaluation |
| Credentials/environment portability | Existing credential exposure and environment locking need a separate scoped migration/rotation assessment; no credentials copied into new notes or evidence |
| Public product | Legacy additive page remains unchanged; export, UI, release and automated updates not part of this checkpoint |

## Artifact cautions resolved by explicit guidance

- `bias_within_quarter.csv.gz` in the original summary omits the environment
  column. Do not pool its reference and conditional rows. Use the independently
  reconstructed, reference-only `quarter_bias.csv` in the review directory.
  This metadata issue does not affect registered contrasts or the leaderboard.
- The earlier bias summary's field `focus_noncorner_three_shortfall_fraction`
  refers to location bucket 5, a distance-based proxy, **not tracking-derived
  corner/noncorner geometry**. Preserve original producer/output hashes and
  interpret the exported name with this caveat; no geometric claim is warranted.
- Historical archived Markdown links may be root-relative by design. Current
  navigation points to the original targets; historical snapshots are not new
  operational instructions.
- The staged whitespace check reports four existing extra EOF blank lines: the
  October 8 archived handoff and the three versioned inference consumers. Their
  exact historical/frozen bytes are preserved. Excluding those four files, the
  staged whitespace check passes; all 270 checked current local documentation
  links resolve, and the compact bundle's producer/output hashes match.
- Checkpoint averaging is prediction/physical-ledger averaging, not weight
  averaging; uncertainty populations, primary cohorts and conditional-context
  scores must not be mixed. Full definitions are in the frozen plan and review.

## Evidence and verification

Bulk local data, trained checkpoints and per-case outputs remain under
`experiments/cache/`. **A git commit is not a backup of those local artifacts**
and does not make this a reproducible fresh-clone distribution.

The small [committed evidence bundle](evidence/v20_closeout_2026_10_09/README.md)
contains exact point/contrast/risk/coherence/training/bias extracts and hashes.
The closeout verifier checks 284 frozen native source/receipt dependencies,
104 review-input hashes, 192 independently reconstructed metric rows, eight
bias-summary input hashes, the completed continuation and all original/reused/new
queue receipts. It does not reread every multi-gigabyte training tensor or rerun
the already completed native inference audits. Those remain preserved evidence.

Verification command (fresh destination only):

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
 /Users/adam/miniconda3/envs/basketball25/bin/python -u \
 -m experiments.v20_closeout --out <fresh-output-directory>
```

The first closeout-verifier attempt assumed that the training queue had the same
summary schema as analysis queues; it stopped before creating its destination.
The verifier now reads the training queue's explicit final status separately.
The successful rerun and original attempt are both retained in
`experiments/cache/v20_closeout_2026_10_09/verification.log`. Neither changed any
run artifact or numerical result.

Resume the discussion from [current handoff](../docs/history/SESSION_HANDOFF.md), not an old
launch command. Read [scientific review](joint_capability_v20_scientific_review.md)
for numerical details and [roadmap](../MODEL_RESEARCH_ROADMAP.md) for priorities.
