> **Scope notice — 2026-09-18:** This is the shipped **additive-based baseline**
> specification, written in September 2026—not the current neural research model.
> Its historical pair terms, coverage gate, data snapshot and conclusions do not
> override the [product contract](CONTEXTUAL_MODEL.md). For the latest research,
> read [current state](JOINT_CAPABILITY_STATE.md), [neural architecture](../../NEURAL_MODEL.md)
> and [scorecard](../../MODEL_SCORECARD.md). Original document body follows unchanged.

# The current state of the model

*Written 2026-09-03 and corrected after the end-to-end audit. Read
`CLAUDE.md` first for the rules of evidence. This file documents the
**incumbent shipped baseline**; `CONTEXTUAL_MODEL.md` is the active product and
research contract. `RESEARCH_OVERVIEW.md` has the derivations and `BACKLOG.md`
has what is open.*

This describes the additive configuration currently embedded in
`tool/five.html`. It is the reproducible benchmark for the contextual model,
not a claim that its asserted coverage gate, pair-history term, or uncertainty
scheme is the finished product.

---

## 1. What it predicts, and how to read the numbers

One **possession** at a time: 5.57M of them, 2002–2025. The target is points
scored on that possession (0, 1, 2, 3…) after two nuisances are removed — the
league mean for that (season, week), and home-court advantage. So the model
predicts how much better or worse than a league-average possession this one
should be, given the ten players on the floor.

A single possession is nearly unpredictable. `var(y) = 1.2807`, and almost all
of it is "who took the shot and did it go in". That is why every r² here looks
tiny. Effects in this project live at 10⁻⁴ r²; **that is the scale of the
phenomenon, not a failure.**

The conversion that makes them legible, used throughout:

```
pts/100 of lineup spread  =  100 × sqrt( delta_r2 × var_y ),   var_y = 1.2807
```

r² = 0.001 is 3.6 points per 100 possessions of genuine spread between
lineups. **These are standard deviations of a term's contribution, so they add
in quadrature, not linearly.**

Every number below is measured **forward in time** — fit on the past, scored on
a future the model has never seen. Numbers from a random game split are not
deployable and are not quoted here; see `CLAUDE.md` rule 1b.

---

## 2. The whole model

For a lineup of five on offense against five on defense:

```
predicted points/possession =

      SUM over the 5 offensive players    theta_off(p)      per-player rating
    + SUM over the 5 defensive players    theta_def(q)      per-player rating

    + SUM over the 10 offensive pairs     c(i,j)            measured chemistry
    + hinges( SUM of career usage rates )                   usage conservation

  where  theta(p) = Z_p . gamma  +  beta_p  +  delta_(p,season)  +  eta_(exp bin)
                    box score       career     this season         career stage
```

Four separately-penalised blocks. Every corner is **nested**: send a penalty to
1e18 and that block disappears exactly, so any comparison is one argument wide.

`theta_def` is the effect of a defender being on the floor on points *scored by
the offense*, so a good defender's coefficient is negative and a lineup's net
rating is `SUM theta_off − SUM theta_def`.

**Why it is fast.** A player-season column is nonzero only inside its season,
so `X'X` is exactly block diagonal by season. The Schur complement collapses
via `G − G D⁻¹ G = alpha_d · G D⁻¹` into a 4,886² assembly instead of 30,000².
Exact, not iterative. `G_{A∪B} = G_A + G_B` also makes a fit on any prefix of
seasons a subset sum of blocks built once — which is what makes rolling-origin
evaluation affordable at all.

---

## 3. The additive core — the big half

Season-ahead protocol: fit ≤ T−1, penalties chosen on T−1, score T, 16 rolling
origins. Each row is the **paired** gain over the base, not a running total.

