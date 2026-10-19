# v9: the architecture, finally — inductive bias, not capacity

2026-09-12 (Opus + Adam). Successor to `JOINT_CAPABILITY_V8_PLAN.md`. Read
`reports/joint_capability_v8_review.md` and `BACKLOG.md` §0aj first.

## Why this version exists

After v8 I told Adam the architecture was a dead end. **That was wrong, and his
push is the reason v9 exists:**

> *"it strikes me though that this small data regime is where architectural
> changes that put in more inductive bias could make a big difference. since i
> had sol switch us back to experimenting with neural nets i dont think we really
> have experimented with the network architecture itself."*

What is actually established is that **added capacity along three axes** —
width (16/32/64, interior at 32), the learned encoder, and pair pooling — does
not help. That is not the same claim. Pair pooling's failure is *evidence for*
Adam's reading rather than against it: more capacity with worse bias, the rank-256
idiosyncrasy of `pair_effects_not_lowrank.md`.

Across v2–v8 the search was: encoder on/off · message on/off · pooling ∈ {mean,
pair, fixed} · width · λ. **Never varied: the aggregation moment, the depth, the
decoder's structure, the sender weighting.**

## The gap that motivates the whole version

The model's teammate summary is a leave-one-out **mean and nothing else**:

```python
sender = (message_in.sum(dim=1, keepdim=True) - message_in) / 4.
```

So four teammates at {+2, −2, +2, −2} and four at {0, 0, 0, 0} produce a
**byte-identical** message. The network can see lineup *average* and not lineup
*variety*.

Meanwhile this is the function v6, v7 and v8 use to decide which lineups are
unusual (`joint_capability_v6_support.composition_vector`):

```python
mean, spread = base.mean(axis=1), base.std(axis=1)
```

**Our own composition measure is half spread, and the model is architecturally
blind to that half.** Every donor-extremity result from v6 onward was computed
with a statistic the network cannot represent.

A five-clone lineup also has spread exactly zero on every coordinate.
*(Phase 0 measured how much that matters: the spread block carries 18.8% of a
median clone's composition distance and ~11% for the extreme donors, so the mean
block dominates and this is a SECONDARY argument. `V9_PHASE0_FINDINGS.md` P0.3
retracts the stronger version of the claim. The case for the spread arm rests on
P0.1 instead — spread is 98% orthogonal to the mean on ORDINARY lineups, where
the training signal and the whole evaluation live.)*

## The regime argument

1,814 parameters, ~180k training rows, effects at 1e-4 r², and every capacity
increase tried has been null or harmful. That is the regime where the right
inductive bias beats more capacity, which is Adam's point and it is correct.

## Phase 0 — no fits, and it can kill arms for free (IT DID: see `V9_PHASE0_FINDINGS.md`)

### P0.1 — does teammate spread carry information the mean does not?

Compute the leave-one-out mean and sd of the four teammates across every real
training row. Regress sd on mean, per coordinate, and report the residual share.

*Pre-registered:* if teammate sd is largely determined by teammate mean — say
under 20% residual variance on most coordinates — then `V9_SPREAD` has almost
nothing to add and is reported as a sized null **before it runs**, with its slot
returned. This is the check that costs a minute and can save three hours.

### P0.2 — how different are the alternative senders, in usable units?

For the same rows, compute four senders: uniform mean (incumbent), mean+sd,
mean+min+max, and a usage-weighted mean. Report the correlation of each against
the incumbent and the spread of the difference in state units. A sender that
correlates 0.99 with the mean is not a different architecture.

### P0.3 — is the clone/real distinction carried by the spread block?

Decompose the Mahalanobis composition distance into its **mean-block** and
**spread-block** contributions, for real lineups and for five-clone fixtures.
Five clones have exactly zero spread, so if the spread block carries most of the
distance for the fixtures, that is a direct demonstration that the model is blind
to what makes a fixture a fixture — and it converts v9 from a hopeful
architecture sweep into a targeted repair.

## Phase 1 — six arms (`V9_USAGE` was killed in Phase 0)

**Backbone:** v8's, **plus standardised message inputs**, which v8 established at
12/12 seasons on all five families for free. `V9_BASE` must therefore reproduce
`V8_STD` bit-identically, the way each version's base has reproduced its
predecessor's winner since v5.

**Everything else frozen:** lr 1e-3, width 32, γ .01, λ .01, seed 17, epoch cap
48, 48 origins, the shared event-loss baseline, the same calibration and cells.

