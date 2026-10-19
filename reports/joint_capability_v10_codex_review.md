# Independent v10 continuation review and discussion

Codex/Astra, 2026-09-13. Adam asked for a review after Sol's usage interruption,
completion of the pending commit, and discussion of the remaining research.
This document qualifies Sol's v10 review. No additional neural fit was run and
no completed run artifact was edited.

## Verified state

The production run completed 96/96 new arm-origins: two doses over 48 quarter
origins, with inner epoch selection and final prefix refitting (192 fits).
The final receipts report 2,572.4 seconds, no failure, and completed reports.
The two saved alpha-zero parity checks, 2016q1 and 2026q4, reproduce the old
V9_SPREAD epoch decisions and every parameter exactly. The five frozen
plan/producer hashes still match. The common-cell join reproduces all 6,179
descriptive cells and their outcomes, exposures, and novelty for both new arms;
the 5,607-cell primary population excludes the four 2015 warmup origins.

The independent full-suite run completed **743 tests in 33.847 seconds, OK**.
Its durable log is `reports/joint_capability_v10_verification.log`. The earlier
untracked-producer failure was resolved by staging the new source files. Earlier
console-only test invocations did not preserve their final exit status in the
conversation; this logged run is the verification receipt of record.
All four input-manifest hashes also match, and all 198 gzip files pass full
decompression/CRC verification. The staged diff has one harmless trailing blank
line warning in the generated `reports/additive_gap_cases.md` inside the
completed run; that frozen artifact is preserved exactly.

## What the comparison supports

Primary population: 44 quarter origins, 2016–2026; 5,607 lineup-quarter cells,
726,364 possessions. Novel fives: 2,073 cells / 226,256 possessions. Ratings and
errors are in points per 100 possessions. These are quarterly snapshots scored
on qualifying lineup outcomes within the following quarter, not full-season
forecast cells or single-possession r2.

| forecast | all MAE | all RMSE | all r2 | novel MAE | novel RMSE |
|---|---:|---:|---:|---:|---:|
| corrected additive | 8.09195 | 10.84099 | .12043 | 8.90390 | 11.85302 |
| V9_SPREAD | 8.14017 | 10.86667 | .11626 | 8.86194 | 11.77283 |
| fixed half additive/V9_SPREAD | 8.07274 | 10.80812 | .12576 | 8.83865 | 11.76624 |
| prior-only GLOBAL | 8.07069 | 10.80970 | .12550 | 8.84177 | 11.77345 |
| TEAM_01 | 8.15905 | 10.87372 | .11511 | 8.91756 | 11.82448 |
| TEAM_1 | 8.11221 | 10.84875 | .11917 | 8.88777 | 11.80225 |
| half additive/TEAM_1, post hoc | 8.05677 | 10.80180 | .12678 | 8.84645 | 11.78334 |

The blend has stronger evidence than Sol's emphasis on MAE suggested:

| season-paired contrast against additive | mean delta | nominal 95% t interval | favorable seasons |
|---|---:|---:|---:|
| half, all MAE | -.02046 | [-.06181, +.02089] | 7/11 |
| half, all RMSE | -.03285 | [-.06466, -.00103] | 9/11 |
| half, novel MAE | -.06702 | [-.14021, +.00617] | 8/11 |
| half, novel RMSE | -.08939 | [-.15632, -.02247] | 9/11 |
| V9_SPREAD, recurring RMSE | +.07389 | [+.00077, +.14700] | 1/11 |

So the fixed blend improves squared-error performance against additive, most
clearly on novel lineups. The standalone NN's recurring-lineup RMSE disadvantage
is also consistent. This supports complementary predictive information, without
identifying exactly which part is individual skill, context, calibration, or
estimation error. Years have been reused for development, the comparisons are
multiple, and seasons share training history; nominal intervals should not be
described as confirmation on fresh untouched data.

The post-hoc half-TEAM_1 result is worth retaining. Against half-V9_SPREAD its
equal-season MAE change is -.01490, CI [-.03956,+.00977], favorable 8/11;
novel MAE change is +.00731, CI [-.03785,+.05247]. It does not establish a better
blend. Historical half-V9_ALL has RMSE 10.80112 and r2 .12689, marginally better
than half-TEAM_1 despite slightly worse MAE (8.06691). There is no universal new
winner across metrics. Its rank-positive FT caveat remains documented.

## Corrections and interpretation

**Attribution labels.** Sol's table labeled V9_SPREAD minus V8_BASE but printed
V9_SPREAD minus V9_BASE. The original source tables are correct. The corrected
combined contrast has squared-error contributions: volume -.16778, allocation
-.00075, location -.14280, conversion -.16849, calibration +.22031. Their sum
is -.25951. Calibration offsets roughly 46% of the other blocks' net favorable
contribution in this particular decomposition. This is exact arithmetic between
two calibrated forecasts, not evidence that removing calibration would help.

