# Preparing the 2026–27 prospective freeze — 2026-10-09 (evening)

Exploratory and engineering work toward the
[draft protocol](prospective_2027q1_protocol_2026_10_09.md). Nothing here
touches the [confirmatory capacity run](capacity_confirmatory_protocol_2026_10_09.md),
which runs from its pinned worktree.

## 1. Two-phase training replaces the v14 parents (decision)

`scripts/two_phase_check.py`, seed 17. Each row compares two-phase training
from scratch with the saved reference at the same origin, on identical outer
rows:
- **Phase A** trains the offense alone.
- **Phase B** is the full model, started from phase A.

Half-blend r² is checkpoint-average with the reference's calibration.

| Origin | References | Phase-A / B epochs | Point MSE | Half r², reference → two-phase |
| --- | --- | --- | ---: | --- |
| 2016q1 | saved v16 | 32 / 7 | −0.46 | .0976 → .1010 |
| 2019q3 | saved v16 | 20 / 16 | −0.52 | .1553 → .1579 |
| 2022q2 | saved v16 | 5 / 20 | +0.93 | .0600 → .0597 |
| 2025q4 | saved v16 | 5 / 5 | −0.07 | .0225 → .0237 |
| 2016q1 | self | 32 / 7 | −0.49 | .0976 → .1009 |
| 2019q3 | self | 20 / 16 | −0.52 | .1553 → .1579 |

- **Overall.** Mean Δ half r² is +0.0017 (saved references), and no origin is
  worse than −0.0003. Event losses are within ±0.0005.
- **2022q2.** This is where single-stage training failed (+10.3 point MSE).
  Two-phase is +0.9 there.
- **Self-references.** These normalize each phase by its own starting model,
  the definition that works at origins without saved references. They
  reproduce the saved-reference fits: the same epochs, and metrics within
  0.03 MSE.

**Decision.** Origins without v14 parents, starting with 2027q1, train
two-phase with self-references. The saved 2015–2026 fits stay as they are.
This is one seed at four origins, so it supports using two-phase where
nothing else exists. It does not show that two-phase is better.
Self-reference runs at 2022q2 and 2025q4 were still running at writing.

**Addendum 2026-10-12.** The self-reference runs at 2022q2 and 2025q4 also
reproduce the saved-reference fits. They select the same epochs (5/20 and
5/5), give the same half r² (.0597 and .0237) and point MSE (+0.93 and −0.07),
and their event losses are within 1e-5. All four origins now agree.

## 2. The additive control is ported

`lineups/additive.py` computes additive_defense for any offense and defense
fives at an origin. The chain is:
- the as-of ridge snapshot;
- centering on prior exposure;
- the offense calibration;
- the defense slope;
- the v16 affine.

It reproduces the saved per-row control to 5e-13 at 2015q1, 2016q1, 2020q3
and 2026q4, including every intermediate parameter (`tests/test_additive.py`).

The ridge fit itself still runs from the old code:
`scripts/additive_origin_fit.py`, using the legacy worktree.
- **Check.** Refitting 2026q1 gives the same penalties, with coefficients
  within 4e-12 of the saved fit.
- **2027q1.** The fit at 2027q1 (opening night 2026-10-20, data through
  2026-06-13) chose penalties career 1e4, prior 1e8, experience 1, delta 1e4.
  - The experience penalty sits at the grid's low edge after two expansions.
    The saved 2025q1 and 2026q1 fits carry the same flag. The last expansion
    moved forecasts by 9e-6 points/100.
  - The league level at 2027q1 is 115.83 (115.63 at 2026q4).

## 3. A stale capability library costs about 0.007 r²

The capability library ends at 2026-03-02, the last backtest origin. A
2027q1 forecast would therefore read player capabilities 7.5 months old,
missing the last quarter and the playoffs. Every backtest origin had a
snapshot at its own start.

