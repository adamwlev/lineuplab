# Rebounding mechanism: experiments and current checkpoint

Recorded before the new forward results, 2026-09-04.

The fixed opportunity budget lets projected ORB change without granting the
extra usage event that an offensive rebound creates. Its conditional ORB
valuation is negative while holding attempts fixed, so this is not a coherent
independent rebounding mechanism.

Compare exactly two ledgers, with no hyperparameter sweep:

- Control: prior league mean `U = FGA + .44 FTA + TO` per possession.
- Candidate: prior mean `(U - credited player ORB)` plus the five players'
  projected ORB rate. One extra projected rebound grants one extra usage event.

Keep player states, shot allocation, shot valuation, shooting skill and assist
supply unchanged. Assisted-finish demand scales with the extra attempts. Each
arm receives its own sign-constrained point/assist calibration from completed
earlier origins only. Evaluate cumulative and latest states on the same
covered lineups, 2016–2026 after 2015 initializes calibration. No known pairs.

Three standards:

1. Report season-paired MAE, raw r² and ordinary correlation, plus direct
   usage/FGA errors. Confirm the fixed control reproduces the saved checkpoint.
2. Holding all else fixed, +1 ORB/100 should create +1 usage event/100 and
   increase points, including after assist-deficit calibration. Check every
   covered real lineup and the named Jokić/centers/guards/repeated-player panel.
3. Re-estimate each arm's game-split residual uncertainty and apply the same
   prior-only interval protocol. Do not reuse fixed-ledger error bars for the
   new mean. Synthetic results remain diagnostic, not verified latent coverage.

This first arm is deliberately an approximate opportunity ledger. It neither
limits ORB by available misses nor models competition among rebounders. Print
predicted ORB relative to predicted missed FGA plus .44 missed FTA, and test a
perfect-shooting diagnostic. Do not hide impossible combinations behind a cap
or infer that the first budget experiment is release-ready if accuracy holds.
Putback-specific allocation and a miss-conditioned rebound model are separate
follow-ups, to be motivated by this test rather than tuned to named outcomes.

## First result and predeclared follow-up

The first completed run exactly reproduces the saved fixed control. Latest
state gains raw r² +0.00526 ± 0.00230 and MAE −0.02284 ± 0.01558 per origin.
It predicts the usage budget better, but still penalizes +1 isolated ORB/100
for almost all real lineups. The conditional valuation contains both a large
intercept and a negative ORB coefficient; its attempt coefficients are not
literal expected points per extra attempt. Budget expansion alone is rejected
as the finished rebounding mechanism. Its results remain `rebound_budget_2026_*`.

Before running a second comparison, specify the change: use literal expected
shot points (training location make rates plus the existing player making
adjustment), with no direct ORB or turnover point coefficient and no creation
intercept. Retain both fixed and rebound budgets so the valuation change and
budget change remain separately measurable. Refit each arm's earlier-origin
point/assist calibration and interval diagnostics as before. This is a
follow-up informed by the failed mechanism, not an untouched confirmatory test
on a newly reserved set. It still fails the perfect-shooting/miss-availability
check by construction; no claim of a completed generative model is permitted.

## Basketball examples supplied by Adam before inspecting these player readouts

- Steven Adams: often exceptional at improving the team's offensive boards;
  value may extend beyond the rebounds credited to him personally.
- Mitchell Robinson: also excellent, with more of the contribution potentially
  visible in his own rebound count.
- Josh Hart: excellent offensive rebounding for his size; do not impose a
  simplistic height/position penalty that erases that ability.

These are mechanism expectations, not a mandated total ranking of the three
players. Inspect their own and teammates' credited ORBs separately. Team on/off
rates are descriptive and confounded by substitutions, teammates and opponents;
they are not causal box-out estimates or known-pair features. The current sum
of own-ORB profiles cannot directly represent teammate facilitation, so a good
total forecast alone does not mean it passes the Adams check.

## Completed results (read and checked across the September 4–5 interruption)

Both runs completed; no evaluation is still pending. Latest-state results:

| valuation / budget | MAE | raw r² | +1 isolated ORB/100 | five-center points/100 |
|---|---:|---:|---|---:|
| conditional / fixed (incumbent prototype) | 7.4742 | +0.01389 | negative | 103.77 |
| conditional / rebound | 7.4525 | +0.01890 | negative in 5,603/5,774 cells | 105.83 |
| expected shot points / fixed | 7.4545 | +0.01822 | zero | 112.09 |
| expected shot points / rebound | 7.5568 | −0.00622 | positive in all 5,774 cells | 125.06 |

