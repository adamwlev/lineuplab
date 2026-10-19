# Joint capability v7: how far out does it hold, and what does the blend cost?

Prepared by Claude Opus 5 with Adam, 2026-09-11. Successor to
`JOINT_CAPABILITY_V6_PLAN.md`. Read `reports/joint_capability_v6_review.md`,
`V6_PHASE0_FINDINGS.md` and `JOINT_CAPABILITY_LEARNINGS.md` first.

**Status: agreed implementation contract. No v7 experiment has been run.**

Boundaries unchanged: no scraper, no database access, no input-cache rebuild, no
scorer promotion, no page deployment, never modify a completed run directory.
Preflight runs under `no_database()` and writes `reproduce.json`; the
reproducibility contract in `experiments/joint_capability_repro.py` applies to
every derived input.

## Context

v6 answered its question. Withholding the unusual quartile of lineups costs
nothing: `HOLD75` has the best withheld-region MAE of five arms, beats the model
trained on everything there, and its five-clone ratings correlate **r = 0.9966**
with the full model's donor by donor, with no gradient in composition distance.
So the selection-on-the-outcome objection — why the tool's coverage gate is
asserted rather than fitted — does not appear to bind a model with no lineup,
pair or identity parameters.

**But 99.5% of v6's withheld cells sat at or below the clean real maximum
composition distance of 10.31.** v6 validated extrapolation *across* the observed
range. The fixtures the tool must actually survive are at **1.81×** and beyond.
That is the gap v7 closes.

Separately, Adam's accuracy question is answered and does not need an experiment:
a flat 50/50 blend of the neural arm and the corrected additive already scores
MAE 8.0603 against the additive's 8.0920 (season-paired −0.0311 ± 0.0235, 7/11),
and the ceiling above it is capped — the two arms' errors correlate **+0.9875**,
so the best achievable blend is 0.16% of RMSE. Distance-weighting the blend buys
+0.0014 MAE over a flat weight **with oracle weights**. There is nothing left to
research in combination, only something to bank — and one thing to check, below.

## Phase 0 — audits, no core fits

**H0.1 — the hyperparameters nobody has ever varied.** `lr = 0.001` is hardcoded
in every module from v2 to v6 and **has never been changed in six versions**.
So have hidden width 32, weight decay 1e-4 and batch target 4096. CLAUDE.md rule
12: *a default is un-audited until some run has walked off it, and is visible in
neither the command line nor the write-up.* This one is load-bearing, because
Phase 0 of v6 found the learned corrections sit at ~2% of state scale after a few
hundred Adam steps — if the model is undertrained, `lr` is the first suspect.

γ (decoder) deserves the same treatment: it was selected on **3.5e-5** of
validation loss against a 1e-5 tie tolerance, on one arm, which is the
tie-break-on-noise pattern that gave v2's control λ = 1.0 and froze it at epoch 1.

On the two development origins only (2014q3, 2014q4), never on a primary origin:
`lr ∈ {1e-3, 3e-3, 1e-2}`, `width ∈ {32, 64}`, `γ ∈ {.003, .01, .03}`. Print the
selected value against **both** grid ends every run. This is an audit of
un-audited defaults, not the open-ended sweep prior plans forbid; say so
explicitly in the write-up.

**Raise the epoch cap from 24 to 48 regardless of what the audit finds.** In v6,
15 of 240 arm-origins ran to the wall, though only **3 of 240** selected epoch 24
and the median last-epoch gain on capped runs was −8e-6 — so the cap is a
boundary to remove rather than a live constraint, and removing it costs almost
nothing. λ stays at .01: v4 and v5 walked off it in both directions and
established an interior optimum.

**H0.2 — what the blend costs the northstar.** No fits. The additive's
duplication curve is *exactly linear* (`tool_breaks_on_repetition.md`), which is
why five copies of a star price at +21 to +26 against a real maximum of +15.6.
**A 50/50 blend therefore reimports half of the 5-Shaq problem.** Score the
additive on the same clone ladders v6 used — `additive_offense_score` takes a
snapshot and lineups directly — and measure how much of the neural arm's sane
clone behaviour the blend destroys. This is the number that decides whether the
blend can ship as-is or only inside the support.

## Phase 1 — the sweep

Backbone frozen at v5/v6 `E0M`, with the epoch cap at 48 and any setting H0.1
establishes. **The factor is again the training population, but withheld by
DONOR EXTREMITY rather than by lineup quantile.**

For each origin, compute every player's *five-clone distance* — the composition
distance of a lineup made of five copies of him — on that origin's training
prefix reference. Rank players by it. `HOLDX` then removes **every training row
containing any player in the top 5%**.

