# V18 role and volume diagnosis

September 30, 2026. Completed saved-output follow-up to the
[v18 scientific review](joint_capability_v18_codex_review.md), under the separately
[frozen diagnostic protocol](v18_role_volume_diagnostic_protocol.md).
No training, inference, database access, scraping, input rebuild, scorer promotion,
deployment or commit. Original artifacts and producer fingerprints are unchanged.

## Conclusions

The existing NN already responds usefully to observed role changes; carrying
forward a player's previous shot share is substantially worse. V18's explicit
allocators improve this slightly on large changes, but do not establish better
lineup point predictions even on that subset. Better allocation remains useful
for faithful explanations, but is not presently the main demonstrated point-error
bottleneck.

Shooting conversion has the largest absolute accounting residual. Team FGA and
FTA errors also matter and often offset each other. This is a reason to investigate
which conversion errors persist beyond shooting noise and shared game environment,
not evidence that the entire conversion residual is learnable. Do not fix excess
FTA independently of the other channels or launch another architecture sweep
solely because a future-outcome oracle looks strong.

## Populations and preservation

Five arms: J_POINT_BOTH, J_ACTION_BOTH, R_ALLOC, R_ROUTE, A_CONTEXT_GATE. Native
selected-checkpoint expected counts are averaged across seeds 17/23/41. Expected
FTM is averaged as each seed's FTA times its FT probability, not a product of
separately averaged factors. All 44 primary quarters are included.

| Population | Cells | Possessions | Use |
| --- | ---: | ---: | --- |
| Original broad offensive fives | 8,345 | 1,013,999 | Original point comparisons |
| Jointly observed FGA/FTA/location rows in broad cells | 8,292 | 874,715 | Exact point-factor decomposition |
| Original substantial transfer cohort | 146 | 47,419 | Unchanged transfer benchmark |
| Joint-label rows in that transfer cohort | 145 | 39,500 | Transfer decomposition only |
| Original broad cells containing a large shot-share changer | 2,139 | 254,582 | New retrospective point/interval slice |
| Joint-label rows in those role-change cells | 2,121 | 217,757 | Role-change decomposition only |

The decomposition loses 139,284 broad possessions, including all rows of 53 cells.
It does not silently redefine the main point benchmark. Its reference direct RMSE
is 11.789, versus 11.061 on the original all-row benchmark: different outcomes and
weights, not a model regression. Eighteen role-change cells have no joint labels;
the independent review restores them to the point and interval comparisons.

## A reusable observed-role library

The library contains 20,712 player-quarter records, including unsupported cases
and nonchanges. There are 12,290 supported comparisons against the immediately
preceding 365 calendar days. Both windows need at least 300 jointly labeled
on-floor possessions, five games and 50 individual FGA. These are diagnostic
support rules, not a product coverage gate.

Fixed thresholds identify 907 FGA-share shifts of at least five percentage points,
824 opportunity-share shifts of at least five points, 725 three-point-fraction
shifts of at least 15 points, and 530 rim-fraction shifts of at least 15 points.
Labels overlap. Opportunity means FGA + .44 FTA + turnovers, not measured creation
or ball handling. Shot share uses team attempts while that player is on court,
not the player's share of all team minutes.

Exposure-weighted FGA-share MAE, in percentage points:

| Forecast | All 12,290 supported player-quarters | 907 large observed changes |
| --- | ---: | ---: |
| Carry forward prior observed share | 2.119 | 6.396 |
| J_POINT_BOTH | 1.785 | 4.367 |
| J_ACTION_BOTH | 1.786 | 4.306 |
| R_ALLOC | 1.788 | 4.314 |
| R_ROUTE | 1.786 | 4.317 |
| A_CONTEXT_GATE | 1.805 | 4.506 |

The reference improves by 2.03 percentage points against the carry-forward
baseline on large changes. R_ALLOC improves another 0.053 points against the
reference; that is a small descriptive increment, not a significance claim.
On all supported records, the reference is marginally better than the allocator.

Illustrative successes and misses (shot-share percentages, not shooting accuracy):

| Player / quarter | Prior | Observed | J_POINT_BOTH | R_ALLOC |
| --- | ---: | ---: | ---: | ---: |
| Harrison Barnes, 2017q1 | 16.89 | 28.19 | 19.41 | 19.20 |
| Mikal Bridges, 2023q4 | 19.64 | 30.49 | 24.01 | 24.01 |
| Russell Westbrook, 2017q1 | 29.66 | 35.68 | 34.52 | 34.88 |
| Russell Westbrook, 2018q1 | 37.98 | 29.03 | 32.91 | 34.24 |

