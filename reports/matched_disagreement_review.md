# Where the structural model misses: joint basketball review

Generated from frozen pre-season predictions. Season = ending year; all scores and errors are offensive points per 100 possessions, **not net rating**. Predictions use only prior seasons, and no known-pair chemistry. These are database ordinary-point totals, which may differ from a website’s possession convention.

Screen: **258 lineups, >= 500 possessions and >= 20 games**. All qualifying possessions are averaged within each season; years are not pooled. Positive error gap means structural is worse. Sorting on errors creates winner’s-curse selection: the worst-looking cases are not representative performance estimates.

The absolute-error gap cannot exceed the distance between the two predictions. When the actual score lies beyond both predictions, that bound is attained; an even more extreme observed score does not increase this ranking statistic.

Whole-game chronological halves are a stability check, not independent model training. Bootstrap ranges below resample whole games (2,000 draws); they are descriptive, not selection-adjusted or proof of a mechanism. Opponents, injuries, rotations, playoffs and within-season development remain possible confounders. See DISAGREEMENT_AUDIT.md.

For context, across **all 258 screened lineups**, structural wins absolute error in 117 cases. Possession-weighted MAE is 3.825 additive / 3.883 structural. This selected, high-exposure, multi-era subset is not a replacement for the full forward benchmark.

## Main shortlist

| Rank | Season | Lineup | Possessions | Games | Actual | Additive | Structural | Extra structural error | Structural worse in both halves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2025 | Russell Westbrook / Nikola Jokić / Jamal Murray / Michael Porter Jr. / Christian Braun | 766 | 31 | 127.68 | 122.98 | 117.04 | 5.94 | True |
| 2 | 2024 | Kyrie Irving / Derrick Jones Jr. / Luka Dončić / Daniel Gafford / P.J. Washington | 804 | 39 | 114.93 | 116.44 | 122.12 | 5.68 | True |
| 3 | 2024 | DeMar DeRozan / Nikola Vučević / Alex Caruso / Coby White / Ayo Dosunmu | 923 | 32 | 109.10 | 113.50 | 118.97 | 5.47 | True |
| 4 | 2018 | Jonas Valančiūnas / Kyle Lowry / DeMar DeRozan / Serge Ibaka / Norman Powell | 555 | 35 | 109.19 | 111.93 | 117.16 | 5.23 | True |
| 5 | 2016 | Kyrie Irving / LeBron James / J.R. Smith / Kevin Love / Tristan Thompson | 1564 | 57 | 119.12 | 117.39 | 112.25 | 5.15 | True |
| 6 | 2024 | Jarrett Allen / Donovan Mitchell / Darius Garland / Max Strus / Evan Mobley | 854 | 32 | 113.58 | 114.94 | 120.08 | 5.13 | True |
| 9 | 2016 | Kyle Korver / Paul Millsap / Al Horford / Jeff Teague / Kent Bazemore | 2067 | 80 | 104.16 | 108.22 | 112.57 | 4.34 | True |
| 15 | 2023 | Kentavious Caldwell-Pope / Aaron Gordon / Nikola Jokić / Jamal Murray / Michael Porter Jr. | 2192 | 61 | 124.09 | 121.24 | 117.61 | 3.63 | True |
| 18 | 2017 | Kyrie Irving / LeBron James / J.R. Smith / Kevin Love / Tristan Thompson | 1525 | 45 | 120.92 | 116.93 | 113.63 | 3.29 | True |
| 132 | 2025 | Jarrett Allen / Donovan Mitchell / Darius Garland / Max Strus / Evan Mobley | 624 | 27 | 120.35 | 118.37 | 118.25 | 0.12 | True |
| 241 | 2024 | Kentavious Caldwell-Pope / Aaron Gordon / Nikola Jokić / Jamal Murray / Michael Porter Jr. | 2404 | 60 | 124.21 | 118.68 | 121.70 | -3.02 | False |

## Separate first-half selection / second-half check

Top ten selected on first-half error gap only among half-eligible cases. Second-half outcomes do not enter this ordering. This is retrospective stability evidence, not a previously untouched validation set.

| Season | Lineup | N1 | Y1 | Gap1 | N2 | Y2 | Gap2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2023 | DeMar DeRozan / Nikola Vučević / Zach LaVine / Patrick Williams / Ayo Dosunmu | 593 | 110.62 | 6.68 | 605 | 114.88 | -1.63 |
| 2022 | Patrick Beverley / Karl-Anthony Towns / D'Angelo Russell / Jarred Vanderbilt / Anthony Edwards | 533 | 128.89 | 6.64 | 545 | 109.91 | -6.64 |
| 2025 | Russell Westbrook / Nikola Jokić / Jamal Murray / Michael Porter Jr. / Christian Braun | 395 | 132.41 | 5.94 | 371 | 122.64 | 5.26 |
| 2024 | DeMar DeRozan / Nikola Vučević / Alex Caruso / Coby White / Ayo Dosunmu | 477 | 106.50 | 5.47 | 446 | 111.88 | 5.47 |
| 2024 | Kyrie Irving / Derrick Jones Jr. / Luka Dončić / Daniel Gafford / P.J. Washington | 408 | 116.67 | 5.23 | 396 | 113.13 | 5.68 |
| 2018 | Jonas Valančiūnas / Kyle Lowry / DeMar DeRozan / Serge Ibaka / Norman Powell | 276 | 104.71 | 5.23 | 279 | 113.62 | 1.85 |
| 2016 | Kyrie Irving / LeBron James / J.R. Smith / Kevin Love / Tristan Thompson | 788 | 117.39 | 5.13 | 776 | 120.88 | 5.15 |
| 2026 | Jakob Poeltl / Brandon Ingram / RJ Barrett / Immanuel Quickley / Scottie Barnes | 350 | 125.14 | 4.80 | 376 | 127.39 | 4.80 |
| 2023 | Kentavious Caldwell-Pope / Aaron Gordon / Nikola Jokić / Bruce Brown / Michael Porter Jr. | 273 | 130.77 | 4.36 | 272 | 117.65 | 1.90 |
| 2016 | Kyle Korver / Paul Millsap / Al Horford / Jeff Teague / Kent Bazemore | 1051 | 104.38 | 4.34 | 1016 | 103.94 | 4.34 |

Structural remains worse in 8/10 second halves. Unweighted gap averages: first half 5.38, second half 2.62 pts/100. Cases sharing players are correlated.

