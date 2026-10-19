# V19 completed scientific review — 2026-10-04

## Decision

Retain J_POINT_BOTH as the point reference. V19 establishes that shared game
situation helps explain basketball events, including shooting and recovery—not
only free throws. It does **not** establish better common-environment player
values, better role transport, a solution to the center-heavy counterfactual,
or validated uncertainty about arbitrary lineups' underlying quality.

This is useful evidence for upstream context-adjusted profiles and a bounded
training-stability comparison. It is not a reason to abandon the useful NN or
declare context adjustment exhausted. No scorer promotion, deployment or new
fits were performed during this review.

## Completion, integrity and population

- All 720 cases / 1,440 inner-final fits and 48 rolling scorecards completed.
  Training/scoring took 49.24 hours; average-opponent integration 2.39 hours.
  The repaired ten-stage post-training continuation completed in 5,792 seconds
  (1.61 hours). These stage times exclude the intervening failure/debugging gap.
- The original post-training failure was observed-label accounting, not failed
  training. Three input rows have recorded points inconsistent with FG/FT
  reconstruction; two occur in 2015 evaluation warmup, **none in primary
  2016–2026 evaluation**. The [repair report](joint_capability_v19_accounting_repair.md)
  records the explicit observed-accounting component and unchanged targets.
- Independent point audit: 144 environment/origin panels, 5,472 calibration
  checks, maximum error 5.68e-14 points/100. Native audits cover all 720 cases,
  both prediction estimators and environments; maximum point-ledger error
  1.14e-13, event-loss error 6.66e-16. These are arithmetic audits, not proof of
  causal identification or of every upstream assumption.
- This review independently recomputed 270 metric rows from saved ensemble
  predictions, checked identical keys/targets/exposures across nine arms,
  verified half-blend arithmetic and 19,926 mirrored matchup records. All pass.
- Primary point population: **8,345 offensive-lineup-quarter cells, 1,013,999
  possessions, 44 quarters / 11 seasons (2016–2026)**. Three seeds are averaged
  before scoring. The 2015 quarters are calibration warmup. “All” is this matched
  >=50-possession cohort, not every NBA possession. Defensive lineups faced
  enter the forecasts. RMSE/MAE/bias are points/100; bias is predicted minus actual.
- The frozen 17 reference-half point contrasts and 28 actual-context event
  contrasts retain their original season-block bootstrap, exact sign-swap and
  Holm families. Other views and slices are descriptive. The historical seasons
  have been reused in model development; this is not fresh prospective evidence.

## 1. Predictive accuracy: no new incremental point winner

Reference predictions integrate physical event ledgers over a common past-only
context distribution. They do not know future clock/score exposure. Half is
50/50 calibrated NN and additive_defense; checkpoint averaging averages saved
predictions, not weights.

| Model | Direct r² | Half r² | Checkpoint-average-half r² | Half RMSE | Half MAE |
| --- | ---: | ---: | ---: | ---: | ---: |
| O_ORDER, retained comparator | .162077 | .163049 | .162999 | 11.054064 | 8.297513 |
| J_POINT_BOTH, retained reference | .161925 | .162915 | .162989 | 11.054951 | 8.299892 |
| C_FIXED, frozen capability + clock | .161930 | .162937 | .162939 | 11.054805 | 8.299948 |
| C_CLOCK, jointly learned capability + clock | .154525 | .159471 | .161697 | 11.077670 | 8.317380 |
| C_FULL, context in additional event channels | .153849 | .159127 | .161724 | 11.079936 | 8.321868 |
| C_ALLOC, clock + allocator | .150282 | .158154 | .161263 | 11.086342 | 8.325250 |
| C_MARGIN, extra score-margin sensitivity | .148436 | .156975 | .159602 | 11.094101 | 8.335999 |

The equally informed additive_defense control has r² .146023 / RMSE 11.165936;
parent_half_defense has .156601 / 11.096562. Every new primary half arm beats
additive_defense after the registered correction. That preserves the broader
NN advantage, but it is not an incremental v19 success.

Selected registered half-RMSE differences (negative favors the left):

| Contrast | Difference | Season-bootstrap 95% interval | Season wins | Holm p |
| --- | ---: | --- | ---: | ---: |
| C_FIXED − J_POINT_BOTH | −.000146 | [−.000310, +.000003] | 7/11 | .888672 |
| C_CLOCK − J_POINT_BOTH | +.022719 | [+.008629, +.039520] | 1/11 | .064453 |
| C_CLOCK − C_FIXED | +.022865 | [+.008889, +.039528] | 1/11 | .058594 |
| C_FULL − C_CLOCK | +.002267 | [−.001468, +.005798] | 4/11 | 1.000000 |
| C_ALLOC − R_ALLOC | +.026249 | [+.006253, +.047715] | 3/11 | .320312 |
| C_MARGIN − C_CLOCK | +.016432 | [+.006984, +.025720] | 2/11 | .105469 |