Sizing, measured at 2026q1 over 993 players in the window:

| holdout | players | rows removed | donor five-clone distance |
|---|---:|---:|---:|
| top 10% | 100 | 49.4% | 1.81× the real maximum |
| **top 5%** | **50** | **27.4%** | **2.10×** |
| top 2% | 20 | 12.5% | 2.36× |

**Top 5% is the operating point.** It removes essentially the same share of
training data as v6's `HOLD75` (25%), which cost nothing — so the comparison is
like for like on data volume, and the only thing that changed is *how far out*
the withheld region sits. Top 10% reaches exactly the 1.81× fixture regime but
costs half the corpus, which would conflate data loss with extrapolation.

| arm | trains on | serves |
|---|---|---|
| **V7_FULL** | everything (alias of v6 `V6_FULL`, no fits) | control |
| **V7_HOLDX5** | all rows *except* those containing a top-5% donor (27.4% removed, donors at 2.10×) | primary |
| **V7_RANDX5** | a random, equally-exposed set of players withheld instead | its control |
| **V7_HOLDX2** | all rows except those containing a top-2% donor (12.5% removed, donors at 2.36×) | extremity dose |
| **V7_RANDX2** | matched random player holdout | its control |
| **V7_LOAD** | everything, plus a constrained overload response (§8.1) | bounds duplication by MECHANISM |
| **V7_SHOT** | everything plus the §10 shot-quality coefficient (built and smoked in v6, never run) | conversion |

Six new arms ≈ 2.6 hours at v6's measured rate; the HOLD arms train on less data
and run faster than `FULL`. H0.1 confirmed the incumbent hyperparameters are an
interior optimum, so there is no `TUNE` arm and every arm fits at lr 1e-3,
width 32, γ .01, λ .01, with the epoch cap raised to 48.

**Why the second holdout pair is worth two arms.** `HOLDX2` removes *less* data
(12.5% against 27.4%) while reaching *further* out (2.36× against 2.10×). So the
two pairs move data volume and extremity in **opposite** directions. If `HOLDX2`
degrades more than `HOLDX5` despite keeping more data, extremity is the cause and
volume is not — which no single pair can establish. v6's HOLD75/HOLD50 varied
only volume; this varies the axis the experiment is actually about.

Each `RANDX` must withhold **players**, not rows, because its `HOLDX` partner
does — matched on player count, rows touched and possessions touched, **measured
and recorded every origin**. Matching rows alone is not enough; v6 showed that
matching one margin can still hand the control an advantage on another.

*Amended mid-run, 2026-09-11.* This began as an assertion and it aborted the
sweep after origin 39 of 48, because 2024q3's matcher landed at 3.22% against a
3% threshold — one pair-origin in 78. The gap is now `match_quality`, which
returns the signed per-field gap and a flag; the runner prints a `MATCH` line and
writes `origins/<tag>/match.json`. Measured across all 48: median 0.83% / 0.64%
for the two pairs, p90 near 1%, one origin flagged. **The sign is the part that
matters** — positive means the random control removed MORE than its holdout, so
the control is handicapped and the holdout flattered, which is the direction that
would manufacture the result. Every contrast is therefore reported twice, with
and without the flagged origins. A quality measure belongs in the analysis, not
in a tripwire that destroys two hours of compute over 0.22 of a percentage point.

### Pre-registered contrasts

1. **`HOLDX5 − RANDX5` on cells containing a withheld donor.** The direct
   analogue of v6's primary contrast, at 2.10× instead of 1.0×.
2. **The difference-in-differences**, `(HOLD − RAND | donor cells) − (HOLD −
   RAND | other cells)`, for each pair. v6 taught that an arm trained only on one
   region beats its partner there by construction, so neither region alone is
   interpretable.
3. **The extremity dose**: `HOLDX2 − RANDX2` against `HOLDX5 − RANDX5`. Less data
   removed, further out. If the deeper holdout hurts more, extremity is the cause
   rather than volume.
4. **Clone-ladder agreement for the withheld donors**: correlation of five-clone
   ratings between each `HOLD` arm and `FULL`, restricted to players that arm
   never saw. v6 got 0.9966 for players it *had* seen in other lineups; this is
   the real test, and the one that speaks to the coverage gate.
5. `V7_SHOT` on the conversion channel first (FG Brier, raw conversion family),
   points second.