Cells are distinct season-lineup combinations, not independent causal trials.
The control exactly reproduces the saved checkpoint's MAE, raw r² and ordinary
correlation. Cumulative state confirms the same mechanism conflict: conditional
valuation penalizes every isolated rebound, even with the expanded budget;
literal shot valuation with the expanded budget makes it positive everywhere.

Compared with its matching shot-expectation/fixed control, the shot-expectation
rebound arm changes latest-state MAE by **+0.10221 ± 0.06988**, raw r² by
**−0.02374 ± 0.01125**, and ordinary correlation by −0.02282 ± 0.01085 across
11 origins. Cumulative-state MAE worsens +0.23081 ± 0.07334. The earlier
conditional/rebound arm slightly improved prediction while failing coherence.
Thus the trade is not settled by choosing the arm with the best metric.

Latest-state raw tail-upper future-half coverage remains roughly nominal:
conditional/rebound 50.49/80.01/95.11%; shot-expectation/rebound
50.36/80.38/95.18%. Cumulative shot-expectation/rebound is worse in the sparse
tail (90.40% at nominal 95%). The schedules still measure assist-deficit
support, not the full rebound/role/matchup state. None verifies synthetic
latent-mean coverage.

The direct opportunity accounting improves held-out usage MAE, but FGA MAE
does not clearly improve. Expanding the budget alone therefore does not prove
that rebounds have been allocated to the right subsequent actions. Every
perfect-shooting synthetic lineup still receives projected rebounds under
both direct-rate ledgers: a known failure, not a tolerated product behavior.

**Decision:** retain the accepted scorer unchanged. Both rebounding variants
are experiments, not fixes to promote. The apparent coherence of the earlier
five-center score partly depended on a conditional coefficient that fails an
independent rebounding perturbation. Fixing that reveals the unconstrained
rebound-rate sum. No arm yet passes both checks.

## Adams / Robinson / Hart descriptive audit

`rebound_player_audit.py` uses existing player-game aggregates and game-cluster
bootstrap intervals. Team ORB / (team ORB + opponent DRB) measures recorded
live rebound opportunities; there is no .44-FTA approximation in this audit.

In 2026 Adams recorded 9.88 ORB/100 offensive possessions and his teammates
9.19; Robinson recorded 10.76 and his teammates 6.51. Adams collected 51.82%
of his team's on-court ORBs; Robinson 62.30%. The 2025 shares are 51.50% and
59.00%. That is consistent with Adam's qualitative distinction, not evidence
that the difference was caused by box-outs rather than teammate composition.

Adams's on-court live-chance recovery is 42.35% in 2026 and 41.56% in 2025.
This directly argues against treating 35% as a physical ceiling. His 2026
team on/off difference is +7.20 percentage points (game-bootstrap 95% interval
2.19–12.32); Robinson's is +11.25 (7.77–14.39). These comparisons control
neither substitutes nor opponents and must not become causal features.

Hart's raw offensive-rebound rate is 2.13/100 in 2026, 2.86 in 2025 and 2.57
in 2024. His team on/off capture difference changes sign across those seasons.
This audit does not adjust for size, role or who replaces him, so it neither
settles his for-size value nor overrides Adam's expectation. Do not fit a
teammate-facilitation coefficient from these three named cases.

## Feedback review: accepted concerns versus untested prescriptions

`MODEL_FEEDBACK_FROM_CLAUDE.md` is Adam's supplied review, left unchanged.
Useful points to retain:

- Limit rebounds by opportunities and model competition. Forward accuracy on
  conventional lineups cannot certify counterfactual means.
- The existing conditional point coefficients are not mechanistic event
  values. The conflicting checks above are the substantive result.
- A same-rig, same-cutoff, same-target head-to-head against the additive
  incumbent is still owed. Historical 0.285-versus-0.57 cross-rig comparisons
  are not a measured accuracy trade. Future comparison must refit the
  incumbent before each origin, not use its all-data ratings export.
- Shot-location adaptation and player-role response deserve explicit follow-up,
  but should not be conflated with this rebound experiment.

Important qualifications:

- `self_2p` / `self_3p` in `game_player_stats.py` mean the player's **overall**
  shooting percentages, not percentages on self-created shots. Reallocating
  shots to self-created attempts needs new measurements; those inputs do not
  already exist under these names.
- Current-data synthetic panels intentionally use latest observed profiles.
  They are not held-out accuracy estimates; no validation table is leaked by
  that choice. Keep this distinction explicit in panel labels.
- 100% is the physical capture bound; an observed-range tail is a support
  diagnostic, not a hard 35% cap or a reason to refuse an estimate.
