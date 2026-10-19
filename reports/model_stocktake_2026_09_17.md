# Model stocktake and next-direction recommendation

2026-09-17, Codex. Adam requested a commit followed by a holistic assessment
of offense-only research versus starting defense. The completed FTA and shared
game-situation work is committed as **5e90381** (13 files;80tests pass).
Generated research artifacts remain local and unstaged. This memo is subsequent
research discussion, not a frozen experiment or permission to launch training.

## Recommendation

**Make actual-opponent/defensive modeling the next substantial experimental
workstream. Keep a bounded offensive action-generation investigation alongside
it, not another prerequisite that postpones defense indefinitely.**

The offensive model is not finished. It is now sufficiently stable and
informative to serve as the offensive half of a matchup experiment. Opponents
are part of the explanation for offensive outcomes, not merely a second output
to bolt on after offense has been perfected. This step also advances the
original two-lineup product more directly than another generic architecture
sweep. There is no guarantee of a large accuracy improvement.

## 1. Progress in perspective

The project has moved from additive ratings plus separate hand-built contextual
adjustments to dated statistical player states, a compact learned teammate
response, coherent event decoding, role inputs, and miss/recovery/renewal
accounting. There are no known-pair chemistry parameters in the primary NN.

The strongest practical learning was not that more network capacity always
helps. It was that particular information/structure mattered: standardized
inputs; mean plus spread of teammate capabilities; role information combined
with creation/load constraints; and making offensive rebounds generate renewed
opportunities rather than merely predicting an extra feature.

Same primary44origins/5,607cells/726,364possessions, raw original forecasts:

| Forecast | RMSE | r² |
|---|---:|---:|
| Corrected additive | 10.84099 | .12043 |
| Older V9_SPREAD NN | 10.86667 | .11626 |
| Older additive/V9_SPREAD HALF | 10.80812 | .12576 |
| V14 combined SHIFT/rebound NN | 10.79367 | .12809 |
| V14 combined HALF | 10.77978 | .13034 |

These are lineup-quarter offensive ratings, not possession-level r². The best
direct NN now has a better pooled point estimate than additive, whereas the
earlier direct model trailed. The blend remains stronger. Its improvement
versus additive is about1.13% of MSE: useful, modest, not a breakthrough.
Three seeds support several directions, but none of19 registered direct
architecture contrasts survived multiplicity correction. No unqualified claim
that the most complex arm is uniquely best.

Retain three candidates: ROLE_SL (simplicity/best blend MAE), RB_RENEW_FAC
(renewal mechanism and novel performance), RB_RENEW_FAC_SHIFT (pooled RMSE).
The combined arm's recent gains are mainly recurring; it is effectively tied
with oldHALF on novel lineups. Three-seed averaging itself accounts for part
of the improvement versus earlier single-seed runs.

The frozen substantial transfer cohort supports contextual forecasts, but its
broader low-exposure counterpart favors oldHALF. Explicit zero-shift replay
finds only a small uncertain contribution from the dedicated role-shift channel.
This is not yet proof that the model knows how a specific player will change
jobs after a trade.

## 2. What the latest diagnostics changed

We had a plausible but misleading simple story: the decoder creates too many
free throws. Across all held-out groups it is nearly unbiased; on substantial
common fives it overpredicts by4FTA/100 because those fives experience very
different deployment, alongside other remaining errors.

The shared prior-fitted clock diagnostic reduces substantial FTA bias from
4.010 to.995, and clock+margin to.913. FGA bias also shrinks. Three-point
attempt underprediction does not improve. NN/HALF relative advantages survive.
These are conditional diagnostics using realized context, not improved frozen
forecasts, and not identified causal fractions.

2016Cleveland remains the largest repeated-unit harm versus additive. Its
combined NN point error goes from-7.50 to-7.98/100 after clock adjustment;
FGA remains roughly4.07/100 too low. Thus deployment explains some apparent
channel failures without explaining away the hard offensive cases. Blindly
subtracting free throws would be the wrong next mechanism.

## 3. The three product standards

