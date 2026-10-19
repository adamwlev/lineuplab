# Day 5: separate reference-average player value from lineup context

Codex/Astra, 2026-09-13. Adam approved the direction in
`reports/joint_capability_v10_codex_review.md` and requested this implementation
plan for Sol. This document specifies the next experiment; it does not launch it.

## 1. Outcome, priorities, and authority

Determine whether additive's individual-value information can be combined with
the NN's interaction response more effectively than averaging their complete
forecasts. Deliver a completed matched forecast experiment, readable player/team
ledgers, basketball checks, numerical sensitivity, and an honest handoff.

First define the decomposition using saved models. Then run the fixed replacement
factorial below. **There are zero new neural or additive fits, zero epochs, and
no hyperparameter search in this plan.** The compute is batched inference and
numerical integration. This is an actual out-of-time forecast comparison on the
existing data, not merely an infrastructure exercise.

This deliberately replaces the earlier shorthand proposal to build a new
"cross-fitted, shrunk mean arm" immediately. We already have a prior-fitted,
regularized additive value arm. Test whether replacing the NN's reference-average
value component helps before fitting another one. The fixed half/full context
weights are the bounded shrinkage comparison; no new shrinkage selector is fit.
The decomposition is also different from Day3's nonlinear mean-*teammate pooling*.

Priorities:

1. Reproduce the existing controls and implement the defined projection.
2. Complete the matched replacement experiment and reference sensitivity.
3. Explain the changes on real failure cases and the basketball fixtures.
4. Complete finite-outcome interval diagnostics and the research handoff.

The three standards in `CONTEXTUAL_MODEL.md` remain co-equal. A small point-metric
loss can be an acceptable trade for better basketball coherence or uncertainty;
print the trade. Do not require a significant win to finish, and do not turn a
null result into an automatic larger search.

When Adam asks to implement: implement, test, reconcile saved controls, and run
the two bounded integration pilots in §6. Then provide verified background,
live-log and status commands and wait for Adam to launch or explicitly authorize
the full inference run. After it finishes, the automated pipeline must produce
the analysis outputs, followed by Sol's written review. No dangling secondary run.

### Boundaries

- No delegation, concurrent editing agent, scraping/network fetch, database
  access or mutation, input-cache rebuild, new model training, deployment,
  scorer promotion, staging, or commits. Establish sole editing ownership.
- Read frozen sources in place. No writes to completed run directories, changes
  to historical producer hashes, edits to original feedback, or revisions to this
  scientific protocol in response to its results. New work uses a new prefix.
- No player/pair ID parameters, chemistry lookup, synthetic outcome labels,
  forced Korver ranking, five-center multiplier, or new coverage gate.
- Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u`; numerical work,
  tests, pilots and the production run all need durable logs with exit status.
- Keep code small and specific. Do not build a general ensemble, training, or
  experiment-management framework. A substantial unrelated defect is a recorded
  blocker, not permission for a repair campaign.

## 2. Starting evidence and sources

Read AGENTS.md and its required context, then the independent v10 review and
this plan. Historical prose suggesting a proved neural ceiling, a proved
measurement-power bottleneck, or message-off being additive is not the contract.

Reuse:

- `experiments/cache/joint_capability_2026_09_09_v3/`: frozen
  `derived/game_lineups.npz`, `derived/player_game_states_v3.npz`, schedule
  provenance and fixture definitions.
- `experiments/cache/joint_capability_2026_09_12_v9/`: all 48 saved
  `origins/<tag>/V9_SPREAD/fit.pt`, calibrations, cells and predictions.
  Existing sidecar/rebound arrays may be read if the data adapter requires them;
  do not invoke builders or fetch missing data.
- `experiments/cache/asof_points_centered_2026/`: corrected additive scores,
  calibrations and centered reference definitions. Follow recorded provenance to
  existing `experiments/cache/asof_points_2026/` fit snapshots for player ledgers.
- `experiments/cache/joint_capability_2026_09_12_v10/`: verified matched controls,
  GLOBAL weights, completed basketball diagnostics and uncertainty conventions.
  TEAM_1 and the post-hoc half-TEAM_1 stay historical references, not new backbones.

Useful code: `joint_capability_v9_model.py`, v9 data/replay adapters,
`joint_capability_v3_diagnostics._origin_profiles`, `asof_additive_reference.py`,
`asof_point_calibration.py`, and pure helpers in `joint_capability_v10_analysis.py`.
The v10 report shows source replay, additive ledgers and fixtures. Do not call
its complete-report/initialization routines on an old prefix: some write reports
or manifests. Prefer explicit read-only loading and new thin adapters.

Primary population is **44 quarter origins, 2016–2026: 5,607 lineup-quarter
cells / 726,364 possessions**; novel fives are 2,073 cells / 226,256 possessions.
The four 2015 origins are warmup. Separately reproduce the full descriptive
48-origin population, 6,179 cells / 803,447 possessions. Do not regroup to annual
forecast cells. Season-paired inference aggregates quarterly errors by season.

| Primary forecast | MAE | RMSE | raw r2 | novel MAE | novel RMSE |
|---|---:|---:|---:|---:|---:|
| corrected additive A | 8.091953 | 10.840994 | .120432 | 8.903899 | 11.853019 |
| V9_SPREAD N | 8.140175 | 10.866667 | .116261 | 8.861940 | 11.772833 |
| HALF = (A+N)/2 | 8.072735 | 10.808119 | .125758 | 8.838646 | 11.766236 |
| prior-only GLOBAL | 8.070689 | 10.809699 | .125503 | 8.841767 | 11.773454 |

Reconcile keys, outcomes, exposures, novelty, cutoffs, league levels and exact
unrounded predictions before comparing new arms. Required cells cannot disappear
through an inner join. Saved ordinary N replay should agree within 1e-4 points/100;
document floating-point effects rather than silently widening that tolerance.

## 3. The decomposition: a reference-defined main effect, not intrinsic talent

Let N_t(x1,...,x5) be the **calibrated** saved V9_SPREAD offense forecast at
origin t, with its original budget, standardized message inputs, player states,
league reference and calibration. No recalibration is performed. It is symmetric
in the five raw player-state vectors, including repeated vectors.

Define a probability distribution q_t over individual player states available
at t. Draw five states independently, **with replacement**, from q_t. Define:

    mu_t    = E[N_t(Z1,Z2,Z3,Z4,Z5)]
    h_t(x)  = E[N_t(x,Z2,Z3,Z4,Z5)]
    u_t(x)  = h_t(x) - mu_t
    M_t(L)  = mu_t + sum_i u_t(x_i)
    C_t(L)  = N_t(L) - M_t(L)

M is the additive main-effect projection under the declared product measure.
In exact integration E_q[u]=0, E[C]=0 and E[C | Z_i=x]=0. C contains all
remaining nonlinear interactions, including finite-budget competition; it is
**not** the message-on/off increment. Numerical estimates only approximate
orthogonality; the accounting identity N=M+C must hold exactly to tolerance.

Interpretation: u(x) is this frozen NN's expected change from inserting x into
a random reference four, relative to its reference mean. It includes x's
average facilitation effect, not just its own scoring. C is departure from that
average in this particular five. These are functional main effects/interactions,
not causal effects or uniquely identified basketball "talent" and "chemistry".

### 3.1 Freeze both reference distributions before evaluation

For each origin, use cached game-lineup rows whose dates satisfy
`t - 365 days <= date < t` and possessions > 0. Sum each player's offensive
on-floor possessions over those rows. Use the player's **origin-t** state, not
the state from each historical game. The donor set is all players with positive
exposure in that window. Do not require a minimum exposure or use future rosters.

- **EXPOSURE, primary:** q(pid) proportional to that prior exposure.
- **UNIFORM, mandatory sensitivity:** equal probability for each player in the
  exact same donor set. This tests dependence on common/high-minute players
  versus the broader recently active population; it is not a second model search.

Use the existing origin fallback for a missing state and record its weight;
never replace it with a later-season state. A truly empty donor population is a
hard input failure, not permission to invent a new reference. IDs only identify
source states. No ID is passed to the neural model. Identical state vectors may
be deduplicated computationally with their q weights summed.

Current injured/stale players are not manually excluded. Record state ages,
effective sample sizes, donor count, effective donor count 1/sum(q^2), fallback
mass and top donor weights. Historical-player transport uses a separately
identified state vector; never key its projection cache by player ID alone.

**Structural assumption:** independent draws break actual roster correlations
and can produce implausible teams. This gives a well-defined reference, not
evidence that those teams are supported by the data. Report sampled composition
distances and duplication frequency. Neither empirical real-lineup orthogonality
nor safe extrapolation follows from product-measure orthogonality. The two
references quantify one sensitivity, not an OOD confidence interval. No extra
reference bandwidth, position filter, or result-selected reference is allowed.

## 4. Numerical integration, with a variance-reducing additive control

Implement a small batched frozen-model evaluator and projection helper. Keep
outcomes entirely out of their APIs. The donor weights and states are finalized
before loading current evaluation outcomes. Requesting a projection for an outer
lineup's known players is allowed; its frequency or outcome cannot change q.

Use the origin's existing fallback raw state as anchor r. Define the purely
additive control function:

    b0       = N_t(r,r,r,r,r)
    b(x)     = N_t(x,r,r,r,r) - b0
    B(L)     = b0 + sum_i b(x_i)
    R(L)     = N_t(L) - B(L)
    b_bar    = sum_{x in donor set} q(x) * b(x)

B is only a numerical control variate; it does not define the scientific
decomposition or force a basketball reference prediction. In exact integration
subtracting and adding B leaves §3 unchanged. For an exactly additive toy N,
R is zero, eliminating Monte Carlo noise in that important control.

For each independent panel, sample K common quadruples from q^4 and evaluate:

    r_hat(x) = mean_k R(x, Z2_k, Z3_k, Z4_k, Z5_k)
    r_bar    = sum_{x in donor set} q(x) * r_hat(x)
    mu_hat   = b0 + 5*b_bar + r_bar
    u_hat(x) = b(x) - b_bar + r_hat(x) - r_bar

Compute r_hat on every donor state and every requested target state. The exact
weighted donor sum integrates the first slot and enforces sum_q u_hat=0 even
at finite K. Common quadruples reduce noise in player substitutions. C_hat=N-M_hat
always reconstructs N; its conditional centering remains approximate.

Use two independent panels, deterministic PCG64 seeds derived with SeedSequence
from `[20260913, origin_index, reference_index, panel_index]`; no Python hash.
Start at K=256 quadruples **per panel**, extend the same draws to 512 and then
1024 only according to the outcome-blind agreement screen below. No further
automatic extension. The final estimate averages the two panels' mu and u.
Persist each panel separately so Monte Carlo sensitivity can be measured.

Agreement probes: up to 64 highest-exposure distinct real fives in the prior
365-day window (ties by sorted IDs), 256 independently sampled product-reference
fives, and predeclared fixtures available without post-t roster/exposure selection.
Keep the historical report's highest-exposure outer-quarter fixture out of this
adaptive screen; it remains in the final basketball report. Probe sampling uses a
separate fixed seed stream; no evaluation outcomes or error-selected cases.
Screen the difference between the two panels' M predictions: unweighted probe
RMS <= .05 and maximum absolute difference <= .25 points/100. These are numerical
agreement thresholds, **not estimated confidence bounds**. Reuse probe identities
at every K. Stop at the first passing K, or at K=1024 with
`integration_limited=true`; retain the forecasts and disclose the limitation.

Evaluate both panels separately on the final population as a numerical audit.
If any primary new-arm pooled MAE or RMSE differs between panels by > .005,
flag fine predictive distinctions as numerically unresolved. Do not increase K
or choose a panel after seeing these outcomes. A capped/unresolved result is a
valid handoff, not an invitation to keep running until a desired answer appears.

Batch inference; do not materialize all state-by-context tensors simultaneously.
Use inference mode, deterministic CPU execution and the source model's precision
for ordinary replay. Use float64 accumulation for expectations and weights.
Sample draws, state hashes, panel estimates and completed-origin receipts must
be resumable. On the independent 256-fives probe, report the sampled residual mean.
Also hold each of the 16 highest-q donor states fixed against 64 independent fours
and report sampled conditional residual means (fixed separate seed streams, no
adaptive extension). These are noisy integration diagnostics, not pass/fail proof
of exact finite-sample orthogonality.

## 5. The fixed experiment: replace value, release context

For each reference define:

    F(beta,gamma) = (1-beta)*A + beta*M + gamma*C

All terms are calibrated points/100. No fitted intercept, new point calibration,
clipping, outcome-tuned weight, or constraint-based rating repair is added.

| Arm | beta | gamma | What it tests |
|---|---:|---:|---|
| A, saved control | 0 | 0 | corrected additive |
| N, saved control | 1 | 1 | frozen neural forecast, reconstructs M+C |
| M_ONLY, diagnostic | 1 | 0 | neural reference-average main effects alone |
| HALF, saved control | .5 | .5 | ordinary half blend, reconstructs exactly |
| VALUE_SWAP | 0 | .5 | replace neural mean, hold half-context fixed |
| CONTEXT_RELEASE | .5 | 1 | keep half-blended mean, retain full NN context |
| FULL_SWAP | 0 | 1 | additive value plus full NN interaction residual |

The last four rows form a fixed 2x2 experiment on beta in {0,.5}, gamma in
{.5,1}. HALF is the unchanged reference. Run all rows for both EXPOSURE and
UNIFORM; never select the reference based on forecast errors. Saved GLOBAL is
an additional benchmark, not a new tuning exercise. Its weights must still be
verified as based only on completed windows with stop <= the next origin start.

Primary scientific contrast: **VALUE_SWAP minus HALF on recurring-lineup RMSE**.
This isolates value replacement at unchanged context weight, motivated by the
consistent recurring NN disadvantage. Mandatory accompanying readouts: all/novel
MAE, RMSE, raw r2 and bias; basketball totals; uncertainty. One statistical primary
does not demote the other product standards.

Secondary fixed contrasts: CONTEXT_RELEASE−HALF (context amplitude),
FULL_SWAP−VALUE_SWAP (context amplitude after value replacement),
FULL_SWAP−CONTEXT_RELEASE (value after context release), N−M_ONLY,
and every new arm against A and N. Report EXPOSURE−UNIFORM changes for the same
arms. Reference sensitivity is a modeling-assumption test, not an ensemble.

These arms do not introduce new event predictions. The NN decoder's events remain
unchanged. Express the final hybrid ledger as:

    hybrid = N + (1-beta)*(A-M) + (gamma-1)*C

Call the last two terms **reference-value replacement** and **interaction
rescaling**, not learned shooting, spacing, or rebound points. Do not modify
event probabilities to make an unmodeled point residual look mechanistic.

## 6. Implementation order and bounded launch

Use new files, for example `joint_capability_v11_projection.py`,
`joint_capability_v11_run.py`, `joint_capability_v11_report.py`, and focused tests.
Use `experiments/cache/joint_capability_<date>_v11/` for a fresh production prefix;
put smoke/pilot work under separate prefixes. Do not alter frozen producers.

Before the full run:

1. Record status, source hashes and required local files. Reconcile A/N/HALF/GLOBAL
   across all origins with the saved tables; this is cheap and may run immediately.
2. Implement and test the projection plus exact accounting. Keep the outcome-blind
   projection stage separate from metric calculation in code and on disk.
3. Run integration pilots only at **2016q1 and 2026q4**, both references, starting
   K=256 and applying the same bounded agreement rule. Pilots validate replay,
   runtime, memory and numerical behavior, not arm selection on outer error.
4. Freeze a protocol/source manifest, expected outputs and input checksums before
   production. A matching completed pilot may be reused; otherwise preserve it
   and recompute in production. Record exactly which happened.
5. Give Adam measured runtime per panel/origin and a total estimate at the initial
   and maximum K. Full bounds: **48 origins x 2 references, two panels each,
   K<=1024 per panel, zero optimizer fits**. Print actual unique-state counts and
   estimated forward evaluations; do not call this a tiny run without timing it.
6. Provide and verify launch/live-log/status commands. Do not launch the full
   inference job until Adam asks. Once authorized, complete both references and
   all secondary analyses automatically without another manual training command.

If projection assumptions cannot be implemented faithfully with frozen inputs,
stop and report the exact mismatch. Do not substitute message-off, fit an
unregistered empirical ridge projection, drop difficult players, or retrain N.

The runner must provide a dry-run/preflight, resume, and status path that never
builds missing inputs. Resume compares existing fingerprints and refuses a
mismatch; it must not overwrite the manifest to make it match. Write outputs
atomically and mark origin completion only after its files validate. A failure
must exit nonzero and retain a traceback. A report is complete only after both
references, all required origins and all analyses have passed completeness checks.

Durable log per origin/reference/panel: cutoff, prior row/date range, donor/fallback
counts, K, evaluated states and forwards, elapsed time, agreement errors, limited
flag, and completion. After each origin, log current and cumulative **primary**
A/N/HALF/GLOBAL/VALUE_SWAP/CONTEXT_RELEASE/FULL_SWAP comparisons, with counts and
MAE/RMSE/r2 deltas. Print warmup separately. Zero qualifying rows is `N/A (0 cells)`,
not zero error; degenerate r2 is explicitly undefined. Distinguish references.
Use a PID/status receipt and command line, not process-name grep alone. Log the
automatic start/completion of basketball, intervals and final reports. Keep test
and pilot logs as well; shell pipelines must preserve the Python exit status.

## 7. Required derived analysis

### 7.1 Prediction and decomposition

Produce primary and descriptive scorecards, origin rows and season rows, all/
novel/recurring and the existing exposure bins. Metrics are possession weighted
within each cohort. For every fixed contrast, use the existing equal-season
paired differences, nominal t95 intervals and favorable-season counts. Do not
substitute cell-IID standard errors. Reused historical years, multiple contrasts
and overlapping training histories preclude claims of fresh confirmation.

For every origin/reference save mu, centered per-state u, q, calibration,
state-source dates and hashes, plus per-cell A/N/M/C/all forecasts and numerical
panel alternatives. Report weighted means, sd and correlations of A, M, C and
A−M on **real** cells; real-cell C need not have mean zero. Do not subtract its
observed mean using current outcomes or future lineup frequencies.

For forecast changes decompose the exact squared-error difference using the
value-replacement and context-rescaling point terms above. For a move P→Q,
each contribution d_j receives `d_j*(P+Q-2*actual)`; contributions sum exactly
to squared-error change. This is arithmetic attribution, not causality.
Do not present a similarly linear identity for absolute error.

### 7.2 Real-lineup cases for Adam

Use primary cells with >=100 possessions, and keep the >=200 subset visible.
Choose up to eight largest weighted squared-error harms and eight benefits of
EXPOSURE VALUE_SWAP versus HALF. Print actual exposure and ORtg, origin, five
names, A/N/M/C, all four factorial totals and their numerical panel variation.
Include a reference-robustness column. These are post-hoc diagnostic cases, not
an additional evaluation population or training examples.

For each case show additive's centered per-player contribution and intercept,
NN u per player and mu, their value differences, and the team interaction term.
Verify sums with the source calibration and centering; do not allocate a team
intercept arbitrarily to players without labeling that convention. The interaction
residual stays a team term: do not invent a pair attribution. Include the frozen
NN's actual usage, mix and make predictions separately when useful for reasoning.
A case ledger must explain how the prediction was obtained, not just rank errors.

### 7.3 Basketball checks: totals and mechanisms, separately

Reuse the frozen panel: conventional real reference; limited centers; five
Goberts and one-through-five Gobert ladder; five Jokics; Jokić/Korver/Westbrook
with Jamal Murray; existing real small-ball/guard fixtures where defined. Do not
choose new named fixtures after observing a surprising result. Print missing
coverage, including unmodeled defense, rather than silently calling it a pass.

For both references compare A/N/HALF/GLOBAL and every new fixed arm. Report full
ORtg, M/C, message-on/off increment in clearly labeled native units, hybrid
adjustment in calibrated units, role/opportunity changes from the unchanged NN,
composition distance, numerical uncertainty and reference spread. Five Goberts
having a negative context term is insufficient if the final offense is ordinary.
Do not require monotonic clone penalties or invent a numeric acceptable ORtg after
seeing the outputs; describe strengths/failures against the pre-existing checks.

For Korver/Westbrook distinguish total ranking, difference relative to A, projected
C difference, and message increment difference. Adam explicitly allows the data
to refute his original intuition. A main effect includes average facilitation,
so these are genuinely different questions. Preserve contradictory findings.

Historical Korver's injected player-state vector is not the same value assumption
as the old additive fixture's current/stale coefficient. Preserve that case but
label additive/hybrid comparisons **unmatched player vintage, diagnostic only**.
Project the historical state against the unchanged origin reference with a distinct
state hash. Do not silently call this a fair player-season comparison or build a
new historical additive scorer. Current-state fixtures remain matched.

### 7.4 Uncertainty

Apply the existing v10 finite-batch interval method with identical residual-history
cutoffs, calibration populations, fallback and support bins to all fixed arms and
both references. Verify any quantile used at t consumes only forecast residuals
from completed windows with stop<=t. Report 80/95% coverage, width and counts by
novelty, exposure and existing composition-distance bins; separate warmup/fallback.
No new interval tuning or distance curve is fit in this experiment.

Separate three different uncertainties: finite future-outcome dispersion;
Monte Carlo integration error; reference-definition sensitivity. None validates
the arbitrary-lineup latent-mean interval. Do not turn panel disagreement or
EXPOSURE/UNIFORM spread into a claimed calibrated epistemic band. Keep the latent-
mean/OOD product requirement open. No expensive game bootstrap or expanded-cell
benchmark is required today.

## 8. Focused verification and completion artifacts

Tests must cover:

- Exact tiny-support enumeration of constant, additive, and known symmetric pair
  toy functions: expectation, main effects, interaction residual, and conditional
  orthogonality; Monte Carlo approximation agrees with exact enumeration.
- Additive control-variate cancellation, nonuniform weights, duplicate-state
  coalescing, held-out target states and the historical/current state-key distinction.
- Strict prior reference dates and origin states, missing-state fallback, future
  outcome mutation not changing projections/forecasts, and prior-only interval/GLOBAL
  history. No synthetic actual outcomes enter the integrator.
- N=M+C, HALF reconstruction under both references and panels, hybrid ledger and
  squared-error identity, centered q-weighted u; permutation invariance including
  repeated players. Use explicit float32 replay vs float64 accounting tolerances.
- Batch-size invariance to documented tolerance, deterministic extension/restart,
  source-manifest mismatch refusal, absent files, duplicate/missing forecast keys,
  empty/constant-target metric cohorts and accurate nonzero failure exits.

Run the focused tests first and the full existing suite at completion with a
durable log. The last verified suite was 743 tests; test count is not the research
deliverable. Do not edit old scientific files to solve unrelated suite failures.

New prefix must contain a frozen protocol/source manifest, input receipts,
reference/state tables, sampled-index seeds/receipts, both projection panels,
per-origin completion/numerical diagnostics, joined forecasts and keys, scorecards,
season contrasts, real case/player ledgers, basketball panel, interval readouts,
and machine-readable overall status. Avoid committing giant forward tensors;
retain small sufficient quantities to reproduce the projection and verify hashes.

Write outside the completed prefix:

- `reports/joint_capability_v11_review.md`: results, quantitative contrasts,
  reference/numerical robustness, basketball totals, all three standards and a
  recommendation with limitations. Do not just say "best MAE".
- `reports/joint_capability_v11_handoff.md`: exact commands, prefixes, source
  hashes, verified completed counts, runtimes/forward counts, logs/test exit status,
  outstanding work, git status, and whether anything is running. Explicitly say
  zero new optimizer fits and no scorer promotion.
- Update the top of SESSION_HANDOFF.md and concise roadmap/backlog/scorecard
  pointers after the results. Preserve older entries, reviews and plans.

Before launch, provide a short operational checkpoint with the verified commands;
after completion, do not leave it as the final handoff. Never overwrite a reviewed
editorial report with a generated stub on resume. No commit is authorized by this
implementation plan; leave the exact change list for review.

## 9. Decision rules and what remains next

The answer may be positive, null, negative, or numerically unresolved. It is useful
provided the controls, populations and decomposition are trustworthy.

- If VALUE_SWAP improves recurring prediction consistently across both references
  without a concerning novel/coherence/uncertainty trade, explicit value separation
  earns a follow-up design discussion. It does not prove C is causal complementarity.
- If CONTEXT_RELEASE helps basketball behavior but costs prediction, quantify that
  trade instead of automatically rejecting it. If it worsens plausible totals,
  retaining more context is not intrinsically better.
- If gains are reference-sensitive or smaller than numerical variation, say so.
  Do not select a reference, seed or K based on the resulting leaderboard.
- If none improves on HALF, keep the fixed blend as the pragmatic research
  benchmark. This rejects these frozen recombinations, not every possible jointly
  trained value/context architecture. A trainable residual/value arm would require
  a separate pre-registration and a clearly diagnosed failure this one exposes.
- Never infer that better predictive scores alone complete the product. Review
  final counterfactual totals and explicitly leave latent-mean uncertainty open.

After this bounded decision, **actual opposing-five/defensive modeling** remains
the strongest distinct next step toward the two-team product. Adaptive role states,
dated creation/finishing information, rebound renewal/facilitation, and calibrated
latent-mean uncertainty remain separate open directions. Do not implement those,
repeat team-loss dose tuning, or open another architecture sweep within this plan.
