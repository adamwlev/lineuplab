# Why the reference rates five centers highly, and a property-suite baseline — 2026-10-09

Exploratory diagnosis on saved weights; no refits. Model: J_POINT_BOTH at the
2026q4 origin, the mixture of all saved checkpoints across seeds 17, 23 and 41
(14 states). Points are native per 100 starting possessions, before
calibration and the additive blend. Players use origin-dated states. A
"neutral defense" is five identical average defenders (zero standardized
defensive inputs, so every defensive effect is zero). Switch-offs are
accounting on fixed weights, not causal effects.

Reproduce: `PYTHONPATH=. python -u scripts/diagnose_centers.py` and
`PYTHONPATH=. python -u scripts/defense_analogues.py`. Outputs are in
`experiments/cache/diagnose_centers_2026_10_09/` and
`experiments/cache/defense_analogues_2026_10_09/`.

## Findings

**1. On offense alone, the centers already lose.** Against the neutral
defense the five legal centers (Gobert, Adams, Robinson, Capela, Allen) score
115.8. That is the 20th percentile of the 206 real 2026q4 offensive fives with
at least 50 possessions (median 119.7, p10 112.3). The Jokić/Murray/Gordon/
Porter/Westbrook lineup scores 126.5 (94th percentile). The neutral margin is
−10.6 for the centers.

**2. Defense flips the sign.** In the matchup the native margin is +4.3 for
the centers, and +4.4 against the Korver variant. The centers' defense takes
10.9 points from the Jokić lineup. The Jokić lineup's defense gives the
centers 4.1 more than a neutral defense would.

Switching on the centers' defensive effects one group at a time, for the
Jokić/Westbrook lineup:

| Effect group | Change in Jokić-lineup points |
| --- | ---: |
| Conversion (make probabilities) | −4.9 |
| Rebound recovery (offensive rebounds lost) | −3.3 |
| Location (rim attempts pushed to mid-range) | −2.3 |
| Actions (FGA, FTA, turnover rates) | −0.7 |
| All together | −10.9 |

**3. The cause is near-additive extrapolation, not saturation.**

- *Inputs.* The centers' mean defensive descriptors sit far outside real
  lineups: mean blocks +5.0 SD and mean defensive rebounds +5.7 SD relative to
  real 2026q4 defensive fives. Their Mahalanobis distance is 11.7; the real
  maximum is 10.6 and the median 5.8.
- *Not saturation.* Pre-activations of the bounded heads stay below 0.5 in
  absolute value, and essentially no hidden units are saturated. The heads are
  in their near-linear range.
- *Which head.* The adjusted-capability head reads the mean of the five
  defenders' lineup-adjusted coefficients. Alone it moves the Jokić lineup by
  −7.1; the raw-descriptor head alone by −4.4.
- *Only mildly sub-additive.* Start from each of 36 heavily used real 2026q4
  defenses without these centers and put all five centers in:
  - The Jokić/Westbrook lineup loses 8.0 points on average (range −15.6 to
    +1.8), against 9.5 for the five single swaps added up.
  - Its rim make falls 5.0 percentage points, against 6.0 for the singles
    summed.

  So five centers count for roughly four centers' worth of rim deterrence
  and rebounding. Opponent three-point accuracy falls 0.3 percentage points rather than
  rising.

**4. The broadcast shape removes the coverage cost.** Against the centers, the
Jokić lineup takes more threes: Jokić's three-point share goes from .28 to .37,
and Porter's from .53 to .61. That direction is plausible. But three-point
accuracy does not rise, because one shift is applied to every attacker and the
centers' shift lowers perimeter conversion slightly. Nothing in the model says
a center is left guarding Murray on the perimeter.

**5. The offense's creation constraint barely binds.** The fitted
shortage-penalty coefficients are small in all three seeds: k_supply 0.13,
k_ft 0.11, k_load 0.01–0.07. The model detects the shortage, but the penalty
moves conversion by only about 0.05 logit. The teammate path does carry
creation: Jokić plus four centers scores 124.1, higher than the real Minnesota
lineup (121.7), and replacing Jokić with Allen costs 8.3.

**6. Observed analogues cannot settle it.** Every game × offense × defense
row in the 44 primary quarters (2016–2026, 2.76M possessions) was grouped by
defensive size, using listed heights from `nba.players`. Residuals are
actual minus the reference forecast, in points per 100, possession-weighted.
Uncertainty is the season-level SE over 11 seasons.