**Prediction:** a credible offensive research candidate with modest gains and
useful complementary signal beyond additive. Not a universal winner by season,
population or metric. Historical evaluation years have repeatedly informed
development; strict-date fits do not make subsequent architecture selection an
untouched confirmatory test.

**Basketball coherence:** progress in allocation, roles and recovery accounting;
still incomplete. Combined native five-Gobert offense120.01 exceeds the real
reference118.84 in the saved fixture. Defense cannot excuse this offensive
failure by making the lineup's net score poor. Action creation versus efficient
finishing remains a real modeling question. Observed donor/recovery signal is
not identified Adams-style causal facilitation. Explanations must distinguish
accounting from causal attribution.

**Uncertainty:** finite-game intervals are reasonably calibrated (leading half
80/95% coverage79.19/94.63%), but hypothetical-lineup latent-quality uncertainty
is not solved. Seed spread is not a posterior;1/sqrt(n) cannot make uncertainty
about an unfamiliar lineup vanish. This is a required workstream, not a final
UI garnish. No coverage gate and no promotion on accuracy alone.

## 4. Why defense is now practical—and what already exists

Read-only inventory this session, exact44primary windows:

- 2,760,546 possession rows have both offensive and defensive fives.
- Zero nonpositive player IDs, duplicate slots within a side, or players on
  both sides of the same recorded possession.
- Game×offensive-five groups:410,292. Game×offensive-five×defensive-five:
  **718,526**, a **1.751×** increase.
- Median group exposure falls4→3possessions;166,888 matchup groups are
  singletons, representing6.05% of possessions. More rows, not more independent
  games. Do not require50possessions per exact matchup and discard most data.

These are identity/size checks, not verification of event-level floor accuracy.
Substitutions during possessions and missing event labels retain their current
caveats. Log: `/tmp/basketball-defense-readiness-2026-09-17.log`. No new training
inputs were built and no database was accessed.

Existing local per-player/game data include own steals, blocks, defensive
rebounds and foul counts, plus on-floor opponent shot mix, conversions, FTA,
turnovers, rebounds, points and exposure. They can support **new strictly dated,
shrunk defensive descriptors** after audit; their raw on-floor values are not
individual causal defensive ability. Height/position are possible supporting
descriptors, not substitutes for defensive outcomes.

We are not starting defense from zero. The older on-floor work evaluated the
additive defensive half and offered an additive opponent offset. It has reusable
centering, sign and prior-calibration helpers in `onfloor_defense.py` and
`onfloor_opponent.py`. Audit/reuse those controls; do not build a parallel
unanchored defensive coefficient system or resurrect the old level leak.

Two important distinctions:

1. V5's unsuccessful opponent-deconfounded **historical player profiles** were
   not a test of the actual opposing five in the neural decoder.
2. Older free attacker-ID×defender-ID effects had very low reliability. That
   argues against pair-identity tables, not a proof that broadly shared
   capability-based matchup mechanisms cannot forecast.

Tracking data are not a prerequisite for this first step. They would help with
assignments/contests/schemes, which these data cannot directly reveal. The
tracking memo is historical reconnaissance, not a verified fresh data feed;
no new claim about current availability or rights is made in this review.

## 5. The experiment I would design next

This is a direction/comparison ladder, not a frozen arm list or training spec.

### A. Matchup-ready representation and honest controls

Use game×offensive-five×defensive-five sufficient statistics, preserving point
rows and target-specific missingness. Reconcile to existing offense-only
aggregates. Splitting groups may alter loss constants or point-auxiliary
weighting: demonstrate control equivalence where claimed; don't assume old
fits can be reused for a different objective.

Compare the current offense-only models, additive offense+defense, and current
NN offense plus the same centered additive defensive main effect. Opponent-
aware NN must beat a comparator that also knows the opponent, not merely the
old blind additive score. Freeze sign, reference and calibration choices using
only prior data. No future season DRtg or evaluation-fitted scaling.

Keep the original benchmark intact. Aggregate conditional matchup forecasts
back onto the same offensive cells and also inspect defensive-five and matchup
populations. Report that realized opposing personnel are additional conditioning
information; don't rename that a better generic pre-season lineup prediction.