- A finite shot total does not by itself establish fixed quotas for rim shots,
  a ball-handling threshold, or a particular spacing function. Those are
  structural hypotheses needing definition and tests, not automatically true
  implementations because their explanations sound basketball-like.
- Composition-assigned load has useful within-player associations, but a
  causal/instrumental interpretation still needs identification assumptions.

## Third experiment: miss-conditioned capture (specified before its results)

Build player rebound-capture profiles from **live opportunities**, using only
prior games, and predict a bounded team capture probability with diminishing
returns to overlapping rebounders. Couple it to projected misses and the
usage budget consistently: extra ORBs create opportunities, and extra
opportunities can create misses. A perfect-shooting lineup must generate no
boards. Use a model of competition, not an asserted cap on points or a forced
five-center ranking.

Check direct future team capture rates and usage/FGA totals before translating
to points. Then rerun the existing isolated and named checks, including the
Adams/Robinson distinction as a diagnostic of the still-unmodeled teammate
facilitation. Preserve the conditional and shot-expectation controls and
re-estimate uncertainty for the changed mean. Do not expand into the full
shot-location/defense architecture before this bounded test has an answer.

Exact first specification: each player's EB-shrunk own capture rate is
`p = own ORB / (on-court team ORB + opponent DRB)`, from the same season/history
window as his shooting profile. Set `h = p/(1-p)` and `H = sum(h)` for the five.
Team capture is `q = H/(H+C)`, with one opponent-strength parameter C fitted by
binomial likelihood on completed earlier lineup origins. This is a competing
strength assumption, not a fitted pair effect or an asserted 35% ceiling.
Capture improves with diminishing returns as H increases.

Let m be predicted missed FGA plus .44 missed FTA per usage event, scaled by
the prior league fraction of such misses that yield credited live rebound
chances. Let B be the prior non-rebound budget. Solve `U=B/(1-q*m)` and
`ORB=q*m*U`. Zero misses implies zero boards; individual projected credits
divide team ORB in proportion to h. Shooting value is literal expected points,
with the same prior-only assist-deficit calibration as the preceding run.

Compare against both the accepted conditional/fixed scorer and the failed
literal-shot/direct-rate ledger, with exact reproduction of their controls.
Report direct capture binomial loss, capture-rate error, ORB/usage/FGA errors,
point metrics, isolated +10% rebound-strength perturbations, perfect-shooting
and named panels. Intervals must include the new rebound-strength support tail
alongside assist deficit; they remain predictive diagnostics, not a complete
posterior for the additional capture parameters or synthetic lineups.

Additional descriptive same-four panel: Murray/White/Bridges/Gordon beside
Adams or Robinson; then Hart replaces Bridges beside Adams. These hypothetical
lineups retain a true guard and isolate the substitutions. No total ranking is
mandated. Report the individual shares as well as the team total. This model
still cannot infer an Adams box-out benefit to another player's capture skill.

## Third experiment results — 2026-09-05

The capture model is implemented and the full 2015–2026 run is complete.
Both existing controls reproduce their saved point metrics exactly. The new
per-possession DRB cache contains 2,047,768 credited defensive rebounds across
6,059,380 possessions, exactly matching the existing player-game total. No
source database rows or incumbent scoring defaults changed.

**Rebounding itself improves.** On latest states, live-chance capture MAE
falls from 5.646 to 4.425 percentage points versus a prior league-average
capture probability. Season-paired change is −1.22234 ± 0.09291 points;
binomial log loss improves in all 11 origins. Against the prior independent
ORB-rate sum, ORB-count MAE falls **2.383 → 2.252 per 100 possessions**;
season-paired change −0.13128 ± 0.02519, improving in 10/11 origins. Cumulative
state also improves ORB-count MAE (2.529 → 2.262).

**The point-accuracy trade is measured, not a promotion claim.** Latest state:

| arm | MAE, points/100 | raw r² | ordinary correlation |
|---|---:|---:|---:|
| accepted conditional/fixed | 7.4742 | +0.01389 | 0.20506 |
| failed literal-shot/direct-ORB | 7.5568 | −0.00622 | 0.18560 |
| literal-shot/capture-renewal | 7.5279 | +0.00060 | 0.19545 |

Capture versus accepted has season-paired MAE +0.04944 ± 0.06861 and raw r²
−0.01179 ± 0.01256. Versus the direct-ORB follow-up, MAE improves
−0.03143 ± 0.01621 and raw r² +0.00721 ± 0.00233. The cumulative-state
point loss is larger: MAE 7.7131 versus 7.4970, paired +0.21722 ± 0.08569.
Future FGA MAE worsens (latest paired +0.24939 ± 0.08175 versus accepted),
despite improved rebound prediction. Do not conflate winning the rebound
target with validating the entire opportunity/shot-assignment model.

