# v8 Phase 0 — no fits

2026-09-11 (Opus + Adam). Analysis of the 288 arm-origins v7 already produced.
No model was trained, no database mutated, no completed run directory touched.

---

## P0.1 — the ensemble interval is a NULL, and the null is precisely located

**Pre-registered to stop here.** The plan said: *"Does spread order error? … If it
is flat, stop and report a null — this is the same shape
`per_lineup_error_bars_null.md` already died on, and it must be allowed to die
again."* It is flat. Test 3 was not run.

### Test 1 — does population disagreement order the error? No.

v7's six arms per origin share a seed and differ only in training population, so
their disagreement is population uncertainty. Headline on the matched pairs
(`|HOLDX2 − RANDX2|` and `|HOLDX5 − RANDX5|`), each comparing two models that
dropped the same count and footprint and differ only in *which* players.

| measure | weighted corr with \|error\| |
|---|---:|
| `spread_matched` | **−0.0102** |
| `gap_holdx2` | −0.0008 |
| `gap_holdx5` | −0.0126 |

The decile table is flat and non-monotone: 7.99, 8.25, 8.52, 8.29, 7.69, 8.34,
7.98, 7.65, 7.74, 8.24 pts/100 across deciles of spread.

By slice — *looked at after the pooled null, and reported in full for that
reason*: ALL −0.0102, donor5 −0.0025, donor2 −0.0094, no-donor −0.0116, novel
−0.0260. Nothing anywhere.

### Test 2 — does the spread measure what we think? **Yes.**

This is what makes the null informative rather than merely disappointing.

| composition-distance band | mean distance | mean spread | mean \|error\| |
|---|---:|---:|---:|
| 1 | 5.08 | 0.414 | 8.19 |
| 2 | 5.69 | 0.474 | 7.66 |
| 3 | 6.10 | 0.470 | 7.96 |
| 4 | 6.56 | 0.508 | 8.26 |
| 5 | 7.62 | 0.531 | 8.30 |

`corr(spread_matched, composition_distance) = +0.1526`, monotone in the bands.
**The ensemble spread is a genuine composition-extremity measure.**

### The diagnosis

Composition distance itself does not order forward error on this population:
`corr(composition_distance, |error|) = +0.0093`, deciles 8.246 → 7.971. And on
the quantity the v4 interval protocol actually models, `|error|·√n`, both are
equally dead — distance **+0.0073** (quintiles 98.9 → 100.0 → 96.2 → 97.9 →
102.3) and spread **−0.0150** (102.2 → 101.4 → 98.9 → 95.2 → 97.8).

**The measure works; the target does not exist here.** No composition-based
interval can succeed on this population, however well composition is measured.
This is `distance_shrink.py`'s finding and `per_lineup_error_bars_null.md`'s
finding reached a **third** independent way, with a new measure and a new method.

### The limit that keeps the question open

Real evaluation cells span composition distance roughly **5.1 to 7.6** by band
mean. Five-clone lineups sit at a median of **10.9** and the withheld donors at
**22–26**. So this null is established over a narrow in-range band where there is
no room for the effect to appear, exactly `composition_extrapolation.md`'s point.
**It does not say a distance-aware interval is wrong out of support. It says this
population cannot answer that**, and therefore that any widening must be derived
from something other than forward error on real lineups — which is precisely what
P0.2 is about.

---

## P0.2 — the two duplication rules agree on SIZE and disagree on WHO

A comparison of two rules, not a validation: no ground truth exists for a lineup
that never played. Fixtures are five copies of one player, priced at 2024q3.
The comparable quantity is each rule's **discount** — the same lineup, same
model, rule off versus rule on.

| five copies of | clone distance | tool gated | ungated | **gate discount** | NN with msg | no msg | **NN discount** |
|---|---:|---:|---:|---:|---:|---:|---:|
| Jokić | 13.70 | 7.83 | 17.61 | **−9.77** | 128.21 | 124.63 | **+3.58** |
| Curry | 13.14 | 10.12 | 22.76 | **−12.63** | 130.79 | 123.42 | **+7.37** |
| LeBron | 11.72 | 10.40 | 23.38 | **−12.98** | 122.97 | 119.29 | **+3.67** |
| Gobert | 23.39 | 0.58 | 1.29 | −0.72 | 117.54 | 128.28 | **−10.74** |
| Whiteside | 23.40 | −0.10 | −0.22 | +0.12 | 110.99 | 123.18 | **−12.19** |
| Zubac | 24.49 | −2.54 | −5.70 | **+3.16** | 114.06 | 125.94 | **−11.88** |
| Capela | 26.22 | −0.16 | −0.35 | +0.19 | 112.50 | 126.02 | **−13.51** |

**Mean discount: gate −4.66, model −4.82.** The two rules agree almost exactly on
how much a five-clone lineup should lose on average, which is not a trivial
agreement — one is asserted from a percentile target, the other fitted on
event-level losses that never saw a lineup outcome.