## How to read the decompositions

**Additive:** calibrated league anchor + five calibrated player terms. A raw player term is profile/career + selected previous-season carry + career stage. The checkpoint combines profile and career; no invented separation is shown. These are regularized model coefficients, not causal player values. The calibration slope multiplies each term once.

**Structural:** prior usage profiles are scaled to a fixed team budget. Shot attempts, FTA, turnovers and assisted-finishing demand scale; ORB and passing supply do not. Predicted channel rates × prior-fitted conditional weights + valuation intercept + shooting surplus form the raw score. Then apply prior-only calibration and assist deficit. In particular the negative ORB weight is a known conditional-accounting weakness, **not** a claim that grabbing a rebound harms offense. The coherent rebound alternative is not the model being audited here.

**Location limitation:** “corner” in the underlying code is only a <=22-foot three-pointer proxy derived from text distance. It is not an observed x/y corner location; the >22-foot bucket can include corner shots. This report uses distance labels. Do not diagnose corner spacing from these categories as though we had tracking coordinates.

**Shooting-input limitation:** a non-shooter can have a league-shrunk 3P percentage while taking virtually no threes. The percentage alone is not a forecast that he can suddenly shoot; his attempt rate controls its contribution.

## Event forecasts across the entire screened sample

| Channel | Predicted | Actual | Bias | Season mean bias | Season sem | Positive seasons |
| --- | --- | --- | --- | --- | --- | --- |
| 3PA <=22 ft (corner proxy) | 0.84 | 0.88 | -0.04 | -0.04 | 0.26 | 4 |
| 3PA >22 ft | 28.11 | 31.23 | -3.12 | -3.15 | 0.40 | 0 |
| FTA | 24.32 | 19.45 | 4.87 | 4.78 | 0.42 | 11 |
| Long-midrange FGA | 10.45 | 9.59 | 0.86 | 0.75 | 0.28 | 7 |
| Midrange FGA | 9.48 | 9.36 | 0.11 | 0.12 | 0.22 | 7 |
| Paint FGA | 13.00 | 13.07 | -0.08 | -0.02 | 0.24 | 6 |
| Player ORB | 10.79 | 10.09 | 0.71 | 0.75 | 0.19 | 9 |
| Rim FGA | 26.90 | 26.52 | 0.38 | 0.50 | 0.46 | 6 |
| Turnovers | 13.83 | 13.68 | 0.15 | 0.15 | 0.17 | 7 |

Rates are events/100; bias = predicted − actual. Season SEM describes variation across the 11 seasons, not independent players. These are intermediate forecasts in the current point score, not recalibrated standalone channel models.

## Rank 1: 2025 — Russell Westbrook / Nikola Jokić / Jamal Murray / Michael Porter Jr. / Christian Braun

Top-six full-season error gap.

766 possessions / 31 games, 2024-11-08 to 2025-05-18. Actual **127.68**, additive **122.98**, structural **117.04**. Absolute errors 4.69 / 10.64; gap **+5.94**.

First 395 possessions: 132.41 actual, gap +5.94. Later 371: 122.64 actual, gap +5.26. Game-bootstrap 95% ranges: actual 118.36–136.59; gap -3.31 to +5.94. Largest single-game exposure: 6.1%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Russell Westbrook | 3.72 | -0.13 | -0.64 | 2.95 | 2.09 |
| Nikola Jokić | 5.70 | 0.44 | 0.20 | 6.34 | 4.47 |
| Jamal Murray | 4.09 | -0.04 | 0.20 | 4.24 | 2.99 |
| Michael Porter Jr. | 2.38 | -0.43 | 0.34 | 2.29 | 1.62 |
| Christian Braun | -0.82 | -0.09 | 0.12 | -0.79 | -0.56 |

Prediction = 30.427544 + 0.706284 × (116.013371 league + 15.031015 player sum) = **122.982147**. Equivalently, anchor 112.3660 + calibrated player sum 10.6162.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Russell Westbrook | 2024 | 27.95 | 23.53 | 50.57 | 33.81 | -0.59 | -0.27 | -0.26 |
| Nikola Jokić | 2024 | 32.88 | 27.68 | 62.11 | 36.37 | 4.96 | 0.06 | 0.44 |
| Jamal Murray | 2024 | 32.16 | 27.08 | 50.39 | 39.17 | 1.02 | 0.75 | 0.34 |
| Michael Porter Jr. | 2024 | 23.40 | 19.70 | 56.80 | 38.97 | 1.31 | 0.84 | 0.11 |
| Christian Braun | 2024 | 17.94 | 15.10 | 51.11 | 36.98 | -0.43 | 0.13 | -0.19 |

Native usage sum 134.3256 → budget 113.0853, common scale **0.841875**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **54.70% / 59.54%**; 3P **37.63% / 42.54%**; FT **78.29% / 79.58%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 27.10 | 30.68 | 0.57 | 15.33 | 11.60 |
| Paint FGA | 17.74 | 18.28 | 0.19 | 3.32 | 2.51 |
| Midrange FGA | 9.21 | 5.74 | 0.13 | 1.20 | 0.91 |
| Long-midrange FGA | 8.78 | 8.22 | 0.11 | 0.93 | 0.70 |
| 3PA <=22 ft (corner proxy) | 0.57 | 0.91 | 0.48 | 0.28 | 0.21 |
| 3PA >22 ft | 27.97 | 28.85 | 0.41 | 11.51 | 8.70 |
| FTA | 19.75 | 18.54 | 0.41 | 8.12 | 6.14 |
| Player ORB | 12.45 | 11.36 | -0.37 | -4.61 | -3.49 |
| Turnovers | 13.02 | 12.14 | -0.86 | -11.20 | -8.47 |

Raw score = valuation intercept 85.092153 + channels 24.868577 + shooting surplus 8.221649 = **118.182379**.

Assist supply 37.0689; assisted-finishing demand 26.8121; deficit max(demand − supply, 0) = **0.0000**. Final = 27.632830 + 0.756500 × 118.182379 + (-0.531819) × 0.000000 = **117.037853**.

Final accounting: anchor 92.0051 + valued channels 18.8131 + shooting 6.2197 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **-10.6384 = -2.1244** from channel-rate forecast discrepancies valued at the existing weights **+ -8.5140** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 2: 2024 — Kyrie Irving / Derrick Jones Jr. / Luka Dončić / Daniel Gafford / P.J. Washington

