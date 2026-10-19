# Independent v5–v9 review and next-work decision

Codex/Astra, 2026-09-12. Read-only review of the completed Opus sprint, followed
by Adam's request for a synthesized implementation plan for Sol. No new model
training, database access, scraping, or scorer change was performed in this
review. The implementation contract is `SOL_JOINT_CAPABILITY_DAY4_PLAN.md`.

## What carries forward

The original project direction survives: dated player capabilities, learned
receiver-dependent teammate responses, finite offensive opportunities, explicit
event accounting, and no known-pair chemistry. This is not a generic graph NN.

V8's standardized message inputs and v9's mean+sd summary are the clearest new
positive findings. Recomputing saved event-loss receipts across 48 origins:

| Contrast | Mean event-loss change | Origin SEM | Favorable origins |
|---|---:|---:|---:|
| V8_STD − V8_BASE | -0.0004123032 | 0.0000368150 | 47/48 |
| V9_SPREAD − V9_BASE | -0.0002459919 | 0.0000160746 | 45/48 |
| V9_SPREAD − V8_BASE | -0.0006582951 | 0.0000340211 | 48/48 |

Each favors the intervention in 12/12 season aggregates. Origin SEM is a
descriptive readout, not an independence claim; use season-paired inference.
These are held-out event losses, not just better fit to training outcomes.

V5's particular richer-input/objective arms did not establish point gains. V6
and v7 improve understanding of composition transport and model sensitivity,
but observed-support withholding is not ground truth for impossible lineups.
V8's common event normalizers correct a genuine cross-arm measurement problem.
V9's variety summary adds useful information cheaply. Additional depth/rank
and minmax do not currently justify displacing the simpler spread backbone.

The commit sequence, complete origin grids, durable artifacts, shared controls,
and explicit negative results are valuable research progress. Keep the
efficient complete-run workflow; do not substitute a long infrastructure phase.

## Apples-to-apples point comparison

Recomputed from saved cell predictions. Primary is the original 2016–2026
sample: 44 origins, 5,607 cells, 726,364 possessions; novel 2,073 cells and
226,256 possessions. Lower MAE/RMSE is better.

| Model | MAE | RMSE | Raw r² | Novel MAE | Novel RMSE |
|---|---:|---:|---:|---:|---:|
| corrected additive | 8.091953 | 10.840994 | .120432 | 8.903899 | 11.853019 |
| v4 E0M_L2 | 8.122390 | 10.879681 | .114143 | 8.857444 | 11.799056 |
| v4 E1P_L2 | 8.109631 | 10.859141 | .117485 | 8.872391 | 11.780787 |
| V8_BASE | 8.120347 | 10.878602 | .114319 | 8.853928 | 11.796550 |
| V9_SPREAD | 8.140175 | 10.866667 | .116261 | 8.861940 | 11.772833 |
| V9_ALL | 8.130058 | 10.854637 | .118217 | 8.871667 | 11.768008 |
| HALF additive / V9_SPREAD | 8.072735 | 10.808119 | .125758 | 8.838646 | 11.766236 |
| HALF additive / V9_ALL | 8.066906 | 10.801115 | .126891 | 8.844054 | 11.763034 |

Equal-season paired MAE differences, primary sample:

- V9_ALL − additive overall: +0.033694 ± 0.042878 SEM; 5/11 favorable.
- V9_ALL − additive novel: -0.033771 ± 0.057675; 8/11 favorable.
- HALF(V9_ALL) − additive overall: -0.025935 ± 0.019233.
- HALF(V9_ALL) − additive novel: -0.060477 ± 0.028572.

These are promising point estimates, not a decisive overall superiority result.
The historical evaluation years have repeatedly informed development. A
prospectively specified next protocol does not make them untouched data again.

Including 2015 produces the recent synthesis's different levels: 6,179 cells /
803,447 possessions; additive MAE 8.034311, V9_ALL 8.067978, HALF 8.006623.
Both descriptions are reproducible, but 2015 was calibration warmup in the v4
primary scorecard. Do not silently change the population when comparing versions.
Also, these qualifying lineup cells are only a subset of available possessions.