**Independent coherence checks pass; full five-center coherence does not.**
Increasing rebound strength by 10% improves the calibrated point estimate in
all 5,774 tested season-lineup cells under each representation, and in every
named diagnostic. Perfect shooting generates zero live chances, zero rebounds
and no rebound-created usage. Player credits partition team rebounds, capture
is bounded, returns diminish, and lineup order has no effect.

Current latest-state five centers now project **19.58 ORB/100**, not 33.81;
five Goberts **16.23**, not 29.58. Their scoring means fall from the direct
arm's 125.06/124.55 to **117.64/117.24**. These are less extreme but still too
respectable to call the user's five-center offense expectation solved: the
2026 ordinary league offense in this database is 116.38. Jokić/Korver scores
122.10, Jokić/Westbrook 120.28, five guards 115.38 and five Jokićs 127.97.
Finishing efficiency and shot mix are still transported into unfamiliar
creation roles. Do not reintroduce a rebound penalty to fix that separate gap.

The two center diagnostics have capture probabilities 51.1% and 47.9%; both
exceed prior p99 rebound-strength support and are explicitly flagged. That is
not a refusal or an asserted mean cap. The competing-strength curve's tail is
a disclosed extrapolation, not validated by a high-level physical bound.

**Uncertainty remains diagnostic.** With the rebound-strength tail added to
assist-deficit support, latest-state raw future-half coverage is
50.73/80.50/95.23% at nominal 50/80/95. Tail 95% coverage is 94.57% across
103 distinct season-lineup cells. Cumulative tail coverage is only 90.76%
across 79 cells. These tails are not the same population as the earlier
assist-only tails. The new capture-parameter and player-state uncertainty are
not fully propagated; synthetic latent coverage is still unverified.

The same-four current panel predicts Adams 15.45 team ORB/100 and Robinson
15.73; Hart for Bridges beside Adams raises team ORB to 15.80. The direct
capture credits give Adams 9.99 and Robinson 10.39. This is not a learned
box-out advantage: the model only has direct capture strengths, and competition
can reduce teammates' individual credits. The actual-lineup residual audit
(`*_player_residuals.csv`) is descriptive, held-out evidence for investigating
unexplained team effects, not a fitted named-player correction.

That audit supplies a concrete lead: on supported 2026 Adams lineups, predicted
capture is 38.19% versus observed 43.67%, a +5.48-point residual. Robinson's
residual is +2.33 and Hart's +0.05. These cover respectively 47.5%, 37.8% and
64.3% of their offensive possessions. Adams's 2025 residual is also positive
(+7.45 points) but covers only 19.4% of his possessions. Small, selected,
overlapping lineup samples and unmodeled opponents/teammates prevent a causal
box-out interpretation. Do not convert these named residuals into bonuses.

**Decision and next work:** retain capture/renewal as a promising, independently
tested rebound component, not a replacement point scorer. Investigate its
remaining team-rebound residuals and the mismatch in shot opportunities before
promoting it. Then test how finisher-heavy lineups' shot mix, turnovers and
efficiency change when someone must create; the current transported rates are
not a solution. Preserve the three standards and both controls. Do not rerun
the completed experiment, tune C to the named cases, or restore the negative
conditional ORB value as a basketball explanation.

The current suite passes 107 database-free tests. New code:
`rebound_capture.py`, `rebound_capture_validation.py`,
`rebound_opportunities.py`, and `tests/test_rebound_capture.py`.

## Reproduce

From the repository root:

```bash
export BASKETBALL_PY=/Users/adam/miniconda3/envs/basketball25/bin/python
"$BASKETBALL_PY" -u -m experiments.rebound_budget_validation
"$BASKETBALL_PY" -u -m experiments.rebound_budget_validation \
  --valuation-mode shot_expectation --prefix experiments/cache/rebound_shot_value_2026
"$BASKETBALL_PY" -u -m experiments.rebound_player_audit
"$BASKETBALL_PY" -u -m experiments.rebound_capture_validation
"$BASKETBALL_PY" -u -m unittest discover -s tests
```

Results: `experiments/cache/rebound_budget_2026_*`,
`rebound_shot_value_2026_*`, `rebound_capture_2026_*`,
`rebound_player_audit_2026.csv`. Compressed detail
files preserve split-level inputs for interval checks; they are not independent
samples. The original scorer and fan-facing page are unchanged.