**Correlation of the two discounts across fixtures: −0.971.** They are nearly
perfectly anti-ordered on *which* lineup should lose it.

### Why, mechanically

The gate's multiplier is **0.4449 for every five-clone lineup**, with diversity
exactly 0.0000 in all seven. It is doing precisely what it was designed to do:
treat all repetition identically. But it is **multiplicative**, so its effect in
pts/100 is `score × (multiplier − 1)` and therefore scales with the lineup's own
quality. Five Currys ungated is +22.76 and loses 12.63; five Zubacs ungated is
−5.70 and **gains 3.16**, because shrinking a negative toward zero is a boost.

The model's penalty is additive and keyed on composition, so it falls on the
composition-extreme lineups — the non-shooting centres at distance 23–26 — and
leaves the stars, who sit near the median distance of 10.9, slightly raised.

### What this means

**The gate cannot tell five Capelas from five Jokićs.** Both get multiplier
0.4449; in the units the page prints, the gate punishes the good clone lineup by
12.98 and *rewards* the bad one by 3.16. A lineup of five non-shooting centres
that cannot space the floor or create a shot is the clearest case in basketball
for a composition penalty, and the incumbent rule gives it a bonus.

That is a defect in the incumbent that the learned rule does not have, and it is
new information: `tool_breaks_on_repetition.md` established that the failure is
repetition rather than excellence, and this shows the *fix* is still keyed to
excellence in absolute terms.

**What is NOT shown:** that the model's magnitudes are right. Five Jokićs gaining
+3.58 from the message is not obviously correct, and nothing here can adjudicate
it. The honest summary is that the two rules bracket the problem — one sizes the
average penalty about right and assigns it wrongly, the other assigns it
plausibly with unvalidated sizes.

---

## A correction to §0ag, made while running P0.2

The first version of `BACKLOG.md` §0ag Part A reported mean |z| as "Gobert 1.26,
Jokić 1.12, Curry 1.07" using player ids 1308 and 1051. **Those ids are Steven
Adams and Ish Smith.** Jokić is 1458 and Curry is 1022.

Corrected: **Gobert 1.26, Jokić 1.48, Curry 1.31, Capela 1.15.** Across all 1,035
players, corr(mean |z|, clone distance) = **+0.6393** and corr(max |z|, clone
distance) = **+0.8349** — so the original claim that "a per-coordinate transform
would not have flagged him" was **wrong**, and is retracted. Marginal extremity
is a fair global proxy.

What survives, and is the point worth keeping: **the top-21 sets overlap in only
6 of 21.** The tail is the only place withholding operates, and there the two
measures pick largely different players — Jokić has the highest marginal
extremity of the six named players and the 84th percentile of clone distance;
Capela has the lowest and the 99.4th.

---

## P0.3 — not yet run

The `V7_SHOT` double-counting diagnostic is still outstanding.

---

## Build verification, 2026-09-11

`V8_BASE` reproduces `V7_FULL` **bit-identically** at 2015q1 — every metric, every
event family, and the selected epoch:

| | `V7_FULL` | `V8_BASE` | difference |
|---|---:|---:|---:|
| MAE | 7.6724956 | 7.6724956 | **0.00e+00** |
| RMSE | 10.1359836 | 10.1359836 | **0.00e+00** |
| raw r² | 0.1099305 | 0.1099305 | **0.00e+00** |
| event loss | 1.0188942 | 1.0188942 | **0.00e+00** |
| selected epoch | 14 | 14 | — |
| conversion / location / counts / free_throw / assisted | — | — | **all 0.00e+00** |

So the shared baseline, the rewritten accumulator and the new weight path change
nothing at the base arm, and every other arm's difference from it is the declared
factor and nothing else.

**`V8_SCALE` moves the message where it was designed to**, visible on the first
origin. Achieved message in units of each coordinate's own spread:

| arm | counts | location | make |
|---|---:|---:|---:|
| `V8_BASE` | 0.195 | **0.087** | **0.491** |
| `V8_SCALE` | 0.209 | **0.106** (+22%) | **0.402** (−18%) |

The penalty's units were the diagnosis in `BACKLOG` §0ag Part A and the arm
responds as that diagnosis predicts. Whether it *helps* is what the run measures.

**The trim was reparameterised twice before it was right**, both times caught by
sizing rather than by a fit:

1. `w = 1/(1 + (e/d0)²)` with `d0` from the PLAYER quantile removed **34.5% of
   the training weight at a p90/p10 discrimination of 1.61x** — overwhelmingly a
   uniform down-weight, which a weight-normalised objective ignores.
2. A fixed scale from the row-extremity tail removed **1.1–1.6%** against v7's
   13.3% — 10x too weak to be a comparable arm.
3. The shipped form solves the scale per origin so the arm removes **exactly the
   share of training weight v7's matching hard arm removed**: 13.20% for
   `V8_TRIM2` and 28.60% for `V8_TRIM5` at every origin tested, spread smoothly
   over the top 26% / 57% of rows, with everything below the threshold at exactly
   weight 1.
