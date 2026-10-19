# Independent v3 review and next architectural decision

2026-09-10. Requested by Adam after Sol's completed v3 run and Opus's
`CLAUDE_MODEL_FEEDBACK_3.md`. This review starts **no optimizer fits** and leaves
the completed v3 directory, its scientific modules, and both agents' earlier
write-ups untouched. The numerical audit and its durable log are in
`experiments/cache/joint_capability_v3_review_2026_09_10/`; `audit_02.log` is the
final replay. All seven frozen source hashes still match.

## Bottom line

The NN direction is paying off. Actual teammate profiles improve forward event
prediction and the point forecast, and the model distinguishes a five-Gobert
offense from a five-Jokic offense without player-specific rules. It is close to
the additive benchmark, not decisively better or worse across seasons. This is
a useful structural research model, not a completed two-lineup product.

Run the **mean-teammate comparison next**, but interpret it as *pooling before
versus after the nonlinear receiver/sender interaction*, not *additive quality
versus chemistry*. Also retain H2 as a serious simpler candidate. A small
matched-regularization factorial can answer both questions without rebuilding
inputs or retuning everything. The executable work contract is
`SOL_JOINT_CAPABILITY_DAY3_PLAN.md`.

## 1. What independently reproduces

Primary population: 44 evaluated quarters, seasons 2016–2026; 2015 supplies four
calibration-warmup quarters. Every arm has 5,607 lineup-quarter cells / 726,364
possessions. Novel: 2,073 / 226,256. These are possession-weighted point metrics,
not single-possession r², full-season forecasts, or latent-quality correlations.

| Arm | All MAE | All RMSE | All raw r² | Novel RMSE |
|---|---:|---:|---:|---:|
| H0, anchored profiles | 8.17540 | 10.94454 | .10355 | 11.90772 |
| H1, learned own-state correction | 8.15862 | 10.91831 | .10784 | 11.87830 |
| H2, real messages without encoder | 8.12280 | 10.87679 | .11461 | 11.81636 |
| H3, encoder + real messages | 8.12290 | 10.87013 | .11570 | 11.81692 |
| H3F, encoder + fixed sender | 8.16042 | 10.92302 | .10707 | 11.88369 |
| Corrected additive | 8.09195 | 10.84099 | .12043 | 11.85302 |

H3's pooled RMSE deficit to additive is **0.02913 points/100**, about 0.27% of
additive RMSE. Its season-average deficit is +.02756, 95% t interval
[-.06708, +.12221]. Novel season-average difference is -.03747, interval
[-.19778, +.12283]. Neither establishes superiority. H3 versus H3F is -.05232
season-average RMSE, interval [-.09762, -.00701], favorable 9/11 seasons.
These intervals are conditional summaries of a repeatedly inspected historical
benchmark, not evidence from a newly untouched test set.

H3 versus H2 is -.00584 ± .04596 SEM on season-average RMSE. That does not prove
equivalence or prove the encoder useless; it does justify testing simplification.
H2 has 1,814 learned parameters versus H3's 4,488.

### H2's previously missing basketball check

I scored the **existing saved H2 fits**, with the same dated states and float64
decoder used for the other arms. No training was necessary.

| Fixture | H0 | H2 | H3 |
|---|---:|---:|---:|
| Five limited centers | 118.69 | 105.66 | 101.40 |
| Five Goberts | 132.65 | 116.37 | 113.98 |
| Five Jokics | 127.22 | 133.11 | 132.37 |
| Warriors 2016q4 | 114.47 | 116.55 | 119.47 |
| Clippers 2021q4 | 115.98 | 121.50 | 122.24 |
| Haliburton same-four | 118.94 | 120.29 | 121.50 |
| McConnell same-four | 116.48 | 116.53 | 118.20 |

These are **native offensive** points/100. They exclude defense and an explicit
rebounding loop; the synthetic levels have no validated latent-mean intervals.
H2 reproduces the encouraging center/Jokic directions. H3 does not uniquely own
that achievement. The sizeable H2/H3 fixture differences also warn against
treating one network's channel ledger as a uniquely identified causal story.

## 2. The mean arm: yes, with a different interpretation

Current message aggregation, for receiver i:

    pair:   c_i = (1/4) sum_{j != i} M(h_i, h_j)
    mean:   c_i = M(h_i, (1/4) sum_{j != i} h_j)
    fixed:  c_i = M(h_i, training_reference)