`scripts/library_staleness_check.py` imitates this at past opening quarters.
- **Setup.** The library is cut at the previous season's quarter-4 start.
  Outer-quarter forecasts of the saved reference (seed 17 checkpoint mixture,
  origin mode) are compared with the normal ones. The rows and calibration
  are identical.
- **Not imitated.** The 2027q1 fit's training rows after March would also be
  stale.

| Origin | Library cut at | Half r², monthly → stale | Calibrated r² change | Native shift, mean (RMS) |
| --- | --- | --- | ---: | ---: |
| 2016q1 | 2015-03-05 | .0976 → .0778 | −0.0280 | +1.59 (1.85) |
| 2017q1 | 2016-03-03 | .1011 → .1226 | +0.0397 | +1.89 (2.17) |
| 2018q1 | 2017-03-02 | .0174 → .0075 | −0.0247 | +0.63 (0.86) |
| 2019q1 | 2018-02-27 | .0525 → .0467 | −0.0048 | +0.68 (1.17) |
| 2020q1 | 2019-02-26 | −.0046 → −.0241 | −0.0345 | +0.99 (1.43) |
| 2021q1 | 2020-03-02 | .1231 → .1244 | +0.0117 | +1.57 (2.04) |
| 2022q1 | 2021-04-26 | −.0629 → −.0962 | −0.0598 | +0.74 (1.53) |
| 2023q1 | 2022-02-27 | .1061 → .0990 | −0.0048 | +1.03 (1.48) |
| 2024q1 | 2023-02-25 | .0954 → .0921 | −0.0052 | +0.85 (1.29) |
| 2025q1 | 2024-03-04 | .0955 → .0896 | +0.0096 | +1.25 (1.61) |
| 2026q1 | 2025-03-03 | .0577 → .0653 | +0.0267 | +1.08 (1.64) |

- **Half r².** Staleness changes half r² by −0.0067 ± 0.0044 on average, worse
  at 8 of 11 origins.
- **Bias.** It raises native forecasts by about 1 point per 100, a bias the
  calibration (fitted on fresh-library history) does not remove.
- **Arm A.** The additive arm does not read the library, so a stale library
  would tilt primary contrast 1 against the neural arms.

**Action.** `scripts/library_extend.py` runs the unchanged legacy chain code
for the snapshot dates the legacy calendar requires once 2027q1 is in the
schedule:
- monthly from 2026-04-01 to 2026-10-01, plus 2026-10-20;
- each chain warm-started from the saved 2026-03-02 state;
- the saved season-2026 penalty, plus a new season-2027 selection for the
  opening-night snapshot.

Check: rebuilding the saved 2026-03-02 snapshot from 2026-03-01 reproduces
it exactly, every array to 0, on the two chains tested. The extension was
running at writing. A new store, `lineups_store_2027q1_library`, adds it with
`scripts/build_prospective_store.py --library-extension`. The first 2027q1
store is left as it was.

## 4. Power of the prospective test, and a level-free metric

Backtest, J_POINT_BOTH half minus additive_defense, per quarter, 2016–2026.
Centered r² removes each forecast's possession-weighted mean error over the
quarter before scoring.

| Metric | Quarters | Mean | SD | Positive |
| --- | --- | ---: | ---: | ---: |
| Raw r² | all 44 | +0.018 | 0.024 | 35 |
| Raw r² | opening 11 | +0.034 | 0.032 | 10 |
| Centered r² | all 44 | +0.013 | 0.014 | 36 |
| Centered r² | opening 11 | +0.021 | 0.007 | 11 |

Raw r² in a single quarter is dominated by level misses.
- **Bias at opening quarters.** The reference's mean error has an SD of about
  2.7 points, and additive's averages +1.9.
- **2026q1.** The reference was 5.2 points too low on average, while ranking
  better than A (correlation .323 vs .295). This is the one opening quarter
  where raw r² favored A.

**Protocol changes, made before any 2026–27 data exist:**
- Centered r² is the primary metric for both prospective contrasts, with raw
  r² and bias reported beside it.
- A whole-season population is added: every 2026–27 game, forecast with the
  opening-night models and states, with no refit.
