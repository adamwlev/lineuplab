# v18 Scientific Review

September 30, 2026. The completed experiment tests seven representation and
role-routing changes against retained controls. It finds no established new
primary predictive winner, but does establish useful intermediate evidence:
learned teammate information contributes beyond mechanical accounting, and
the explicit allocator improves count prediction. Neither finding yet solves
role transport, implausible center matchups or hypothetical-quality uncertainty.

Retain J_POINT_BOTH as the research reference, with O_ORDER as the near-tied
ordering control. Keep R_ALLOC, R_ROUTE and A_CONTEXT_GATE as targeted research
candidates, not promoted scorers. Do not convert an exploratory slice or
checkpoint ranking into the registered winner.

## Completion and verification

The original `joint_capability_2026_09_28_v18_prod` campaign and every automatic
stage completed: 1,008 cases, 2,016 inner/final fits, 48 origins, three seeds,
41.188 supervisor hours. All fits stayed below the 96-epoch cap; median selected
epochs range from 8 to 11 among new arms. Another long run with more epochs is
not justified merely by the absence of a point improvement.

The automatic review verified 75,921 source/artifact files and independently
reconstructed 220 point metric rows. This follow-up additionally recomputed
all 264 transfer metric rows, verified antisymmetry across 8,118 seed-mean
fixture pairs, and exported full transfer cases plus equal-sized benefit/harm
tails. Maximum saved slot-permutation difference is 0.0001385 points/100,
within the combined absolute/relative numerical tolerance, not exact equality.
Twenty-two model, scoring, analysis and preview tests passed.

No fits, database access, upstream rebuilds, frozen-producer edits, promotion,
deployment or commit occurred in this review. The automatic pass establishes
artifact/arithmetic integrity, not causal identification or product acceptance.

## Prediction on the registered population

All tables here use three-seed prediction means. The primary target is
possession-weighted offensive-five quarter ratings against actual defensive
opponents: 8,345 cells with at least 50 possessions, 1,013,999 possessions,
44 quarters in 2016–2026. The 2015 quarters warm up calibration. These are
reused development seasons, not fresh prospective confirmation.

Half means 50% separately calibrated neural prediction plus 50% equally
informed additive_defense. Calibration uses earlier completed quarters only.
RMSE and MAE are points per 100; r² is unscaled weighted 1−SSE/SST.

| Model | Direct r² | Primary half r² | Half RMSE | Half MAE |
| --- | ---: | ---: | ---: | ---: |
| O_ORDER | .162077 | .163049 | 11.054064 | 8.297513 |
| J_POINT_BOTH | .161925 | .162915 | 11.054951 | 8.299892 |
| A_GATE | .161247 | .162629 | 11.056837 | 8.301255 |
| R_ROUTE | .159578 | .162308 | 11.058958 | 8.297882 |
| R_ALLOC | .160241 | .162136 | 11.060093 | 8.299963 |
| A_CONTEXT_GATE | .160636 | .161385 | 11.065046 | 8.318314 |
| A_CONTEXT | .160827 | .161092 | 11.066981 | 8.320469 |
| A_ACCOUNT | .152988 | .159740 | 11.075896 | 8.317255 |
| A_SELECT | .153629 | .158480 | 11.084199 | 8.336107 |
| Additive_defense | .146023 | .146023 | 11.165936 | 8.412297 |

The seven new half models all beat additive_defense under the registered
23-comparison Holm family. None establishes its intended incremental point
advantage. A_GATE minus J_POINT_BOTH RMSE is +.001887, season-bootstrap 95%
interval [−.002891, +.007627]. R_ROUTE minus R_ALLOC is −.001135
[−.011789, +.011206]. A_SELECT is descriptively worse by +.029248
[+.011992, +.046999], but its Holm p=.1465 does not pass the family threshold.
Intervals crossing zero do not prove equivalence.

### Checkpoint averaging and later seasons