No intended incremental point improvement clears the registered correction.
Unadjusted bootstrap intervals and corrected tests answer different questions;
do not call the joint-model regressions Holm-significant at .05.

### Training and calibration are part of the story, not the entire explanation

Checkpoint-average-half recovers C_FULL from .159127 to .161724, versus the
same-view reference .162989. C_CLOCK and C_ALLOC also recover substantially.
Native r² improves with averaging too (C_FULL .143561 → .148694), so this is
not merely an artifact of the downstream calibrator.

The direct C_CLOCK MSE gap to J_POINT_BOTH is 1.0804: about .3028 comes from
quarter-level mean errors and .7776 from within-quarter error. For C_CLOCK,
checkpoint averaging reduces within-quarter MSE 120.7546 → 120.1788 even while
quarter-bias MSE increases 2.6822 → 2.7995. Thus “just fix the intercept” is not
a sufficient diagnosis; the remainder also includes spread/ranking errors.

Primary median selected epochs: C_FIXED 24, C_CLOCK 12, C_FULL 13, C_ALLOC 12,
C_MARGIN 14.5; no primary cap hits. Averaging helps, but neither proves a
stopping-rule bug nor licenses selecting epochs from outer evaluation. A
predeclared inner-only stabilization comparison is warranted. Increasing epoch
limits alone is not justified by these results.

## 2. What worked: context explains events beyond a mean correction

Actual-context scores condition on the realized game states. They are diagnostic
scores with additional information, not the fan-facing common-environment
forecast. Their point controls are equally informed prior-only nuisance controls.

C_FIXED conditional-clock direct r² is .181401; C_CLOCK .179206 and C_FULL
.178642 (checkpoint averages .181853 and .181960). The equally informed
J_POINT_BOTH_context control is .171472 and additive_defense_context .153946.
The frozen capability plus learned nuisance already captures much of the point
benefit; joint relearning is not necessary to establish that situation matters.

C_MARGIN conditional direct r² is .223626, versus reference .148436. Do not
treat the former as a new product record: score margin is partly an outcome of
player quality and uses future realized deployment. Better conditional prediction
does not identify better neutral-context player values.

The most useful mechanism result is **C_FULL versus C_CLOCK**:

| Actual-context event family | NLL difference, lower better | Season wins | Holm p, family of 28 |
| --- | ---: | ---: | ---: |
| Counts | −.00010670 | 11/11 | .027344 |
| Shot location | −.00093965 | 11/11 | .027344 |
| Conversion | −.00018528 | 11/11 | .027344 |
| Recovery | −.00041280 | 11/11 | .027344 |

These small, consistent proper-loss gains show that count-only context is too
narrow for conditional event prediction. They do not establish the full plan's
stronger branch of improved reference behavior as well. Conversion learning
should not be declared permanently closed.

C_FIXED improves counts against J_POINT_BOTH (−.00220469, Holm .027344), but
has a tiny conversion cost (+.00000325, also Holm .027344), consistent with
coupled physical accounting. C_CLOCK does not establish an additional event
win over C_FIXED. C_ALLOC improves counts against old R_ALLOC, but its extra
count gain against C_CLOCK does not survive Holm (.117188).

Native count biases across the wider event-valid primary evaluation population:

| Model/environment | FGA/100 bias | FTA/100 bias | TO/100 bias |
| --- | ---: | ---: | ---: |
| J_POINT_BOTH, no context | −.081 | +.076 | −.077 |
| C_FIXED, actual context | −.246 | +.607 | −.099 |
| C_CLOCK, actual context | −.022 | −.133 | +.044 |
| C_FULL, actual context | −.059 | −.132 | +.037 |
| C_ALLOC, actual context | −.088 | −.043 | +.072 |

These use channel-specific observation masks: 2,505,033 FGA-exposure,
2,746,029 FTA-exposure and 2,760,546 turnover-exposure possessions, **not** the
1,013,999-possession broad point cohort. Near-zero overall count bias can coexist
with systematic subgroup error. Do not compare this table directly with the
older broad-cohort FTA bias +1.890 or infer that every cohort is now calibrated.

