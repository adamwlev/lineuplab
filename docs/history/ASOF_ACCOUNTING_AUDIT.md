# Date-aware valuation and opportunity-accounting audit

## Protocol fixed before the diagnostic run (2026-09-05)

This is the next bounded step in `ASOF_MODEL_EXPERIMENT.md`, not a new accepted
point model. The three standards remain co-equal. The lead owns interpretation;
Opus implements the specified helpers and tests. No production promotion,
named-player correction, new bandwidth selection, or additive comparison here.

### Strict-date league environment

Aggregate per-game sufficient statistics from the existing possession context
and parsed outcomes. At each cutoff, fit the original nine-channel conditional
valuation plus intercept, using only games strictly before that date. Preserve
the original 1e-6 numerical ridge and six distance-bucket definitions so the
no-decay preseason environment can reproduce the old helper exactly. Also
report actual conversion percentages, full FGA/3PA/FTA/TO rates, known/unknown
shot-location exposure, and effective weighted possession exposure.

Compare historical-all-prior preseason, 365-day-weighted preseason, and the same
365-day-weighted environment refreshed quarterly. These are environment inputs,
not a completed historical-player-to-current-era transport model. Conditional
OLS coefficients, particularly ORB, are not causal event values. Actual
conversion probabilities must remain separate and bounded.

### Trace the reconstruction, do not insert an FTA correction

Reuse the completed quarter test's identical cells, outcomes, cached live
180/365-day profiles, and historical-frozen league usage budget. Recover each
player's strictly prior, identically weighted raw counts. Compare:

1. Current EB profile reconstruction (must reproduce cached predictions).
2. Direct raw count rates, with the same lineup usage normalization.
3. Four one-at-a-time substitutions of raw usage, turnover rate, FTA/FGA, or
   3PA rate into the current EB profile.
4. All four raw substitutions together, to audit the round trip separately
   from raw direct counts.

These are diagnostic ablations, not seven proposed shipping models. One-at-a-
time changes are not additive causal attributions. Raw FTA/FGA is undefined
when FGA is zero: retain the current ratio for that diagnostic substitution,
count and disclose those cases, and retain direct raw counts as the independent
reference. Report clipping, zero-usage cases, and any discrepancy between the
declared usage and reconstructed FGA + 0.44 FTA + TO. Do not silently fix an
incoherent hybrid or drop its cells. The 0.44 formula is a usage proxy, not an
exact possession identity; rebound continuation remains separately unresolved.

Reconcile matched player counts with full possession event counts by game and
in each weighted prefix. In particular, unassigned/team turnover events and
unknown shot locations must be visible rather than mistaken for model error.
No parser or source-cache changes are authorized by this audit.

### Evaluation and acceptance

Use the existing 2015 warmup and 2016–2026 quarter origins, >=50-possession
common cells. Report FGA, 3PA, FTA, TO, usage and the two shot-mix ratios,
with possession-weighted errors and season-paired differences plus SEM.
Ratio metrics use actual FGA exposure, as in the source experiment. Quarters
and recurring fives are not independent replicates. No inference that a lower
raw-count error alone establishes a better player-state estimator.

Must-pass tests: strict date/future identity invariance, weighted sufficient
statistics versus a direct possession fit, no-decay old-environment reproduction,
permutation invariance, count round-trip recovery for valid positive-FGA inputs,
explicit zero-FGA/clipping behavior, and exact reuse of the source common cells.
Only existing current-epoch caches may be read; missing/stale inputs must stop,
not trigger a rebuild. Output uses a new prefix and records provenance and
completion state. Start with one 2025 smoke, then one full audit if checks pass.

The next decision is whether the primary issue is reconstruction/shrinkage,
player-versus-possession attribution, league drift, or remaining role response.
Quarter point evaluation with prior-only calibration and an equally refreshed
additive control is still owed regardless of this audit's outcome.

## Completed readout — 2026-09-06

The smoke and full audits are complete; no jobs remain. The full run took
31 seconds. It reuses all **6,179** source cells including 2015 warmup, with
**5,607 cells / 726,364 possessions / 44 windows** in the 2016–2026 readout.
These are recurring window-lineup cells, not independent distinct fives.
Both profile bandwidths use exactly the same cells. The reconciliation covers
32,173 games present in the possession cache; none lack player-game rows.

The no-decay environment reproduces the original helper with maximum difference
**0.0** on the real prefix. Current channel reconstruction reproduces every
saved core forecast within **8.53e-14 per 100**. The accepted scorer, HTML,
source caches and database are unchanged. **192 tests pass.**

### Reconstruction/shrinkage is not the main FTA problem

For recent-180 live profiles, possession-weighted errors on the common cells:

| Target, per 100 possessions | Current EB MAE | Raw-count MAE | Raw minus EB, season mean ± SEM |
|---|---:|---:|---:|
| 3PA | 4.63049 | 4.64370 | +0.01360 ± 0.00184 |
| FTA | 6.36623 | 6.36931 | +0.00295 ± 0.00132 |
| Turnovers | 2.48309 | 2.49451 | +0.01143 ± 0.00133 |

Removing shrinkage worsens 3PA and turnover MAE in 11/11 seasons. FTA worsens
9/11. More importantly, FTA bias barely changes: **+3.35115 → +3.34771**.
Replacing only FTA/FGA also leaves the bias essentially intact (+3.34880).
The 365-day profile gives the same substantive conclusion: FTA bias
**+3.48531 → +3.48355**, with turnover MAE worsening 11/11. Retain shrinkage;
do not rebuild it as the proposed explanation for the broad FTA excess.

