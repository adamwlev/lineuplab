# Team-change benchmark and repeated failures — September 17, 2026

## Outcome

The first bounded post-v14 work block is complete: a systematic team-change
cohort, saved-weight role-channel intervention, substantial-lineup case library,
and event-accounting audit. No models were trained or promoted.

**The contextual models help on substantial first-quarter team-change lineups,
but the explicit SHIFT architecture is not the winner there.** Its role-shift
channel contributes only a small, uncertain increment. A clearer next lead is
systematic overprediction of free-throw volume in substantial lineups, including
both transfers and recurring failure cases. This is an allocation diagnosis,
not permission to subtract a post-hoc FTA correction.

The preceding v14 review/source checkpoint was committed as **f7e89aa** before
this new work. This block's source/docs and derived outputs are separate.

## What was frozen and what was measured

`TRANSFER_ROLE_BENCHMARK.md` was written before inspecting cohort scores.
This is retrospective development on the same historical seasons, not untouched
confirmation or causal trade evaluation. All three product standards remain
co-equal. The experiment makes no new extreme-lineup or latent-OOD claim.

The local database supplied16,798 game identity/date/home/away records in a
read-only repeatable-read transaction; no scores were queried. Original
possession context supplied356,213 player/game/team memberships. No ambiguous
same-game membership or unmatched grouped/cell mappings occurred. Charlotte's
name change was normalized; original caches and DB contents were not changed.

An eligible move is an observed change from the last offensive appearance in
the preceding season to the first in the new season, with >=10 prior games and
>=300 prior offensive possessions, occurring within the destination's first10
games and q1. These are **observed team changes**, not verified transactions:
free agents and some early-season moves can be included. Eventual appearances
and exposure label the retrospective cohort; they never update the preseason
model states, normalizers, weights or calibration.

There are1,175 observed changes, of which1,030 meet the fixed support/timing
rules. The registry includes eligible players without any scored lineup.

| Exposure slice | Cells | Possessions | Movers with cells | Team-seasons |
| --- | ---: | ---: | ---: | ---: |
| All available matched cells | 959 | 117,070 | 576 | 245 |
| >=100poss and5games | 337 | 73,405 | 342 | 187 |
| **Primary: >=200poss and5games** | **146** | **47,419** | **197** | **123** |
| >=500poss and5games | 12 | 7,301 | 20 | 12 |
| Primary, >=2movers | 67 | 23,489 | 130 | 57 |

All but the500poss slice span11 seasons; that slice spans8. Each lineup is
counted once, even if several movers appear. The primary population contains
only197 of1,030 eligible moves; healthy, retained, stable rotations are strongly
selected. This does not forecast whether a new lineup will receive minutes.
The rules even exclude a famous case: Kawhi's2019 move has416 preceding-season
offensive possessions but only9 games. We did not relax the cutoff after seeing
that; Toronto lineups can still qualify through Danny Green.

Quarter definitions and historical playoff coverage follow the existing
schedule. Outcomes are lineup-window offensive ratings, not single possessions.
The lower RMSE than the full v14 scorecard reflects larger-exposure cells and
a different population; it is not a sudden improvement from10.8 to6.6.

## Accuracy on the primary cohort

All original neural forecasts are the completed, separately calibrated
three-seed ensembles. Nothing was refit for this cohort.

| Forecast | MAE | RMSE | r² |
| --- | ---: | ---: | ---: |
| Additive | 5.07365 | 6.85781 | .16373 |
| Old V9 HALF | 4.92049 | 6.68694 | .20488 |
| ROLE_SL direct | 4.89265 | **6.58670** | **.22854** |
| ROLE_SL half | **4.86800** | 6.63805 | .21647 |
| RB_RENEW_FAC direct | 4.93162 | 6.59685 | .22616 |
| RB_RENEW_FAC half | 4.87890 | 6.64233 | .21545 |
| RB_RENEW_FAC_SHIFT direct | 4.97263 | 6.68083 | .20633 |
| RB_RENEW_FAC_SHIFT half | 4.91508 | 6.68329 | .20575 |
| Same SHIFT weights, zero-shift channel direct | 4.98904 | 6.70743 | .20000 |
| Same SHIFT weights, zero-shift channel half | 4.92719 | 6.69235 | .20359 |

ROLE_SL half minus additive has pooled ΔRMSE−.21976, destination-team-season
cluster bootstrap95% interval[−.36205,−.08653]. Equal-season mean−.19834,
t95[−.36773,−.02896],9/11 favorable seasons. Renewal half is similar:
pooled−.21547, cluster interval[−.36323,−.07029],10/11 favorable seasons.

