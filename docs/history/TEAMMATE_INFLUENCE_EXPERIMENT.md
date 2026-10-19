# On-floor influence: what a player does to the other four

**Status: design + reconnaissance complete, estimator not yet built.**
Opened 2026-09-07 at Adam's request. Read `CLAUDE.md`, then
`MODEL_RESEARCH_ROADMAP.md` R03/R04, which name this direction; this document
turns those into a specific estimand, a specific design, and the pre-registered
tests it has to pass. Nothing here promotes a scorer, edits a completed run,
touches the database, or changes `MODEL_FEEDBACK_FROM_CLAUDE.md`.

## 1. The question, stated precisely

Adam's framing: *"how much players affect the team as a whole when on and off
the floor — Jokić increasing his teammates' shooting percentage, Shai decreasing
his team's turnovers."*

That is three separate estimands, and they must not be pooled:

1. **Conversion response.** Teammate q converts a shot from a given location
   better with p on the floor than without him, beyond q's own shooting ability.
2. **Opportunity response.** Teammate q's *mix* changes with p on the floor —
   more threes, more rim attempts, more free throws, fewer long twos — beyond
   what the usage budget already forces.
3. **Ball-security response.** The other four turn it over less with p on the
   floor, beyond their own turnover rates.

All three are effects **on the other four players**, not on p's own line. This
is the distinction that makes the question answerable: p's own production is
already in the model, and mixing it back in just re-estimates what we have.

## 2. What the current models do with this today

**The structural model has none of it, by construction.** `asof_state.py`
builds each player's 16-dimensional profile from his OWN counts
(`own_fg2m`, `own_tov`, `own_shot_ast`, …) with `ton_poss` used only as a
denominator. `asof_point_allocation.predict` then assembles five fixed profiles
under a shared usage budget and a category-share calibration. The only place
one player's presence changes another player's number is (a) the proportional
usage rescaling and (b) the assisted-demand-minus-passing-supply deficit. Shot
location shares within twos and within threes are held fixed per player, and
`self_2p` / `self_3p` are never modified by who else is on the floor. So it
cannot express "Jokić's teammates finish better," even in principle.

**The additive model has all of it, undifferentiated.** `asof_additive.py`
fits `theta` on the possession points target with the ten on-floor identities in
the design. That IS a regularized adjusted plus/minus: on/off, teammate-adjusted
and opponent-adjusted, collapsed into one number per player per side. It knows
Jokić helps; it cannot say through which channel, and it cannot say it in
points-per-100 of rim attempts or turnovers.

That is the gap in one sentence: **the arm that measures the effect can't explain
it, and the arm that explains can't measure it.**

## 3. Reconnaissance — the raw numbers for Adam's two examples

Descriptive only, from the cached `game_player_stats.pkl` (game×player), seasons
2017+, players with ≥6,000 on-floor and ≥3,000 off-floor offensive possessions
(575 players). "Teammate" quantities remove the player's own shots, own
turnovers and own free throws from the on-floor totals, so these are effects on
the other four. Off-floor is his team without him, same games.

| player | teammate eFG on | off | lift (eFG pts) | teammate TOV/100 lift | teammate 3PA-share lift | team pts/100 lift |
|---|---:|---:|---:|---:|---:|---:|
| Nikola Jokić | .559 | .515 | **+4.37** | **−5.52** | +3.30 | +10.29 |
| Shai Gilgeous-Alexander | .549 | .523 | +2.52 | **−5.55** | +5.38 | +7.04 |
| Stephen Curry | .575 | .520 | **+5.55** | −3.83 | −2.80 | +9.28 |
| Kevin Durant | .577 | .525 | +5.16 | −4.45 | +0.49 | +8.72 |
| Trae Young | .562 | .515 | +4.65 | −6.68 | −0.08 | +7.19 |
| Joel Embiid | .558 | .520 | +3.86 | −6.36 | +7.38 | +5.88 |
| Rudy Gobert | .534 | .543 | −0.96 | −1.82 | +6.39 | +0.60 |
| Domantas Sabonis | .532 | .529 | +0.32 | −4.23 | +7.15 | +1.09 |

League spread of teammate eFG lift: mean −0.24, sd 1.64, range −6.66 to +5.55.

**Adam's read of the tape is confirmed descriptively, and the size is large**
— Jokić's +4.37 eFG points on his teammates is roughly 4 points/100 of offense
on its own, several times the entire non-additive budget the project has ever
measured on the points target.

**And the raw number is not usable as it stands.** Mean teammate-TOV lift across
all 575 players is **−2.57/100**: essentially everybody's teammates turn it over
less when he plays, because "off" is a bench-heavy, garbage-time-heavy
population. The bottom of the eFG-lift table is Zeke Nnaji at −6.66, which is
not a statement about Nnaji — it is a statement about Denver without Jokić. Raw
on/off is a statement about *who else was out there*, which is exactly why the
estimator in §5 has to put all ten identities in one design.

Prior evidence pointing the same way: `prior_ridge.DROP` era — the box-score
prior is worth +0.000175 forward **only after dropping the on/off columns**
(`tmlift_*`, `dlift_*`), which are the naive version of this feature used as a
prior for a player's own value. That is a different use than the one proposed
here, and its failure is not evidence against §5.

## 4. Screen — is there anything the models are missing?

Pre-registered before running: summed teammate-eFG lift should carry a POSITIVE
slope on a model's residual, summed teammate-TOV lift a NEGATIVE slope,
teammate FT% lift is the PLACEBO and must be flat. Population: the 44 primary
quarter origins of the completed centered run
(`experiments/cache/asof_points_centered_2026`), cells whose five players all
clear 1,500 prior on-floor and 750 prior off-floor possessions — **5,369 cells /
702,917 possessions**. Lifts use games strictly before each origin's window
start, EB-shrunk with `eb_diff`, exposure-centered. Features are summed over the
five slots; features and targets are centered within origin; slopes are
possession-weighted with a 400-draw block bootstrap over origins; bootstrap standard errors move in the last printed
digit with the seed.

| feature | vs actual (rel. league) | vs additive − structural prediction | vs structural residual | vs additive residual |
|---|---:|---:|---:|---:|
| teammate eFG lift | **+49.2 (t +10.6)** | **+15.7 (t +7.9)** | +7.5 (t +1.6) | −8.2 (t −1.6) |
| teammate TOV lift | **−50.8 (t −7.3)** | **−22.4 (t −7.4)** | +3.4 (t +0.5) | +25.8 (t +3.9) |
| teammate 3PA-share lift | +4.5 (t +1.6) | +0.9 (t +1.1) | +0.4 (t +0.1) | −0.5 (t −0.2) |
| team pts/100 lift | **+32.2 (t +13.7)** | **+9.7 (t +8.2)** | +6.4 (t +2.8) | −3.3 (t −1.3) |
| **teammate FT% lift (placebo)** | +18.5 (t +2.4) | −2.9 (t −1.4) | +8.0 (t +1.2) | +10.9 (t +1.7) |

Three things follow.

**(a) The feature carries real content.** Both pre-registered signs come out
right against the actual cell rating, at t = +10.6 and −7.3.

**(b) Against the actual rating, that content is partly roster selection** —
the placebo also fires (t = +2.4). Good players play with good players. Nothing
built on the raw feature against the outcome can be trusted, which is the same
warning `context_profile.py` earned with the same placebo.

**(c) The load-bearing row is `additive − structural`, and it is placebo-clean.**
The two arms' predictions differ, cell by cell, in exactly the direction of the
on/off lifts (eFG t = +7.9, TOV t = −7.4, points t = +8.2) while the placebo is
flat (t = −1.4). No outcome enters that column, so selection cannot produce it.
**What the additive arm has and the structural arm lacks is, quantitatively,
the on-floor influence content.** That is the strongest single piece of evidence
for building this, and it is consistent with the corrected additive arm's
standing win on ranking and squared error (`ASOF_ADDITIVE_REFERENCE_RESULTS.md`:
pooled r² .1204 vs .1072, correlation .2382 vs .2040 within quarter).

**What the screen does NOT establish.** The structural residual rows are
suggestive at best (points-lift t = +2.8 against a placebo already at +1.2), so
a crude summed lift bolted onto the structural arm is not a ready lever. The
44 origins share players and overlapping training prefixes, so the block
bootstrap understates uncertainty (rule 3). This is a screen, not a result.

## 5. The estimator to build

One design, three channels, fitted the way the rest of the project fits things.

For possession-level or cell-level channel outcome `y` of an offensive five
`L_off` against a defensive five `L_def`, at origin cutoff `T`:

```
y  =  f_structural(L_off ; profiles<T)          # OFFSET, not refitted
      + sum_{p in L_off} a_p                    # offensive on-floor influence
      + sum_{q in L_def} d_q                    # defensive on-floor influence
      + e
```

with `a` and `d` separately ridge-penalized, penalties selected on a held-out
strictly-prior window and evaluated on a third disjoint one. Fit one such model
per channel:

| channel | target | the mechanism it prices |
|---|---|---|
| conversion | teammates' made points above their own location-conditional expectation | "Jokić's teammates finish better" |
| ball security | teammates' turnovers per possession | "Shai's team turns it over less" |
| mix | teammates' 3PA share and rim share within FGA | "he gets them better shots" |

The structural assembly is the **offset**, so `a_p` is by construction *what the
profile assembly misses* — the interaction, not the level. Putting all ten
identities in one design is what makes `a_p` an adjusted quantity rather than
the confounded on/off of §3: `a_Nnaji` is then estimated from Denver possessions
with and without Jokić, holding Jokić's own coefficient fixed.

Reasons to expect this to work better than the project's previous interaction
attempts, all of which are documented nulls:

- **The target is a channel, not points.** `possession_outcomes.py`'s founding
  argument: three quarters of possession-points variance is make/miss noise.
  Turnovers and shot mix are near-deterministic per possession; the estimation
  problem is a different one.
- **It is a level shift per player, not a pair effect.** `pair_effects_not_lowrank`
  and `pair_effects_unpredictable` killed pair-indexed structure. This is
  n_players parameters, the same count the additive model already estimates
  well, and it inherits the additive model's identification.
- **The additive arm already demonstrates the content exists forward** (§4c).

### Identification and the traps to design against

1. **Attribution / double counting.** Teammate q's own profile was measured
   while playing with p, so part of p's influence is already inside q's profile,
   `a_p` is attenuated, and transporting q to a lineup without p over-credits
   him. The fix is the same loop `context_deconfound.py` already implements and
   verified to 1e-14: estimate `a`, deconfound the profiles against
   co-occurrence, re-estimate. Its forward payoff was null on the additive
   points target; it has never been run on channels inside the structural model.
   Report the attenuated and deconfounded versions side by side; do not quietly
   ship one.
2. **Deployment, not chemistry.** Q1/Q3 overrepresentation and garbage time are
   already documented in `ASOF_DEPLOYMENT_AUDIT.md`. Coarse clock/score controls
   go in the design, and the raw-versus-controlled `a` must be reported.
3. **The placebo is not optional.** Teammates' FT% must read flat. Every claim
   in §4 that survived did so because the placebo did not.
4. **Extrapolation is the product risk.** `sum_{p} a_p` additive across five
   means five Jokićs each get four Jokić-sized conversion bonuses — the exact
   shape of the 5-Shaq failure (`selection_on_the_outcome`: lineups are chosen
   on the outcome, so every fitted composition effect extrapolates the wrong
   way). The influence term must be capped by a conserved quantity — you cannot
   raise the other four's conversion above what the shots allow — or it will
   break the counterfactual standard while improving forward MAE. Decide the
   functional form BEFORE reading the forward result.
5. **Grid boundaries.** Print the selected penalty against both grid ends every
   run (rule 12), and widen twice (rule 10).

### What was actually built (2026-09-08)

`experiments/onfloor_influence.py` and its runner implement the above with one
simplification and one addition worth stating plainly.

**The simplification.** The estimand is not separately identified as "effect on
the other four". A possession's parsed outcome names the events but not, in the
channel table, which of the five produced them, so the residual is a TEAM
channel residual and a player's coefficient absorbs both his effect on his
teammates and his own profile's error. The document calls this *on-floor
influence* rather than *teammate influence* for that reason, and §5's
identification note stands: the decomposition is not established, only the
prediction.

**The addition.** Every quarter of the corpus from 2003 on gets its own
strictly prior assembly — `PlayerHistory.snapshot` at 180/730 days,
`EnvironmentHistory.snapshot` at 365 days, and the protocol's own frozen usage
budget — and the residual is taken against THAT, so a coefficient is what the
assembly missed at the time, not what it misses today. 96 quarters,
5,200,547 covered possessions of 5,831,664 (89.2%; Q1 coverage is 68% because a
five containing a player with under 100 prior possessions is dropped rather
than priced from a shrunk-to-league profile).

Fitting is one forward pass: the normal equations accumulate quarter by quarter,
so an origin's fit reads every possession before it and none after it by
construction rather than by a mask. Each channel's ridge penalty is chosen on
the last completed quarter as a held-out set. Scoring injects the coefficients
through `asof_point_allocation.predict` itself — the component influences shift
`team_components` and are renormalised to the same usage budget, the conversion
influences shift the making probabilities — so the arm is the structural model
with a different allocation, not a structural score plus a bolt-on.

### Population and evaluation

Reuse the completed run's cells exactly — `p0..p4`, `possessions`, `actual`,
`league`, `novel`, per origin, in
`experiments/cache/asof_points_centered_2026/origins/*/cells.csv.gz`. A new arm
scored on that identical population is directly comparable to the corrected
additive 8.0920 and structural 8.1461 without refitting either and without
touching the frozen protocol fingerprint, which would invalidate the resume.
Report MAE, RMSE, bias, within-quarter correlation, pooled raw r², the `novel`
slice separately, and season-paired differences with SEM.

### Pre-registered acceptance

The experiment is worth carrying forward if, on that population:

- the influence terms are **placebo-clean** (teammates' FT% influence
  indistinguishable from zero), and
- the structural arm's MAE improves and its within-quarter correlation moves
  toward the corrected additive's 0.2382, and
- the per-channel decomposition is **basketball-legible** — Jokić's conversion
  term and Shai's turnover term should be near the top of their channels, which
  is a face-validity check, not evidence, and
- five copies of a high-influence player do not print a rating outside the real
  range (standard 2).

Failing the third and fourth while passing the first two is still a result, and
it must be reported as one rather than tuned away.

## 6. Results — completed 2026-09-08

Population: the centered run's own **5,607 primary cells / 726,364 possessions /
44 quarter origins**, 2016–2026, with 2015 as chronological calibration warmup.
Nothing was refitted and no completed run directory was touched.

### The arm is comparable, verified before any claim

The rebuilt parent reproduces the published
`structural|180|live|recent_live|raw|base` allocation to **≤1e-13 pts/100** at
every origin, and after this module's own prior-only calibration reproduces the
published `...|deficit` arm's forward metrics **to the digit** (MAE 8.143983
both). Profiles, valuation, conversion reference and the frozen usage budget are
therefore the protocol's own, not a lookalike.

**Penalty boundaries** (rule 12, printed against both ends): across 44 primary
origins × 8 identity channels, **0 of 352 selections sit on the low edge**; 15
sit on the high edge and all 15 are the free-throw placebo, which is the
selector correctly shrinking a null channel to nothing.

**The antisymmetric level direction that broke the additive arm is absent**:
`(mean θ_off − mean θ_def)/2` is `0.000000` on every one of the eight channels,
because the residual is detrended and the ridge splits the level symmetrically.