The current model's mean usage proxy is close: predicted **113.29488**, actual
**113.17126**. Its composition is not: FGA bias **−1.28580**, FTA **+3.35115**,
3PA **−2.08268**, TO **−0.06509**. The FGA/FTA/TO discrepancies satisfy the same
usage arithmetic. Another scalar budget adjustment cannot fix those shares.

Neither current EB nor direct raw counts violates the usage ledger in these
cells. The deliberately mixed raw-usage/EB-turnover diagnostic sometimes does;
those cases remain flagged, not repaired or removed. This says nothing about
synthetic extreme lineups, which were not the target of this audit.

### Event attribution is a real limitation, not the FTA explanation

At the 2025–26 fourth-quarter cutoff, in the recent-365 league prefix, full
possession events exceed matched player events by **0.105 FTA**, **0.880 FGA**,
**0.459 3PA**, **0.843 TO**, and **0.144 ORB** per 100. Offensive possession
exposures reconcile exactly. These gaps can include team/unassigned events;
the audit does not identify each cause. The FTA gap is small and has the wrong
direction to explain excess player-derived forecasts. Turnover attribution is
large enough to keep explicit in future mechanism work. No parser repair or
constant event correction is justified by these totals alone.

### Date-aware league conditions are now available

The legacy all-history preseason environment at the 2025–26 fourth-quarter
cutoff carries **28.36%** three-point attempt share and **62.38%** rim conversion.
The strictly prior, recent-365 live environment carries **40.77%** and **68.06%**.
The code also carries date-aware conditional valuation coefficients, separate
from these actual percentages, and records their conditioning and exposure.

This confirms meaningful league drift in the inputs. It does not establish a
point-score gain: creation valuation and the above-expectation making term
interact, and some changes can offset algebraically. No environment bandwidth
or updated point scorer has been selected.

### Post-hoc population clue (descriptive, not preregistered)

After the audit, `asof_population_readout.py` compared all possessions with the
common-cell subset within each identical quarter. Both populations are averaged
using common-cell exposure so their calendar weighting agrees:

- Full-league actual FTA: **22.58401 / 100**.
- Common-cell actual FTA: **20.35646 / 100**.
- Current recent-180 model on those cells: **23.70761 / 100**.

The full-minus-common FTA gap is positive in **11/11 seasons**, with a
season-mean difference **2.25496 ± 0.10548 SEM**. The pooled gap is 2.22755.
The subset also has more FGA (90.435 versus 89.383) and fewer TOs (13.779 versus
14.390); its 3PA rate is similar (32.994 versus 32.941).

This is a comparison of different lineup/game-context populations, NOT an
identified cause of the forecast error or a prospective league-mean forecast.
Future league outcomes are used only descriptively. Do not subtract this gap
from forecasts or claim it explains a particular percentage of the error.
It motivates examining deployment, foul/game-state mix and player exposure
before attributing the entire discrepancy to intrinsic player complementarity.
Neither late-game fouling nor any other specific mechanism is established here.

## Resume after this audit

**Follow-up complete:** read `ASOF_DEPLOYMENT_AUDIT.md` rather than repeat this
audit. Coarse state reweighting reduces the descriptive full/common FTA gap
from 2.228 to 1.037/100; common fives overrepresent Q1/Q3. This is not a causal
offset. `ASOF_OPPORTUNITY_EXPERIMENT.md` now completes the empirical joint-share
calibration control, with teammate-response and point comparisons still
separate. Latest full suite: 278 tests; all jobs finished.

1. Retain the EB states and existing controls; do not rerun the raw-ratio
   ablations seeking a cure for the FTA bias.
2. Separate current league environment from evaluation-population/deployment
   effects when designing a **joint FGA/FTA/TO share model**. Any correction or
   context-response coefficient must be estimated strictly before the cutoff.
   Test composition effects against a reference with comparable freshness and
   exposure, not against a global mean drawn from different game situations.
3. Integrate the available date-aware environments into the quarter point
   factorial, with prior-only calibration/bandwidth selection and an equally
   refreshed chemistry-free additive control. The evidence for league drift
   does not replace that comparison.
4. Role adaptation, two-team defense and OOD calibration remain separate work.
   All three product standards retain equal standing; no coverage gate returns.

### Implementation / review / reproduction

Opus implemented the two audit modules and their tests under a bounded contract.
It hit its turn limit without a final handoff. Lead review found and repaired
a raw-prefix cache keyed only by half-life (which would freeze raw counts after
quarter one), fractional-weight FT conversion, and missing-player aggregate
reconciliation. Added an end-to-end two-cutoff test, a non-vacuous future-row
mutation test, conversion checks, input protocol/date checks, and exact final
cell-set verification **before reporting real-data results**. The raw-prefix
bug did not enter either completed audit. The secondary population readout and
its tests were written by the lead. No worker outside-scope edits were detected.

Completed outputs: `experiments/cache/asof_accounting_2026_*`; the
`_population_*` files are explicitly post-hoc and have a separate provenance
manifest. The separate `asof_accounting_smoke_*` run is only a 2025 smoke,
not additional evidence. Original source results remain intact. Commands:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.asof_accounting_audit
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.asof_population_readout
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest discover -s tests
```

The audit/readout refuse existing output prefixes; do not rerun completed work
without a reason and a new prefix. Logs: `/tmp/basketball-asof-accounting.log`,
`/tmp/basketball-asof-accounting-smoke.log`,
`/tmp/basketball-asof-accounting-full-tests.log`. Worker review artifacts:
`/var/folders/0q/vr0lp8p56s7ddsz7k2d30j100000gn/T/opus-worker-501/run-8ym6l3x7`.