The models adapt strongly in some cases but miss both expansions and contractions.
The complete library retains favorable and harmful cases; the top-100 inspection
list is ranked by realized share movement, not by an arm's error. These examples
are selected illustrations, not another acceptance criterion.

All change labels use the future evaluation quarter and are retrospective.
Selection on large observed changes includes sampling noise and regression to
the mean. Forecasts are conditional on supplied realized lineups/opponents, not
predictions of future roster availability. The comparison does not isolate causal
teammate effects from shrinkage or other model differences. Historical quarters
have already been inspected repeatedly.

The export also records prior-only teammate familiarity for every supplied player
and five: the fraction of prior teammate possession mass belonging to the supplied
four. This is continuous, not a gate or an injury detector. The original eligible
opening-team-change registry is joined separately. A false opening-move flag
means absent from that registry, not a verified same-team/no-injury case.

## Do role-change lineups benefit?

All original 2,139 matching cells / 254,582 possessions, counted once each.
Half means the existing fixed NN/additive-defense blend; no new weights fitted.

| Model | RMSE | MAE | r² |
| --- | ---: | ---: | ---: |
| J_POINT_BOTH half | 11.3217 | 8.4140 | .18102 |
| R_ALLOC half | 11.3252 | 8.4131 | .18051 |
| A_CONTEXT_GATE half | 11.3266 | 8.4371 | .18030 |
| R_ROUTE half | 11.3365 | 8.4262 | .17887 |
| J_ACTION_BOTH half | 11.3629 | 8.4684 | .17504 |
| Additive defense | 11.4201 | 8.5211 | .16671 |

The retained contextual reference outperforms additive descriptively; the new
role mechanisms do not improve its point result here. Direct results and the
complementary no-supported-large-change population are exported too. The latter
includes unsupported players and must not be relabeled a verified stable-role set.
No bootstrap or multiple-testing superiority claim is added for these new slices.

## Where the point errors arise

Factor field-goal expected points into total attempts, player shares, player
location shares and conversion rates; factor FT points analogously. Sequentially
replace factors with realized outcomes, first in the protocol's forward order,
then in reverse as a sensitivity. Add calibration and event-ledger discrepancies.
The components reproduce direct prediction minus observed points on identical
rows. Rebounds/turnovers are not added again as point bonuses or penalties.

Reference forward-order signed contributions, points per 100 possessions:

| Component | Broad joint-label | Transfer joint-label | 2026 joint-label |
| --- | ---: | ---: | ---: |
| FGA volume | −0.904 | −1.642 | −1.851 |
| FG player allocation | −0.058 | −0.177 | −0.037 |
| FG location mix | +0.108 | +0.584 | +0.264 |
| FG conversion | −1.026 | −2.527 | −2.422 |
| FTA volume | +1.471 | +3.300 | +2.173 |
| FT player allocation | +0.022 | +0.037 | +0.017 |
| FT conversion | −0.090 | −0.049 | −0.245 |
| Saved point calibration | +0.157 | +0.309 | +0.665 |

Positive means an overprediction contribution. Observed event-ledger discrepancy
is numerically zero. The transfer pattern is fewer predicted FG points offset by
too many FT points, not uniformly excessive predicted scoring.

Absolute component magnitudes give a different view from signed bias:

| Broad reference component | Forward mean absolute | Reverse mean absolute |
| --- | ---: | ---: |
| FGA volume | 4.951 | 4.981 |
| FG player allocation | 0.505 | 2.108 |
| FG location mix | 1.794 | 4.005 |
| FG conversion | 8.326 | 8.546 |
| FTA volume | 4.500 | 4.515 |

Allocation attribution changes substantially with replacement order. The forward
0.505 is not a causal importance estimate or proof that allocation is irrelevant.
Conversion is the largest absolute component in both orders, but includes noisy
realized shooting, within-cell context/opponent variation and possible systematic
miscalibration. Sparse observed player-location rates are especially noisy.

Subtracting the forward conversion component lowers joint-label reference RMSE
from 11.789 to 7.480; the reverse component gives 9.080. Removing the forward FGA
volume component instead raises RMSE to 12.581, and removing FTA volume raises it
to 11.871. These are future-outcome **accounting-component removal** calculations.
Because each component is computed after other sequential replacements, they
are not generally equivalent to changing just that factor in the original model.
They are neither attainable forecast gains nor bounds on achievable accuracy.