Top-six full-season error gap.

804 possessions / 39 games, 2024-03-05 to 2024-06-17. Actual **114.93**, additive **116.44**, structural **122.12**. Absolute errors 1.52 / 7.19; gap **+5.68**.

First 408 possessions: 116.67 actual, gap +5.23. Later 396: 113.13 actual, gap +5.68. Game-bootstrap 95% ranges: actual 108.26–122.12; gap -5.67 to +5.68. Largest single-game exposure: 4.6%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Kyrie Irving | 3.20 | 0.08 | -0.04 | 3.23 | 2.16 |
| Derrick Jones Jr. | 0.12 | 0.22 | 0.01 | 0.35 | 0.24 |
| Luka Dončić | 3.44 | 0.37 | 0.03 | 3.84 | 2.57 |
| Daniel Gafford | 0.55 | 0.12 | 0.03 | 0.69 | 0.46 |
| P.J. Washington | -0.17 | -0.99 | 0.03 | -1.14 | -0.76 |

Prediction = 34.554297 + 0.668593 × (115.499562 league + 6.981260 player sum) = **116.444113**. Equivalently, anchor 111.7765 + calibrated player sum 4.6676.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kyrie Irving | 2023 | 32.01 | 27.88 | 57.12 | 37.39 | 2.78 | 0.46 | 0.66 |
| Derrick Jones Jr. | 2023 | 16.12 | 14.04 | 57.63 | 36.00 | -0.04 | 0.02 | -0.05 |
| Luka Dončić | 2023 | 40.98 | 35.69 | 58.34 | 35.95 | 3.75 | 0.05 | -0.16 |
| Daniel Gafford | 2023 | 17.41 | 15.16 | 70.40 | 36.41 | 3.46 | 0.00 | -0.31 |
| P.J. Washington | 2023 | 23.39 | 20.37 | 52.28 | 35.58 | 0.74 | -0.05 | -0.07 |

Native usage sum 129.9144 → budget 113.1376, common scale **0.870863**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **59.17% / 58.72%**; 3P **36.32% / 31.91%**; FT **76.20% / 71.83%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 25.81 | 24.38 | 0.56 | 14.52 | 10.72 |
| Paint FGA | 16.81 | 17.16 | 0.18 | 3.09 | 2.28 |
| Midrange FGA | 9.61 | 10.70 | 0.13 | 1.23 | 0.91 |
| Long-midrange FGA | 5.32 | 6.22 | 0.11 | 0.57 | 0.42 |
| 3PA <=22 ft (corner proxy) | 0.28 | 0.87 | 0.49 | 0.14 | 0.10 |
| 3PA >22 ft | 30.26 | 34.20 | 0.41 | 12.45 | 9.19 |
| FTA | 29.13 | 17.66 | 0.41 | 11.96 | 8.83 |
| Player ORB | 12.03 | 11.69 | -0.37 | -4.43 | -3.27 |
| Turnovers | 12.24 | 14.18 | -0.86 | -10.50 | -7.75 |

Raw score = valuation intercept 84.960181 + channels 29.016977 + shooting surplus 11.254181 = **125.231339**.

Assist supply 26.7299; assisted-finishing demand 21.6317; deficit max(demand − supply, 0) = **0.0000**. Final = 29.658110 + 0.738326 × 125.231339 + (-0.562721) × 0.000000 = **122.119671**.

Final accounting: anchor 92.3864 + valued channels 21.4240 + shooting 8.3093 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **+7.1943 = +3.5746** from channel-rate forecast discrepancies valued at the existing weights **+ +3.6197** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 3: 2024 — DeMar DeRozan / Nikola Vučević / Alex Caruso / Coby White / Ayo Dosunmu

Top-six full-season error gap.

923 possessions / 32 games, 2023-12-02 to 2024-04-19. Actual **109.10**, additive **113.50**, structural **118.97**. Absolute errors 4.40 / 9.87; gap **+5.47**.

First 477 possessions: 106.50 actual, gap +5.47. Later 446: 111.88 actual, gap +5.47. Game-bootstrap 95% ranges: actual 103.51–114.83; gap +2.80 to +5.47. Largest single-game exposure: 4.8%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| DeMar DeRozan | 1.61 | 0.55 | -0.06 | 2.10 | 1.40 |
| Nikola Vučević | -0.22 | -0.36 | -0.04 | -0.62 | -0.42 |
| Alex Caruso | 0.79 | 0.15 | 0.01 | 0.95 | 0.63 |
| Coby White | 0.47 | 0.89 | 0.03 | 1.39 | 0.93 |
| Ayo Dosunmu | -0.50 | -0.75 | 0.00 | -1.25 | -0.83 |

Prediction = 34.554297 + 0.668593 × (115.499562 league + 2.572294 player sum) = **113.496310**. Equivalently, anchor 111.7765 + calibrated player sum 1.7198.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DeMar DeRozan | 2023 | 30.75 | 33.59 | 52.71 | 35.32 | 3.84 | -0.05 | 1.06 |
| Nikola Vučević | 2023 | 24.27 | 26.51 | 59.24 | 35.29 | 3.60 | -0.11 | 0.21 |
| Alex Caruso | 2023 | 12.59 | 13.76 | 56.08 | 36.68 | 0.21 | 0.14 | 0.10 |
| Coby White | 2023 | 19.60 | 21.42 | 54.60 | 37.28 | 0.62 | 0.46 | 0.18 |
| Ayo Dosunmu | 2023 | 16.35 | 17.86 | 57.95 | 34.78 | 0.70 | -0.15 | 0.09 |

Native usage sum 103.5702 → budget 113.1376, common scale **1.092375**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **55.72% / 51.87%**; 3P **36.15% / 34.23%**; FT **84.23% / 87.82%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 23.19 | 24.49 | 0.56 | 13.05 | 9.63 |
| Paint FGA | 12.12 | 13.87 | 0.18 | 2.23 | 1.64 |
| Midrange FGA | 12.07 | 8.23 | 0.13 | 1.55 | 1.14 |
| Long-midrange FGA | 13.68 | 8.56 | 0.11 | 1.46 | 1.08 |
| 3PA <=22 ft (corner proxy) | 0.78 | 1.52 | 0.49 | 0.38 | 0.28 |
| 3PA >22 ft | 29.34 | 34.56 | 0.41 | 12.07 | 8.91 |
| FTA | 19.76 | 16.90 | 0.41 | 8.11 | 5.99 |
| Player ORB | 6.36 | 7.04 | -0.37 | -2.34 | -1.73 |
| Turnovers | 13.27 | 11.38 | -0.86 | -11.38 | -8.41 |

