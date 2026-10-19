# Bounded offensive and uncertainty diagnoses alongside v15

2026-09-17. These are retrospective diagnostics of **completed v14**, not v15
training results, new fitted corrections, or reasons to change the frozen v15
design. Source: `experiments/joint_capability_v15_companion.py`; completed
outputs/log/receipt under
`experiments/cache/joint_capability_2026_09_17_v15_companion_v2/`.
The first prefix is preserved after a path-resolution failure: reused ROLE_SL
fits live in v13 and must be resolved through their reference records.

## 1. The fixed Cleveland failure is primarily an action-allocation problem

The previously reviewed Irving/LeBron/Smith/Love/Thompson unit,2016q2–q4,
supplies1,332 jointly complete event possessions (1,564 total point possessions).
The table averages the three seeds and weights quarters by those same1,332
known-label possessions. It does not select a new case from the v15 results.

| Stage / target | FGA/100 | FTA/100 | TO/100 |
| --- | ---: | ---: | ---: |
| Sum of five dated raw profiles |103.579|30.581|14.778|
| Profiles normalized to common usage budget |88.392|26.093|12.608|
| Combined model, learned own decoder only, before renewal |88.288|26.206|12.663|
| With teammate messages, before renewal |88.724|24.656|12.909|
| With constraints, before renewal |88.724|24.656|12.909|
| With rebound renewal, full model |89.597|24.898|13.036|
| Observed on joint-complete labels |95.270|19.520|11.637|

The raw five demand1.318 actions per possession under the FGA+.44FTA+TO
convention; normalization reduces that to the1.125 league reference. That is
not itself a bug: simply accepting all five historical usages would overspend
the available possessions. But it exposes the decision the model must learn:
**which actions give way when these players share a court?**

Here it retains too many free throws and turnovers, and too few field-goal
attempts. Learned own adjustments barely alter normalized shares; teammate
effects move in the right direction but insufficiently. Renewal adds about
.87FGA/100. Turning off creation/load constraints changes none of these rates
for this case, so weakening those penalties is not a supported fix.

The FGA deficit has an exact accounting decomposition:

`FGA error = usage-budget error − .44×FTA error − turnover error`.

Of the roughly5.67missing FGA/100, about1.91 comes from lower total modeled
usage,2.37 from excess FT usage, and1.40 from excess turnovers. This is
bookkeeping, **not** a causal recoverable-gain estimate. In particular, the
completed clock diagnostic says some FT difference reflects deployment; its
residualized targets are not themselves a new generative event ledger.

An independent replay of the eligible rebound labels on those same1,332
possessions finds11.637observed ORBs/100 versus9.888predicted. The1.75ORB
shortfall accounts for most of the1.91usage-budget deficit under the stationary
renewal convention; the remaining non-rebound-budget discrepancy is about.16.
This is one reason defensive rebound opposition is worth testing, although
it does not establish that opponents explain the error. Recovery probabilities,
miss volume, phase effects and offensive facilitation can all contribute.

This supports a future focused test of **context-dependent allocation of
action types**, rather than removing resource conservation, hand-adjusting
Cleveland, or broadening an undiagnosed network. It does not establish that
the same allocation change would help all lineups. The actual-opponent
experiment proceeds unchanged and can reveal how much of this residual is
associated with defense.

## 2. Persistent error is not just finite-game shooting noise

For183same-five/season units with at least two>=200-possession quarters,
construct383pairs of nonoverlapping quarters. Take the product of their point
forecast errors, average pairs within each unit, then average within seasons.
The interval bootstraps the11seasons. A second statistic first removes the
quarter-wide mean error on the substantial-cell population.

| Forecast | Cross-quarter error product | After quarter-bias removal,95% season interval |
| --- | ---: | ---: |
| Additive |9.161|5.756 [1.991,9.836]|
| RB_RENEW_FAC HALF |8.028|5.058 [1.200,8.741]|
| Combined SHIFT HALF |8.099|5.194 [1.457,9.154]|

Units are `(points per100)²`. Positive products indicate errors that tend to
persist in the same direction. The positive centered intervals challenge the
idea that all remaining error is independent quarter-to-quarter sampling noise.
They do **not** identify a latent-quality variance or prove a difference
between models: the contrasts have not been tested here, and fitted-state
error, opponent schedules, deployment, persistent omitted context and changing
true lineup quality can all contribute.

These are selected recurring high-exposure lineups. They cannot validate an
uncertainty interval for a never-played five-center lineup. Quarter demeaning
uses retrospective outcomes only for this diagnostic; it never enters a
forecast. Do not take a square root of this table and ship it as a universal
uncertainty floor.

The practical implication is narrower and important: continue reporting
finite-game intervals and seed variation, but do not interpret their narrowing
with more possessions as proof that hypothetical lineup quality is known.
Latent/OOD uncertainty remains an explicit unmet product standard.
