# v5 Phase 0: sizing the levers before building

2026-09-10, Claude Opus 5 with Adam. Read-only on saved artifacts plus one new
derived prefix (`experiments/cache/v5_opponent_states/`). No fits, no run
directory touched, no scorer or page change.

CLAUDE.md rule 8 — measure the ceiling before building the model. Three of the
four Phase 0 diagnostics are now complete and **all three shrank or killed a
lever that was slated for a v5 arm.** That is the point of Phase 0, but it
changes what v5 should be.

Headline: **every identified defect prices out at ~0.005 RMSE or less, against a
benchmark that resolves ~0.04 and a gap to the corrected additive of 0.018.**

---

## D1 — the "free" over-dispersion shrink is not available. KILLED.

`BACKLOG.md` §0ad item 4 claims both arms are too wide after calibration and that
an extra shrink of ~0.79 takes 0.5% off MSE for no modelling. Measured on the
v4e cells it does not hold.

Out-of-sample slope of `(actual − league)` on `(prediction − league)`,
possession-weighted, 5,607 cells — 1.0 is correctly dispersed:

| arm | slope | oracle ΔMAE | prior-only ΔMAE | prior-only ΔRMSE |
|---|---:|---:|---:|---:|
| E0F_L2 | 0.9854 | −0.0016 | **+0.0191** | +0.0110 |
| E0M_L2 | 0.9424 | −0.0074 | **+0.0085** | +0.0078 |
| E1M_L2 | 0.9672 | −0.0036 | **+0.0148** | +0.0089 |
| E1P_L2 | 0.9603 | −0.0041 | **+0.0123** | +0.0077 |
| corrected additive | 1.0200 | +0.0010 | **+0.0119** | +0.0096 |

Three things. The arms are only 2–6% over-dispersed, not 21%. The *oracle*
shrink — which illegally uses the window it corrects — buys at most 0.007 MAE
and nothing at all for the additive. And the deployable **prior-only** shrink
makes **every arm worse**, because the per-origin estimate swings 0.82–1.21 and
applying a noisy correction costs more than the miscalibration it removes.

**Correction to my own v3 review.** `CLAUDE_MODEL_FEEDBACK_3.md` §G5 reported
"all arms are over-dispersed by ~12%" from a slope computed on raw levels rather
than league-centered deviations; that conflated between-window league movement
with within-window lineup spread. The league-centered slopes above are correct.
The separate §G5 point — that "exceptional lineups are shrunk too hard" is a
selection artifact common to every arm — stands on its own evidence.

**Do not re-run.** The prior-only calibration is already doing this job.

---

## D2 — the opponent asymmetry is REAL, cleanly established, and worth 0.002 RMSE.

The question: `asof_additive.identity_design` returns `(n, 2P)` — offence *and*
defence blocks — so the additive's θ_off is estimated controlling for who was
defending. The neural model's 18 coordinates are raw EB-shrunk historical rates.
Does that contaminate the neural states, and by how much?

**Method.** One chronological pass over all 6,059,380 possessions builds, for
every player and every date, (a) his decayed points-allowed-per-defensive-
possession and (b) the decayed mean defensive strength he *faced* on offence.
Beginning-of-day states price the day's possessions; the day's results update
afterwards, so every value is strictly prior and one build serves all 48 origins.
730-day half-life, EB-shrunk toward the running league mean with a 500-possession
prior. Saved as `experiments/cache/v5_opponent_states/defence_faced_k500.npz`
(96,431 player-origin rows) — this is the artifact V5-OPP would consume.

Lineup-level defence faced, centered within origin: **sd 0.104 pts/100**.
Correlation with the *scored*-window schedule is **+0.034** — a 730-day window
averages the schedule out, so this is not lever (a) in disguise. Controlling for
scored-window schedule anyway changes nothing.

**The paired test.** Regressing `(neural residual − additive residual)` on
defence-faced cancels the shared noise, so it tests the asymmetry directly rather
than comparing two noisy slopes:

| contrast | slope | sem | t | seasons + | pts/100 per 1 sd |
|---|---:|---:|---:|---:|---:|
| **E0F_L2 − additive** | **+5.08** | 0.64 | **8.00** | **11/11** | +0.528 |
| E0M_L2 − additive | +2.39 | 1.12 | 2.15 | 7/11 | +0.249 |
| E1M_L2 − additive | +2.26 | 1.23 | 1.84 | 7/11 | +0.235 |
| E1P_L2 − additive | +2.38 | 1.21 | 1.97 | 8/11 | +0.247 |

Placebo: permuting defence-faced across cells within origin, 200 draws, gives
mean +0.015 and sd 0.336; the real value exceeds **100%** of draws.

Unpaired, with scored-window schedule controlled, the additive itself reads
+1.37 ± 1.76 (t = 0.78) — the placebo arm reading ~zero, as predicted.

**Two findings.**

1. **The asymmetry is confirmed.** Without teammate context the neural model
   carries 0.53 pts/100 of systematic residual per sd of schedule contamination
   that the additive does not, at t = 8.00 across 11/11 seasons with a dead
   placebo. Adam's question — is the NN on equal footing with the additive? — is
   answered: no, and this is the size of it.
