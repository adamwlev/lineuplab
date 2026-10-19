# Quarter-origin additive tuning — 2026-09-07

## Protocol specified before running

Build on `ASOF_ADDITIVE_FOUNDATION.md`. This is a chemistry-free comparator,
not a change to the three co-equal product standards or the accepted scorer.
The next bounded deliverable is a tested selector plus **one 2026 Q3 pilot**,
with a 300-second runtime cap. No 44-origin sweep is authorized by this pilot.

### Match the validation horizon

For target season T, quarter q, take its already-defined causal window start.
Choose the most recent **completed earlier-season window with the same q**.
Its stop must be <= the target start. Fit the inner model strictly before that
earlier window's start, select on that window's raw possession outcomes, then
refit all available history strictly before the target start. Never use the
target window's outcomes for selection, normalization, calibration or tuning.
Use the existing 300/600/900-game window schedule, not future quantiles.

This matches both season-transition status and approximate within-season
evidence: Q1 validates previous-season carry into a new season; Q2/Q3/Q4
validate a current-season delta at roughly the same accumulation of games.
The deliberately simple tradeoff is annual rather than latest-quarter
hyperparameter refresh. Model coefficients and the cumulative profile prior
still ingest all newly available games. This is a research control protocol,
not a claimed optimal updating schedule. No automatic other-quarter fallback.

Use all possessions in the selected validation window, matching the annual
additive fitting criterion; do not select its population using future
common-lineup coverage. Report unsupported-player counts. Keep normal fitting
weights uniform and the existing cumulative EB box/height/position prior.
Profile recency/era weighting is a separate later decision.

### Objective, carry and level

For each career/prior/experience/season penalty combination, get the inner
model's base b and latest-season delta d. Select rho analytically on [0,1]
to minimize mean `(raw_points - prior_side_baseline - b - rho*d)^2` over the
validation window. A zero carry design selects rho=0. The side baseline is
the inner prefix's last observed season raw side mean, never the validation
window's mean. Refit with the chosen penalties and retain its chosen rho;
save base, carry and prior baseline separately for later comparison/calibration.
There is no additional point-score calibration or opponent-adjusted target
in this pilot. No test-window metric or named-lineup ranking will be printed.

### Penalty boundaries are part of the protocol

Start with `matched_additive.DEFAULT_GRIDS`. Evaluate the initial Cartesian
grid, and two successively wider grids: on **every finite axis**, add the old
minimum /10 and maximum *10 each round. Preserve BIG as an explicit disabled
corner, not a finite upper boundary. These grids are fixed before looking at
results; computing the union once and classifying candidates by earliest grid
round is algebraically equivalent and avoids repeated factorizations.

Choose each round's winner by MSE, then (exact ties) stronger delta, prior,
experience, career penalties, matching the annual convention. Save all candidate
losses/rhos and all three winners, finite boundary flags, and exact validation
prediction RMS differences between adjacent winners. Call the default two-round
audit stable only when **both** adjacent changes are <=0.001 pts/100 and the
final winner is not on a finite boundary. The threshold is an explicit
numerical-control diagnostic, not an accuracy or OOD standard. Failure is
reported as provisional, not silently repaired or promoted. A later expansion
can be designed using prior validation data only; no held-out test peeking.

Restrict quadratic calculations to active validation columns without changing
their meaning. Release spectral preparations after each delta to bound memory.
Keep candidate and boundary audit output distinct from outer-test predictions.

## Pilot scope and provenance

