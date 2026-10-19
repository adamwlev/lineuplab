# Joint capability v5: the input factorial

2026-09-11, Claude Opus 5 with Adam. Run
`experiments/cache/joint_capability_2026_09_10_v5/`. 384 arm-origins (8 arms ×
48 origins), all verified — every required file present, cell and group counts
matching `complete.json`, every checkpoint loading, no non-finite prediction.
No scorer or page promoted.

## Bottom line

**Nothing beats the backbone.** v4 froze the architecture at E0M_L2; v5 varied
only the inputs and the target, six ways, and every intervention is null or
harmful. On the decision sample V5_BASE has the best novel MAE, RMSE and r² of
the eight arms, and no arm-minus-BASE contrast favours the intervention.

Two contrasts are *established against* an intervention, and together with v4
they turn a knob into a finding: **λ = .01 is an interior optimum.** v4 showed
λ = .0001 is worse on novel lineups; v5 shows λ = .1 is too.

The one intervention that demonstrably did what it was built to do — the
opponent deconfounding — bought nothing in points, exactly as Phase 0 sized it.

## 1. Decision sample

2016–2025, 40 origins, 5,179 cells, 675,434 possessions. 2026 was held out and
is reported separately in §5.

| arm | all MAE | all RMSE | all r² | novel MAE | novel RMSE | novel r² |
|---|---:|---:|---:|---:|---:|---:|
| corrected additive | **8.06600** | **10.79675** | **.11635** | 8.79872 | 11.76137 | .09096 |
| **V5_BASE** | 8.09859 | 10.83974 | .10930 | **8.74621** | **11.70624** | **.09947** |
| V5_OPP | 8.10047 | 10.83394 | .11025 | 8.76933 | 11.70815 | .09917 |
| V5_LEV | 8.10298 | 10.84053 | .10917 | 8.79952 | 11.75212 | .09239 |
| location + shooting | 8.10472 | 10.84747 | .10802 | 8.75773 | 11.72845 | .09605 |
| V5_BIO | 8.11030 | 10.83624 | .10987 | 8.79650 | 11.74292 | .09381 |
| V5_L1 | 8.11172 | 10.84383 | .10862 | 8.77040 | 11.73059 | .09571 |
| V5_RICH | 8.11494 | 10.84915 | .10775 | 8.79195 | 11.72375 | .09677 |
| structural parent | 8.11889 | 10.87175 | .10403 | 8.78200 | 11.75331 | .09221 |
| V5_ORB | 8.12045 | 10.86293 | .10548 | 8.77026 | 11.73739 | .09467 |
| V5_ALL | 8.13821 | 10.85300 | .10712 | 8.81410 | 11.72591 | .09644 |

## 2. Pre-registered contrasts

Season-paired over the 10 decision seasons, mean ± sem with a 95% t interval.
Positive MAE/RMSE means the intervention is **worse** than BASE.

### All cells — nothing helps

    V5_OPP  - BASE   MAE +0.00079 +- 0.02237   5/10      RMSE -0.00504 +- 0.02078   5/10
    V5_BIO  - BASE   MAE +0.01006 +- 0.01866   4/10      RMSE -0.00389 +- 0.01444   6/10
    V5_ORB  - BASE   MAE +0.01938 +- 0.02264   4/10      RMSE +0.02172 +- 0.01962   2/10
    V5_RICH - BASE   MAE +0.00828 +- 0.04704   5/10      RMSE +0.00633 +- 0.04094   4/10
    V5_ALL  - BASE   MAE +0.03725 +- 0.04362   4/10      RMSE +0.01295 +- 0.03473   6/10
    V5_L1   - BASE   MAE +0.01298 +- 0.01692   4/10      RMSE +0.00548 +- 0.01260   5/10
    V5_LEV  - BASE   MAE +0.00044 +- 0.01545   5/10      RMSE -0.00072 +- 0.01406   5/10

Every MAE point estimate is positive. The two negative RMSE estimates — OPP and
BIO — are a fifth of their own sem.

