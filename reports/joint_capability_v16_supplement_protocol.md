# Post-v16 supplemental analyses — frozen bounded design, 2026-09-26

Run only after the repaired v16 registered analysis and independent audit pass.
Separate derived outputs; no NN refits, input changes, scorer promotion or
retroactive edits to the v16 protocol. This is historical development evidence,
not a fresh confirmatory holdout. Preserve all three product standards.

## Common population and reporting

Use the exact corrected `broad_off5_ge50` population, three-seed predictions
averaged before evaluation, all 48 quarterly origins for history and 44
2016–2026 quarters for primary scores. Weight by possessions. Report all,
novel and recurring cells; no gate or silent exclusions. Use seed 160926.

## A. Neural + additive ensembles

Members: all 22 registered neural arms, each in direct and checkpoint-average
view, plus common-calibrated additive_defense. Exclude ADJUSTED_CHANNEL from
this neural ensemble question. Never blend already-half forecasts. Controls
include all fixed single-member halves and parent_half_defense.

Nine bounded ensemble methods:

- For each of the two views, equally average all 22 NNs, then mix 50/50 with
  additive_defense (two fixed controls).
- For each view, rank arms by possession-weighted MSE on all **earlier**
  completed quarters and average the top 1, 3 or 5; mix 50/50 with
  additive_defense (six forward-selected methods). Lexicographic ties; before
  any prior observations, use all 22 instead of privileging an arbitrary arm.
- One nonnegative, sum-to-one stack of all 44 native-view calibrated NN
  forecasts plus additive_defense. No intercept or current-quarter bias
  correction. Minimize prior possession-weighted MSE / prior outcome variance
  plus lambda times squared distance to weights (.5 additive, .5/44 each NN).
  Candidate lambdas .01, .1, 1, 10; choose on the last prior quarter using
  strictly earlier quarters to fit. Prefer larger lambda on a numerical tie
  (1e-10 MSE). Refit weights on all prior quarters. Require at least four prior
  quarters and 500 earlier tuning-training cells; otherwise use the anchor.
  SLSQP, analytic gradient, tolerance 1e-10, cap 500; failure is reported and
  stops the analysis, not a result-dependent alternative optimizer/weight rule.

Store per-origin member weights, tuning results, raw predictions, costs as
nonzero member count, quarter/season and pooled RMSE/MAE/r²/correlation/bias.
Paired comparisons to additive_defense and parent_half_defense use 10,000
season-block resamples and exact season swaps, with Holm across the nine
methods × two controls separately for each metric and population slice.
Full-run residual covariance and hindsight rankings are descriptive only;
they cannot choose the weights used in the forward table. No post-hoc oracle
combination is presented as a forward forecast.

For finite-quarter uncertainty, independently apply the existing U0 procedure
to each ensemble's own earlier **out-of-sample** errors, rather than averaging
members' intervals. Report 95% coverage/width for all/novel/recurring, with
cold-start omissions explicitly counted. This does not establish latent/OOD
coverage. For direct-view mixtures, compose available fixed-fixture direct
predictions using that fixture origin's saved forward weights and common
additive forecast. Mixtures requiring checkpoint-average fixture predictions
are marked NOT_EVALUATED where those ledgers were not produced; do not replace
them with direct predictions. This limitation precludes claiming an overall
three-pillar winner from their point performance alone. Report missing
coherence evidence explicitly and any additional inference needed.
If member-specific numerical integration used different additive references,
mark those fixture combinations NOT_EVALUATED too; do not silently take the
first arm's reference and pretend it was shared.

## B. Empirical reliability / noise sensitivity

Aggregate original game×off5×def5 outcomes to game×off5 inside each exact broad
lineup-quarter. Keep whole games disjoint. For cells with at least two games,
compare (i) 100 seeded random near-equal-game-count splits, (ii) chronological
first/second splits, and (iii) odd/even-date splits. No best split is selected.
For each split, let h be the first half's fraction of possessions and d its
PPP100 difference from the second half. Estimate full-sample noise variance
as h(1-h)d². This requires a stable mean and inverse-exposure independent noise;
role drift, opponent mix, correlated games and heteroskedasticity violate it.

Report weighted target variance, weighted estimated noise, and the untruncated
diagnostic ratio 1 − noise/target variance. Show global and within-quarter
centered denominators. The noise contribution to weighted variance includes
the finite-number-of-cells correction sum(w*v)/W − sum(w²*v)/W²; apply it
within quarter for the centered variant. This ignores cross-cell covariance
from shared games: disclose it, and use season-block uncertainty rather than
pretending lineup cells are independent replicates.

Use 2,000 resamples of the 11 complete season blocks, preserving all cells in
each selected season. Also compute a >=8-game sensitivity, disclosing its
changed support. Cells that cannot be split retain their presence in the
population accounting; report their cell/possession share. If any are missing,
the reliability number describes only the identified subset, not all cells.
Do not plug in zero noise for missing cells or claim a theoretical ceiling.

Repeat split estimates after subtracting the **dated archived additive
defensive adjustment** (v15 inherited additive_defense minus additive, before
the extra v16 affine step; three-seed mean), aggregated over actual opponents. This is a
model-dependent opponent-mix sensitivity, not an identified context-free
target or a new forecast. Report changes in half-opponent ratings/time separation.

## Handoff

New outputs and logs, source/protocol/code fingerprints and resumable receipts.
Report negative results and missing evidence. The statistical supplements do
not alter registered arm contrasts or promote a scorer. Human interpretation
of the complete three-pillar evidence remains a separate final decision.