### Forward accuracy

| arm | MAE | RMSE | bias | raw r² | corr | novel MAE | season-paired ΔMAE vs parent |
|---|---:|---:|---:|---:|---:|---:|---|
| parent (rebuilt = published) | 8.1440 | 10.9214 | −0.680 | 0.1073 | 0.2898 | 8.8903 | — |
| components | 8.1355 | 10.8996 | −0.631 | 0.1109 | 0.2942 | 8.8821 | −0.0031 ± 0.0217 (5/11) |
| conversion | 8.1482 | 10.9107 | −0.522 | 0.1091 | 0.2955 | 8.9106 | +0.0064 ± 0.0273 (6/11) |
| all | 8.1418 | 10.8990 | −0.494 | 0.1110 | **0.2975** | 8.9007 | +0.0046 ± 0.0376 (5/11) |
| all, recency-weighted | 8.1578 | 10.9088 | −0.535 | 0.1094 | 0.2965 | 8.9222 | +0.0207 ± 0.0356 (5/11) |
| **all, separately priced** | **8.1333** | **10.8949** | −0.528 | **0.1117** | 0.2973 | 8.8948 | −0.0047 ± 0.0335 (5/11) |
| smooth control alone | 8.1794 | 10.9406 | −0.605 | 0.1042 | 0.2857 | 8.9235 | +0.0363 ± 0.0152 (3/11) |
| control, separately priced | 8.1591 | 10.9197 | −0.618 | 0.1076 | 0.2903 | 8.9149 | +0.0163 ± 0.0084 (3/11) |
| identities + control (joint) | 8.1699 | 10.9217 | −0.572 | 0.1073 | 0.2919 | 8.9077 | +0.0303 ± 0.0274 (4/11) |
| joint, separately priced | 8.1516 | 10.9073 | −0.595 | 0.1096 | 0.2942 | 8.9100 | +0.0119 ± 0.0231 (4/11) |
| placebo | 8.1476 | 10.9237 | −0.682 | 0.1070 | 0.2895 | 8.8952 | +0.0034 ± 0.0018 (5/11) |
| placebo, penalty-matched | 8.1477 | 10.9236 | −0.682 | 0.1070 | 0.2896 | 8.8949 | +0.0036 ± 0.0017 (3/11) |
| placebo, separately priced | identical to the parent to 4e-16 | | | | | | |
| corrected additive (published) | 8.0920 | 10.8410 | −0.548 | 0.1204 | 0.3096 | 8.9039 | −0.0466 ± 0.0478 (6/11) |
| best saved structural | 8.1330 | 10.9046 | −0.458 | 0.1101 | 0.2896 | 8.8957 | −0.0098 ± 0.0127 (6/11) |

**The MAE gain is not established.** Every season-paired difference is a small
fraction of its own SEM and 5/11 seasons is a coin flip. Quarters and recurring
fives are not independent replicates, so that SEM is itself a lower bound
(rule 3).

**Ranking and squared error move consistently.** Correlation goes
**0.2898 → 0.2975** and RMSE **10.9214 → 10.8949**, and the influence arm now
carries the best structural RMSE, pooled r² and correlation on this population.
It does not close the gap to the corrected additive on MAE or r².

The influence is worth about **0.9 pts/100 of extra spread** in the score before
calibration, and the calibration keeps roughly 39% of it.

### The placebo result is the load-bearing one

Given a free nonnegative price on completed prior windows only, the calibration
pays for the influence and refuses to pay for the placebo:

| priced arm | c, mean | min | max | origins with c = 0 |
|---|---:|---:|---:|---:|
| influence (career) | **+0.3869** | +0.2973 | +0.5850 | **0 of 44** |
| influence (recency-weighted) | +0.4455 | +0.3057 | +0.6859 | 0 of 44 |
| identities + smooth control | +0.3388 | +0.2154 | +0.5521 | 0 of 44 |
| smooth control alone | +0.3067 | +0.1534 | +0.4962 | 0 of 44 |
| **free-throw placebo** | **+0.0000** | 0 | 0 | **44 of 44** |

Forty-four independent prior-only fits price a real channel at about 0.39 and
the placebo at exactly zero, every time. Nothing a teammate does changes a free
throw, and the calibration discovers that on its own. `c ≈ 0.39` also matches
the reliability below: the influence is real and belongs shrunk to about 40% of
its raw size, which is what the data does unprompted.

### Reliability, measured on nearly disjoint data

The recency accumulator has a 6-quarter half-life, so the fits at 2019q1 and
2026q4 share about 2.8% of their weight. For the 694 identities with ≥12,000
prior offensive possessions:

| channel | near-disjoint corr | same-span career fits (SHARED data) |
|---|---:|---:|
| make_two | **+0.375** | +0.784 |
| turnover | **+0.368** | +0.817 |
| three_attempt | +0.322 | +0.742 |
| ft_usage | +0.313 | +0.861 |
| two_attempt | +0.277 | +0.815 |
| orb | +0.210 | +0.830 |
| make_three | +0.197 | +0.806 |
| **make_ft (placebo)** | **+0.086** | +0.793 |

The right-hand column is printed to make a point: two career fits eight seasons
apart share nearly all their training data, so their 0.8 agreement says nothing
about reliability — the placebo scores 0.793 there too. On nearly disjoint data
the real channels reproduce at 0.20–0.38 and the placebo at 0.086. Teammate
turnover suppression and two-point conversion are the most reliable; three-point
conversion is close to noise, which agrees with the project's standing finding
that shot-making is the low-signal half.

### Face validity

Top of the total-influence ranking at 2026q4, among identities with ≥6,000 prior
offensive possessions: **Trae Young (+7.58 pts/100), Steve Nash (+6.15), John
Wall (+5.78), Luka Dončić (+5.50), Damian Lillard (+5.50), James Harden (+5.44),
Stephen Curry (+5.35), Chris Paul (+5.24)**. Bottom: low-usage centres — Etan
Thomas (−5.05), Andrew Bynum (−4.81), Michael Olowokandi (−4.74), Eddy Curry
(−4.74), Clint Capela (−4.57). Jokić's conversion channel is +4.21 with a
teammate two-point shift of **+3.25 percentage points**, and the largest teammate
turnover suppressions are John Wall, Trae Young, Joel Embiid and Shai
Gilgeous-Alexander. Adam's two named examples both land where he said they would.

A plausible ordering is a check, not evidence.

### A worked swap, which is what the product is for

Dallas at the 2025q3 cutoff (2025-01-17), Kyrie Irving out and James Harden in,
alongside Dončić, P.J. Washington, Gafford and Thompson:

| | 2PA/100 | 3PA/100 | FTA/100 | TO/100 | structural | with influence | priced forecast |
|---|---:|---:|---:|---:|---:|---:|---:|
| with Irving | 53.9 | 36.7 | 22.5 | 12.6 | 121.70 | 127.32 | **120.65** |
| with Harden | 48.9 | 38.1 | 25.8 | 14.7 | 118.90 | 125.75 | **119.46** |

The structural model alone says the swap costs 2.80 pts/100; with the influence
priced it costs **1.19**, because Harden's teammate two-point conversion shift
(+6.24 percentage points) exceeds Irving's (+5.13) and partly offsets a worse
profile fit. The mechanism is legible — fewer two-point attempts, more threes,
more free throws, more turnovers — which is the whole reason to carry a
structural arm rather than one rating per player. It is a forecast against a
league-average defence for a five that never played, not a measured trade effect.

## 7. Is this chemistry, or a repair to the allocation rule?

**64% of the variance in a player's total influence is a linear function of his
OWN eight-dimensional profile** (usage, assist rate, 3PA rate, ORB, turnover
rate, assisted share, 3P%, rim share; R² = 0.638, and 0.563 / 0.446 for the
creation and conversion halves separately). Guards positive, centres negative,
almost monotonically. That is what it would look like if the structural model's
proportional usage allocator mis-prices roles and the identity design were
repairing the ALLOCATION RULE rather than measuring anything about teammates.

Rule 10 requires a control free to absorb everything the arm above it could, so
the run adds one: **the residual regressed on the model's OWN predictions for
that five** — its four allocated components, ORB, its three implied make
probabilities, the spread and maximum of its five native usages, and its assist
supply, demand and deficit. Thirteen columns, available identically at training
and scoring, with no player identity in them. They enter the same augmented
design, and the identity-only, control-only and joint fits all come out of one
Gram because the identity normal equations are exactly its leading block.

**The control does not transfer forward, and it does not displace the
identities.** Alone it is *worse than doing nothing* (8.1794 against the parent's
8.1440, 3/11 seasons better); given its own free nonnegative price it is still
worse (8.1591); and partialling the identities against it makes them worse
(joint 8.1699 and 8.1516 priced, against 8.1418 and 8.1333 for the identities
alone). So the part of the influence that a smooth function of the model's own
predictions can express is precisely the part that does **not** forecast. What
carries forward is idiosyncratic to the player.

Two disclosures on that control, because it decides the interpretation.

**First, its original specification was wrong and its first verdict was
discarded.** The four component columns sum to the usage budget, which moves only
0.5% across the whole corpus (1.1305 → 1.1486 per possession), so with an
intercept the design was collinear to 5e-3 — condition number 2.3e6 — and its
ridge had been pinned at 1e-9. A control fitted along a direction the data barely
identifies is not a control; that is rule 10's failure in a new costume. The
intercept was dropped (the components already span the constant) and the block
was given a selected penalty. The corrected control gives the same verdict.

**Second, its penalty grid still ends on the low edge** — 65 of 220 count-channel
selections sit at 1e-4 after the grid was widened two decades downward. The
control keeps asking for less shrinkage and still fails forward, and widening
the grid changed the answer by 0.0001 pts/100 (8.1793 → 8.1794), which is rule
10's "widen twice and get the same answer". The high end of the grid annihilates
the control and was available at every origin; the count channels never chose it.

**What this does and does not license.** It licenses saying that the forward
content is player-specific rather than a smooth function of role. It does NOT
license calling it chemistry: the residual is a TEAM channel residual, so a
coefficient still absorbs both a player's effect on his teammates and his own
profile's error, and no design here separates them. The honest name remains
on-floor influence.

### Reproduce

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_influence_run --residuals   # 55s
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_influence_run --fit          # 27 min
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_influence_run --score        # 30s
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_influence_readout --origin 2026q4
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_influence_swap \
    --lineup "Luka Dončić,Kyrie Irving,P.J. Washington,Daniel Gafford,Klay Thompson" \
    --out "Kyrie Irving" --in "James Harden" --origin 2025q3
