# Strict-date additive comparator foundation — 2026-09-07

## Purpose and scope (specified before implementation)

The quarter point comparison needs an additive control allowed to observe the
same recent games as the structural model. Keep the established chemistry-free
objective: box/height/position prior + career player effect + season player
effect + shared experience bins, with separate offensive/defensive coefficients.
This milestone implements date-safe fitting and validation inputs, not a new
estimator, tuned benchmark, or scorer promotion.

The old `fractional_eval.py` globally normalizes outcomes and uses future
possession quantiles for slices. It is not the implementation to reuse. Reuse
the tested `matched_additive.SpectralFit` algebra, not those information rules.

## Information and modeling decisions

- The cutoff is a local, timezone-naive game date; exclude the entire cutoff
  date, even if the caller supplies a time of day. Filter before reading
  outcomes, player identities, computing profiles, or normalizing outcomes.
  Missing game dates are an error because they cannot be safely classified.
- Derive season/week labels inside the prefix using the existing calendar
  convention (including COVID), overwriting any supplied week labels.
  Subtract prefix-only season/week means, then prefix-only season/side means.
  Recompute the unfinished week when the cutoff advances.
- Compact player IDs from prior possessions only. Construct profile priors
  using only player-game rows for those prior games. Keep the existing
  cumulative EB box prior and its prefix-fitted column selection, scaling,
  roster features and SVD; do not silently bundle recency with era z-scoring.
  Refresh cadence is the change here; profile bandwidth selection is later.
- Supply roster and debut metadata explicitly, without database/file access
  in the new helper. Height/position/debut are pinned static metadata, not
  historically versioned measurements; disclose this limitation. Restrict
  imputation/transforms to prefix players. Missing debut falls back to that
  player's first observed **prior possession** season. Unseen query players
  have zero player and experience contribution and an explicit support flag;
  they do not acquire a fabricated veteran bin.
- Every nonempty observed season contributes a Gram block, including a short
  current season. Do not inherit Stack's silent <2,000-possession exclusion.
  Accumulate in float64. No target normalization based on the scoring window.
- Return the latest observed season's fitted delta separately from the base.
  Within-season forecasts thus have access to current-season delta; preseason
  forecasts have only the previous observed delta. A future caller must choose
  its carry coefficient on completed prior validation data. No rho is fixed or
  selected by this foundation.
- Expose the last observed season's raw side means as a prior-only baseline
  control (fallback to its overall mean if a side is absent), not a fitted
  current-environment claim. Later point comparisons must make league-offset
  and calibration choices explicit and matched across the relevant controls.
- Validation summaries must require a completed interval: start >= fit cutoff,
  stop > start, stop <= outer selection cutoff. Filter to that interval before
  reading outcome values. Preserve raw future points minus the supplied prior
  baseline; never detrend using validation/test-window outcomes. No grid search
  or automatic model selection in this helper.

## Acceptance checks

Future/same-day outcome, identity and player-game mutations leave the earlier
fit unchanged; advancing the cutoff actually incorporates newly prior data.
Partial-week normalization matches a direct truncated-frame calculation and
differs from the leaking full-week calculation in a non-vacuous fixture.
Season Grams and fitted coefficients/latest delta match an independently
constructed dense penalized objective. Cover a <2,000-row season, disabled
blocks, missing debut, unknown players, slot permutations, two sides, strict
completed-window selection, raw-target validation losses, and supplied metadata
without database access. Existing annual callers retain their default behavior.

No source-cache rebuild, scraping, database mutation, expensive sweep, accepted
scorer/page change, bandwidth selection or claim of a predictive improvement.
This is one dependency of the still-pending quarter point factorial. The three
product standards in `CONTEXTUAL_MODEL.md` remain co-equal.

## Completed foundation

`experiments/asof_additive.py` now implements `AsOfPrefix`, pure identity and
experience designs, explicit player-support counts, separate base/carry
predictions, and completed-window validation sufficient statistics. It uses
the existing `SeasonBlock` / `SpectralFit` solver and exposes a checked `solve`
wrapper. The four penalties and carry remain caller decisions, not defaults
chosen here. Existing `prior_ridge` callers retain their default behavior;
optional `roster=` injection permits a fully database-free date-prefix build.

