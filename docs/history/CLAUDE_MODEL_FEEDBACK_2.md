# Review of the joint capability model (v2 core run)

Prepared by Claude Opus 5 on 2026-09-09 at Adam's request, for Sol and Codex.

**Status: read-only review of saved artifacts. No fit, refit, or run directory
was created; nothing in `experiments/cache/joint_capability_2026_09_09_v2/` was
touched, and no repair below has been attempted or verified by running it.**
Sol owns implementation of `JOINT_CAPABILITY_MODEL_PLAN.md` §0; this document is
a handoff, not a result of my own.

Every number traces to a saved file, named at the point of use:
`reports/metrics.csv`, `development/selected.csv`, `development/grid.csv`,
`logs/core.log`, `logs/develop.log`, `manifest.json`, and the per-origin
`cells.csv.gz` / `calibration.json`. Derived quantities (debiased metrics,
season-paired contrasts, native correlations) were recomputed from
`origins/*/*/cells.csv.gz`; the arithmetic is stated so it can be reproduced.

---

## 0. Summary

The architecture is the right shape for the northstar and produces the best
novel-lineup numbers on record here. The comparison that is supposed to prove it
is not yet identified, because the control arm was regularized 100x harder than
the candidate and never trained at all.

Three sentences, if that is all anyone reads:

1. **H0 selects epoch 1 in 48/48 origins.** The control is frozen at
   initialization while H3 trains 5.6 epochs, because one lambda multiplies the
   shared decoder penalty and H0's lambda was set by a tie-break on 3e-5 of noise.
   Every H-minus-H0 contrast conflates learned structure with decoder freedom.
2. **Debias each arm and the MAE ordering disappears** (8.1584 / 8.1596 / 8.1607
   / 8.1516). RMSE and native correlation survive, so there is real
   discrimination in H3 — but the headline MAE table mostly reports which arm was
   allowed to move its intercept.
3. **H3's novel-off5 r² of .10770 and correlation of .33057 are the best this
   project has measured**, from a model sitting ~2% off its initialization. That
   is a floor, not a ceiling, and it is the slice the northstar says matters.

Do not build any §8 extension before §5's Tier 1 and Tier 2 are done.

---

## 1. What the run says

Run state (`manifest.json`): `core_complete`, 192/192 arm-origins, 384 fits,
3,076.9 s of fitting, 58.3 s preflight, cpu, torch 2.10.0, numpy 2.3.4,
git HEAD `e68c53a`. Roughly one wall-clock hour against the plan's 12-hour
ceiling, and 384 of the 600 permitted fit invocations.

### 1.1 Pooled primary cohort

5,607 cells / 726,364 possessions, 2016-2026. `reports/metrics.csv` for the first
four numeric columns; "MAE debiased" and "native corr" recomputed from the saved
cells (`prediction` minus its own possession-weighted bias; `native` is the
uncalibrated points/100 column).

| arm | MAE | MAE debiased | RMSE | raw r² | bias | native corr |
|---|---:|---:|---:|---:|---:|---:|
| H0 historical | 8.1815 | 8.1584 | 10.9576 | .10142 | -0.801 | .3192 |
| H1 learned state | 8.1673 | 8.1596 | 10.9305 | .10585 | -0.447 | .3271 |
| H2 fixed-state context | 8.1606 | 8.1607 | 10.9052 | .10999 | -0.026 | .3305 |
| H3 joint | 8.1522 | 8.1516 | 10.8874 | .11289 | -0.058 | .3340 |
| corrected additive | 8.0920 | 8.0856 | 10.8410 | .12043 | -0.548 | — |
| structural parent | 8.1440 | 8.1342 | 10.9214 | .10733 | -0.680 | — |
| location + shooting | 8.1312 | 8.1315 | 10.8964 | .11142 | -0.462 | — |

H3 loses to the corrected additive by 0.060 MAE and to location+shooting by
0.021. On the pooled population this is not a candidate.