| arm | the one change | why |
|---|---|---|
| **V9_BASE** | none; reproduces `V8_STD` | parity control |
| **V9_SPREAD** | sender = [mean, **sd**] of the other four | the moment our own measure uses and the model cannot see |
| **V9_MINMAX** | sender = [mean, **min, max**] | extremes rather than dispersion — *which* moment matters, not just "more than mean" |
| **V9_DEPTH** | **two** message rounds, second zero-initialised | one round cannot represent "A's effect on B depends on C" |
| **V9_DECODER** | `intercept + slope·z + U(Vᵀz)`, rank 3, `U` zero-initialised | today coordinate *j* maps only to output *j* — §8j's `self_2p`-is-one-number defect in neural clothing |
| **V9_ALL** | SPREAD + DEPTH + DECODER | do they stack or overlap? v5's ALL arm, which caught that the parts summed exactly |

### Nesting is the whole design

**Every arm reproduces `V9_BASE` exactly when its new block is zeroed**, and every
new block is zero-initialised, so each arm starts *at* the base model and can only
depart if the data pays for it. This is what makes them one factor wide and what
makes a null interpretable rather than ambiguous (rule 10).

Parameter cost, against the base's 1,814: SPREAD +576, MINMAX +1,152,
DEPTH +1,778, DECODER +108.

### Construction notes

- **`V9_SPREAD`.** Leave-one-out sd, computed as
  `sqrt(max(E[x²]_{-i} − (E[x]_{-i})², 0))` so it stays a single pass. Concatenate
  to the sender: message input 36 → 54. The new columns' first-layer weights start
  at zero.
- **`V9_DEPTH`.** Round two reads the round-one output: `z₁ = base + msg₁`, then
  `msg₂ = M₂(z₁, mean_{j≠i} z₁)`, `z = z₁ + msg₂`. Separate parameters, zeroed
  output layer. The free-throw mask applies to both rounds.
- **`V9_DECODER`.** Keep the diagonal term. The low-rank correction is additive on
  top, so interpretability degrades gracefully rather than being discarded, and
  `U = 0` is the incumbent. **Tension to record:** the diagonal decoder is part of
  why each coordinate stays anchored to its own meaning; if `V9_DECODER` wins,
  what it costs in interpretability is a real finding and not a footnote.

### Pre-registered contrasts

Each arm minus `V9_BASE` on **event loss and its five families first**, season-
paired with sem and seasons-favourable — that is the readout with power, and v8
established points cannot resolve gains of this size (slope −3.68 ± 21.39,
r = −0.0102 over 288 paired deltas). Points reported second, as a separate table,
with the expectation of a null stated in advance.

Plus: `V9_ALL` against the sum of its parts (overlap); the achieved message per
coordinate group.

## Phase 2 — diagnostics

v8's suite, plus one specific to this version: **re-run the five-clone ladder and
ask whether any winning arm now separates clone lineups from real ones
differently**, since spread is exactly zero for clones. Report mean |difference|
in pts/100 beside any correlation (the v6→v7 lesson).

## Phase 3 — learnings and checkpoint

As every version since v5: the five headings in
`JOINT_CAPABILITY_LEARNINGS.md`, `MODEL_SCORECARD.md`, `BACKLOG.md` open and
do-not-re-run entries, `CLAUDE.md`'s header, `SESSION_HANDOFF.md`, then commit.

## Expectation setting, stated before the run

Every capacity increase tried in this workstream has been null or harmful, and
three of these arms add capacity. The honest prior is that most of them fail.
What makes v9 worth running anyway is that **the axes are different in kind** —
these are statements about what the network is allowed to *see*, not how much it
can *fit* — and that one of them is a demonstrable blindness to a statistic the
project's own measurements depend on.

`V9_BASE` winning is a real outcome and would close the architecture question
properly, which seven versions of not asking have not.

## Verification

- `V9_BASE` reproduces `V8_STD` bit-identically.
- Every arm reproduces `V9_BASE` when its new block is zeroed — asserted by test,
  not argued.
- Event-loss baseline shared per origin, verified identical across all
  arm-origins as in v8.
- All prefix quantities (usage share, state moments) refit per origin; a
  future-mutation test shows appending later games changes nothing.
- Full suite against the 719-test starting point; new prefix
  `experiments/cache/joint_capability_2026_09_1x_v9`; v8 immutable.

## Not in scope

Tracking (§0ai — still v10 or later, and the pair-block refit comes first);
defence and the second side; the objective itself (v8 established the
objective/target gap is resolution, not misalignment — **do not change the
objective**); the coverage gate and anything product-side; scorer promotion.
