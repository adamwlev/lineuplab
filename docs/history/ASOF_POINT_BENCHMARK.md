# Quarterly point comparison — registered 2026-09-07

## Question and scope

Does current player evidence, current league valuation, or calibrated opportunity
mix improve the structural point model against an equally date-refreshed,
chemistry-free additive control? This is a controlled forward-prediction
experiment, not a new teammate-response mechanism or a production selection.
All three standards in `CONTEXTUAL_MODEL.md` remain co-equal. Counterfactual
means, latent/OOD intervals and full opponent defense remain unfinished; a
point-metric win alone cannot promote this construction.

Implement a resumable runner, then perform at most the first TWO warmup origin
fits (2015 Q1 and Q2), each invocation capped at 450 seconds. Synthetic tests
and a source/preflight check are included. This authorizes reconstructing
in-memory research snapshots from existing caches, not rewriting those caches,
scraping, database access, the full 48-origin run, or any scorer/page change.
No point result was inspected in choosing the following protocol.

## Cohort, dates and target

Reuse exactly the source `asof_channels_2026` four-window schedule and common
five-man cells, >=50 offensive possessions per window. Preserve 2015 warmup;
primary 2016–2026 is 44 windows / 5,607 cells / 726,364 possessions. The common
cohort is a diagnostic population, NOT a proposed product coverage gate.
Every arm has identical keys, exposures, raw targets and calibration histories.
Missing or irreproducible cells stop the run rather than silently shrinking it.
Additive unknown-player effects remain zero with explicit support counts;
they are not a reason to filter the cohort.

Target: 100 times the raw mean `points_scored` on exactly those offensive
possessions in [start, stop). Report full-window raw offensive targets, not
test-demeaned or opponent-adjusted targets. This compares offense in observed
deployment; it does not establish a neutral-opponent or full-matchup estimand.
Also retain games, exposures and whether the sorted five was observed strictly
before the origin. Future lineup identity is a query, never a training feature.

Build a 2014 four-window schedule from existing cached game dates using
`asof_state.rolling_windows`, for the additive warmup inner validation only.
Reproduce every existing 2015–2026 source boundary/count. Never change the
source schedule or choose boundaries from future quantiles. All state/valuation
fits exclude the whole cutoff date. Only completed windows with stop <= start
can enter either calibration stage.

## Structural factorial and accounting

24 base arms: role half-life {180,365} days x profile cadence {frozen,live} x
environment {historical_frozen,recent_frozen,recent_live} x opportunity
{raw,calibrated}. Shooting half-life is 730 days throughout. Frozen means the
same estimator before Q1, not the annual latest-season estimator. Environments
are the saved matched conditional valuations AND shooting references; recent
means the existing 365-day weighting. Usage budget stays historical_frozen in
ALL arms. Weighting, cadence and budget changes must not be conflated.

Important source correction: saved Q1 profile CSVs contain only identities used
in Q1 queries. They omit identities needed by later cells in all 72 later
profile/windows. Reconstruct complete frozen snapshots with `PlayerHistory`
from existing player-game/date caches; reproduce their saved overlapping
profiles and all saved frozen channel forecasts. Use saved live profiles,
checking their cutoff/last-observed dates. Do not remove later-season cells to
fit a truncated Q1 extract. Q1 raw player profiles and channel forecasts must
agree. In later seasons, final calibrated Q1 predictions may differ because
the two cadence policies have different completed calibration histories.

For each of the four profile/cadence streams, fit opportunity offsets on that
stream's OWN completed-window raw forecasts and actual channel totals, using
unchanged `fit_prefix_offsets` (365-day decay, >=30 cells, otherwise raw).
Share offsets across valuation environments, since valuation does not change
opportunities. Reproduce saved live calibrated forecasts and frozen/raw source
forecasts. Never borrow live offsets for a frozen stream.

Use `asof_point_allocation.predict` for all raw/calibrated scores and deficits.
Preserve player shares within categories, recompute shooting and assisted
demand from assigned attempts, keep native assist supply and ORB. Retain
explicit player usage/creation/making ledgers and the single team intercept.
The negative conditional ORB coefficient is not a causal price. This is not
the separate miss-conditioned rebound mechanism or a new role allocation fit.

## Shared league level and point calibration

Let L_t be 100 x `recent_live.points_per_poss` from the saved strict-prior
365-day league environment at origin t. It is shared by EVERY arm.

- Additive R_t is the offensive sum of identity + carried season effect +
  experience, in points/100. It is already relative; do NOT subtract L again.
- Structural R_t = its absolute creation+making score minus L_t.
- Target residual Y_t = raw actual points/100 minus the same L_t.

