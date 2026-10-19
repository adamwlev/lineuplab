# Joint capability v5: inputs and target

Prepared by Claude Opus 5 with Adam, 2026-09-10. Successor to
`SOL_JOINT_CAPABILITY_DAY3_PLAN.md` (v4). Read
`reports/joint_capability_v4_review.md`, `CLAUDE_MODEL_FEEDBACK_4.md` and
`JOINT_CAPABILITY_LEARNINGS.md` first.

**Status: agreed implementation contract. No v5 experiment has been run.**

## Working agreement for this cycle

Adam and Claude are the two participants this week; Sol/Codex/Astra usage is
exhausted. The cycle is deliberately version-sized, because the fitting cost is
dominated by the 48-origin sweep and six arms therefore cost barely more per arm
than one:

1. Holistic review of status and fruitful paths.
2. A plan for one new version running 4-8 arms, so a chunk of the space is
   tested in a single build.
3. Adam runs the long build himself, outside Claude, 2-4 hours, verbose, with the
   cumulative scoreboard reprinted as it goes. Claude does not sit and poll a
   healthy process.
4. Diagnostics, benchmarks, tests, reflection.
5. Learnings written to `JOINT_CAPABILITY_LEARNINGS.md` and a git commit, so each
   version is a checkpoint in the code for posterity.
6. Meet, discuss, write the next version.

