# Capacity-law defense: confirmatory protocol — 2026-10-09

Frozen before the run started. Approved by Adam on 2026-10-09. The analysis
code, `scripts/capacity_score.py`, is committed with this protocol and is not
revised after results are seen. Any post-hoc analysis is labeled as such in
the results report.

## What is run

- **Arm.** `CapacityDefense` version 2 (`lineups/model.py` at the commit that
  adds this file). It is built with
  `EventModel.from_parent(v14 parent, seed, defense="capacity")`.
- **Protocol.** The full reference protocol in `lineups.train.fit_origin`:
  - inner epoch selection: patience 8, cap 96;
  - a fresh final fit for the selected number of epochs;
  - the last five checkpoints are kept.
- **Origins and seeds.** All 48 origins, 2015q1–2026q4. 2015 is warmup for
  calibration only. Seeds are 17, 23 and 41, giving 144 fits.
- **Runner.** `scripts/capacity_run.py`, writing to
  `experiments/cache/capacity_v2_run_2026_10_09/`.
- **Comparator.** The saved J_POINT_BOTH fits (v16 production) on identical
  rows.

## Primary contrasts and decision rules

1. **Accuracy (pillar 1), non-inferiority.**
   - *Population.* The primary benchmark: 44 quarters, 2016–2026, broad
     offense-five cells with at least 50 possessions, actual defenses,
     possession-weighted, points per 100.
   - *View.* Checkpoint-average forecasts, seed-mean, each model with its own
     prior-only affine calibration, blended half and half with
     additive_defense.
   - *Statistic.* Δr² = capacity − reference, pooled over all quarters.
     Uncertainty comes from the 11 per-season Δr² values (SD/√11).
   - *Rule.* Non-inferior if Δr² − 1.812 × SE > −0.003 (one-sided 95%, t with
     10 df).
2. **Weird lineups (pillar 2), fixtures across time.** At each of the 44
   primary origins, compute the native margin from three-seed checkpoint
   mixtures for:
   - legal centers vs Jokić/Westbrook;
   - legal centers vs Jokić/Korver;
   - five Goberts vs Jokić/Westbrook.

   *Rule.* A demonstrated pillar-2 gain needs all of the following:
   - the legal-centers margin against Jokić/Westbrook is lower under capacity
     at 75% or more of origins;
   - its mean reduction is at least 2 points;
   - at most one of the seven properties named under contrast 3 is worse
     under capacity by more than 0.05, on average over its four origins.
3. **Property suite.** `lineups.properties` at 2024q4, 2025q4, 2026q2 and
   2026q4, using three-seed checkpoint mixtures.
   - Pass rates are reported for every property.
   - Perimeter coverage and coverage targeting are reported but not counted
     in rule 2. The screen already showed perimeter coverage regressing, and
     targeting is chance-level for both models.
   - The seven properties that count are spacing_rim, handler_conversion,
     handler_teammate_turnovers, clone_synergy, rim_synergy, rebound_synergy
     and permutation.

## Secondary (reported, no decision rule)

- **Real unusual cells.** Residual bias (actual minus forecast) for each
  model, with season-level SE, on:
  - offenses with two or more non-spacing bigs;
  - offenses whose best passer is below 5 assists per 100;
  - defenses with two or more bigs (6'10"+).

  These use row-level residuals in the 44 primary quarters, half blend.
- **Novel-lineup r².** The direct view and the native r².
- **Outer event objective.** Mean over origins.

## Power

The screen's per-origin SD of Δr² was about 0.005 at a single seed. With 44
origins and three seeds, the season-level SE should be about 0.001. A true
Δr² of −0.001 would then pass, and a true −0.003 would fail.