Raw score = valuation intercept 84.960181 + channels 25.112899 + shooting surplus 10.892656 = **120.965736**.

Assist supply 28.0290; assisted-finishing demand 26.1754; deficit max(demand − supply, 0) = **0.0000**. Final = 29.658110 + 0.738326 × 120.965736 + (-0.562721) × 0.000000 = **118.970265**.

Final accounting: anchor 92.3864 + valued channels 18.5415 + shooting 8.0423 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **+9.8695 = -2.0073** from channel-rate forecast discrepancies valued at the existing weights **+ +11.8768** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 4: 2018 — Jonas Valančiūnas / Kyle Lowry / DeMar DeRozan / Serge Ibaka / Norman Powell

Top-six full-season error gap.

555 possessions / 35 games, 2017-10-19 to 2018-04-04. Actual **109.19**, additive **111.93**, structural **117.16**. Absolute errors 2.74 / 7.97; gap **+5.23**.

First 276 possessions: 104.71 actual, gap +5.23. Later 279: 113.62 actual, gap +1.85. Game-bootstrap 95% ranges: actual 100.24–116.80; gap -4.51 to +5.23. Largest single-game exposure: 8.5%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Jonas Valančiūnas | -0.92 | 0.09 | 0.00 | -0.84 | -0.70 |
| Kyle Lowry | 4.43 | 0.16 | 0.00 | 4.58 | 3.84 |
| DeMar DeRozan | 1.43 | 0.17 | 0.00 | 1.60 | 1.34 |
| Serge Ibaka | -0.26 | -0.03 | 0.00 | -0.29 | -0.24 |
| Norman Powell | 1.26 | 0.02 | 0.00 | 1.28 | 1.07 |

Prediction = 15.015220 + 0.836688 × (109.497884 league + 6.334362 player sum) = **111.930622**. Equivalently, anchor 106.6307 + calibrated player sum 5.2999.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Jonas Valančiūnas | 2017 | 22.73 | 19.00 | 55.10 | 36.29 | 1.61 | 0.00 | 0.20 |
| Kyle Lowry | 2017 | 27.48 | 22.97 | 52.08 | 39.32 | 0.51 | 0.92 | 0.38 |
| DeMar DeRozan | 2017 | 37.47 | 31.31 | 48.73 | 33.42 | 2.07 | -0.13 | 0.91 |
| Serge Ibaka | 2017 | 23.96 | 20.02 | 52.17 | 37.54 | 1.75 | 0.31 | 0.19 |
| Norman Powell | 2017 | 24.09 | 20.13 | 50.34 | 35.58 | -0.73 | -0.03 | 0.19 |

Native usage sum 135.7388 → budget 113.4319, common scale **0.835663**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **51.38% / 54.64%**; 3P **37.37% / 34.36%**; FT **82.17% / 76.74%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 25.36 | 21.98 | 0.55 | 13.84 | 11.14 |
| Paint FGA | 14.59 | 11.35 | 0.18 | 2.57 | 2.07 |
| Midrange FGA | 11.33 | 10.99 | 0.12 | 1.34 | 1.08 |
| Long-midrange FGA | 16.01 | 6.13 | 0.11 | 1.80 | 1.45 |
| 3PA <=22 ft (corner proxy) | 0.27 | 2.88 | 0.51 | 0.13 | 0.11 |
| 3PA >22 ft | 21.11 | 32.25 | 0.43 | 8.99 | 7.24 |
| FTA | 28.11 | 23.24 | 0.40 | 11.36 | 9.15 |
| Player ORB | 11.10 | 7.93 | -0.36 | -4.01 | -3.23 |
| Turnovers | 12.39 | 14.95 | -0.85 | -10.57 | -8.52 |

Raw score = valuation intercept 84.673295 + channels 25.451734 + shooting surplus 8.163698 = **118.288727**.

Assist supply 21.0913; assisted-finishing demand 19.6747; deficit max(demand − supply, 0) = **0.0000**. Final = 21.886766 + 0.805418 × 118.288727 + (-0.643814) × 0.000000 = **117.158623**.

Final accounting: anchor 90.0842 + valued channels 20.4993 + shooting 6.5752 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **+7.9694 = +0.3979** from channel-rate forecast discrepancies valued at the existing weights **+ +7.5715** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 5: 2016 — Kyrie Irving / LeBron James / J.R. Smith / Kevin Love / Tristan Thompson

Top-six full-season error gap.

1,564 possessions / 57 games, 2015-12-25 to 2016-06-19. Actual **119.12**, additive **117.39**, structural **112.25**. Absolute errors 1.73 / 6.87; gap **+5.15**.

First 788 possessions: 117.39 actual, gap +5.13. Later 776: 120.88 actual, gap +5.15. Game-bootstrap 95% ranges: actual 114.12–124.18; gap -1.40 to +5.15. Largest single-game exposure: 3.2%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Kyrie Irving | 4.77 | 0.11 | 0.07 | 4.95 | 4.02 |
| LeBron James | 8.55 | 0.05 | -0.99 | 7.61 | 6.18 |
| J.R. Smith | 3.18 | -0.03 | -0.99 | 2.16 | 1.75 |
| Kevin Love | 3.14 | -0.18 | -0.20 | 2.76 | 2.24 |
| Tristan Thompson | -0.23 | 0.33 | 0.07 | 0.17 | 0.14 |

Prediction = 17.047234 + 0.811173 × (106.046356 league + 17.656289 player sum) = **117.391524**. Equivalently, anchor 103.0692 + calibrated player sum 14.3223.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kyrie Irving | 2015 | 29.02 | 25.02 | 48.68 | 40.27 | 0.01 | 0.81 | 0.61 |
| LeBron James | 2015 | 38.53 | 33.22 | 51.65 | 33.50 | 0.93 | -0.40 | -0.32 |
| J.R. Smith | 2015 | 23.61 | 20.35 | 46.82 | 37.60 | 0.34 | 0.53 | 0.00 |
| Kevin Love | 2015 | 24.99 | 21.55 | 47.72 | 36.59 | -0.06 | 0.16 | 0.27 |
| Tristan Thompson | 2015 | 15.64 | 13.48 | 54.30 | 35.49 | 0.14 | -0.00 | -0.62 |

