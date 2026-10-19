# Prospective test: small guards × rim anchor (H1), 2026–27 — pre-registration

**Frozen 2026-10-12, before opening night (2026-10-20). Adam approved.**

This is a separate addendum. It does not modify the frozen 2026–27
prospective record (`reports/prospective_2027q1_protocol_2026_10_09.md`).
The motivation is H1 in the
[synergy results](synergy_hypotheses_results_2026_10_12.md):
- strong in 2016–2026: −0.66 ± 0.19 points per 100 per small defender,
  9/11 seasons;
- does not replicate in 2007–2013.

## Hypothesis

On defense, small defenders cost fewer points when the five has a rim anchor
than when it doesn't. The direction is declared: the interaction coefficient
is **negative**.

## Data and definitions (as in `scripts/synergy_hypotheses.py`)

- **Rows.** Every game × offense five × defense five row of the 2026–27
  season, in the four quarter windows that `lineups.schedule.build` produces
  for season 2027. Rows are possession-weighted.
- **Baseline.** The frozen R arm at origin 2027q1: three-seed calibrated
  network, using the calibration in the freeze record. It forecasts every
  2026–27 row, and its best additive approximation is fitted within each
  window, as in `scripts/synergy_check.additive_projection`. The residual is
  actual points per 100 minus that approximation.
- **Profiles.** Origin states at 2027q1 from
  `experiments/cache/lineups_store_2027q1_library`, with listed heights. The
  block-rate percentile is taken among players appearing in each window's
  rows.
- **Small defender:** listed 6'3" (75 in) or shorter.
- **Anchor:** a defender 6'9" (81 in) or taller, with block rate in the top
  10%.
- **Model.** The residual (points allowed) on n_small, anchor and
  n_small × anchor, centered within window and possession-weighted.

## Decision

- **Primary.** The interaction coefficient, with a one-sided p-value from
  1,000 game-block bootstrap resamples (numpy seed 20261020). The effect is
  **confirmed** if the coefficient is < 0 and p < .05.
- **Secondary.** The residual of fives with two or more small defenders and
  no anchor, minus that of fives with two or more and an anchor. Predicted
  > 0.
- **Power.** From the 2016–2026 season-to-season spread (SD 0.62 around a
  mean of −0.66), one season detects the effect about 28% of the time. **A
  miss in one season does not refute it.**
- **Accumulation.** The same test is pre-registered for 2027–28. The pooled
  two-season estimate, with power of about 44%, is then the decision.
- **Scoring** needs the 2026–27 data refresh, which is Adam's call.

## What a confirmation would mean

A confirmation would make a labeled defensive interaction a candidate for the
forecast: small defenders' cost would depend on rim protection. A held-out
check of its in-range accuracy would still be required before any change to
what the tool prints.
