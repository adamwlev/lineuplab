# Joint capability v8 — the inputs were never standardised, and it matters

2026-09-12 (Opus + Adam). Run `experiments/cache/joint_capability_2026_09_11_v8/`,
**336/336 arm-origins**, 48 origins, 12 seasons, 6,179 cells, 803,447 possessions,
9,828 s. Zero errors, no resume needed.

## The one-paragraph answer

v8 froze the architecture again and made the **objective's conditioning** the
factor, on a measurement built for the purpose. The result is a genuine, large,
unanimous improvement to what the model is trained on, and it buys nothing in
points. **`V8_STD` — standardising the message network's inputs and nothing else
— improves the event objective in 47 of 48 origins and 12 of 12 seasons, on every
one of the five families**, including conversion, which had not moved in seven
versions. In points it is +0.0125 ± 0.0233, fifth of seven arms. `V8_SCALE`
confirmed its diagnosis exactly — the message budget moved from conversion to
location as predicted — and the reallocation is worth nothing. And the one
accuracy lead v7 produced **did not survive**: with the footprint matched to
13.20%, a continuous extremity trim is worse than the base arm on both readouts.

## The measurement, which was the point of building v8

v7 normalised every event family by the untrained model on **that arm's own**
training rows, so an arm that reweights moves its own denominator; at 2024q3 the
artifact was 3.5x the effect. v8 computes one baseline per origin and hands it to
every arm. Verified across all 336 arm-origins: the **worst relative difference
between any arm's baseline and `V8_BASE`'s is 0.00e+00**, against v7's 1.7–3.0%.

`V8_BASE` reproduces `V7_FULL` bit-identically — MAE, RMSE, r², event loss, all
five families, and the selected epoch.

## Points — nothing is established

| arm | MAE | RMSE | raw r² | bias |
|---|---:|---:|---:|---:|
| corrected additive | **8.0343** | 10.7600 | 0.1439 | −0.4842 |
| `V8_HL365` | 8.0633 | 10.8013 | 0.1373 | −0.0927 |
| `V8_TRIM5` | 8.0661 | 10.8094 | 0.1360 | −0.0037 |
| **`V8_BASE`** | 8.0663 | 10.8041 | 0.1368 | −0.1073 |
| `V8_SCALE` | 8.0725 | 10.8041 | 0.1368 | −0.0912 |
| `V8_TRIM2` | 8.0787 | 10.8185 | 0.1345 | −0.1401 |
| `V8_FLAT` | 8.0828 | 10.8100 | 0.1359 | −0.0562 |
| location + shot | 8.0832 | 10.8318 | 0.1324 | −0.3807 |
| `V8_STD` | 8.0837 | 10.8050 | 0.1367 | −0.1531 |
| structural parent | 8.0981 | 10.8594 | 0.1280 | −0.5884 |

Season-paired against `V8_BASE`, 12 seasons — **no arm clears two standard
errors in either direction**:

| arm | MAE vs BASE | seasons |
|---|---|---|
| `V8_HL365` | −0.0033 ± 0.0117 | 7/12 |
| `V8_TRIM5` | −0.0025 ± 0.0164 | 7/12 |
| `V8_SCALE` | +0.0060 ± 0.0037 | 5/12 |
| `V8_TRIM2` | +0.0117 ± 0.0082 | 4/12 |
| `V8_STD` | +0.0125 ± 0.0233 | 5/12 |
| `V8_FLAT` | +0.0143 ± 0.0207 | 7/12 |

The corrected additive still leads: `V8_BASE − additive` = +0.0310 ± 0.0436,
4/12. Not established, and unchanged from v7.

## Event loss — this is where v8 has something to say

Shared baseline, so these are comparable for the first time. `*` = interval
excludes zero; negative is better.

| arm | event loss | conversion | location | counts |
|---|---|---|---|---|
| **`V8_STD`** | **−4.12e-04 ± 4e-05, 12/12 \*** | **−1.39e-04, 12/12 \*** | **−7.35e-04, 12/12 \*** | **−2.06e-04, 12/12 \*** |
| `V8_FLAT` | −6.98e-06 ± 4e-05, 7/12 | −2.69e-06, 7/12 | +1.53e-05, 6/12 | −3.43e-05, 7/12 |
| `V8_SCALE` | +1.21e-05 ± 2e-05, 8/12 | +3.40e-05, **0/12 \*** | **−6.13e-05, 10/12 \*** | +7.52e-06, 4/12 |
| `V8_TRIM2` | +8.17e-05 ± 2e-05, 1/12 \* | +4.71e-05, 1/12 \* | +3.47e-05, 6/12 | +5.04e-05, 2/12 \* |
| `V8_TRIM5` | +1.06e-04 ± 2e-05, 0/12 \* | +7.34e-05, 1/12 \* | +1.29e-04, 2/12 \* | +7.99e-05, 1/12 \* |
| `V8_HL365` | +1.06e-04 ± 3e-05, 1/12 \* | +1.03e-04, **0/12 \*** | +9.29e-05, 5/12 | +5.50e-05, 3/12 \* |

### `V8_STD` is the finding

**Negative in 47 of 48 origins** (median −3.66e-04, min −1.08e-03, max +8.51e-05),
12/12 seasons, and every family moves the same way. About 10 sem.