For every structural base arm, retain BOTH calibration-only and
calibration-plus-assist-deficit. Fit expanding possession-weighted least squares
on all completed prior common cells, without recency weighting at this stage:

    Y = a + b R [+ d D],  b >= 0, d <= 0
    current prediction = L + a + b R [+ d D]

Use each past origin's own saved R, D and L, never a retrospective refit of its
players. Coefficients are separate per arm; protocol, dates, rows and weights
are identical. Before 30 prior cells, disclose cold start and use a=0,b=1,d=0;
retain rows and raw forecasts for warmup. Invalid eligible inputs or a failed
optimizer are errors, never a silent finite-row filter. Disclose training cell
count, possession sum, latest completed stop, rank and coefficients.

Additive has the same calibration-only control, plus an additive+deficit
diagnostic using the EXACT deficit from recent180/live/recent_live/calibrated.
Thus there are 50 scored arms (48 structural + 2 additive), not 50 independent
experiments. The designated structural comparison is recent180/live/
recent_live/calibrated/+deficit; recent365 is a registered sensitivity, NOT a
production bandwidth selection. Report targeted one-factor contrasts, not a
post-hoc winning factorial cell. Also show calibration-only controls so generic
calibration is not called synergy.

## Additive fitting and numerical status

Each origin calls its own checked `choose_window_plan` / `fit_origin`, with
the original default grids and two expansions, min_profile_poss=200 and the
generic `prior_observed` debut policy. Preserve uniform fitting weights,
prefix-only normalization, all nonempty season blocks and the current-season
carry rules. The pinned roster CSV from the completed pilot replaces database
access. Height/position/debut are static metadata, not historically versioned.

Persist the chosen penalties/rho, ALL candidate losses, original audit flags,
plan, inner/outer metadata and coefficient snapshot before point scoring.
No global Q3 penalties, no automatic additional grid walks and no outcome-based
retuning. Keep `provisional` exactly as returned. A completed origin with a
provisional search is computationally complete, not certified converged.
Report finite boundaries and adjacent RMS changes for every origin, including
how many scored cells/possessions depend on provisional tuning. The earlier
Q3 one-axis finding applies only to Q3, not other origins. Review the two
warmup audits before authorizing a larger batch; a material unresolved boundary
requires a separately registered validation-only follow-up, not a convenient
test-result adjustment. This is numerical research status, not an OOD gate.

## Persistence, provenance and execution limits

New output directory only; no overwriting old research prefixes. Pin source
epoch, explicit input hashes, relevant computational module hashes, fixed
protocol, extended schedule and pinned roster. Read existing artifacts directly;
do not call rebuild-capable context/GP/outcome loaders or access the database.
Validate the completed source manifest/hash chain and source protocols.

Atomic per-origin fit checkpoint, then atomic completed-origin bundle containing
forecasts, player ledgers, actual targets, calibration/offset coefficients,
support/coverage and audit metadata. The next invocation reuses verified
completed fits/origins; never rerun them. Refuse mismatched source/code/protocol
or corrupt checkpoints. Failures preserve completed checkpoints and record an
incomplete/paused run with the failing phase. A partial origin is never accepted
as complete. A second process must not write this directory concurrently.

Default --max-origins=1, --max-seconds=450; count newly completed origins, not
already verified ones. Runtime caps are wall-clock guards, checked between
phases; BLAS may only return control after a kernel finishes. A resume at its
limit is paused, not a failed model or a finished 48-origin benchmark. Full
metrics must never be presented from an incomplete set as the full study.

First bounded real check: 2015 Q1, then an explicit resume for 2015 Q2. Verify
Q1 files/hashes are unchanged and Q1 fitting was not called again. Source
reconstruction, complete common support and calibration provenance must pass.
Do not launch 2015 Q3 or the full sweep in this initial authorization.

## Reporting and acceptance

Preserve cell predictions and per-player accounting for the disagreement review
Adam requested. Report possession-weighted MAE, bias, RMSE, ordinary correlation
and raw r², with counts, by origin/season/arm, all and novel. Undefined variance
metrics stay explicitly undefined. Report paired season differences (quarters
are not independent seasons) for the designated contrasts once all primary
origins are complete. This initial runner does not invent latent uncertainty
intervals or recycle annual corrected-correlation headlines onto quarter cells.

Tests must cover cutoff/future-outcome exclusion in both calibrations, exact
league-offset accounting, shared histories, own-stream frozen calibration,
per-player sum identities, unknown additive slots, Q1 equivalence, same source
keys/exposures, deterministic resume, partial-fit recovery, corruption/source/
code/protocol mismatch, runtime interruption, duplicate writer protection and
synthetic end-to-end flow with fitting injected/mocked. Run the full unittest
suite with basketball25. No estimator, accepted scorer or page changes.