Supported residual persistence reinforces that distinction. At threshold100,
mean FTA residual correlations over the five registered random-game splits are
.2828 for the context-free reference, .1979 C_FIXED, .1715 C_CLOCK, .1739 C_FULL
under actual context. Chronological counterparts are .2283, .1459, .1263,
.1272. These are reductions, not elimination; conditional point persistence does
not uniformly fall. The full covariance matrices remain authoritative; component
errors are not independent. Do not compare these high-support correlations to
the previous threshold20/all-cohort conversion summary as if populations match.

All primary learned context tables have zero saturated coordinates under the
registered tanh threshold. The full supported observed-curve cohort was exported
and audited, not selected on favorable errors. Bounded effects and correct ledgers
do not themselves prove plausible extrapolation.

## 3. Basketball coherence, roles and transport

Novel lineups: 3,489 cells / 361,361 possessions; half r² J_POINT_BOTH .144082,
C_FIXED .144140, C_CLOCK .140155, C_FULL .139961, C_ALLOC .138433. No novel-lineup
gain from joint context fitting.

Original transfer cohort: 146 cells / 47,419 possessions. Half RMSE reference
6.674457, C_FIXED 6.673352, C_CLOCK 6.713951, C_FULL 6.721401, C_ALLOC 6.768853,
C_MARGIN 6.696149. These descriptive comparisons do not support improved transport.

The 907 retrospective large-FGA-share-change cases show modest allocation progress:
share MAE falls from 4.3674 percentage points for J_POINT_BOTH to 4.2965 C_ALLOC
(old R_ALLOC 4.3142; unchanged-prior predictor 6.3963). This is an outcome-selected
diagnostic, not a prospective role-change win. On the original 2,139 role-change
lineup cells, half r² falls from .181020 reference to .176268 C_ALLOC.

Center-heavy counterfactuals remain problematic. At 2026q4 against the fixed
Jokić/Westbrook lineup, three-seed means are:

| Model | Centers' calibrated offense | Opponent's offense | Centers' direct margin | Centers' FTA/100 |
| --- | ---: | ---: | ---: | ---: |
| J_POINT_BOTH | 120.285 | 115.579 | +4.707 | 31.161 |
| C_CLOCK | 119.380 | 115.669 | +3.712 | 35.543 |
| C_FULL | 119.589 | 115.541 | +4.048 | 35.271 |
| C_ALLOC | 119.604 | 115.896 | +3.707 | 37.069 |
| C_MARGIN | 118.986 | 116.270 | +2.716 | 35.508 |

All nine evaluated models still favor the legal-center fixture against both
Jokić fixtures. A somewhat smaller margin is not a solved offense mechanism:
new joint models actually increase its free-throw projection. Against the three
fixed prior-common opponents, legal-center FTA rises from 31.927 reference to
36.950 C_FULL; five-Gobert FTA from 34.475 to 40.997. This is an extrapolation
warning, not permission to force a center penalty.

Observed two-big analogues (65 cells / 8,471 possessions) retain positive half
bias: reference +3.048, C_CLOCK +3.469, C_FULL +3.336, C_ALLOC +3.239 points/100.
The small real analogue cohort also does not show the desired improvement.

Rebound same-four fixtures still give Robinson higher capture than Adams:
against the three prior-common opponents in 2026q4, reference .3308/.3233 and
C_FULL .3270/.3183. No newly identified teammate-facilitation effect. Korver's
mixed-date feature limitation remains; these fixtures cannot settle a universal
Jokić/Korver/Westbrook chemistry ranking.

Average-opponent half r²: reference .148368, C_FIXED .148369, C_CLOCK .145345,
C_FULL .145278, C_ALLOC .143837. These are 512 prior-opponent integrations
evaluated against realized outcomes, not observed neutral-opponent ground truth.

## 4. Uncertainty: useful finite-game controls, no latent-OOD solution

The automated pooled uncertainty tables include 2015 warmup. This review
re-pools their original quarterly sufficient statistics over 2016–2026 only,
matching the point population and previous independent reviews. Original tables,
bands, residual fits and scoring rules are unchanged. Use review2's
`finite_uncertainty_primary.csv` / `persistent_uncertainty_primary.csv` for these
comparisons. This is a population clarification, not a training or band repair.