Native usage sum 131.7835 → budget 113.6121, common scale **0.862112**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **50.10% / 50.05%**; 3P **37.05% / 42.57%**; FT **75.15% / 72.76%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 26.84 | 27.81 | 0.55 | 14.66 | 11.07 |
| Paint FGA | 10.98 | 10.55 | 0.18 | 1.94 | 1.46 |
| Midrange FGA | 8.68 | 9.14 | 0.12 | 1.03 | 0.78 |
| Long-midrange FGA | 13.10 | 13.04 | 0.12 | 1.51 | 1.14 |
| 3PA <=22 ft (corner proxy) | 0.96 | 1.34 | 0.51 | 0.49 | 0.37 |
| 3PA >22 ft | 27.53 | 33.50 | 0.43 | 11.93 | 9.01 |
| FTA | 27.53 | 19.25 | 0.40 | 11.12 | 8.40 |
| Player ORB | 12.82 | 12.98 | -0.36 | -4.65 | -3.51 |
| Turnovers | 13.41 | 12.40 | -0.85 | -11.42 | -8.62 |

Raw score = valuation intercept 84.591094 + channels 26.602448 + shooting surplus 2.392770 = **113.586312**.

Assist supply 26.4492; assisted-finishing demand 20.6092; deficit max(demand − supply, 0) = **0.0000**. Final = 26.454279 + 0.755302 × 113.586312 + (-0.670484) × 0.000000 = **112.246222**.

Final accounting: anchor 90.3461 + valued channels 20.0929 + shooting 1.8073 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **-6.8714 = -0.5575** from channel-rate forecast discrepancies valued at the existing weights **+ -6.3140** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 6: 2024 — Jarrett Allen / Donovan Mitchell / Darius Garland / Max Strus / Evan Mobley

Top-six full-season error gap.

854 possessions / 32 games, 2023-11-03 to 2024-04-27. Actual **113.58**, additive **114.94**, structural **120.08**. Absolute errors 1.36 / 6.49; gap **+5.13**.

First 424 possessions: 115.57 actual, gap +3.89. Later 430: 111.63 actual, gap +5.13. Game-bootstrap 95% ranges: actual 107.90–119.93; gap -4.84 to +5.13. Largest single-game exposure: 5.2%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Jarrett Allen | -0.24 | 0.28 | 0.01 | 0.05 | 0.04 |
| Donovan Mitchell | 2.78 | 0.22 | 0.01 | 3.01 | 2.01 |
| Darius Garland | 1.86 | 0.67 | 0.03 | 2.56 | 1.71 |
| Max Strus | 0.84 | -0.86 | 0.03 | 0.00 | 0.00 |
| Evan Mobley | -0.78 | -0.11 | 0.00 | -0.89 | -0.59 |

Prediction = 34.554297 + 0.668593 × (115.499562 league + 4.737085 player sum) = **114.943674**. Equivalently, anchor 111.7765 + calibrated player sum 3.1672.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Jarrett Allen | 2023 | 18.21 | 16.39 | 64.16 | 35.67 | 2.54 | -0.00 | -0.12 |
| Donovan Mitchell | 2023 | 35.50 | 31.95 | 56.48 | 37.55 | 2.15 | 0.62 | 0.58 |
| Darius Garland | 2023 | 30.06 | 27.05 | 49.98 | 39.10 | 0.91 | 0.76 | 0.53 |
| Max Strus | 2023 | 19.25 | 17.32 | 56.31 | 35.55 | 0.37 | -0.08 | 0.18 |
| Evan Mobley | 2023 | 22.69 | 20.42 | 58.62 | 32.97 | 2.18 | -0.14 | -0.39 |

Native usage sum 125.7240 → budget 113.1376, common scale **0.899889**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **57.13% / 58.41%**; 3P **36.99% / 33.96%**; FT **79.39% / 79.34%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 26.86 | 30.56 | 0.56 | 15.11 | 11.16 |
| Paint FGA | 15.87 | 15.81 | 0.18 | 2.91 | 2.15 |
| Midrange FGA | 9.05 | 7.49 | 0.13 | 1.16 | 0.86 |
| Long-midrange FGA | 6.51 | 6.67 | 0.11 | 0.69 | 0.51 |
| 3PA <=22 ft (corner proxy) | 0.26 | 0.35 | 0.49 | 0.12 | 0.09 |
| 3PA >22 ft | 31.76 | 30.68 | 0.41 | 13.07 | 9.65 |
| FTA | 22.97 | 14.17 | 0.41 | 9.43 | 6.96 |
| Player ORB | 11.30 | 10.19 | -0.37 | -4.16 | -3.07 |
| Turnovers | 12.73 | 15.22 | -0.86 | -10.92 | -8.06 |

Raw score = valuation intercept 84.960181 + channels 27.416758 + shooting surplus 10.086058 = **122.462997**.

Assist supply 27.4795; assisted-finishing demand 26.2039; deficit max(demand − supply, 0) = **0.0000**. Final = 29.658110 + 0.738326 × 122.462997 + (-0.562721) × 0.000000 = **120.075731**.

Final accounting: anchor 92.3864 + valued channels 20.2425 + shooting 7.4468 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **+6.4926 = +2.8443** from channel-rate forecast discrepancies valued at the existing weights **+ +3.6483** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 9: 2016 — Kyle Korver / Paul Millsap / Al Horford / Jeff Teague / Kent Bazemore

Additional high-exposure case (>=1,500 possessions).

2,067 possessions / 80 games, 2015-10-27 to 2016-05-08. Actual **104.16**, additive **108.22**, structural **112.57**. Absolute errors 4.06 / 8.40; gap **+4.34**.

First 1051 possessions: 104.38 actual, gap +4.34. Later 1016: 103.94 actual, gap +4.34. Game-bootstrap 95% ranges: actual 99.95–108.11; gap +4.34 to +4.34. Largest single-game exposure: 2.4%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Kyle Korver | 2.38 | 0.81 | -0.99 | 2.20 | 1.78 |
| Paul Millsap | 2.25 | 0.52 | -0.23 | 2.54 | 2.06 |
| Al Horford | 0.54 | 0.20 | -0.23 | 0.51 | 0.41 |
| Jeff Teague | 2.04 | 0.07 | -0.20 | 1.90 | 1.54 |
| Kent Bazemore | -0.85 | -0.04 | 0.09 | -0.80 | -0.65 |