### Novel lineups — three intervals exclude zero, all against the intervention

    V5_LEV  - BASE   MAE  +0.05244 +- 0.02174  [+0.00327,+0.10161]   1/10  *
    V5_LEV  - BASE   RMSE +0.04700 +- 0.02054  [+0.00053,+0.09346]   2/10  *
    V5_L1   - BASE   RMSE +0.02636 +- 0.01128  [+0.00084,+0.05187]   1/10  *
    V5_L1   - BASE   r2   -0.00453 +- 0.00192  [-0.00886,-0.00019]   1/10  *
    V5_OPP  - BASE   MAE  +0.02704 +- 0.02488                        1/10
    V5_ORB  - BASE   MAE  +0.02150 +- 0.02303                        2/10
    V5_RICH - BASE   MAE  +0.04552 +- 0.04508                        4/10
    V5_BIO  - BASE   MAE  +0.05433 +- 0.03562                        3/10
    V5_ALL  - BASE   MAE  +0.06772 +- 0.05545                        3/10

**λ = .01 is an interior optimum.** v4: λ = .0001 costs novel RMSE +0.03233
[+0.00912, +0.05554] at 3/11. v5: λ = .1 costs +0.02636 [+0.00084, +0.05187] at
1/10. Both directions are established worse out of sample, from independent runs.

**Points-leverage family weighting is established worse on novel lineups.**
Pointing the objective at conversion did not move conversion (§4) and cost
generalisation. This closes a proposal I made in three consecutive reviews.

### Stacking — the components do not interact

    MAE   sum of singles +0.03851   V5_ALL +0.03725   interaction -0.00126
    RMSE  sum of singles +0.01912   V5_ALL +0.01295   interaction -0.00617

ALL is the sum of its parts. Four independent, independently mildly harmful
changes, with no offsetting structure between them.

### BASE against the frozen controls

    all    vs additive       MAE +0.03228 +- 0.05255  4/10    RMSE +0.04114 +- 0.04611  5/10
    all    vs location+shot  MAE -0.00355 +- 0.04663  5/10    RMSE -0.00889 +- 0.03663  5/10
    novel  vs additive       MAE -0.05453 +- 0.07212  5/10    RMSE -0.06041 +- 0.07040  7/10
    novel  vs location+shot  MAE -0.01130 +- 0.05334  5/10    RMSE -0.02144 +- 0.03992  6/10

Unchanged from v4: behind the additive in support, ahead on novel lineups, tied
with location+shooting, nothing established either way.

## 3. Did the opponent arm do what it was built to do?

The pre-registered criterion for V5_OPP was never MAE — Phase 0 sized that prize
at 0.0024 RMSE, seventeen times below what this benchmark resolves. The criterion
was the **paired residual loading on state-window schedule collapsing toward
zero**, which is well powered.

Paired loading of `(arm residual − additive residual)` on state-window schedule,
scored-window schedule controlled:

| arm | slope | sem | t | pts/100 per 1 sd |
|---|---:|---:|---:|---:|
| V5_BASE − additive | +2.3385 | 1.2322 | 1.90 | +0.2434 |
| **V5_OPP − additive** | **+1.4886** | 1.4562 | 1.02 | +0.1550 |
| V5_ALL − additive | +2.3618 | 1.3175 | 1.79 | +0.2459 |

Phase 0 measured the v4 ancestor of V5_BASE at **+2.39**; V5_BASE reproduces it
at **+2.34**, which independently validates both the Phase 0 measurement and the
v5 port.

The adjustment is real and correctly signed — OPP moves predictions by a mean of
0.336 pts/100 (max 2.47), and `corr(OPP − BASE, schedule) = −0.214`, negative as
designed. It removes **36%** of the asymmetry. It does not close it, the collapse
is not statistically separable given the sems, and it buys nothing in points.

Curiously V5_ALL shows no collapse at all (+2.36), so whatever the other three
changes do, they reintroduce the schedule dependence that OPP removes.

## 4. Event channels, and a measurement trap