### 1.2 Novel-off5 — where it is interesting

2,073 cells / 226,256 possessions.

| arm | novel MAE | novel RMSE | novel r² | novel corr | corr drop all→novel |
|---|---:|---:|---:|---:|---:|
| **H3** | 8.8991 | **11.8045** | **.10770** | **.33057** | **-0.009** |
| location + shooting | **8.8674** | 11.8208 | .10523 | .32715 | -0.014 |
| H2 | 8.9019 | 11.8382 | .10260 | .32673 | -0.008 |
| structural parent | 8.8903 | 11.8466 | .10132 | .32171 | -0.015 |
| corrected additive | 8.9039 | 11.8530 | .10035 | .32064 | -0.033 |
| H1 | 8.9243 | 11.8879 | .09504 | .31156 | -0.021 |
| H0 | 8.9278 | 11.8940 | .09411 | .30844 | -0.020 |

**H3 has the best novel r², best novel RMSE and best
novel correlation of any arm on record**, and H2/H3 lose only ~0.009 of
correlation moving from `all` to `novel` where the corrected additive loses
0.033. The additive is a better in-support model and a worse extrapolator; that
asymmetry is the single most encouraging thing in this run.

### 1.3 Season-paired contrasts

11 primary seasons, possession-weighted within season, equal-season mean ± SEM,
seasons favorable. Negative = first arm better.

| contrast | MAE | | RMSE | |
|---|---:|---:|---:|---:|
| H1 − H0 | -0.0143 ± 0.0162 | 5/11 | -0.0275 ± 0.0132 | 8/11 |
| H2 − H0 | -0.0219 ± 0.0350 | 6/11 | -0.0533 ± 0.0314 | 9/11 |
| H3 − H1 | -0.0160 ± 0.0214 | 6/11 | -0.0432 ± 0.0187 | 8/11 |
| **H3 − H2** | **-0.0084 ± 0.0404** | **5/11** | **-0.0175 ± 0.0363** | **7/11** |
| H3 − H0 | -0.0303 ± 0.0320 | 6/11 | -0.0708 ± 0.0299 | 8/11 |
| H3 − parent | +0.0106 ± 0.0280 | 4/11 | -0.0339 ± 0.0240 | 7/11 |
| H3 − location+shooting | +0.0204 ± 0.0329 | 5/11 | -0.0110 ± 0.0293 | 7/11 |
| H3 − additive | +0.0572 ± 0.0419 | 4/11 | +0.0449 ± 0.0387 | 5/11 |
| H3 − additive (novel) | -0.0113 ± 0.0956 | 5/11 | -0.0522 ± 0.0735 | 7/11 |

Factorial interaction `(H3−H1)−(H2−H0)`: **+0.0058 MAE, +0.0092 RMSE, −0.00153
r²** on `all` — sub-additive, i.e. the two ingredients are substitutes there. On
novel r² it is **+0.00417**, super-additive. Both are inside noise; report the
number, do not tell a story with it yet.

---

## 2. Findings

### F1 — The control arm never trains, and its penalty was set by a tie-break on noise

`development/selected.csv`:

    arm  lambda  validation_loss  boundary
     H0    1.00         0.996378      True
     H1    0.10         0.995581     False
     H2    0.01         0.995152     False
     H3    0.01         0.994222     False

`development/grid.csv`, means over 2014q3/q4:

    lambda     0.001     0.010     0.100     1.000    spread
    H0     0.9963502 0.9963500 0.9963488 0.9963781   2.9e-5
    H1     0.9955319 0.9955309 0.9955808 0.9959557   4.2e-4
    H2     0.9951482 0.9951518 0.9953415       —     1.9e-4
    H3     0.9942276 0.9942224 0.9945272       —     3.0e-4