| Half model, nominal95 U0 | Cell coverage | Possession-weighted coverage | Mean width, points/100 | Interval score, lower better |
| --- | ---: | ---: | ---: | ---: |
| J_POINT_BOTH | 93.47% | 93.19% | 47.824 | 60.671 |
| C_FIXED | 93.48% | 93.19% | 47.835 | 60.669 |
| C_CLOCK | 93.62% | 93.10% | 48.019 | 60.736 |
| C_FULL | 93.68% | 93.20% | 48.109 | 60.731 |
| C_ALLOC | 93.57% | 93.15% | 47.983 | 60.797 |
| C_MARGIN | 93.90% | 93.36% | 48.455 | 60.800 |

Small coverage increases generally accompany wider bands, not better proper
scores. Debut weighted95% coverage remains low: reference90.49%, C_FULL90.89%,
C_ALLOC90.97%. No established uncertainty breakthrough.

U1 primary repeated-pair controls identify 2,037 of 2,095 eligible pairs.
Mean log score (higher better): reference −7.869949, C_FIXED −7.870684,
C_CLOCK −7.872718, C_FULL −7.873781, C_ALLOC −7.873956, C_MARGIN −7.877505.
Differences are descriptive. These are predictions of noisy observed outcomes
with deployment mismatch; neither U0 nor U1 certifies hypothetical latent-quality
coverage. No synthetic-quality uncertainty model was added in v19.

## 5. Implications for v20 — proposed, not frozen or launched

1. **Make upstream context adjustment the leading hypothesis.** Fit shared clock
   effects alongside player/channel effects in the adjusted profiles, respecting
   each row's own date and inner/final cutoffs. Historical deployment remains in
   the current inputs; decoder adjustment cannot guarantee removing it. Test the
   hypothesis rather than assuming that it explains the observed regression.
2. **Separate upstream and downstream changes.** A small profile-by-decoder
   comparison should include current profiles/no context, adjusted profiles/no
   context, current profiles/context, adjusted profiles/context. Preserve frozen
   capability+nuisance controls and the useful C_FULL event result. New profile
   semantics require NN refits, not blindly swapping inputs under old weights.
   Decide the exact decoder/arm roster before seeing new results.
3. **Bound training stabilization before another architecture sweep.** Compare a
   small, equally applied inner-only stabilization policy against the current
   selected checkpoint and fixed averaging policy. Preserve the old references;
   measure native/calibrated, bias/within-quarter and seed/epoch behavior. No
   outer-selected epochs, retrospective best checkpoint or assumed benefit from
   simply running longer.
4. **Test whether player effects can actually be recovered.** Synthetic examples
   with known player/context effects should include uneven deployment and weak
   overlap. They test identification behavior, not only gradients/accounting.
   Real prospective transport and matched cohort checks remain necessary. Clock
   is the first candidate; margin stays a separate endogenous sensitivity.
5. **Give uncertainty and transport their own modeling task.** Predeclare a
   past-only discrepancy/support hypothesis and evaluate noisy-game scores,
   repeated outcomes and supported transport separately. If latent quality is
   not empirically identified, say so and present uncertainty without a coverage
   gate. Do not spend another full campaign merely reproducing the same U0/U1
   tables while claiming progress on this pillar.

The next step is to agree and freeze a bounded v20 plan, including runtime and
its three-pillar acceptance evidence. None of these recommendations authorizes
a profile rebuild, new training campaign, database mutation or promotion.

## Reproduction and handoff

Original source: `experiments/cache/joint_capability_2026_09_30_v19_prod`.
Continuation: `experiments/cache/joint_capability_2026_10_03_v19_posttrain1`;
its `_summary`, `_evidence`, `_persistence`, `_audit`, `_native_review` and other
siblings are the completed derived stages. Original `_scored` and `_average`
remain at the original source prefix. All original artifacts are preserved.

Independent review: `experiments/cache/joint_capability_2026_10_04_v19_review2`.
Durable log: the same path plus `.log`. Review1 is preserved but superseded:
its selected count-event export was empty because the extended-ledger table does
not contain FGA/FTA/TO; review2 explicitly reads the count table and asserts all
three channels. Other original review1 results were unchanged.

To reproduce, use a **new, nonexistent** output prefix:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
/Users/adam/miniconda3/envs/basketball25/bin/python -u \
  -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v19_completed_review \
  --source experiments/cache/joint_capability_2026_10_03_v19_posttrain1 \
  --out experiments/cache/joint_capability_2026_10_04_v19_review3 \
  > experiments/cache/joint_capability_2026_10_04_v19_review3.log 2>&1
```

Seven combined review/accounting unit tests pass; the original repair additionally
passed its 13-test targeted/production suite and unchanged-quarter dataframe
parity checks. No active training or analysis launched by this review remains.
Documentation/code are uncommitted; the current task did not authorize a commit.