| term | what it does | Δr² | pts/100 | t | seasons |
|---|---|---|---|---|---|
| **base** | one ridge coefficient per player, per side of the ball | +0.001322 | **4.11** | — | — |
| **+ box-score prior** | 32 box-score dims through one shared map to value, so a thin-minutes player falls back to what his stat line implies rather than to zero | +0.000175 | **1.50** | +4.87 | 14/16 |
| **+ height and position in that prior** | height, height², position (the 1–5 number) and its square, on top of the 32. Known before a player takes a possession, so as available for a hypothetical five as for a real one | **+0.000037** | **0.69** | **+6.33** | **15/16** |
| **+ experience curve** | 9 shared bins of career stage | +0.000238 | **1.75** | +4.61 | 16/16 |
| **+ this-season δ, carried forward** | per-(player, season) deviation from career, shrunk by ρ = 0.6 | +0.000115 | **1.21** | +9.31 | 16/16 |
| **= full additive stack** | all four, together | **+0.001799** | **4.80** | +11.28 | 16/16 |

*The stack total is the measured `all_cf` of one run — `fwd_exp_shared.csv`,
the true-debut career-stage curve with the shipped numeric-position prior, 16
matched origins — not the sum of the rows above it, which overlap.*

Three things a newcomer should know about these rows:

- **The prior is the most robust lever in the project.** It also names the
  biggest data gap: the box score explains **78%** of a player's true offensive
  rating and only **52%** of his defensive one. That gap is the strongest
  argument for tracking data anywhere in this work — and height and position
  are the cheapest piece of it available without any. The one-hot variant of
  position reads slightly larger (+0.000043, t=+3.88, 13/16) and the paired
  difference between the two is null; the numeric form is what ships, being
  4 columns instead of 21 and 15/16 rather than 13/16.
- **The prior's own penalty has never been selected.** Every rig sweeps
  `a_gamma` over {1e6, BIG} — on or off — so 1e6 is a pinned value inherited
  from a 32-dim prior. `forward_eval --a-gamma` now makes it a real grid.
- **+0.000077 of the experience curve was a data fix, not modelling.** 27% of
  possessions carried the wrong debut year (2002 read as 100% rookies).
  Correcting it won 16/16 seasons. Age LOSES to experience, and a spline LOSES
  to 9 bins. Substantively: a rookie creates shots at league average (+0.03)
  and cannot finish them (−0.79); defence ages the other way and never
  collapses.
- **δ is worth exactly 0.000000 as fitted** and +0.000115 *carried forward*. It
  is not a better description of last season — it is a recency signal about
  next season. Mid-season, where this season's δ is partly observed, it is the
  single biggest lever in the project (+0.000140, t=+7.63).

---

## 4. The composition terms — the small half

Measured against a **fresh** baseline (`fractional_pairs.py`: fit through slice
j−1 of the test season, score slice j, 45 origins). That baseline is a better
model than the season-ahead one — +0.002026 against +0.001701 — so there is
*less* room on top of it. That is what makes it the honest test rather than an
easier one.

| term | why it is defined for a lineup that never played | Δr² | pts/100 | t | seasons |
|---|---|---|---|---|---|
| **usage demand** | a possession has one ball and five usage shares must fit inside 100%. Hinges in Σ career usage rate. Pure arithmetic, so it is defined for *any* five | +0.000007 | **0.30** | +4.03 | 33/45 |
| **free pair chemistry** | one free coefficient per teammate pair with ≥50 shared possessions. Generalises to unseen *lineups* because the PAIRS are observed even when the five is not | +0.000025 | **0.57** | +2.48 | 32/45 |
| **= northstar-aligned model** | | **+0.002056** | **5.13** | | |

*Both were measured before height and position entered the prior. With the
shipped prior the fresh-baseline stack reads **+0.002145** carrying last
season's δ and **+0.002160** carrying this season's — the best deployable
numbers in the project (`frac_k2_bionum.csv`, `frac_k2_thl.csv`).*

**Both survived the check that killed two other candidates.** `slice_horizon.py`
scores the test season in quarters with the fit held constant: a composition
effect is flat in the slice index, a block that is really re-levelling a
drifted baseline rises through the season. Free pairs sit 5.0 sem and usage
demand 8.3 sem below the slope a pure drift-absorber would need.

**The practical caveat on chemistry.** Only a small fraction of possible player
pairs have ever shared a floor. At the ≥50-possession bar the tool now uses, a
randomly-typed five has **0.54 of its 10 pairs known** and **58.4% have none at
all** (at the old ≥200 bar it was 0.43 and 65.5%). So the 0.57 pts/100 is measured on real
lineups; for the arbitrary five a user types first, the term is mostly zero.
An unseen *lineup* is not an unseen *pair*, and that distinction is the whole
reason two earlier readings of this project contradicted each other.