**H0's entire response across the whole grid spans 2.9e-5, against a declared tie
tolerance of 1e-4.** So `_prefer_larger_lambda_within_tolerance` walked H0 to the
0.1 edge, triggered the one permitted expansion, and then chose lambda=1.0 —
which is H0's *worst* grid point, worse than 0.1 by 2.9e-5, i.e. inside the
tolerance again. H2/H3 have a real 1.9e-4 / 3.0e-4 response, so their selection
is meaningful. H0's is a coin flip that always lands on "more penalty", because
the flattest arm is the one the tie rule pushes hardest.

The consequence, from `logs/core.log` (selected-epoch counts across 48 origins):

    H0: epoch 1 x48                                    mean 1.0
    H1: 1 x14, 2 x13, 3 x14, 4 x4, 5 x1, 6 x2          mean 2.4
    H2: 2 x1, 3 x9, 4 x10, 5 x8, 6 x9, 7 x8, 8 x2, 9 x1  mean 5.1
    H3: 1 x5, 3 x4, 4 x5, 5 x5, 6 x12, 7 x6, 8 x8, 9 x2, 10 x1  mean 5.6

**H0 selects epoch 1 in 48 of 48 origins** and its train loss sits at 1.000024 —
it never improves on its own initialization.

The cause is in `experiments/joint_capability_model.py:112-119`:

```python
def regularization(self, prediction, neff, coefficient):
    own     = (prediction.encoder_delta.square()*exposure_weight).mean()
    context =  prediction.context_delta.square().mean()
    decoder = (self.intercept.square().mean() +
               torch.log(torch.clamp(self.slope, min=1e-8)).square().mean())
    return float(coefficient)*(own+context+decoder)
```

One lambda multiplies all three, and the decoder is **shared by every arm**. So
H0's 36 decoder parameters are penalized 100x harder than H3's identical 36. H0
is therefore not "no learned teammate response"; it is "no fitting at all". This
is CLAUDE.md rule 10 in a new costume — a control arm on a grid boundary is not a
control — and memory `feedback_boundary_control.md` records that 58% of an
apparent 5x result was once exactly this.

**How it reaches points.** In `forward()`, a common shift in the three log-rate
intercepts cancels: `q` is renormalized by `scale = budget/normalizer`, so
allocation depends only on *relative* rates. The six conversion-logit intercepts
do not cancel — `player_points = Σ_b attempts_b · make_b · value_b` — so shifting
them moves the score directly. And that shift is nearly free in the training
objective: conversion validation loss moves only 0.658909 → 0.658477 (**0.066%**)
across the whole H0→H3 span. A parameter the event objective barely constrains,
which the arms were permitted to move by different amounts, is setting the point
bias spread (-0.801 → -0.026). §2.4 of the plan warned "do not let a weakly
penalized intercept shift masquerade as capability"; the implementation produced
the mirror image — a *differently* penalized intercept masquerading as capability.

**Consequence for the factorial: H3 − H2 is the only contrast fitted at matched
lambda (0.01 vs 0.01), and it is null** — -0.0175 ± 0.0363 RMSE, 7/11. H1 sits at
0.1 and H0 at 1.0, so H1−H0, H2−H0, H3−H1 and H3−H0 are all confounded.

### F2 — Most of the headline MAE gain is level, not skill

Debiasing each arm by its own possession-weighted bias:

    arm   MAE     MAE debiased    RMSE      RMSE debiased
    H0    8.1815  8.1584          10.9576   10.9282
    H1    8.1673  8.1596          10.9305   10.9213
    H2    8.1606  8.1607          10.9052   10.9052
    H3    8.1522  8.1516          10.8874   10.8872

The MAE ordering vanishes: H1 and H2 are marginally *worse* than H0 once the
level is removed. RMSE survives (10.9282 → 10.8872) and so does native
correlation, which is invariant to any affine map: **.3192 → .3271 → .3305 →
.3340**, monotone across the four arms, measured before calibration touches
anything. So there is genuine discrimination — but the MAE column in the
cumulative scoreboard is not where it lives, and F1 is a candidate explanation
for part of the correlation gain too, since 18 free per-coordinate decoder slopes
are themselves a recalibration.