ROLE_SL direct has the lowest pooled RMSE, but its equal-season interval versus
additive crosses zero. The cluster and season analyses summarize different
variation; neither is a causal design or fresh confirmatory evidence.

The combined SHIFT half is effectively tied with old HALF:
ΔRMSE−.00366, cluster interval[−.14283,+.14285]. It is not the new preferred
transfer architecture just because it led the full-population leaderboard.

### Sensitivity to the exposure threshold matters

On **all available cells**, old HALF is best among these saved forecasts:
RMSE10.90785 versus ROLE_SL half10.92121, renewal half10.92238, combined
half10.93178 and additive11.00330. At>=100poss, old HALF8.33533 also beats
the new half forecasts8.34737/8.35637/8.36525. At>=500poss the combined
neural model leads, but there are only12 cells. The two-or-more-mover primary
slice also favors old HALF6.56621 over the new forecasts.

Thus the contextual-vs-additive bright spot is genuine on this prescribed
substantial cohort, but the ranking of contextual variants is population-
dependent. Do not tune a blend weight or gating policy on these results.

## What the role intervention actually identifies

For RB_RENEW_FAC_SHIFT, all five players' last four role-head inputs were set
to **raw context change zero**, standardized with the saved training mean/scale.
This differs from setting standardized coordinates to zero. Player capability,
recent-role inputs, proposed-team main messages, recovery inputs, weights and
calibration stayed fixed. No optimizer was instantiated.

Unchanged replay matches all saved selected raw predictions to1.43e-14pts100
across the11 q1 origins and three seeds. Full SHIFT versus zero-shift gives
direct ΔRMSE−.02660 with cluster interval[−.17832,+.13791]; half−.00906 with
interval[−.08790,+.07564]. Direction is mildly favorable, evidence is weak.

This is a test of the **explicit role-change channel**. It does not freeze all
teammate context or demonstrate how a coach would assign responsibilities.
The general NN advantage cannot be attributed entirely to this channel.

## Basketball cases and event accounting

Every primary cell is preserved in the case library, with movers/from/to,
games/exposure, all forecasts, additive player contributions, neural counts,
and both top10 benefit/harm tails. Examples are selected by the fixed error
ranking, not by fame:

- Detroit2016q1, Ilyasova/Jackson/Morris/Drummond/Caldwell-Pope:811poss,
  actual107.27, additive112.45, combined half109.69.
- Golden State2017q1, Pachulia/Durant/Curry/Thompson/Green:465poss,
  actual115.91, additive113.13, combined half116.32.
- Utah2023q1, Conley/Olynyk/Clarkson/Markkanen/Vanderbilt:335poss,
  actual114.93, additive115.03, combined half117.15—a harm case.
- Cleveland2024q1, Allen/Mitchell/Garland/Strus/Mobley:302poss,
  actual111.92, additive117.45, combined half119.31—another harm case.

The full-population repeated-case library contains183 identical-five/season
units with >=2 substantial quarters. Cleveland2016 is the largest summed
weighted squared-error harm for the new half versus additive; Detroit2016 and
Denver2024 are among the largest improvements. Rankings are descriptive and
exposure-weighted, not independent proof of persistent talent misvaluation.

### The FTA problem is observable on real lineups

Using each target's own valid-label support in the primary transfer cohort:

| Event /100 | Observed | Combined NN | Valid possessions |
| --- | ---: | ---: | ---: |
| FGA | 89.965 | 88.665 | 39,681 |
| FTA | **18.705** | **23.202** | **46,848** |
| Turnovers | 13.775 | 13.376 | 47,419 |

ROLE_SL and renewal also predict23.180 and23.144FTA/100, respectively.
This is not peculiar to SHIFT. It is a substantial-lineup conditional error;
the campaign's all-game/group aggregate FTA bias was much smaller. Exposure,
rotation, late-game/intentional-foul situations, opponents and event measurement
are possible explanations to separate before prescribing a structural fix.

We then decomposed event errors on rows with jointly complete FG/location/FT
labels. The union of transfer and repeated libraries has529 distinct cells;
526 have any joint-complete rows, giving1,578 arm/cell decompositions. The
three missing cells remain in point metrics. Transfer joint-complete support
is39,500 possessions over145 of146 cells. Fixed-order accounting is:
FG volume → shot-location mix → within-bin conversion, then FT volume → FT
accuracy, followed by observed-label gap and point calibration. Empty observed
shot bins use the model rate as an explicit decomposition convention. This is
an identity, not causal attribution or an estimate of recoverable improvement.

