# Quarter point integration — 2026-09-07

**Subsequent checkpoint:** the runner described as next work below is now
implemented, with two completed real warmup origins. Read
`ASOF_POINT_BENCHMARK_STATUS.md`. The source Q1 profile extracts were incomplete
for later queries; the runner reconstructs full preseason snapshots and verifies
their saved overlaps/forecasts without excluding cells. This document's bridge
specification remains unchanged. No primary-season point result is claimed.

## Bounded next deliverable

The additive single-origin numerical follow-up is complete; see
`ASOF_ADDITIVE_TUNING.md`. This document specifies the **player/channel
accounting bridge** before implementation or point-score results. It is a
dependency of the quarter point comparison, not authorization for the full
44-origin additive sweep, a scorer promotion or a new teammate mechanism.

The first deliverable is a pure, tested helper plus a saved-input reconstruction
check. Preserve current scoring functions and completed research artifacts.
No database access, source-cache regeneration or target-point evaluation is
needed to verify this accounting decision.

## Allocation decision: preserve within-category player shares

Start with the current profile reconstruction and its alpha=1 team usage scale.
For each player, keep the six located shot-attempt rates, FTA, ORB and turnovers
used by `channel_points_validation._predict_components`. Rates are per offensive
possession. The four usage components are **2PA, 3PA, 0.44 FTA, TO**, not literal
mutually exclusive possession endings.

For calibrated target component totals C'_c and reconstructed totals C_c, use
the category multiplier **k_c = C'_c / C_c**. Apply k_2 to each player's four
two-point locations; k_3 to both three-point locations; k_FT to his FTA; and
k_TO to his turnovers. ORB is unchanged. Within each category, players retain
their relative attempt shares; each player's within-two/within-three location
mix is unchanged. Team totals must match the supplied calibrated components,
whose sum must equal the original team usage budget.

**Player total usage is allowed to change.** Preserving both each player's total
usage and the new team category totals would require a different allocation
assumption. It could force a shooter to give up other attempts whenever the
team's three-point share rises. We do not introduce that role constraint into
an empirical calibration control. Print each player's before/after usage so
this decision is visible. This is not evidence that the new allocation is
optimal or that players adapt causally to new teammates.

Zero-to-zero categories stay zero. A positive target with no source attempt
mass, or positive attempts with no within-category location mix, is an explicit
unsupported accounting input: raise with the category named, never silently
invent a shooter/location or drop the mass. The saved observed-cohort check
must report whether this occurs; no rows may be silently excluded. Missing
profiles retain the existing explicit unknown-row mask. These are research
input limitations, not a proposed fan-facing coverage gate or a claim that
arbitrary-lineup support is solved.

## One ledger for creation, making and passing demand

Recalculate all terms from the **same allocated attempts**:

- Creation points: the supplied training-only conditional valuation applied to
  the nine team channels, plus its intercept once per team, not per player.
- Making residual: each player's two-point, three-point and FT attempts times
  his corresponding shooting surplus over the same supplied league reference.
  Location-weighted expected two/three conversion uses his retained location
  mix. Never change the creation reference while keeping the making reference
  from another environment.
- Assisted-finishing demand: allocated expected field-goal makes times that
  player's prior assisted fraction. Assist supply stays the existing native
  sum of `rast`; deficit is max(demand minus supply, zero). An assisted make is
  not an extra make or extra points.
- ORB stays the existing native sum and conditional-valuation term. This
  intentionally preserves the incumbent rebound limitation rather than silently
  inserting the separate competing-capture model into a freshness experiment.

Expose per-player creation channels, usage, creation-point contributions and
making contributions, the team intercept, and the exact summed point score.
Return the uncalibrated point score and deficit separately. The later point
calibration/deficit coefficient is not fitted by this helper.

These conditional regression valuations are **not causal points per event**;
the previously documented negative isolated ORB value remains a limitation.
The bridge is a coherent reuse of the current scoring construction, not the
finished physical possession model.

## Acceptance checks

1. With no team adjustment, reproduce `_predict_components`, the current
   assisted-demand/supply calculation and fixed-budget point arithmetic.
   Passing the reconstructed component totals reproduces that same control.
2. Assigned player channels sum exactly to supplied team totals; total usage
   is conserved. Within-category player shares/location shares stay unchanged.
3. The player contributions plus the single team intercept reproduce the
   score; recomputed demand follows allocated attempts. ORB and supply do not
   inadvertently scale with shots.
4. With physical test valuations (2/3 times league conversion and FT conversion,
   zero other terms), creation plus making equals direct expected player points.
   A change in the league reference cancels between the two terms when shooting
   ability and attempts are held fixed. This catches double counting.
5. Player-slot permutations preserve totals and permute player outputs;
   repeated identical profiles receive identical treatment, without pair IDs.
   Validate shapes, finite covered inputs, budget identity and impossible zeros.
6. Before any point evaluation, reconstruct raw and calibrated opportunity
   totals on the saved common cohort for both recent profile bandwidths; preserve
   every key/exposure and report maximum reconstruction errors. This can reuse
   existing CSV profiles, environments and prior-only calibrated totals. No new
   profile fit or target points are needed for this check.