Prediction = 17.047234 + 0.811173 × (106.046356 league + 6.350719 player sum) = **108.220747**. Equivalently, anchor 103.0692 + calibrated player sum 5.1515.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kyle Korver | 2015 | 15.90 | 16.09 | 48.64 | 43.43 | 0.30 | 2.22 | 0.28 |
| Paul Millsap | 2015 | 26.17 | 26.49 | 49.83 | 35.36 | -0.28 | -0.06 | 0.00 |
| Al Horford | 2015 | 24.88 | 25.18 | 54.07 | 34.44 | 3.09 | -0.04 | 0.02 |
| Jeff Teague | 2015 | 28.20 | 28.54 | 48.81 | 34.74 | -0.55 | -0.15 | 0.72 |
| Kent Bazemore | 2015 | 17.11 | 17.31 | 48.88 | 35.32 | -0.60 | -0.11 | -0.51 |

Native usage sum 112.2582 → budget 113.6121, common scale **1.012060**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **50.79% / 51.58%**; 3P **38.32% / 34.76%**; FT **77.55% / 82.31%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 29.02 | 32.22 | 0.55 | 15.85 | 11.97 |
| Paint FGA | 12.73 | 7.31 | 0.18 | 2.24 | 1.70 |
| Midrange FGA | 7.18 | 6.97 | 0.12 | 0.85 | 0.64 |
| Long-midrange FGA | 13.82 | 11.85 | 0.12 | 1.59 | 1.20 |
| 3PA <=22 ft (corner proxy) | 1.71 | 1.50 | 0.51 | 0.88 | 0.67 |
| 3PA >22 ft | 23.54 | 30.09 | 0.43 | 10.20 | 7.70 |
| FTA | 23.28 | 13.40 | 0.40 | 9.40 | 7.10 |
| Player ORB | 7.81 | 8.13 | -0.36 | -2.83 | -2.14 |
| Turnovers | 15.37 | 15.05 | -0.85 | -13.09 | -9.89 |

Raw score = valuation intercept 84.591094 + channels 25.096711 + shooting surplus 4.321196 = **114.009001**.

Assist supply 28.4456; assisted-finishing demand 27.3447; deficit max(demand − supply, 0) = **0.0000**. Final = 26.454279 + 0.755302 × 114.009001 + (-0.670484) × 0.000000 = **112.565480**.

Final accounting: anchor 90.3461 + valued channels 18.9556 + shooting 3.2638 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **+8.4049 = +0.4259** from channel-rate forecast discrepancies valued at the existing weights **+ +7.9789** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 15: 2023 — Kentavious Caldwell-Pope / Aaron Gordon / Nikola Jokić / Jamal Murray / Michael Porter Jr.

Additional high-exposure case (>=1,500 possessions).

2,192 possessions / 61 games, 2022-10-19 to 2023-06-12. Actual **124.09**, additive **121.24**, structural **117.61**. Absolute errors 2.85 / 6.48; gap **+3.63**.

First 1103 possessions: 124.93 actual, gap +3.63. Later 1089: 123.23 actual, gap +3.63. Game-bootstrap 95% ranges: actual 119.40–128.66; gap -0.05 to +3.63. Largest single-game exposure: 2.5%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Kentavious Caldwell-Pope | 2.14 | -0.21 | -0.07 | 1.86 | 1.18 |
| Aaron Gordon | 2.52 | 0.26 | -0.07 | 2.71 | 1.72 |
| Nikola Jokić | 5.46 | 0.12 | -0.06 | 5.52 | 3.51 |
| Jamal Murray | 4.56 | 0.00 | -0.06 | 4.50 | 2.86 |
| Michael Porter Jr. | 3.41 | -0.09 | -0.07 | 3.25 | 2.07 |

Prediction = 38.171032 + 0.635628 × (112.848647 league + 17.834444 player sum) = **121.236843**. Equivalently, anchor 109.9008 + calibrated player sum 11.3361.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kentavious Caldwell-Pope | 2022 | 20.98 | 18.46 | 48.98 | 37.71 | 0.58 | 0.44 | 0.31 |
| Aaron Gordon | 2022 | 22.22 | 19.55 | 59.40 | 34.51 | 1.48 | -0.18 | -0.08 |
| Nikola Jokić | 2022 | 35.55 | 31.28 | 64.46 | 34.61 | 5.71 | -0.17 | 0.37 |
| Jamal Murray | 2021 | 28.29 | 24.89 | 53.04 | 39.29 | 1.89 | 0.87 | 0.36 |
| Michael Porter Jr. | 2022 | 21.58 | 18.99 | 51.98 | 33.96 | 0.69 | -0.41 | -0.08 |

Native usage sum 128.6181 → budget 113.1659, common scale **0.879860**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **57.08% / 59.04%**; 3P **36.33% / 39.38%**; FT **80.29% / 76.12%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 21.53 | 25.96 | 0.56 | 12.02 | 8.50 |
| Paint FGA | 14.98 | 17.93 | 0.18 | 2.68 | 1.89 |
| Midrange FGA | 8.99 | 8.03 | 0.13 | 1.12 | 0.79 |
| Long-midrange FGA | 11.81 | 8.90 | 0.11 | 1.27 | 0.89 |
| 3PA <=22 ft (corner proxy) | 0.27 | 0.50 | 0.49 | 0.13 | 0.09 |
| 3PA >22 ft | 32.70 | 31.93 | 0.41 | 13.48 | 9.52 |
| FTA | 20.18 | 18.34 | 0.41 | 8.26 | 5.84 |
| Player ORB | 10.44 | 10.36 | -0.37 | -3.82 | -2.70 |
| Turnovers | 14.02 | 12.14 | -0.86 | -12.01 | -8.49 |

Raw score = valuation intercept 84.871445 + channels 23.133748 + shooting surplus 11.796805 = **119.801998**.

Assist supply 28.6997; assisted-finishing demand 27.8222; deficit max(demand − supply, 0) = **0.0000**. Final = 32.954908 + 0.706600 × 119.801998 + (-0.537531) × 0.000000 = **117.607014**.