## Qualifications to the standing synthesis

1. No universal accuracy ceiling has been established. The old random-split
   interaction-budget estimates are not a bound on all future neural models.
   Highly correlated prediction errors can reflect shared outcome noise, not
   identical usable signal. The blend's improvement itself suggests some
   complementary errors. Failed tested variants do not close whole classes.
2. Event/point misalignment versus limited power remains unresolved. The weak
   relationship across 288 arm-origin changes cannot establish that resolution
   is the ONLY problem; those observations also share arms, games and origins.
   Allocation changes can leave team totals unchanged, or channel changes can
   cancel. Test the conversion to points directly before asserting the cause.
3. Common centering leaves loss unchanged. Verified on the saved V9_ALL cells:
   subtracting league from both y and prediction leaves MAE 8.0679775 and RMSE
   10.7770166 unchanged. Raw r² changes from .1411457 to .0533573 because its
   denominator changes. That is not lower-noise MAE. Existing comparisons are
   already paired; more independent outcomes may help, mere regrouping need not.
4. Recurring versus novel is a useful diagnostic, not causal identification.
   Additive may retain omitted individual-value information through free player
   effects. That is a hypothesis, not proof of memorization. No IDs in the NN
   does not remove coaching/lineup-selection confounding or inherited context
   in historical player states. Novel observed fives are not five pure centers.
5. V5 did not test actual opposing-five interactions; v8 row decay did not test
   role-state adaptation; v5's ORB coordinate did not test rebound facilitation
   or a possession-renewal loop. Keep these distinct in the backlog.
6. A mean-context model already permits A's effect on B to depend on C through
   a nonlinear receiver response to collective context. Mean and pair pooling
   at fixed width had equal parameter counts, not simply different capacity.
   Marginal sd adds direct dispersion information; minmax is not another
   second moment, and summary orthogonality alone is not a predictive result.

## Two bounded v9 defects verified in code and saved-model replay

`experiments/joint_capability_v9_run.py:104` disables only the first message
layer for its zero-message prediction. Depth-enabled arms retain message2.
In a fixed-seed synthetic replay at the saved 2026q4 fits, disabling the first
versus both rounds changed scores by up to ~1.04 points/100 for V9_DEPTH and
~1.40 for V9_ALL. These magnitudes are synthetic diagnostic results, not
observed evaluation loss changes. Ordinary saved forecasts remain unchanged.

`experiments/joint_capability_v9_model.py:154` permits contextual coordinates to
enter FT conversion through its rank-positive decoder. Holding a receiver
fixed while changing teammates in synthetic replay changed FT probability by
up to ~.00282 for V9_DECODER and ~.00228 for V9_ALL. BASE/SPREAD/DEPTH with
diagonal decoders had exactly zero change in that test. Masking message
coordinate 15 before a cross-coordinate decoder is insufficient for isolation.

Do not change old fits/results to conceal these findings. Correct the derived
all-message-off diagnostic under a fresh prefix. Use rank-zero V9_SPREAD as
the new backbone and test FT isolation after learning. No V9_ALL refit is
needed for the Day4 questions. Do not assert these bugs explain its predictive
results without an appropriate new experiment.

## Direction chosen

Day4 combines saved-artifact explanation and forward-only blending with a
small new training test: add a team-point squared loss to the existing event
objective through the SAME basketball decoder, at two frozen doses. It adds
no player IDs, free point head, or architecture block. It directly tests a
question not settled by v5's relative family weighting.

Retain prediction, basketball behavior and uncertainty side by side. A blend
can improve prediction while diluting useful counterfactual response; expose
that trade. Observed-lineup interval coverage does not establish latent-mean
uncertainty for hypothetical extremes. Product deployment/gates remain deferred.

The detailed contract prioritizes completion over another broad search and
records later routes: separate own value/context, dated tracking, actual
opponents, role-state adaptation, cross-capability summaries, OOD uncertainty,
and rebound/defense mechanisms. None is automatically launched by the roadmap.
