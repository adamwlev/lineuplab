# V18 residual persistence diagnostic protocol

Frozen September 30, 2026 before computing the diagnostics below. Adam authorized
further diagnostics to inform direction. This is exploratory historical research,
not fresh confirmation. Stop after the bounded analyses, audits and interpretation.
No neural/additive training, new inference, database access, scraping, input-cache
rebuild, promotion, deployment or commit. Use new derived outputs and durable logs.

## Questions and fixed models

Does within-location shooting error recur in different games? Is it a common
level error or stable player/lineup error? Does game environment explain the
offsetting FGA/FTA errors? Can a simple dated shooting control reveal an unnecessary
neural conversion error? Do errors survive into the next evaluation quarter?

Use J_POINT_BOTH, R_ALLOC, R_ROUTE and A_CONTEXT_GATE, three saved primary seeds
17/23/41, all 44 primary quarters 2016–2026. Same original 8,345 broad off5 cells
and their joint FGA/FTA/location-label subset; disclose losses. Use all joint-label
rows for player-location diagnostics, reporting that different population clearly.
Keep original transfer and retrospective role-change memberships unchanged.
No best-seed, checkpoint-view, threshold or model selection.

## Row conditional accounting and shooting controls

For every matchup row, actor and location, recover each seed's make probability
as expected makes / expected attempts, then average probabilities equally across
seeds. Positive predicted attempts are required; fail on unsupported zero division.
Compare probabilities on actual attempts, not predicted shot frequencies.
Expected FT makes for point accounting remains mean(FTA times probability).

Field goal residual equals two exact components: (predicted FG points minus
expected points at the observed actor/location attempts) plus (expected points
at observed attempts minus actual FG points). Analogous FT components plus saved
calibration reconstruct point error. These are conditional descriptive accounting
components, not causal interventions or deployable predictions using future shots.
No extra TO or rebound point term. Record FGA/FTA/TO count residuals separately.

Compare NN conditional probabilities with two strict pre-origin controls:
league location rates and individual player-location rates. Both use a trailing
1,095-day window with 365-day half-life. Player rates pool 50 attempts toward
the league rate. No tuning; these are shooting diagnostics, not full point models.
Report binomial log loss and Brier score using observed attempts/makes, per-location
bias, fixed probability deciles, season/quarter summaries and matched contrasts.
Clip only for log calculations at 1e-6; disclose boundary counts. Player controls
are not claimed identical to the NN's existing profile definition.

## Game disjoint persistence

Aggregate row residuals to game/offensive five, keeping possession sums. For each
broad lineup-quarter use five fixed random global game partitions (seeds
11,29,47,71,97); all appearances of a game share a side within a repetition.
Also split each unit's games chronologically by game count. No game occurs in both
sides of a unit. Random splits need at least two games and20joint-label possessions
on each side; print excluded cells/exposure. A predeclared sensitivity requires
100possessions per side. These are diagnostic support thresholds, not product gates.

Measure total direct point error, conditional FG conversion, other FG error,
conditional FT conversion, other FT error, FGA/FTA/TO rates and saved calibration.
Weight a cell by its full joint-label exposure. Report signed bias, half variances,
cross-half covariance/correlation, uncentered cross product, and covariance after
weighted within-origin centering. Do not call these a theoretical accuracy ceiling.
Split variances are unequal; do not apply a naive equal-half correction.

Summarize each random partition separately and their mean. Season-block bootstrap
2,000 draws, seed180930, recomputes the mean statistic across the same five
partitions; repetitions are not independent seasons. Chronological results are
a distinct sensitivity. Uncentered product includes common bias; origin-centered
covariance asks about within-origin persistent differences. Eleven seasons and
reused players limit inference. Covariance can be negative and is not clipped.

For a concrete cross-game check subtract the other half's residual shrunk by
n/(n+200) from each half's prediction. Report held-out-half MSE change relative
to no correction; this is within-quarter diagnostic adaptation using outcomes,
not an improved original pre-quarter forecast. No tuning of the200constant.

## Opponent and game environment sensitivities

Actual opposing fives already enter the saved neural probabilities. Use the
saved additive_defense minus additive row prediction as an opponent-strength
descriptor, aggregated to each half. Repeat reference persistence on units with
absolute half-to-half descriptor difference at most1point/100; disclose retained
mass. This is a limited measured-opponent-balance sensitivity, not full assignment
control or average-opponent inference.

Reuse verified prior-only shared CLOCK/MARGIN effects from the completed
game_situation_2026_09_17_v2 fit_rates export. Reconstruct diagnostic group-state
exposures from immutable possession/shot extracts in memory, validating exact
parent game/off5 ledgers. Apply those effects to the current v18 rows and masks;
do not reuse old cohort aggregate offsets. No nuisance refit or input-cache write.
Verify every saved fit cutoff against the original schedule/producer evidence.
Historical reference effects use full target-specific populations; applying them
to the joint-label subset is explicitly a sensitivity, not causal identification.

Report unadjusted, CLOCK and MARGIN point/FGA/FTA/conversion residuals, including
matched additive and half point controls. Add expected context-minus-historical-
reference counts to prediction-minus-observed errors. Conversion offsets weight
within-location make effects by actual attempts and point values. Do not combine
independently residualized channels into a physical scorer or clip adjusted targets.
Margin may mediate player quality; keep it separate from CLOCK. Missing context
uses the previously defined parent fallback and is counted.

## Player location persistence and dated correction

Aggregate conditional probability errors to player/location/quarter, using all
joint-label rows. Report adjacent-quarter residual correlation with at least20
attempts in each quarter. Consecutive means adjacent positions in the original
schedule, including across seasons, not the previous available appearance after
a gap. Record gap/calendar dates; player and season dependence remain.

Predeclare one untuned diagnostic: adjust current probability by subtracting the
previous quarter's mean probability error, shrunk by previous attempts/(attempts+100).
No prior quarter means zero correction. Read only previously completed quarter
records. Evaluate log loss/Brier on all current attempts, plus corrected-support
counts; no target-based selection. Clip resulting probabilities to[1e-6,1-1e-6].
This is a lightweight dated residual control, not a promoted NN change. Report
season consistency and paired season-bootstrap loss differences versus each arm's
uncorrected probabilities; no point-gain claim follows without coherent integration.

## Interpretation and acceptance

Persistence alone can reflect shared unobserved context, label errors, players or
fit bias. Nonpersistence does not prove no learnable shot quality. Significant
league drift is not necessarily lineup complementarity. Large gains from observing
future shots or the other half are not forecast gains. Name both successes and
failures; retain full tables rather than tuning named-player examples.

Prediction, mechanism coherence and uncertainty retain equal standing. These
diagnostics may identify an uncertainty discrepancy source but cannot validate
synthetic lineup means or latent-quality intervals. No synthetic inference is
required. Finish with measured findings, limitations and a prioritized future
direction, not an automatic architecture sweep.

Tests and audits: strict prior control dates, future-mutation immunity, exact
conditional point accounting, per-seed probability versus count averaging,
game-disjoint partitioning, unequal exposure/covariance arithmetic, no self-quarter
residual correction, context/parent row alignment, source hashes and full original
point metrics. Preserve completed outputs; corrections use versioned producers.