Final accounting: anchor 92.9251 + valued channels 16.3463 + shooting 8.3356 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **-6.4806 = -2.3036** from channel-rate forecast discrepancies valued at the existing weights **+ -4.1770** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 18: 2017 — Kyrie Irving / LeBron James / J.R. Smith / Kevin Love / Tristan Thompson

Additional high-exposure case (>=1,500 possessions).

1,525 possessions / 45 games, 2016-10-25 to 2017-06-12. Actual **120.92**, additive **116.93**, structural **113.63**. Absolute errors 3.99 / 7.29; gap **+3.29**.

First 755 possessions: 116.16 actual, gap +1.76. Later 770: 125.58 actual, gap +3.29. Game-bootstrap 95% ranges: actual 114.46–127.31; gap -1.64 to +3.29. Largest single-game exposure: 3.7%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Kyrie Irving | 4.50 | -0.32 | 0.16 | 4.35 | 3.34 |
| LeBron James | 8.70 | 0.29 | -1.93 | 7.06 | 5.43 |
| J.R. Smith | 3.23 | 0.07 | -0.97 | 2.33 | 1.79 |
| Kevin Love | 3.14 | 0.02 | -0.18 | 2.98 | 2.29 |
| Tristan Thompson | -0.09 | 0.09 | 0.16 | 0.17 | 0.13 |

Prediction = 21.795964 + 0.769215 × (106.783686 league + 16.889922 player sum) = **116.927592**. Equivalently, anchor 103.9356 + calibrated player sum 12.9920.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kyrie Irving | 2016 | 33.52 | 29.63 | 49.82 | 36.12 | 0.99 | 0.09 | 0.54 |
| LeBron James | 2016 | 35.54 | 31.42 | 57.04 | 33.67 | 1.76 | -0.30 | -0.28 |
| J.R. Smith | 2016 | 19.22 | 16.99 | 45.69 | 39.68 | 0.08 | 1.15 | -0.15 |
| Kevin Love | 2016 | 26.87 | 23.75 | 45.50 | 36.64 | -0.32 | 0.20 | 0.41 |
| Tristan Thompson | 2016 | 13.27 | 11.73 | 56.31 | 35.90 | 0.22 | -0.00 | -0.70 |

Native usage sum 128.4169 → budget 113.5239, common scale **0.884026**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **51.86% / 52.31%**; 3P **37.01% / 44.01%**; FT **74.70% / 75.65%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 28.95 | 25.11 | 0.55 | 15.78 | 11.01 |
| Paint FGA | 11.60 | 11.28 | 0.18 | 2.04 | 1.42 |
| Midrange FGA | 8.36 | 8.66 | 0.12 | 0.99 | 0.69 |
| Long-midrange FGA | 11.31 | 11.74 | 0.11 | 1.29 | 0.90 |
| 3PA <=22 ft (corner proxy) | 1.14 | 0.26 | 0.51 | 0.59 | 0.41 |
| 3PA >22 ft | 28.88 | 34.75 | 0.43 | 12.40 | 8.65 |
| FTA | 24.67 | 20.20 | 0.40 | 9.96 | 6.95 |
| Player ORB | 13.78 | 11.21 | -0.36 | -4.99 | -3.48 |
| Turnovers | 12.42 | 13.77 | -0.85 | -10.59 | -7.39 |

Raw score = valuation intercept 84.578188 + channels 27.474989 + shooting surplus 3.692228 = **115.745405**.

Assist supply 25.2776; assisted-finishing demand 22.1204; deficit max(demand − supply, 0) = **0.0000**. Final = 32.876710 + 0.697704 × 115.745405 + (-0.605377) × 0.000000 = **113.632765**.

Final accounting: anchor 91.8873 + valued channels 19.1694 + shooting 2.5761 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **-7.2853 = +1.4078** from channel-rate forecast discrepancies valued at the existing weights **+ -8.6930** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 132: 2025 — Jarrett Allen / Donovan Mitchell / Darius Garland / Max Strus / Evan Mobley

Same exact five in another season (not an independent player sample).

624 possessions / 27 games, 2024-12-31 to 2025-05-13. Actual **120.35**, additive **118.37**, structural **118.25**. Absolute errors 1.99 / 2.11; gap **+0.12**.

First 305 possessions: 121.31 actual, gap +0.12. Later 319: 119.44 actual, gap +0.12. Game-bootstrap 95% ranges: actual 109.95–130.87; gap -0.12 to +0.12. Largest single-game exposure: 6.1%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Jarrett Allen | 1.10 | 0.26 | 0.19 | 1.55 | 1.10 |
| Donovan Mitchell | 4.09 | -0.20 | 0.19 | 4.08 | 2.88 |
| Darius Garland | 2.59 | -0.53 | 0.34 | 2.40 | 1.70 |
| Max Strus | 1.17 | 0.14 | 0.34 | 1.66 | 1.17 |
| Evan Mobley | -0.91 | -0.44 | 0.15 | -1.20 | -0.85 |

Prediction = 30.427544 + 0.706284 × (116.013371 league + 8.497295 player sum) = **118.367482**. Equivalently, anchor 112.3660 + calibrated player sum 6.0015.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Jarrett Allen | 2024 | 21.97 | 19.63 | 62.88 | 36.35 | 2.76 | 0.00 | -0.11 |
| Donovan Mitchell | 2024 | 34.96 | 31.25 | 53.93 | 36.71 | 1.31 | 0.29 | 0.63 |
| Darius Garland | 2024 | 27.88 | 24.92 | 50.60 | 37.22 | 0.62 | 0.34 | 0.20 |
| Max Strus | 2024 | 18.61 | 16.63 | 55.33 | 35.86 | -0.06 | 0.01 | 0.08 |
| Evan Mobley | 2024 | 23.11 | 20.65 | 59.90 | 36.71 | 2.07 | 0.05 | -0.16 |

Native usage sum 126.5309 → budget 113.0853, common scale **0.893736**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **57.06% / 59.94%**; 3P **36.59% / 35.97%**; FT **78.88% / 79.67%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 29.94 | 23.40 | 0.57 | 16.93 | 12.81 |
| Paint FGA | 16.12 | 17.47 | 0.19 | 3.02 | 2.28 |
| Midrange FGA | 7.14 | 6.41 | 0.13 | 0.93 | 0.70 |
| Long-midrange FGA | 5.76 | 3.53 | 0.11 | 0.61 | 0.46 |
| 3PA <=22 ft (corner proxy) | 0.31 | 0.32 | 0.48 | 0.15 | 0.11 |
| 3PA >22 ft | 29.77 | 40.22 | 0.41 | 12.24 | 9.26 |
| FTA | 22.57 | 19.71 | 0.41 | 9.28 | 7.02 |
| Player ORB | 11.75 | 12.98 | -0.37 | -4.35 | -3.29 |
| Turnovers | 14.11 | 15.38 | -0.86 | -12.13 | -9.18 |