```

Outputs under `experiments/cache/onfloor_influence_*`; logs in
`logs/onfloor_chain*.log`. 14 tests in `tests/test_onfloor_influence.py`.

## 8. Own line or the other four — the split, 2026-09-08

§7 established that the forward content is player-specific, and refused to call
it chemistry because one coefficient still absorbs two things: the model
mispricing the player himself, and the player changing what his teammates do.
This separates them by changing the unit of observation.

A row is one **(game, player)** pair. Its target is what THAT player did minus
what the structural model predicted HE would do — actual counts from
`game_player_stats`, which attributes each parsed event to the man who produced
it, against `asof_point_allocation`'s own per-player allocation accumulated over
exactly the possessions he was on the floor for. A row is kept only when every
one of his offensive possessions that game was priced, so the two sides cover
the same exposure rather than approximately the same: **486,278 rows** over 96
quarters. The aggregation is exact, not an approximation — summing the row
equation over a player's possessions gives `n·own + Σ (shared possessions)·tm`,
so a game-level row with co-occurrence fractions is the sufficient statistic.

### The free split is not identified, and its first answer was discarded

Fitting `own` and `teammate` as two free blocks gives coefficients that cannot
be true. For a pair who always play together, raising `own_p` while lowering
`tm_p` and doing the reverse for his partner leaves every training row's fitted
value unchanged — but not a lineup containing one of them without the other. The
direction is flat in the loss and explodes on extrapolation. Summed over the
completed run's own evaluation fives, that fit implies lineup-level shifts
**4× to 74× larger** than the team-level fit that was actually validated
forward:

| channel | free split, implied sd | validated team fit | ratio |
|---|---:|---:|---:|
| two_attempt | 109.40 | 1.48 | 74× |
| turnover | 50.53 | 1.06 | 48× |
| three_attempt | 54.76 | 2.12 | 26× |
| make_two | 7.39 | 2.01 | 3.7× |

A lineup does not take 109 more two-point attempts per 100 possessions. That
fit is discarded; only its held-out penalty selections are reported, and its
coefficients are not interpreted.

### Anchoring the total, so only the split is estimated

Substituting `own_q = influence_q − 4·tm_q` removes the freedom: one block
remains, the design becomes *teammate fractions minus four times the own
indicator*, and the lineup total is pinned by construction to the team-level
influence the point arm already scores. The penalty grid's top annihilates the
teammate block, so "all of it is his own line" is a choice the selector can make.

Because `own` and `4·tm` are constrained to sum to a fixed total, their
covariance shares with that total sum to exactly 1, and **a share outside [0,1]
is the signature of a split that is still cancelling rather than decomposing.**

| channel | share own | share teammate | sd(own) | sd(4·tm) | reading |
|---|---:|---:|---:|---:|---|
| **make_two** | **+0.09** | **+0.91** | 0.019 | 0.048 | identified: on the other four |
| **make_ft (placebo)** | **+0.88** | **+0.12** | 0.011 | 0.003 | identified: his own line |
| orb | +1.00 | 0.00 | 0.003 | 0.000 | teammate block switched off |
| make_three | +0.50 | +0.50 | 0.010 | 0.010 | borderline |
| ft_usage | +0.07 | +0.93 | 0.082 | 0.082 | borderline |
| three_attempt | +1.28 | −0.28 | 0.165 | 0.165 | NOT identified |
| turnover | −2.05 | +3.05 | 0.087 | 0.089 | NOT identified |
| two_attempt | −7.89 | +8.89 | 0.320 | 0.321 | NOT identified |

**The one clean answer is the one Adam asked for.** On two-point conversion —
"does he make his teammates shoot better, holding their own ability and shot
locations fixed" — the split is identified and **91% of the effect is on the
other four**. The free-throw placebo splits the other way, 88% his own line,
which is what a channel nobody can influence should do.

The volume channels are not identified by this design. Their own and teammate
parts each carry 27× the spread of the total they must sum to, and the readout
shows why it must not be read: it prints turnover coefficients of +43 per 100
for a player's own line, which is impossible. Whether the model's proportional
allocator or a teammate effect owns the volume error remains open.

### Face validity on the identified channel

Teammate two-point conversion at 2026q4, percentage points, with each player's
own-line term beside it:

| player | effect on teammates | his own line |
|---|---:|---:|
| Trae Young | **+4.13** | +2.55 |
| Victor Wembanyama | +3.87 | +1.48 |
| **Nikola Jokić** | **+3.86** | +0.80 |
| Stephen Curry | +3.66 | +0.84 |
| Luka Dončić | +3.52 | +2.41 |
| Steve Nash | +3.37 | +1.48 |
| James Harden | +3.27 | +0.90 |
| Baron Davis | +3.14 | +0.79 |
| LaMelo Ball | +3.04 | −2.71 |
| Franz Wagner | +2.93 | +1.93 |

Jokić is third in the league at raising his teammates' two-point conversion,
+3.86 percentage points, against +0.80 on his own shooting — which is the
hypothesis Adam opened this workstream with, now separated from his own line and
anchored to a total that was validated forward.

It is still not a causal estimate. The design identifies the split off roster
turnover, the same variation `context_profile.py` uses, and lineups are not
randomly assigned.

    python -u -m experiments.onfloor_attribution_run --build --fit --anchored
    python -u -m experiments.onfloor_attribution_readout --origin 2026q4

## 8b. What this says about additive versus structural

`ASOF_POINT_BENCHMARK.md` registers `structural_versus_additive` as a contrast.
This workstream says the framing is wrong: the two are not substitutes, and the
gap between them has a name.

**The gap is on-floor influence.** §4 showed the per-cell difference between the
two arms' predictions tracks prior on/off lifts at t = +7.9 (eFG), −7.4
(turnovers) and +8.2 (points) with the free-throw placebo flat at −1.4. No
outcome enters that comparison. The additive arm is a regularised adjusted
plus/minus, so it carries that content as one undifferentiated number; the
structural arm carried none of it.

**Transplanting it closes about a third of the gap, and no more.**

| | MAE gap to additive | pooled r² gap | correlation gap |
|---|---:|---:|---:|
| structural parent | +0.0520 | −0.0131 | −0.0198 |
| + on-floor influence | +0.0413 | −0.0088 | −0.0123 |
| **closed** | **21%** | **33%** | **38%** |

**On novel fives the ordering is already the other way.** Every structural arm
beats the corrected additive there — parent −0.0136, best published structural
−0.0082, the influence-component arm **−0.0218**. Small, but the sign is
consistent across four arms, and novel fives are the slice the product exists
for.

**Additive's advantage was never on MAE anyway.** Season-paired, structural
minus corrected additive is +0.049 ± 0.045 with 5/11 seasons favouring
structural — not established. The published RMSE, r² and correlation contrasts
are 1/11, 1/11 and 2/11, which are. The additive arm wins on squared error and
ranking, and this work shrinks that win without erasing it.

**And they are complementary, which nobody had tested.** The defensive run
priced the additive defensive half and the influence channels as separate
columns and got 8.3314 against 8.3398 and 8.3984 alone. `onfloor_combined.py`
asks the same question on offence, prior-only, on the completed run's own cells:

| arm | MAE | RMSE | raw r² | corr | novel MAE |
|---|---:|---:|---:|---:|---:|
| structural + influence | 8.1418 | 10.8990 | 0.1110 | 0.2975 | 8.9007 |
| additive | 8.0927 | 10.8429 | 0.1201 | 0.3094 | 8.9041 |
| **both, priced together** | **8.0814** | **10.8341** | **0.1216** | **0.3110** | **8.8849** |

Both together is the best number this project has on every pooled metric and on
novel fives. **The increment over additive alone is not established**
(−0.0088 ± 0.0102, 4/11); over structural alone it is suggestive at
−0.0592 ± 0.0297, 7/11. The `additive` row is refitted with this module's own
calibration history and lands 0.0007 from the published 8.0920.

**What it means for the direction.** Choosing between them is the wrong
question. The additive arm is a compressed summary of exactly what the
structural arm was missing, and it costs nothing in accuracy to carry both —
the structural spine supplies the mechanism the product needs, the additive
column supplies a level the channel decomposition does not fully capture, and
the combination is at worst tied with the best arm available. Two of the three
co-equal standards point the same way: only the structural arm can say which
channel a difference came from, and only the structural arms lead on lineups
that have never played.

## 8c. Complementary or redundant? Overwhelmingly redundant

§8b showed that pricing both arms together beats either alone. A joint fit
cannot say why: two predictors help each other either because each knows
something the other does not, or because averaging two noisy estimates of the
same thing cancels noise. `onfloor_blend.py` separates those.

### What averaging actually buys

| arm | MAE | RMSE | raw r² | corr | novel MAE | vs additive, season-paired |
|---|---:|---:|---:|---:|---:|---|
| structural + influence | 8.1418 | 10.8990 | 0.1110 | 0.2975 | 8.9007 | +0.0504 ± 0.0358 (4/11) |
| additive | 8.0927 | 10.8429 | 0.1201 | 0.3094 | 8.9041 | — |
| **plain 50/50 average** | 8.0763 | 10.8318 | 0.1219 | 0.3096 | **8.8668** | −0.0147 ± 0.0160 (8/11) |
| **blend weight chosen prior-only** | **8.0753** | **10.8303** | **0.1222** | 0.3102 | 8.8716 | −0.0159 ± 0.0120 (8/11) |
| free joint least squares | 8.0814 | 10.8341 | 0.1216 | **0.3110** | 8.8849 | −0.0088 ± 0.0102 (4/11) |

Averaging helps, and gives the best MAE and r² this project has. **The gain over
additive alone is not established** at 1.3 SEM. Note also that the *fixed*
average and the prior-chosen weight both beat the *free* joint least-squares
fit: the extra degree of freedom overfits the prior windows, so a fixed blend is
the more robust construction as well as the simpler one.

The prior-only weight is stable — mean 0.607, median 0.60, range [0.50, 0.70]
across 44 origins — and lands close to the descriptive optimum of 0.679, so
nothing here depends on choosing it well.

### But the reason it helps is noise, not knowledge

**Forward error correlation between the two arms: 0.9856.** With error variances
that close and that correlated, the closed-form minimum-variance blend can only
reach RMSE 10.8267 against the better single arm's 10.8429 — **the entire
theoretical prize from optimal ensembling is 0.15% of RMSE**, and the descriptive
curve confirms it (minimum 10.8268 at weight 0.70).

The decisive test is incremental information: regress each arm's forward error
on the other arm's score. Noise averaging cannot produce a nonzero slope there;
only genuine complementarity can.

| | slope | MSE | as a share of what the arm explains |
|---|---:|---:|---:|
| structural's error on the additive score | −0.0693 | 118.789 → 118.715 | **+0.50%** |
| additive's error on the structural score | +0.0003 | 117.569 → 117.569 | **+0.00%** |

**The structural arm's score explains nothing the additive arm has not already
used** — not 5%, not 1%, zero to four decimal places. The additive score adds
half a percent of what the structural arm explains, which is real but negligible.
Informationally the structural arm is close to a subset of the additive one.

That is exactly what §4 predicted and §6 measured from the other side: the gap
between the arms IS on-floor influence, the additive arm carries it as one
number, and transplanting a third of it into the structural arm moved the
structural arm most of the way to parity. There was never a second body of
information to combine.

### The one place the blend earns more

| slice | error correlation | optimal additive weight | best blend RMSE gain |
|---|---:|---:|---:|
| all cells | 0.9856 | 0.679 | +0.15% |
| **novel fives** | 0.9876 | **0.459** | **+0.26%** |
| previously seen | 0.9845 | 0.782 | +0.07% |

On lineups that never played, the blend is worth nearly four times what it is
worth on lineups that did, and the optimal weight sits near 50/50 — not because
the arms disagree more there, but because neither dominates: additive's edge on
seen fives disappears on unseen ones. The plain average's novel MAE, **8.8668**,
is the best novel number measured anywhere in this workstream.

### What this means for research direction

**Stop looking for gains from combination.** Ensembling these two arms caps out
at 0.15% of RMSE and the cap is nearly reached by a 50/50 average, so there is
nothing left in that direction. Ship the blend because it is free and slightly
better, not because it is a finding.

The corollary is the useful part: **more accuracy requires information neither
arm has.** Both are built from the same player-identity-and-box-score substrate,
and their errors say so. The open leads that are not more of the same substrate
are the ones §8 and §9 named — the volume channels the own/teammate split cannot
yet identify, shot quality, and opponent-aware matchups — plus the tracking-
derived inputs in `MODEL_RESEARCH_ROADMAP.md` R03/R04. The structural arm's case
was never incremental accuracy; it is mechanism, and the novel-five slice.

    python -u -m experiments.onfloor_blend

## 8d. Sizing the next levers

Two descriptive measurements on the evaluation cells (`onfloor_levers.py`).
Neither is a deployable arm; both size a lever.

**A reporting inconsistency, first.** `metrics()` computes raw r² possession-
weighted and Pearson correlation UNWEIGHTED, so the correlations quoted through
this document (0.2898 → 0.2975, etc.) are unweighted and are not on the same
scale as the r² beside them. Every arm is measured the same way so the contrasts
stand, but the weighted correlations are lower: **0.2052 structural, 0.2265
additive.**

**Dispersion.** Both calibrated arms remain over-dispersed. The prediction's
spread is 0.261 of the actual spread against a weighted correlation of 0.205, so
the MSE-optimal extra shrink is **λ = 0.785** for structural and 0.835 for
additive, worth **0.53% and 0.46% of MSE**. Small, free, and it applies to both
arms, so it changes no comparison — but it is real, and it points at the same
thing the project's horizon-0 shrink already says: these ratings should be
trusted less than they are.

**Strength of defences faced — the big one.** Every offensive cell met a
particular mix of defences; its forecast assumes the league. With the defensive
arm of §9 that mix is now measurable. Its spread across cells is **1.67 pts/100**,
and regressing each arm's forward residual on it, centered within quarter:

| | slope | block-bootstrap SE | t |
|---|---:|---:|---:|
| structural residual | **−0.8135** | 0.0792 | **−10.3** |
| additive residual | −0.8746 | 0.0868 | −10.1 |

The slope is close to −1, which is what it should be if the defensive score is a
well-scaled measure of the defence faced: a five that drew defences one point
per 100 weaker scores about one point per 100 more than either model expects.

**Size.** The opponent mix explains `slope² × var` ≈ 1.8 (pts/100)², about
**1.5% of cell-level MSE — but 14% of everything either model explains**, since
both sit at r² ≈ 0.11–0.12. It is larger than the entire additive-versus-
structural gap and roughly six times what the on-floor influence layer bought.
Neither arm uses any of it.

It is available two ways, and they are different claims. As an **evaluation**
correction it is unimpeachable: the target is currently contaminated by a
schedule neither model was asked to predict. As a **prediction** feature it
requires a named opponent — which is exactly what the two-lineup product
specifies, and is not available in the current one-sided benchmark.

## 8e. Opponent adjustment — the first lever, taken

§8d sized the strength-of-defences-faced lever; `onfloor_opponent.py` takes it,
as an evaluation correction. Each possession's defensive five is priced with the
additive fit's defensive half centered on its own strictly prior reference, put
on the calibrated points scale by the defensive arm's OWN prior-only slope, and
averaged over the possessions a cell actually played. Only the DEVIATION from
the window's average schedule is removed; the level stays with the league term.
The adjustment coefficient is **1 by construction** — the defensive prediction
is already in points per 100 — and every arm is recalibrated prior-only against
the adjusted target, so the comparison stays like for like.

Schedule deviation spread across cells: **0.993 pts/100.**

| arm | raw MAE | adjusted MAE | season-paired | raw r² | adjusted r² |
|---|---:|---:|---|---:|---:|
| structural + influence | 8.1418 | 8.1193 | −0.0245 ± 0.0132 (8/11) | 0.1110 | 0.1158 |
| additive | 8.0927 | 8.0537 | −0.0409 ± 0.0140 (9/11) | 0.1201 | 0.1261 |
| blend | 8.0763 | **8.0417** | −0.0361 ± 0.0137 (9/11) | 0.1219 | **0.1276** |

On **novel fives the gain is largest**: the blend goes 8.8668 → **8.8229**, and
its r² 0.1062 → 0.1119. Unsurprising — a five with little history also has a
small, lumpy sample of opponents, so its schedule deviates further.

**It works.** The residual-on-schedule slope goes **−1.194 → −0.209**, so a
coefficient of exactly 1, fitted on nothing, removes 83% of the contamination.

**Three honest qualifications.**

*It is smaller than §8d estimated.* That section sized the lever from the raw
defensive score's spread of 1.67; the quantity that actually matters is the
calibrated, within-window-centered schedule deviation, which is 0.993. The
lever is real and it is about half what the first estimate implied.

*A fitted coefficient does not help.* A prior-only κ (mean 1.059, range
[0.924, 1.432]) removes more of the contamination — residual slope −0.149
against −0.209 — and yet scores slightly WORSE (blend 8.0440 against 8.0417),
because its per-origin noise costs more than its extra correction buys. The same
pattern as §8c, where a fixed 50/50 average beat a free joint fit: κ = 1 is both
the assumption-free choice and the better one. A free fit on the evaluation data
wants 1.194, which is the honest size of what κ = 1 leaves behind.

*It helps the additive arm more.* −0.041 against −0.025, so the gap between the
arms widens slightly, 0.049 → 0.066. The schedule contaminates both, and there
is no reason a correction to the target should favour either; the difference is
within its own uncertainty and should not be read as one.

**What it is and is not.** This is a correction to the TARGET: the population
now measures how good a five is rather than how good it was against the
defences it happened to draw. It is not a model improvement and no arm predicts
anything new. The prediction-side use — conditioning a forecast on a NAMED
opposing five — needs a two-sided population the current benchmark does not
have, and is what `CONTEXTUAL_MODEL.md`'s two-lineup product asks for.

    python -u -m experiments.onfloor_opponent

## 8f. The two-lineup forecast, which is the northstar

`CONTEXTUAL_MODEL.md` asks for a tool that compares two five-man lineups. With
a defensive arm (§9) and an opponent term validated at coefficient 1 (§8e),
`onfloor_influence_swap.py --opponent` produces one: a five priced against a
NAMED defensive five rather than against the league, with the mechanism on both
sides.

Dallas at the 2025q3 cutoff against a Gobert-anchored Minnesota five:

```
five: Dončić, Irving, P.J. Washington, Gafford, Thompson
  2PA/100 53.9   3PA/100 36.7   FTA/100 22.5   TO/100 12.6
  versus a league-average defence          120.59 pts/100
opposing five: Gobert, McDaniels, Edwards, Conley, Randle
  defensive term  −3.011 pts/100  (raw −4.134 × prior-only slope 0.728, 5/5 priced)
  versus THIS defence                      117.58 pts/100
