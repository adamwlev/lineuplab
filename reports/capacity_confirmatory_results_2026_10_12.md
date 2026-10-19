# Capacity-law defense: confirmatory results — 2026-10-12

These are the results of the run registered in
[the protocol](capacity_confirmatory_protocol_2026_10_09.md).
- **Run.** 144 fits (48 origins × seeds 17, 23, 41), in
  `experiments/cache/capacity_v2_run_2026_10_09/`.
- **Scorer.** The frozen `scripts/capacity_score.py`, unchanged since the
  freeze. Its output is in `.../score/result.json`.

Anything not named in the protocol is marked **post hoc**.

## Verdict under the frozen rules

| Rule | Result | Decision |
| --- | --- | --- |
| 1. Accuracy non-inferiority (margin −0.003) | Δr² = +0.0005, season SE 0.0016, lower bound −0.0025 | **Non-inferior** |
| 2a. Legal centers vs Jokić/Westbrook lower under capacity at ≥75% of origins | 31 of 44 (70.5%) | **Fails** |
| 2b. Mean reduction ≥ 2 points | −2.29 | Passes |
| 2c. At most one counted property worse by > 0.05 | none worse by > 0.05 | Passes |
| **Pillar-2 gain demonstrated** | | **No (rule 2a missed by two origins)** |

The capacity-law model is as accurate as the reference. The registered
pillar-2 gain was not shown.

## 1. Accuracy

Primary benchmark:
- 44 quarters, 8,345 broad offense-five cells;
- checkpoint-average forecasts, seed-mean, each with its own prior-only
  calibration, half blend with additive_defense.

| | Reference | Capacity |
| --- | ---: | ---: |
| Half r², all cells | .16299 | .16345 |
| Half r², novel lineups | .14450 | .14537 |
| Calibrated r², all | .16148 | .16353 |
| Native r², all | .15575 | .16008 |
| Native r², novel | .14235 | .15107 |

Per-season Δ half r² (capacity − reference):

| 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| +.0017 | +.0008 | −.0014 | −.0014 | −.0003 | −.0012 | −.0042 | +.0016 | −.0035 | −.0004 | +.0158 |

Four of 11 seasons are positive; 2026 alone carries the positive mean.
**Post hoc:** without 2026, the mean is −0.0008 (SE 0.0006, lower bound
−0.0020), still non-inferior. The fair reading is "no detectable difference"
rather than "better".

## 2. Fixtures (native margins, three-seed checkpoint mixtures, 44 origins)

| Matchup | Reference mean | Capacity mean | Lower under capacity | Loses: reference → capacity |
| --- | ---: | ---: | ---: | --- |
| Legal centers vs Jokić/Westbrook | −2.57 | −4.85 | 31/44 | 64% → 86% |
| Legal centers vs Jokić/Korver | −1.26 | −4.20 | 33/44 | 64% → 86% |
| Five Goberts vs Jokić/Westbrook | +3.87 | −3.23 | 44/44 | 18% → 70% |

**Post hoc, by season.**
- **2016–2018.** Capacity *raised* the legal-centers margin at 10 of 12
  origins. At those origins the reference already had the centers losing by 8
  to 15 points.
- **2019–2026.** Capacity lowered the margin at 29 of 32 origins, by 1.2 to
  6.2 points per season.

The registered rule counts every origin equally, so the early seasons decide
it.

## 3. Property suite (2024q4, 2025q4, 2026q2, 2026q4; mean pass rate)

| Property | Reference | Capacity | Counted in rule 2 |
| --- | ---: | ---: | --- |
| spacing_rim | .998 | .995 | yes |
| handler_conversion | .977 | .970 | yes |
| handler_teammate_turnovers | .994 | .996 | yes |
| clone_synergy | .979 | .951 | yes |
| rim_synergy | 1.000 | .969 | yes |
| rebound_synergy | 1.000 | .955 | yes |
| permutation | 1.000 | 1.000 | yes |
| perimeter_coverage | .715 | .293 | no (reported) |
| coverage_targeting | .388 | .546 | no (reported) |
| handler_turnovers | .546 | .526 | no (not in either list) |