**40 new tests; 318 total tests pass.** The focused additive/benchmark suite
passes 49 tests. Direct dense penalized fits reproduce theta, shared experience
and latest-season delta across 12 penalty corners including disabled blocks.
Full profile/SVD output with injected metadata reproduces the mocked legacy
database path. Cutoff-day/future outcomes, identities, counts and future-only
metadata cannot move an earlier fit. An additional test changes discarded
values to strings: whole-column dtype inference must not alter valid retained
rows. Advancing the cutoff does change the fit; a deliberately loud future
partial week exposes the normalization leak that this helper avoids.

Opus implemented three authorized files, then lead review tightened parsed-date
and outcome handling, query feature validation, threshold/profile checks and
mixed-type discarded-row handling. The worker independently added a float64
identity design excluding OOV columns before completion, resolving the early
review concern about float32 Gram accumulation. No outstanding review issue
is being treated as an accuracy finding.

### Bounded real-cache smoke

A small integration check uses sampled dates 2023-10-24 through 2023-10-26 and
2024-10-22 through 2024-10-25, with cutoff **2024-10-24**. It reads existing
cache files explicitly (no loader that can regenerate them) and patches database
access to fail. Training: **4,769 possessions / 24 games / 370 players**, with
2,377 and 2,392 possessions in its two season blocks. Queries: 2,814 possessions,
of which 1,800 have all ten players in the sampled fitting map. This is a tiny
sampled-date fixture, not full-history training or a coverage result.

Changing every later outcome and player identity, and later player-game counts,
changes fitted coefficients by **exactly 0**. The quadratic validation loss
matches direct row predictions within **2.22e-16**. Arbitrary test penalties
are used only to verify arithmetic; no accuracy metric, tuned rho or ranking
is claimed. Pinned metadata comes from the existing ratings export and bio CSV;
the export covers only 286 of these 370 sample players. Do not silently use
that incomplete export as the final benchmark's roster source.

Epoch `1788577025507373000-37f71aa800a1`, cache key `ba7aeb377198`.
No source cache, database, accepted scorer, result CSV or page was changed.

## Resume next

**Continuation 2026-09-07:** `ASOF_ADDITIVE_TUNING.md` now implements completed
matching-quarter selection and records the finished 2026 Q3 pilot. 387 tests
pass. The full fit/search/refit took 253.7 seconds, so runtime is measured, not
speculative. One prior-penalty edge remains provisional; the tuning document
specifies the next narrow sensitivity. It also records the opt-in prefix-only
debut reconciliation policy; the foundation's default remains strict. Follow
that newer checkpoint instead of repeating the implementation steps below.

This is a completed dependency, **not the completed fresh-additive benchmark**.
Before a sweep, specify completed prior-window penalty/carry selection and
league-baseline/calibration controls. Do not pass these date prefixes to the
annual `select_penalties`, which expects integer seasons, or pin penalties
from the smoke test. Pay particular attention to current-season delta versus
previous-season carry: they are not the same forecast horizon.

Then build the quarter point factorial on the existing common cells, retaining
raw/calibrated opportunity controls and explicitly assigning team channels back
to players/locations. Simple category scaling preserves within-category player
shares but changes each player's total usage; preserving both row usage and
column totals is a different allocation assumption. No choice between those
has been implemented or credited as a new mechanism. League conversion changes
also enter both creation valuation and the making reference; avoid double
counting their effect. No additional generic FTA audit is needed first.

The helper currently rebuilds prefix Grams/profiles. Measure real full-prefix
cost before implementing incremental caching or launching 44-origin tuning.
No full-corpus fit, bandwidth choice, grid search or OOD calibration was run.

Private verification artifacts (do not publish worker snapshots/logs):

- Worker contract: `/private/tmp/basketball-opus-asof-additive-contract.md`.
- Worker audit: `/var/folders/0q/vr0lp8p56s7ddsz7k2d30j100000gn/T/opus-worker-501/run-df6yymoi`.
  Exit zero, exactly three allowed paths, no warnings or permission denials.
- Full tests: `/private/tmp/basketball-asof-additive-full-tests-final.log`.
- Smoke script/log: `/private/tmp/basketball-asof-additive-smoke.py` and
  `/private/tmp/basketball-asof-additive-smoke-final.log`.

All jobs are complete; no worker needs restarting.
