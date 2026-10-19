# Joint capability v7 — donor extremity, and a mechanism that fits

2026-09-11 (Opus + Adam). Run `experiments/cache/joint_capability_2026_09_11_v7/`,
**288/288 arm-origins, 48 origins, 12 seasons, 6,179 cells, 803,447 possessions**,
1,585 s of core time after the resume. Every arm scored on identical cells,
possessions and actuals — verified, not assumed.

## The one-paragraph answer

v6 asked whether the model extrapolates across the observed range and found that
it does. v7 pushed the holdout out to the range that actually matters — withhold
the players whose five-clone lineup sits furthest from anything ever played — and
found **two things v6 could not see.** First, removing the most extreme 2% of
donors makes the model *better*, by −0.0164 ± 0.0077 MAE against its matched
random control, the only contrast in v7 that clears two standard errors. Second,
and cutting the other way, **the composition-distance gradient that v6 reported
absent is present once you go far enough out**: a model that never trained on a
withheld donor disagrees with the full model about that donor's five-clone rating
by 1.64 pts/100, against 0.51 on donors it did train on. v6's "no gradient" was a
statement about how far v6 went, not about the model. Separately, §8.1's overload
response **fits non-zero in 48/48 origins on conversion** and exactly zero on
turnovers — the first mechanism in this workstream to find a real interior value
on one channel and the exact boundary on another.

## Scoreboard

MAE, possession-weighted, 48 origins.

| arm | ALL | donor5 | donor2 | no donor |
|---|---:|---:|---:|---:|
| corrected additive | **8.0343** | **7.7970** | 7.6252 | **8.1648** |
| **V7_HOLDX2** | **8.0565** | **7.8452** | 7.6227 | **8.1727** |
| V7_LOAD | 8.0637 | 7.8613 | **7.6185** | 8.1749 |
| V7_FULL | 8.0663 | 7.8611 | 7.6255 | 8.1791 |
| V7_RANDX2 | 8.0736 | 7.8661 | 7.6375 | 8.1876 |
| V7_RANDX5 | 8.0775 | 7.8901 | 7.6856 | 8.1805 |
| location + shot | 8.0832 | 7.8981 | 7.6243 | 8.1849 |
| V7_HOLDX5 | 8.0969 | 7.9304 | 7.7164 | 8.1884 |
| structural parent | 8.0981 | 7.9046 | 7.6244 | 8.2045 |

`V7_HOLDX2` is the best neural arm on three of four regions and `V7_LOAD` on the
fourth. **The corrected additive still leads on three of four.** On `donor2` —
the cells containing the most extreme players, the regime the tool has to
survive — every serious arm is inside 0.007 MAE of every other, including the
additive, which is a tie and should be read as one.

Two things not in the table. The neural arms carry far less bias: −0.03 to −0.12
pts/100 on ALL against the additive's **−0.484** and the structural parent's
−0.588. And the additive keeps a real edge in rank quality — r² 0.1439 against
`V7_HOLDX2`'s 0.1373, consistent with `ASOF_ADDITIVE_REFERENCE_RESULTS.md`.

## The contrasts

Season-paired, 12 seasons, `k/n` = seasons favouring the first arm. `*` = the
interval excludes zero.

| contrast | ALL | donor5 | donor2 | no donor |
|---|---|---|---|---|
| `HOLDX2 − RANDX2` | **−0.0164 ± 0.0077, 7/12 \*** | −0.0141 ± 0.0130 | −0.0099 ± 0.0214 | −0.0152 ± 0.0103 |
| `HOLDX5 − RANDX5` | +0.0193 ± 0.0221 | +0.0494 ± 0.0265 | +0.0307 ± 0.0340 | +0.0061 ± 0.0228 |
| `HOLDX2 − FULL` | −0.0088 ± 0.0156 | −0.0139 ± 0.0218 | +0.0014 ± 0.0267 | −0.0056 ± 0.0137 |
| `RANDX2 − FULL` | +0.0092 ± 0.0149 | +0.0002 ± 0.0237 | +0.0113 ± 0.0242 | +0.0096 ± 0.0126 |
| `HOLDX5 − FULL` | +0.0285 ± 0.0183 | **+0.0596 ± 0.0216, 2/12 \*** | **+0.0889 ± 0.0355, 2/12 \*** | +0.0067 ± 0.0176 |
| `LOAD − FULL` | −0.0026 ± 0.0025, 8/12 | +0.0011 ± 0.0034 | −0.0050 ± 0.0055 | −0.0042 ± 0.0033 |