---

## 5. The fork that decides what the tool prints

The single most important thing to understand about the current state.

| baseline | usage demand | free pairs, measured ON TOP of demand |
|---|---|---|
| static career ratings | +0.000007, t=+4.03 | **+0.000025, t=+2.48** |
| + this season's δ | +0.000006, t=+2.48 | **−0.000004, t=−0.49** |

Give the model current-season form and measured chemistry adds **nothing** —
because "these two play well together this year" and "both of them are playing
well this year" are largely the same information seen from two sides. Usage
demand survives both, because it constrains arithmetic rather than describing
form.

The tool prices **hypothetical, cross-era** lineups (five Shaqs; Curry beside
Jordan). There is no common "this season" for those, so it runs on career
ratings — the static row — and chemistry does belong on the page.

*Caveat: with δ on, the interaction block sits on a partly in-sample residual,
so all three δ-row numbers are lower bounds. The ORDERING is the finding, not
the levels.*

---

## 6. What is deliberately absent, and the measured reason

Anyone new asks why there is no neural network. There was, repeatedly.

| tried | forward result |
|---|---|
| profile bilinear, `Σ_{i<j} z_i' M z_j`, 351 cells | −0.000001, a powered null |
| …sparsified to the 10 best-signal cells | +0.000001, t=+0.23 |
| quadratic prior — is value a *curved* function of the box score? | −0.0000022 ± 0.0000047 |
| flexible random-feature pair function, output layer solved jointly with the player block | −0.000007 ± 0.000007 |
| set attention / cross attention / two-stream / cross-init (4 architectures) | all null |
| lineup composition: order statistics, dispersion, threshold counts, height, position | nothing reaches t = 2 |
| diminishing returns to stacking scorers | null; curvature flips sign between splits |
| offense × defence matchups | at the noise floor, reliability +0.02 |
| usage conservation in its MULTIPLICATIVE form, `I·(D̄/D−1)` | −0.0000001 ± 0.0000034 over the demand hinges — a powered null |
| carrying more than one season's δ forward (lags 1–4) | −0.000002, t=−0.42, 10 of 16 origins identical |
| index curvature, offense (`I²`) | +0.000000, t=+0.59. All of the forward curvature is DEFENSIVE, and its sign is wrong for the tool |

The sparse-bilinear row is a cautionary tale: it read **+0.0000153, t=+2.70**
until a test-set leak was found in its *basis selection* step — a
per-possession mask indexed by cell ids, which silently selected the whole
corpus. Clean, it is +0.0000008. 95% of what was then the live lead. The fit
and the scoring were both clean, which is why "is this forward?" passed.

All the architectural nulls are explained by one measurement: **pair effects
are not low-rank.** Reproducing them needs rank ~256; rank 8 gives exactly zero
on novel lineups. Chemistry lives in specific pairs of *people*, and predicting
a pair effect from profiles is capped at 2–3% of its variance whatever the
functional form. A richer function of the same inputs cannot beat a ceiling
that is about the inputs.

**Also measured and not shipped:** floor geometry (shot-map diversity) predicts
well — +0.000008, t=+3.50 on the fresh baseline, independent of usage demand —
but 3 of its 5 pre-registered signs came back **inverted**, the predictive
content sits entirely in the inverted columns, and extrapolated it hands five
copies of anyone a *bonus*. It helps accuracy and breaks the tool. There is no
sign-constrained subset of it that predicts anything.

---

## 7. The error bars are part of the model, not a caveat

The tracked page uses the horizon-0 calibration selected for a current/default
player state: **0.61 on offense and 0.70 on defence**. Every additive rating it
prints is shrunk by those.

Earlier experiments found that posterior standard deviations over the
incumbent player-rating model varied only 1.3× across real lineups and did not
order calibration quality. That does **not** settle uncertainty for structurally
novel lineups. The next model must calibrate error against distance from role,
composition, and matchup support and widen its interval out of distribution.

The observed known-pair chemistry residual carries its separately measured
slope of 1.0. It is present in the incumbent page, but the primary contextual
model must run without it; see `CONTEXTUAL_MODEL.md` §4.

