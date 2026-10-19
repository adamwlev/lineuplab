# v12 partial-run diagnosis

2026-09-14, Codex. Exploratory analysis of saved forecasts and checkpoints; zero
new fits. This is not the completed Day6 review or a replacement pre-registration.

## Decision

Do not repeat the full run to repair a numerical receipt check. The current
additive-anchored hybrids have weak predictive results and a specific, measurable
failure in their basketball interpretation. Investigate that design before more
training. Keep corrected additive, V9_SPREAD and their existing HALF/GLOBAL
combination as research controls. Nothing is promoted.

The preceding recommendation to rerun all completed fits because a tolerance
changed was unnecessarily rigid. Preserving original artifacts and recording a
reviewed, tolerance-only change can support a separate continuation with explicit
provenance. Such a continuation has not been implemented or launched here.

## Evidence scope and reproducibility

- Historical source: `experiments/cache/joint_capability_2026_09_13_v12_prod_final/`.
  There are 74 completed arm-origins: both arms at 37 quarterly origins.
- Primary analysis excludes the four 2015 warmup origins: 33/44 quarters,
  4,284 cells and 558,579 possessions. Eight complete seasons, 2016--2023,
  plus 2024q1. Season contrasts below exclude the partial 2024 season.
- Mechanism analysis uses the separately saved 2026q4 prescribed pilot fits
  under `...v12_pilot_final5/`. It is a latest-origin fixture diagnosis, not a
  claim of replicated behavior across every historical fit.
- The repaired 2024q2 diagnostic fits and other pilots are not added to the
  historical evaluation population. This keeps its population easy to audit.
- New outputs: `experiments/cache/joint_capability_2026_09_14_v12_partial_audit/`.
  Producer: `experiments/v12_partial_audit.py`; durable log:
  `reports/joint_capability_v12_partial_audit.log`.
- The producer verified all 74 completion receipts, their file hashes and gzip
  reads, ran under `no_database()`, and verified its explicitly manifested
  source artifacts were unchanged after analysis. The manifest links the
  upstream manifests and actual saved fits/cells/anchors; it is not a claim that
  every transitively imported source module was independently re-audited here.

## 1. Prediction: the original NN signal survives, but v12 loses it

Possession-weighted scores on the identical partial primary population:

| model | MAE | RMSE | novel RMSE | recurring RMSE |
|---|---:|---:|---:|---:|
| Additive | 8.06143 | 10.80654 | 11.79896 | 10.31305 |
| V9_SPREAD | 8.10140 | 10.81686 | **11.69184** | 10.38533 |
| HALF | 8.03491 | **10.76273** | 11.69454 | 10.30120 |
| GLOBAL | **8.03317** | 10.76535 | 11.70361 | **10.30043** |
| Frozen anchored full swap | 8.18153 | 10.93021 | 11.87072 | 10.46456 |
| ADAPT_CONTEXT | 8.12945 | 10.86143 | 11.83482 | 10.37820 |
| ADAPT_VALUE_CONTEXT | 8.12403 | 10.85056 | 11.82172 | 10.36847 |

The useful original pattern is still visible: the NN helps novel fives, additive
helps recurring fives, and their simple combination is strongest overall. The
anchored hybrids do not preserve that novel-lineup advantage.

Across the eight complete seasons, flexible minus HALF mean RMSE is +0.08687,
nominal paired t95 interval [-0.03787,+0.21162], with 2/8 favorable seasons.
This is unfavorable evidence, not a statistically definitive rejection of all
hybrids. These repeatedly inspected historical seasons are development evidence.

Flexible minus strict is -0.01094 [-0.03076,+0.00888], favorable in 6/8 seasons.
The value-head capacity has a small encouraging direction but uncertain benefit.
Strict adaptation improves over frozen anchored full swap in pooled RMSE by
about .069; its complete-season interval also crosses zero. The poor result is
not evidence that training made every frozen hybrid worse.

The missing 11 quarters contain 167,785 possessions. To erase the current pooled
deficit to HALF, the flexible arm would need remaining-window RMSE about 10.6656
against HALF's saved 10.9579 (approximately .292 better). To erase the deficit
to additive, it would need about 10.8091 against 10.9549. Those are arithmetic
break-even thresholds, not probability estimates or alternative stopping rules.

## 2. The exact accounting explains the center-lineup failure

