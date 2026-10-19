# v8: condition the objective, and cash the two northstar results v7 found by accident

2026-09-11 (Opus + Adam). Successor to `JOINT_CAPABILITY_V7_PLAN.md`. Read
`reports/joint_capability_v7_review.md` and `BACKLOG.md` §0ag/§0ah first.

## Context: what v7 actually handed us

v7 set out to test extrapolation by donor extremity. It answered that question
and produced two things it was not looking for, both of which speak to the
northstar more directly than anything on the accuracy track.

1. **A distance signal with dynamic range.** A model that never trained on a
   withheld donor disagrees with the full model about that donor's five-clone
   rating by **1.64 pts/100**, against **0.51** on donors it did train on, rising
   monotonically with composition distance (+0.0616/unit). No lineup outcome
   enters this quantity, so the selection-on-the-outcome objection that killed
   `distance_shrink.py` does not apply to it.
2. **A duplication penalty the model derived rather than asserted.** At matched
   no-message score, clones in the far half by composition distance are pulled
   down **3.004 ± 0.432 pts/100** more than the near half, **8/8 origins**, while
   real lineups sit at **+0.196**. That is what `tool/five.html` currently
   asserts and what four fitted attempts failed to produce.

Neither needs a single new fit. They are Phase 0.

The accuracy track meanwhile produced one lead and one closed door.
**`V7_HOLDX2` beat its matched random control by −0.0164 ± 0.0077 uniformly
across regions** — which says extreme donor states mis-condition the SHARED
objective, since the benefit appears on cells those players never touch. And
**`V7_SHOT` is established harm on conversion** (+0.000033 ± 0.000008, better in
1/12 seasons), closing the §10-coefficient route after three versions of
deferral.

**Expectation-setting, stated before the run.** v5 varied six inputs and every
one was null or harmful. The accuracy arms below are a one-in-three proposition
at best, they are chasing ~0.02 MAE on a population that resolves ~0.04, and
`V8_BASE` winning is a perfectly likely outcome. **The value of v8 is
concentrated in Phase 0**, which is why Phase 0 runs first and is not contingent
on anything.

## Revision, 2026-09-11, after Adam's steer

> *"i again want to emphasize i dont care about gates at this stage i only care
> about model improvement. gates would be a product decision to be made later."*

Phase 0 as first written was half product work. It ran, it is recorded in
`V8_PHASE0_FINDINGS.md`, and it is **parked**: P0.1's interval is a measured null
and P0.2's gate comparison is a product question for later. Neither is pursued
further.

**What the pivot to model improvement actually changed is the MEASUREMENT, and
that turned out to be the highest-leverage item in v8.**

The point benchmark resolves ~0.04 MAE and these arms chase ~0.02, which is why
v5 produced six nulls. The model is trained on five event-level families, and
that readout is far sharper on the same fits: `V7_SHOT` is **0.0 sem on MAE and
4.0 sem on conversion**.

**But event loss as v7 computes it is not comparable across arms.** The
normalising baseline is the untrained model evaluated on `train_idx`, which is
different data for every arm that reweights or withholds. Measured at 2024q3:

| arm | max baseline gap vs `V7_FULL` | artifact ÷ its own measured effect |
|---|---:|---:|
| `V7_SHOT` | **0.0000%** | 0.00x — clean, its result stands |
| `V7_LOAD` | 0.0130% | **1.37x** |
| `V7_HOLDX2` | 1.6906% | **3.49x** |
| `V7_HOLDX5` | 2.9571% | — |

Run naively, `HOLDX2 − FULL` reads 21.4 sem on event loss against 0.6 on MAE.
That is an artifact of a moving denominator — `feedback_matched_flags` in a new
costume. **v8 therefore builds a SHARED baseline first**: the untrained model on
one fixed reference set per origin, identical for every arm. It is a small change
and without it the seven arms are scored on a benchmark that cannot separate
them.

**Revised priority — model improvement only:**

1. **Shared-baseline event loss.** The measurement, not an arm. Build first.
2. **`V8_TRIM2` / `V8_TRIM5`** — the one accuracy lead v7 produced, made shippable.
3. **`V8_SCALE` / `V8_STD`** — measured mis-conditioning of the objective.
4. **`V8_HL365` / `V8_FLAT`** — an un-audited pinned default.

Everything below stands except as amended here.

## Phase 0 — no fits, RUN AND PARKED (see `V8_PHASE0_FINDINGS.md`)

### P0.1 — A distance-aware interval from v7's existing ensemble

v7 saved six fits per origin trained on **different populations** with the same
seed, so all disagreement between them is population uncertainty rather than
initialisation noise. That is exactly the quantity an out-of-support interval
should be made of, and 288 of them are already on disk.

For every evaluation cell, compute the cross-arm prediction spread. Then test,
in this order, each pre-registered before running:

1. **Does spread order error?** Weighted correlation of cross-arm sd with
   |actual − prediction|, and mean |error| by spread decile. If it is flat, stop
   and report a null — this is the same shape `per_lineup_error_bars_null.md`
   already died on, and it must be allowed to die again.
