# J_POINT_BOTH product-mode follow-up — independent review, 2026-09-27

**Complete, not promoted.** The point candidate retains a predictive advantage
when actual opponents are replaced by a common prior-opponent reference.
Its uncertainty estimates are usable research diagnostics, not a solved
out-of-distribution product. The center-heavy concern remains a bounded
role/opportunity/coverage question, not a reason to abandon the NN or to force
a particular synthetic matchup result.

Design: [frozen follow-up protocol](joint_capability_v16_followup_protocol.md).
Basketball evidence: [matchup diagnosis](joint_capability_v16_matchup_followup.md).
This is follow-up on repeatedly examined historical seasons, not fresh
confirmation. No NN refits, database access, scorer edits or deployment.

## Completion and independent checks

48/48 average-opponent quarters and48/48 chronological uncertainty quarters;
zero failed jobs, roughly31.9minutes in the two execution queues. Completed
source:
`experiments/cache/joint_capability_2026_09_27_v16_point_followup`.

New read-only review:
`experiments/cache/joint_capability_2026_09_27_v16_point_review`.
Reproducer: `experiments/v16_point_followup_review.py`; durable log
`logs/review.log`. Root/stage/quarter receipts checked,40 average score rows
independently recomputed from per-seed cell forecasts,60 persistent score rows
reconstructed from error/interval details, model-fit cutoffs checked,248 consumed
files fingerprinted unchanged before/after. Seed means, exact half-blend
identities, population keys and reused controls agree. Full fitting/scoring
producers and original experiment artifacts remain unchanged.

## 1. Average-opponent prediction

Same broad cohort:44 primary quarters2016–2026,2015 warmup,8,345 offensive
lineup-quarter cells /1,013,999 possessions; at least50 possessions per cell.
Three-seed predictions averaged first, possession-weighted errors second.
Each offense is integrated over the same origin-prior defensive reference,
with365-day exposure decay and512 deterministic inverse-CDF samples. The
original conditional affine calibration is retained; there is no refit against
the average-mode evaluation outcomes.

Important estimand limit: these forecasts are scored against the same **realized
offensive ratings**, which still reflect the opponents actually faced. This
checks prediction when the eventual opponent schedule is withheld. It does
not supply observed ground truth for how each lineup would play a perfectly
average opponent. Do not mix these numbers with the actual-opponent leaderboard.

| Forecast | RMSE | MAE | r² | Correlation | Bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| Integrated additive_defense | 11.25620 | 8.46737 | .132160 | .366253 | +.39032 |
| D_MAIN_RB half | 11.19990 | 8.41805 | .140820 | .377038 | +.44103 |
| J_BOTH half | 11.18496 | 8.41427 | .143111 | .380892 | +.52031 |
| J_ALL_BOTH half | 11.18057 | 8.40920 | .143782 | .380610 | +.37814 |
| J_POINT_BOTH direct | 11.15573 | 8.37684 | .147584 | .385719 | +.31382 |
| J_POINT_BOTH half | **11.15059** | **8.36724** | **.148368** | **.386329** | +.35207 |
| J_POINT_BOTH checkpoint-average | 11.18173 | 8.41665 | .143606 | .383425 | +.51284 |
| J_POINT_BOTH checkpoint-average-half | 11.15989 | 8.38167 | .146947 | .385403 | +.45158 |

Errors/bias are points per100; positive bias is overprediction. Checkpoint
averaging is not universally better. Keep both prespecified candidate views
reported; do not silently replace the earlier candidate with a retrospectively
selected view for every task.

### Strength of the comparison

Prespecified season-block bootstrap and exact11-season swaps, Holm correction
across four views ×three controls separately per metric/cohort:

| Point-half versus | RMSE difference | 95% bootstrap interval | Seasons better | Holm p |
| --- | ---: | --- | ---: | ---: |
| Integrated additive | −.10561 | [−.13944,−.07433] | 11/11 | .01172 |
| D_MAIN_RB half | −.04931 | [−.07597,−.02386] | 9/11 | .05859 |
| J_BOTH half | −.03437 | [−.05824,−.01086] | 8/11 | .16406 |

The improvement over additive is consistent. The smaller gains over already
contextual controls are promising, not established by the corrected family.
J_ALL_BOTH is a descriptive table comparator, not an extra registered contrast.

### Novel and thin-history lineups

Novel cohort:3,489cells /361,361possessions.

| Forecast | Novel RMSE | Novel r² | Novel bias |
| --- | ---: | ---: | ---: |
| Integrated additive | 12.36079 | .100727 | +1.22535 |
| J_BOTH half | 12.21769 | .121428 | +.93787 |
| Point direct | **12.13751** | **.132922** | **+.22859** |
| Point half | 12.17839 | .127071 | +.72697 |
| Point checkpoint-half | 12.18106 | .126688 | +.76484 |

Point-half beats additive in11/11 novel-cohort seasons, RMSE−.18240
[−.24529,−.12499], Holm p=.01172. Pure point-direct is strongest descriptively
on novel lineups; versus additive RMSE−.22329,10/11, Holm p=.04883.

The same descriptive pattern appears in thin/debut cohorts. For545 debut cells,
additive/direct/half RMSE is13.067/12.269/12.524 and bias+4.588/+1.659/+3.123.
For750 thin cells, RMSE13.071/12.490/12.657. This motivates a future study of
reliability-dependent blending, not an outcome-selected switching rule now.
Direct's own persistent-uncertainty model was not part of this two-half-view
follow-up; do not transfer the half-model uncertainty to it.

### Integration sensitivity: reassuring contrasts, not exact integration