**Team supervision.** The stronger dose worsens outer normalized event loss by
.0006292 +/- .0000536 season SEM, in 11/11 seasons. The small native team-MSE
improvement is real as a point estimate, but 0.027% of total noisy MSE is not a
fraction of the learnable signal. Its standalone point gain is uncertain. Keep
it as a research reference; stop repeating this exact dose experiment. These
results do not show every team objective must fail.

**Context magnitudes.** Smaller responses are not automatically worse. We lack
ground truth for the correct penalty on five copies of a player. Event-loss
accuracy informs the predictive standard; it is not an independent veto that
replaces the other two standards.

**Basketball totals remain unfinished.** V9_SPREAD gives five Goberts 117.85
offensive points/100 and the real reference 118.27. TEAM_1 gives 119.43 versus
119.13. Those are substantial negative adjustments from their own no-message
forecasts, but the resulting offense is still surprisingly respectable. The
fixed blend lowers five Goberts to 114.82, yet raises five Jokics from the NN's
127.21 to 130.94. The hybrid improves some extremes and worsens others relative
to the NN; it needs its own full basketball review. No single penalty magnitude
should be imposed from these examples.

**The Jokic comparison has two distinct meanings.** Relative to the separate
additive forecast, V9_SPREAD favors the Korver lineup by an extra +2.856. Its
own native message-on/off increments, however, are +2.887 for Korver and +6.049
for Westbrook. The learned message gives Westbrook more uplift in this test.
Both can be true because the non-message model has a different player-value map
and finite-budget interactions. An NN-minus-additive difference does not isolate
the learned teammate mechanism. This is central to the next experiment.

**Evaluation and uncertainty.** The expanded population demonstrates a different
estimand; it does not prove extra data can never improve precision. The exact
game-cluster bootstrap was explicitly omitted, so no measured precision gain
or failure from that method exists. Observed finite-outcome intervals remain
reasonably calibrated, with mild undercoverage in some slices. No result here
calibrates uncertainty about a synthetic lineup's latent mean.

## What is left on the table

The immediate recommendation remains **separating individual value from context**,
but it needs a precise definition before a new model build. A useful schematic is

    neural = individual-value component + contextual component
    half blend = 0.5 * additive + 0.5 * individual-value component
                               + 0.5 * contextual component

The research question is whether we can retain additive's individual-value
information while estimating the contextual component independently. An additive
projection of the NN over a declared prior reference population is one possible
definition. Its remaining residual includes finite-budget interactions. Simply
turning off the messages does not produce a pure additive model, and adding that
message difference to the existing additive model would leave both double
counting and baseline choice unresolved.

Start with a bounded analysis of saved models: separate the NN's additive
projection from its interaction residual using only prior information, examine
their predictive contributions and their basketball totals, then specify one
matched mean/context replacement experiment. The reference population, centering,
shrinkage and prior-only tuning rules must be fixed before reading its evaluation
results. The additive contribution needs an honest residual-value label unless
the event decoder accounts for it; it cannot be relabeled as measured spacing or
shooting quality. This is a proposal for the next plan, not an authorized run.

The broader backlog still contains distinct opportunities:

- **Actual opposing-five effects and defense:** historical schedule correction
  in profiles did not test the offensive matchup against five particular
  defenders. This also advances the original two-team product directly.
- **Role adaptation and creation/finishing information:** changing training-row
  decay did not test quicker state updates after a role change. Dated tracking
  could distinguish creation from assisted finishing; full-season aggregates
  cannot be used earlier in their own season.
- **Possession renewal and rebound facilitation:** adding an ORB feature did
  not test a miss/recovery/extra-attempt mechanism or Adams-style facilitation.
- **Uncertainty about the mean:** profile uncertainty and variation in learned
  responses should be propagated and checked on real support shifts. A global
  finite-game interval does not answer this product requirement.

These deserve separate bounded experiments. Improving offense by another few
hundredths is not the only way to make this tool more useful. For the immediate
research decision, individual-value/context separation best follows the evidence
from v10; actual-opponent/defensive modeling is the strongest subsequent step
toward the full product.

## Operational handoff

The existing production/scientific artifacts remain unchanged. The original
review's attribution table and interpretation were corrected; this document and
the follow-up tables live outside the completed run. The pending Day4 source,
planning documents, derived forecasts and reviews are committed together at
Adam's request. Binary model checkpoints and input arrays remain local under
the repository's existing ignore policy; this commit is not a complete backup
of those files. Production and independent verification logs are explicitly
included. No worker is editing and no next experiment has been launched.
