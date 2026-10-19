# Joint capability v9 — teammate variety is real, and Adam was right

2026-09-12 (Opus + Adam). Run `experiments/cache/joint_capability_2026_09_12_v9/`,
**288/288 arm-origins**, 48 origins, 12 seasons, 6,179 cells, 803,447 possessions,
9,145 s. Zero errors, one launch.

## The one-paragraph answer

v9 exists because Adam pushed back on my claim that the architecture was a dead
end, and **he was right**. Giving the message network the leave-one-out **standard
deviation** of its teammates — a 576-parameter addition to an 1,814-parameter
model — improves the training objective in **12 of 12 seasons and 45 of 48
origins**. Stacked with v8's input standardisation it reaches **−6.58e-04 event
loss against v8's base, 12/12 seasons**, which is the largest and most consistent
model improvement this workstream has produced. A second message round is
**established harm**, the low-rank decoder is null, and min/max works about as
well as sd, so the finding is "the second moment", not "more capacity". **In
points it is worth nothing** — `V9_ALL` minus `V8_BASE` is −0.0008 ± 0.0254 — which
is v8's resolution conclusion holding exactly.

## Event loss — the primary readout

Season-paired against `V9_BASE`, shared baseline (verified identical to
**0.000e+00** across all 288 arm-origins). `*` = interval excludes zero; negative
is better.

| arm | event loss | conversion | location | counts | origins better |
|---|---|---|---|---|---|
| **`V9_ALL`** | **−2.57e-04 ± 3e-05, 12/12 \*** | −1.29e-05, 8/12 | −2.68e-04, 11/12 \* | −1.70e-04, 12/12 \* | **46/48** |
| **`V9_SPREAD`** | **−2.46e-04 ± 2e-05, 12/12 \*** | −5.38e-06, 7/12 | −2.56e-04, 11/12 \* | −1.68e-04, 12/12 \* | **45/48** |
| `V9_MINMAX` | −2.35e-04 ± 3e-05, 11/12 \* | +1.34e-05, 5/12 | −2.05e-04, 10/12 \* | −1.93e-04, 12/12 \* | 45/48 |
| `V9_DECODER` | −1.76e-05 ± 1e-05, 8/12 | +2.61e-06, 6/12 | −5.28e-06, 4/12 | −4.22e-06, 6/12 | 28/48 |
| `V9_DEPTH` | **+4.05e-05 ± 2e-05, 3/12 \*** | +2.67e-05, 1/12 \* | +9.09e-05, 4/12 \* | +2.55e-05, 3/12 \* | 17/48 |

### It compounds with v8

Cross-version, identical cells and origins:

| contrast | event loss | seasons |
|---|---|---|
| `V8_STD` − `V8_BASE` | −4.12e-04 ± 4e-05 | 12/12 \* |
| **`V9_SPREAD` − `V8_BASE`** | **−6.58e-04 ± 3e-05** | **12/12 \*** |
| `V9_ALL` − `V8_BASE` | −6.69e-04 ± 6e-05 | 12/12 \* |

Two representational fixes — standardise what the message reads, then tell it how
varied its teammates are — take the objective down **−6.6e-04 in 12/12 seasons**
for 576 extra parameters. Nothing else in eight versions has been this consistent.

### Phase 0 called it

Phase 0 predicted this before any fit: teammate sd is **98.1% orthogonal** to
teammate mean (median over 18 coordinates, 17 of 18 above 80%), and its own spread
runs 0.033–0.408 against coordinate sds of 0.089–0.862. The information was there
and the model could not see it. That is the version's whole content.

### Where the gain lives

`location` and `counts` carry it — −2.56e-04 (11/12) and −1.68e-04 (12/12) — and
**conversion does not move** (−5.38e-06, 7/12, ns). That is coherent: variety in
your teammates changes *where and how often* you shoot, which is §8g–8h's
basketball-legible composition channel, and does not change how well you shoot.

## What failed, and why the failures are informative

**A second message round is established harm** (+4.05e-05, 3/12, worse on every
family, better in only 17 of 48 origins) — and the block **grew to 45% of round
one**. The data used the extra round and it generalised worse. One round of
message passing is the right depth, measured rather than assumed.

**The low-rank decoder is null** (−1.76e-05, 8/12) and `U` grew to only 4.7% of
the diagonal slope. The diagonal decoder's strong bias — coordinate *j* maps only
to output *j* — is not costing anything, and its interpretability is safe.