swap Irving out, Harden in                 116.36 pts/100   (−1.22)
```

**The two sides are added, not interacted**, which is a deliberate limitation
rather than an oversight: `matchup_noise_floor.md` records that off × def
matchup effects sit at the noise floor (reliability +0.02 against +0.25 for
teammate pairs), so an interaction term would be fitting noise. The consequence
is visible above — the Harden swap costs the same 1.22 against any defence.

Everything the §6 caveats say still applies: it is a forecast for a five that
never played, against a defence it never faced, from strictly prior inputs.

## 8g. Shot mix — the total is real, the split still is not

§8 left the volume channels unidentified. This is the follow-up, and it starts
by asking what kind of error the volume error is. Across identities with ≥20,000
prior possessions, the team-level influence on two-point and three-point
attempts correlates at **−0.504**, and the standard deviation of their SUM
(1.239) is barely below either component (1.352, 1.094). So it is roughly half
substitution and half level — and the substitution half has a name.

The sign pattern says which way. The largest positive three-point-attempt shifts
belong to **Giannis, Ben Simmons, Luka, John Wall, Blake Griffin, De'Aaron Fox** —
rim pressure and drive-and-kick. The largest negative ones belong to **Danny
Green, Malik Beasley, James Jones, Bruce Bowen** — three-point specialists. That
is not "specialists suppress threes"; it is the model **over-extrapolating a
specialist's own-context rate into a new lineup**, which is the profile-measured-
in-his-own-context problem `context_profile.py` named.

### Why composition and not volume

A lineup's usage is zero-sum: the budget is fixed, so "he shoots more" and "his
teammates shoot less" are close to the same statement, which is why §8's split
could not separate them. **A composition is not zero-sum** — everyone's
three-point share can rise at once. So four composition channels were added,
each an attempt-weighted rate of what a player does WITHIN his own attempts:
`three_share`, `rim_share`, `ft_rate`, `assisted_share`.

### The split does not identify, for a second and different reason

Reported because it is the second identification failure in this document and
they are not the same failure.

The own block is intrinsically worse conditioned than the teammate block: a
player's own column carries his own possessions, while his teammate column
appears once in each of four teammates' rows, so at equal penalty the teammate
block is shrunk roughly three times less and wins by construction.

The first grid made this visible the wrong way — the own penalty ran off the top
edge in **19 to 34 of 44 origins** and the "teammate" coefficient came back
correlated **0.98 to 1.00 with the TOTAL**, which is an artifact, not a split.
Widening both ends (rule 10) did not rescue it: the selector then **annihilates
the own block outright** in 13 to 30 of 44 origins, and `4 × teammate` equals the
total to four decimals. The teammate parameterisation can reproduce the same
fitted values more cheaply, and lineup variation does not separate them at this
precision.

**So no teammate claim is made for composition.** What the fit determines
robustly is the TOTAL composition effect, and that is what is reported below.

### The totals are real, and they are the shot-mix error

The held-out selector keeps the composition block in **41/44, 36/44, 35/44 and
43/44** origins for the four channels. The lists are tops of their columns,
not chosen, and each one names a mechanism the model does not have:

| channel | who raises it most | what it is |
|---|---|---|
| **three-point share** | Zion, Giannis, Harden, Embiid, Griffin, Dončić, Rose, LeBron, Simmons | rim pressure creating kick-outs |
| **rim share** | **Curry**, Carmelo, Kevin Love, Cousins, Ray Allen, Pierce, Klay, Dirk, Korver | **spacing** — shooters creating rim attempts for others |
| **assisted share** | Nash, Rondo, Dončić, Harden, Zion, Barea, Baron Davis, LeBron, Embiid, Shai | playmaking |
| free-throw rate | Clifford Robinson, Tony Allen, Matt Bonner, Tolliver, McCarty | **not interpretable — treat as the weak channel** |

The rim-share column is the one to notice. The project's standing finding is
that **spacing is null** (`the_ball_is_the_interaction`: shot_rim × r3pa reads
−0.000001, t = −0.44). That was measured on the POINTS target. Here the same
mechanism appears cleanly in the shot-mix channel, with Curry, Korver, Ray Allen
and Dirk at the top — which is what spacing is supposed to look like, and is
consistent with the project's own explanation for why points-channel searches
fail: three quarters of possession-points variance is make/miss noise.

`assisted_share` also replicates `CREATION_EXPERIMENT.md`'s finding that teammate
passing support predicts assisted-made share, from a different design.

### The lever this identifies

The structural model holds each player's shot mix FIXED — `r3pa` and the six
location shares are properties of the player, carried unchanged into any
lineup. These coefficients say that is wrong, lineup-dependently, in a direction
basketball explains. Making the mix a function of the five is the accuracy
pathway; it is not scored here, because `asof_point_allocation.predict` takes no
per-player mix override and adding one is a change to the allocation itself
rather than a shift applied after it.

    python -u -m experiments.onfloor_attribution_run --build --composition

## 8h. The mix-aware allocation is NULL — for a narrower reason than first stated

§8g measured a real, basketball-legible shot-mix effect and named the lever:
make the model's fixed per-player mix a function of the five. `onfloor_mix.py`
does it properly — it mirrors `asof_point_allocation.predict` step for step
rather than wrapping it, because a mix change belongs BEFORE the usage
normalisation and the category factors, and it reproduces the original to 1e-12
at zero shift (asserted in the tests).

Each player's usage is held fixed while his mix moves: a free-throw-rate change
recomputes attempts through the model's own identity
`fga = (usage − turnovers) / (1 + 0.44 ftr)`, so a mix shift never smuggles in a
volume change. Rim share cannot exceed the two-point attempts that carry it, and
clips are counted (11–15 per origin).

Because §8g could not identify own from teammate, both extreme readings were
scored — they distribute the same total differently across players with
different shot volumes, so the forward test answers what the fit could not — plus
a placebo that keeps the shift magnitudes and PERMUTES the coefficients across
identities.

| arm | MAE | RMSE | raw r² | corr | novel | vs parent | vs placebo |
|---|---:|---:|---:|---:|---:|---|---|
| parent | 8.1440 | 10.9214 | 0.1073 | 0.2898 | 8.8903 | — | |
| mix, own attribution | 8.1359 | 10.9220 | 0.1072 | 0.2889 | 8.8952 | −0.0073 ± 0.0034 (8/11) | −0.0057 ± 0.0049 (8/11) |
| mix, teammate attribution | 8.1402 | 10.9210 | 0.1074 | 0.2895 | 8.8849 | −0.0040 ± 0.0031 (7/11) | −0.0024 ± 0.0041 (7/11) |
| mix + on-floor influence | 8.1394 | 10.8980 | 0.1112 | 0.2974 | 8.8951 | +0.0020 ± 0.0371 (5/11) | +0.0037 ± 0.0384 |
| **placebo (permuted identities)** | 8.1427 | 10.9212 | 0.1074 | 0.2899 | 8.8909 | −0.0017 ± 0.0023 (5/11) | — |

**It is null.** The best arm beats the placebo by 0.0057 ± 0.0049 — t = 1.2 — and
its RMSE, r² and correlation are all very slightly WORSE than the parent's. The
correction is not inert: it moves each cell's prediction by 0.21 pts/100 on
average, against the placebo's 0.13. It moves things; it does not move them
usefully.

Nor is it pointing the wrong way. Regressing the parent's residual on the
correction, centered within quarter, gives slope **−0.585** for the own
attribution and −0.551 for the teammate one against **−0.385** for the placebo,
so the real coefficients do carry direction the permuted ones do not. The
direction is right and the size is nothing.

### Why: the model prices a mix swap at 0.0137 points

At the 2026q4 environment, the conditional valuation says a two-point attempt is
worth **0.4456** points and a three-point attempt **0.4593**. Moving one attempt
from a two to a three is therefore worth **+0.0137 points** — and the making term
adds nothing, because it is defined as shooting ABOVE the shot-mix expectation
and is zero at league skill by construction.

So a two-percentage-point shift in three-point share on about 90 attempts per
100 possessions is 1.8 attempts moved, worth **0.025 points per 100**. That is
the whole prize, and it is an order of magnitude below the noise.

**The model is nearly indifferent to the TWO-VERSUS-THREE distinction at fixed
volume** — and that is a fact about basketball, not a defect. On the league mix
the average two and the average three really are worth about the same, which is
why teams are indifferent at the margin.

**It is NOT indifferent to where the shot comes from.** See §8i, which corrects
the first version of this section: the model's per-location valuation tracks raw
points per attempt at **+0.989**, and moving an attempt from a long two to the
rim is worth **+0.548** — forty times a two-to-three swap. The null above is
therefore a statement about the CHANNELS THIS ARM MOVED, not about the model's
sensitivity to shot quality.

    python -u -m experiments.onfloor_mix_score

## 8i. Correction: the model prices LOCATION well, and that is the lever

§8h's null stands and its arithmetic is right, but the explanation I drew from
it was too broad and is corrected here rather than quietly edited. The claim was
"the structural model is nearly indifferent to shot mix at fixed volume, by
design." It is not.

At the 2026q4 environment, per location bucket:

| bucket | share of FGA | FG% | raw points per attempt | model valuation |
|---|---:|---:|---:|---:|
| rim | .2608 | .681 | **1.3613** | **0.6928** |
| paint | .1731 | .446 | 0.8915 | 0.2956 |
| mid | .0982 | .448 | 0.8964 | 0.2376 |
| long mid | .0602 | .410 | **0.8201** | **0.1450** |
| corner three | .0065 | .377 | 1.1314 | 0.5032 |
| above the break | .4012 | .364 | 1.0909 | 0.4586 |

The model's conditional valuation correlates with raw points per attempt at
**+0.989**, and its spread across buckets (0.548) matches the raw spread (0.541).
Moving one attempt from a long two to the rim is worth **+0.548** in the model
and +0.541 in reality. **The valuation already prices shot quality by location,
and prices it well.**

What is worth ~nothing is the two-versus-three TYPE distinction on the league
mix — 0.4456 against 0.4593, a 0.0137 difference — because league twos are a
blend of rim (1.36) and long mid (0.82) that averages out near a three. That is
basketball, not a modelling error.

**So §8h was null because it moved the wrong things.** Its channels were
`three_share`, worth 0.0137 per attempt moved, and `rim_share`, whose measured
coefficient was only 0.39 percentage points. The six-bucket location mix — the
one that can express "fewer long twos, more rim" — was never modelled.

### Sizing the real lever

`onfloor_location_size.py` prices, for each evaluation cell, the gap between the
located attempts the model predicted and the ones the five actually took:

- within-quarter sd of that gap: **2.9604 pts/100**, three times the
  opponent-schedule lever;
- mean **+0.6716**, so the allocator's location mix is systematically too
  conservative;
- split-half on game parity, 3,890 cells with ≥20 possessions a side:
  half-to-half correlation +0.117, Spearman-Brown reliability **0.209**;
- so the **reliable** part of the gap is **1.354 pts/100** — larger than the
  opponent adjustment already banked.

That 1.354 is still an upper bound on a forecastable lever: a split-half inside
one window cannot tell a transferable lineup property from stable within-window
deployment or schedule. But it is the right order of magnitude, and it is
measured rather than assumed.

### What this means for tracking data

**Tracking data is not needed to price location** — the model already does.
What tracking would add is quality WITHIN a bucket: how open the shot was, how
far the nearest defender stood. That is a real further step and an external
dependency, and it is no longer the first thing. The first thing is a
lineup-dependent SIX-BUCKET location mix, using existing data and the valuation
that already prices it correctly.

## 8j. Second correction: the location mix is CANCELLED, and that is the defect

§8i corrected §8h and went too far the other way. It is corrected here, in the
same style, because I propagated it into `CLAUDE.md`, `BACKLOG.md`,
`SESSION_HANDOFF.md`, a memory and `STRUCTURAL_MODEL.md`, and made it the
project's top-ranked next build.

§8i priced a long-two-to-rim move at **+0.548** and concluded "the valuation
already prices shot quality by location, and prices it well." That number came
from the **valuation column alone**. The model does not score a shot with the
valuation alone. It scores it with the valuation PLUS a making term that
subtracts the league make rate at the very locations the player shoots from:

    making = 2 * 2PA * (self_2p - two_mix @ league_pct_by_location)

so a player who moves to the rim is expected to make more, and is credited less
for making it. The two nearly cancel. Perturbing a real origin's profiles and
re-scoring through `asof_point_allocation.predict` itself, 2026q4, 134 cells:

| move | share of 2PA moved | points | per attempt moved |
|---|---:|---:|---:|
| long mid → rim | 4.62% | +0.0153 /100 | **+0.0062** |
| mid → rim | 4.92% | −0.0252 /100 | **−0.0096** |
| long mid → paint | 4.62% | +0.1811 /100 | +0.0735 |

**§8i said that first move was worth +0.548. It is worth +0.006, ninety times
smaller, and the second move is NEGATIVE.**

### Why, exactly

The model's two-point score decomposes exactly — verified to 2.2e-14 —

    2-point score = 2 * 2PA * self_2p  +  sum_b 2PA_b * (value_b - 2 * pct_b)

The first term does not contain the mix at all. So **the only route by which
shot location reaches the score is the second term**, and `value_b - 2*pct_b` is
the possession's opportunity cost, which is nearly the same at every bucket:

| bucket | value_b | 2 x league pct | difference |
|---|---:|---:|---:|
| rim | 0.6928 | 1.3613 | −0.6684 |
| paint | 0.2956 | 0.8915 | −0.5959 |
| mid | 0.2376 | 0.8964 | −0.6588 |
| long mid | 0.1450 | 0.8201 | −0.6752 |

Spread **0.0793** against the 0.548 §8i quoted. A mix shift sums to zero across
buckets, so it is multiplied by the SPREAD of that column, not by the spread of
the valuation. Location is 90% priced out of this model by construction.

### The real defect, and it is bigger than the lever it replaces

The identity above says it plainly: **the model asserts that a player's
two-point percentage does not depend on where he shoots from.** `self_2p` is a
single number, so a center's rim attempts and a guard's long twos convert at the
same personal rate. That is false, it is the reason the mix cancels, and it is a
counterfactual failure exactly where the project cares: move a rim-finisher into
a lineup that generates rim attempts and the model gives him nothing for it.

The fix is not a lineup-dependent mix on top of a model that cannot feel it. It
is **location-specific conversion** — replace the scalar `self_2p` with per
bucket make rates `self_2p_rim`, `self_2p_paint`, `self_2p_mid`,
`self_2p_longmid` (and `self_3p_c3`, `self_3p_ab3`), so that

    2-point score = sum_b 2 * 2PA_b * self_2p_b  +  sum_b 2PA_b * (value_b - 2 * pct_b)

Then moving an attempt from a long two to the rim is worth
`2 * (self_2p_rim - self_2p_longmid)`, about **+0.54 for a league-average
player** — the number §8i wanted, now EARNED by the player's own skill at that
location rather than cancelled. It also makes §10's shot-quality coefficient
location-aware, and it is the precondition for any lineup-dependent mix to be
worth building.

The data exists: `shot_quality.build()` already caches 5,372,539 field goals
with distance on 100% and the shooter matched on 98.9%, and
`possession_outcomes._bucket2` defines the buckets (rim ≤3ft, paint ≤9, mid ≤15,
long mid >15; corner three ≤22ft).

### What §8i still gets right

The valuation's +0.989 correlation with raw points per attempt is real, and the
2-versus-3 type distinction really is worth only 0.0137. What was wrong was
reading the valuation in isolation, and the sizing that followed:
`onfloor_location_size.py`'s 1.354 pts/100 "reliable location gap" is priced with
the same valuation-only arithmetic and is therefore an upper bound on a
quantity the current model cannot express, not a lever waiting to be taken.

## 9. The defensive half — now scored, 2026-09-08

Both halves of the ten-identity design were always estimated, and so is the
additive fit's (`theta`, `delta` and `eta` run over 2 × n_players, and
`asof_point_calibration.additive_offense_score` says in its own comment that
"the defensive half prices the other team's five"). Neither had ever been
scored, for one reason: the completed run's cells are OFFENSIVE fives facing a
league-average defence, so the population does not name the defence it faced.

`onfloor_defense_run.py` builds the missing population — every defensive five
with ≥50 possessions in an origin's window, and the points it actually allowed —
on the same 44 rolling origins. It is larger than the offensive one:
**8,340 defensive fives / 1,010,779 possessions**, median exposure 81.

Sign convention: both targets are what the OFFENCE did, so a positive
coefficient is points allowed and a good defender is negative. No flip anywhere.

### Face validity of the coefficients

**Most turnovers forced per 100** (2026q4, ≥6,000 prior defensive possessions):
Alex Caruso **+3.44**, Matisse Thybulle +2.90, Tony Allen +2.65, Brevin Knight
+2.36, Ricky Rubio +2.22, Mario Chalmers +2.21, Xavier Tillman +2.14, Herbert
Jones +2.10, Kris Dunn +2.08, Ausar Thompson +2.01.

**Most two-point conversion suppressed, percentage points**: Victor Wembanyama
**−4.68**, Chet Holmgren −4.66, Rudy Gobert −4.53, Alonzo Mourning −4.40, Joel
Embiid −3.94, Walker Kessler −3.94, Kevin Garnett −3.85, Tim Duncan −3.85,
Dikembe Mutombo −3.78, Joel Anthony −3.54. Gobert also pushes opponents to
**+1.41 more threes and −2.37 fewer free throws per 100**, which is the drop
coverage signature written in the channels rather than asserted.

Neither list was chosen; they are the tops of their columns.

### Forward accuracy, against a league-level null

| arm | MAE | RMSE | bias | raw r² | corr | novel MAE | season-paired ΔMAE vs league |
|---|---:|---:|---:|---:|---:|---:|---|
| league level only | 8.6219 | 11.3820 | −0.799 | 0.0661 | 0.2260 | 9.4432 | — |
| **additive defensive half** | 8.3398 | 11.0817 | −0.720 | 0.1147 | 0.2925 | 9.2049 | **−0.2887 ± 0.0360 (11/11)** |
| **influence defensive channels** | 8.3984 | 11.1588 | −0.959 | 0.1023 | 0.2780 | 9.2225 | **−0.2285 ± 0.0267 (11/11)** |
| **both, priced separately** | **8.3314** | **11.0750** | −0.772 | **0.1158** | **0.2939** | **9.1950** | **−0.2975 ± 0.0360 (11/11)** |
| **defensive FT placebo** | 8.6219 | 11.3820 | −0.799 | 0.0661 | 0.2260 | 9.4432 | **+1.6e-16 (0/11)** |

**Both defensive arms beat the null in 11 of 11 seasons**, at roughly eight
times their own SEM. That is a different kind of evidence from the offensive
influence result in §6, whose MAE gain was never established — here the
comparison is a model against nothing, and it is not close.

**The placebo is identical to the null to 1.6e-16.** Given a free slope on
completed prior windows, the calibration set it to exactly zero for the
defensive free-throw channel at every origin. Nothing a defence does changes an
opponent's free-throw shooting, and the calibration discovered that unprompted
for a second time, on a second population.

The channel arm adds a little over the additive defensive rating (8.3314 against
8.3398), so a defensive rating decomposed into forced turnovers, suppressed
conversion and shifted shot mix is not merely a re-description of the same
number — but the increment is small and unestablished on its own.

### Do not read this as bigger than the offensive result

Against the crudest possible null, `|actual − league|`, the offensive cells sit
at **9.014** and the defensive at **8.629**. The best offensive arm takes 0.92
off its null; the best defensive arm takes 0.30 off its own. **The same class of
model captures about a third as much on defence as on offence**, which agrees
with the project's standing finding that the box score explains 78% of offensive
rating and 52% of defensive. The defensive result is decisive in significance
and modest in size.

What is now true that was not: there is a defensive population, a defensive
comparator, a defensive placebo that behaves, and two arms that beat the null on
every season. `CONTEXTUAL_MODEL.md`'s requirement that both sides ship is no
longer blocked on estimation.

    python -u -m experiments.onfloor_influence_readout --origin 2026q4 --side defense
    python -u -m experiments.onfloor_defense_run

## 10. Shot quality IS measurable from this data — Adam's test, 2026-09-08

Adam's hypothesis: fit field-goal percentage as a function of distance from the
hoop, then compare the residuals for one team's shots with a player on and off
the floor. If the residual is higher with him on, that is shot quality the model
does not have.

**It is right, and it survives the check that kills most on/off results.**

### The data was always there

The raw distance is in the play-by-play text of every shot and has never been
kept: `possession_outcomes.py` reads it only to assign a six-way bucket and
`game_player_stats.py` keeps a per-game mean. `shot_quality.py` keeps the shot —
**6,846,563 attempts (5,372,539 field goals, 1,474,024 free throws)**, with
distance on **100%** of field goals and the shooter matched to the five on the
floor on 98.9% of them.

The isotonic fit is a nuisance function: monotone non-increasing by
construction, fitted once on all 5.37M attempts, shared by both sides of every
comparison so it cannot manufacture a difference. It reads 0 ft → .666,
3 ft → .482, 5–15 ft → .407, 20 ft → .397, 24 ft → .376, 30 ft → .306.

### Jokić, Denver shots, on minus off

| control | field goals (distance-adjusted) | free throws (PLACEBO) |
|---|---:|---:|
| none | **+4.80** | **+4.63** |
| shooter fixed effects | +1.84 | −0.42 |
| shooter + game fixed effects | **+1.69 ± 0.36 (t = 4.7)** | **+0.38** |

**The raw number is personnel, and the placebo proves it.** A free throw has no
defender and no distance, yet Denver's free-throw percentage is 4.6 points
higher with Jokić on. The players who share his minutes are simply better
shooters than the bench, and the naive +4.80 is mostly that.

**Shooter fixed effects remove it.** The comparison becomes the same man on and
off; the placebo collapses to zero and the field-goal effect survives. Game
fixed effects then remove opponent team, venue and game state, and it barely
moves. Shooter fixed effects also handle his OWN shots without a special case —
they are all in the "on" group, so after demeaning they contribute nothing —
which makes this a teammates-only estimate by construction.

**So the same players make 1.69 percentage points more of their field goals,
from the same distance, when Jokić is on the floor, and their free throws do not
move.**

### The league, and the aggregate checks that matter

933 players with ≥8,000 on-floor and ≥3,000 off-floor field goals:

| statistic | mean | sd |
|---|---:|---:|
| raw on/off | −0.133 | 1.067 |
| + shooter FE | −0.067 | 0.657 |
| + shooter and game FE | −0.075 | 0.628 |
| **free-throw placebo, same FE** | **+0.068** | 0.902 |

1. **The placebo vanishes in aggregate**: mean +0.068 pp against a raw personnel
   effect of +3 to +5.
2. **The placebo does not track the signal**: correlation between a player's
   field-goal effect and his free-throw placebo is **+0.099**.
3. Jokić sits **4.5 true sd above the mean, 99.2nd percentile**.

Top of the list: Jamal Murray +2.03, Baron Davis +1.83, **Curry +1.80**, Doug
Christie +1.76, Chris Webber +1.74, **Embiid +1.71**, **Jokić +1.69**,
**Wembanyama +1.61**, Iverson +1.61, **Draymond Green +1.50**. Bottom: Jaxson
Hayes −2.35, Shabazz Muhammad −2.00, Jahlil Okafor −1.95.

### What it is worth, and what is not yet established

Between-player variance decomposes into a true sd of **0.396 pp** against a mean
sampling variance that gives **reliability 0.397** — most of the observed spread
is noise, and only the extremes are individually resolvable (61 players positive
and 63 negative at |t| > 2, against ~46 expected by chance).

In points: a lineup takes about 90 field-goal attempts per 100 possessions at
roughly 2.4 points per make, so one percentage point of shot quality is about
**2.2 points per 100**. A one-sd player is worth ~0.86, and Jokić ~3.6 —
comparable to the opponent lever (0.99) and the location lever (1.35), and
**entirely absent from the model**, which carries a fixed `self_2p` and
`self_3p` per player.

**This is descriptive and in-sample. It is not yet a forecast**, and by this
project's own rules that is the only thing that counts. The next step is the
forward test: estimate each player's shot-quality coefficient on data strictly
before an origin, and ask whether it predicts his teammates' distance-adjusted
shooting in the window after it. Reliability 0.397 says heavy shrinkage will be
needed, and the honest prior is that a large part of this will not carry.

Three further limits. The isotonic curve uses distance alone, so a corner three
and an above-the-break three at the same distance are pooled, and "at rim" shots
with no numeric distance are all recorded at zero feet. Game fixed effects
control the opponent TEAM, not the particular defensive five on the floor. And
none of this is causal: lineups are not randomly assigned.

    python -u -m experiments.shot_quality_sweep

## 10b. It FORECASTS — and only if it is shrunk

§10 was descriptive. `shot_quality_forward.py` is the test that counts: at every
one of 44 origins the isotonic distance curve, each shooter's baseline and each
player's on/off coefficient are refitted on data **strictly before** the origin,
and used to predict the shots taken after it.

    P(make) = isotonic(distance) + shooter baseline + sum of TEAMMATE coefficients

Both the baseline and the coefficient are shrunk by their own exposure,
moment-matched in the project's own style: `tau² = var(estimates) − mean(sampling
variance)`, each estimate keeping `tau²/(tau² + se²)`. The independent-shot
sampling variance is justified: a game-level block bootstrap gives standard
errors **0.96×** the independent-shot ones, so clustering costs almost nothing
for this statistic.

**2,657,801 field goals and 678,990 free throws scored out of sample.**

| | slope on the teammate term | SEM | seasons positive | Brier gain, shrunk | Brier gain, RAW |
|---|---:|---:|---:|---:|---:|
| **field goals** | **1.082** | 0.084 | **12/12** | **+7.07e-5** | **−27.3e-5** |
| free throws (placebo) | −7.92 | 17.66 | 3/12 | +4.05e-5 | −53.7e-5 |

A slope of 1.0 means the shrunk coefficient is correctly scaled out of sample;
0 means it forecasts nothing. **It comes out at 1.082 ± 0.084, positive in all
twelve seasons** (season slopes 0.68 to 1.45). The empirical-Bayes shrinkage is
not merely helpful, it is calibrated.

### The answer to "do we shrink by sample size?" is that nothing works without it

The raw, unshrunk coefficient makes forecasts **worse** — Brier −27.3e-5 — while
the shrunk one makes them better at +7.07e-5. Shrinkage keeps **20%** of the raw
field-goal spread. That is the whole difference between a usable parameter and a
harmful one, and it is exactly what reliability 0.397 predicted.

### The placebo passes in the most informative way available

The free-throw channel is not argued down; **the empirical Bayes annihilates it
on its own**. Its `tau²` collapses, so shrinkage keeps **1%** of its raw spread
against 20% for field goals — a factor of twenty. The procedure was never told
which channel was the placebo; it detected that free-throw on/off is noise and
removed it. The residual slope of −7.9 ± 17.7 is then meaningless by
construction, because there is nothing left to scale, and that is the right
reading of it.

### What it is worth

The shrunk teammate term has a spread of **0.389 percentage points** of
field-goal percentage across shots, realised at slope 1.082, so **0.42 points of
FG% of true lineup spread**. At about 90 attempts per 100 possessions and 2.4
points per make that is **0.91 points per 100 of lineup spread** — the same
order as the opponent adjustment (0.99) and larger than anything else added in
this workstream, and the structural model has no term for it at all.

### A bug this found

The first forward run reported slope 0.810. Its two-way demeaning drained one
key fully and then the other, which is sequential residualisation and leaves the
first key's means non-zero — not two-way fixed effects. A test written for the
purpose caught it (`test_two_way_demeaning_removes_both_sets_of_means`), and
alternating the sweeps properly moved the slope to 1.082. The §10 league sweep
was unaffected; it had the loops the right way round.

### Still open

This is a shot-level forecast, not a points-level one. Feeding the coefficient
into the structural arm's making term and scoring it on the completed run's own
cells is the next step, and is the only thing that would let it change a lineup
rating. The controls are shooter and game, so opponent TEAM is removed but not
the particular defensive five.

    python -u -m experiments.shot_quality_forward

## 10c. Priced in points: right direction, clean placebo, not established

§10b showed the coefficient forecasts at the shot level. A shot-level forecast
changes nothing until it is priced, so `shot_quality_points.py` puts it into the
structural arm's own making term and scores it on the completed run's own cells,
against the parent every arm here is measured against.

The arithmetic is the model's: player q's make probability shifts by the sum of
his teammates' coefficients, and the points are
`Σ_q (2·2PA_q + 3·3PA_q) × (sum of the other four)`, using the allocation's own
per-player attempts, so a coefficient earns more in a lineup that shoots more.
Zero coefficients reproduce the parent, which is gate-checked to 1e-13.

| arm | MAE | RMSE | raw r² | corr | novel | season-paired vs parent |
|---|---:|---:|---:|---:|---:|---|
| parent | 8.1440 | 10.9214 | 0.1073 | 0.2898 | 8.8903 | — |
| **shot quality, shrunk** | **8.1321** | **10.9048** | **0.1100** | **0.2922** | **8.8745** | −0.0103 ± 0.0158 (5/11) |
| shot quality, RAW | 8.1583 | 10.9332 | 0.1054 | 0.2863 | 8.9077 | +0.0150 ± 0.0277 (5/11) |
| **placebo** | 8.1451 | 10.9228 | 0.1071 | 0.2898 | 8.8898 | +0.0009 ± 0.0012 (6/11) |
| combined with §6 influence | 8.1421 | 10.8990 | 0.1110 | 0.2967 | 8.9005 | +0.0045 ± 0.0375 |

**Every metric moves the right way** — MAE −0.012, RMSE −0.017, r² +0.0027,
correlation +0.0024, and novel-lineup MAE −0.016. **The placebo is the parent**
(+0.0009 ± 0.0012); its term's spread on these cells is 0.023 pts/100 against
0.765 for the real one, a factor of 33, because the empirical Bayes had already
annihilated it. **And the unshrunk version is worse than doing nothing**
(+0.0150), which is the Brier result of §10b reappearing in points.

**But the MAE gain is not established**: −0.0103 against a season-paired SEM of
0.0158.

### What that says about the evaluation, not the mechanism

The term is worth 0.765 pts/100 of spread across cells and the calibration keeps
0.689 of it, moving each prediction by about 0.5 pts/100. Against cell-level
error of ~11 pts/100 RMSE and 44 origins, that is simply below what this
population can resolve. The comparison is calibrated by what has resolved here:
the opponent adjustment, worth about three times as much, established at
−0.036 ± 0.014 with 9/11 seasons; the on-floor influence layer at 0.011 did not;
shot quality at 0.012 does not either.

So the honest statement is that **this benchmark can establish a mechanism worth
roughly 0.04 MAE and cannot establish one worth 0.01**, and shot quality is in
the second class. It forecasts — that was settled at the shot level on 2.66M
attempts, where the noise is a thousand times smaller — and it prices in the
right direction with a clean placebo. Whether it belongs in a shipped scorer is
a judgement about mechanism and the counterfactual standard, not something the
point benchmark can answer at this size.

    python -u -m experiments.shot_quality_points

## 11. The other three factors — turnovers, steals, rebounding, 2026-09-08

Adam: *"What about turnovers? Steals? Rebounding (defensive and offensive)?
Shai reducing team turnovers, Josh Hart increasing team steals, Steven Adams
increasing team offensive rebounding. Is this in the current model?"*

### Is it in the model? Mostly no, and the part that is there has the wrong denominator

The structural profile (`asof_state.PROFILE_FIELDS`) carries **`rtov` and
`rorb`** — a player's OWN turnover and offensive-rebound rates — and nothing
else from this family. `stl`, `drb`, `blk` and the foul columns all exist in
`game_player_stats` and the profile never reads them. Defensive rebounding is
absent *in concept*, not merely from the feature list, because the structural
arm is offence-only (§9 built a separate defensive half).

And both of the rates that are there are **per possession**, which conflates two
different things. Steven Adams's claim is not "his team misses more"; it is "his
team collects more of the misses it takes". Those need different denominators:

| channel | opportunity |
|---|---|
| turnover | offensive possession |
| steal | defensive possession |
| offensive rebound | own missed field goal |
| defensive rebound | opponent missed field goal |

Nothing in the model separates a per-opportunity influence from a per-possession
own rate, and no channel in this family is measured on the other four at all.

### Adam's observation: this is the four factors

Adam, mid-run: *"It strikes me that we are reinventing the 'four factors'
framework from first principles."*

Correct, and worth recording because it was arrived at from the other end.
Oliver's four factors are shooting, turnovers, rebounding and free-throw rate;
§10 is the first, §11 is the second and third, and §11c below adds the fourth.
The per-opportunity denominators in the table above are the four factors' own
denominators, re-derived here from the requirement that an expectation must be
something the player cannot move by himself.

What is **not** the four factors: that framework decomposes a TEAM's outcome
into four accounting terms with fixed weights. It says nothing about which of
five men moved a factor, and nothing about a lineup that has never played. The
question here is who moves each factor *for his teammates* — the factors supply
the coordinates, not the answer.

### The estimator

Identical to §10b, so the channels are comparable with shooting. The
expectation a player cannot move is the sum of the five men's own rates:

    E = d * sum over q in the acting five of r_q

with `d` the opportunities on that possession. Subtracting each man's own rate
is the exact analogue of the shooter fixed effects that turned the raw shooting
on/off from personnel into signal: a lineup of five careless players is expected
to turn it over more and gets no credit for doing so. Every rate is
empirical-Bayes shrunk by its own exposure, the residual is demeaned by game so
opponent and game state go, and the on/off coefficient is shrunk again. At each
of 44 origins everything is refitted strictly before the origin.

**A defect of my own, found and fixed:** the first run asserted the residual
variances that drive the shrinkage, and the module's docstring claimed they had
been checked against the data. They had not — they were 0.75 to 0.97 times the
truth. `measured_variance` now measures each origin's variance from its own
prior residuals. The second run then divided by the TOTAL weight rather than the
unit count, which is right for turnovers and steals (`d = 1`) and about 2.3x too
small for the rebound channels. Both are CLAUDE.md rule 12 in a new costume: a
constant nobody audited.

### Result: three of the four forecast

    python -u -m experiments.channel_influence_run

| channel | forward slope | seasons + | unshrunk | spread |
|---|---|---|---|---|
| defensive_rebound | **1.210 ± 0.032** | 12/12 | 0.938 | 5.13 /100 opp |
| turnover | **0.592 ± 0.019** | 12/12 | 0.425 | 2.10 /100 opp |
| steal | **0.569 ± 0.111** | 12/12 | 0.129 | 0.19 /100 opp |
| offensive_rebound | −0.938 ± 0.419 | 3/12 | 0.094 | 1.04 /100 opp |

Slope 1.0 means the shrunk coefficient is correctly scaled out of sample; 0
means it forecasts nothing. Shrinkage is again worth more than the coefficient
(§10b), most extremely for steals, where the raw coefficient keeps 0.129 of its
scale and the shrunk one keeps 0.569.

### And the face lists say three of them are measuring the wrong thing

    defensive rebounding, most helpful:
      Robin Lopez, Brook Lopez, Ryan Hollins, Damjan Rudez, Luka Garza
    defensive rebounding, least helpful:
      Andre Drummond, Marcus Camby, Luka Doncic, Hassan Whiteside, Giannis

That is an inverted list of who rebounds, and `corr(own rate, coefficient)` is
**−0.527**. The cause is in the expectation: `E = d * sum of own rates` assumes
the five men's rates ADD, and rebounds do not — only one player can collect a
given miss. A lineup containing a dominant rebounder collects fewer than the sum
of its individual rates, and the estimator charges him the difference. **A
coefficient that is a linear function of a man's own rate is an accounting
correction to a mis-specified expectation. It can forecast perfectly and be no
evidence at all about his effect on the other four** — which is exactly how
defensive rebounding scores 1.210 with 12/12 seasons.

The same diagnostic across all four:

| channel | corr(own rate, coefficient) |
|---|---|
| defensive_rebound | −0.527 |
| turnover | −0.415 |
| offensive_rebound | −0.294 |
| **steal** | **+0.280** |

Steals are the only positive one, and displacement cannot produce a positive
sign: if I take the ball, you do not. A positive correlation is the signature of
genuine complementarity — pressure on the ball creating steals for someone else.
Its spread is also the smallest of the four, 0.19 steals per 100 possessions.

## 11b. The discriminator: orthogonalise against the man's own rate

    python -u -m experiments.channel_influence_orth

At every origin the coefficient is regressed on the player's own rate,
exposure-weighted, and the forward slope test is re-run on **the residual
alone** — the part of the coefficient that a man's own production does not
explain. This is the same move as the free-throw placebo in §10: strip what a
rival explanation can account for and see what survives.

| channel | own rate explains | full slope | ORTHOGONAL slope | seasons + |
|---|---|---|---|---|
| defensive_rebound | 40% | 1.210 | **0.908 ± 0.037** | 12/12 |
| turnover | 35% | 0.592 | **0.434 ± 0.024** | 12/12 |
| steal | 3% | 0.569 | **0.512 ± 0.100** | 12/12 |
| offensive_rebound | 20% | −0.938 | **1.031 ± 0.264** | 11/12 |

**All four forecast once the accounting is removed.** Offensive rebounding is
the informative case: as a whole it forecast *negatively* (3/12 seasons), and
the own-rate-orthogonal part forecasts at 1.03 with 11/12. The accounting
correction was not merely uninformative there, it was wrong-signed out of
sample, and it was hiding a real effect underneath.

The caveat, stated rather than buried: sub-additivity is only approximately
linear in the own rate, so **a residual slope above zero is an upper bound on
the influence, not a clean measurement of it.** The face lists agree with that
reading — cleaned up, they are:

- **turnover: face-valid.** Shai Gilgeous-Alexander −1.77 per 100 (Adam's own
  example, and the fifth-largest in the league), Chris Paul −1.69, Jokic −0.71,
  Draymond −0.53; the bottom is low-usage bigs and backups. Own rate explains
  35%, and what is left is the ball-handlers who keep their teammates out of
  trouble.
- **steal: face-valid and tiny.** Jae Crowder, Xavier Tillman, Al-Farouq Aminu,
  Boris Diaw, Payton Pritchard — versatile perimeter defenders. Spread 0.07 per
  100 after orthogonalisation. Josh Hart is +0.06, the right sign, near the top
  quartile, and nowhere near resolvable on its own.
- **defensive rebounding: still not face-valid at the extremes.** Steven Adams
  moves to +2.08 and Jokic to +1.14, which is progress, but the Lopez brothers
  still head the list. The linear correction has not removed the competition
  artifact.
- **offensive rebounding: not face-valid.** Steven Adams is −0.44, which
  contradicts the hypothesis that motivated the channel.

So the honest verdict is **one clean channel (turnovers), one clean but
negligible channel (steals), and two channels that forecast for reasons the
data cannot yet separate from rebound competition.** Fixing the rebound
channels needs a contested-rebound model — an expectation that knows only one of
five can collect — not a bigger fit.

### A finding about §6, not about rebounds

The §6 on-floor influence layer already carries a `turnover` count channel,
fitted on the POINT residual of the structural assembly. Compared with the
direct per-possession turnover coefficient measured here, at the same origin,
over 1,670 shared identities:

    corr = -0.003        sd 0.0074 (section 6)  vs  0.0078 (section 11)

**The same spread and no relationship at all.** The point residual is too noisy,
and its design too collinear, to identify a channel that is plainly identifiable
when measured on its own events. That is a general argument for measuring
mechanisms on their own outcome and pricing them afterwards — the §10 route —
rather than fitting them on points and hoping the channel decomposition is real.

## 11c. The fourth factor — free-throw rate

Adam's four-factors observation leaves one gap, so it is closed here. Free
throws MADE are shooting skill and are already the §10 placebo; **attempts** are
the factor. The shooter's name precedes the mark in the play-by-play
(`b. griffin makes free throw 1 of 2`), so this channel is parsed as a prefix;
`(drawn by ...)` cannot be used in its place because an OFFENSIVE foul names the
defender in that slot. Denominator: offensive possessions.

    python -u -m experiments.channel_influence_run
    python -u -m experiments.channel_influence_orth

The five-channel run reproduces the original four to six digits, which is the
regression check on the new prefix parse. Free-throw rate:

| | forward slope | seasons + | unshrunk | spread |
|---|---|---|---|---|
| full coefficient | **0.409 ± 0.008** | 12/12 | 0.346 | 6.84 FTA/100 |
| own-rate orthogonal | **0.271 ± 0.014** | 12/12 | — | 5.93 FTA/100 |

The own rate explains 30% of it, and the largest spread of any of the five
channels survives orthogonalisation. Taken at face value this is the biggest of
the four factors' influence terms.

**It should not be taken at face value.** The face list is end-of-bench players:

    gets teammates to the line: Mario West, Dwayne Jones, Bernard Robinson,
                                Jermaine Jackson, Darvin Ham, Othyus Jeffers
    fewest                    : Todd MacCulloch, Deandre Ayton, Ryan Nembhard

and on the FULL coefficient the bottom is Shaquille O'Neal (−11.36), Yao Ming,
Ilgauskas and MacCulloch — Hack-a-Shaq, which is a real effect on the wrong
player, since it is the OPPONENT choosing to foul him.

The obvious rival explanation is **garbage time**: deep-bench minutes
concentrate in blowouts, where the trailing team fouls intentionally, and
demeaning by game removes the game's mean but not the within-game concentration.
One diagnostic argues against the simplest version of it — the spread is flat
across exposure quintiles, so this is not small-sample noise that the shrinkage
failed to control:

| channel | sd of coefficient by exposure quintile, low to high | corr(log exposure, abs coefficient) |
|---|---|---|
| turnover | 0.66 0.71 0.70 0.61 0.68 | −0.042 |
| steal | 0.03 0.05 0.07 0.09 0.11 | **+0.476** |
| offensive_rebound | 0.36 0.41 0.42 0.46 0.48 | +0.115 |
| defensive_rebound | 1.85 1.84 1.78 1.76 1.71 | −0.044 |
| free_throw_attempt | 2.43 2.56 2.26 2.41 2.26 | −0.168 |

Steals are the one channel whose spread RISES with exposure, which is what real
signal looks like when shrinkage is working: the better-measured players keep
more of their coefficient. Free-throw rate does the opposite, weakly.

So free-throw rate is **recorded, not banked.** The named test that would settle
it is to demean by (game, score-margin bucket) or drop possessions inside
garbage time, and re-run — cheap, and not run here.

### Where the four factors stand

| factor | measured? | forecasts? | face-valid? | verdict |
|---|---|---|---|---|
| shooting (§10) | yes | 1.082 ± 0.084 | yes | keep, priced in §10c |
| turnovers | yes | 0.434 ± 0.024 orth | **yes** | keep — the clean one |
| rebounding, off | yes | 1.031 ± 0.264 orth | no | needs a contested model |
| rebounding, def | yes | 0.908 ± 0.037 orth | no | needs a contested model |
| free-throw rate | yes | 0.271 ± 0.014 orth | no | garbage-time confound open |

Two of the five are ready to price. Turnovers are the one the structural model
can absorb directly, because `turnover` is already a component of its usage
budget — §6's `shift_components` moves it while preserving the budget exactly —
and because §11b showed the point-residual fit is NOT already capturing it. That
is the next thing to build.

Sizing it honestly first, using the same arithmetic as §10c: the orthogonal
turnover coefficient has a spread of 0.72 turnovers per 100 possessions, and a
turnover costs roughly the value of a possession, about 1.1 points. So the term
is worth on the order of **0.8 pts/100 of spread** — comparable to shot quality
(0.765) and about a quarter of the opponent adjustment. By §10c's calibration
of what this benchmark can resolve, that means it will forecast at the channel
level and will not be establishable at the point level. That is the expected
outcome, not a reason to skip it.

## 11d. Turnover influence priced in points: it does NOT convert

    python -u -m experiments.turnover_points

§11b left turnovers as the one clean channel, and `turnover` is one of the four
components of the structural usage budget, so the model has a place to put it.
This is not a bonus bolted on the side: `shift_components` moves the turnover
component and renormalises the freed usage into two-point attempts, three-point
attempts and free throws in the proportions the allocation already chose. A
lineup that turns it over less **gets the possession back** and spends it the
way that lineup spends possessions. The parent reproduces to 8.5e-14 and no cell
was ever clipped.

**The forward slope is the calibration factor, and I priced it wrong first.**
§11b measured the channel slope at 0.434 — a slope below 1 says the coefficient
is that many times too large out of sample — and the point calibration cannot
repair it, because `b` scales the whole score and not one term inside it. Priced
at full scale the term moved cells by 2.0 pts/100 and MAE by +0.0089. Scaling by
a slope fitted on strictly earlier origins (`running_slopes`, which never sees
its own origin; the estimate lands at 0.431 against §11b's 0.434, measured
independently) halves the term to 0.81 pts/100:

| arm | MAE | vs parent | RMSE | r² | novel MAE |
|---|---|---|---|---|---|
| parent | 8.1440 | — | 10.9214 | 0.10733 | 8.8903 |
| turnover, full scale | 8.1506 | +0.0089 ± 0.0258 | 10.9320 | 0.10561 | 8.8795 |
| **turnover, slope-scaled** | 8.1446 | **+0.0025 ± 0.0150** | 10.9198 | 0.10759 | 8.8823 |
| turnover, not orthogonalised | 8.1625 | +0.0201 ± 0.0258 | 10.9413 | 0.10408 | 8.9245 |
| placebo (permuted identities) | 8.1674 | +0.0186 ± 0.0290 | 10.9621 | 0.10068 | 8.9239 |
| + shot quality | 8.1394 | −0.0015 ± 0.0218 | 10.9097 | 0.10925 | 8.8759 |

**Two pre-registered predictions hold.** The orthogonal coefficient beats the
un-orthogonalised one on every metric, which is §11b's finding reappearing in
points; and both beat the permuted-identity placebo, so the machinery is not
manufacturing the result. That validates the §11b method independently.

**And the term still does not convert.** The parent is bit-identical across this
run and §10c, so the two are directly comparable, and shot quality alone scores
8.1321 while turnover-plus-shot-quality scores 8.1394 — adding turnovers makes
shot quality WORSE, on MAE, RMSE and r² alike.

### Why: the incremental point content is zero, and it is not a scaling problem

Regressing the parent's out-of-sample residual on each term:

| term | slope of the parent residual |
|---|---|
| turnover, as priced | −0.161 |
| turnover, orthogonal to the parent score | **−0.028** |
| turnover, orthogonal to parent and shot quality | −0.336 |
| shot quality, as priced | +0.531 |
| shot quality, orthogonal to the parent score | **+0.637** |

A correctly scaled term reads +1.0. Turnover reads **−0.028 once what the parent
already prices is removed** — not wrong-signed, not mis-scaled, simply empty.
Season by season the slope is **5/12 positive** and ranges from +1.72 to −2.28,
which is what noise looks like. Shot quality on the identical test reads +0.637
and is the reason it was kept.

The lineup sum of turnover coefficients correlates +0.345 with the parent's own
score and +0.435 with the shot-quality term, so the information is largely
already in the model by another route. **The player-level ATTRIBUTION is new —
which of the five deserves credit — but the lineup TOTAL is not, and points only
see the total.** That is the distinction the channel-level forecast cannot make
and the point benchmark can.

### The verdict, against Adam's own bar

Adam's rule is that a principled hypothesis moving the right way with a clean
placebo is worth keeping even below the significance bar, *when it moves every
metric the same way*. This one does not: +0.0025 MAE against −0.0016 RMSE and
+0.00026 r², 5/11 seasons, and it degrades the one term already kept. So
**turnover influence is recorded and not shipped.** Its channel-level forecast
stands — 0.434 ± 0.024 over 3.0M possessions, 12/12 seasons — and remains the
right basis for an explanation in the tool ("this five protects the ball"), just
not for a change to the number.

The general lesson is the sharper output of this section, and it is the mirror
of §11b's: **a mechanism can forecast on its own events and still carry no
incremental points, because the model may already price the lineup total through
another route.** §11b said do not trust a channel fit on the point residual;
§11d says do not assume a channel that forecasts will pay in points. Both are
arguments for measuring on the channel AND pricing on points, and believing
neither one alone.

## 12. Location-specific conversion — the model's predictor is worse than no player at all

§8j found the defect: `self_2p` is one number, so the model's implied per-bucket
curve is FLAT — it asserts a player converts a rim attempt and a long two at the
same personal rate. `experiments/location_skill.py` measures the replacement and
`location_skill_run.py` tests it forward on 44 origins, everything refitted
strictly before each one, with the SAME 730-day recency and effective-exposure
correction the box-score profile uses (`asof_state.decay_weights`), so the
comparison is one change wide.

Four nested predictors of a held-out field-goal attempt. Brier, lower better:

| predictor | Brier | vs current | seasons better |
|---|---|---|---|
| **current** — the player's scalar rate for that shot type | 0.241412 | — | — |
| **league** — the league's rate at that BUCKET, no player at all | 0.234347 | −0.007065 ± 0.000172 | 12/12 |
| **offset** — league at the bucket + one skill offset per player | 0.233400 | −0.008012 ± 0.000164 | 12/12 |
| **bucket** — the player's own rate AT that bucket | 0.233077 | −0.008335 ± 0.000173 | 12/12 |

**The model's current per-attempt predictor is worse than ignoring the player
entirely and using the league's rate for that location.** Knowing where a shot
came from is worth more than knowing who took it, and the model knows only who.

The player-by-location interaction is real on top of the offset —
**−0.000323 ± 0.000020, 12/12 seasons** — but it is an order of magnitude
smaller than simply knowing the location.

## 12b. Priced: it works, and it is orthogonal to shot quality

    python -u -m experiments.location_points

The model's own identity makes this a one-line replacement. Its two-point score
is `Σ_b 2PA_b (value_b − 2 pct_b) + 2 Σ_b 2PA_b · self_2p`, so swapping the
scalar for a per-bucket curve changes only the making term. **It is exactly
nested**: feed the profile's own scalar into all six buckets and the delta is
zero, because `2 Σ_b 2PA_b (s − pct_b)` collapses to the model's own
`2 · 2PA · (s − mix @ pct)`. That identity is asserted at every origin, not
assumed — observed worst case **1.4e-14**, alongside the parent gate at 1.1e-13.
Coverage is 94.3% of lineup slots; below `MIN_EFFECTIVE_ATTEMPTS` a slot keeps
the parent's own scalar, so a thin player is scored exactly as before.

### Two defects of my own, both found by a control that refused to sit still

**First, the source and the recency were bundled.** My first rates were flat
all-history while the profile decays shooting at a 730-day half-life. The
`pbp_scalar` control — the same scalar skill, sourced from the play-by-play —
read +0.0252 MAE with 3/11 seasons, which is a source effect masquerading as a
location effect. Matching the recency moved that control to **−0.0010 ± 0.0017,
8/11**, i.e. to nothing, which is exactly what a control that isolates the
change is supposed to do. Everything below it is now location.

**Second, the league anchor was the wrong league.** I built each player's curve
around a league vector fitted here, while the making term subtracts the model's
own `environment['location_pct']`. The difference left a constant
`2 · 2PA · (league_mine − pct) @ mix` in every score — a level shift, which
hides inside the calibration's intercept and surfaces as BIAS rather than error:
parent −0.680 against offset −0.830. Rebasing every candidate on the model's own
curve fixed it, and the arm now has **better bias than the parent** (−0.495).

### Results, 5,607 cells / 726,364 possessions, 2016+

| arm | MAE | RMSE | r² | bias | novel MAE |
|---|---|---|---|---|---|
| parent | 8.1440 | 10.9214 | 0.10733 | −0.680 | 8.8903 |
| pbp_scalar (the source control) | 8.1427 | 10.9208 | 0.10744 | −0.684 | 8.8911 |
| **pbp_offset** | 8.1428 | **10.9120** | **0.10888** | **−0.495** | **8.8812** |
| pbp_bucket | 8.1492 | 10.9175 | 0.10797 | −0.515 | 8.8894 |
| placebo (permuted identities) | 8.3204 | 11.0970 | 0.07840 | −1.001 | 9.0399 |
| **+ shot quality** | **8.1374** | **10.9016** | **0.11056** | −0.481 | **8.8722** |
| corrected additive | 8.0920 | 10.8410 | 0.12043 | −0.548 | 8.9039 |

### The decisive test

Regressing the parent's out-of-sample residual on each term, where 1.0 is
correctly scaled — the test that killed turnover influence at −0.028 and kept
shot quality at +0.637:

| term | sd (pts/100) | as priced | orthogonal to parent | orth. to parent AND shot quality | seasons + |
|---|---:|---:|---:|---:|---|
| **pbp_offset** | 0.614 | +0.686 | **+0.635** | **+0.641** | 9/12 |
| pbp_bucket | 0.715 | +0.536 | +0.449 | +0.454 | 9/12 |
| placebo | 3.141 | +0.064 | **+0.004** | +0.031 | 7/12 |
| shot quality (reference) | 0.777 | +0.531 | +0.637 | — | — |

and the number that matters most for whether it ADDS:

    corr(location term, shot-quality term) = -0.030
    corr(location term, parent score)      = -0.112

**Essentially orthogonal to both.** Turnover influence failed §11d partly
because it correlated +0.435 with shot quality and +0.345 with the parent — it
was re-pricing what was already priced. This is new information, which is why
`combined` improves every metric at once and reaches the best structural numbers
on record: MAE 8.1374, RMSE 10.9016, r² 0.11056.

### Two findings worth keeping beyond the arm

**The player-by-location interaction does not survive aggregation.** `bucket`
beats `offset` at the attempt level (Brier −0.000323, 12/12) and LOSES to it at
the lineup level (+0.449 against +0.635). Averaged over five players and
thousands of possessions, "who is differentially good at the rim" is noise;
"where this five shoots and how good they are overall" is signal. Ship `offset`.

**Per-bucket conversion is necessary but not sufficient for a lineup-dependent
location effect.** In the current allocation a player's mix is his own history
and the lineup never changes it, so `Σ_b 2PA_b · pct_b` varies across lineups
only through WHO is in them, not through what the lineup does to them. Per-bucket
conversion fixes the pricing of a player; it does not yet let a lineup move
anybody's shots. **That is what makes §8i's lineup-dependent mix worth building
NOW and not before** — on a flat curve it moved a quantity the model could not
feel (§8j), and on this curve it can. The two must ship together.

## 13. Teammates really do move where you shoot from

    python -u -m experiments.mix_influence_run

§8j killed this question on the old model and §12b revived it. The estimator is
**§10's, not §11's**, and the difference is the whole lesson of §11b: the unit
is one ATTEMPT with a known shooter, so

    residual_b = 1[this attempt came from bucket b] - (the shooter's own share of b)

Every attempt is compared to the man who took it — the shooter fixed effect that
made §10 work — and a player's influence is measured over his **teammates'
attempts only**, his own excluded outright. There is therefore no own-rate
component to strip, and no §11b orthogonalisation is needed or possible.

**A parameterisation error, caught by a bucket that would not behave.** My first
run normalised the mix over all six buckets, and the corner three came back at
−0.077 with 0/12 seasons while everything else forecast. The model does not
parameterise it that way: `two_mix` is a simplex over the four two-point buckets,
`three_mix` over the two three-point buckets, and the 2-versus-3 split belongs to
`r3pa` — which §8i priced at 0.0137 points, i.e. nothing. Pooling the six let "he
takes more threes" leak into "he shoots from different places among his twos".
Measuring each side separately, as the model does:

| bucket | forward slope | seasons + | spread of the shift |
|---|---|---|---|
| rim | 0.793 ± 0.033 | 12/12 | **4.27 pp** |
| mid | 0.836 ± 0.051 | 12/12 | 1.68 pp |
| paint | 0.647 ± 0.070 | 12/12 | 1.62 pp |
| long mid | 0.609 ± 0.045 | 12/12 | 2.67 pp |
| corner three / above break | 0.390 ± 0.087 | 12/12 | 0.85 pp |

**All six forecast, 12/12 seasons, on 2.66M held-out attempts.** One standard
deviation of teammates moves a player's rim share by **4.3 percentage points**.
This is a large, well-measured effect and it is the single cleanest influence
measurement in the workstream, because the design removes the confound instead
of correcting for it afterwards.

## 13b. Priced — and the pair really does have to ship together

    python -u -m experiments.mix_points

The experiment is built to test §12b's claim rather than repeat it. `flat_mix`
applies the **identical** mix shift to the parent's flat conversion curve;
`location_mix` applies it to the per-bucket curve. Same coefficients, same
lineups, one difference.

    flat_mix      moves the score 0.069 pts/100
    location_mix  moves the score 1.230 pts/100

**Eighteen times more.** §8j's claim — that the mix is cancelled out of the
score on a flat curve — is now demonstrated on the same shift that the
per-bucket curve prices at 1.2 points, rather than argued from a decomposition.
The gate that a flat curve with no shift reproduces the parent holds at 1.9e-14.

### But the mix does not convert at face value

| arm | MAE | RMSE | r² | bias | novel |
|---|---|---|---|---|---|
| parent | 8.1440 | 10.9214 | 0.10733 | −0.680 | 8.8903 |
| flat_mix | 8.1443 | 10.9210 | 0.10741 | −0.661 | 8.8907 |
| **location** (§12b) | **8.1428** | **10.9120** | **0.10888** | −0.495 | 8.8812 |
| location_mix | 8.1645 | 10.9121 | 0.10886 | **−0.428** | 8.8807 |
| placebo (permuted mix) | 8.1514 | 10.9295 | 0.10602 | −0.516 | 8.9025 |
| combined + shot quality | 8.1577 | 10.9046 | 0.11008 | −0.408 | 8.8745 |

Isolating the mix term on top of `location`, and regressing the parent's
out-of-sample residual on it:

| term | sd | slope, orthogonal to parent AND location | seasons + |
|---|---:|---:|---|
| **mix shift alone** | 1.077 | **+0.185** | 8/12 |
| placebo mix alone | 0.998 | −0.086 | — |

Real — it beats its placebo cleanly, and the sign is right in 8 of 12 seasons —
but **roughly five times over-scaled**. The same pattern as §11d: a channel that
forecasts strongly on its own events converts weakly into points.

The likely reason is basketball, not arithmetic. The arm gives a player pushed
to the rim by his teammates the rim conversion he earns on his OWN rim attempts,
and a shot created for you is not the shot you create for yourself. Pricing that
properly needs the assisted/unassisted split the profile already carries
(`assisted`), which is the next thing to try rather than a bigger fit.

### Slope-scaling it: helps the metric, does not fix the term

My own backlog says the first move for any term whose forward slope is below 1
is to scale it prior-only, so I did (`prior_scale`, using only earlier origins).
It recovers most of the loss — MAE +0.0191 becomes **+0.0064 ± 0.0134**, RMSE
10.9106 and r² 0.10911 both beat the `location` arm alone, and with shot quality
the combination sets the best structural RMSE and r² on record:

| arm | MAE | RMSE | r² | novel |
|---|---|---|---|---|
| shot quality alone (§10c) | **8.1321** | 10.9048 | 0.11005 | 8.8745 |
| location + shot quality (§12b) | 8.1374 | 10.9016 | 0.11056 | 8.8722 |
| location alone | 8.1428 | 10.9120 | 0.10888 | 8.8812 |
| **location + scaled mix + shot quality** | 8.1423 | **10.8986** | **0.11106** | **8.8719** |

**But the scaling does not calibrate the term, it only shrinks it.** If the
prior scale were tracking the true slope, the scaled term would price near 1.0;
instead it prices at **+0.120 with 7/12 seasons**, below the unscaled +0.185 with
8/12. The prior estimate ranges from **−0.277 to +0.580** across origins — it is
too unstable to be a calibration. What the scaling really does is use less of a
term that is over-weighted, which improves the metric without earning it.

### Verdict

**Ship `location` (§12b); hold `location_mix`, scaled or not.** No arm dominates
— shot quality alone has the best MAE, the location family the best RMSE, r² and
novel MAE — and that spread is itself the §10c point: this population resolves
about 0.04 MAE and these differences are 0.005. Per-bucket conversion improves
RMSE, r², correlation, bias and novel MAE and prices at slope 0.635. The mix
shift on top is a real, well-measured, placebo-clean mechanism that currently
costs 0.019 MAE because it enters at five times its earned weight. It should
return either slope-scaled — the §11d method, `running_slopes`, already exists —
or conditioned on how the shot was created.

## 14. The mixing rule itself: measured, and it is nearly right

    python -u -m experiments.allocation_rule

Adam asked whether there is a more elegant mechanism for learning profiles and
mixing them. Before answering by taste, the current mixing rule is worth
measuring, because it makes a sharp assertion. The whole of it is one scalar:

    player[:, :, SCALED] *= budget / total_usage        (asof_point_allocation.py:127)

with the category factors also per-lineup scalars. So the model asserts

    share of q in lineup L  =  usage_q / sum over p in L of usage_p

**exactly.** A lineup may rescale the pie and never redistribute it. Jokic
beside four non-creators gets precisely his usual share. That is the most
obvious thing about a basketball lineup and the model cannot express it.

Measured on 6.8M usage events (field goals, 0.44 free throws, turnovers) over
3,266 five-man units of at least 200 possessions, with each player's marginal
rate computed **leave-one-unit-out** so the unit being scored never contributes
to the rate that predicts it:

    the model asserts slope 1.000; observed 1.0574

| slice | rows | slope | rmse of the share |
|---|---|---|---|
| 200–500 possessions | 12,385 | 1.088 | 0.035 |
| ≥500 possessions | 3,945 | 1.024 | 0.028 |

| predicted share | observed | miss |
|---|---|---|
| ≤ .15 | .1307 | −0.0020 |
| .15–.18 | .1636 | −0.0022 |
| .18–.21 | .1931 | −0.0021 |
| .21–.25 | .2301 | +0.0019 |
| **> .25** | **.2788** | **+0.0054** |

**Shares AMPLIFY: the rich get richer.** A high-usage player takes about half a
percentage point more of his lineup's usage than his marginal rate implies, and
everyone below the mid-band gives up about two tenths. Errors-in-variables in
the leave-one-out rate attenuates the estimate, so 1.057 is a lower bound.

**But the rule is right to within about six percent**, which is the finding that
matters for architecture. The proportional allocator is not the weak point of
this model; it is a good approximation to a mild amplification. The natural
elegant replacement is a softmax over the five with a learned temperature, which
contains proportional allocation as the temperature-1 case and would recover
that six percent — worth doing for coherence and for the trade counterfactual
("swap Harden for Kyrie"), not worth doing for accuracy.

Note what it does NOT change: five identical players still split the ball five
ways under any symmetric rule, so this is not a 5-Shaq lever.

## 14b. The channels share ONE player factor — the case for a joint model

    python -u -m experiments.channel_factor

The workstream has now measured four per-player quantities on four separate
high-count event streams. Their correlations across 1,432 players with more than
300 effective attempts at 2026q4 (the `mix_rim`/`mix_longmid` pair is arithmetic
— two components of a zero-sum simplex — and is excluded):

| | convert_2p | mix_rim | shot_quality | turnover_infl |
|---|---:|---:|---:|---:|
| convert_2p | 1.000 | −0.001 | +0.060 | −0.179 |
| convert_3p | +0.201 | +0.087 | −0.006 | −0.108 |
| mix_rim | −0.001 | 1.000 | **+0.330** | **−0.366** |
| shot_quality | +0.060 | +0.330 | 1.000 | **−0.337** |
| turnover_infl | −0.179 | −0.366 | −0.337 | 1.000 |

**Two clean blocks.** The three INFLUENCE channels — pulling teammates' shots to
the rim, raising their percentage, lowering their turnovers — correlate with each
other at 0.33 to 0.37 with the signs basketball would predict. They are three
noisy views of one latent thing, which one could fairly call creation or gravity.
The two CONVERSION channels correlate with each other (+0.201) and with the
influence block barely at all (|r| ≤ 0.18): how well you shoot and how much you
help others are separate dimensions.

**This is the first positive evidence in this project for a latent-factor
structure, and it is a different object from every latent structure the record
has closed.** Those nulls — the profile bilinear at every width, 128 random
features, a jointly-fitted quadratic prior, a 76k-parameter transformer beaten by
55 parameters, "pair effects are not low-rank, rank 256 needed" — are all about
`f(profile_i, profile_j)` predicting a PAIR effect from a 1e-4 points residual.
This is a per-player latent shared across channels, each identified on millions
of events. Nothing on the record speaks against it.

**Why it should pay.** Reliability, not signal, is this project's binding
constraint: `lineup_scoreboard` puts 38% of the rating spread down to estimation
noise, and §10 measured shot quality's own split-half reliability at 0.397, so
"most of the spread is noise and only extremes resolve". Three channels
correlated at ~0.35 can borrow strength from each other. A shared factor is the
principled way to raise the reliability of all three at once, and raising
reliability is worth more here than finding another mechanism.

## 14c. The channels DO predict each other — asymmetrically, which says what to build

    python -u -m experiments.factor_test

§14b's correlations are suggestive and not sufficient: correlated ESTIMATES can
come from correlated NOISE, and shrinking two channels toward shared centres
would manufacture some of it. The decisive test is out of sample and needs no
factor model. For each channel, regress its held-out outcome on its OWN prior
coefficient and the OTHER channels' prior coefficients together, with a
permuted-identity placebo carried alongside — same distribution, pairing
destroyed. All predictors standardised; season-level refits give the errors,
because 3M rows clustered by player and origin would make a pooled SEM a fiction.

**Turnovers** (3,006,165 possessions), own weight alone 0.0075:

| predictor | weight | sem | seasons same sign |
|---|---:|---:|---|
| own (turnover coefficient) | 0.0051 | — | — |
| **rim-share influence** | **−0.0047** | 0.0007 | **12/12** |
| shot quality | −0.0018 | 0.0004 | 9/12 |
| **placebo** | **+0.0002** | 0.0003 | 7/12 |

**Rim share** (1,695,171 attempts), own weight alone 0.0339:

| predictor | weight | sem | seasons same sign |
|---|---:|---:|---|
| own (mix coefficient) | 0.0353 | — | — |
| turnover influence | +0.0032 | 0.0014 | 5/12 |
| shot quality | −0.0010 | 0.0012 | 8/12 |
| placebo | −0.0010 | 0.0010 | 8/12 |

**The information flows one way.** For turnovers the rim-share coefficient is
worth **92% as much as the turnover coefficient itself**, 12/12 seasons, against
a placebo that reads zero — and adding the other channels drops turnover's own
weight from 0.0075 to 0.0051, so **a third of what the turnover coefficient was
carrying is information the other channels also have.** For rim share, nothing
helps: the real predictors are indistinguishable from the placebo (0.0032 ±
0.0014 at 5/12, against placebo −0.0010 ± 0.0010 at 8/12).

That asymmetry is exactly what the measurement quality predicts. Rim share is
estimated on 1.7M attempts with a shooter fixed effect that removes the confound
by construction (§13); turnover influence is estimated on a possession-level
residual with a known accounting problem (§11b). **The well-measured channel
lends to the badly-measured one, and not the reverse.**

### What that means for the architecture

A shared per-player factor is worth building, and it is worth building for a
specific and limited reason: **it raises the reliability of the noisy channels by
borrowing from the clean ones.** It will do nothing for rim share or shot
quality, which already measure what they measure. It should do a great deal for
turnovers — and by extension for steals and the two rebound channels, which §11
left forecasting but uninterpretable.

That also gives §11d a second chance. Turnover influence failed to convert into
points partly because it was noisy (slope +0.185 at the channel level, −0.028 in
points). A factor-improved turnover coefficient is the version worth re-pricing.

And it says what NOT to do: do not put the well-measured channels through a
shared latent and hope for a lift. Measure each mechanism on its own events
where you can, and pool only where the events are thin.

## 15. The shared factor: it works, and it mostly launders shot quality

    python -u -m experiments.channel_factor_run
    python -u -m experiments.turnover_points

§14c said the well-measured channels lend to the thin ones. This builds the
lender: one factor across six per-player coefficients — two **anchors**
(rim-share influence, shot quality) and the four **thin** channels of §11 — with

    theta[p, c] = loading[c] * factor[p] + residual[p, c]

and the sampling variance recovered by **inverting each channel's own
shrinkage** rather than asserted. The estimator is validated on a synthetic
null: loadings recovered to within 6%, factor score correlating 0.94 with truth.

**A defect worth recording, because its symptom did not name its cause.** My
first inversion assumed the shrinkage centred on zero. `channel_influence.shrink`
centres on the exposure-weighted mean, so every player's recovered keep factor
was wrong, the sampling variance with it, and each channel's own remainder was
mis-shrunk — the visible symptom being a "factor plus remainder" arm that
collapsed *exactly* onto the pure factor, `both == factor` to the digit. Nothing
about that says "wrong centre". Two intermediate specifications gave three
different orderings of the four channels before the exact inversion settled it.

### At the channel level: one winner, two losers, one coin flip

| channel | r² own | r² factor+remainder | slope own → both |
|---|---:|---:|---|
| **turnover** | 471 | **515** | 0.434 → 1.91 |
| defensive_rebound | 7,256 | 6,120 | 0.908 → 1.24 |
| offensive_rebound | 771 | 139 | 1.031 → −1.35 |
| steal | 12.7 | 6.8 | 0.512 → 6.34 |

(r² × 1e6 on held-out events.) Turnover improves under **every** sampling
specification I tried (+9% and +14%); both rebound channels get worse under all
of them; steals flip sign between specifications and should be called unstable
rather than either way. The rebound result is informative rather than
disappointing: offensive-rebound influence is not "gravity", and forcing it onto
a shared factor destroys a coefficient that forecast at 1.03 on its own.

### In points, against the parent, it converts — the first time turnovers have

| arm | MAE | vs parent | RMSE | r² | novel |
|---|---|---|---|---|---|
| parent | 8.1440 | — | 10.9214 | 0.10733 | 8.8903 |
| turnover, raw (§11d) | 8.1506 | +0.0089 | 10.9320 | 0.10561 | 8.8795 |
| turnover, slope-scaled (§11d) | 8.1446 | +0.0025 | 10.9198 | 0.10759 | 8.8823 |
| **turnover, factor-improved** | **8.1406** | **−0.0045 ± 0.0056** | **10.9130** | **0.10871** | **8.8717** |
| placebo | 8.1674 | +0.0186 | 10.9621 | 0.10068 | 8.9239 |

Every metric moves the right way, 7/11 seasons, against a placebo that is the
worst arm in the table. §11d's channel had failed at −0.028; this one clears
Adam's keep-bar against the parent.

### And then the comparison that matters

**Borrowed strength must be judged against the lender, not against the
parent.** The factor is built from anchors that include shot quality, so the
improved turnover coefficient inherits shot quality's information:

    corr(factor turnover term, shot-quality term) = +0.518
    slope orthogonal to the parent                = +0.292
    slope orthogonal to the parent AND shot quality = -0.239

| arm | MAE | RMSE | r² | novel |
|---|---|---|---|---|
| shot quality alone | **8.1321** | 10.9048 | 0.11006 | 8.8744 |
| + factor-improved turnover | 8.1348 | **10.9027** | **0.11040** | **8.8641** |

Against shot quality — which is already in hand, cheaper, and better understood
— the factor turnover adds only novel MAE and r², costs pooled MAE, and prices
NEGATIVE once shot quality is controlled. **Most of what looked like rescuing
the turnover channel is shot quality wearing a turnover hat.**

### Verdict, and the rule it earns

The factor is real and it is not free information. Keep it for one narrow
purpose — it is the only thing that has ever made the turnover channel behave,
and the novel-lineup gain (8.8641, the best in this workstream) is where the
northstar looks. Do NOT report it against the parent, which flatters it by 0.007
MAE, and do not extend it to the rebound channels, which it damages.

**The rule, which is this session's third variant of the same trap:** §11d
warned that a channel forecasting on its own events need not pay in points;
§12b warned to check a new term's correlation with the terms already kept; this
adds that **a coefficient improved by borrowing must be scored against what it
borrowed from.** All three are the same discipline — a new number is only worth
what it adds to the numbers you already have, and the comparison must be made
against those, never against a stripped-down parent.

## 16. Everything that survived, scored together

    python -u -m experiments.assembled

Four mechanisms earned a place in this workstream and none had ever been scored
beside the others. They are applied in the order the accounting requires: the
turnover shift moves the usage budget, so it changes the ALLOCATION and goes
first through `shift_components`; everything else is a making-term or mix change
on whatever allocation results. The gate that a flat conversion curve with no
shift reproduces the parent holds at 1e-14.

| arm | MAE | RMSE | r² | **novel MAE** | novel r² |
|---|---|---|---|---|---|
| parent | 8.1440 | 10.9214 | 0.10733 | 8.8903 | 0.10132 |
| location (§12b) | 8.1428 | 10.9120 | 0.10888 | 8.8812 | 0.10342 |
| shot quality (§10c) | **8.1321** | 10.9048 | 0.11005 | 8.8745 | 0.10311 |
| turnover, factor (§15) | 8.1406 | 10.9130 | 0.10871 | 8.8717 | 0.10338 |
| location + mix (§13b) | 8.1497 | 10.9086 | 0.10942 | 8.8772 | 0.10476 |
| all four | 8.1517 | 10.9024 | 0.11044 | 8.8678 | 0.10604 |
| **best three (no mix)** | 8.1386 | **10.8965** | **0.11140** | **8.8612** | **0.10618** |
| corrected additive | **8.0920** | **10.8410** | **0.12043** | 8.9039 | 0.10035 |

**Dropping the mix improves everything**, which is §13b's hold decision
confirmed on a fourth independent scoring: `all` is worse than `best_three` on
MAE, RMSE, r² and novel alike.

### Do the pieces overlap?

    location  shot_q  turnover   mix
    location     1.000  -0.030     0.120  0.845
    shot_q      -0.030   1.000     0.518  0.213
    turnover     0.120   0.518     1.000  0.568
    mix          0.845   0.213     0.568  1.000

(The mix row is definitional — the `mix` arm contains `location` underneath it,
because §13b showed the mix cannot be felt without it. Read the other cells.)

**Location and shot quality are orthogonal (−0.030) and genuinely add.** Turnover
overlaps shot quality at 0.518, which is §15's finding reappearing: the
factor-improved turnover coefficient is substantially shot quality re-expressed,
so its marginal contribution is small even though it helps on its own.

### What it is worth, stated honestly

Season-paired, 11 seasons:

| comparison | slice | difference | seasons better |
|---|---|---|---|
| best three − parent | novel | **−0.0298 ± 0.0194** | **9/11** |
| best three − parent | all | −0.0043 ± 0.0247 | 6/11 |
| best three − additive | novel | −0.0445 ± 0.0736 | 6/11 |
| best three − additive | all | +0.0423 ± 0.0334 | 3/11 |

The solid result is the first row: **on novel lineups the assembled arm improves
its own parent by 0.030 with 9 of 11 seasons agreeing**, which is the slice the
northstar cares about most and the only comparison here whose season count is
convincing. Its RMSE and r² improve on every slice.

**The additive comparison is NOT established either way.** The structural family
already held a small novel edge (parent 8.8903 against additive 8.9039) and this
widens it to 0.045 — but at ±0.074 with 6/11 seasons, that is a point estimate
and nothing more. On the pooled set the additive remains ahead by 0.042 ± 0.033.
Nothing here overturns `MATCHED_BENCHMARK.md`; it moves the structural arm
toward the additive on the pooled set and further ahead on novel, both within
the noise the population allows.

### The state of the structural model, after this workstream

Best pooled MAE is still **shot quality alone** at 8.1321. Best RMSE, r² and
novel MAE are **best_three** at 10.8965 / 0.11140 / 8.8612. No single arm
dominates, and the spread between them (0.007 MAE) is a fifth of what §10c
showed this population can resolve. That is the honest ceiling on what any of
today's mechanisms can be shown to be worth here.

## 17. Not in scope

No scraper, no database write, no cache rebuild, no edit to any completed run
directory, no scorer or page promotion, no known-pair chemistry, and no change
to `MODEL_FEEDBACK_FROM_CLAUDE.md`. The frozen benchmark stays frozen: new work
gets a new prefix.

## 18. Reproduce the reconnaissance and the screen

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_influence_screen --recon
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.onfloor_influence_screen --screen
```