The pilot's maximum difference of.065 did not describe every quarter. On880
fixed primary sensitivity cells (first20 lexicographic cells per quarter),
maximum512-versus4096 differences are.15194 direct,.14629 half,.16673 checkpoint
and.15369 checkpoint-half. Mean absolute differences are approximately.05.
Across all48 quarters including warmup, the checkpoint-half maximum is.27601.
77/880 primary half predictions differ by more than.1pts/100.

On this **same880-cell subset**, half RMSE is11.20811 at512 and11.20475 at4096.
The half-minus-additive RMSE difference is−.07095/−.07126, and half-minus-J_BOTH
is−.03266/−.03267. Thus most approximation movement is common to forecasts and
controls in this check. It does not overturn their sampled comparison, but it
does not establish exact convergence for every broad cell. No outcomes or
protocol were changed to resolve the discrepancy; preserve the sensitivity
label and revisit integration before a user-facing precision claim.

## 2. Persistent uncertainty: candidate-specific models now evaluated

U1 models a constant persistent-error variance; U2 lets it depend on lineup
descriptors. Both use prior-only fits/noise forecasts,200 whole-game bootstrap
draws, three disjoint-game splitting schemes and the original numerical
acceptance/recovery rules. Candidate per-seed predictions come from verified
per-fit archives; checkpoint-half uses its own seed disagreement.

Eligibility requires at least8 games/100 possessions. After cold-history
identification, each primary split has2,037 pairs, including580 novel pairs;
43 primary quarters are identified. The first five quarters of the full
schedule (including2016q1) remain explicitly NOT_IDENTIFIED for U1/U2. This
does not hide their point forecasts or impose a product coverage gate.

| Candidate / game split | U2−U1 joint log score |
| --- | ---: |
| Half / balanced-date | −.002264 |
| Half / odd-even | −.001662 |
| Half / first-second | +.000177 |
| Checkpoint-half / balanced-date | −.001049 |
| Checkpoint-half / odd-even | −.002106 |
| Checkpoint-half / first-second | −.001121 |

Higher is better. Five of six differences are slightly negative; the lone
positive is tiny. **No convincing contextual-uncertainty improvement.** U1
remains the required benchmark. These are descriptive comparisons, not six
independent datasets or a fresh significance test.

Candidate joint scores improve descriptively against old controls in all36
matched model/control/split/kind rows. That mixes changes in the point forecast,
error distribution and fitted noise; it is not proof that the uncertainty
architecture itself improved. Balanced-date point-half U1 log score−7.86995
versus parent−7.87866; checkpoint-half−7.86912.

Nominal95% balanced-date U1 finite-half coverage is94.21% for half and94.16%
for checkpoint-half, with mean full widths47.54/47.48pts/100. Thin/debut
coverage is about92.98%/93.07%, on only114/101 pairs. Under the working model,
mean finite-noise variance is128.17 versus persistent variance22.48 for half:
sampling noise dominates much of the uncertainty, but that decomposition rests
on the model's identification assumptions.

### Do not confuse three different interval readouts

1. The generic U0 summary includes220,381 offensive-five/quarter cells, mostly
   tiny exposures: coverage96.07%, mean width about215pts/100. That is not the
   broad >=50-possession cohort and is not a useful headline for the tool.
2. Restricting those same U0 forecasts to the broad8,345 cells, coverage is
   **93.19% half /93.27% checkpoint-half**, possession weighted; novel coverage
   **92.72% /92.67%**. Cell-weighted overall coverage is93.47%/93.64%.
   Mean possession-weighted full widths38.56/38.57pts/100.
3. The earlier ensemble supplement's93.86% broad coverage uses a different
   calibration-history population (broad cells only). The generic U0 procedure
   uses all earlier offensive-five cells. These are different interval
   constructions despite the same point prediction; neither number overwrites
   the other. Persistent U1/U2 split-game bands are a third construction.

All are finite-outcome checks. **None validates true-quality coverage for five
centers or another arbitrary hypothetical lineup.** Candidate synthetic
discrepancy bands and fully consistent cross-era player-state transport remain
explicitly deferred.

## 3. Decision and next work

Keep J_POINT_BOTH half/checkpoint-half as retained research candidates, direct
as an important comparison, and J_BOTH as the event/mechanism control. The
new result supports the average-opponent product direction without solving
coherence or uncertainty. No all-three-standards pass and no promotion.

Adam agreed to a bounded role/opportunity/coverage investigation:

- Extend the check from five centers to realistic crowded frontcourts, missing
  initiators and successful unconventional units. Freeze cohort definitions
  and mechanism expectations before inspecting a new candidate's predictions.
- Separate **creating an opportunity** from **finishing it**, and isolate
  offensive opportunity constraints from defensive volume/location/conversion
  and rebound recovery. Existing teammate messages already reduce the center
  optimism; do not treat “add interactions” as an untried solution.
- Read earlier overload/composition work before designing arms: v7 already
  learned a conversion-under-overload effect, and v6 tested holdouts within the
  observed composition range. Neither established behavior at synthetic
  extremes. A renamed generic overload penalty would repeat old work.
- Carry the unchanged point candidate, J_BOTH, equal-information additive and
  seasonal-level controls. Judge total ratings, event channels, coherent role
  responses and uncertainty together—not merely a forced matchup winner.
- Stop or reconsider if a change only improves the synthetic example. Do not
  start by suppressing offensive rebounds; a real rebounding advantage may be
  appropriate even when the surrounding offensive opportunity model is wrong.

Next deliverable: a focused, frozen learning experiment with explicit controls,
arm differences and acceptance/tradeoff rules. No new training campaign is
implemented or authorized by this review. Synthetic-mean regularization and
reliability-dependent blending are proposals, not current scorer behavior.