Related, from the per-origin `calibration.json`: native prediction spread grows
4.141 → 4.613 → 4.994 → 5.343 across the arms while the fitted calibration slope
falls 0.834 → 0.812 → 0.758 → 0.711. The calibrator is discounting most of the
extra spread each arm produces. Calibrated spread only moves 4.291 → 4.527
against an actual spread of 11.559.

### F3 — The 730-day training time weight was never implemented

`JOINT_CAPABILITY_MODEL_PLAN.md` §5.1: *"Training examples carry a 730-day time
weight common to all five losses and all arms; it is distinct from role-state
recency."*

There is no such weight in `event_losses`, in `train`, or in `game_batches`.
Losses are normalized by event exposure only; every game in the 5-year lookback
counts equally. This is a frozen-protocol deviation and should be recorded as one.

It is also likely costing accuracy. League 3PA share moved 28.36% → 40.77% over
this window (`ASOF_ACCOUNTING_AUDIT.md`); `ratings_go_stale.md` and
`profile_recency_works.md` both say drift is the exploitable part, the latter
finding an interior optimum at a 0.4-season half-life. A decoder fitted uniformly
over five years sits roughly 2.5 years stale, which is the natural explanation
for H0's **-0.801** point bias: under-prediction in a rising-scoring era.

That yields a clean pre-registered prediction worth writing down before the fix
is run: **adding the specified time weight should improve all four arms and
narrow the bias spread between them**, because it removes the staleness that the
arms are currently correcting by unequal amounts.

### F4 — The model is barely off its initialization

`encoder_norm` and `context_norm` in `cells.csv.gz` are RMS per-coordinate state
corrections:

    arm  encoder_norm (mean / p95)   context_norm (mean / p95)
    H1      0.0425 / 0.0585                 0 / 0
    H2           0 / 0                 0.0629 / 0.0945
    H3      0.0813 / 0.1174           0.0650 / 0.1142

Base coordinates are log-rates near -2.5 and logits of order 1, so these
corrections are **~2% of the state scale**. With ~199k training rows at
`target_rows=4096` that is ~49 batches per epoch, and arms select 1-6 epochs:
**roughly 250-400 Adam steps at lr 1e-3, from zero-initialized output layers.**
Whatever this architecture is worth, this run measures a lower bound on it.

Three compounding causes, each cheap to remove:

- **`learning_rate: .001` is a pinned default that no run in this project has
  ever varied.** CLAUDE.md rule 12: a default grid is un-audited until some run
  has walked off it, and a default is visible in neither the command line nor the
  write-up. This one is load-bearing and invisible.
- **`minimum_improvement=1e-4` per epoch against a total run improvement of
  ~1.7e-3.** At 2026q3/H3 the inner validation went 1.032176 → 1.030425 over ten
  epochs; the per-epoch stopping bar is ~6% of all the signal there is. The curve
  is genuinely decelerating, so this is not the dominant cause — but it is the
  wrong scale for the effect being measured.
- **The message MLP reads unstandardized state.** In `contextual_state`, the
  encoder gets the z-scored `x` (standardization fitted on training rows), but
  `self.message` is fed `pair = cat([h_i, h_j])` where `h = base + enc` is raw:
  log-rates near -2.5 alongside centered logits near 0 alongside conversion
  logits near -0.5. Same default `nn.Linear` init, very different input scales.
  The encoder was given a conditioned problem and the message net was not. This
  is a defect, not a design choice, and it plausibly explains why H2 needs 5.1
  epochs to reach what H1 reaches in 2.4.

### F5 — The channel that carries points is the one that does not move

