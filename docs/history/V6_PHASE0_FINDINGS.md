# v6 Phase 0: the support measure, the clone ladder, and the strata

2026-09-11, Claude Opus 5 with Adam. No fits. Everything below ran inside
`no_database()`; no run directory, scorer or page was touched. New code:
`experiments/joint_capability_v6_support.py`, 8 tests, 666 in the suite.

Phase 0 changed two things I had written into the v6 plan and confirmed the
third. It also produced a result that reframes what v4 and v5 claimed about
degenerate lineups.

---

## P0.1 — the support measure. PASSES, after two corrections to my own test.

The v3–v5 measure is `sqrt(mean(((v − μ)/σ)²))` over the 36-dim vector
`[mean over the five of base, sd over the five of base]`. An RMS over 36
coordinates averages extremes away, which is why five Goberts scored 3.191
against a real maximum of 3.105.

**The 36-dim vector is rank 31, and the five missing directions are exact
accounting identities, not noise.** Condition number 4.3e16, with exactly five
numerically-zero eigenvalues, accounted for one for one:

| identity | directions |
|---|---:|
| the six centered location logits sum to zero, so their mean does too | 1 |
| the four two-point make coordinates are one shrunk offset broadcast over the league curve, so their spread across five players is identical | 3 |
| likewise the two three-point make coordinates | 1 |

Dropping them **by name** leaves a full-rank 31-dim problem
(`feedback_rank_deficient_control.md`); a numerical eigenvalue floor would have
hidden the reason. Note the means are *not* collinear even though the spreads
are, because the league curve moves over the corpus — the pairwise gap has sd
6.5e-2. A first version of my unit-test fixture froze that curve, was therefore
*more* degenerate than reality, and demanded the module drop coordinates it must
keep. The fixture was wrong, not the module.

**Two corrections to my first acceptance test, both of which mattered.**

1. **The "real maximum" was a thin-history artifact.** 9.5% of training rows
   contain a player with zero effective exposure anywhere; those rows carry the
   entire tail. Real maximum including them 15.50; **excluding them, 10.31.**
   A support measure calibrated against a contaminated tail understates how far
   out a synthetic lineup really is.
2. **The clone ladder needs extreme donors.** Five copies of a *median* player
   is a plausible lineup and should not score as far out.

With both fixed, five copies of one well-exposed player, against the real
maximum of 10.31:

| donor | five-clone distance | × real maximum |
|---|---:|---:|
| median player | 10.66 | 1.03 |
| p90 player | 13.44 | 1.30 |
| **p99 player** | **18.69** | **1.81** |
| most extreme | 31.11 | 3.02 |

**1.81× at a p99 donor is exactly the scale the old profile measure had** —
`composition_extrapolation.md` put real fives at 4–11.5 and five Shaqs at 20.9,
roughly 1.8×. The legacy measure gives 1.03× on the same comparison. The
dynamic range is restored.

---

## P0.2 — the clone ladder. The reframing result.

The additive's duplication curve is *exactly linear*
(`tool_breaks_on_repetition.md`), which is why five copies of a star price above
anything ever played. Does `E0M` bend? Scored through the model's own scorer on
the v5 `BASE` checkpoint at 2026q1, 1,500 well-exposed donors.

**On average the curve is linear too.** Deviation from the straight line through
rungs 1 and 5: +0.107, +0.184, +0.020 points/100 at rungs 2, 3 and 4.

**Per donor there is real curvature, but its sign is a coin flip.** Midpoint
deviation has |mean| 1.383 and sd 1.730 against a signed mean of **+0.002**;
**50.5%** bend down. Median curvature is 24% of the total 1→5 move. The total
move itself is mean +0.40 with sd 7.65 and 45% of donors going down — so
direction is donor-specific, which is the good news: this is not "unusual is
bad".

**The model does not bend more once it leaves the support.** Mean |curvature|
is 1.285 inside, 1.456 at 1.0–1.5×, 1.263 beyond 1.5×;
`corr(distance beyond support, |curvature|) = −0.016`.

**And roughly half the clone response survives zeroing the message.** Zeroing
the message head at inference — a decomposition of this model's behaviour, not a
substitute for a refitted control — leaves the 1→5 move at mean +0.66/sd 6.82
against +0.40/sd 7.68 with it on, correlated **+0.500**, and widens the spread of
five-clone levels by only **1.16×**.

**What this means.** `E0M`'s sane behaviour on degenerate lineups comes
substantially from the **shared finite budget** — five players competing for one
prefix-estimated `U`, accounting asserted by construction — and not from a
learned redundancy penalty. There is no systematic penalty: the response is
linear in the number of copies, donor-specific in direction, and no different in
character outside the support than inside it.

So v4's framing, repeated in v5, that *"mean pooling supplies the missing
creation/fit penalty without a player-specific rule"* **overstates it.** Mean
pooling modulates; the budget does at least as much work.

This is not bad news for the programme. A bound that comes from fixed accounting
cannot inherit selection bias, which is precisely the objection
`selection_on_the_outcome.md` raises against every fitted schedule. But it does
mean the fixture numbers describe *a player's own profile replicated under a
fixed budget*, and should be described that way.

It also sharpens the v6 hypothesis: a model whose out-of-support behaviour is a
smooth continuation of its in-support function should lose relatively little when
the unusual region is withheld from training. **HOLD ≈ RAND is now the prior, not
a hope** — which makes the experiment a test of a stated prediction rather than a
fishing trip.

---

## P0.3 — the strata. v6 is well powered.

Composition distance computed per origin from the training prefix only, so the
threshold is prefix-only and refit inside each split (CLAUDE.md rule 9). The p75
threshold is stable across the corpus — 5.97, 5.93, 5.92, 5.86 at 2016q1,
2020q1, 2023q1, 2026q1 over ~172k–187k training rows each.

**The evaluation population is far more unusual than the training population.**
Of the 5,179 decision cells:

| | cells | possessions |
|---|---:|---:|
| total | 5,179 | 675,434 |
| **above the training p75** | **2,473 (47.8%)** | **314,975 (46.6%)** |
| of those, novel | 923 | — |

Withholding the top quartile of *training rows* leaves **47.8% of evaluation
cells** in the withheld region, because the benchmark scores recurring five-man
units and those are systematically more distinctive than the average
game-lineup row. The primary contrast has roughly 315k possessions of exposure,
which is ample.

---

## Consequences for the v6 plan

- **P0.1 passes**, with the support measure rebuilt and the real maximum
  redefined to exclude zero-exposure rows. Downstream interval work should use
  the well-exposed maximum of 10.31, not 15.50.
- **P0.2 changes the framing, not the design.** The claim under test in Phase 1
  is unchanged, but its prior is now explicit and the write-up must stop
  attributing the clone behaviour to a learned penalty.
- **P0.3 confirms power** and fixes the strata definition.
- One addition to Phase 1: because roughly half the clone response is the budget
  rather than the message, the holdout arms should also be scored with the
  message zeroed, so the degradation can be attributed to the learned part
  rather than to the accounting that every arm shares.