The hybrid takes the native neural forecast F, builds an additive approximation
B from five separate insertions into a synthetic all-anchor lineup, and retains
the difference C = F - B:

    H = A + b + G + (F - B)
      = F + (A + b + G - B)

The second expression exposes the risk: replacing B with A can remove part of
what made F basketball-coherent. Additivity is an algebraic property; it does
not ensure that B and A represent interchangeable player values.

Latest-origin flexible-arm ledger (points per 100):

| fixture | A | b | G | native F | anchored B | C=F-B | final H |
|---|---:|---:|---:|---:|---:|---:|---:|
| Five Goberts | 111.80 | -.02 | +1.30 | 121.69 | 109.75 | +11.93 | **125.01** |
| Limited centers | 111.16 | -.02 | -.22 | 109.09 | 103.11 | +5.99 | **116.91** |
| Conventional real five | 119.06 | -.02 | +.36 | 117.74 | 117.82 | -.08 | **119.32** |
| Five Jokics | 134.66 | -.02 | +3.33 | 130.18 | 144.52 | -14.34 | **123.63** |

The limited-center decoder is about 8.65 points below the conventional decoder.
The hybrid shrinks that gap to 2.41 points. Five Goberts finish about 5.69 points
ABOVE the conventional unit and 1.38 above five Jokics. Negative five-Jokic C
alone is not the failure; the final center-lineup comparison is.

For five Goberts, the trained all-anchor forecast is 115.06. Replacing one
anchor with Gobert yields 114.00, a decrement of about 1.06. Repeating that
single-insertion decrement five times gives B=109.75. The actual five-Gobert
decoder gives 121.69, so its difference from that extrapolated subtotal is
+11.93. Calling this difference a chemistry bonus would be misleading.

This separation was my proposed architectural choice. Its exact algebra was
correct, but I gave that algebra too much credit as a representation of the
basketball quantity we wanted. More unit tests of F=B+C cannot resolve that
conceptual mismatch.

## 3. Learned teammate messages penalize centers; subtraction changes the sign

Holding the trained decoder and input states fixed, turn off only its learned
teammate message. This is an intervention on the model, not a causal estimate
of real basketball effects and not a refitted comparison arm.

For five Goberts, flexible arm:

| calculation | messages off | messages on | change |
|---|---:|---:|---:|
| Native F | 130.92 | 121.69 | **-9.23** |
| Anchored B | 126.75 | 109.75 | **-17.00** |
| Residual C | +4.16 | +11.93 | **+7.77** |

The network's learned message lowers center offense. But it lowers the additive
anchor approximation even more, so subtracting B makes C more positive. The
problem is not that the message network learned a +12-point Gobert synergy.

Limited centers show the same mechanism: messages lower native offense by 8.27,
but C rises from +1.16 to +5.99. This also shows why simply naming C the context
head hides important behavior already distributed through F and B.

## 4. A positive residual exists even without teammate messages

The independent-player decoder still allocates a common event budget. Let d_i
be each player's unnormalized FGA + .44 FTA + TOV propensity, and s_i the
corresponding unnormalized expected scoring. With messages off:

    F(X) = 100 * U * sum(s_i) / sum(d_i)

This ratio is nonlinear in a set of players even though each player's raw
rates depend only on their own state. Its anchored residual can be nonzero
without a learned teammate effect.

For five identical x states versus anchor r, define q=d_x/d_r and R=s/d.
The exact independent-decoder residual is:

    C(x,x,x,x,x) = 100 * U * 4*(1-q)/(q+4) * (R_x - R_r)

A low-volume, high-efficiency player can therefore receive positive C merely
because the same five copies must collectively consume the full budget. The
trained message-off Gobert demand is about .722 times the anchor's, and its
positive residual is +4.16. Five Jokics have a message-off residual of -5.35.
At initialization, before fitting either arm, these residuals already have
approximately the same signs and magnitudes: +4.08 and -5.35.

This allocation nonlinearity can be useful basketball structure, but it is not
automatically evidence of spacing, creation or teammate facilitation. Retaining
it after swapping the reference player values needs separate justification.

## 5. The native decoder has a remaining OOD problem too

Even before the additive substitution, the flexible decoder gives five Goberts
121.69 versus 117.74 for the conventional five. The decomposition amplifies an
existing extrapolation problem; it is not its only cause.