Difference-in-differences (donor5 effect minus no-donor effect):

- `HOLDX2` vs `RANDX2`: **+0.0011 ± 0.0178, 6/12** — dead zero.
- `HOLDX5` vs `RANDX5`: +0.0433 ± 0.0222, 3/12.

### What the dose curve says

Removing the top 2% of donors helps; removing the top 5% hurts, and hurts worst
exactly where those donors play (`HOLDX5 − FULL` is +0.0596 on donor5 and +0.0889
on donor2, both 2/12 and both excluding zero). That is a coherent curve and the
second holdout pair was added precisely to find it. Trim a little and you drop
players whose states distort a shared mapping; trim more and you delete the
signal needed to price that archetype at all.

### The correction v7 forces on its own partial result

At 39 origins `HOLDX2 − FULL` read −0.0311 on donor5 and the story looked like
"the model prices donors *better* having never seen them." **That did not
survive.** At 48 the donor5 figure is −0.0139 ± 0.0218 and the
difference-in-differences is +0.0011 ± 0.0178 — indistinguishable from zero.

The surviving claim is narrower and different in kind: `HOLDX2` beats `RANDX2`
by about the same amount in *every* region (−0.0164 ALL, −0.0141 donor5, −0.0152
no-donor). The benefit is **uniform, not extremity-specific**. Removing the most
extreme players improves the shared parameters *everywhere*, including on cells
those players never touch. That is outlier trimming on a shared fit, not
improved extrapolation.

It is also the fourth time in this workstream that less has beaten more, after
width 64, pair pooling and the learned encoder.

**Nothing here is established except two negatives.** `HOLDX2 − RANDX2` clears
two sem pooled but is 7/12 on seasons, which is close to a coin flip; the honest
reading is one suggestive positive and two clean negatives against `HOLDX5`.

### Against the additive

| region | `HOLDX2 − additive` | seasons |
|---|---|---|
| ALL | +0.0222 ± 0.0331 | 4/12 |
| donor5 | +0.0220 ± 0.0615 | 5/12 |
| **donor2** | **−0.0163 ± 0.0919** | 6/12 |
| no donor | +0.0144 ± 0.0525 | 5/12 |

The gap to the additive is **not established in either direction anywhere**, and
on `donor2` the sign flips. This is `BACKLOG` §0's standing calibration restated:
the population resolves ~0.04 MAE and these are ~0.02.

## The mechanism arm

`V7_LOAD` fits three non-negative coefficients, initialised at 0.1, with zero an
exactly attainable boundary:

| coefficient | channel | result across 48 origins |
|---|---|---|
| `k_make_over` | conversion falls when overloaded | **non-zero in 48/48**, mean 0.0709, range 0.0402–0.1108 |
| `k_to_over` | turnovers rise when overloaded | **exactly zero in 47/48** |
| `k_make_under` | conversion when under-used | exactly zero in 42/48 |

Two of three coefficients found the zero boundary and one did not. Adam's weight
decay is 1e-4 over ~560 steps, a shrinkage factor of ~1.0, so the zeros are the
clamp binding against a real negative gradient — not decay from the initial
value. **Give a man more of the offence than he has historically carried and this
model says his shooting gets worse and his turnovers do not move**, which is a
falsifiable basketball claim and the first one this workstream has fitted rather
than asserted.

