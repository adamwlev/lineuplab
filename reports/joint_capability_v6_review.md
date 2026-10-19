# Joint capability v6: does it extrapolate, or interpolate?

2026-09-11, Claude Opus 5 with Adam. Run
`experiments/cache/joint_capability_2026_09_11_v6/`. 240 arm-origins (5 arms ×
48 origins), all verified — required files present, cell counts matching
`complete.json`, every checkpoint loading, no non-finite prediction. 7,070 s of
fitting. Preflight ran under `no_database()` and wrote `reproduce.json`. 680
tests pass. No scorer or page promoted.

## Bottom line

**Withholding the unusual quartile of lineups from training costs nothing.**

A model trained only on the 75% most typical lineups prices the unusual ones as
well as a model trained on everything — including in the region it never saw.
The clone response is essentially unchanged: five-clone ratings correlate
**r = 0.9966** between the held-out model and the full one.

So this architecture's behaviour on unusual fives does not come from having seen
similar fives. It comes from the player states and the fixed accounting. **The
selection-on-the-outcome objection, which is why the tool's coverage gate is
asserted rather than fitted, does not appear to bind a model with no lineup,
pair or identity parameters.**

**The limit of the claim, stated up front:** 99.5% of the withheld cells sit at
or below the clean real maximum composition distance. v6 validates extrapolation
**across the observed range, not beyond it.** Five copies of a p99 player sit at
1.81× that maximum and remain untested.

## 1. The design

Architecture frozen at v5's `E0M` backbone — mean pooling, no encoder, λ = .01,
γ = .01, seed 17. **The factor is the training population.** `V6_FULL`
reproduces v5 `BASE` **bit-identically** (native and calibrated predictions
identical on every shared origin, max difference exactly 0.0), so every contrast
is one factor off the v5 backbone rather than a re-implementation of it.

Composition distance is Mahalanobis on the identity-free 31-dim composition
vector (Phase 0), fitted per origin on that origin's training prefix alone.

| arm | trains on |
|---|---|
| V6_FULL | everything |
| V6_HOLD75 | composition distance below the prefix p75 |
| V6_RAND75 | a matched random 75% |
| V6_HOLD50 | below the prefix p50 |
| V6_RAND50 | a matched random 50% |

The RAND partners are the load-bearing control and took three attempts.
Matching possessions alone left the random arm with 4% more *distinct* lineups —
more composition diversity, a confound pointing toward the conclusion I expected
— because the rows a HOLD arm drops are smaller than average. Stratifying on the
exact possession count matches rows exactly and possessions to 0.05%, and
`assert_matched` raises rather than trusting the sampler.

Decision sample: 5,607 cells, 726,364 possessions, 11 seasons, of which **2,596
cells (46.3%) fall in the withheld region** — far more than the 25% of training
rows removed, because the benchmark scores recurring five-man units and those
are systematically more distinctive than the average game-lineup row.

## 2. Results

### Levels (MAE, decision sample)

| arm | all | withheld | inside | novel |
|---|---:|---:|---:|---:|
| corrected additive | **8.0920** | 8.3454 | **7.8833** | 8.9039 |
| **V6_HOLD75** | **8.1199** | **8.3164** | 7.9581 | 8.8781 |
| V6_FULL | 8.1224 | 8.3342 | 7.9479 | **8.8575** |
| V6_RAND50 | 8.1308 | 8.3391 | 7.9592 | 8.8736 |
| V6_HOLD50 | 8.1322 | 8.3536 | 7.9498 | 8.9224 |
| V6_RAND75 | 8.1381 | 8.3357 | 7.9754 | 8.9143 |

**`V6_HOLD75` has the best withheld-region MAE of the five arms — better than
the model that trained on everything.**

### The primary contrast, pre-registered

Season-paired over 11 seasons, mean ± sem with a 95% t interval. Negative means
the first arm is better.

    WITHHELD region
      HOLD75 - RAND75   -0.0050 +- 0.0288  [-0.0702,+0.0601]   5/11
      HOLD50 - RAND50   +0.0189 +- 0.0234  [-0.0340,+0.0718]   5/11
      HOLD75 - FULL     -0.0079 +- 0.0202  [-0.0536,+0.0377]   6/11
      HOLD50 - FULL     +0.0210 +- 0.0139  [-0.0105,+0.0524]   5/11

    inside the p75 support
      HOLD75 - RAND75   -0.0241 +- 0.0232  [-0.0766,+0.0283]   7/11
      RAND75 - FULL     +0.0267 +- 0.0160  [-0.0095,+0.0629]   2/11

    all cells
      HOLD75 - RAND75   -0.0133 +- 0.0243  [-0.0682,+0.0416]   5/11
      HOLD75 - FULL     -0.0011 +- 0.0202  [-0.0468,+0.0445]   5/11

Nothing is established — every interval crosses zero — but every point estimate
points the same way: **the composition holdout is free at 75%.** `HOLD75` is
within 0.001 MAE of `FULL` on all cells while training on a quarter less data,
and is 0.008 *better* in the region it never saw.