For the combined model, transfer errors include **+3.54pts100 from FT volume**,
partly canceled by−1.35 from FG volume and−1.73 from within-bin conversion.
Repeated cells show the same broad pattern (+3.07 FT volume,−1.80 FG volume,
−1.95 conversion). FT *accuracy* contributes little to mean error. Within-bin
conversion has the largest average absolute component (~5.2pts100), but it
contains shooting noise and shooter-selection differences, not just missing
shot-quality skill. Do not claim all5.2points can be learned away.

For Cleveland2016 across its three substantial quarters (1,564 possessions;
1,332 joint-complete), the combined direct error on the complete subset is
−6.64pts100. Components:

| Component | Model minus observed, pts100 |
| --- | ---: |
| FG volume | −6.22 |
| Shot-location mix | −.65 |
| Within-bin conversion | −3.73 |
| FT volume | +3.74 |
| FT accuracy | +1.40 |
| Point calibration | −1.19 |

The observed event ledger matches recorded points within9.2e-6pts100 across
the diagnostic cells. Missing-label populations are disclosed rather than
discarded from the headline point comparison. There is no single common
failure direction:2024 Cleveland overpredicts conversion/FTA, while2026 Toronto
underpredicts conversion. A generic “give stars more credit” adjustment would
not address both and is not proposed.

## Uncertainty / third product standard

Unchanged prior-only intervals on these146 cells: ROLE_SL half80/95 coverage
79.45%/95.21%; combined half80.82%/93.84%; additive78.08%/93.84%.
These are finite-game outcome intervals on selected real lineups. No intervals
were borrowed for the intervened replay, and no latent-quality claim is made.
The former v14 five-center failure still applies; this cohort does not override
it. Neither a transfer result nor a good aggregate interval is product acceptance.

## Next implementation priority

Keep the original three research candidates and these frozen benchmarks. The
evidence argues against spending the next run solely on a larger role head.

Before an architectural sweep, make the next bounded diagnostic distinguish:

1. **Action/FTA allocation:** compare large versus small exposure units and
   game situations; investigate initial rates versus normalization and creator
   constraints. Any revised allocator must preserve the opportunity ledger and
   redistribute attempts/turnovers coherently, not subtract a fitted4.5FTA from
   the observed cohort. Keep full-population accuracy, transfer cells, center
   probes and uncertainty together in the acceptance table.
2. **Actual defense/opponents:** map offensive groups to opposing personnel
   using the already available possession context. A future fit needs matchup-
   keyed grouping (not falsely one opposing five per offensive game group),
   strict dated defensive profiles and an opponent-aware additive control.
   Begin with a simple opponent main effect before cross-team interactions;
   otherwise attribution of a richer neural architecture's gain is ambiguous.
   Preserve offensive-lineup aggregation as a common reporting view and share
   the directional scorer so swapping teams negates predicted margin.
3. **First/second-chance offense and uncertainty:** keep stationary renewal as
   the control for a separate phase decoder; distinguish latent support error
   from finite-game noise. These remain separate design questions, not silent
   additions to a response to this cohort.

No new training was required here. An actual next fit needs its own frozen
design; no architecture, loss, stopping policy or production scorer was changed.

## Reproduction and handoff

Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u` with fresh output
paths (completed prefixes must not be overwritten):

```sh
python -u -m experiments.transfer_role_benchmark extract --output-dir NEW_METADATA
python -u -m experiments.transfer_role_benchmark run --metadata-dir NEW_METADATA --output-dir NEW_BENCHMARK
python -u -m experiments.transfer_failure_diagnostics --benchmark-dir NEW_BENCHMARK --output-dir NEW_DIAGNOSTICS
```

Only the first command accesses the DB, read-only. Subsequent stages use
`no_database()`. Existing metadata may be reused by passing its path instead.
Durable logs, provenance and CSVs:

- `experiments/cache/transfer_role_2026_09_17_metadata`
- `experiments/cache/transfer_role_2026_09_17_v1`
- `experiments/cache/transfer_failure_2026_09_17_v2`

The first failure diagnostic prefix is preserved. Its overly strict identity
check exposed float32 arithmetic in the diagnostic, not a model error. Promoting
the decomposition inputs to float64 preserves the formula and passes the original
1e-8 tolerance; source forecasts/labels were unchanged. Six focused tests pass,
including raw-zero versus standardized-zero, cohort timing/support boundaries,
cluster resampling and float32/empty-bin accounting. All33 unchanged replay
checks and all final event ledgers pass. Original90 v14 producer hashes remain
unchanged. No scraping, mutation, fit, promotion, delegation or deployment.
