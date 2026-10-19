# v16 implementation conventions — before neural pilot forecasts

This supplements, not replaces, `JOINT_CAPABILITY_V16_PLAN.md` design 1.
No v16 neural pilot results informed these choices. Completed numerical audits
and feature-likelihood diagnostics are not neural model-selection experiments.

## Execution and arithmetic

Adam authorized exploring three simultaneous CPU fits. Use three independent
processes with one numerical thread each, unchanged CPU arithmetic and seeds.
Shared contexts complete before arm workers read them. A chronological completed-
origin barrier controls calibration and live comparisons. Pilots retain their
own provenance and are not silently copied into production (48 extra cases,
about 1.5% of the campaign). Production remains a separate launch action.

The capability optimizer changes solver, not estimand: at most 500 total
L-BFGS/Newton iterations with the original objective, gauge and both convergence
criteria. Counts/conversion/recovery reuse exact constrained factors across
32 score-perturbation solves. Location caches its exact sparse multinomial
Hessian blocks, using a Kronecker matrix only as a **preconditioner**. Every
location draw passes the original matrix-free Hessian's residual test. The
preconditioner is not a posterior covariance approximation or a new prior.
All older development outputs and failed fits remain untouched.

## Dated diagnostic descriptors

- Player support: preceding five years of on-floor possession exposure with
  730-day decay. Thin is at/below the tenth percentile of minimum player
  support across unique prior offensive fives. Stale means last seen more than
  365 days before origin; never-seen is separately disclosed. No score gate.
- Offensive, defensive and exact ten-player novelty use separate strictly
  prior membership sets. Future appearances or outcomes do not change labels
  at an earlier cutoff.
- Composition distance: RMS standardized displacement of mean/SD raw own-
  skill profiles from the dated prior unit distribution. Role distance uses
  the established eight recent/historical role-context coordinates. Opponent
  distance uses mean/SD defensive raw profiles. Reference exposures decay at
  365 days; the reference and profiles stop at the scoring origin. These are
  descriptive input distances, not identified coaching or role-change effects.
- The U2 variance feature is log1p of the trace of joint linear-link projections:
  mean own + four times mean teammate capability, and sum defensive capability.
  Each of eight bank/family fits supplies its own 32 joint draws. Summing these
  *descriptor* traces does not assert a cross-family joint posterior or combine
  interval widths. The learned variance model must earn calibration on later
  windows. Three-seed disagreement is measured after pooling the forecast.

## Uncertainty and explanations

The primary two-half split pairs adjacent date-sorted games and assigns one
to each half, choosing the first side to balance accumulated possessions.
Odd/even and first/second-date halves are separately labeled sensitivities.
All need eight games/100 possessions and at least four games per half.

Each completed half gets 200 whole-game bootstrap resamples. Its local variance
is shrunk with twenty effective prior games toward the previously completed
pairs' per-effective-game noise. That estimate may inform **later** model fits.
The scored quarter's joint log score uses only the earlier noise estimate divided
by its effective game count—never its own measured residual variance. The same
prequential noise rule applies to U2 penalty-validation quarters. No noise
history means the persistent model is unavailable, not the lineup prediction.

Hypothetical capability sensitivity uses the full scorer's input derivative,
projected onto the 32 shared joint GLM draws, at the exact prior-opponent mean.
It is explicitly a **linearized conditional input sensitivity**, separate from
seed variation, finite-game bands, persistent discrepancy and quadrature error.
Bank/family effects are not added into an asserted posterior point interval.
Nonlinear checks use draws 0 and 1 from every enabled bank/family for J_BOTH and
J_ALL_BOTH, seed17, on Jokić/Westbrook and five-Gobert fixtures. Discrepancies are
reported, not suppressed or used to select favorable draws. Shared identities
and shared reference weights preserve covariance in swaps and clones.

The existing limited-center fixture is retained. A separate currently supported
legal pure-center probe is Gobert/Adams/Robinson/Capela/Allen. The Cleveland
2016q2–q4 and Denver 2024q1–q4 repeated-error units are fixed from old reviews.
Low-support, debut and stale substitutions use deterministic IDs/support, not
current points. These use 2026q4. The archived bio table lacks the newest
players; select from the immutable matchup roster as well, disclosing an ID
when its human-readable name is unavailable. Missing bio names do not exclude
rookies. The machine-readable registry records IDs, cutoff and support.
The historical Korver injection preserves its explicit mixed-era assumption;
it does not silently transplant rebound, adjusted or defensive career states.
Each fixture also faces the three highest prior-exposure actual defensive
fives at that origin, selected without current outcomes. Both scoring
directions use the same model; repeated identities across hypothetical teams
are labeled, not presented as a physically possible observed matchup.

The average-opponent product keeps the *same* already-calibrated conditional
scoring function and integrates it over a shared dated reference; affine
calibration commutes with integration. No separate mean-mode calibration is
fitted to outer outcomes. All fixed fixtures use 4,096 references with exact
fallback; exact finite-reference values also measure the integration error.
The separate broad task retains its fixed three models, 512 references and
4,096-reference sensitivity on the first twenty lexicographic eligible cells.

Hypothetical U0 displays a declared 100-possession horizon; the fixed U1/U2
fixture models display eight independent effective games and a separate
persistent-discrepancy range. These are extrapolations from earlier real-lineup
errors, not validated synthetic true-mean coverage. Their point predictions are
never gated or silently bias-corrected. Model-intervention switch cases have no
own OOS forecast history, so no calibrated interval is asserted for them.
Split-covariance diagnostics use earlier-pair quartiles of date separation and
opponent-distance change. Bootstrap-measured noise from cold quarters can inform
later persistent-model fits; validation log scores always use their own earlier
noise forecasts. Unavailable predictive noise retains the cold strongest-penalty
rule instead of inspecting the validation quarter's sampling variance.

## Statistical accounting

Season-block metric intervals use 10,000 paired resamples. Nominal paired tests
use exact within-season model-label swaps (2^11 configurations for eleven
primary seasons). Holm covers every frozen named contrast, separately by
co-primary population, forecast view and outcome family; unfavorable contrasts
are not removed. Every seed and every quarter remains visible. Event NLL
averages across seeds are labeled as such, not confused with likelihood of
the ensemble's averaged event ledger. Centered error is descriptive only.

None of these checks proves causal player effects, arbitrary-lineup true-mean
coverage, or authorizes scorer promotion. Three product standards remain equal.

Alongside the frozen named-architecture family, print every new arm's paired
contrast against A+D, N+D, old HALF+D and archived MAIN_RB half in a separately
named retained-control family (all arms, no winner selection). Apply Holm within
each family/population/view/metric. The bounded average-mode task reports the
two fixed new models versus archived MAIN_RB, direct/half separately. These
reporting conventions are frozen before pilots; no extra training or tuning.
