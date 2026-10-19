> **Historical architecture — 2026-09-18 notice:** This describes the
> **pre-neural structural prototype** as written on 2026-09-08. Its “current,”
> accuracy and absent-mechanism statements refer to that version. For implemented
> v14/v15 behavior read [NEURAL_MODEL.md](../../NEURAL_MODEL.md); for retained models
> read [current state](JOINT_CAPABILITY_STATE.md). Original body follows unchanged.

# The structural model, term by term

*Written 2026-09-08. `CURRENT_MODEL.md` is the same document for the **additive**
model embedded in `tool/five.html`; this is its counterpart for the structural
arm, which had no single-file spec until now. Read `CLAUDE.md` first for the
rules of evidence, `CONTEXTUAL_MODEL.md` for the product contract.*

The structural model prices a five-man lineup by **simulating a possession's
accounting** rather than by summing player ratings. Every quantity in it is a
rate a broadcast would recognise, and its central constraint — that five men
share one possession — is an identity enforced to 1e-11, not a fitted effect.
That constraint is the entire reason the model exists: it is the only mechanism
on this project that prices an unseen lineup without inheriting the
selection-on-the-outcome bias that ruins every fitted composition structure
(`RESEARCH_OVERVIEW.md` §20.5).

**It is also, today, less accurate than the plain additive model.** That tension
is the subject of §6.

---

## 1. The pipeline

`experiments/asof_point_allocation.py:38`, `predict()`. Pure: no fitting, no
I/O. The caller owns strictly prior profiles, valuation and calibration.

### Stage 1 — five player profiles

`PROFILE_FIELDS` (`asof_point_allocation.py:19`), all empirical-Bayes shrunk and
built strictly before the origin by `asof_state.PlayerHistory.snapshot`:

| field | meaning |
|---|---|
| `usage` | share of team possessions the player consumes |
| `rtov` | turnovers per possession |
| `own_ftr` | free-throw rate per field-goal attempt |
| `r3pa` | three-point attempts per possession |
| `rorb` | offensive rebounds per possession |
| `rast` | assists per possession (the passing SUPPLY) |
| `self_2p`, `self_3p`, `ft_pct` | conversion rates |
| `assisted` | share of his makes that are assisted (the DEMAND) |
| `shot_rim`, `shot_paint`, `shot_mid`, `shot_longmid` | two-point location mix |
| `shot_c3`, `shot_ab3` | three-point location mix |

Each mix is normalised to sum to 1 **per player**
(`channel_points_validation.py:107`). Nothing about the lineup changes it — see
§6 and `TEAMMATE_INFLUENCE_EXPERIMENT.md` §8i.

### Stage 2 — the shared usage budget

Each player's creation vector is scaled by `budget / Σ usage`, so a lineup of
five high-usage players does not get five high-usage seasons. The four team
components

    COMPONENTS = ('2PA', '3PA', '0.44 FTA', 'TO')

must sum to the budget, checked to `TOLERANCE = 1e-11`
(`asof_point_allocation.py:130`). The budget is frozen once per season at the
Q1 start (`onfloor_influence.frozen_usage_budget`), an accounting anchor rather
than a league forecast.

**This is the model's load-bearing idea.** Offensive rebounds are deliberately
NOT in the budget: a rebound generates another opportunity rather than
consuming one.

**The mixing rule is one scalar, and it asserts lineup-invariant shares.**
Measured leave-one-unit-out on 6.8M usage events over 3,266 units: observed
slope **1.0574** against the asserted 1.000, so shares amplify — a high-usage
player takes ~0.5pp more than proportional and the rest give up ~0.2pp
(§14). Right to within 6%; a softmax with a learned temperature contains this
rule as its temperature-1 case. Not a 5-Shaq lever: five identical players split
the ball five ways under any symmetric rule.

### Stage 3 — category calibration

`team_components` targets rescale the four components; player shares WITHIN each
category are preserved, each player's total usage is not
(`asof_point_allocation.py:140`). This is the seam through which every mechanism
in the influence workstream enters — `onfloor_influence_score.shift_components`
moves a component and renormalises so the budget survives exactly.

### Stage 4 — valuation

Nine channels, `VALUATION_CHANNELS` = six shot locations + `fta` + `orb` +
`tov_ev`, priced by a date-aware league value vector
(`asof_environment.EnvironmentHistory`). Then a separate **making-above-shot-mix
expectation** term, which is what makes a good shooter worth more than his
attempts:

    2 * 2PA * (self_2p - two_mix @ league_pct_by_location)
    3 * 3PA * (self_3p - three_mix @ league_pct_by_location)
    FTA     * (ft_pct  - league_ft_pct)

A player is credited only for making MORE than the league makes from the places
he shoots from. **This term also cancels the shot mix** — see §6.4 and
`TEAMMATE_INFLUENCE_EXPERIMENT.md` §8j. The two-point score decomposes exactly
as `2*2PA*self_2p + Σ_b 2PA_b*(value_b − 2*pct_b)`, and the first term has no
mix in it, so location reaches the score only through the spread of the second,
which is 0.079 rather than the 0.548 of the valuation alone.

### Stage 5 — the assist deficit

    deficit = max(passing DEMAND - passing SUPPLY, 0)

where demand is `Σ expected_makes * assisted` and supply is `Σ rast`. A lineup
of five men who all need someone else to create for them is charged. It enters
the calibration with a sign-constrained non-positive price.

### Stage 6 — the point calibration

`asof_point_calibration.fit_point_calibration`, fitted on origins strictly
before the current one:

    prediction = league + a + b * score + d * deficit,   b >= 0, d <= 0

