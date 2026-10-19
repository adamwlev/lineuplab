# Game-situation diagnostic — protocol fixed 2026-09-17

Adam authorized implementation of a diagnostic situation model, not adding
game-state controls to the fan-facing model. No neural/additive refits, scorer
promotion, input-cache rebuild, scraping, database mutation, deployment or
commit. New source/derived outputs only; preserve completed artifacts. Direct
implementation, no delegation. This protocol precedes its fitted readout.

## Estimand and controls

Keep all original v14 forecasts and 5,607 primary common lineup-quarter cells
(2016–2026, 44 origins). Fit shared nuisance event/point rates from strictly
earlier games, using cached possession-start context and shot labels. Three
nested models: ENV (dated league rate); CLOCK (period/time); MARGIN (add
offense-perspective pre-possession margin interacting with period/time).
No player identity, opponent, possession duration, realized foul, result,
lineup exposure or future season statistics are explanatory inputs.

Regulation periods1–4 and OT are separate. Fixed remaining-time bins:
[0,30], (30,60], (60,120], (120,240], (240,480], (480,720]; OT may
occupy only bins consistent with its300-second limit. Margin bins <=-10,
-9..-4, -3..3, 4..9, >=10. Unknown context remains an explicit category.
Clock-only excludes margin entirely, including its missingness.

Use a fixed three-calendar-year approximation (1,095 days) before each cutoff,
with365-day half-life. This supplies the dated league environment. Fit partial
pooled rates: each clock bin gets500 effective exposure units of the global
prior; each margin×clock bin gets250 units of its clock prior. Exposure units
are possessions for counts, attempts for percentages/shares. These are fixed
regularization choices, not tuned results or a claim of optimality. Save all
training effective exposures, rates, fallback flags, cutoffs and actual dates.
An unsupported bin falls back to its parent. Unknown context gets the global
rate rather than a learned missingness effect. No sweep or selection.

For each target, center the contextual effect to zero under the **historical
training exposure distribution**, including label masks. This defines an
origin-specific average environment, not a special score/clock entered by a
user. It is a descriptive historical reference, not identified causal quality.

## Targets and comparisons

Count rates per100 possessions: points, FGA, FTA, turnovers, 3PA.
Percentages: overall FG%, FT%, six location shares, and six within-location
make percentages. Apply original grouped event-observation masks; shot-location
targets require complete FGA and location labels. Never drop point cells due
to unavailable event labels. Unsupported cell percentages remain unavailable.
Raw event aggregation must reconcile to original grouped labels before fitting.

Compute each cell's actual-situation minus historical-reference expected rate,
using its realized context mix, and subtract that offset from the observed
target **for diagnostics only**. The same adjusted point target is compared
against additive, oldHALF, and ROLE_SL / RB_RENEW_FAC / RB_RENEW_FAC_SHIFT
direct and half forecasts. Event forecasts exist only for the NN arms.
Diagnostic adjusted rates can leave physical bounds; do not clip, reinterpret
as a generative event ledger, or export them as predictions. Counts and
percentages have different denominators; never add their adjustments together.

Using realized future situations/exposures makes these conditional diagnostic
comparisons, **not new pre-quarter forecast scores**. ENV preserves the original
target exactly. Report original metrics alongside CLOCK and MARGIN, including
season comparisons, novel/recurring, >=200poss, and the frozen primary transfer
cohort. Save all cell offsets and revisit the fixed repeated/transfer library,
especially2016Cleveland, without choosing a new model from the diagnostic.
Also report held-out nuisance-only performance and sparse-bin support.

## Interpretation and limits

Margin may mediate lineup quality; CLOCK and MARGIN must remain separate.
State effects also absorb composition differences: shared rates are not causal
effects and do not remove all confounding. Shot-attempt conditioning similarly
does not identify shooting quality. No claim of better latent OOD calibration
or five-center behavior follows from this diagnostic. All three product
standards remain binding. Bonus/foul status is a later metadata audit, not an
input in this first build. Completion-lineup attribution and reconstructed-score
caveats from ASOF_DEPLOYMENT_AUDIT remain.

## Verification and outputs

Test clock/margin boundaries, unknowns, prior-only exclusion (including poisoned
future outcomes), parent fallback, zero-mean historical centering, partial
pooling, common adjustment across models, row-order invariance and label masks.
Reuse the existing pre-possession score tests. Verify unchanged v14 producer
hashes, original point metrics/exposure and event ledgers. Record source/code/
protocol hashes, verbose origin logs, all derived tables and COMPLETE receipt
under a fresh prefix refusing overwrite. No long neural run is required.