Here h_i is the anchored state, optionally plus the learned own-state encoder.
The mean is an 18-coordinate capability summary, **not one average player-value
coefficient**. A receiver-dependent nonlinear M can learn that a particular
creator benefits from collective shooting, or that another finisher adds less
when creation is scarce. The finite opportunity allocator then couples all five
players again. This is still an identity-free contextual model.

Mean versus pair asks whether preserving the individual sender profiles through
the nonlinear message calculation is worth the extra computation. The pair arm
can distinguish distributions sharing the same sender mean; the mean arm can
apply nonlinear responses to collective supply directly. At fixed width these
are different function classes, not a clean nested capacity ladder. With an
encoder, the mean of learned h already contains nonlinear functions of the
original player features. Even without it, the state averages logs/logits, not
raw basketball percentages. Label the statistic accurately.

Neither model has known-pair IDs. A mean-arm tie would **not** refute player
complementarity or require an additive product. It could give us a cleaner,
cheaper implementation of it: five rather than twenty effective message
evaluations per lineup, with the same parameter count. For a receiver whose
four sender states are identical, mean and pair messages coincide at identical
weights. Thus pooling does not inherently lose the clone distinction.

## 3. Where I agree with Opus—and where I do not

**Agreements:** prioritize mean pooling; give the simpler H2 a fair test;
separate context evidence from causal identification; qualify synthetic
magnitudes; correct the failure-selection story; investigate uncertainty support;
eventually test better-conditioned messages and more direct shooting supervision.

**Regularization is a qualification, not a discovered protocol violation.**
V3 explicitly allowed separate network lambdas. H3 chose .0001, H3F .01, with
H3's boundary flag disclosed. That is a legitimate tuned-system comparison but
not a fixed-lambda ablation. H2 versus H3F at .01 also changes the encoder and
parameter count; it is not a matched-architecture replication. Nor can we infer
that differing lambdas caused the narrower SEM without the matched refits.
Refitting H3 at .001 alone would still not match H3F's .01. The next plan
specifies actual matched comparisons.

**The encoder has not established a lineup-prediction benefit; it is not proved
dead.** H1 improves conversion over H0. Shared learned states might also help a
later response architecture. Simplification is a practical choice to test, not
a statistical conclusion from a non-significant contrast.

**Conversion is not a null.** The saved event report calls
`sum A*(p-M/A)^2 / sum A` a Brier score. This is squared error against a grouped
shooting fraction. The per-attempt Bernoulli Brier numerator is instead
`M*(1-p)^2 + (A-M)*p^2`. The omitted term is independent of p, so same-cohort
model differences survive exactly; absolute values and percentage-improvement
interpretations need correction.

Corrected FG Brier: H0 .233044, H2 .232718, H3 .232664, H3F .232719.
H3–H3F has **season-average delta -.00005603 ± .00001300 SEM, favorable
10/11 seasons**. This is small but consistent. Dividing it by a loss dominated
by make/miss noise does not measure how much learnable conversion signal was
recovered. Earlier shot-quality work found improvements of a similar order,
although its population/conditioning differ, so the studies are not directly
interchangeable. Next measure the conversion change in both event units and its
actual point contribution; do not assume it is the entire remaining point gap.

**Assisted share is auxiliary supervision, not automatically wasted gradient.**
Its decoded output is absent from the point identity, but it supervises shared
weights and its player-game prediction is weighted by expected makes. It can
influence point-bearing channels. An ablation would test whether this helps;
the absence of a direct additive assisted-points term does not answer that.
Likewise, location is explicitly valued by location-specific make rates in this
NN; the old structural scorer's algebraic cancellation should not be attributed
to v3 without an actual perturbation calculation.

**Raw message inputs are an explicit frozen design choice**, stated in Day2
§4.1, not an accidentally missed repair. Standardizing them could help training,
but changes conditioning, initialization, and effective regularization. Do not
bundle it into the pooling ablation.

**The interval comparison is encouraging, not failed.** The composition method
is narrower at 50/80/95%, closer to nominal under possession weighting at all
three levels, and closer under cell weighting at two of three. Moving 80%
coverage from 84.04% to 78.96% reduces absolute calibration error. Nevertheless,
its change also introduces exact 1/sqrt(n) scaling and a different calibration
split. We have not isolated the contribution of composition distance itself.
A constant-scale control using the identical split and n scaling is needed.
Coverage should ideally remain near nominal across distance bins; it need not
increase with distance. Coverage ordering does not identify persistent-error
ordering, and good finite-batch coverage does not validate synthetic means.