`experiments/onfloor_influence_screen.py` regenerates every number in §3 and §4
in about a minute. It reads only `experiments/cache/game_player_stats.pkl`, the
completed centered-run cells, and two read-only `select`s against `nba.games`
and `nba.players`; it writes only its own `experiments/cache/onfloor_screen_*`
prefix. It fits nothing. The estimator of §5 will land in a separate module with
tests.

## 19. Dated correction pointer — 2026-09-09

Do not use §13–§16 as the current decision record without the bounded repair in
[`reports/influence_repair_2026_09_09.md`](../../reports/influence_repair_2026_09_09.md).
The original results above are preserved as run history. The repair found that
the mix estimator counted a player's own attempts in his off sample, its
shrinkage omitted off-sample variance, the assembled point arm borrowed
turnover's scale for mix, and the factor inherited the affected rim-mix input.

On the clean 48-origin rerun, corrected mix still forecasts its shot-location
channel but does not add established point value. The refreshed factor improves
the turnover channel but not the preferred point candidate. The current
structural research candidate is location+shooting (MAE 8.1312, RMSE 10.8964,
r² .11142); corrected additive remains the pooled predictive baseline (8.0920,
10.8410, .12043). No scorer/page promotion followed. The complete replacement
artifact is `experiments/cache/influence_repair_2026_09_09_v2/`.