2. **Does spread rise with composition distance?** It must, or it is not
   measuring what we want.
3. **Does it beat the matched constant-width interval** on interval score at 50 /
   80 / 95%, the same comparison v4 and v6 used? A constant interval is the
   control and it has beaten every composition measure tried so far.

**Two honest limits to write into the result.** Six members is a small ensemble,
and the members are NOT exchangeable — `V7_HOLDX5` is a measurably worse model,
so its disagreement partly reflects being wrong rather than being uncertain.
Report the headline on the **matched pairs only** (`HOLDX2`/`RANDX2`,
`HOLDX5`/`RANDX5`), where the two members differ in *which* players were removed
and not in how many.

### P0.2 — Calibrate the duplication penalty against the incumbent gate

The direction is established 8/8; the magnitude is unchecked. There is no ground
truth for a lineup that never played, so this is a **comparison of two rules**,
not a validation, and the write-up must say so.

- Price the canonical fixtures both ways: the neural model's own clone score,
  and `tool_audit.py`'s page arithmetic with the coverage gate on. Five Jokićs,
  five Shaqs, five Goberts, five LeBrons, and the best five DISTINCT offensive
  and defensive units.
- Report the **cost in range** on the same basis the gate reports it: of 18,071
  real units the gate moves 1.00% at all, mean absolute change 0.0012 pts/100.
  The neural penalty's in-range cost is +0.196 mean swing, which is not the same
  statistic; compute the gate's statistic on the neural model so the two numbers
  are comparable.
- Deliverable: a table saying, for each fixture, what the assertion says, what
  the model says, and how far apart they are. If they agree within a point or
  two on the fixtures the gate was designed around, that is the strongest
  argument this project has ever had for **deriving** the gate rather than
  asserting it.

### P0.3 — Why `V7_SHOT` hurt conversion

One diagnostic, to close the question rather than leave a hypothesis in the
record. Correlate the §10 shot-quality coefficient against the message's own
make-logit output on the same player-rows in `V7_FULL`. If the message already
reproduces the coefficient, `V7_SHOT` was double-counting a teammate→conversion
estimate the model derives for itself, which would explain a consistent
out-of-sample loss. If the correlation is near zero, that explanation is wrong
and the loss needs a different one.

### P0.4 — Sizing for `V8_TRIM`, deliberately NOT done

v7's `HOLDX2` removed 21 players and 13.3% of rows. The trim arms below replace
that with a continuous weight. Adam's standing instruction from v5 applies:
*"let's proceed with the build plan, test out the ablations, then reflect and
learn after. I'm not sure how exact we can know these ablations before we try
them."* The scale parameters are therefore **declared from v7's own thresholds,
never selected**, and the grid is reported against both ends.

## Phase 1 — the sweep, seven arms

**Frozen backbone, identical in every arm:** E0M mean pooling, no encoder,
λ_net .01, γ_dec .01, lr 1e-3, width 32, seed 17, epoch cap 48 (v7 showed it is
not binding: median 12, max 30, none at the cap), 48 origins, the same
calibration and the same cells.

| arm | the one change | question |
|---|---|---|
| **V8_BASE** | none; reproduces `V7_FULL` bit-identically | parity control |
| **V8_TRIM2** | training rows down-weighted by donor extremity, gentle | can the objective buy what deleting players bought? |
| **V8_TRIM5** | the same, harsh | the dose curve, and interiority |
| **V8_SCALE** | message penalty weighted per coordinate by `1/sd_j²` | is the message budget allocated by basketball or by units? |
| **V8_STD** | message INPUTS standardised, skip path untouched | features mis-scaled, as distinct from the prior |
| **V8_HL365** | training-row half-life 365 days | recency, downward |
| **V8_FLAT** | no training-row decay at all | recency, and equal footing with the additive |

**No secondary block.** `V7_SHOT` sat in one for three versions and was never
launched; `V6_SHOT` before it. An arm is either in the run or it is not in the
plan. This is the single most useful process change v7 produced.

### Construction notes

**`V8_TRIM2` / `V8_TRIM5`.** Row weight multiplies the existing 730-day recency
weight:

```
e_i  = max over the row's five players of the prefix five-clone distance
w_i  = 1 / (1 + (e_i / d0)^2)
```

`d0 = ∞` is exactly `V8_BASE`, so the nesting is exact. `d0` is **declared** from
v7's own prefix quantiles, refit per origin like every other prefix quantity:
`V8_TRIM2` takes the p98 threshold (gentler — a higher `d0` down-weights less),
`V8_TRIM5` the p95 (harsher). With `BASE` that is three points on a dose curve.

*Pre-registered prediction, written before the run:* if v7's mechanism is
outlier trimming on a shared fit, `V8_TRIM2` beats `V8_BASE` and `V8_TRIM5` is
no better than `V8_TRIM2` — mirroring hard removal, where 2% helped and 5% was
established harm. If instead both trims are null, the `HOLDX2` result was about
removing those players' rows entirely rather than about their leverage, and the
lead is dead.