In points it is worth −0.0026 ± 0.0025 on ALL (8/12 seasons) and −0.0042 ± 0.0033
off the donor cells (8/12). Consistent in sign, an order of magnitude below what
this benchmark resolves. `channel_forecast_vs_points.md` again: a channel that
fits need not be worth points.

## The gradient v6 could not find

Five-clone ladder at 2026q4, all 1,068 players, each scored as five copies of
himself, each arm through its own calibration.

| | mean \|diff\| vs `V7_FULL` | on players it NEVER trained on | on the rest |
|---|---:|---:|---:|
| `V7_HOLDX5` (54 withheld) | 0.570, r = 0.9955 | **1.643** | 0.513 |
| `V7_HOLDX2` (22 withheld) | 0.345, r = 0.9982 | **1.210** | 0.327 |

And the gradient is monotone in composition distance — mean \|diff\| by distance
quartile, then the top 5%:

- `V7_HOLDX5`: 0.434 → 0.457 → 0.454 → 0.757 → **1.643**, slope +0.0616/unit
- `V7_HOLDX2`: 0.203 → 0.254 → 0.291 → 0.524 → **1.056**, slope +0.0512/unit

**This qualifies v6's headline.** v6 reported r = 0.9966 and *no* distance
gradient, and concluded the model extrapolates. Both statements were true of v6's
holdout, where 99.5% of withheld cells sat at or below the real maximum. Pushed
to donors whose clone lineups exceed anything ever played, the correlation still
holds (0.9958 on the never-seen players) but **the level moves by ~1.6 pts/100,
3.2x what it moves on players the model did see.** Correlation was the wrong
statistic: it is insensitive to exactly the level shift that matters for a tool
that prints a number.

1.6 pts/100 is not small in this context. The opponent lever is ~0.9 pts/100 of
lineup spread and shot quality ~0.91.

## The fixture guardrail, corrected

*This section replaces the one first written on 2026-09-11, which read the
guardrail column as a defect. The sign was never checked. It is a feature.*

The standing column, at 2026q4:

| arm | real-lineup max context swing | five-clone max swing | as % of in-range max |
|---|---:|---:|---:|
| `V7_FULL` | 8.094 | 20.614 | 255% |
| `V7_HOLDX2` | 9.322 | 22.626 | 243% |
| `V7_HOLDX5` | 7.601 | 17.952 | 236% |

v3 quoted 226% and v4 192%, and all three versions reported the number as
evidence of instability out of distribution. **The magnitude was measured and the
direction was not.** It is negative:

- The 20 largest-|swing| clone lineups at 2026q4 are **negative 20 of 20**, mean
  **−17.30 pts/100**. Their no-message scores have median 126.94 and max 145.14;
  after the message, 110.12 and 128.68.
- The swing correlates **−0.385** with composition distance: the further out the
  clone, the harder the message pulls it down.
- On **real** lineups the mean swing is **+0.07** and roughly symmetric (6,291 of
  13,054 negative). The correction does not touch the observed range.

**And it is a composition penalty, not score shrinkage.** Regressing the clone
swing on both the no-message score and composition distance gives partial
correlations of −0.408 and −0.412 — equal, and nearly orthogonal (R² 0.145 and
0.148 separately, 0.290 together). The decisive slice holds the score fixed:
among clones in the p40–p60 band of no-message score, the far half by distance
gets a swing of −1.97 against −0.03 for the near half.

Across eight origins spanning 2016–2026, at matched score:

| | mean |
|---|---:|
| far-minus-near swing | **−3.004 ± 0.432, negative 8/8** |
| partial r on distance, score held | **−0.447, negative 8/8** |
| CONTROL: mean swing on real lineups | **+0.196** |

**The model has learned a duplication penalty from data.** It leaves real lineups
alone and pulls repeated-player lineups down in proportion to how far their
composition sits from anything real. That is what `tool/five.html` currently does
by assertion, and what four fitted attempts failed to do — `distance_shrink.py`,
floor geometry, index curvature, defensive coverage.

