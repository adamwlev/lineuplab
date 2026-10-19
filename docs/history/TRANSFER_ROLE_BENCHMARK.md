# Historical team-change / role-transport benchmark — frozen first pass

Registered 2026-09-17 after the v14 review, before computing transfer-cohort
model errors. Adam authorized the next work. Codex implements directly.
This is retrospective development on already-used seasons, not new confirmatory
evidence and not a causal estimate of a trade. No new fits or scorer promotion.

## Questions

1. On substantial first-quarter lineups containing offseason team changers,
   do the retained contextual candidates outperform additive and old HALF?
2. Does the explicit proposed-minus-historical role channel help, with player
   values and all other model inputs held fixed?
3. Which event/allocation errors recur across both helpful and harmful cases?
   Do finite-game intervals behave differently on this cohort?

## Data and cohort (fixed before cohort scores)

Use the completed v14 prediction cells and grouped labels. Obtain game identity,
date, home and away team **only** from the local DB in a read-only repeatable-read
transaction. Resolve player/game/team membership from the original possession
context, not from current rosters or guessed team labels. Preserve source files;
save a new source-linked metadata extract. Normalize Charlotte Bobcats/Hornets
to one franchise. Ambiguous same-game membership or unmatched mappings are
reported and excluded rather than assigned arbitrarily. No scraping/DB mutation.

Seasons2016–2026, q1 only. Season bounds come from the existing frozen schedule,
including its historical playoff coverage; don't silently redefine the calendar.
An **observed opening-season team change** is a player's first offensive appearance in
the season on a different franchise from his last offensive appearance in the immediately
previous season. Require >=10 offensive-appearance games and >=300 offensive
on-court possessions in that previous season. The new first appearance must
fall within the destination's first10 scheduled/recorded games and inside q1.
Do not require future roster stability, a positive team result, or a successful
season. No requirement on the player's name or additive coefficient.

This detects changes in observed team affiliation, including free agents and
possibly early-season moves; it does **not** certify transaction type/date.
First appearance and eventual playing time are retrospective cohort labels,
never model inputs. Injured/inactive players and never-used lineups cannot be
evaluated this way. Print these selection limitations and exclusions.

Evaluate q1 lineup cells belonging unambiguously to that destination and
containing >=1 qualifying mover. A lineup containing multiple movers contributes
once to pooled metrics. The case library may list all its movers, but never
count the same possessions twice in an aggregate.

Primary substantial-cell threshold: >=200 possessions and >=5 observed games.
Mandatory sensitivities: every available matched cell, >=100 and >=500
possessions (the same >=5-game rule for the latter two). Print eligible moves,
moves with any evaluated cell, team-seasons, cells, games and possessions at
each step. Zero-scored moves remain in the registry. A two-or-more-mover slice
is descriptive. These rules select a benchmark population, not a product gate.

## Forecasts and cutoffs

Reuse additive, old V9 HALF, and three-seed ROLE_SL, RB_RENEW_FAC,
RB_RENEW_FAC_SHIFT, each direct and external half. All states, fit normalizers,
weights and point-calibration parameters are the saved q1-origin artifacts.
No q1 events refresh player states or fit any benchmark parameter. Assert
identical lineup keys/outcomes/possession counts across arms.

**Zero-shift channel replay**, for RB_RENEW_FAC_SHIFT: using the same weights,
replace the last four role-head inputs with the standardized representation of
raw context change zero: `(0 - saved_shift_mean) / saved_shift_scale`.
Retain recent-role inputs, individual capabilities, proposed-team main messages,
rebound inputs and calibration. Apply to all five players in a queried unit.
Replay unchanged inputs first and reproduce saved raw forecasts within1e-4
pts100. Average separately calibrated seeds, then form the external half.

This is a bounded *explicit role-channel intervention*, not a retrained model,
not replacement of all teammate context, and not a calibrated alternative
deployment candidate. Zero standardized coordinates would instead mean the
training-average shift and is the wrong intervention. Do not interpret its
delta as the full causal effect of moving teams. Compare it with full SHIFT
on identical cells; calibration remains fixed to isolate the pathway.

## Analysis

Report possession-weighted MAE/RMSE/r²/correlation/bias; raw sample size and
season breakdowns; all eight original forecasts and the two replay paths.
Cluster paired differences by destination team-season with2000 bootstrap draws,
fixed RNG20260917, and also show equal-season differences/t95 when supported.
Clusters are an approximation, not independent random assignment; years remain
historical development evidence. No arm/policy selection from this cohort.

Reuse existing prior-only80/95 finite-outcome intervals for the unchanged
forecasts, matched to the same cells. Do not invent latent-mean intervals or
give the intervened replay borrowed coverage claims. Report support distance
and seed/replay sensitivity without calling them posterior uncertainty.

Case library: every primary cell, plus equal-sized top10 benefit/harm lists for
new half minus additive; keep the full registry to prevent cherry-picking.
Include player names, movers/from/to, possessions/games, all forecasts, observed
ratings, additive player contributions and NN event forecasts. For all primary
cells, aggregate observed FGA/FTA/turnovers/shot mix and recovery counts using
the original target-specific missing-label masks. Preserve the broader point
population. Point-ledger contributions and expected scorer shares have different
interpretations; do not relabel either as pure chemistry.

Separate repeated-failure diagnostic on the whole primary v14 population:
>=200poss and>=5games per cell; group identical fives within season; require
>=2 eligible quarters and print all such units ranked by summed weighted
squared-error change. Both benefit and harm tails. This is exploratory and
cannot revise the transfer cohort. Cleveland2016 is an example, not a filter.

## Deliverables / stopping

One new benchmark prefix with manifest, metadata receipt, cohort before scores,
durable verbose log, all/matched counts, saved replay predictions and parity,
scorecards, cluster/season comparisons, finite-outcome coverage, event/case
library and both tails. Read-only inputs and reproducible commands. Bounded
saved-weight inference, no optimizer calls, source-cache rebuild or new training.
Report methods limitations alongside results. Update SESSION_HANDOFF and write
a review connecting the evidence to action-generation and opponent/defense
design. Stop this block once those outputs and checks are complete; a new
architectural experiment gets its own frozen plan and launch authorization.
