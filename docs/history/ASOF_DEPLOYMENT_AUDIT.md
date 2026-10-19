# Deployment-population check

## Protocol fixed before the new readout — 2026-09-06

This is a bounded follow-up to `ASOF_ACCOUNTING_AUDIT.md`, not a new fitted
model. The full-league versus common-lineup FTA gap is already known. The new
question is whether coarse game-state mix accounts for much of that descriptive
gap, or whether it remains within comparable situations. This helps define the
reference for a joint FGA/FTA/TO model; it does not identify player synergy.

Reuse exactly the completed audit's 2016–2026 quarter windows and common cells.
Do not remove invalid-duration possessions, change the >=50-possession rule,
refit profiles, scrape, mutate the database, or rebuild caches. Read current
cached context/outcomes and the saved audit only. Reconstruct every common
cell's exposure and FGA/3PA/FTA/TO targets before accepting the results.

Partition each window's offensive lineup possessions into three exclusive
groups: below 50 possessions, >=50 but not in the saved common population,
and common. Also report the full and all->=50 populations. These are evaluation
selection categories, NOT a product coverage gate or a proposed exclusion.

### Fixed game-state description

Use the score **before** the possession, reconstructed from the full game,
from the offense's perspective. Sort by game, quarter, descending start clock,
then possession id for deterministic tied-clock order. State is quarter 1/2/3/4
or overtime, crossed with >120 versus <=120 seconds remaining in that period,
crossed with offensive margin <=-10, -9..-4, -3..3, 4..9, or >=10. Invalid
quarter/clock/margin goes into a disclosed unknown stratum, never dropped.
Regulation clock must be in [0,720], overtime in [0,300]. Report tied clocks
and invalid-duration exposure as data-quality flags. Reconstructed margin is
not an independently verified scoreboard, and these bins do not measure the
bonus, foul intent, matchups, or substitution decisions.

For each window and event, let full-league state rates be r_F(s), and full and
common state weights be w_F(s), w_C(s). Compute:

- Full rate: sum w_F(s) r_F(s).
- State-reweighted full rate: sum w_C(s) r_F(s).
- Common rate: its actual observed rate.
- Mix component: full minus state-reweighted full.
- Within-state remainder: state-reweighted full minus common.

The two components must add exactly to the observed population gap. Full
contains common, so every state with common exposure must have full support;
an absent common state contributes zero weight, not an imputed rate. This
reference-specific arithmetic decomposition is descriptive, NOT a causal
explanation or forecast. Never subtract either component from model predictions.
Aggregate all window comparisons using common-cell possession weights; report
season-paired means and SEM, treating seasons rather than quarters as replicates.

Report late regulation/overtime (<=120 seconds) exposure and event contribution.
Also report rows with FTA>0, FGA=0, TO=0 as an **outcome-defined diagnostic**,
without labeling them intentional fouls or using them as predictors. No filter
or bin is selected in response to the readout.

### Acceptance and next decision

Tests must cover pre-possession scoring, game reset, offense perspective,
ties, row and lineup-slot permutation, boundary/unknown bins, empty strata,
exact gap decomposition, exclusive-group accounting, saved-cell reproduction,
and missing/duplicate/mismatched inputs. Use a new output prefix, record source
and code provenance, refuse overwrites, and mark complete only after all checks.
Run synthetic tests first, then one full descriptive readout; this is not an
expensive sweep. Keep all prior results intact.

Regardless of the result, retain EB and the original matched evaluation cohort.
A sizable mix component would require an explicit deployment reference in the
next opportunity model. A sizable within-state remainder means coarse clock
and score alone are insufficient; do not equate that remainder with synergy.
The next predictive test should compare strictly prior joint-share calibration
against a composition-response extension, with identical usage budget, profile
freshness, and calibration population. The quarter point factorial and equally
fresh chemistry-free additive comparison remain owed. No scorer, HTML, or OOD
claim changes here; all three product standards remain co-equal.

## Completed readout — 2026-09-06

The single full readout completed in **11.37 seconds**. All **5,607 common
window-lineup cells / 726,364 possessions / 44 windows** reproduce: maximum
exposure difference **0**, maximum event-rate difference **1.42e-14/100**.
The full population remains **2,760,546** possessions. No windows were skipped,
no games lacked a season mapping, and no source data or scorer changed.
An independent comparison against the previous population CSV also reproduces
its full/common rates and exposures. **245 tests pass; no jobs remain running.**

### A substantial state-mix component, and a substantial remainder

All columns below use the same common-cell possession weights across windows.
These are population descriptions, not forecasts.

| Event /100 | Full league | Full league reweighted to common state mix | Common cells |
|---|---:|---:|---:|
| FGA | 89.38325 | 89.61487 | 90.43496 |
| 3PA | 32.94063 | 32.72169 | 32.99379 |
| FTA | **22.58401** | **21.39392** | **20.35646** |
| TO | 14.39045 | 14.30698 | 13.77946 |