2. **Mean pooling already removes 53% of it** (+5.08 → +2.39). Teammates share
   schedules, so the teammate-mean channel partly encodes team-level schedule and
   lets the model deconfound itself. This is a new mechanistic fact about *why*
   mean pooling works — and a slightly deflating one for the teammate-influence
   story. It does **not** explain the v4 result: the deconfounding accounts for
   ~0.003 of mean pooling's 0.060 RMSE gain, about 5%.

**But the prize is 0.0024 RMSE.** The surviving differential is +2.39 slope ×
0.104 sd = 0.249 pts/100 of systematic residual; removing it entirely moves RMSE
from 10.8797 to 10.8773. That is ~17× below what this benchmark resolves.

**Verdict: build it for correctness, judge it on the residual loading, not on
points.** V5-OPP's success criterion should be "does the paired loading collapse
from +2.39 toward zero" — a well-powered test — and never "does MAE improve".

---

## D3 — the FTA composition gap does not reach the score. LARGELY KILLED.

`CLAUDE_MODEL_FEEDBACK_4.md` §C1 flagged that on the evaluation cells the model
over-predicts FTA by +2.9/100 against +0.1 on the full cohort, and suggested it
might be part of the remaining gap to the additive. It is not.

The description is right: E0M_L2 predicts 23.24 FTA/100 where the cells realise
20.32, carrying the full-population rate into a subpopulation that draws fewer
fouls. But the budget is shared and near-constant across cells (sd 0.204), so
over-predicting FTA mechanically under-predicts FGA, and the residual level is
absorbed by the affine calibration. Orthogonal to the arm's own prediction:

| regressor | slope | sem | t | seasons + |
|---|---:|---:|---:|---:|
| pred_fta | +0.0185 | 0.0528 | 0.35 | 5/11 |
| pred_three | −0.0390 | 0.0371 | −1.05 | 6/11 |
| pred_fga | +0.0995 | 0.0834 | 1.19 | 7/11 |

Dead. Even the uncontrolled version implies only 0.0048 RMSE.

**Correction to my own v4 review.** C1's description of the miscalibration stands
and is worth reporting as an event-channel fact; the inference that it was "a
plausible part of the last gap to the additive" is not supported.

---

## D3b — the fixed opportunity budget is NOT the cap either. KILLED.

Before writing the section below I asserted that the shared league budget `U` was
the structural reason the model cannot beat the additive: every lineup is handed
the same `FGA + 0.44·FTA + TO`, so the model can only reallocate and change
efficiency. Measured, that is wrong.

Across 8,907 real five-man units with ≥100 possessions (2,481,236 possessions):

| quantity | mean | sd across units |
|---|---:|---:|
| realised budget per 100 | 112.587 | **4.261** |
| model's assigned budget per 100 | 112.102 | **0.204** |
| realised offensive rating | 110.083 | 9.126 |

So real lineups vary enormously in opportunity budget and the model represents
essentially none of it — a 21× compression. But the slope of offensive rating on
budget is **−0.0909**, so one sd of budget moves ORtg by only −0.387 pts/100:
**0.18% of realised ORtg variance, worth at most 0.008 pts/100 of spread.**
Opportunity volume is close to orthogonal to efficiency, and part of even that
slope is definitional, since turnovers sit inside the budget and are bad.

This also sizes §8.2 of the original plan: **ORB budget feedback and variable
pace are not where the value is.** Do not build them for accuracy.

---

## What this means for v5

Four independent, well-motivated structural defects, each sized honestly:

| lever | status | RMSE prize |
|---|---|---:|
| over-dispersion shrink (D1) | not available; prior-only version is harmful | negative |
| opponent input contamination (D2) | **real**, t = 8.00, placebo dead | 0.0024 |
| FTA composition gap (D3) | absorbed by calibration, t = 0.35 | ~0 |
| fixed opportunity budget (D3b) | orthogonal to efficiency | 0.008 |

**Everything we can name in this architecture prices out below 0.01 pts/100.**

The decisive context is that **the gap to the corrected additive is not
established in the first place.** v4's own contrasts: E1P_L2 versus additive is
+0.0266 MAE and +0.0276 RMSE with both intervals crossing zero. The two families
are statistically tied on points. We have been treating a within-noise difference
as a deficit to explain, and then sizing explanations for it an order of
magnitude below what the benchmark can see.

What the neural family *does* have, and the additive does not:

- the best novel-lineup numbers on record — E0M_L2 best novel MAE 8.85744,
  E1M_L2 best novel RMSE 11.77732 and r² .11181, all ahead of additive's
  8.90390 / 11.85302 / .10035 — with mean-versus-fixed at **11/11 seasons**;
- coherent extreme-lineup behaviour with no position rule: five Gobert clones
  down, five Jokić clones up, five limited creators down 10–12 points;
- an explicit mechanism ledger that reconciles to 1e-13.

Two of the three product standards — basketball-coherent counterfactuals at
*validated magnitudes*, and honest OOD uncertainty — remain unmet, and neither is
a points problem. The fixture swings are still 193–228% of anything the model
produces in range, and the support measure still cannot separate five Goberts
from a real NBA five by more than 3%.

**The fork for v5, to decide before spending three hours of compute:** keep
hunting point accuracy in a regime where every named lever is 5× below the noise
floor, or turn v5 toward the two standards the neural arm is uniquely positioned
to satisfy and where the measurements are well powered. Recorded here; settled in
the session discussion, not by this document.