**The trap first.** `event_loss` is scaled by each arm's *own* untrained
baseline. For BASE/BIO/ORB/RICH/L1/LEV the base state is identical so the
baselines agree and the scaled totals compare fairly — but **OPP's base state is
adjusted, so its baseline differs and its scaled total is not comparable.** OPP
appears to have the best scaled event loss (0.993959 vs BASE's 0.994737) and on
raw families it is *worse* on location. Compare raw families, not the scaled
total, whenever an arm changes the anchored state.

Raw per-family outer loss, difference from BASE (negative = better):

| arm | counts | location | conversion | free throw | assisted |
|---|---:|---:|---:|---:|---:|
| V5_ALL | −0.001063 | −0.000306 | −0.000014 | +0.000023 | −0.000701 |
| V5_RICH | −0.000967 | −0.000971 | +0.000046 | −0.000001 | −0.000569 |
| V5_BIO | −0.000193 | −0.000017 | −0.000019 | +0.000001 | −0.000166 |
| V5_ORB | +0.000019 | −0.000182 | +0.000040 | −0.000001 | −0.000032 |
| V5_OPP | −0.000011 | **+0.000978** | +0.000050 | +0.000026 | +0.000032 |
| V5_L1 | +0.000053 | +0.000466 | +0.000202 | +0.000001 | +0.000249 |
| V5_LEV | −0.000009 | +0.000182 | −0.000035 | +0.000001 | +0.000453 |

**RICH and ALL genuinely improve the event channels** — counts, location and
assisted share all move the right way — and both are *worse* in points. The
recurring pattern of this workstream, now reproduced on the input side.

**Conversion did not move, in any arm, for the fifth consecutive version.** The
largest absolute change across all seven interventions is 5.0e-5, and the arm
built specifically to point capacity at conversion (LEV) moved it by 3.5e-5
while losing novel generalisation.

Training behaviour explains the direction of the damage:

| arm | median selected epoch | cap hits |
|---|---:|---:|
| V5_BASE | 13 | 2 |
| V5_OPP / V5_BIO | 12 | 1 / 0 |
| V5_RICH | 11 | 1 |
| V5_ORB | 10.5 | 0 |
| V5_ALL | 9.5 | 0 |

Wider message inputs stop earlier. At fixed data and fixed steps, extra input
width buys fit and costs generalisation, which is exactly the novel-slice
ordering.

## 5. The holdout, and what it was worth

2026 was fitted and withheld from every number above; revealed once, after the
decision.

4 origins, 428 cells, 50,930 possessions. Every arm's r² is between −0.005 and
+0.023 against 0.10–0.12 in the decision sample, and correlations run 0.12–0.20
against 0.33. The rankings scramble completely — V5_ORB is best on both slices,
V5_RICH worst, neither resembling its decision-sample position.

**The holdout is too small to adjudicate.** 428 cells cannot resolve 0.03 MAE.
It neither confirms nor refutes the decision; the honest statement is that no
arm's advantage replicates, which is what a table of nulls predicts. Reserving a
confirmation slice was the right discipline and 8% of the sample was the wrong
size — a lesson for v6, not a result.

## 6. Verification

- 384/384 arm-origins verified: files present, `n_cells`/`n_groups` matching,
  checkpoints loading, all predictions finite.
- **V5_BASE reproduces v4's E0M_L2 to max 3.8e-5 points/100** on the shared
  origin — float32 accumulation noise, the same order as v4's own alias audit.
  Every contrast above is therefore one factor off a verified baseline.
- Identical cell counts (6,179 across 48 origins) for all eight arms, joined
  one-to-one against the frozen benchmark cells.
- A concurrent-launch race killed one process mid-run; all completed work
  verified intact and a run lock plus atomic checkpoint writes were added
  (`a0b5f8b`). Operational only; no scientific fingerprint changed.
- 654 tests pass.

## 7. Decision

**Keep V5_BASE — which is v4's E0M_L2 — as the structural research backbone.**
1,814 parameters, 18 inputs, and nothing we added to its inputs earned its place.
Corrected additive remains the predictive baseline. No scorer promoted.

Retire from the candidate list: opponent-deconfounded inputs, bio, offensive
rebounding as a 19th coordinate, the wide feature routing, points-leverage family
weighting, and λ ≠ .01.

## 8. What I would do next

v5 tested six ways of feeding the model more, and the model wanted none of them.
Combined with Phase 0 — where four independently motivated defects all priced out
below 0.01 RMSE — the input hypothesis is now well explored and closed.

The open standards are not accuracy standards. The fixture magnitudes remain
roughly twice anything the model produces in range, and the support measure still
cannot separate five Gobert clones from a real five by more than 3%. Neither is
a points problem and both are well powered. That is where v6 should go, and the
case for it is stronger now that the input route is closed.