- **Counted properties.** None is worse by more than 0.05. Rebound synergy
  (−0.045) and rim synergy (−0.031) come closest.
- **Perimeter coverage regresses sharply,** as the screen showed. Each
  attacker reads only his assigned defender, so the extra perimeter cost of a
  slow defender stays local.

## 4. Real unusual cells (secondary; residual = actual − half forecast, points per 100, season SE)

| Cohort | Possessions | Reference | Capacity |
| --- | ---: | ---: | ---: |
| Offense with ≥2 non-spacing bigs | 21,751 | −2.45 ± 2.94 | −2.49 ± 2.95 |
| Offense whose best passer < 5 ast/100 | 105,323 | −2.31 ± 0.53 | −2.35 ± 0.53 |
| Defense with ≥2 bigs (6'10"+) | 549,957 | −0.94 ± 0.20 | −0.98 ± 0.18 |

On real unusual lineups the two models are indistinguishable. Both
overpredict offenses with a weak best passer by about 2.3 points. That is a
real creation shortfall both models share, inside the observed range.

**Not computed.** The protocol also listed the outer event objective as a
secondary output. The frozen scorer does not compute it, and it was not
added afterwards.

## What this means

- **The capacity law is free in accuracy, and it changes the extremes.**
  - It is non-inferior, with no detectable accuracy cost.
  - It reverses the five-Goberts verdict at most origins.
  - It deepens the legal-centers loss after 2018.

  These are exactly the properties of a legitimate assumption model: it fits
  observed lineups as well as the reference, and it disagrees only where the
  data are silent.
- **It is not a demonstrated pillar-2 improvement.**
  - The registered rule failed.
  - Perimeter coverage regresses.
  - The early-season reversals show its effect on legal centers is not
    uniform.
- **Recommendation (promotion is Adam's call).**
  - Keep the reference as the single forecast.
  - Use the capacity model as the named alternative in the assumption band
    for hypothetical lineups (STATUS item "Band"), and keep it as arm C of
    the prospective test.
  - Its disagreement with the reference is the assumption-based uncertainty
    the decisions of record ask for.
- **The band has an offense-side gap.** The two models share the same
  offense. A lineup flagged "no ball handler" therefore gets no extra width
  from offensive extrapolation. An offense-side assumption model is needed
  for that reason to widen the band: a declared hinge that acts only beyond
  the observed range of creation shortfall, so in-range accuracy is unchanged
  by construction.

## Addendum 2026-10-12 (post hoc): level-free accuracy, and the neural model alone

`scripts/nn_alone_check.py`, on the same population and forecasts. Adam
suggested that pillar-2 fixes come more easily through the neural model
alone, without the additive half. Centered r² removes each forecast's mean
error per quarter, so it measures ranking skill without level misses.

| Contrast (per quarter) | Raw r², mean | Centered r², mean ± season SE | Seasons positive (centered) |
| --- | ---: | ---: | ---: |
| Capacity half − reference half | +0.0006 | −0.0011 ± 0.0004 | 2/11 |
| Capacity alone − reference alone | +0.0024 | −0.0024 ± 0.0008 | 2/11 |
| Reference alone − reference half | −0.0026 | −0.0006 ± 0.0016 | 6/11 |

Pooled raw r²: reference half .1630, reference alone .1615, capacity alone
.1635.

- **This qualifies "non-inferior".** Capacity ranks lineups slightly but
  consistently worse than the reference. The registered raw-r² result leans
  on level differences, mostly in 2026.
  - On centered r² the half blend would still pass the −0.003 margin.
  - The neural model alone, at −0.0024 ± 0.0008, would not: its lower bound
    is about −0.004.
- **Dropping the additive half costs the reference almost nothing in
  ranking** (−0.0006 per quarter). Its raw-r² cost (−0.0015 pooled) is level
  noise that the additive half used to average away.
- **The prospective protocol now uses the neural model alone** as its primary
  forecast, with half blends secondary.
