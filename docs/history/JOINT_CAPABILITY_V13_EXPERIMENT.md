# v13: value integration, creation constraints, and richer teammate structure

Codex, 2026-09-14. Written before v13 pilots or outer results. Adam explicitly
authorized a large multi-ablation run, implemented by Codex without delegation.
Full training is to be launched by Adam from the supplied script.

## Scientific question and fixed scope

v12's F-B residual can reverse the meaning of learned messages. On the saved
latest fixture, messages lower five-Gobert F by 9.23 but B by 17.00, so C rises
7.77. On 33 primary quarters its flexible model trails HALF and loses the old
NN's novel advantage. This is grounds to investigate the interface, not abandon
contextual models. Read `reports/joint_capability_v12_partial_codex_review.md`.

Twenty trajectories, 48 quarterly origins each, inner selection and reset/full
refit: 960 arm-origins, 1,920 fits. Two trajectories are seed replications;
18 are distinct designs. No result-dependent addition/removal of arms, tuning
grid, extra epochs or automatic promotion. Original artifacts stay unchanged.
This campaign is exploratory development on repeatedly used years, not fresh
confirmation. Prediction, coherent counterfactuals and honest uncertainty have
equal standing. No known-pair chemistry or named-player penalties.

## Arms and planned contrasts

F is the complete event decoder, F_off uses the SAME trained decoder with
learned teammate messages disabled. Its shared-budget interactions remain.
A is the existing causal, calibrated additive forecast. b is a scalar trained
in points-per-possession units and printed as 100*b points/100. No anchor B.

| arm | forecast before rolling calibration | objective | change / comparator |
|---|---|---|---|
| E_BASE | F | event | new optimization control for saved V9 |
| J_BASE | F | event + team | matched joint-training control / E_BASE |
| B_BASE | .5*(A+F)+100*b | event + team | train the entire blend / J_BASE |
| R_BASE | A+F-F_off+100*b | event + team | intervention residual, not ANOVA / B_BASE |
| B_POINT | .5*(A+F)+100*b | team | importance of event supervision / B_BASE |
| J_SELF | F | event + team | extra individual profile correction inside decoder / J_BASE |
| J_COV | F | event + team | leave-one-out cross-capability covariance / J_BASE |
| J_ATTN | F | event + team | receiver-dependent attention over the other four / J_BASE |
| J_SUPPLY | F | event + team | assisted creation supply constraint / J_BASE |
| J_LOAD | F | event + team | assigned load versus own expected event rate / J_BASE |
| J_SUPPLY_LOAD | F | event + team | joint creation and load constraints / each single |
| E_SUPPLY_LOAD | F | event | objective contrast / J_SUPPLY_LOAD and E_BASE |
| B_SUPPLY_LOAD | .5*(A+F)+100*b | event + team | whole blend + constraints / B_BASE |
| R_SUPPLY_LOAD | A+F-F_off+100*b | event + team | residual + constraints / R_BASE |
| J_ATTN_SUPPLY_LOAD | F | event + team | attention with constraints / J_SUPPLY_LOAD |
| J_ROLE | F | event + team | dated recent/long and prior teammate role features / J_BASE |
| J_ROLE_SUPPLY_LOAD | F | event + team | role-conditioned constraints / J_ROLE, J_SUPPLY_LOAD |
| J_DROPOUT | F | event + team | 10% hidden-unit dropout / J_BASE |
| J_BASE_S23 | F | event + team | seed 23 replication of J_BASE |
| J_SUPPLY_LOAD_S23 | F | event + team | seed 23 replication of J_SUPPLY_LOAD |

All others use seed17. Optional layers use a separate seeded RNG so base weights
match. Extra output layers start zero. No width/depth sweep. Attention is one
round, 16-dimensional query/key/value and an 18-dimensional zero output head;
it supplements mean+SD rather than confounding removal of that summary.
Covariance adds the 153 off-diagonal entries of each receiver's four-teammate
18-state covariance, projected to the existing 32 hidden units with zero weights.
SELF is an 18->32 tanh->18 individual correction before decoding; FT conversion
may change through this individual head but not through teammate messages.
ROLE is the cached eight recent-minus-long and historical teammate coordinates
(x[55:63]), standardized on the training prefix. A 26->32->18 head reads own
current state and role features and contributes to the teammate message.