**`V8_SCALE`.** The penalty is currently `mean(msg²)` in RAW coordinate units,
so one sd of effect costs `sd_j²` — a 93x spread across coordinates, and the fit
follows the price list (make logits achieve 0.440 sd of message, location logits
0.125). Replace with `mean(w_j · msg_j²)`, `w_j ∝ 1/sd_j²`, `sd_j` prefix-
estimated per origin from the same weighted moments that already produce the
reference state.

**The weights must be normalised to average exactly 1**, `w_j = n · (1/sd_j²) /
Σ(1/sd_j²)`, or this is a λ change wearing a units change's clothes — the
recency/era gotcha restated. (An earlier draft said "rescale λ so the penalty has
the same value at initialisation"; that is vacuous, because the message head is
zero-initialised and the penalty is exactly 0 at init either way. Mean-one
weights are the correct nesting: uniform weights reproduce the current model.)

**`V8_STD`.** Feed `(base − mean)/sd` to the message network only; `base` itself
continues into the skip path unchanged so the decoder, the budget and the point
identity are untouched. Kept separate from `V8_SCALE` because "the prior is
mis-scaled" and "the features are mis-scaled" are different claims.

**`V8_HL365` / `V8_FLAT`.** One constant, `HALF_LIFE_DAYS`, currently 730 and
never audited. `V8_FLAT` is `None` (no decay), which is the additive's own
convention, so the pair also measures the time-handling asymmetry between the two
arms that has sat under every quoted MAE gap since v2. Three points — 180 is
deliberately NOT included; if `V8_HL365` wins, the grid widens down in v9 rather
than being believed at the boundary.

### Pre-registered contrasts

Declared before the run: each arm minus `V8_BASE` on all / donor5 / donor2 /
no-donor MAE, season-paired over 12 seasons with a sem and a seasons-favourable
count; `V8_TRIM2` against v7's `V7_HOLDX2 − V7_FULL` of −0.0088 ± 0.0156 and
against the `HOLDX2 − RANDX2` target of −0.0164 ± 0.0077; `V8_SCALE`'s achieved
message in sd units per coordinate group, which should move from 0.440/0.125
(make/location) toward parity if the mechanism is what §0ag says; and every arm
against the corrected additive as a separate table, never mixed in.

Plus the two standing columns, every arm, every version: the fixture context
swing **with its sign and its distance slope** — not the magnitude alone, which
is how three versions misread it — and event bias on both cohorts.

## Phase 2 — diagnostics

v7's suite unchanged: the clone ladder with mean |difference| in pts/100 reported
beside every correlation; degradation by donor-extremity decile;
difference-in-differences before any claim that a benefit is localised; the point
transfer ledger; context-shuffle and free-throw negative controls. Plus P0.1's
interval measure re-run on the v8 ensemble, and the per-coordinate message
diagnostics for `V8_SCALE`/`V8_STD`.

## Phase 3 — learnings and checkpoint

As every version since v5: append a v8 section to
`JOINT_CAPABILITY_LEARNINGS.md` under the same five headings, update
`MODEL_SCORECARD.md`, `BACKLOG.md` (both the open items and the new
do-not-re-run entries), `CLAUDE.md`'s header and `SESSION_HANDOFF.md`, then
commit with the session's attribution lines.

## Verification

- `V8_BASE` must reproduce `V7_FULL` bit-identically, as `V7_FULL` did `V6_FULL`.
- Every arm: 48 origins, one-to-one join on identical cells, possessions equal
  and actuals matching to 1e-9.
- `d0`, `sd_j` and the half-life are **prefix-only and refit per origin**; a
  future-mutation test must show that appending later games changes no prior
  weight, fit, selection or prediction.
- Every selected penalty and every declared constant printed against both ends of
  its range, every origin (rule 12).
- Full suite against the 697-test starting point; new prefix
  `experiments/cache/joint_capability_2026_09_1x_v8`; v7 immutable.

## Cost

Seven arms × 48 origins at v7's measured ~32 s per arm-origin ≈ **3.0 hours**,
inside Adam's stated tolerance and run by him outside the session. Phase 0 is
minutes and needs no fits, so it happens first and its results are in hand before
the sweep is launched.

## Not in scope for v8

**Tracking data — deferred to v9 by decision, not by drift.** The investigation
is done and recorded in `BACKLOG.md` §0ai: 2013-14 start, schemas identical
across all 13 seasons, a definition break in the Drives family at 2024-25, the
vendor switch clean, `DateTo` works so prefix-only pulls are ~24 minutes, three
granularities available including **pair-level passing**, and a 99.4% name join.
The `pair_predictability` screen came back inconclusive on the matched cohort
(everything inside a ±2% placebo band) because the restriction costs more power
than tracking adds; the next step there is to refit the pair block on the
tracking era so target and features cover the same period.

Also out: defence and the second side; the additive's own missing profile
recency (the comparator stays frozen — changing it retroactively invalidates
every gap quoted since v2); any new conversion arm, since §10 is now closed
harm and the live route is role, via `V7_LOAD`'s `k_make_over`; architecture
changes; scorer promotion; page changes; database mutation.