## What remains before the point benchmark

The quarter benchmark still needs a separately specified orchestration contract:
which profile/league refresh arms, shared prior-only point-calibration histories
and league-level controls, additive origin fits, common cells and reporting.
Do not recycle annual integer-season normalization or let either model observe
newer games than its comparator. Keep raw/calibrated opportunity controls and
do not credit generic calibration as complementarity. Freshness, historical
weighting, and response to a new teammate context are different hypotheses.

Counterfactual checks and honest OOD uncertainty remain co-equal with accuracy.
No result of this accounting bridge by itself licenses the full five-center
offensive mean, a neutral opponent interpretation or a calibrated synthetic
lineup interval.

## Completed bridge and saved-input reconstruction

`experiments/asof_point_allocation.py` implements the pure bridge without
changing any incumbent scoring function. **446 tests pass**, including 21 new
bridge tests. Unadjusted scores reproduce the original construction; supplied
targets conserve category totals while changing player usage. Player-level
contributions, refreshed assisted demand, fixed supply/ORB, physical-valuation
cancellation, permutations/repeats and invalid/unknown inputs are tested.

The lead implemented this part locally after the second worker call was denied
by the permission reviewer. Adam subsequently **explicitly approved sending
relevant task instructions and repository code to Anthropic through his Claude
Code subscription for future bounded worker runs**. The already-completed local
implementation was not re-delegated. Existing lead-review/scope/no-API-fallback
rules still apply; this approval does not authorize publishing or other actions.

The saved-CSV replay completed in **2.20 seconds**. It checked both recent180
and recent365 profiles against all three saved valuation/reference environments
(historical_frozen, recent_frozen, recent_live): **288 profile/environment/window
checks**, including 2015 warmup. Primary 2016–2026 support remains **5,607 cells /
726,364 possessions per profile**, with no exclusions or unsupported allocations.
These environment replays are accounting checks, not independent observations.

Maximum reconstruction discrepancies:

- raw opportunity components: 5.69e-14 per100;
- calibrated opportunity components: 4.27e-14 per100;
- raw nine-channel creation, assist supply and ORB: exactly zero;
- raw making: 7.11e-15 pts/100;
- raw assisted demand: 1.43e-14 per100;
- assigned team usage: 1.14e-13 per100;
- player contributions plus team intercept versus score: 4.27e-14 pts/100.

No actual point targets were loaded, no calibration was fitted and no point
accuracy result was computed. The replay consumed the existing profiles and
previously calibrated channel forecasts, not reconstructed player histories.
All source/code hashes and prior-date boundaries pass; original input files
are unchanged. Outputs are `experiments/cache/asof_point_allocation_2026_manifest.json`
and `_windows.csv`. The manifest pins inputs/code and the private verification
script hash. Independent output/hash/count checks pass. No jobs remain running.

Private verification: `/private/tmp/basketball-point-allocation-replay.py` and
`.log`; `/private/tmp/basketball-point-allocation-full-tests.log`.

## Next implementation: quarter point evaluation

The bridge and additive one-axis checks are done; **do not rerun them as open
research questions**. The next substantial unit is the date-safe, resumable
quarter point runner, not another channel diagnostic. Before its first scored
run, finalize and record the runner contract, including computational caps and
per-origin numerical-boundary handling. Useful settled inputs/controls:

- Frozen-versus-live weighted player states can use the existing same-bandwidth
  Q1 snapshot versus each quarter's snapshot. Keep both 180/365 role bandwidths
  and the same 730-day shooting bandwidth; do not choose a production winner
  from the old intermediate results.
- All three saved environment states are available. Historical_frozen versus
  recent_frozen isolates historical weighting at the same date; recent_frozen
  versus recent_live isolates updating under the same weighting. Each includes
  the matching conditional valuation AND making reference.
- Keep the historical-frozen usage budget for the first controlled comparison.
  Changing that budget is a separate intervention already known to move shot
  totals; it must not be bundled invisibly with valuation refresh. Preserve raw
  and calibrated opportunity arms. Frozen-player calibration needs its OWN
  earlier-window forecasts, not offsets fitted on the live-player arm.
- Common raw-point targets and completed-window point-calibration histories
  must be identical for additive and structural models. A shared current
  prior-league level can be separated from each score; the additive offensive
  coefficient sum is relative, whereas the structural creation+making score is
  absolute. Do not subtract a league mean twice from the additive side.
- Additive warmup forecasts also require inner validation windows: the existing
  source schedule begins in 2015, so matching-quarter tuning for 2015 requires
  constructing the **2014 causal schedule** from already-cached game dates.
  Preserve/reproduce every existing 2015–2026 origin; no future quantile cutoffs
  or source-schedule overwrite.
- Every origin must use its own checked additive selection; the successful
  2026 Q3 sensitivity does not license globally pinning its penalties. Save
  origin fits and completed selection artifacts so interruptions do not restart
  earlier work. No full 44-origin sweep has been launched or completed here.

The actual point comparison, named counterfactual recheck under this newer
construction, complete matchup defense and latent/OOD calibration remain open.