**The support metrics deserve diagnosis, not a threshold chosen to fire.**
I reproduced the stored fixture distances. Clone distances near 3.2 versus a
pooled observed maximum near 3.1 are not a calibrated measure of tail probability;
maxima from different normalizers/eras are particularly weak comparators. A
covariance-aware or neighborhood distance is worth a later controlled test, but
cannot be selected merely because it places five clones farther away. The raw
historical role-share SD has median .148 across exported player-origin states;
it includes short game-lineup sampling variation and is not uncertainty in a
player's latent role. Audit that before changing the >2 threshold.

**Zero minimum coordinate exposure is not a missing player.** In the limited-
center fixture, Robinson has minimum coordinate neff 0 but maximum 2,921 and a
recent last appearance. Bogut has nonzero exposure and a stale historical state.
No member of this fixture is the all-player generic fallback. The fixture is
partly stale and has weakly observed coordinates; it is not five fallback players
or evidence that one entire player's history is absent.

**The Korver hypothesis needs its reference named.** Current-state Korver-minus-
Westbrook is +1.448 native / +.854 calibrated under H3. Corrected additive gives
-1.084 calibrated: the difference of calibrated swaps favors Korver by +1.937.
But the H3-minus-H1 swap contrast favors Westbrook by 3.076 native points.
These answer different questions. The original user hypothesis was relative to
additive; it is not globally falsified by the H3/H1 result. Adam also explicitly
allows the hypothesis to be wrong. Keep both contrasts, do not force either sign,
and do not label either a uniquely identified Jokic pair effect.

## 4. Holistic architecture assessment

Keep the broad shape: dated partially pooled states -> shallow contextual set
map -> finite opportunities -> location-specific attempts and makes -> exact
point ledger -> prior-only point calibration. It is compact, learnable on events,
permutation equivariant, and useful for explanations. Do not replace it with a
large unconstrained points-only network to chase a few hundredths of RMSE.

The unresolved structure is more important than extra depth:

- States summarize historically observed roles, not context-free intrinsic
  talent. Shared contextual prediction does not by itself deconfound ability,
  coaching, opponents, selection, and teammate effects.
- The learned message changes several channels, but there is no explicit joint
  creator/finisher responsibility model. A low five-center score is encouraging
  behavior, not proof that primary creation has been identified.
- U is a league-level budget. The network reallocates it but has no physical
  miss/rebound/extra-opportunity loop. Rebounding is not an independent mean lever.
- Opposing defenders are absent. A same-five offensive model cannot yet be the
  requested matchup simulator, even with excellent offensive event fits.
- Empirical future-outcome intervals, parameter/seed sensitivity, role support,
  and uncertainty in an arbitrary lineup's latent mean are different objects.

After the controlled pooling comparison, the most promising sequence is: diagnose
which channel changes reach points; test a targeted conversion/creator-state
improvement if warranted; add prior-only opponent conditioning; then connect
creation and rebounding to opportunities. Support/uncertainty proceeds alongside,
not as a post-deployment caveat. No architecture should be selected by r² alone.

## 5. Next work and handoff

The Day3 plan makes the next main deliverable an actual complete data experiment,
not another open-ended audit campaign. Four new common-lambda arms complete a
2×3 encoder/pooling comparison using two verified existing controls; two further
arms supply a matched low-lambda sensitivity. Saved-output corrections and
focused invariants support that experiment without changing v3 inputs/objective.

There are real Day2 delivery gaps: native/within-quarter/exposure tables and
common-cell event diagnostics are incomplete; broad-channel output contains
unweighted predictions rather than actual-minus-predicted biases over qualifying
cells; H2 was absent from fixtures; interval radii were not independently fully
replayed. Those are derived-output work, not reasons to rerun v3. The count-family
implementation also uses a pooled numerator/pooled exposure, rather than the
sum of separately normalized channels described in Day2. Day3 explicitly freezes
the implemented loss to isolate architecture and discloses the discrepancy.

No current training job was launched. Codex is finished editing at this review's
handoff; establish sole editing ownership before Sol begins the new plan.
