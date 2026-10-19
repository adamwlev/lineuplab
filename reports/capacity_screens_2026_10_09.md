# Capacity-law defense screens and an assumption-band prototype — 2026-10-09

Exploratory. Follows the [coverage screen](coverage_screen_2026_10_09.md),
which found that learned coverage terms stay inert. This report tests the other
route in the decision of record: assert a capacity law, learn everything else,
and keep the model as a second assumption for the band.

## The assumption model

`lineups.model.CapacityDefense` replaces the reference's broadcast defense,
which averages the five defenders. The principle is that **no team input
averages the five defenders**. Each pooled input is a set of real individual
defenders, so an impossible lineup maps to inputs that real lineups also
produce. Effects are grouped by where they happen:

| Law | Effects | Defenders read |
| --- | --- | --- |
| One rim | Rim and paint location and conversion; rebound recovery | The two with the most inside presence (blocks + defensive rebounds) |
| Five for five | Mid-range and three-point location and conversion, per attacker | His assigned defender (sorted listed position) |
| Pressure | FGA, FTA and turnover rates, per attacker | His assigned defender plus the two inside defenders |

The heads are learned, bounded and zero at the start; only the pooling is
asserted. Under these laws five centers look like a real two-big lineup
inside.

## Screen design (`scripts/capacity_screen.py`, fixed before the first run)

- **Fit.** The full reference protocol, starting from the v14 parents: inner
  epoch selection, a fresh final fit and the last five checkpoints.
- **Scope.** Seed 17, at the same eight origins as the coverage screen.
- **Comparator.** The saved J_POINT_BOTH fit at the same origin and seed,
  which `lineups.train` reproduces exactly.
- **Accuracy.** Broad outer cells, checkpoint-average view, half blend.
  Calibration is approximated two ways: the reference's prior-only affine
  applied to both models ("prior"), and each model's own in-quarter affine
  ("oracle", identical for both).

**Three versions were screened. Versions 2 and 3 are post-hoc revisions.**

- **Version 1** read pressure from the mean of all five. The pressure inputs
  of five centers extrapolated, giving +16% opponent turnovers and a third
  fewer free throws. Ties in inside presence also depended on slot order.
- **Version 2** read pressure from the assigned defender plus the inside two,
  and broke ties by player id. It is kept as the current class.
- **Version 3** removed listed height and position from the heads, keeping
  them only for the assignment. It is not kept.

## Results

Accuracy is capacity minus reference, mean ± origin-level SE over 8 origins:

| Version | Δr² half, prior | Δr² half, oracle | Δr² NN, oracle |
| --- | ---: | ---: | ---: |
| v1 | +0.0003 ± 0.0017 | −0.0005 ± 0.0011 | −0.0010 ± 0.0017 |
| v2 | −0.0019 ± 0.0025 | −0.0004 ± 0.0019 | −0.0015 ± 0.0034 |
| v3 | −0.0028 ± 0.0027 | −0.0008 ± 0.0020 | −0.0023 ± 0.0035 |

None is distinguishable from the reference. A single seed at eight origins
cannot establish non-inferiority at −0.003, because the 95% intervals reach
about ±0.004–0.005. The "prior" column also mixes in a calibration mismatch.
One origin dominates the spread: v2 at 2019q4 loses .0117 under the
reference's calibration but gains .0025 under its own.

Five-center fixtures, native margin against Jokić/Murray/Gordon/Porter/Westbrook
(checkpoint mixtures, seed 17):

| Version | Origins where legal centers lose | Mean change vs reference | Five Goberts, mean change |
| --- | ---: | ---: | ---: |
| Reference | 3/8 | — | — |
| v1 | 6/8 | −2.1 | −4.7 |
| v2 | 6/8 | −3.4 | −7.2 |
| v3 | 6/8 | −3.4 | −7.3 |

- **Origin trend.** Versions 2 and 3 lower the centers' margin at every
  origin from 2019q4 on: by 1.4–2.8 points at 2019q4 and 2021q2, and by 5–8
  at the four latest. At 2017q2 and 2018q3 they raise it by up to 2.5 points;
  the centers' states were different then.
