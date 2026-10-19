# v9 Phase 0 — no fits

2026-09-12 (Opus + Adam). Measured on the 2024q3 training prefix, 178,059 rows,
using v7's cached data. No model trained, no database touched.

**Outcome: one arm strongly supported, one arm killed, and one claim in the plan
retracted.**

---

## P0.1 — teammate spread is nearly orthogonal to teammate mean ✅

The gate, declared before running: *"if teammate sd is largely determined by
teammate mean — say under 20% residual variance on most coordinates — then
`V9_SPREAD` has almost nothing to add."*

Regressing each coordinate's leave-one-out sd on its leave-one-out mean:

| | residual share of sd variance |
|---|---:|
| median over 18 coordinates | **98.1%** |
| minimum (location_logit_above_break3) | 55.1% |
| coordinates above 80% residual | **17 of 18** |

Only `location_logit_above_break3` shows real structure (r = −0.670), which makes
basketball sense: a lineup whose average three-point tendency is extreme has less
room to vary. Everything else is essentially free information.

The magnitudes are not trivial either — the sd of the leave-one-out sd runs from
0.033 (`make_logit_corner3`) to 0.408 (`location_logit_above_break3`), against
coordinate sds of 0.089–0.862. **Teammate variety is roughly a third to a half the
size of teammate average, and the model receives none of it.**

`V9_SPREAD` passes and is the strongest-motivated arm in the version.

---

## P0.2 — how far the alternative senders actually sit from the mean

The gate: *"a sender that correlates 0.99 with the mean is not a different
architecture."*

| candidate sender | mean \|corr\| vs the mean | mean \|difference\| in coordinate sds |
|---|---:|---:|
| leave-one-out **sd** | **0.165** | **3.805** |
| leave-one-out **max** | 0.696 | 1.024 |
| leave-one-out **min** | 0.706 | 1.023 |
| usage-weighted mean, α = 1 | — | **0.026** |
| usage-weighted mean, α = 3 | — | 0.078 |
| usage-weighted mean, α = 10 | — | 0.255 |

**`V9_USAGE` is killed.** Within-lineup usage share has an sd of only 0.050 around
its mechanical mean of 0.197, so the five players are close to equally weighted
however the softmax is tuned. At any α the model would plausibly fit, the
usage-weighted sender sits **0.026–0.078 coordinate sds** from the uniform mean —
two orders of magnitude below the sd sender's 3.805. There is nothing there to
learn, and its slot is returned as the plan promised.

Worth recording as the reason: *the question "which teammate is loudest" cannot be
answered with usage share, because in this state representation the five players
are nearly equally loud by construction.* A different notion of influence might
still work; usage is not it.

`V9_MINMAX` survives but is clearly the weaker sender arm — |corr| 0.70 against the
sd sender's 0.165.

---

## P0.3 — the plan's fixture claim is RETRACTED

The plan said: *"a five-clone lineup has spread exactly zero on every coordinate…
spread is precisely the statistic that separates a clone fixture from a real five."*
The first half is true; the second half overstates it.

Decomposing the Mahalanobis composition distance by substituting the reference
mean into one block at a time (median):

| | full | MEAN block only | SPREAD block only |
|---|---:|---:|---:|
| real lineups | 5.40 | 4.33 | 3.98 |
| five clones | 10.90 | 8.85 | 6.81 |
| top-21 donors | 24.63 | 21.85 | 6.81 |

Spread columns are **exactly 0.0000e+00** for clones against a mean |value| of
0.4299 for real lineups, as claimed. But the spread block contributes only
**18.8%** of a median clone's distance and about **11%** for the extreme donors —
the **mean block dominates**, and it dominates more as the donors get more extreme.

So the model's blindness to spread is real but is **not** the main thing that makes
a fixture a fixture. The honest version: a clone lineup sits 1.7x further out on
the spread block alone (6.81 vs 3.98), which is a genuine signal and a secondary
one.

**The case for `V9_SPREAD` therefore rests on P0.1, not on the fixtures** — it is
about information the model lacks on ORDINARY lineups, which is where the training
signal and the entire evaluation live. That is the stronger argument anyway, and
the plan reached for the flashier one.

---

## Revised Phase 1 — six arms

| arm | change | status after Phase 0 |
|---|---|---|
| `V9_BASE` | none; reproduces `V8_STD` | control |
| `V9_SPREAD` | sender = [mean, **sd**] | **strongly supported** (P0.1, P0.2) |
| `V9_MINMAX` | sender = [mean, **min, max**] | supported, weaker |
| `V9_DEPTH` | two message rounds | unchanged; no Phase 0 gate |
| `V9_DECODER` | rank-3 additive correction to the diagonal | unchanged; no Phase 0 gate |
| `V9_ALL` | SPREAD + DEPTH + DECODER | overlap test |
| ~~`V9_USAGE`~~ | usage-weighted sender | **killed by P0.2** |

Six arms × 48 origins at v8's measured rate ≈ **2.3 hours**.

---

## Build verification, 2026-09-12

**Exact nesting, asserted not argued.** Every arm reproduces `V9_BASE` at
initialisation to `0.000e+00` on the predicted points, because each new block
enters through separately-constructed zero-initialised parameters while the
shared blocks are drawn in the same order from the same seed:

| arm | parameters | max \|prediction − base\| at init |
|---|---:|---:|
| `V9_BASE` | 1,814 | — |
| `V9_SPREAD` | 2,390 | **0.000e+00** |
| `V9_MINMAX` | 2,966 | **0.000e+00** |
| `V9_DEPTH` | 3,592 | **0.000e+00** |
| `V9_DECODER` | 1,922 | **0.000e+00** |
| `V9_ALL` | 4,276 | **0.000e+00** |

An arm therefore starts *at* the base model, so a null reads "the data did not pay
for this block" rather than "it started somewhere else."

**`V9_BASE` reproduces `V8_STD` bit-identically** at 2015q1 — MAE, RMSE, r², bias,
event loss, all five families and the selected epoch, every difference exactly
`0.00e+00`.

**The blocks are alive.** On the smoke origin all three grew from zero, which is
the readout `architecture_report` exists to give:

| arm | block growth | event loss vs base |
|---|---|---:|
| `V9_SPREAD` | sender block at **38% of the base first-layer norm** | −5.7e-04 |
| `V9_DEPTH` | round two at **45% of round one** | −1.5e-04 |
| `V9_DECODER` | `U` at 5.8% of the diagonal slope | −1.9e-04 |

One smoke origin proves nothing about whether they help; it proves the blocks are
wired in and being used, which is the precondition for a null to mean anything.

**A test caught a vacuous test.** The first version of the "a live block changes
the prediction" assertion passed for the wrong reason: the message head is itself
zero-initialised, so nothing upstream of it can move the prediction at init, and
the assertion would have kept passing had the sender block never been wired in at
all. It now wakes the head first, and a companion test proves the extra input
enters *only* through the new block.
