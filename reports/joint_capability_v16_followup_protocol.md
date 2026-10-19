# Post-v16 product follow-up — fixed design, 2026-09-27

Adam authorized the recommended follow-up after committing completed v16 work
as 3eede4cb. Direct implementation; no NN training, scraping, database mutation,
input rebuild, source-artifact edits, scorer promotion or deployment. Outputs
go to a new prefix. This is historical diagnostic/follow-up evidence, not a
new confirmatory holdout or a revision of the v16 experiment.

## A. Diagnose the two-lineup extrapolation

Use the frozen 2026q4 legal_pure_centers, jokic_westbrook,
highest_exposure_real_2026 and small_guards fixtures. All ordered pairs,
including mirrors, three seeds, J_RAW/J_BOTH/J_POINT_BOTH/J_ALL_BOTH.
Replay direct native and calibrated points and additive/half; checkpoint means
for J_POINT_BOTH use their own affine calibration and saved checkpoint list.
Verify unmodified predictions against the completed panel where available.

Record each player's points, attempts, conversion, turnovers, creation supply,
demand, shortage/load, and rebounds; team first-chance versus renewed points,
FT/2PT/3PT components and rebound capture. These are accounting identities, not
causal credits. Verify exact reconciliation and team-swap antisymmetry.

Direct-state interventions: full, messages_off, adjusted_offense_off,
defense_off (raw and adjusted defense), messages_and_adjusted_off,
messages_and_defense_off, adjusted_and_defense_off, all_three_off,
constraints_off (zero k_supply/k_ft/k_load), defense_recovery_off (override0).
All use saved weights; restore after each change. First-only accounting drops
renewed phase contributions without changing initial attempts: a descriptive
decomposition, not a normalized basketball forecast. Do not tune any switch,
modify a scorer, or demand a named lineup ranking based on this diagnostic.

Observed analogues: all 44 primary quarters / broad >=50 possession cells,
same rows/forecasts as completed evaluation. Define a nonspacing big by archived
height >=82 inches and origin-prior raw 3PA/100 <1; disclose missing height and
prior state. Report all, >=2 nonspacing bigs, >=3, maximum player prior AST/100
<5, and >=2 bigs combined with that low-creation condition. Thresholds are fixed
before reading cohort errors, not selected for model disagreement. Retain all
cells in the overall table; unavailable descriptors are counted, not dropped
silently. Names/height come from existing archived metadata; role features are
strictly origin-dated. Report cells, exposure, observed PPP, RMSE/MAE/r²/bias
for additive_defense, parent_half_defense and the four specified NN direct and
half forecasts. No independent-season significance claim for tiny subsets.

## B. Missing average-opponent mode for the point leader

J_POINT_BOTH only, three seeds, all48 origins with2015 warmup, four views:
direct, checkpoint_average, half, checkpoint_average_half. Use all exact broad
cells and the existing dated 365-day-decayed defensive reference: first512 of
the common4096 inverse-CDF sample; first20 lexicographic cells get4096 sensitivity.
Same conditional scoring calibration as the original study, no average-mode
refit. Average predictions across seeds before scoring. Reuse the completed
D_MAIN_RB/J_BOTH/J_ALL_BOTH average-mode controls on identical keys; verify
additive and integrated-additive equality before comparisons.

Report all/novel/recurring/thin/debut, quarterly and season sufficient statistics,
pooled weighted metrics, paired season bootstrap/exact swaps against integrated
additive, D_MAIN_RB-half and J_BOTH-half. Holm across4views×3controls separately
per metric/cohort. No new view or ensemble selection from these results.

## C. Persistent uncertainty for the actual candidate

Run existing U0/U1/U2 likelihood, penalty grid, game splits, bootstrap/noise
protocol and numerical recovery for J_POINT_BOTH:half and
J_POINT_BOTH:checkpoint_average_half only. All48 chronological quarters, primary
2016–2026; no borrowing uncertainty parameters from another scorer. In particular
checkpoint-half seed disagreement must use checkpoint-half seed forecasts, not
direct-half forecasts. Retain the original half-view bootstrap seeding formula.

Reuse dated inputs and forecasts read-only. Original U1/U2 controls remain in
their completed outputs and are compared on identical model-independent cell,
quarter and split keys. Report finite coverage and joint scores, support cohorts,
missing identification and model-dependent noise assumptions separately. No
synthetic true-quality coverage claim. Synthetic candidate discrepancy bands
and fully consistent cross-era player-state transport remain a subsequent step;
do not borrow J_BOTH bands for J_POINT_BOTH.

## Execution and acceptance

Independent stage receipts with source/protocol/producer hashes, no overwrite
of complete outputs. Durable verbose logs; up to three CPU processes, one compute
thread each. Diagnose first; run early/late average-mode pilots and chronological
uncertainty regression tests before the full follow-up. The full follow-up run
requires a verified launch command; no new NN training campaign is authorized.
Report quantitative diagnostic results and actual pilot runtime, then finish
the current handoff or continue the authorized bounded analysis. Do not start
the proposed loss/channel/seasonal-refit experiment until its design is agreed.
