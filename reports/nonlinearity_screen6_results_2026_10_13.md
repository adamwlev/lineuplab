# A pure-interaction module on the frozen network: results — 2026-10-13

Results of the [protocol](nonlinearity_screen6_protocol_2026_10_13.md),
committed (68f2561e) before any fit. This is an exploratory screen: one seed
(17) at the 20 quarters of 2022–2026.
- Script: `scripts/nonlinearity_screen.py`.
- Output: `experiments/cache/nonlinearity_screen_2026_10_13/`
  (`frozen_pure_*`, `screen6_*`, `level_diagnostic_frozen_pure.*`).

## Summary

- **Part A fails on the new declared bar, forward-calibrated accuracy.**
  - Calibrated like the tool, from each arm's own earlier quarters, the arm
    loses −0.0131 (SE 0.0077) r²; the bar was −0.003.
  - `frozen_fixed` lost −0.0114 (0.0071) on the same seed. Centering did not
    help.
- **Everything else passes:**
  - χ²_H 163 (bar 184);
  - χ²_N 1,151 (bar 1,417);
  - equal-calibration accuracy −0.0023 (bar −0.003);
  - five Goberts' offense +0.3 (SE 0.7), legal centers' +0.2 (0.7);
  - Jokić/Westbrook score +2.2 (0.5) more against the Goberts.
- **Part B was not evaluated,** by the rule. Its 40 fits ran with Part A and
  finished; their outcomes were not read.
- **My diagnosis for screen 6 was wrong, or at least incomplete.**
  Centering the features did not remove the quarter-level shift: its SD
  across quarters is 1.11, against 1.09 for `frozen_fixed`.
- **Post hoc, the shift comes mostly from the defensive term,** and from the
  module fitting the training window's level.
- **The frozen route stops here.** The tool keeps the bolted-on layer.

## Results

| Seed 17, 20 quarters | Bar | frozen_fixed (5b) | frozen_pure |
| --- | --- | ---: | ---: |
| χ²_H, 14 held-up cells | ≤ 184 | 145.5 | 162.9 ✓ |
| χ²_N, 511 other cells | ≤ 1,417 | 1,093 | 1,151 ✓ |
| Accuracy, equal calibration | ≥ −0.003 | −0.0019 (0.0028) | −0.0023 (0.0028) ✓ |
| **Accuracy, own forward calibration (16 quarters)** | ≥ −0.003 | −0.0114 (0.0071) | **−0.0131 (0.0077)** ✗ |
| Accuracy, reference's prior calibration | — | −0.0088 (0.0057) | −0.0085 (0.0059) |
| Non-additive share | — | 0.0186 | 0.0188 |
| Five Goberts' offense vs reference | ≤ +1 | +0.5 (0.7) | +0.3 (0.7) ✓ |
| Legal centers' offense vs reference | ≤ +1 | +0.6 (0.6) | +0.2 (0.7) ✓ |
| Jokić/Westbrook's offense vs Goberts | > 0 | +2.3 (0.4) | +2.2 (0.5) ✓ |
| Level shift on real lineups, SD over quarters | — | 1.09 | 1.11 |

Property suite at 2026q4 (pass rates; reference / frozen_fixed / frozen_pure):

| Property | Reference | frozen_fixed | frozen_pure |
| --- | ---: | ---: | ---: |
| spacing_rim | 0.999 | 0.974 | 0.987 |
| handler_turnovers | 0.410 | 0.405 | 0.379 |
| handler_conversion | 0.985 | 0.959 | 0.969 |
| clone_synergy | 0.988 | 0.908 | 0.925 |
| rim_synergy | 1.000 | 0.997 | 0.990 |
| perimeter_coverage | 0.658 | 0.732 | 0.484 |
| coverage_targeting | 0.342 | 0.632 | 0.468 |
| handler_teammate_turnovers, rebound_synergy, permutation | 1.000 | 1.000 | 1.000 |

## Post hoc: where the level shift comes from

From `--level-diagnostic`. This is the possession-weighted change in native
points per 100 when the module is switched on, against the same frozen
network with it off. It is split into the offensive and defensive pair
terms, which is an accounting split. Outer rows are each origin's quarter;
training rows are a 40,000-row sample of its training window with inputs as
in training.

| | Offensive term | Defensive term | Both |
| --- | --- | --- | --- |
| Outer rows: mean, SD over 20 quarters | −0.08, 0.35 | +0.22, **0.85** | +0.14, **1.11** |
| Training rows: mean, SD | −0.18, 0.27 | +0.13, 0.38 | −0.05, 0.60 |

The module's level on its own training rows predicts its level on the next
quarter (correlation 0.65 over origins), and the outer shift is larger.

**Reading.**
- **The defensive term is a level knob.** It is one shift applied to every
  possession of a lineup. Even with centered features, the learned
  covariance between teammates' features sets its average.
- **Training past the network's stopping point.** The network was
  early-stopped. Trained on top of it for 8 more epochs, the module keeps
  fitting the training window, including its level, and it does so
  differently in every fit.
- **Forward calibration cannot remove it.** Calibration is fitted on
  earlier quarters, whose module fits had other offsets.
- **Spread is a second cost.** With the level removed entirely (screen 5b's
  test), a cost of −0.0042 remained from spread that does not predict.
- Centering the module's outputs on the training mean would remove at most
  the predictable part of the level: about 40% of its variance by these
  numbers. It would not reach the bar, so I did not try it.

## Where the learned route stands

| | Off-support (clone bigs) | Real-lineup accuracy, forward calibration |
| --- | --- | --- |
| Co-trained module (screens 1–4) | optimistic: +2 even with the module held, via the shared network | kept: +0.002 |
| Frozen module (screens 5–6) | held: within +1, on fresh seeds too | lost: about −0.01 |
| Bolted-on layer (in the tool) | held by type counts | kept: +0.00003 |

Each approach fails one of the two requirements, for a reason now
understood.
- **Co-training** lets the module free the shared network to fit real
  lineups differently, and that carries off-support.
- **Freezing** stops that drift, but the module then fits past the
  network's early stopping, mostly as a fit-specific level.

The bolted-on layer meets both because it has no free level and no main
effects by construction. Its effects are measured, not fitted alongside the
forecast.

## What follows

- **The tool keeps the layer.** This route has now tried eight designs on
  seed 17. Further variants would be tested against the same 20 quarters,
  and I stopped rather than keep spending their credibility.
- **A different use of the learned module (proposal for Adam).** It
  consistently shrinks residual interaction structure outside the 14
  held-up cells (χ²_N 1,417 → 1,093–1,151). Those cells are candidates for
  more *measured* layer effects:
  - discovered by the model in 2022–2026;
  - confirmed or rejected on the replication era 2007–2013, under the
    discovery protocol's rules.

  That keeps the product's guarantees and could grow the set of combination
  effects Adam wants to show.