Selected-epoch inner-validation family losses, mean over 48 origins, from
`logs/core.log`:

    arm       val      counts    location  conversion  free_throw   assisted
    H0   1.000022    1.008844    1.372787    0.658909    0.519106   0.610914
    H1   0.998902    1.004992    1.372031    0.658700    0.518831   0.610725
    H2   0.998638    1.006600    1.369948    0.658631    0.519107   0.609591
    H3   0.997555    1.003454    1.368902    0.658477    0.519045   0.608913

H3 vs H0 as a percentage of the H0 level:

    counts      -0.534%   who shoots — zero-sum inside a five
    assisted    -0.327%   auxiliary head; does NOT enter player_points
    location    -0.283%   where — partly cancelled by construction (§8j)
    conversion  -0.066%   the term that actually scores
    free throw  -0.012%

The objective divides each family by its own training baseline and averages the
five equally, so **a fifth of the gradient goes to `assisted`, which has no path
into the score** (check `forward()`: `player_points` uses `fga`, `location`,
`make`, `fta`, `ft_make`; `assisted` appears in `Prediction` and nowhere else),
and conversion is weighted the same as everything else.

This matters because §10/§10b established that teammate influence on *conversion*
is real and forecasts: Jokić +1.69 ± 0.36 pp on the same shooters from the same
distance after shooter and game fixed effects, forward slope 1.082 ± 0.084
positive in 12/12 seasons over 2.66M held-out attempts, ~0.9 pts/100 of lineup
spread, free-throw placebo +0.38. **The one teammate effect this project has
established forward is the one the message pass finds almost none of.** With
~400 optimizer steps, a penalty on message outputs, and equal family weights,
the network will always spend its capacity on `counts` — where the loss gradient
is largest — rather than hunt a 1.7pp conversion effect.

Reallocating *who* shoots inside a fixed budget is close to zero-sum in points
unless the players differ in efficiency, and the location mix is partly cancelled
by construction. So the small point gain is exactly what this channel table
predicts. §11.3 anticipated this case ("channels improve but points do not");
this is it, and the diagnosis is specific.

### F6 — No placebo exists, so nothing here is decidable yet

`experiments/joint_capability_diagnostics.py` **does not exist**.
`joint_capability_run.py:484` imports `run_diagnostics` from it, so the
`diagnostics` subcommand raises ImportError. Not run, therefore:

- the **context-shuffle negative control** (§4) — the load-bearing test;
- the **FT-context diagnostic** (§4);
- the **fixtures panel** (§6.2) — Jokić/Korver/Westbrook with Murray retained,
  Haliburton same-four, five centers, five small guards, Gobert and Jokić clones,
  the two small-ball fives;
- **seed sensitivity** (§5.4, seeds 29/43 on four fixed origins);
- the **interval and support audit** (§7);
- the **high-exposure disagreement review** (§12.5);
- `reports/joint_capability_2026_09_09.md` (§12). `reports/` holds only
  `metrics.csv`.

Tests: 10 exist (6 model, 2 data, 2 run) against the ~20 required by §9. Absent
are the three that would guard the claims made above — future mutation (§9.1),
brute-force vs incremental history (§9.4), and the synthetic additive /
complementarity generators (§9.7). §9.4 is the one that would catch a subtly
wrong chronological recurrence, and §9.7 *is* the placebo at unit-test scale:
"context should not systematically improve truly independent held-out data."

Adam's relaxed significance rule (`feedback_significance_bar.md`) explicitly
keeps the placebo discipline while relaxing the decision rule. H3 does move every
metric the same way against H0 — MAE -0.030, RMSE -0.071, r² +0.011, bias -0.801
→ -0.058, native correlation +0.015 — but with no placebo and a compromised
control, that pattern cannot yet be cashed.

---

## 3. What is genuinely good

Not a courtesy paragraph; these are the reasons the program is worth continuing.

- **The novel-lineup result.** Best novel r², RMSE and correlation on record,
  and the smallest degradation from `all` to `novel` of any arm. Extrapolation to
  unseen fives is the northstar's binding constraint and the thing the coverage
  gate currently *asserts* rather than derives.