- **2026q4, v2.** Legal centers −1.7 against Westbrook and −2.3 against
  Korver; five Goberts +2.7, down from +11.8.
- **Mechanism at 2026q4, v2.** The centers' defense now costs the Jokić lineup
  6.3 points instead of 11.6. The Jokić lineup's defense now gives the centers
  0.5 points instead of 4.1.

Property suite at 2026q4 (checkpoint mixtures, seed 17):

| Property | Reference | v1 | v2 | v3 |
| --- | ---: | ---: | ---: | ---: |
| spacing_rim, handler_conversion, handler_teammate_turnovers | .98–1.00 | .98–1.00 | .98–1.00 | .98–1.00 |
| clone_synergy | .99 | .98 | .97 | .99 |
| rim_synergy | 1.00 | .92 | .95 | .92 |
| rebound_synergy | 1.00 | .93 | .96 | .96 |
| perimeter_coverage | .66 | .68 | .39 | .47 |
| coverage_targeting | .34 | .50 | .48 | .52 |
| permutation | 1.00 | .99 | 1.00 | 1.00 |

- **Synergy dips.** The hard top-two selection makes the inside response
  discontinuous, so stacking protectors is sometimes super-additive, by up
  to about one percentage point of rim make.
- **Perimeter coverage gets worse.** Per-attacker heads learn the in-range
  pattern that a bigger assigned defender contests better. A center replacing
  the shortest defender shifts every assignment up a size and lowers opponent
  three-point accuracy. Removing listings from the heads (v3) did not fix
  this, so the measured descriptors carry the same pattern.

## Assumption-band prototype

`scripts/assumption_band.py` reports, at 2026q4, the reference's native
margin (three-seed mixture), the v2 capacity margin (seed 17) and the
out-of-support reasons from `lineups.support`:

| Matchup | Reference | Capacity v2 | Support |
| --- | ---: | ---: | --- |
| Real Minnesota five vs Jokić/Westbrook | +2.3 | +2.3 | within |
| Knicks four + Gobert vs Minnesota five | −0.8 | −0.7 | within |
| Five small guards vs Jokić/Westbrook | −10.7 | −10.2 | within |
| Legal centers vs Jokić/Westbrook | +4.3 | −1.7 | composition beyond every trained five; no shooter; five non-spacing bigs |
| Legal centers vs Jokić/Korver | +4.4 | −2.3 | same |
| Limited centers vs Jokić/Westbrook | −8.3 | −11.5 | composition; no shooter; four non-spacing bigs |
| Five Goberts vs Jokić/Westbrook | +9.8 | +2.7 | also no ball handler; repeated player |
| Five Jokićs vs Jokić/Westbrook | +23.0 | +18.6 | composition; repeated player |

The two models agree to within 0.5 points inside observed support and differ
by 3–7 points exactly where the support reasons fire. This is the intended
property of an assumption-based band: it widens by construction where a
declared law changes the answer, and it names why. It is not validated as a
probability interval.

## Reading

- **Inside capacity is the law that moves the fixtures.** It cuts the
  centers' extrapolated defense roughly in half at recent origins. Adding it
  costs no measurable accuracy at this screen's resolution.
- **The perimeter half is still unsolved.** No version learns that centers
  guarding the perimeter is costly. Two routes remain: in-range data plus an
  asserted magnitude, or support from the 2002–2013 era. The property suite
  catches the regression, as it should.
- **Five Goberts still don't fail.** No version makes them lose by a wide
  margin. The offense's creation constraint is nearly inert (see the
  diagnosis). An offensive capacity law, such as an initiator requirement,
  would be the matching assumption model.
- **Settling non-inferiority needs the full run.** Version 2 on 44 origins,
  plus 2015 warmup, with three seeds is about 144 fits, or 6–7 hours at four
  in parallel. That exceeds the six-hour limit, so it needs Adam's approval.