**Why this one escapes selection-on-the-outcome.** `selection_on_the_outcome.md`
records that every fitted structure extrapolates the wrong way, because a coach
fields an unusual five only when it works, so in range "unusual" correlates with
"good" and every fit inherits that sign. This fit inherits the **opposite** sign.
The message is not fitted on lineup points; it is fitted on five event-level
families per player — who shoots, from where, and whether it goes in. Five
rim-only players genuinely cannot all shoot at the rim, and that constraint is
visible in event data without any lineup outcome being consulted. The selection
bias pushes the other way and the effect survives it, which makes the evidence
stronger rather than weaker.

**What is NOT shown.** That the magnitude is *calibrated*. The direction is
established 8/8 and the size is not checked against anything. Five copies of the
best player still print 132.43 pts/100, 106.6% of the model's own in-range
maximum, and whether that is right is unknown. Calibrating it is a v8 question.

## Process: two things worked

**The matching gate became a measurement, mid-run.** `assert_matched` aborted the
sweep after origin 39 of 48 because one pair-origin landed at 3.22% against a 3%
threshold. Replaced with `match_quality`, which records the signed gap. Final
distribution over 48 origins: `HOLDX5` median 0.94% / p90 1.17% / max 3.22%, one
flagged; `HOLDX2` median 0.84% / p90 0.98% / max 2.75%, none flagged.

Every contrast was re-read with 2024q3 dropped, as promised: **the headline moves
from −0.0164 ± 0.0077 to −0.0164 ± 0.0076.** Nothing in v7 rides on the badly
matched origin. The resume was verified bit-exact first — saved masks re-derive
with 0 mismatches across 108 field comparisons at 2015q1, 2019q2 and 2024q3.

**The epoch cap is resolved.** Adam noticed v6 runs reaching the 24-epoch limit.
v7 raised it to 48. Across 288 arm-origins the selected epoch has median 12,
maximum **30**, with **0 at the cap** and 3 above 24. The cap is no longer
binding and can be left where it is.

## What I would take from this

1. **`V7_HOLDX2` is not a shippable configuration.** It wins by removing 21
   players — including Gobert, Capela and Zubac — from training, and a tool has
   to price those players. What it identifies is a *defect*: extreme donor states
   distort a shared mapping. The fix is a better-conditioned objective, not a
   smaller training set. `BACKLOG` §0ag Part A is the first candidate, since the
   message penalty's units currently spend the budget on conversion and starve
   location.
2. **The gradient result reopens uncertainty as the live problem.** The model's
   disagreement with itself grows with composition distance at ~0.05–0.06 pts/100
   per unit, reaching 1.6 at the donors that matter. That is a *measured*
   quantity with dynamic range — exactly what `distance_shrink.py` could not fit
   and what the coverage gate currently asserts. Applying it to the intervals has
   been carried since v5 and is now the item with the best evidence behind it.
3. **The overload response is worth keeping as a mechanism, not as accuracy.**
   48/48 on conversion and 47/48 exact zeros on turnovers is a clean readout.
4. **The fixture swing is a learned duplication penalty, not a defect** — and
   it is the first data-derived candidate to replace the asserted coverage gate.
   Direction established 8/8 origins; magnitude unchecked. This is the second
   northstar-facing result v7 produced and neither was what v7 set out to find.

## Verification

- 288/288 arm-origins; `completion_status.json` `core_complete`.
- Every arm joined one-to-one on identical cells: possessions equal, actuals and
  saved additive equal to 1e-9.
- Match quality recorded for all 48 origins; every contrast reported with and
  without the flagged origin.
- `assert_unseen` held on every `HOLDX` arm-origin: no withheld donor survived in
  any training row.
- 697 tests pass. No scorer promotion, no page change, no database mutation, no
  completed run directory touched.
