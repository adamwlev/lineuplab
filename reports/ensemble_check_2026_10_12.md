# Seed and variant ensembles — 2026-10-12

Exploratory. Script: `scripts/ensemble_check.py`; rows and output in
`experiments/cache/ensemble_check_2026_10_12/`.

**Forecast.** The calibrated neural model alone. Each seed is calibrated by
its own prior-only affine and is already a mixture of its last five
checkpoints.

**Population.** Broad offense-five cells (at least 50 possessions), in points
per 100:
- *benchmark:* 2016–2026, 11 seasons, using the saved reference and the
  confirmatory capacity run;
- *era:* 2007–2013, 7 seasons, using the era backtest fits.

Raw r² is pooled as in the scorecards. Centered r² is within quarter.
Differences are season means ± season SE.

## Results

| | Benchmark raw | Benchmark centered | Era raw | Era centered |
| --- | ---: | ---: | ---: | ---: |
| Single seed (mean of 3) | .1594 | .1004 | .1434 | .1347 |
| Three-seed mean (R) | .1615 | .1012 | .1464 | .1358 |
| Capacity, three seeds (C) | .1635 | .0990 | .1446 | .1330 |
| Mean of R and C | .1638 | .1007 | .1464 | .1351 |

- **Seeds.** Going from one seed to three gains about +0.002–0.003 raw and
  +0.001 centered.
  - Under simple averaging, the remaining gain from infinitely many seeds is
    about half the 1→3 gain: roughly +0.0005 centered. Ten seeds would get
    about a third of that.
  - Raw r² is noisy at the seed level. On the benchmark, seed 17 alone beats
    the three-seed mean, through its calibration.
- **Variants.** Averaging the reference and capacity does not improve
  ranking:
  - benchmark centered −0.0005 ± 0.0004 (3 of 11 seasons better);
  - era centered −0.0008 ± 0.0007 (3 of 7).

  Its raw gain on the benchmark, +0.0028 ± 0.0028, is a level effect from
  capacity's calibration, not better ranking.

## Earlier ensemble work (from docs/history)

- **v16, forward-selected stacks.** Multi-NN stacks of v16 arms plus additive
  scored .1609–.1614 raw. That is below the single reference half blend,
  .1630. The forward top-one selector chose the reference at all 44 origins.
- **v14–v16, checkpoint average.** Averaging the last five checkpoints rather
  than the best epoch gains +0.00007 (half blend).
- **v7–v8, ensemble spread as uncertainty.** Disagreement among members did
  not order forecast error (a pre-registered null). The spread does
  measure how extreme a composition is.
- **Network + additive half blend.** This was the one ensemble that helped:
  +0.0015 raw and +0.0006 centered over the network alone. The product drops
  it by Adam's decision of 2026-10-12, and the trade is printed.

## Reading

Ensembling is used up as a source of accuracy. Three seeds of five
checkpoints each, the shipped configuration, captures most of what seed
averaging can give. Variants of the same architecture make nearly identical
in-range predictions. Their disagreement belongs in the band, not in the
point forecast.