At 50% a cost begins to appear: `HOLD50 − FULL` in the withheld region is
+0.0210 ± 0.0139 at 5/11. A dose–response in the expected direction, still
inside noise.

### The right statistic, and a correction to my own reasoning

I told Adam mid-run that the sanity check was `HOLD − RAND` inside the support
being ≈ 0. **That was wrong.** `HOLD75` trains *exclusively* on inside-support
lineups, so it should be better there — it is a specialist, and it is (−0.0241).
That is expected specialisation, not a broken control.

The clean statistic nets it out — how much worse is HOLD in the region it never
saw, relative to the advantage it earns where it trained?

    (HOLD75 - RAND75 | withheld) - (HOLD75 - RAND75 | inside)
      = +0.0191 +- 0.0138  [-0.0121,+0.0503]   7/11 seasons
    HOLD50 vs RAND50
      = +0.0058 +- 0.0261  [-0.0532,+0.0647]   5/11

Positive means HOLD pays something out there. At 1.4 sem it is a hint, not a
finding, and it is the only number in v6 that leans against the headline. It
rests on the assumption that the specialisation advantage would have carried
into the withheld region.

### No gradient with distance

`HOLD75 − RAND75` by decile of cell composition distance shows no trend:
−0.046, +0.013, −0.026, −0.016, −0.018, −0.044, −0.032, −0.032, +0.065, −0.049.
If the model were interpolating from neighbours, the penalty should grow as
cells move away from what it trained on. It does not.

### The clone response is invariant to the holdout

1,200 donors at 2026q1, scored through each arm's own checkpoint:

| arm | 1→5 move | % down | five-clone level | r with FULL | mean gap |
|---|---:|---:|---:|---:|---:|
| V6_FULL | +0.49 | 44% | 115.79 | 1.0000 | — |
| V6_HOLD75 | +0.40 | 45% | 116.38 | **0.9966** | +0.60 |
| V6_RAND75 | +0.51 | 45% | 115.61 | 0.9990 | −0.17 |
| V6_HOLD50 | +0.52 | 42% | 115.81 | 0.9874 | +0.03 |
| V6_RAND50 | +0.41 | 44% | 115.34 | 0.9962 | −0.44 |

A model that never saw the unusual quartile produces nearly the identical
five-clone rating, donor by donor. The residual disagreement — HOLD75 at 0.9966
against RAND75's 0.9990 — is a real composition-specific effect and it is worth
about 0.7 pts/100 on ratings of ~116.

## 3. What this does and does not establish

**Does.** Within the observed range of NBA lineup composition, this model's
pricing of unusual fives does not depend on having trained on unusual fives.
Remove them and both the point predictions and the clone response survive. That
is the first direct evidence in this repository that an identity-free
architecture escapes the selection-on-the-outcome trap that
`distance_shrink.py` and four fitted composition blocks ran into.

**Does not.** The withheld region reaches a median composition distance of 6.44
and a p95 of 7.78, against a clean real maximum of 10.31 — **99.5% of it sits
at or below that maximum.** The degenerate fixtures the tool actually has to
survive are further out: five copies of a median player 1.03×, of a p99 player
**1.81×**, of the most extreme donor **3.02×**. v6 says the model extrapolates
across the range we can check. It says nothing about 1.8×, and
`composition_extrapolation.md` is explicit that a composition result without its
range is not a result.

Nor is anything here statistically established. Every interval crosses zero.
What v6 has is six point estimates pointing the same way, a clean dose–response,
a flat distance gradient, and a clone correlation of 0.9966.

## 4. Verification

- 240/240 arm-origins verified; identical cell counts across arms; one-to-one
  join against the frozen benchmark cells.
- `V6_FULL` reproduces v5 `BASE` **bit-identically** — native and calibrated
  predictions identical on every shared origin, max difference exactly 0.0,
  pooled MAE agreeing to eight decimals. Stronger than the v5↔v4 parity check
  (3.8e-5), because v6 passes the state array through unchanged where v5
  concatenated it and took a different BLAS path.
- HOLD/RAND exposure matching asserted every origin; rows exact, possessions
  within 0.05%.
- The withheld region is a property of the **cell**, computed from the full
  training prefix, so it is identical across arms — a defect caught in the
  smoke, where the random control had an empty region to be compared in.
- Preflight under `no_database()`; `reproduce.json` written; producing code all
  tracked.

## 5. Decision and what follows

Keep `V6_FULL`/v5 `BASE` as the structural research backbone; corrected additive
remains the predictive baseline; no scorer promoted.

**The northstar consequence is the interesting one.** The tool's coverage gate is
asserted because `selection_on_the_outcome.md` argued no fitted structure can
supply it. v6 is the first evidence that the argument does not bind an
identity-free model. That does not license replacing the gate — the range that
matters is 1.8× and v6 checked 1.0× — but it changes the question from *"can
this ever be derived?"* to *"how far out does it hold?"*, which is answerable.

The obvious v7: push the holdout further out. Withhold by *donor extremity*
rather than by lineup quantile — train without ever seeing the players whose
five-copy lineups sit furthest out, then price those clones. That reaches the
1.8× regime with real labels for the players, if not for the clone lineups
themselves, and it is the same machinery.