Boundaries unchanged from prior plans: no scraper, no database access, no input
cache rebuild, no scorer promotion, no page deployment. Never modify a completed
run directory; new work gets a new prefix. Preserve `MODEL_FEEDBACK_FROM_CLAUDE.md`.
Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u`.

## Context

v4 settled the architecture question. Mean pooling carries the whole teammate
effect (novel RMSE −0.122, **11/11 seasons**, interval excluding zero); pair
pooling adds nothing and is worse out of sample; the learned encoder is null at
matched pooling; λ = .0001 hurts novel lineups. The backbone is **E0M_L2** —
1,814 parameters, 18 inputs per player.

What is left is not the network. Three things now point at the **inputs and the
target**:

1. **The additive's offensive coefficients are opponent-deconfounded and the
   neural states are not.** `asof_additive.identity_design` returns `(n, 2P)` —
   offence block *and* defence block — so every θ_off is estimated controlling
   for who was defending. The neural model's 18 coordinates are raw EB-shrunk
   historical rates; a player whose last 730 days came against weak defences
   carries an inflated shooting offset into every lineup. The two arms are not
   on equal footing on their inputs, and nobody has measured the cost.
2. **The backbone reads 18 of its 64 features.** E0 arms have no encoder, so
   exposure, missingness, the recency contrasts, the prior-teammate reference,
   staleness and ORB are all unused. Effective free dimensions per player: 13
   (3 rates + 5 mix + 2 shooting offsets + FT + assist + assisted share), against
   `box_score_explains_rating.md`'s measured 32 dims for 78% of offensive rating.
3. **A large, undiscussed population miscalibration.** On the evaluation cells
   the model over-predicts FTA by +2.9/100 against +0.1 on the full cohort — the
   documented common-fives deployment artifact, reproduced exactly, an order of
   magnitude larger than the differences the arms are arguing over.

**v5 therefore freezes the architecture and varies only the inputs and the
target.** Every arm is a one-factor change on E0M_L2.

Two pieces of expectation-setting, stated up front so we do not misread the
result: this benchmark resolves a lever worth ~0.04 MAE and **not** one worth
~0.01 (BACKLOG §0), and the best neural arm already trails the corrected additive
by 0.018 MAE. The realistic v5 win condition is **mechanism plus novel-slice
movement**, not beating the additive on pooled MAE.

## Phase 0 — diagnostics that need no fits

Run before the v5 sweep. These size the levers (CLAUDE.md rule 8) and one of them
is a free win we should bank first so v5 is measured on the better footing.

**D1 — bank the over-dispersion shrink.** BACKLOG §0ad item 4: both arms are too
wide after calibration and an extra shrink of ~0.79 takes 0.5% off MSE for no
modelling. I measured the same thing independently in v3: the regression slope of
actual on prediction is ~0.88 for *every* arm including the additive. Re-measure
prior-only on the v4e cells, apply the identical shrink to every arm, and report
both the shrunk and unshrunk tables. Free, symmetric, changes no comparison.

**D2 — the differential opponent test (gates V5-OPP).** For each cell, compute the
exposure-weighted mean defensive strength faced by the five offensive players
**during their 730-day state window** — not during the scored window, which is
lever (a) and already settled. Regress each arm's forward residual on it.

*Pre-registered prediction:* the neural residual loads positively and the
additive's reads ≈ 0, because θ_off is already opponent-controlled. **The
additive is the built-in placebo.** Reuse `onfloor_opponent.opponent_strength`
and `onfloor_defense.centered_defense_score`; do not build a new defensive metric.

*Pre-registered gate, declared before running D2:* if the neural residual's slope
on state-window defence is under 1 sem, or implies under 0.01 pts/100 of cell
spread, V5-OPP is reported as a sized null and its slot goes to V5-L1.

**D3 — the deployment decomposition.** Surface event bias on common cells beside
the full cohort (already computed in `event_metrics.csv`, never reported), then
split the mean-versus-fixed event gain by the coarse clock × score-margin buckets
from `ASOF_DEPLOYMENT_AUDIT.md` that cut the descriptive FTA gap from 2.228 to
1.037/100. Answers whether part of what "context" learned is deployment.

**D4 — rebuild the support measure and re-run the intervals.** No fits. Real
cells span composition distance 0.515–3.105 and five Goberts scores 3.191 — 3%
beyond the real maximum — so "composition distance does not help" is a statement
about the measure, not the idea. Recompute on the Mahalanobis profile scale of
`composition_extrapolation.md` (real fives 4–11.5, five Shaqs 20.9), re-derive the
role-stress threshold from the realized distribution instead of the pinned 2
(which fires on 0 of 5,607 cells), and re-run the same pre-registered isotonic
method on saved v4e predictions.

## Phase 1 — the v5 sweep

**Frozen backbone, identical in every arm:** E0M pooling (leave-one-out teammate
mean), no encoder, λ_net = .01, γ_dec = .01, seed 17, max 24 epochs / patience 3 /
min-delta 1e-5, 730-day training weight, shared prefix budget `U`, five loss
families, 48 origins, same calibration and same 5,607 cells.

λ stays a **declared factor, never selected per arm** — v4's single best design
decision, and what removed the boundary-control problem that compromised v2 and v3.

### Primary block — six arms

| arm | the one change | question |
|---|---|---|
| **V5-BASE** | none; v4e E0M_L2 reproduced under v5 code | parity control, audited like v4's aliases |
| **V5-OPP** | states built from opponent-deconfounded event rates | does equal footing on inputs close the additive gap? |
| **V5-BIO** | height, position and debut year added to the message input | the biggest measured additive lever, absent here |
| **V5-ORB** | ORB **per team miss** as a 19th coordinate, decoded, with its own binomial family; **budget unchanged** | Oliver's missing fourth factor, estimation only |
| **V5-RICH** | the 46 unused `x` features routed straight into the message input | is the encoder null a *feature* null or a *routing* failure? |
| **V5-ALL** | OPP + BIO + ORB + RICH | do they stack or overlap? |

### Secondary block — two arms, only if primary finishes inside budget

| arm | change | question |
|---|---|---|
| **V5-L1** | BASE at λ_net = .1 | .0001 hurt novel lineups; upward is untested |
| **V5-LEV** | five families weighted by prior-only points leverage | does pointing capacity at conversion finally move conversion? |

**Cost.** v4e measured ~18 s per fit, two fits per arm-origin. Primary
6 × 48 × 2 × 18 s ≈ **2.9 h**; with secondary ≈ **3.8 h**. The split is the safety
valve — primary alone is a complete result.

### Construction notes

- **V5-OPP.** Build one *continuous daily* defensive-strength series inside the
  existing chronological day loop — prior-only at every date, therefore valid for
  all 48 origins from a single build. Do **not** build 48 per-origin tensors.
  Adjust each family's rate as `raw − β_family · (defence_faced − league)`, with
  β estimated prior-only per family and printed per origin. β = 0 is exactly
  V5-BASE, so the nesting is exact. Caution from BACKLOG: a *fitted* κ for the
  **target** correction scored worse than κ = 1 — that is the target side, but it
  argues for the simplest coefficient and for printing its stability.
- **V5-BIO.** Height and position are static and knowable at debut, which answers
  the plan's temporal-provenance objection; record the provenance rule explicitly
  and never use a future roster fact.
- **V5-ORB.** Per **miss**, not per possession — per-opportunity denominators are
  the discriminator established by the four-factors work. No budget feedback in
  v5; that is a later, separate change.

### Pre-registered contrasts

Declared before the run: each single arm minus BASE on all and novel
MAE/RMSE/r²; ALL minus BASE; ALL against the sum of the singles (overlap);
and for OPP, the D2 residual loading, which should collapse toward zero if it
worked. Everything is additionally scored against the opponent-corrected target
as a **clearly separate table** — never mixed into one leaderboard.

### Two discipline changes I want in v5

1. **A real holdout.** The 2016–26 benchmark has now been read across v2, v3, v4
   and four reviews. Reserve **2026q1–q4 as a confirmation slice** that no v5
   contrast is read on. Decide on 2016–2025 (40 origins), then look once. It
   costs ~10% of power and it is the only genuine mitigation for accumulated
   selection.
2. **Two standing guardrail columns**, reported for every arm every version:
   the fixture context swing as a **percentage of the in-range maximum** (five
   Goberts has been 226% / 228% of it in v3 and v4 while being quoted as a
   result), and **event bias on both cohorts** so C1 can never hide again.

### Logging

Keep v4's format — Adam follows the run live. Per completed arm-origin:

```
origin=... arm=V5-OPP fit_end=... test=[...,...) cells=... poss=...
event_loss=... FG_Brier=... mix_CE=... FTA_bias100=... beta_opp=...
MAE=... additive=... delta=... RMSE=... r2=... novel_MAE=... epoch=... elapsed=...
```

and the **cumulative primary scoreboard reprinted every few origins**, all arms
plus corrected additive, location+shooting and structural parent.

## Phase 2 — diagnostics and reflection

Reuse v4's suite unchanged: point-transfer ledger (opportunity / location /
conversion, both path orderings, reconciling below 1e-13), basketball fixture
panel, failure review selected on the first chronological half and tested on the
second, context-shuffle and FT negative controls, seed sensitivity, rolling
intervals. Add per-arm D2 re-run, the two guardrail columns, and D4's rebuilt
support measure. Full suite green, fit ledger with matched start/completion,
hashes for plan and protocol, superseded prefixes preserved.

## Phase 3 — document the learnings and checkpoint

Every version ends with a written record and a commit. You already started this
(`f8d7017` after v3, `e27d116` after v4); what is missing is the *learnings*
being a first-class artifact rather than something spread across a review, a
feedback doc and a handoff. Git sees nothing under `experiments/cache` — all of
it is ignored — so a checkpoint is docs and code only and stays small.

**New file `JOINT_CAPABILITY_LEARNINGS.md`**, one section per version, appended
never rewritten, each carrying the same five headings:

1. **What changed** — the arms and the one factor each varied.
2. **What was established** — with the contrast, interval and seasons-favourable.
3. **What was killed** — negatives are the expensive half; pair pooling and the
   encoder belong here from v4.
4. **What it cost** — fits, wall clock, and what we chose not to run.
5. **Still open** — carried into the next version's arm list.

Backfill v2/v3/v4 sections from the existing reviews as the first act, so the
file starts complete rather than starting now.

Alongside it, the four canonical files get their standing updates, which is
already this repo's convention: a `MODEL_SCORECARD.md` row per surviving
candidate, `BACKLOG.md` gaining both the new open items and — more importantly —
the new **do-not-re-run** entries, `CLAUDE.md`'s header summary, and a prepended
`SESSION_HANDOFF.md` entry.

Then commit, with the message naming the version and its one-line finding, ending
with the session's attribution lines.

**Immediate first action, before any v5 work:** commit `CLAUDE_MODEL_FEEDBACK_4.md`
to close out the v4 checkpoint, and backfill the learnings file.

Then we meet, read it together, and write v6.

## Verification

- V5-BASE must reproduce v4e E0M_L2 to the same standard v4 held its aliases to
  (function parity 0.0 on a fixed row sample, frozen source hashes checked).
- Every arm: 48 origins, one-to-one join against the frozen benchmark cells with
  possessions equal and actual points matching to 1e-9.
- Before any fit: brute-force-versus-incremental test on the new daily defensive
  series, and a future-mutation test showing that appending later games changes
  no prior feature, fit, selection or prediction.
- Full repository suite compared against the 640-test starting point, unrelated
  failures preserved.
- New prefix `experiments/cache/joint_capability_2026_09_1x_v5`; v4e and its
  report prefixes immutable.

## Not in scope for v5

Opponent conditioning of the *prediction* (lever a) — the target correction at
coefficient 1 is free and already banked, and a fitted coefficient is in
do-not-re-run. ORB budget feedback. Defence as a second side. Any architecture
change. No scorer promotion, no page change, no database access, no cache rebuild.