R_ROUTE's 2026 forward conversion contribution is −2.747 versus reference −2.422;
its FGA-volume contribution is −2.266 versus −1.851. Its trouble is not explained
by player allocation alone. A_CONTEXT_GATE's corresponding FGA-volume contribution
is −0.887, but conversion remains −2.311 and calibration adds +0.986. No single
channel explains an overall winner. Novel-cell and all-arm/order tables are retained.

## Coherence and uncertainty

The role examples and event accounting improve our ability to inspect basketball
mechanisms; they do not solve the legal-center synthetic failure or validate a
forced Jokić pairing ranking. No synthetic inference was rerun.

On the 2,139 outcome-selected role-change cells, existing nominal 95% finite-game
bands have the following coverage:

| Half model | Cell coverage | Possession-weighted coverage |
| --- | ---: | ---: |
| J_POINT_BOTH | 92.80% | 93.09% |
| R_ALLOC | 92.99% | 93.26% |
| R_ROUTE | 92.99% | 93.30% |
| A_CONTEXT_GATE | 93.45% | 93.59% |

Reference mean width is 48.09 points/100, mean interval score 61.80. These bands
remain somewhat undercovered; small differences do not establish a new winner.
Outcome-selected coverage cannot establish prospectively calibrated uncertainty,
and finite-game intervals do not validate hypothetical latent lineup quality.
All three product standards remain unfinished; no promotion follows.

## Recommended next work

1. Freeze a bounded **conversion-residual persistence** analysis. Use game-disjoint
   splits, support/shrinkage and matched opponent/environment sensitivities to
   distinguish repeatable location-conditioned errors from realized shooting noise.
   Keep original cells, disclose unsplittable cases and dependence uncertainty.
2. Revisit **joint game-environment residuals**, including FGA and FTA together.
   The earlier [situation study](game_situation_diagnostic_review.md) showed shared
   clock/score context explained much of transfer FTA bias; its exact adjustments
   must not be transplanted onto these different rows or models. Realized context
   is a diagnostic, not a requested fan-facing input or pre-quarter forecast input.
3. Use this role library to design a small, predeclared test of **dated role-state
   adaptation**, if persistent misses warrant it. Barnes/Bridges-style expansion
   and Westbrook-style contraction are inspectable cases, not labels to force.
   Compare with current profiles/allocators before a latent role/ability redesign.

Refits are welcome when justified; none is authorized by this completed diagnostic.
The next experiment should target a measured, persistent residual and assess
points, mechanism fidelity and uncertainty together—not chase the oracle result.

## Outputs, checks and repair provenance

Paths below are relative to `experiments/cache/`:

- `joint_capability_2026_09_30_v18_role_volume1/`: 44 completed origin calculations,
  player roles/forecasts, prefix familiarity and exact decompositions. Its final
  summary failed on a duplicated `cells` keyword; top-level completion is absent.
  Preserve it as the origin source, not a successfully completed top-level run.
- `joint_capability_2026_09_30_v18_role_volume_summary2/`: successful summary-only
  completion, without recomputing or editing origins. `component_summary.csv`,
  `role_change_library.csv.gz`, `role_prediction_metrics.csv`,
  `role_forecasts_and_changes.csv.gz`, `largest_observed_changes.csv` and audits.
- `joint_capability_2026_09_30_v18_role_volume_review1/`: independent identity/date/
  uniqueness checks; **authoritative all-original-cell** `all_original_point_metrics.csv`,
  `all_original_finite_intervals.csv`, `all_original_role_change_cells.csv.gz` and
  `supported_player_forecasts.csv.gz`. These supersede summary2's role-lineup
  point/interval tables, whose membership included only joint-label cells.

Each prefix has a durable sibling `.log`. Eight focused tests passed in
`joint_capability_2026_09_30_v18_role_volume_tests3.log` (final rerun). Independent review passed
on 82,920 component rows (8,292 cells × five arms × two orders), all 44 strict
prior cutoffs, unique player/arm keys, original cell joins and receipt checks.
Harmless pandas future downcasting warnings are preserved in the review log.

Sources: [origin calculation](../experiments/v18_role_volume.py),
[versioned summary completion](../experiments/v18_role_volume_finish.py),
[independent review](../experiments/v18_role_volume_review.py). Do not edit these
completed producers or rerun into existing prefixes. The original top-level
runner retains its summary defect for provenance; use the versioned finisher
when reproducing summaries from the verified origin outputs.

No job remains running. Current navigation and this review document the next
decision; original reports and frozen plans are unchanged.