The change is one line in what the message network reads. The 18 coordinates have
means from −3.663 to +1.307 and sds spanning 9.7x, and they went into
`Linear(36, 32)` raw. `V8_STD` feeds `(base − mean)/sd` to the message only; the
skip path keeps raw `base`, so the decoder, the shared budget and the point
identity are untouched. The achieved message grows everywhere — counts
0.1945 → 0.2268, location 0.1052 → 0.1281, make 0.4809 → 0.6040 — and the model
gets better at all five families at once.

**Conversion moved.** It had not in seven versions, and `V7_SHOT` made it worse.
It moves here, 12/12, because the network could finally read its inputs.

Scale, honestly: `V8_BASE`'s event loss is 0.997119 with a between-origin sd of
0.010657, so −4.12e-04 is **3.9% of that spread**. The effect is modest in size
and extraordinary in consistency.

**And it is worth nothing in points** — +0.0125 ± 0.0233, 5/12, with RMSE and r²
indistinguishable from `V8_BASE` (10.8050 vs 10.8041; 0.1367 vs 0.1368). This is
`channel_forecast_vs_points.md` in its purest form yet: a large, unanimous
improvement to the training objective that the point benchmark cannot see.

### `V8_SCALE` — the diagnosis was right and the fix is worth nothing

`BACKLOG` §0ag Part A said `lambda_network` prices the message in raw coordinate
units, so one sd of effect costs `sd_j²` — a 93x spread — and predicted the
budget would move if the units were fixed. It moved, exactly as predicted:

| arm | counts | location | make |
|---|---:|---:|---:|
| `V8_BASE` | 0.1945 | 0.1052 | 0.4809 |
| `V8_SCALE` | 0.2065 | **0.1251** | **0.4046** |

And the families follow the reallocation: **location −6.13e-05 (10/12 \*)**,
**conversion +3.40e-05 (0/12 \*)**, net **+1.21e-05 (ns)**, points +0.0060 ±
0.0037. The mis-pricing was real; correcting it trades conversion for location at
par. **§0ag Part A is closed:** the units were wrong and the wrongness was free.

### `V8_TRIM` — v7's lead did not survive

Both trims are worse on event loss (`TRIM2` +8.17e-05 at 1/12, `TRIM5` +1.06e-04
at 0/12) and `TRIM2` is worse on points (+0.0117 ± 0.0082). The footprints were
matched to v7's by construction — 13.20% and 28.60% of training weight at every
origin — so this is not a strength mismatch.

v7's `V7_HOLDX2 − V7_RANDX2` was −0.0164 ± 0.0077 at 7/12 seasons, the one
contrast that cleared two sem. **It does not reproduce as a continuous
down-weight.** Either the mechanism is hard removal specifically — which is not a
shippable model, since a tool must price Gobert and Capela — or it was the
coin-flip-on-seasons it looked like. Given 7/12 and a dead
difference-in-differences, the second reading is now the more likely one.

### Recency — the pinned default survives

Monotone on event loss: half-life 365 **+1.064e-04 (established harm)**, 730 the
reference, none **−6.979e-06 (ns)**. On points, `HL365` is the best arm
(−0.0033 ± 0.0117) and `FLAT` nearly the worst (+0.0143 ± 0.0207), neither
established.

The additive/neural time asymmetry is answered too: `V8_FLAT` adopts the
additive's own no-decay convention and is **worse** in points than `V8_BASE`.
That asymmetry was not costing the neural arm anything, and 730 does not need
widening down.

## The apparent objective/target conflict is RESOLUTION, not misalignment

Across the six arms the event-loss and MAE improvements look inversely ranked —
Spearman −0.886, Pearson −0.533. That is six points, chosen after seeing them,
and **it does not survive a test with power.**

Pooling every (arm, origin) pair gives **288 paired deltas** of the same two
quantities. Regressing the MAE gain on the event gain:

> **slope −3.68 ± 21.39 MAE per unit event loss, r = −0.0102, n = 288**

Indistinguishable from zero — **not negative**. And `V8_STD` alone, the only arm
with real event movement (gains spanning −1.08e-03 to +8.51e-05 across origins),
reads **r = +0.038 over 48 origins**. Per-arm correlations scatter from +0.456 to
−0.535 on n = 48 each, which is what noise looks like.

**So the objective is not pulling away from the target; the target cannot see the
objective.** That is `BACKLOG` §0's standing calibration restated — this
population resolves a lever worth ~0.04 MAE and cannot establish one worth ~0.01
— and it is the benign reading of the two.

The consequence for v9 is concrete and it is the opposite of what the six-arm
ranking suggested: **do not change the objective.** `V8_STD` is a real
improvement to a well-specified objective, and the reason it does not show in
points is the benchmark, not the model. v9's choice is between accepting
event-level improvement as the deliverable and finding a point evaluation with
more power — not between event families and something else.

## Verification

- 336/336 arm-origins; `completion_status.json` `core_complete`; zero errors.
- Event-loss baseline identical across all 336 arm-origins to **0.00e+00**.
- `V8_BASE` reproduces `V7_FULL` bit-identically on every metric and family.
- Every arm exactly one field from the base spec, asserted by test.
- Penalty weights normalise to mean one, asserted by test, so `V8_SCALE` is a
  units change and not a λ change.
- Future-mutation test: appending games after the cutoff changes no weight,
  threshold or solved scale for any arm.
- Selected epoch max 25 against a cap of 48 — still not binding.
- 719 tests pass. No scorer promotion, no page change, no database mutation, no
  completed run directory touched.