---

## 8. How much is left on the table

| | Δr² | pts/100 |
|---|---|---|
| linear (additive) ceiling, **random split** | +0.002759 | 5.94 |
| **this model** | **+0.002056** | **5.13** |
| forecastable non-additive ceiling | +0.00017 | 1.48 |
| of which this model reaches (demand + pairs) | +0.000032 | 0.64 |

**Read that table with §26 in hand.** The ceiling row is a RANDOM-SPLIT
number, and the headroom it implies is roughly double the deployable one:
measured forward on the same rig the gap between the best noise-free score and
the best full-data fit is **+0.000262**, not +0.000499 — and forward there is
no α→0 limit to call a ceiling at all, because removing shrinkage removes
shrinkage bias *and* increases drift exposure. Better estimation of β is worth
about half what this table says. Freshness keeps its standing.

So roughly **74% of the reachable additive signal** and **19% of the
forecastable non-additive budget**. The remaining headroom is mostly in the
additive half, and mostly needs *new inputs* rather than a better function —
the 48% of defensive rating the box score cannot explain is the clearest
target.

**One lever is measured and not yet folded in.** Recency-weighting the
box-score profile improves the prior in both regimes — +0.000068 (t=+3.47,
14/16) season-ahead and +0.000053 (t=+2.63, 13/16) at fractional origins, at a
**0.4-season half-life**, an interior optimum. It does not reach the full stack
in either regime, because carry-forward and this-season δ were already doing
the recency job. Note the trap: `profile_matrix` bundled recency with
within-season z-scoring, and era adjustment on its own costs the prior
−0.000081. A knob that bundles two changes measures neither.

---

## 9. The 5-Shaq rule: what it actually was, and what now stands in for it

**The requirement had been argued about in the wrong units.** Every number on
the record came from `five_shaq_audit.py`, which prices with the RAW additive
model. The current tool prints
`(offense × 0.61 + chemistry × 1.0 + usage demand) × gate` and
`defense × 0.70 × gate`. `tool_model.py` is the database-free reference
implementation; `tool_audit.py` uses it to price real five-man units with the
same arithmetic.

| real units, ≥50 poss, as the page prints them | p1 | p50 | p99 | max |
|---|---|---|---|---|
| net | −5.48 | +4.55 | +14.76 | **+21.64** |

Face validity: the Warriors' death lineup prints **+18.47**, and the 2014 Spurs
+16.57.

**The page is not broken by excellence. It is broken by repetition.**

| lineup nobody fielded | raw | after the gate |
|---|---|---|
| five Nikola Jokićs | +33.61 | **+14.34** |
| five LeBron Jameses | +32.19 | +13.59 |
| five Rudy Goberts | +26.22 | +11.66 |
| five Shaquille O'Neals | +11.51 | +4.56 |
| **the five best DISTINCT offensive players** | **+22.18** | +20.75 |
| the five best DISTINCT defensive players | +23.55 | +18.64 |

The best five distinct offensive players at +20.75 against a real maximum of
+21.64 is not an absurd answer, and the gate leaves that lineup alone. The raw additive
duplication curve — k copies plus (5−k) league-average fillers — is exactly
linear in k; usage demand and the coverage gate bend the final page output.

### Why the gate is asserted, and why that is now the correct answer

Four structures have been fitted to try to measure one: floor geometry,
index curvature, defensive coverage, and usage conservation in its
multiplicative form. The two with clean, controlled, placebo-passed forward
signal both extrapolate the **wrong way** — five copies of anyone get a
*bonus*. The mechanism is `selection on the outcome`: a coach fields an unusual
five only when it works, so within the observed range "unusual" is correlated
with "good" and every fit inherits that sign.

That is stronger than the earlier conclusion. `distance_shrink.py` showed the
schedule cannot be fitted **on this corpus**; selection says it cannot be
fitted **in principle** from lineups that someone chose to play, and that the
bias has a known direction. So asserting the device is correct rather than a
compromise.

### The device

```
d      mean pairwise distance in play style, height and position
       (empty-empty pairs skipped, so a partial five is not punished)
gate   FMIN + (1 - FMIN) * min(1, d / d_floor)
       d_floor = the 1st percentile of real units
       FMIN    = the 99th-percentile real unit / the worst five-copy five
```