---

## 2. What it scores

All figures: 5,607 cells / 726,364 possessions, seasons 2016+, the centered
quarterly run (`experiments/cache/asof_points_centered_2026`). Lower MAE better.

| arm | MAE | r² | provenance |
|---|---|---|---|
| **structural, parent** | **8.1440** | **0.1073** | `onfloor_influence_metrics.csv` |
| + on-floor influence, priced | 8.1333 | 0.1117 | §6, `priced_all` |
| + shot quality | **8.1321** | 0.1100 | §10c, `shot_quality_points_metrics.csv` |
| + turnover influence | 8.1446 | 0.1076 | §11d, does NOT convert |
| **corrected additive** | **8.0920** | **0.1204** | `saved_additive` |
| 50/50 blend | 8.0763 | 0.1219 | `onfloor_blend_metrics.csv` |
| **blend + opponent-adjusted target** | **8.0417** | **0.1276** | `onfloor_opponent_metrics.csv` |

On the **novel** slice (2,073 cells) the assembled arm reaches **8.8612**
against the parent's 8.8903 (−0.0298 ± 0.0194, **9/11 seasons**) and the
additive's 8.9039 — the one comparison in §16 whose season count is convincing.
The pooled additive lead is unchanged at 0.042 ± 0.033.

Defence, separate population (8,340 fives / 1,010,779 possessions):

| arm | MAE | provenance |
|---|---|---|
| league null | 8.6219 | `onfloor_defense_metrics.csv` |
| additive defensive half | 8.3398 | 11/11 seasons |
| influence channels | 8.3984 | 11/11 seasons |
| free-throw placebo | 8.6219 | identical to the null to 1.6e-16 |

---

## 3. What each mechanism is worth

In pts/100 of lineup spread, which is the unit that decides whether a term can
matter at all:

| mechanism | spread | status |
|---|---|---|
| **location-specific conversion** | **0.61 spread, slope 0.635** | §12b — **BUILT, works, orthogonal to shot quality** |
| location mix (six buckets) | ~0.006 per attempt moved | §8j — cancelled on a FLAT curve; live on a per-bucket one |
| opponent schedule | ~0.035 MAE | **banked**, coefficient 1, no fitting |
| shot quality | 0.91 | §10 — forecasts 1.082, prices right, not shipped |
| turnover influence | 0.81 | §11d — forecasts 0.434, prices to ZERO |
| on-floor influence layer | ~0.4 | §6 — priced at c≈0.39 in 44/44 origins |
| 2-vs-3 attempt swap | 0.0137 | the model is nearly indifferent, by design |

---

## 4. What is NOT in the model

- **`stl`, `drb`, `blk`, fouls.** They exist in `game_player_stats`; the profile
  never reads them (§11).
- **Defence, structurally.** The defensive half is a separate additive-style
  model, not this pipeline run in reverse.
- **Any lineup-dependence of the shot mix** — and it would not matter if there
  were, because the mix is cancelled out of the score (§8j).
- **Location-specific conversion** is measured and priced (§12) but is not in
  `asof_point_allocation` itself; it is applied as an exact making-term
  replacement in `location_points.py`, nested to 1.4e-14.
- **Shot quality.** Measured, forecasting, priced — still not in the scorer.
- **Lineup-dependent uncertainty.** The coverage gate is asserted;
  `distance_shrink.py` showed the decay cannot be fitted on this corpus.

---

## 5. Reproduce it

```bash
cd /Users/adam/Documents/basketball
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_influence_score
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_blend
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_opponent
```

Every arm rebuilds the parent from profiles and gate-checks it against the saved
cells to 1e-6 before scoring anything; observed reproduction is 1e-13 to 1e-14.
An arm that cannot reproduce the parent raises rather than reporting.

---

## 6. The honest weaknesses

1. **It loses to the additive model on the pooled set**, 8.1321 at best against
   8.0920 (+0.042 ± 0.033, 3/11 seasons). Nothing in this workstream closed that
   gap. On NOVEL lineups the ordering is the other way — assembled 8.8612
   against the additive's 8.9039 — but at ±0.074 with 6/11 seasons that is a
   point estimate, not a result (§16).
2. **The two arms are redundant.** Forward errors correlate **0.9856**, and
   neither arm's score explains the other's error. The whole prize from optimal
   ensembling is 0.15% of RMSE. So a better structural model is not
   automatically a better product — the blend already holds nearly everything
   both contain.
3. **The evaluation cannot resolve what is being built.** This population
   establishes a lever worth ~0.04 MAE and cannot establish one worth ~0.01
   (§10c). Shot quality, on-floor influence and turnover influence are all in
   the second class.
4. **The model asserts a player's FG% does not depend on where he shoots.**
   `self_2p` is a scalar, so the six location buckets cancel out of the score:
   moving an attempt from a long two to the rim is worth +0.006, not the +0.548
   the valuation alone suggests (§8j). §12 shows the resulting per-attempt
   predictor is WORSE than ignoring the player and using the league's rate at
   that location (Brier 0.2414 against 0.2343, 12/12 seasons). §12b replaces it
   and the term prices at slope 0.635 orthogonal to the parent, orthogonal also
   to shot quality (−0.030), placebo +0.004. **This is the first mechanism in
   the workstream that adds rather than re-prices.** It is not yet in the
   allocation itself.
5. **A channel that forecasts need not pay.** §11d: turnover influence forecasts
   at 0.434 over 3.0M possessions, 12/12 seasons, and its point-level slope
   orthogonal to the parent is **−0.028**. The player-level attribution was new;
   the lineup total was not, and points see only the total.