R_ROUTE checkpoint-average-half reaches r² .163469 and RMSE 11.051291;
R_ALLOC .163316 / 11.052301; J_POINT_BOTH .162989 / 11.054459. This is a real
descriptive lead in the stored alternative view, not the primary result.
R_ROUTE beats the same reference view in 8/11 seasons. A supplemental paired
season bootstrap gives ΔRMSE −.003168 [−.011613, +.005321], still inconclusive.
This post-hoc comparison is not added to or substituted for the frozen family.

Reproduction of that sensitivity: use `point_season.csv`, broad/all,
checkpoint_average_half, sorted by season. Per season let SSE=weight×RMSE².
Resample 11 season indices with replacement 10,000 times using NumPy
default_rng(180930); subtract sqrt(sum SSE/sum weight) between R_ROUTE and
J_POINT_BOTH. Report the 2.5/97.5 percentiles; no selection-adjusted claim.

The earlier live lead was not a stable result: primary R_ROUTE half RMSE in
2026 is 11.88046 versus J_POINT_BOTH 11.81675. Averaging checkpoints reduces
some errors but retains a 2026 same-view deficit of .03123. This motivates
examining transport and training variability, not choosing a favorable endpoint.

### Novel lineups and average opponents

On 3,489 novel cells / 361,361 possessions, J_POINT_BOTH half r² is .144082,
R_ROUTE .141323, A_CONTEXT_GATE .142856, and additive_defense .118400.
Direct forecasts do better on this slice: O_ORDER .148813, J_POINT_BOTH
.148573, A_CONTEXT_GATE .148327. This does not authorize an outcome-selected
novel-lineup blending rule.

Average-opponent half r² is .148764 for O_ORDER, .148368 J_POINT_BOTH,
.148056 A_GATE, .147548 R_ROUTE and .132160 integrated additive_defense.
The same lack of a new overall winner appears in this product mode. The
512-versus-4096 integration sensitivity is about .055–.060 half-prediction RMS,
up to .152 points/100 on the first 20 cells per primary quarter. Those are
integration differences, not uncertainty bands; small arm gaps should not be
overinterpreted. Realized outcomes still reflect actual, not neutral opponents.

## What the mechanisms learned

The separate registered event family has 36 comparisons with season-block
resampling and Holm correction. Loss units differ by channel; their numeric
deltas must not be compared directly to points/100 or to one another.

| Contrast | Finding | Season direction | Event-family Holm p |
| --- | --- | --- | ---: |
| A_ACCOUNT minus J_POINT_BOTH | Worse counts, location and conversion | All three worse in 11/11 | .03516 each |
| R_ALLOC minus J_POINT_BOTH | Better count loss, Δ−.000178 | Better in 11/11 | .03516 |
| A_CONTEXT_GATE minus A_CONTEXT | Better count loss, Δ−.000108 | Better in 11/11 | .03516 |
| A_GATE minus J_POINT_BOTH | Lower location loss, Δ−.000047 | Better in 10/11 | .06055 |
| R_ROUTE minus R_ALLOC | Small favorable pooled changes in four channels | Mixed | 1.0 each |

The clearest conclusion is that trained current-teammate information is doing
useful predictive work beyond shared opportunity and rebound accounting.
A_ACCOUNT retains nonlinear accounting, own history and defense, yet loses
event fidelity. This is not proof that messages identify causal chemistry;
the ablation changes several paths and the pretrained initial function.

The allocator also does something measurable. Compared with J_POINT_BOTH,
R_ALLOC improves player share cross-entropy for FGA, FTA and turnovers on the
full broad population. The event-only J_ACTION_BOTH remains still better on
those three shares. Point supervision trades some event fidelity for points.
On transfer cells the allocator improves FGA and FTA shares but worsens turnover
shares: J_POINT_BOTH 1.565801 versus R_ALLOC 1.566993 and R_ROUTE 1.567010.
This is not a general role-transport victory.

The learned gates are active, not stuck at identity. Across the fixed fixture
panel, A_GATE offense gains span .861–1.342 and defense .251–1.346.
Median-of-family/seed/date medians are 1.023 and 1.073 respectively. These are
fixture distributions, not league estimates or posterior confidence. Gate
activity by itself does not establish more faithful reliability handling.

## Team changes and role allocation