Exactly 1.00 for any five at least as varied as the least varied unit ever
fielded. **Cost in range, measured rather than argued: of 18,071 real units,
1.00% move at all and the mean absolute change is 0.0012 pts/100.** The target
is the 99th percentile and not the maximum, because landing five Jokićs exactly
on the best unit ever measured still answers "tied for the best lineup of all
time", which is the sentence the requirement exists to prevent.

**What it does not do.** It does not cap five distinct specialists: the five
best defenders ever still print +19.79 against a real maximum of +17.24. They
are differentiated, so the gate leaves them alone, and whether an all-time
defensive five really would be 15% past the best real unit is a question the
data cannot answer either way. Inventing a second constant to force it down
would be worse than saying so.

## 10. What the published baseline contains

`tool/five.html` matches the exported arithmetic tested in `tool_model.py`.
The changes that were previously recorded as gaps are now all present:

1. **Pairs export at ≥50 shared possessions**, the bar the forward-validated
   model uses — 36,688 pairs instead of 28,446, with the top and bottom of the
   list unchanged.
2. **Chemistry carries its own slope of 1.0** rather than being folded into an
   additive slope. The death lineup's chemistry
   goes from an effective +0.50 to +1.12 across 10/10 pairs.
3. **The prior carries height and position** (§3). Ratings correlate 0.996 with
   the previous export; the movers are the tallest and shortest players with
   the thinnest records.
4. **Usage demand is included**, using career usage profiles and the fitted
   hinge coefficients in the export.
5. **The additive slopes are horizon-0 values**, 0.61 offense and 0.70 defence.

This is still an incumbent benchmark. Known-pair chemistry is not the desired
primary representation of complementarity, and the asserted coverage gate is
not the desired source of either the OOD mean or its uncertainty.

`tool/README.md` has the rebuild-and-republish procedure, and the artifact must
go to the EXISTING url or the user's link breaks.

---

## 11. Provenance

Every number above is traceable to a module and a cached result.

| claim | module | cache |
|---|---|---|
| additive lever decomposition | `forward_eval.py` | `fwd_prof_flat.csv` |
| composition terms, fresh baseline | `fractional_pairs.py` | `fractional_demand_pair.csv`, `fractional_pairs_off_*.csv` |
| composition vs staleness | `slice_horizon.py` | `slice_horizon_*.csv` |
| the 5-Shaq magnitude | `five_shaq_audit.py` | prints only; `logs/five_shaq_audit.log` |
| distance-aware shrinkage | `distance_shrink.py` | `distance_shrink_forward.csv` |
| the nonlinear-prior null | `nonlinear_prior.py` | `nonlinear_prior.csv` |
| the flexible pair-function null | `forward_pairs.py --rff 128` | `forward_rff_off.csv` |
| profile recency | `forward_eval.py --profile-halflife --profile-no-era` | `fwd_prof_decay*.csv`, `frac_k2_*.csv` |
| linear / non-additive ceilings | `additive_ceiling.py`, `lineup_variance.py` | `additive_ceiling.csv`, `lineup_variance_full.csv` |
| calibration slope | `lineup_scoreboard.py`, `lineup_uncertainty.py` | `scoreboard_prior.csv`, `scoreboard_horizon.csv` |
| geometry coefficients and signs | `geom_readout.py`, `coverage_readout.py` | `geom_readout.csv` |
| height/position in the prior | `forward_eval.py --prior-bio[-num]` | `fwd_prior_bio.csv`, `fwd_prior_bionum.csv`, `frac_k2_bio.csv` |
| what the TOOL prints, vs real units | `tool_audit.py` | `tool_audit_real_net.csv` |
| the duplication gate and its in-range cost | `tool_safety.py`, `export_ratings.py` | `tool_safety.csv` |
| the multiplicative conservation null | `forward_pairs.py --scale` | `forward_pairs_off_points_scale_wide.csv` |
| index curvature, per side | `index_curvature.py` | `index_curvature_forward_0.csv` |
| multi-lag carry-forward | `forward_eval.py --multilag` | `fwd_multilag.csv` |