**`V9_MINMAX` ≈ `V9_SPREAD`** (−2.35e-04 vs −2.46e-04) while its block grew
*larger* (0.443 vs 0.352 of the base first-layer norm). So the finding is **any
second moment**, and sd is the more efficient encoding of it — two extra
coordinate-blocks' worth of min/max buys slightly less than one of sd.

**`V9_ALL` is roughly additive.** Predicted from the parts: −2.46e-04 − 1.76e-05
+ 4.05e-05 = −2.23e-04; observed −2.57e-04. The factors barely interact, and
`V9_SPREAD` carries the version.

## Points — net zero across two versions

| arm | MAE | RMSE | raw r² | bias |
|---|---:|---:|---:|---:|
| corrected additive | **8.0343** | 10.7600 | 0.1439 | −0.4842 |
| `V9_ALL` | 8.0680 | 10.7770 | 0.1411 | −0.1162 |
| `V9_MINMAX` | 8.0718 | 10.7885 | 0.1393 | −0.1507 |
| `V9_SPREAD` | 8.0730 | 10.7845 | 0.1400 | −0.2356 |
| `V9_DEPTH` | 8.0775 | 10.8013 | 0.1373 | −0.2086 |
| `V9_DECODER` | 8.0809 | 10.8003 | 0.1374 | −0.1528 |
| `V9_BASE` | 8.0837 | 10.8050 | 0.1367 | −0.1531 |

Every arm beats `V9_BASE`, all six negative — `V9_SPREAD` −0.0088 ± 0.0114 (7/12),
`V9_ALL` −0.0133 ± 0.0171 (4/12) — and **none clears two sem**. Unlike v8, at
least the signs are unanimous.

**The cross-version number is the honest one, and it is a wash.** `V9_BASE` *is*
`V8_STD`, which was v8's worst points arm at 8.0837 against `V8_BASE`'s 8.0663.
So:

| | MAE |
|---|---:|
| `V8_BASE` | **8.0663** |
| `V8_STD` (= `V9_BASE`) | 8.0837 |
| `V9_ALL` | 8.0680 |

Standardisation cost +0.017 in points; the architecture won back −0.013.
**`V9_ALL` − `V8_BASE` = −0.0008 ± 0.0254, 6/12 — dead level.** And
`V9_ALL` − additive = +0.0302 ± 0.0393, unchanged from v7 and v8.

So: **−6.6e-04 of objective improvement at 12/12 seasons, and 0.0008 of points.**
That is v8's finding restated with a much bigger objective effect behind it — the
benchmark cannot see gains of this size (v8: slope −3.68 ± 21.39, r = −0.0102 over
288 paired deltas). It is not evidence the improvements are fake; it is evidence
about the ruler.

## One behavioural note

Re-running the clone ladder at 2026q4 (a clone lineup has teammate spread
**exactly zero**, an input the second-moment arms almost never saw in training):

| arm | mean message swing on clones | on real lineups |
|---|---:|---:|
| `V9_BASE` | −0.855 | +0.289 |
| `V9_SPREAD` | −1.921 | +0.433 |
| `V9_MINMAX` | −2.094 | +0.445 |
| `V9_ALL` | −2.757 | +0.218 |

Arms that can see teammate variety penalise zero-variety lineups **2–3x harder**,
while the composition-distance gradient is essentially unchanged (−2.56 to −3.06
far-minus-near). Recorded as a mechanism observation, not pursued: it is
product-side, and no ground truth exists for a lineup that never played.

## Process

Epoch means 8.77–11.19 against a cap of 48 — not binding. Every arm reproduced
`V9_BASE` to **0.000e+00** at initialisation, so each null reads "the data did not
pay for this block" rather than "it started elsewhere". Every block grew
substantially and consistently across 48 origins, which is what makes `V9_DEPTH`'s
harm and `V9_DECODER`'s null interpretable.

## Verification

- 288/288 arm-origins, `core_complete`, zero errors.
- Event-loss baseline identical across all 288 arm-origins to **0.000e+00**.
- `V9_BASE` reproduces `V8_STD` bit-identically — every metric, all five families,
  the selected epoch.
- Exact nesting at init for all six arms, asserted by test; a companion test
  proves the extra sender input enters only through the new block.
- 735 tests pass. No scorer promotion, no page change, no database mutation, no
  completed run directory touched.