The complete original registry maps with no exclusions. The substantial cohort
remains 146 lineup-quarter cells / 47,419 possessions, at least 200 possessions
and five games per cell. These are retrospectively identified opening-season
team changes, not a sample selected for large measured role changes. Multiple
movers in one lineup do not duplicate its possessions.

| Model | Direct RMSE | Half RMSE |
| --- | ---: | ---: |
| A_CONTEXT_GATE | 6.560252 | 6.648785 |
| J_POINT_BOTH | 6.651611 | 6.674457 |
| R_ALLOC | 6.674910 | 6.682901 |
| R_ROUTE | 6.761330 | 6.716741 |
| Additive_defense | 6.947335 | 6.947335 |

A_CONTEXT_GATE leads descriptively at all-cell, 100-possession and
200-possession transfer thresholds. At 500 possessions A_SELECT leads, but
there are only 12 cells. No transfer-specific significance claim or blend
selection follows. R_ROUTE's proposed role separation has not delivered a
transfer advantage here, and compact raw context has a potentially useful
transport tradeoff despite its overall point cost.

The new case export preserves every primary lineup with names, movers,
observed ratings, all four views, the J_POINT_BOTH reference and both error
tails. Illustrations, selected by weighted squared-error differences:

- The 2023 opening Minnesota Gobert/Towns/Russell/Edwards/McDaniels lineup
  has 522 possessions and observed 109.39. R_ROUTE half predicts 114.50 versus
  reference 115.18: an improvement, but both remain too high.
- The 2026 Houston Durant/Okogie/Şengün/Smith/Thompson cell has 258 possessions,
  observed 129.84, R_ROUTE 116.32 and reference 117.23: a harm example.
- A_CONTEXT_GATE helps the 2022 Washington Dinwiddie/Beal/Caldwell-Pope/Kuzma/
  Gafford cell, but it still predicts 116.54 versus observed 94.12. A relative
  improvement is not an explanation of that huge residual.

These examples are statements about the repository's recorded sample, not
causal effects of those transactions or proof of a role mechanism.

### Volume remains a distinct problem

On event-valid transfer exposure, observed FTA is 18.705/100, versus
J_POINT_BOTH 22.827, R_ALLOC 23.075 and R_ROUTE 23.116. Observed FGA is 89.965,
versus 88.419, 88.288 and 88.206 respectively. Improving shares among players
does not fix team volume. Overall broad FTA is also high, but less so:
observed 20.058 versus R_ROUTE 22.063. Denominators follow each event's masks.

Earlier game-situation findings remain relevant; these numbers do not by
themselves show that excessive FTA is missing synergy. Do not subtract a
cohort-fitted offset. Separate deployment mix, team action volume and player
allocation before changing the event process.

## Basketball coherence

All eleven models still favor the legal-center fixture against both Jokić
fixtures. Against the Westbrook version, direct center offense / opponent
offense / margin is:

| Model | Center offense | Opponent offense | Center margin |
| --- | ---: | ---: | ---: |
| J_POINT_BOTH | 120.285 | 115.579 | +4.707 |
| R_ALLOC | 119.612 | 115.459 | +4.153 |
| R_ROUTE | 119.971 | 115.880 | +4.091 |
| A_CONTEXT_GATE | 119.853 | 116.257 | +3.597 |
| A_ACCOUNT | 123.061 | 112.372 | +10.689 |

R_ROUTE's smaller margin is not a solved offense or defense mechanism. Its
centers still generate 31.61 FTA/100 and 15.18 native renewed-possession points.
Against three dated prior-common opponents, their mean direct offense is
114.754, close to J_POINT_BOTH 114.946. Those three references are not a full
league-average integral. The failure is matchup-sensitive, not simply every
center lineup receiving a fixed excessive offense score.

Removing learned teammate paths makes the problem worse, not cleaner.
A_ACCOUNT also lowers the real 2021 Clippers small-ball fixture's offense
from 118.20 to 114.64 against those three references. One should not accept
synthetic changes while ignoring effects on real coherent lineups.

