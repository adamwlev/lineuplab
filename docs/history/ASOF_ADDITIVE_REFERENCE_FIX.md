# Additive offensive reference correction — 2026-09-07

## Decision before corrected results

Adam authorized the bug fix and complete saved-fit replay after the original
48-origin run completed. This is an explicitly post-diagnosis scoring correction,
not an untouched new experiment or outcome-based hyperparameter selection.
Preserve `asof_points_2026` and its immutable protocol/code. The defect is that
joint offense/defense fits can have offsetting levels; their unanchored offensive
halves are not on one stable league-relative scale across origins. Original
validation and accounting checks did not identify this measurement error.

No penalty floors, refits, new profile model, source-cache changes, known pairs,
scorer promotion or deployment. The three co-equal product standards remain.

## Fixed reference

At origin t, score each prior player with THAT origin's saved identity,
rho-carried season effect and experience at the FORECAST season t. In units
of points/100 per player, call this total v_pt. Use every offensive possession
strictly before the origin's start, not just common evaluation lineups. Give
each possession on date d weight `2 ** (-(t-d).days / 365)`. This is a 365-day
half-life over all prior history, NOT a trailing-365-day hard window, matching
the existing `recent_live` league level. No future query/exposure/outcome enters
this reference. Weight players by their offensive on-court possession counts.

Let m_t = sum(weighted player exposure * v_pt) / sum(weighted player exposure).
The five-player league reference is M_t = 5*m_t. For a supported five,
corrected score R_t = original offensive sum - M_t. Per-player contributions
are v_pt-m_t. Preserve raw base/carry/experience and record their reference
means separately for explainability. An unknown query player contributes zero
on this centered scale, not a fictitious -m_t; support stays disclosed. Every
real reference player must be known to the saved prefix. All original query
slots happen to be supported, so the real correction is constant within origin.

Reconstruct the same weighted prior raw league scoring level from the context
and compare to each saved L_t. Fail on a mismatch, do not substitute another
population or alter L_t. Retain source hashes and each reference's dates,
raw/weighted possessions, player exposures and reference decomposition.

## Chronological replay

New output only: `experiments/cache/asof_points_centered_2026/`. Reuse all 48
verified fit/bundle checkpoints. In each origin, replace only the two additive
scores and rebuild their expanding prior-only point calibrations using each
past origin's OWN corrected R, saved L and saved deficit. Same fitter,
constraints, cold-start rule, observations, weights and forecast dates as before.
Do not merely subtract M_t from final predictions, reuse contaminated old
calibrators, or re-score past origins with later player coefficients.

Retain original additive arms alongside corrected arms in the replay output.
Keep all 48 structural arms and their predictions unchanged except possible
CSV round-trip noise <=1e-12. No uncertainty claim follows from this mean fix.
Original numerical/provisional flags remain original, not upgraded to stable.

## Verification and reporting

Focused checks: prior reference cutoff/future mutation invariance, direct
possession-versus-player-exposure arithmetic, fixed zero-centered reference,
known/unknown query behavior, lineup order invariance, cancellation of arbitrary
opposite offense/defense shifts in the corrected rating, chronological
calibration, identical target/weight populations and unchanged structural rows.
Reject mismatched/corrupt sources; never overwrite the original run. Tests do
not fit the model or rebuild caches. Then run the FULL replay, not another
one-origin pilot. Lead independently checks real saved arithmetic and sources.

Report original/corrected additive, designated structural and fixed controls;
MAE/RMSE/bias/correlation/raw r2 by origin and season, pooled primary metrics,
and paired season differences with uncertainty. Also separate within-quarter
association from between-era level tracking. Do not average quarter correlation
coefficients as an overall statistic. Pool centered covariance/variances for
within-quarter correlation. Exclude all 2015 warmup from primary summaries.

Next diagnosis uses season-five aggregates of the retained quarter observations
at >=500 possessions and >=20 games; disclose partial-season coverage. Preserve
quarter-specific predictions in aggregation. Review the largest extra structural
absolute errors and persistence across earlier/later quarters, with complete
additive and structural accounting. These selected failures are descriptive,
not causal effects or a representative model comparison.