Five Goberts receive 77.71 FGA, 39.58 FTA and 17.16 turnovers per 100, with
62.1% expected FG conversion and only 1.87% of attempts from three. About 24.71
points come from free throws. The allocation assumes the lineup can consume
the full budget while retaining very efficient shot conversion. Messages reduce
the message-off forecast by nine points, but do not reduce it enough to encode
the difficulty of manufacturing those shots without perimeter creation.

We cannot infer which specific new input or mechanism will fix this from a
synthetic example. What is established is that learned corrections to observed
profiles plus budget normalization do not yet validate this extreme transfer
of shooting efficiency and opportunity creation.

## 6. On real fives, C adds more movement than useful error correction

Across observed primary cells, flexible C has mean +.258 and RMS 1.278 points.
Its weighted correlation with additive prediction error is only -.0149. It
partly corrects additive's negative level bias, but its squared size exceeds
that benefit and its small association with remaining errors.

For the full flexible correction, exact symmetric squared-error attribution
relative to A assigns weighted MSE changes of:

- C: +.89525
- G: +.03164
- b: +.02628
- total: +.95317, equal to the model's MSE increase over A up to float precision.

Thus about 94% of this excess is attributed to C under this particular
accounting convention. This is reference-dependent arithmetic, not a causal
percentage or a uniquely identified decomposition of harm.

Post-hoc component removals confirm where the numerical problem lies:

| saved-fit diagnostic | overall RMSE | novel RMSE |
|---|---:|---:|
| Full flexible H | 10.85056 | 11.82172 |
| Same fitted model with G omitted | 10.84939 | 11.82600 |
| Same fitted model with C omitted | 10.80920 | 11.79886 |
| Additive | 10.80654 | 11.79896 |

These are diagnostics, not validated candidate models. Notably, the flexible
arm's modest edge over strict is not simply the direct contribution of G:
it jointly changes the learned backbone, C and b. Removing G alone preserves
most of that edge overall. We should not claim G has independently demonstrated
a useful portable value correction.

## 7. Concrete disagreement cases

Eight largest possession-weighted squared-error harms versus HALF are exported
at >=100 possessions, with >=200 sensitivity. Examples:

| origin / lineup | poss | actual | HALF | A | flexible H | C |
|---|---:|---:|---:|---:|---:|---:|
| 2018q4 Curry / Thompson / Durant / Green / Looney | 227 | 107.49 | 121.72 | 121.88 | 128.39 | +6.23 |
| 2018q4 Paul / Harden / Ariza / Tucker / Capela | 769 | 111.96 | 119.46 | 120.09 | 122.70 | +2.47 |
| 2022q1 Walker / Fournier / Barrett / Randle / Robinson | 564 | 103.55 | 115.37 | 116.52 | 118.12 | +1.21 |
| 2024q1 Lillard / Beasley / Middleton / Giannis / Lopez | 376 | 129.52 | 122.22 | 119.60 | 117.40 | -3.62 |

This is not only excessive optimism about good-looking lineups. In the Bucks
case, context pushes an existing underprediction further down. The top eight
harms account for about 28.5% of net excess SSE versus HALF, so a handful of
stories cannot explain the full result. Selection is post-hoc; outcomes remain
noisy and include opponent/schedule context that H does not model. These cases
do not establish the causal quality of any named lineup.

## 8. What to carry forward

1. Keep the original NN's novel-lineup signal and the existing ensemble. The
   matched partial population still supports both as useful research assets.
2. Stop treating an algebraically nonadditive remainder as self-evidently
   transferable basketball complementarity. Require the final total, the event
   ledger and model interventions to agree in meaning before replacing values.
3. Retain profile-value learning as an open idea, with the qualification that
   v12's head has not established an independent predictive contribution.
4. Any next design should preserve the connection between event creation,
   opportunity allocation and the final number. Replacing a scalar subtotal
   after decoding currently breaks that connection. Adding richer role or
   opponent information remains a separate possibility, not a conclusion of
   this test.
5. There is no demonstrated uncertainty improvement to compensate for the other
   shortcomings. Outcome intervals and anchor sensitivity do not establish
   uncertainty about the latent mean for five centers. This analysis does not
   generate a new interval method or claim synthetic coverage.

The next useful work is a bounded design discussion informed by these ledgers,
not another width/epoch sweep or a full rerun for its own sake. If completing
Day6 later is useful for a clean record, finish only the missing work through
an explicitly audited continuation and keep it labeled as development evidence.