The observed two-big analogue cohort remains optimistic: 65 cells / 8,471
possessions, half bias +3.05 for J_POINT_BOTH, +3.10 R_ROUTE, +2.86
A_CONTEXT_GATE, +3.74 A_ACCOUNT. The 184-cell low-creation cohort has smaller
positive bias, about +.63 to +1.04 across these models. Sparse real analogues
cannot validate a five-center synthetic mean. Korver mixed-era profile transport
is still incomplete; his named comparison is not causal spacing evidence.

## Uncertainty

U0 valid-row handling is correct in this run; broad and all-off5 summaries are
identified rather than accidentally rejecting FINITE_GAME_BAND statuses.
Nominal 95% finite-quarter coverage by cell / possession weight:

| Half model | Cell coverage | Weighted coverage | Mean width | Mean interval score |
| --- | ---: | ---: | ---: | ---: |
| J_POINT_BOTH | 93.47% | 93.19% | 47.824 | 60.671 |
| A_GATE | 93.64% | 93.23% | 48.011 | 60.667 |
| R_ROUTE | 93.58% | 93.31% | 47.949 | 60.680 |

Lower interval score is better. The differences are tiny; modestly wider
intervals do not establish a new uncertainty mechanism. Retained point-half
weighted coverage is 92.72% novel, 91.22% thin and 90.49% debut. U1 persistent
discrepancy scores are also close on 2,037 commonly identified pairs, with 58
unidentified. Neither finite outcomes nor stable-quarter discrepancy validates
uncertainty about the true quality of arbitrary hypothetical lineups.

## Recommended next work

1. **Use the role exports for a bounded diagnostic before another wide sweep.**
   Separate player share error, team action-volume error, shot location and
   conversion on the same rows. Audit where R_ALLOC's count gain fails to help
   points, and compare A_CONTEXT_GATE's transfer gains with its ordinary-lineup
   costs. Include late-season/2026 failures and successful cases, not only tails.
2. **Extend the case library with an explicitly defined role-change taxonomy.**
   Preserve this transfer benchmark unchanged. Define moves in shot share,
   location and responsibility using dated pre/post exposure and minimum
   support; separately mark retrospective realized shifts and prospectively
   available changes in teammates. Include within-team departures/injuries
   only when their dated labels are available. No new confirmatory claim from
   selecting the largest realized changes in already-inspected seasons.
3. **Freeze a small next training experiment after that diagnosis.** Candidate
   directions are stronger separation of team volume from player shares,
   regularized context-dependent policy versus slower capability state, and
   checkpoint stabilization. R_ALLOC and compact-context gating deserve
   controls; R_ROUTE's conversion restriction alone is not the demonstrated
   solution. Retain equal event, point, coherence and uncertainty reporting.
4. **Address uncertainty and transport as product work, not garnish.** Diagnose
   debut/thin weighted undercoverage, dated profile-bank consistency and the
   reference game environment. Do not add a coverage gate or claim that seed
   spread solves unknown-lineup quality uncertainty.

This sequence is a recommendation for discussion, not authorization for a new
fit campaign, fresh data collection or tool promotion. If the next objective
is an internal usable tool, the existing reference is a reasonable research
backend with explicit limitations; a new architecture need not precede every
interface improvement.

## Artifacts and reproduction

- Frozen design: [JOINT_CAPABILITY_V18_PLAN.md](../docs/history/JOINT_CAPABILITY_V18_PLAN.md).
- Original campaign: `experiments/cache/joint_capability_2026_09_28_v18_prod`.
- Original tables and automated packet: its `_summary` and `_handoff` siblings.
- Separate review exports: `experiments/cache/joint_capability_2026_09_30_v18_codex_review`.
- Durable review log: the same review prefix plus `.log`.
- Test log: `experiments/cache/joint_capability_2026_09_30_v18_review_tests.log`.

The review exports can be recreated in a fresh directory:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v18_scientific_review \
  --run-dir experiments/cache/joint_capability_2026_09_28_v18_prod \
  --out experiments/cache/NEW_V18_REVIEW_PREFIX
```

The script refuses an existing output destination. Original reports, protocols,
fits, receipts and generated summaries remain untouched. Before the next commit,
stage explicit source/docs only; the working tree contains many unrelated
generated cache files. No commit is included in this task.