The pooled FTA gap **2.22755** decomposes into **1.19009** from different state
weights and **1.03746** remaining within the chosen bins. Season means ± SEM
are **1.18432 ± 0.05918** for the mix component and **1.07064 ± 0.10061** for
the remainder; both are positive **11/11 seasons**. Thus the fixed coarse
state reweighting reduces slightly more than half of the descriptive population
gap. This is NOT the fraction of the model's +3.35 FTA error causally explained.

The sample is strongly tilted toward first/third-quarter possessions:
**65.27% common versus 50.13% full league**. The first ten minutes of those
quarters alone comprise **61.47% versus 41.81%**. The common fives do not
experience the same rotation/time distribution as a whole-game player profile.
These figures describe deployment; they do not establish which players or
coaching choices caused it.

### Selection at the possession threshold matters

| Population | Possessions | FTA/100, common-calendar weighting |
|---|---:|---:|
| Below 50 possessions per window-lineup | 1,746,547 | **24.05399** |
| All qualifying >=50 units | 1,013,999 | **20.10117** |
| Common evaluation cells | 726,364 | **20.35646** |
| Qualifying but not common | 287,635 | **19.41474** |

The large FTA difference is already present at the sample-size threshold;
requiring the shared player-profile coverage does not create it from scratch.
Do not remove the threshold in the existing primary comparison or mistake
these data-selection categories for a product coverage gate.

Final-two-minute regulation/overtime exposure is **4.993% full versus 3.771%
common**, carrying **2.046 versus 1.699 FTA per 100 total possessions**.
FT-only rows (FTA>0, FGA=0, TO=0) comprise **8.640% versus 7.798%** of exposure
and carry **17.482 versus 15.775 FTA/100 total**. These are outcome descriptions,
NOT labels for intentional fouling. A post-hoc sensitivity computed from the
saved state table, excluding the final two minutes of regulation/OT, gives
**21.618 versus 19.390 FTA/100**: the population gap remains. This sensitivity
does not replace the primary all-possession readout and did not alter any fit.

### Data and interpretation limits

There are **83,825 invalid-duration** and **40,994 tied-start-clock** full-league
rows in the evaluated windows; common cells contain **22,084** and **9,255**.
All remain included. No row has an unknown state in the real run. Margins are
reconstructed from ordinary-possession points, not independently verified full
scoreboards (technical points are not in that ledger). Tied clocks use the
fixed possession-id order.

Read-only source inspection also confirms that both `scrape_br.ipynb` and
`experiments/bref_ingest.py` generally record the five present at possession
completion. Substitutions can occur during a free-throw trip; the newer parser
has a specific scoring-lineup fallback when its scorer has left. This is a
real schema/attribution limitation, **not an established explanation of the
measured gap**. No parser, scrape, database or cache change is justified here.

### Decision and next bounded work

Retain EB, the original evaluation cells and all three standards. Do not add
an FTA penalty and call its broad calibration gain complementarity. First
establish a **strictly prior joint opportunity-share calibration control** on
the same recurring-lineup population; any composition-response extension must
beat that control, not merely the uncalibrated profile average. Historical
training cells may be used only after their full window has ended. Future
clock/score distributions and the offsets above must not enter forecasts.

**Follow-up completed:** `ASOF_OPPORTUNITY_EXPERIMENT.md` now records the
prior-only baseline run: FTA/3PA MAE improve 11/11, with a small TO loss.
This calibration cannot by itself supply a
neutral-game counterfactual or solve arbitrary-lineup means/uncertainty. The
date-aware point factorial with an equally refreshed chemistry-free additive
comparator remains owed; do not claim an intermediate gain settles it.

### Review and reproduction

Opus completed only the two authorized code/test files (47 synthetic tests),
without permission denials or git changes. Lead inspection repaired primitive
count validation (NaN/negative buckets could disappear in sums), added source
hash/window/date checks and pre-score validation, and made per-state mix and
remainder contributions sum correctly even when a state has no common exposure.
Six additional regression tests bring this module to 53 tests and the whole
suite to 245. Changes were verified before the real readout.

Outputs: `experiments/cache/asof_deployment_2026_{states,populations,windows,
seasons,paired,manifest}` (CSV tables and JSON manifest). In `_states.csv`,
`mix_contribution_*`, `remainder_contribution_*`, and `common_weight` are defined
on **full-population rows only**; sum those rows to reconstruct each window's
decomposition. Other populations' blanks in those columns are intentional.

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.asof_deployment_audit
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest discover -s tests
```

The completed output prefix refuses overwrite; do not repeat the run without
a reason. Logs: `/tmp/basketball-asof-deployment.log`,
`/tmp/basketball-asof-deployment-tests.log`. Worker audit:
`/var/folders/0q/vr0lp8p56s7ddsz7k2d30j100000gn/T/opus-worker-501/run-65b5z02n`.
