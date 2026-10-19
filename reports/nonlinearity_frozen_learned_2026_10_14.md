# What the frozen module learned (post hoc) — 2026-10-14

A post-hoc, descriptive check on screens 5b and 6. The question: are the
frozen module's (`frozen_fixed`) changes real interactions? The inputs are
the saved per-cell coefficients
(`experiments/cache/nonlinearity_screen_2026_10_13/`: `screen6_summary_*`
for seed 17, `screen5b_summary_s{23,41}_*`).

**Method.** For each type-pair cell, the module's learned change is the
reference's residual coefficient minus the arm's. The test is the discovery
test: within-quarter centered, with type-count controls, on the outer
quarters 2022–2026. Each fit was trained before its quarter, so the
comparison with that quarter's actual coefficients is forward.

## Results (3 seeds)

- **Systematic.** The learned changes on the 511 other cells correlate
  0.86–0.89 between seeds.
- **Real, in direction.** The 3-seed mean change correlates with the actual
  interaction pattern at 0.86 on the 14 held-up cells, which were selected
  on other windows. On the other 511 cells the correlation is 0.52.
- **Small.** It learns about a fifth of each effect: slope 0.20–0.27
  on held-up cells, 0.16–0.20 on the others. On the 58 other cells with
  |z| ≥ 2.58 the slope is +0.17.
- **Not invented.** On the 453 weak cells its changes average 0.36 SE.

Share of each held-up effect learned (3-seed mean):

| Event | Combination | Actual | Share learned |
| --- | --- | ---: | ---: |
| FTA | bigs × bigs (defense) | +0.87 | 37% |
| FTA | small × self-creator | +0.27 | 32% |
| FTA | small × small (defense) | +0.59 | 30% |
| FTA | small × passer | +0.44 | 23% |
| Rim share | rim protector × rebounder (defense) | +0.44 | 23% |
| Rim share | bigs × bigs (defense) | +0.74 | 22% |
| Rim share | bigs × rim protector (defense) | +0.35 | 21% |
| Three share | big × crasher | +0.33 | 16% |
| Three share | crasher × crasher | +0.74 | 15% |
| FTA | small × small (offense) | +0.57 | 14% |
| Three share | non-shooter × crasher | +0.52 | 14% |
| TOV | non-shooter × crasher | −0.22 | 12% |
| TOV | shooter × self-creator | −0.13 | 10% |
| TOV | slasher × usage | −0.11 | −2% |

Residual χ² by family, 3-seed mean (reference → frozen_fixed):
- FTA: 98 → 52 on the 5 held-up cells, 539 → 407 on 100 others.
- Points: 175 → 131 on 105 cells.
- Three share: 62 → 45 held-up, 279 → 233 others.
- Rim share: 60 → 37 held-up, 167 → 178 others.
- TOV: 31 → 26 held-up, 252 → 215 others.

## Reading

- **The interactions it learns are real.** They are the measured ones,
  learned at about a fifth of full strength, mostly in free throws and in
  rim and three-point share.
- **The accuracy loss comes from elsewhere.** The cell tests remove each
  quarter's average and r² does not. The −0.01 loss is the fit-specific
  level shift plus non-predictive spread (screen 6 report). It is not
  learned interaction structure.
- **The 511 other cells.** The module's agreement there supports the
  proposed second discovery round. The strong cells look like real
  structure, but that remains to be replicated on 2007–2013.
- **Caveat.** These are the 20 quarters every screen was judged on.
  Everything here is descriptive.