### B. Defensive mechanisms before a full tactical simulator

Start with pooled defender capabilities that can affect:

- where shots are attempted and conversion at those locations;
- turnovers forced and foul-drawing opportunity;
- the defense's chance to end a possession with a rebound.

The central contrast is **generic defensive strength versus offense-dependent
response to defensive capabilities**. For example, does changing rim protection
alter a rim-dependent offense differently from a perimeter-heavy offense?
Such examples are hypotheses to pre-register, not guaranteed rankings.

Use the existing compact profile/message architecture where appropriate; do
not simultaneously change offensive backbone, tracking, optimizer, stopping
and model size. Distinguish point-additive controls from decoder-level effects,
which may already interact through nonlinear normalization. Rebound opposition
should change recovery probabilities, not add another independent point bonus.
Opponent inputs must not directly change the same shooter's FT conversion.

Do not start with25 named matchups, learned one-to-one defensive assignments,
pick-and-roll coverage states or a full spatial simulator. Those claims need
data we have not established. One strong, bounded campaign with clear nested
controls is more informative than many undifferentiated architectures.

### C. Two-lineup product behavior and all three standards

A shared directional scorer supplies F(A,B) and F(B,A); per100 net margin is
their difference. Team swap must negate margin; slot permutations must do
nothing. Average-opponent mode should marginalize over a declared prior
reference rather than silently equating five mean profiles with the mean
defense of a nonlinear model. No clock/score controls need appear in the UI.

Keep the current offensive coherence panel and add defensive/matchup probes
before results. Five guards' rim/rebound problems are now testable; five
centers' missing creation still needs to appear on offense. Show intervals and
support for both sides and the difference, without presenting seed spread as
validated OOD uncertainty. Identify the latent-quality uncertainty evaluation
in the plan rather than again marking it an unspecified later task.

## 6. Ranked remaining roads

| Road | Recommendation now | What would make it worthwhile |
|---|---|---|
| Actual opponents/defense | Next substantial campaign | Point/event gains or a disclosed coherent-matchup benefit beyond opponent-aware additive/main-effect controls |
| Offensive action volume, creation versus finishing | Bounded companion investigation; one change only if a general failure is identified | Fix persistent real-case FGA/3PA errors and extremes without case-specific bonuses |
| Latent-quality/OOD uncertainty | Explicit acceptance work alongside expansion | Distinguish finite-game noise, shared-state uncertainty and persistent unsupported-mean error; test what is identifiable |
| First-chance versus post-ORB decoder | Strong bounded follow-up after opponent baseline | Better phase mix/conversion and points beyond stationary renewal, without observed-future-phase leakage |
| Role adaptation and richer creation/shot context | Keep active, narrower than a generic recency sweep | Incremental transfer/role signal with strict-date inputs; separate new information from new architecture |
| Tracking/spatial enrichment | Small access/date/coverage pilot when choosing a concrete target | Verified historical data and same-population gains; don't block the initial defense experiment |
| Larger networks/attention/loss/stopping sweeps | Park absent a diagnosed bottleneck | A specific representational or optimization failure, not just another architecture name |

I would spend the majority of the next modeling effort on opponents, a smaller
bounded block on residual offensive failures, and explicitly budget uncertainty
evaluation. This is prioritization, not permission to lower either non-accuracy
standard or to promise defense will solve every offensive issue.

## Handoff

Sources reviewed: v5–v9 independent synthesis; v5 input findings; v10–v12 value/
residual findings; full v14 independent review; transfer and repeated-failure
review; latest FTA/situation diagnostics; roadmap/backlog; older on-floor defense
and opponent work; local channel/group/profile schemas. No new fits or external
research were performed. Prior public-tracking claims were not revalidated.

Commit5e90381 contains the completed diagnostic work. This new overview and
the accompanying checkpoint are subsequent, uncommitted documentation. No
training is active. Next action is agreement on this direction, then a frozen
opponent/matchup experiment plan—not immediately launching or modifying v14.