- **The causal data path is the most careful in this repository.**
  Beginning-of-day states, explicit end-of-day update, teammate reference
  accumulated from the same beginning-of-day states, per-origin frozen states for
  both inner validation and outer test, standardization fitted on training rows
  only, `usage_budget` strictly prefix. `build_states` decays `c180/q180` and
  `c730/q730` per elapsed day and aggregates same-day appearances before
  `np.add.at` so squared-weight exposure treats a day as the update block. I
  looked for a leak here and did not find one.
- **The population join is exact.** `_aggregate_cells` merges against the frozen
  control cells `validate="one_to_one"` and raises on any missing cell, any
  possession mismatch, or any actual-point mismatch above 1e-9. The point
  comparison against the corrected additive, the parent and location+shooting is
  genuinely apples-to-apples.
- **No player-ID, pair, team or lineup parameters.** Identical states get
  identical treatment by construction, so 5-Shaq invariance is structural rather
  than asserted, and `selection_on_the_outcome.md`'s objection — that no fitted
  structure can supply the fix because lineups are selected on the outcome — does
  not bite the same way when nothing is fitted per identity.
- **Per-location conversion means the mix is live in the score.** §8j's defect
  (a scalar `self_2p` cancelling the shot mix, long-two→rim worth +0.006 not
  +0.548) is fixed by design here, and §12's lesson is correctly absorbed.
- **Player-level event supervision inside known lineups is the real new
  ingredient.** §7/§8 could not identify volume or composition effects from
  lineup residuals — zero-sum inside a five, and the selector annihilated the own
  block. Here *who shot* is directly observed on 897,778 game-lineup rows, so
  reallocation is identified in a way it previously was not. That is the
  substantive argument for why this attempt is not the bilinear/attention nulls
  repeating, and it survives review.
- **One shared decoder** for training, scoring and any future panel; valid
  probabilities and a budget identity by construction.

---

## 4. Two things to be honest about in the write-up

- **This has been examined repeatedly.** §0 of the plan says so, and it is right
  to. The 44 origins are not an untouched holdout, and each new architecture
  scored against them buys a little more selection. The novel-off5 advantage is
  the most credible number here precisely because no previous arm was tuned
  toward it.
- **The pooled result is a loss.** H3 is 0.060 MAE behind the corrected additive
  and 0.021 behind location+shooting, with 4/11 and 5/11 seasons. `MODEL_SCORECARD.md`
  should say that plainly. The interesting claim is narrower and should be stated
  narrowly: *best extrapolation to unseen fives, from an architecture that has
  not yet been trained to convergence, with the core factorial not yet identified.*

---

## 5. Recommended next steps

Ordered. Tier 1 is ~1 hour of compute and can change the headline. Remaining
budget under the plan's own ceiling: ~11 of 12 wall-clock hours and 216 of 600
fit invocations. Every run goes to a new prefix
(`joint_capability_2026_09_09_v3`), never into v2.

### Tier 1 — make the factorial mean something (~1 h)

1. **Split the decoder penalty from the network penalty.** Give `decoder` in
   `regularization()` its own fixed coefficient, identical in all four arms, and
   let the selected lambda govern only `own + context`. This is what §2.4
   actually requires. H0 then has no free lambda at all, which is the honest
   statement of the control.
2. **Re-run all four arms** on the 48 origins (~51 min measured; ~16 s per
   arm-origin). Pre-register both outcomes: if the H-minus-H0 point contrasts
   collapse, the factorial was measuring decoder freedom; if the native
   correlation ordering .3192 / .3271 / .3305 / .3340 survives, the architecture
   is doing something.
3. **Report `H3 − H2` as the primary encoder contrast**, since it is the only one
   the v2 run identified, and say so.

### Tier 2 — the missing placebo (~30 min)