Scoring variants, no extra fits: every arm is additionally scored with the
message zeroed, so degradation attributes to the learned context rather than to
the shared budget that Phase 0 of v6 showed carries about half the clone
response; and every cell carries the neural, additive and 50/50 blend prediction
so the Phase 2 handoff can be evaluated without refitting.

### What each outcome means

- **`HOLDX ≈ RANDX` and clone agreement stays high.** The model prices players it
  has never seen from their states alone, out to 2.1× the observed maximum. That
  is the evidence needed to argue the coverage gate could be *derived* rather
  than asserted — the northstar argument `ROLE_MODEL.md` made for the whole
  hierarchical programme.
- **`HOLDX` degrades.** Extrapolation holds across the observed range (v6) and
  fails beyond it, which is a sharp and useful boundary: it tells the product
  exactly where to stop trusting the model and start asserting.

## Phase 2 — bounding duplication by mechanism, not assertion

**H0.2 killed the premise this section originally had.** I had proposed "blend
inside the support, neural model outside it" on the theory that the blend
reimports the additive's linear duplication while the neural arm is safe. It is
not: at the top decile of donor value the neural arm moves **+16 points** from
one copy to five and exceeds the 99th percentile of real single-copy ratings
**89%** of the time, and above the top 5% it blows up *more* than the additive.
The shared budget bounds volume, not efficiency.

Adam's direction is that an asserted gate is not the answer. The alternative was
already specified and never built — `JOINT_CAPABILITY_MODEL_PLAN.md` §8.1, an
explicit responsibility response, framed there as "a constrained overload
response, not a position rule":

    excess = max(0, assigned_share - his own prior share) / max(prior_sd, 0.05)
      + k_TO * excess   on the turnover-versus-FGA log odds
      - k_FG * excess   on the FG make logits

Two parameters, both constrained non-negative with zero an exact boundary, fitted
on **real events** under the same protocol as everything else. In a five-clone
lineup every player is assigned roughly five times his historical share, so the
penalty binds hard — learned from real games where players were overextended,
rather than decided by us.

Three reasons it is worth an arm beyond the framing. This repository's own record
says **usage conflict is the only named mechanism with signal**
(`the_ball_is_the_interaction.md`) and usage demand is the one composition
structure that survived forward (`usage_demand_forward.md`, t = +4.84), so there
is prior evidence the effect exists. Two parameters cannot overfit their way to a
flattering answer. And the spec is honest about failure: *if k fits zero or the
mechanism fails, record it; do not force a positive value.*

`V7_LOAD` is judged on three things, in order: does `k` fit non-zero on real
events; does it bound the duplication blow-up H0.2 measured; and what does it
cost on real lineups. Allocation is taken from the base forecast in one pass and
the budget renormalised after the turnover adjustment — no circular fixed point,
per §8.1.

Also in Phase 2: the degradation curve by donor-extremity decile, the analogue of
v6's flat distance gradient; and interval recalibration on the rebuilt
Mahalanobis measure, carried from v6 and still not done.

## Phase 3 — learnings and checkpoint

Append a v7 section to `JOINT_CAPABILITY_LEARNINGS.md` under the same five
headings, update `MODEL_SCORECARD.md`, `BACKLOG.md` (do-not-re-run first),
`CLAUDE.md` and `SESSION_HANDOFF.md`, then commit.

## Verification

- `V7_FULL` must reproduce v6 `V6_FULL` bit-identically, as `V6_FULL` did v5.
- Donor ranking and holdout masks **prefix-only and refit per origin**; a ranking
  built from the full sample leaks the test window's composition.
- `HOLDX`/`RANDX` matching on players, rows and possessions **measured** per
  origin and carried into the contrast, never asserted (see Phase 1).
- No withheld donor may appear in any `HOLDX` training row — this one IS
  asserted, directly rather than inferred from the mask. It is a different
  animal: zero tolerance, deterministic, and it fires only on an actual leak.
  A bug detector, not a quality threshold.
- `reproduce.json` present, `untracked_code()` empty, preflight under
  `no_database()`.
- Full suite against the 680-test starting point; new prefix
  `experiments/cache/joint_capability_2026_09_1x_v7`; v6 immutable.

## Not in scope

**Tracking data — deferred to v8 by decision.** The probe
(`experiments/probe_tracking.py`) reached `stats.nba.com` with HTTP 200 and
parsed 572 player rows including `POTENTIAL_AST`, so the 2026-09-02 block is not
in force and the route is open when we want it.

Also out: any architecture change beyond what H0.1 selects; further input
enrichment beyond `V7_SHOT`; defence and the second side; and chasing pooled
point accuracy, which the blend has already settled and redundancy has capped.