## Creation and load mechanisms (explicit structural assumptions)

Use pregame/as-of base log-assist as potential assist supply. Preliminary decoder
expected assisted makes are demand. Each player's shortage is the positive
maximum of log(team assisted-make demand / team assist supply) and log(their
own assisted-make demand / other-four assist supply), clipped at 4. This proxy
is observational, not measured potential assists or tracking-based creation.

SUPPLY subtracts k_supply * shortage * predicted assisted share from the six FG
make logits. A separate k_ft reduces FTA by exp(-k_ft*shortage); the removed .44
usage units are transferred to turnovers, conserving the event budget. That
transfer represents failed opportunity creation, an assumption to evaluate on
turnovers/FT labels. It does not impose synthetic target scores.

LOAD subtracts a nonnegative per-location coefficient times
max(log(allocated FGA+.44FTA+TOV / exp(base logFGA)+.44exp(base logFTA)+exp(base logTOV)),0),
clipped at4, from FG conversion logits. This revisits load under a new objective
and its interaction with creation supply, not as a claim that v7 never tested
overload. Role-assisted variation and single-factor controls distinguish it.

Coefficients are initialized zero and projected onto [0,4] after Adam updates.
Thus all constraints nest at baseline initially and can be rejected by data.
They retain the exact points=sum(FG makes*value)+FT makes identity. FT conversion
never depends on teammates. For R arms, F_off disables learned messages but
retains these explicit constraints; the intervention is labeled accordingly.

## Inputs, splits, objectives and stopping

Use existing frozen V3 grouped rows/states, V9 sidecars/rebound labels and V10
controls. No scraping, database access, input-cache rebuilding or deployment.
Recompute only fit-local moments and new model outputs. Causal additive offsets
are the verified v12 replay, checked by hashes and reconciled on saved cells.
Before 2015, A is missing: retain event supervision and omit team supervision
for ALL arms there, preserving a matched eligible team population. B_POINT
uses event supervision only for an entirely no-A warmup fit. No missing-A
row is silently dropped from the other arms' event objective.

Same five-year lookback and 730-day decay, whole-game batches, shared V9 untrained
event normalizers and shared seed17 native team MSE denominator on eligible
training rows. For ROLE, use the existing prefix x mean/scale, not whole-data
moments. Team loss is weighted MSE in points/possession; each batch uses its
contribution to the global training denominator. Event weight=1 (0 B_POINT),
team weight=1 (0 E arms), network/decoder penalties .01, Adam .001, weight decay
.0001, gradient clip5. No decay on scalar b or projected mechanism coefficients.

96 maximum epochs, patience8, min_delta1e-5 on inner event+team composite with
the ARM'S stated event/team weights, excluding regularization. Exact best epoch
is distinct from the patience threshold. All arms use this larger shared budget
to permit slower extra modules to learn; report caps instead of extending them.
Use the preceding quarter for inner validation, never the outer quarter.
Reset and fit the full prefix for exactly the selected epochs, with new prefix
moments and denominator. Do not initialize inner fits from outer checkpoints.

Primary point forecasts use the SAME prior-completed-quarter affine calibration
procedure for every new arm. Calibration uses that arm's saved H and past outcomes
only, dates checked, never current outcomes. Report raw H alongside calibrated
prediction; event outputs reconstruct F, and H/readout/calibration differences
are separate ledgers. This explicitly tests whether v12's lack of calibration
contributed to its gap, without a result-selected rescue transform. Saved
A/V9/HALF/GLOBAL remain exact controls; also print a predeclared half(A+new
calibrated native forecast) for every arm as secondary, not a selected winner.