| Defensive bigs (6'10"+) | Possessions | Residual | Season SE |
| --- | ---: | ---: | ---: |
| 0 | 598,687 | −0.28 | 0.16 |
| 1 | 1,611,902 | −0.86 | 0.16 |
| 2 | 523,704 | −0.97 | 0.18 |
| 3+ | 26,253 | −0.39 | 1.80 |

The planned interaction compares two residual gaps: two-plus-big defenses
against spread offenses (4+ players with at least 4 3PA per 100) versus
non-spread offenses, minus the same gap for smaller defenses. It is −0.20 ±
0.43, positive in 4 of 11 seasons. On observed lineups, nothing shows the
broadcast defense mispricing big defenses against spread offenses. Three-big
defenses are too rare to say anything.

All rows sit at about −0.7 because calibration is fit on cells with at least
50 possessions, and small cells score lower. This is consistent with the
selection lead in STATUS (coaches keep lineups that are working).

## Property-suite baseline

`lineups/properties.py` defines directional properties: real lineups are
perturbed in a basketball-meaningful way, and the forecast must move in a
declared direction. The directions were written before the first run.

Two kinds of change were made after that run, and both are marked post hoc:

- A teammate-turnover property was added.
- The three ladder properties were rewritten as synergy comparisons. The
  ladder versions compared successive steps, which mixed the number of copies
  with which player was replaced. On defense they also added newcomers
  best-first, so an additive model could pass or fail them by construction.
  Their first-run pass rates (.76–.98) are not interpretable. The base lineups are
the real offense and defense fives with at least 50 possessions in each
origin's quarter (195–235 per origin). Defensive properties are scored
against the 40 most-used real offenses. Model: the same native checkpoint
mixture. Run: `PYTHONPATH=. python -u scripts/property_suite.py 2024q4 2025q4
2026q4`.

| Property (required direction) | 2024q4 | 2025q4 | 2026q4 |
| --- | ---: | ---: | ---: |
| spacing_rim: top shooter out, teammates' rim make must not rise | 1.00 | 1.00 | 1.00 |
| handler_conversion: top passer out, others' make must not rise | .98 | .98 | .98 |
| handler_turnovers: top passer out, team turnovers must not fall | .71 | .47 | .40 |
| handler_teammate_turnovers (post hoc): others' turnovers must not fall | 1.00 | .99 | 1.00 |
| clone_synergy: k copies of the star gain no more than k single copies summed | .96 | .97 | .99 |
| rim_synergy: k added rim protectors do no more than k single additions summed | 1.00 | 1.00 | 1.00 |
| rebound_synergy: same, for opponent offensive rebounds | 1.00 | 1.00 | 1.00 |
| perimeter_coverage: center for the shortest defender, opponent 3P% must not fall | .68 | .57 | .81 |
| coverage_targeting: that swap helps shooters more than non-shooters | .34 | .24 | .56 |
| permutation: slot order does not matter | 1.00 | 1.00 | 1.00 |

Readings:

- **Teammate directions on offense are right.** Spacing, creation and the
  transfer of ball-handling to teammates move the right way in almost every
  case.
- **The turnover failure is mostly mis-specification.** When the top passer
  leaves, the other four's turnovers rise in every case. Team turnovers still
  fall in about half the cases, because low-assist players have lower own
  turnover rates (median 8% of their usage, against 14% for the passers they
  replace). The post-hoc teammate version isolates the basketball claim.
- **Diminishing returns hold in range, and only mildly at the extreme.**
  Adding up to three rim protectors or rebounders to a real lineup always does
  less than the single additions summed, and stacked star copies gain less
  than single copies summed. At the five-center extreme, though, the joint
  effect is still about 84% of the singles summed (finding 3).
- **Perimeter coverage is neutral.** Replacing a lineup's shortest defender
  with a non-spacing center moves opponents' three-point accuracy by about
  zero (median −0.06 to −0.17 percentage points). It falls by more than the
  0.2-point tolerance in 19–43% of cases.
- **Targeting is at chance**, as expected for a broadcast defense.

These rates are the pillar-2 baseline for new arms. On real lineups, the
reference fails only the coverage properties (and the mis-specified team
turnover property). The fixtures fail because a
mildly concave, coverage-blind defense is extrapolated far beyond the data.

## What this means

- **The fix is mainly in defense.** Offense alone already ranks the centers
  low. The defense extrapolates rim protection and rebounding almost
  additively, and it has no notion of who guards whom. The second gap is
  the bigger one: nothing charges the centers for guarding the perimeter.
- **The data in range cannot choose the shape.** Fits on the 2016–2026 window
  see almost no lineups with three or more bigs on defense. The decision of
  record covers exactly this case: declare a structure (rim protection as a
  finite resource, perimeter coverage as a weakest link or an assignment),
  then test it on the closest real analogues.
- **One analogue test has real power: leave-structure-out.** Train without
  rows whose defense has two or more bigs, then forecast those rows (524k
  possessions, season SE about 0.2). This checks whether an aggregation
  extrapolates from one big to two, and it needs no new data.
- **Offense is still optimistic.** Five centers at the 20th percentile, and
  Jokić plus four centers above a real top lineup, are too generous by Adam's
  prior. The creation constraint is present but nearly inert. An initiator or
  finite-rim structure is the matching offensive test.
- **Distance is measurable.** The defensive inputs of the legal centers, five
  Goberts and five Jokićs lie beyond the real maximum Mahalanobis distance;
  the "limited centers" fixture sits at the real extreme. That is a candidate
  signal for the "far from observed" reason in the uncertainty band.