4. **Mean-field control** — cheaper and sharper than the planned shuffle, and I
   would run it first. Replace `c_i = mean_j M(h_i, h_j)` with
   `c_i = M(h_i, h̄)`, where `h̄` is the prefix league-average state: same
   parameter count, same recalibration capacity, **zero teammate-specific
   information**. If H2 is not distinguishable from mean-field, the message pass
   is a state recalibrator and the word "context" has to come out of the
   write-up. This is the same discriminator as own-rate orthogonalisation in the
   four-factors work (`four_factors_influence.md`): strip the component that
   would be there under the null, then look at what is left.
5. Then the protocol's own **context shuffle** (§4) on the four fixed origins,
   and the **FT-context** head. The FT head is the free-throw placebo this
   project has used successfully three times.

### Tier 3 — let the model actually train (~1 h)

6. **Standardize the message inputs** in `contextual_state` using the same fitted
   mean/scale path the encoder already uses. Pure defect fix; no protocol
   argument needed.
7. **Audit the learning rate and step budget** on the two development origins
   only: lr ∈ {1e-3, 3e-3, 1e-2}, `max_epochs` 12 → 40, `minimum_improvement`
   1e-5. Print the selected value against both grid ends every run. State
   explicitly that this is an audit of an un-audited default under rule 12, not
   the open-ended sweep §11.2 forbids — the distinction is the write-up, and a
   default that no run has walked off is exactly what rule 12 names.
8. **Implement the 730-day training weight** the protocol already specifies (F3),
   with the pre-registered prediction stated there.

### Tier 4 — point the capacity at the channel that pays (~2 h)

9. **Weight the five families by points leverage** instead of equally. Leverage
   is derivable from the decoder itself and is prior-only, so this does not put a
   points loss into training and does not violate §2.7. At minimum, ablate
   `assisted`: it is a fifth of the gradient and cannot reach `player_points`.
10. **Feed the measured shot-quality on/off coefficient in as a teammate-context
    input.** It is the one teammate effect established forward here (12/12
    seasons, slope 1.082 ± 0.084), the refit-strictly-before-each-origin
    machinery already exists in `shot_quality.py`, and the message pass currently
    recovers 0.066% of the conversion channel. If the network cannot find it from
    raw states in 400 steps, hand it the coordinate.

### Not now

§8.1 overload response, §8.2 rebound competition, §8.3 opponents. All three are
well specified and all three sit on a core comparison that is not yet identified.
Building them first is how a research program acquires machinery it cannot
interpret.

### Conditions on any re-run

New prefix; v2 immutable; both `metrics.csv` compared cell-for-cell on the same
frozen keys; the `_aggregate_cells` guards kept as they are. Land the three §9
tests that guard these claims — future mutation, brute-force vs incremental
history, and the synthetic additive generator — before believing a re-run.

---

## 6. Suggested `MODEL_SCORECARD.md` row

Not added by me — Sol owns that table under §12. Ready to paste:

```
| joint capability H3 | 8.1522 MAE / .11289 r²; novel 8.8991 / **.10770 novel r², best on record** | Fixtures not yet run; no ID parameters, so clone invariance is structural | Not audited; §7 deferred | Core factorial not identified: control arm regularized 100x harder and selected epoch 1 in 48/48 origins; no placebo run | research-only |
```

---

## 7. Provenance

| claim | source |
|---|---|
| pooled and novel metrics | `reports/metrics.csv` |
| debiased metrics, native corr, season pairing | recomputed from `origins/*/*/cells.csv.gz` |
| lambda selection and grid response | `development/selected.csv`, `development/grid.csv` |
| selected-epoch counts, family losses | `logs/core.log` |
| calibration a/b per arm | `origins/*/*/calibration.json` |
| correction norms | `encoder_norm` / `context_norm` in `cells.csv.gz` |
| run state, fits, timing, versions | `manifest.json`, `logs/preflight.log` |
| coverage and match rates | `input_audit.json` |
| missing diagnostics module | absence of `experiments/joint_capability_diagnostics.py` |

No test suite was run for this review; nothing executable was changed.