## Readouts and decision policy

Primary: 2016--2026, 44 quarter-origin common populations, with 2015 descriptive
warmup. Exact keys/exposure/outcomes/novelty must match saved controls. Print MAE,
RMSE, raw R2, bias; all/novel/recurring, season, era, exposure, composition and
player-history support. Compare every arm against HALF and its table comparator.
Export equal-season differences, t95 and favorable counts. Eighteen designs
create multiplicity: nominal intervals rank hypotheses but do not prove the
best observed arm generalizes. No automatic selection/promotion. Use two fixed
seed replications to check fragility of the control and principal mechanism.

Save per-player FGA/FTA/TOV, six location/make probabilities, FT conversion,
assisted demand, shortage, load, point contributions, F/F_off/H/b and calibration.
Fixtures: current conventional unit, clone ladder, five Goberts/Jokics, limited
centers, guards, Jokic/Murray/Korver and Westbrook, separate historical Korver
injection. Native and final predictions both matter; no forced named rankings.
Diagnostics turn off messages and constraints separately at the saved fits.
Largest possession-weighted squared-error harms/benefits vs HALF at >=100 and
>=200 possessions, exact point ledgers and event families are automatic.

Prior-only 80/95 finite-outcome intervals: reuse corrected procedure, nullable
boolean coverage and weighted/unweighted widths across support slices. MC-dropout
16 passes on the latest fixture panel and seed-pair disagreement are sensitivity
diagnostics only, not validated latent-mean credible intervals. A synthetic
center lineup cannot calibrate its own uncertainty. No coverage gate.

## Synthesis of delayed work

- Actual opponent fives/tracking: grouped caches do not contain aligned opposing
  fives. Cached past-defense exposure is a different estimand; V5 already tested
  it. Defer actual matchup input alignment to a separately authorized data task.
- Rebounding: existing per-miss labels do not by themselves settle an offensive
  rebound/extra-opportunity loop with defensive competition. Do not bolt a free
  ORB bonus onto this campaign; the fixed budget remains explicitly approximate.
- Adaptive states/injury/era: use all existing dated contrasts in ROLE; no claim
  of new change-point states, tracking or fresh scrape. Era slices stay explicit.
- Learned individual value: SELF moves it upstream into the event decoder. This
  differs from discarding B after decoding. B/R contrasts test other interfaces.
- Rich interactions: covariance and receiver-dependent attention address what
  mean/SD misses; they are not another arbitrary larger MLP or message round.
- Uncertainty: finite-outcome calibration and fixed dropout/seed diagnostics are
  included; full latent uncertainty and withheld-role validation remain open.

## Operations and verification

Pilot every arm for one epoch on bounded real batches, then full inner/final
pilots for E_BASE, B_BASE and J_SUPPLY_LOAD at 2016q1, plus J_SUPPLY_LOAD at
2026q4. Test algebra, permutation/clone behavior, zero nesting, gradients and
causal invariance. Exercise resume without training and corrupted receipts.
Preserve failed attempts and use new prefixes after producer corrections.
Pilot outcomes cannot change registered arms or losses.

Single durable background command includes all fits and automatic analyses.
Save each inner and final fit independently before reporting checks; resumed
processes reuse completed phases. A real lock protects process metadata and
logs. Each phase receipt hashes its outputs; full CRC validation for gzip.
Atomic status RUNNING/PAUSED/FAILED/TRAINED/ANALYSIS_COMPLETE, wrapper PID/start/
command/exit, append-only logs. Failures print the precise origin, phase and
exception. No filesystem fingerprint mismatch is silently accepted. Do not
retrain complete fits to fix a report; derive corrected reports under a new
prefix with explicit producer provenance.

Record imported scientific modules and actual consumed inputs, versions, seeds,
dirty baseline, fit wall time, best epochs, gradient norms and cap hits. Give
Adam a measured ETA, launch/live/status/resume commands. Do not launch full
training until asked. No commit or delegation in this task.
