# Coverage screen, selection check and creation analogues — 2026-10-09

All exploratory. Follows the
[five-center diagnosis](five_centers_diagnosis_2026_10_09.md).

## 1. A learned coverage assignment changes nothing

Design is in `scripts/coverage_screen.py`, fixed before running.

- **Start point.** Each arm is warm-started from the saved J_POINT_BOTH final
  weights (seed 17) and trained four more epochs on the same rows and batches.
- **Origins.** Eight: 2017q2, 2018q3, 2019q4, 2021q2, 2022q3, 2023q4, 2025q2
  and 2026q4.
- **Arms.**
  - *control*: the reference, continued unchanged.
  - *matched*: per-attacker effects from the defender assigned by sorted
    listed position (`lineups.model.Coverage`).
  - *matched_help*: adds team help, discounted when the helper is assigned to
    a floor spacer, with a learned tethering strength κ in [0, 1].
- **Starting function.** Coverage outputs exactly zero at the start, so all
  arms begin at the same function.
- **Accuracy metric.** Broad outer-quarter cells, actual defenses,
  possession-weighted. Each arm uses the reference's prior-only calibration
  and the half blend.

| Arm minus control (8 origins) | Δr², half | Δr², NN calibrated | Δ event objective |
| --- | ---: | ---: | ---: |
| matched | −0.0003 ± 0.0003 | −0.0009 ± 0.0006 | −0.00002 ± 0.00002 |
| matched_help | −0.0004 ± 0.0003 | −0.0011 ± 0.0007 | −0.00002 ± 0.00002 |

- **Accuracy.** Both arms are well inside the −0.003 non-inferiority margin.
  Neither improves forward accuracy.
- **Tethering.** The learned κ is 0.01–0.03, so help is essentially never
  discounted.
- **Fixtures.** Five-center margins move by less than ±1.5 points, in no
  consistent direction.
- **Properties at 2026q4.** Coverage targeting falls from .74 to .51,
  roughly chance.

**Reading.** Real lineups do not contain the mismatches that would teach a
coverage structure. That matches the residual check in the diagnosis (no big
defense × spread offense interaction, −0.20 ± 0.43) and §31 of the research
overview (a correctly signed assignment cost worth about 0.2 points per SD in
range). A flexible coverage term fitted in range stays near zero, and so does
its extrapolation. Data alone will not make five centers fail.

**The verdict depends on the origin.** The reference's own margin for legal
centers against Jokić/Westbrook (mean of the three seeds' checkpoint
mixtures):

| Origin | Mean margin | Seed SD |
| --- | ---: | ---: |
| 2024q4 | −3.3 | 0.8 |
| 2025q4 | −2.9 | 1.5 |
| 2026q4 | +4.2 | 1.7 |

The real Minnesota lineup shifts by a similar amount between 2025q4 and
2026q4, so part of the 2026q4 result comes from the comparison lineup's
2026 states. Five Goberts win at all three origins, by 1.2 to 9.6.

## 2. Early possessions beat the forecast: selection confirmed in residuals

`scripts/selection_check.py`:

- **Rows.** All 2.76M possessions in the 44 primary quarters, each joined to
  its row forecast (half blend). Possession and point counts match the rows
  exactly.
- **Cell.** Offense five × quarter. Possessions are ordered by date and
  in-game order; "early" is the first 25.

| Cell size | Cells | Raw gap | Residual gap | Season SE | Seasons > 0 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 25–49 | 12,497 | +5.44 | +5.47 | 0.43 | 11/11 |
| 50–99 | 5,267 | +3.18 | +3.11 | 0.39 | 11/11 |
| 100–199 | 1,952 | +1.36 | +1.21 | 0.38 | 10/11 |
| 200+ | 1,126 | +0.78 | +0.98 | 0.64 | 7/11 |

The forecast does not explain the gap; it is constant within a game and
opposing five. A lineup-quarter's first 25 possessions outscore the forecast
by 3–5 points per 100 more than its later possessions in the size range of
the benchmark cohort. This fits coaches keeping lineups that start well.
Other explanations, such as opponents adjusting over a quarter-season, are
not excluded.

Consequences:

- The benchmark cohort scores partly selected outcomes.
- The finite-game noise model's exchangeability assumption is violated.
- In-range fits flatter lineups that survive.

Unusual offenses (two or more non-spacing bigs, or best passer below 5
assists per 100) show +2.0 ± 1.5 against +3.2 ± 0.4 for ordinary ones. This
is underpowered and shows no extra selection.

## 3. Creation: the neural model already carries most of it

`scripts/creation_analogues.py`. Rows are grouped by the offense's best passer
(highest prior assist rate per 100). Residual is actual minus forecast; the
standard errors are season-level.

| Best passer (AST/100) | Possessions | Actual | Half residual | NN-calibrated residual |
| --- | ---: | ---: | ---: | ---: |
| 10+ | 800,414 | 114.4 | −0.29 ± 0.15 | −0.06 ± 0.21 |
| 8–10 | 930,938 | 113.2 | −0.66 ± 0.22 | −0.52 ± 0.22 |
| 6–8 | 747,724 | 111.5 | −0.98 ± 0.13 | −0.69 ± 0.18 |
| 5–6 | 176,147 | 109.6 | −1.42 ± 0.35 | −0.51 ± 0.33 |
| 4–5 | 91,826 | 106.8 | −2.40 ± 0.65 | −1.36 ± 0.59 |
| < 4 | 13,497 | 106.2 | −1.74 ± 1.31 | −0.51 ± 1.30 |

All rows sit near −0.7 because of the small-cell selection above.

- **The blend over-forecasts weak-creation offenses.** Its additive half has
  no creation term.
- **The neural model alone leaves a modest gradient.** It is about −0.8
  points from the 8–10 band to the 4–5 band.
- **Extrapolation adds little.** Pushed linearly to the centers' best passer
  (about 2.5 assists per 100), that gradient adds roughly a point, not enough
  to make the five centers fail.

## What follows

1. **Pillar 2 cannot be reached from 2016–2026 data plus learned structure.**
   The coverage term, the creation gradient and the residual checks all point
   the same way. The data support a poor-but-not-failing center offense and a
   strong center defense, and they cannot see the mechanisms Adam's prior
   rests on: no one to bring up and create, and slow closeouts on the
   perimeter.
2. **Two routes remain, matching the decision of record:**
   - **More real support.** 2002–2011 has about ten times more big lineups
     and far fewer shooters. The matchup rows already reach back to 2001–02.
     Origin states, normalizers and the capability library (which starts in
     March 2009) do not, so the upstream builders must be ported first. The
     2026–27 refresh needs the same builders.
   - **Assumption models plus disagreement.** Build one or two models that fit
     as well in range but assert a capacity law: help and rim protection
     saturate; perimeter coverage needs perimeter defenders. Report their
     spread for out-of-support lineups as an assumption-based band with named
     reasons (no handler beyond observed lineups, defensive inputs beyond the
     real maximum distance). This is the acceptable outcome in the decision of
     record, and it is reachable now.
3. **Selection belongs in the uncertainty model and in the scorecard.** A
   late-possession score, or one with the first 25 possessions of each cell
   excluded, is worth adding as a secondary benchmark.