**Pre-pilot input clarification:** the first full-prefix timing attempt stopped
on player 1499 (John Holland): the cached index says 2018, while four prior
possessions are dated 2016-04-19. His 2016 playoff appearance is confirmed by
the [Cavaliers' official media guide](https://ak-static-int.nba.com/wp-content/uploads/sites/3/2017/09/Cavaliers-Preseason-2017.pdf),
printed p.21. The existing bio builder interpreted the index's `year_min` as
an unrestricted NBA debut; that assumption does not cover this case.

For this pilot, use the explicit **prior_observed** debut-reconciliation policy:
if a valid supplied debut year is later than an already-observed prior season,
use that player's earliest prior possession season and record the supplied,
observed and used years in the fit metadata. Do this independently at each
prefix, with no player-name exception and no future appearance used. The
foundation's default stays **strict** (raise on conflict), preserving existing
callers. No source bio row or possession record is changed. This repairs a
metadata-definition mismatch, not a learned basketball mechanism.

Read the existing epoch-matched context, player-game and quarter-window
artifacts explicitly; missing/stale files cause an error, never a rebuild.
Read roster id/height/position once in a **read-only** DB transaction and pin
that table in the pilot output. Read debut from the existing bio CSV. Do not
reuse the incomplete ratings export as the roster source. Static metadata is
not historically versioned; preserve that limitation in the manifest.

Write new `asof_additive_pilot_2026q3_*` research artifacts only: manifest,
candidates, boundary audit, pinned roster and final coefficient snapshot.
Refuse to overwrite existing outputs. Hash input/code dependencies; record
date plan, selected penalties/rho, validation support, population counts,
timings, runtime cap, data epoch and audit status. A timeout/error leaves an
explicit incomplete manifest and any completed candidates, not a completed fit.
The final snapshot contains player map, references, coefficients, carry and
baseline—not the full source frames or bulky fitting systems.

No scraper, source-cache rebuild, source DB mutation, scorer/page promotion,
bandwidth selection, scientific point-gain claim or full benchmark run.

## Acceptance checks

- Date-plan selection depends only on completed matching-quarter windows;
  later outcomes/windows and future identities cannot move earlier selection.
- Reject missing matches, invalid dates, incomplete intervals and mismatched
  carry-season status; no automatic horizon substitution.
- Candidate quadratic losses/rhos agree with direct row predictions on a
  synthetic real-profile fixture. Selected values refit at the outer cutoff,
  not the older inner cutoff. Advancing observed data changes the refit.
- Exact ties, BIG corners, active-column reduction, grid-round nesting and
  boundary diagnostics have deterministic tests, including an unresolved edge.
- Legacy helpers remain unchanged. Full unit suite passes. Pilot completion
  does not imply that tuning boundaries passed or that the scorer improved.

## Completed pilot and interpretation

The **2026 Q3 pilot completed in 253.7 seconds** under the 300-second cap.
All 5,760 distinct candidates and the outer coefficient snapshot are saved.
The implementation is verified; the tuning audit is **provisional**, not stable.
No target-window outcome was scored and no additive/structural contrast was run.

Date/population accounting:

- Inner fit: strictly before **2025-01-17**, 30,133 games / 5,658,437
  possessions / 2,388 players. Validation: **2025-01-17 through 2025-03-02**,
  58,999 possessions; 57,823 fully supported and 1,176 contain an unseen player.
  These unsupported rows remain in selection, with unknown-player terms zero.
- Outer refit: strictly before **2026-01-15**, 31,454 games / 5,918,458
  possessions / 2,481 players. It retains all 119,750 observed 2025–26
  possessions, not just completed seasons.
- Both prefixes independently reconcile the single Holland debut conflict
  described above. No other conflict appears; no source metadata changed.
- Stages: inner prefix 26.1s, validation 0.3s, search 176.4s, outer refit 49.8s.
  The pinned roster has 2,545 players. Snapshot size is about 445 KiB.

The career, experience and season-delta penalties stay at **10,000** in all
three rounds. The prior-coefficient penalty keeps moving to its finite lower
edge, **100 → 10 → 1**. Carry rho is **1** throughout. This means the bounded
validation choice retains the current-season delta; it does not establish an
optimal recency policy or a general basketball result.

| Grid round | Candidates available | Prior penalty | Validation MSE | Prediction RMS change, pts/100 |
|---|---:|---:|---:|---:|
| 0 | 480 | 100 | 1.419088 | — |
| 1 | 2,016 | 10 | 1.419085 | 0.042593 |
| 2 | 5,760 | 1 | 1.419085 | 0.004438 |

The residual changes are small in basketball units, but neither the finite
edge nor the predeclared 0.001 numerical threshold may be silently waived.
Do not call the selector converged or treat this validation MSE as held-out
model performance. Keep the complete pilot artifacts unchanged.

### Next bounded check (specified after the pilot, before that check)

Do **not** repeat the Cartesian grid or launch the 44-origin benchmark yet.
Reconstruct the same inner prefix and the same prior validation window, hold
career/experience/delta at 10,000, and evaluate prior penalties
**[1, 0.1, 0.01, 0.001]** with the same analytical rho selection. One spectral
preparation is sufficient. Cap the whole diagnostic at **90 seconds**, record
partial/incomplete status if exceeded, and use a new append-only result prefix.
No outer refit, target-window metric or additional axis search is needed.

Report validation prediction RMS changes both sequentially and relative to
the saved prior=1 candidate; first reproduce that candidate's loss/rho. The
question is whether the remaining edge materially affects the selected
predictions, not whether a further decimal of validation loss can be won.
If every alternative differs from the saved candidate by <=0.001 pts/100,
record the edge as numerically immaterial **for this one-axis sensitivity**
and retain prior=1; leave the original full-grid stable/provisional flags intact.
Otherwise record it as unresolved and decide the next step explicitly. This
does not certify a global optimum or justify ignoring other origins' edges.

Then settle the structural player/location opportunity accounting and shared
league/calibration controls for the quarter point comparison. The point
factorial, matchup defense and latent/OOD uncertainty remain unfinished.

## Implementation review and reproducibility

### Completed one-axis follow-up — 2026-09-07

The pre-specified follow-up completed in **53.5 seconds / 90-second cap**.
The saved prior=1 validation MSE reproduced exactly, **1.4190846920202858**,
and rho remained 1 for all four candidates. Relative-to-reference prediction
RMS changes were approximately **0.000446, 0.000490, 0.000495 pts/100** for
prior penalties 0.1, 0.01, 0.001. All are below the declared 0.001 threshold.

**Decision: retain prior=1; this one-axis edge is numerically immaterial at
this origin.** The original full-grid stable=False/provisional=True flags
remain untouched. This is not a global-optimum certificate, an automatic pass
for other origins or a target-window predictive result. The numerical
follow-up is complete; do not repeat it.

The same 58,999 validation possessions and 1,176 unsupported rows are retained.
Input/source/code hashes, saved candidate and artifact hashes independently
verify. Results: `experiments/cache/asof_additive_boundary_2026q3_{manifest.json,candidates.csv}`.
The new module is `experiments/asof_additive_boundary.py`. **425 tests pass**,
including 38 new boundary tests. Opus changed exactly the two contracted files
and hit its turn limit; lead review corrected two synthetic fixtures whose
assumed negligible movement was actually above threshold, without changing the
protocol, and added a zero-response check on the actual ladder. Source inputs,
the original pilot, scorer and page remain unchanged. No jobs are running.

Private audit: `run-8suwm5so` under the worker audit parent below; no permission
denials or git mutations. Logs: `/private/tmp/basketball-prior-edge-full-tests.log`
and `/private/tmp/basketball-asof-additive-boundary-2026q3.log`.

Code: `experiments/asof_additive_tuning.py`, `asof_additive_pilot.py`, and the
opt-in debut policy in `asof_additive.py`; tests in `tests/test_asof_additive*.py`.
**387 tests pass**, including 109 focused date-additive/tuning tests. The
synthetic tests compare candidate quadratic losses with direct predictions,
reject inconsistent handcrafted plans/non-PSD validation statistics, preserve
future-data invariance, and verify grid nesting and honest provisional status.
Pilot tests cover stale/missing inputs, duplicate bio IDs, source mutation,
atomic output reservation, signal/timer restoration and incomplete manifests
for loading, candidate-write and final-snapshot failures.

Opus implemented the bounded task and correction. The correction hit its turn
limit with saved edits; the lead completed missing wrapper safeguards/tests
and independently verified both code and outputs. The written worker handoff
was not used as proof of correctness. No worker is still running.

Artifacts: `experiments/cache/asof_additive_pilot_2026q3_{manifest.json,candidates.csv,boundary.csv,roster.csv,snapshot.pkl}`.
Epoch: `1788577025507373000-37f71aa800a1`. The manifest pins input/code hashes,
source stats captured before reads, roster hash, complete date plan and both
prefix populations. Independent read-only review reproduced all three winners
from the candidate table and verified artifact/code hashes and snapshot dates,
dimensions and finite coefficients. No scorer, page, database or source cache
changed; no existing result was overwritten.

Private verification artifacts (not for publication):

- Contracts: `/private/tmp/basketball-opus-quarter-tuning-contract.md` and
  `/private/tmp/basketball-opus-quarter-tuning-corrections.md`.
- Worker audits under `/var/folders/0q/vr0lp8p56s7ddsz7k2d30j100000gn/T/opus-worker-501/`:
  `run-vzay1q_r` (three allowed files, exit zero) and `run-lkwg2cx2` (five allowed
  files, turn limit). Neither reports permission denials or git mutations.
- Full tests: `/private/tmp/basketball-quarter-full-tests.log`.
- Pilot: `/private/tmp/basketball-asof-additive-pilot-2026q3.log`.
- Independent review: `/private/tmp/basketball-review-quarter-pilot.py`.

The completed command was `python -u -m experiments.asof_additive_pilot` using
the repository's basketball25 interpreter. Its default prefix now exists and
must be refused on repeat. **All jobs are complete.**