Raw score = valuation intercept 85.092153 + channels 26.680174 + shooting surplus 8.006587 = **119.778914**.

Assist supply 32.3315; assisted-finishing demand 27.3219; deficit max(demand − supply, 0) = **0.0000**. Final = 27.632830 + 0.756500 × 119.778914 + (-0.531819) × 0.000000 = **118.245633**.

Final accounting: anchor 92.0051 + valued channels 20.1836 + shooting 6.0570 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **-2.1069 = +1.6620** from channel-rate forecast discrepancies valued at the existing weights **+ -3.7689** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Rank 241: 2024 — Kentavious Caldwell-Pope / Aaron Gordon / Nikola Jokić / Jamal Murray / Michael Porter Jr.

Same exact five in another season (not an independent player sample).

2,404 possessions / 60 games, 2023-10-24 to 2024-05-19. Actual **124.21**, additive **118.68**, structural **121.70**. Absolute errors 5.53 / 2.51; gap **-3.02**.

First 1210 possessions: 126.86 actual, gap -3.02. Later 1194: 121.52 actual, gap -2.67. Game-bootstrap 95% ranges: actual 119.31–129.10; gap -3.02 to +1.76. Largest single-game exposure: 2.6%.

### Additive player coefficients

| Name | Profile + career | Prior-season carry | Career stage | Raw player coefficient | Final player contribution |
| --- | --- | --- | --- | --- | --- |
| Kentavious Caldwell-Pope | 1.01 | -0.36 | -0.04 | 0.61 | 0.41 |
| Aaron Gordon | 1.07 | 0.81 | 0.01 | 1.89 | 1.26 |
| Nikola Jokić | 2.99 | 1.28 | 0.01 | 4.28 | 2.86 |
| Jamal Murray | 2.22 | -0.29 | 0.01 | 1.95 | 1.30 |
| Michael Porter Jr. | 1.31 | 0.27 | 0.03 | 1.61 | 1.07 |

Prediction = 34.554297 + 0.668593 × (115.499562 league + 10.323962 player sum) = **118.679020**. Equivalently, anchor 111.7765 + calibrated player sum 6.9025.

### Structural usage and shooting inputs

| Name | Profile season | Native usage | Assigned usage | Prior 2P% | Prior 3P% | 2P surplus | 3P surplus | FT surplus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kentavious Caldwell-Pope | 2023 | 15.42 | 14.23 | 52.14 | 39.15 | 0.52 | 0.61 | 0.13 |
| Aaron Gordon | 2023 | 22.21 | 20.48 | 60.87 | 36.11 | 1.44 | 0.03 | -0.84 |
| Nikola Jokić | 2023 | 31.27 | 28.84 | 64.08 | 38.44 | 5.56 | 0.26 | 0.44 |
| Jamal Murray | 2023 | 29.85 | 27.53 | 50.83 | 38.80 | 1.26 | 0.82 | 0.39 |
| Michael Porter Jr. | 2023 | 23.92 | 22.06 | 56.32 | 38.79 | 1.21 | 0.97 | 0.11 |

Native usage sum 122.6726 → budget 113.1376, common scale **0.922272**. Shooting surplus columns are raw points/100 above league shooting for each player’s own predicted shot mix; percentages are shrunk prior overall 2P/3P%, not self-created shooting percentages.

Lineup predicted vs observed shooting: 2P **57.94% / 58.94%**; 3P **38.53% / 38.16%**; FT **76.94% / 80.33%**. Unclassified observed FGA: 0.00/100. Event scoring identity minus recorded ordinary points: +0.0000/100. Observed shooting is noisy and opponent-dependent; this comparison does not establish that a player’s underlying shooting skill changed.

### Structural channel ledger

| Label | Predicted events/100 | Observed events/100 | Conditional weight | Raw points | Final points |
| --- | --- | --- | --- | --- | --- |
| Rim FGA | 24.18 | 27.29 | 0.56 | 13.60 | 10.04 |
| Paint FGA | 16.00 | 16.64 | 0.18 | 2.94 | 2.17 |
| Midrange FGA | 8.05 | 9.65 | 0.13 | 1.03 | 0.76 |
| Long-midrange FGA | 9.32 | 9.44 | 0.11 | 0.99 | 0.73 |
| 3PA <=22 ft (corner proxy) | 0.42 | 1.12 | 0.49 | 0.20 | 0.15 |
| 3PA >22 ft | 32.38 | 30.16 | 0.41 | 13.32 | 9.83 |
| FTA | 23.21 | 17.55 | 0.41 | 9.53 | 7.04 |
| Player ORB | 10.92 | 11.31 | -0.37 | -4.02 | -2.97 |
| Turnovers | 12.59 | 12.19 | -0.86 | -10.80 | -7.97 |

Raw score = valuation intercept 84.960181 + channels 26.798669 + shooting surplus 12.908862 = **124.667711**.

Assist supply 32.4785; assisted-finishing demand 29.9534; deficit max(demand − supply, 0) = **0.0000**. Final = 29.658110 + 0.738326 × 124.667711 + (-0.562721) × 0.000000 = **121.703529**.

Final accounting: anchor 92.3864 + valued channels 19.7862 + shooting 9.5309 + deficit -0.0000.

Diagnostic error ledger (prediction − actual): **-2.5061 = +0.4513** from channel-rate forecast discrepancies valued at the existing weights **+ -2.9574** remaining scoring residual. The remainder combines shooting, valuation/calibration and omitted context; it does not isolate a causal shooting or gravity effect. Changing event rates would also change dependent making terms, so this is accounting, not a deployable correction.

## Reproduce

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.matched_disagreement
```

Separate CSV outputs retain all screened lineups, including structural wins, game totals, full-precision player/channel ledgers, and both selection lists. All reconstructed scores and observed totals must match the source benchmark within 1e-8 before this report is written. No scorer or benchmark source is changed.
