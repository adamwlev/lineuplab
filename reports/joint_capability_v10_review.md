# Joint capability v10 review

Reviewed by Codex/Astra on 2026-09-13 after the frozen Day4 run completed.
Independent continuation review and qualifications:
`reports/joint_capability_v10_codex_review.md`.
The implementation contract is `SOL_JOINT_CAPABILITY_DAY4_PLAN.md`; the run is
`experiments/cache/joint_capability_2026_09_12_v10/`. This review separates
pre-registered outputs from post-run read-only analyses and keeps forward
prediction, basketball coherence, and honest uncertainty on equal footing.

## Bottom line

The experiment completed cleanly, and it answered its three questions.

1. **The event-to-points disconnect is real cancellation, not one broken event
   channel.** Relative to the old mean-only backbone, standardisation plus
   teammate spread improved squared point loss through volume, location, and
   conversion, but calibration gave much of the gain back. The mechanisms move
   points usefully while their aggregate ranking signal remains small.
2. **The additive and structural models contain complementary predictive
   information.** The pre-registered fixed half blend improves primary MAE from
   8.0920 additive / 8.1402 structural to **8.0727**, RMSE to **10.8081**, and
   raw r2 to **.12576**. The prior-only GLOBAL blend is virtually tied at
   8.0707 / 10.8097 / .12550. Against the structural backbone, the fixed blend's
   equal-season MAE interval excludes zero; against additive, the improvement is
   favorable but not established.
3. **Direct team-point supervision is not the missing objective.** `TEAM_1`
   slightly improves the native team-MSE target it directly sees and improves
   on the structural backbone, but does not reliably beat it and still trails
   additive. It worsens held-out event loss in all 11 primary seasons and
   changes contextual magnitudes. `TEAM_01` is worse. Neither arm should
   replace `V9_SPREAD`.

The most promising next experiment is a clean separation of **individual value**
from **contextual response**: a strictly prior-only, cross-fitted, shrunk
individual-value/mean arm combined with a zero-centred `V9_SPREAD` contextual
residual. This follows the blend's success without known-pair chemistry.

## Protocol and completion

- 48 quarterly origins, 2015q1–2026q4; 2015 is blend/calibration warmup.
- Primary inference: 44 origins, 2016–2026, 5,607 lineup-quarter cells and
  726,364 possessions; 2,073 novel-five cells and 226,256 possessions.
- Two new arms: `TEAM_01` (alpha .1) and `TEAM_1` (alpha 1), both exactly the
  rank-zero, one-round, standardised mean+sd `V9_SPREAD` architecture plus the
  fixed auxiliary loss.
- 96/96 new arm-origins, 192 optimizer fits, no failures, 2,572.4 seconds
  (42m52s). `TEAM_01` selected 4–22 epochs (median 9); `TEAM_1` selected 1–14
  (median 6.5). Neither touched the 48-epoch cap.
- Each origin used an inner validation quarter for epoch selection and then a
  fresh prefix refit for exactly that epoch count. The outer evaluation quarter
  was not used for stopping.

The production command and verbose log are preserved in run-local
`logs/production.command` and `logs/production.log`. `SUCCESS.json` was written
only after mandatory reports completed. Frozen plan/code hashes are in
`protocol.json` and `code_hashes.json`; immutable input hashes are in
`source_manifest.json`.

## Forward prediction

Primary pooled results (points per 100 possessions):

| model | all MAE | all RMSE | all raw r2 | novel MAE | novel RMSE | novel raw r2 |
|---|---:|---:|---:|---:|---:|---:|
| additive | 8.09195 | 10.84099 | .12043 | 8.90390 | 11.85302 | .10035 |
| `V9_SPREAD` (`BASE`) | 8.14017 | 10.86667 | .11626 | **8.86194** | **11.77283** | **.11248** |
| half(additive, BASE) | 8.07274 | **10.80812** | **.12576** | **8.83865** | **11.76624** | **.11348** |
| prior-only GLOBAL | **8.07069** | 10.80970 | .12550 | 8.84177 | 11.77345 | .11239 |
| `TEAM_01` | 8.15905 | 10.87372 | .11511 | 8.91756 | 11.82448 | .10468 |
| `TEAM_1` | 8.11221 | 10.84875 | .11917 | 8.88777 | 11.80225 | .10804 |

The fixed and fitted blends are effectively tied. GLOBAL's final weight on the
structural arm is 0.439 and remains within the frozen [0, 1] rule; the extra
freedom earns no practical advantage over half.

Season-paired `model - BASE` results make the uncertainty explicit:

| contrast | mean MAE delta | 95% t interval | favorable seasons |
|---|---:|---:|---:|
| additive - BASE | -0.04254 | [-0.13506, +0.04997] | 6/11 |
| half - BASE | **-0.06300** | **[-0.11798, -0.00803]** | 7/11 |
| GLOBAL - BASE | **-0.06465** | **[-0.12543, -0.00387]** | 7/11 |
| `TEAM_01` - BASE | +0.02162 | [-0.03781, +0.08105] | 6/11 |
| `TEAM_1` - BASE | -0.02619 | [-0.07605, +0.02367] | 8/11 |

Against additive directly, `TEAM_1` has mean season MAE delta +0.01635 with a
95% interval [-0.08369, +0.11640], favorable in 6/11 seasons. That is a tie at
the available resolution, not a predictive win.

The fixed blend's **RMSE** evidence against additive is stronger than its MAE
evidence: mean season RMSE delta -0.03285, 95% CI [-0.06466,-0.00103], 9/11
seasons favorable. On novel lineups the corresponding delta is -0.08939,
CI [-0.15632,-0.02247], 9/11 favorable. These are nominal historical intervals;
repeated model development on these years limits fresh-confirmation claims.

### Post-run blend follow-up

After seeing the results, we asked one narrow read-only question: what happens
if each new arm is blended with additive under the same fixed-half and prior-only
GLOBAL rules? This was not the frozen primary comparison and is labeled post hoc.

| constituent | blend | all MAE | all RMSE | raw r2 | novel MAE | season MAE delta vs additive (95% CI) |
|---|---|---:|---:|---:|---:|---:|
| `TEAM_01` | half | 8.07923 | 10.81287 | .12499 | 8.86094 | -0.01295 [-0.04884, +0.02294] |
| `TEAM_01` | GLOBAL | 8.07630 | 10.81426 | .12477 | 8.86136 | -0.01572 [-0.04522, +0.01377] |
| `TEAM_1` | half | **8.05677** | **10.80180** | **.12678** | 8.84645 | -0.03536 [-0.08087, +0.01016] |
| `TEAM_1` | GLOBAL | 8.05760 | 10.80505 | .12625 | 8.85301 | -0.03436 [-0.07389, +0.00517] |

The half-`TEAM_1` blend is the best pooled MAE observed on this exact primary
population. It is not a promotion result: the equal-season interval crosses
zero, it was examined after seeing the arm results, and its novel MAE is slightly
worse than half-BASE (8.84645 versus 8.83865). Machine-readable results are in
`reports/joint_capability_v10_followup_blends.csv`.

## What direct team supervision learned

On the grouped team target used by the auxiliary loss, BASE native MSE is
2025.088. `TEAM_01` reduces it by 0.359 and `TEAM_1` by 0.547: only 0.018% and
0.027%. Equal-season deltas are likewise small: -0.331 +/- 0.441 SEM for
`TEAM_01`, and -0.513 +/- 0.512 for `TEAM_1`.

That small direct gain has a clear cost on the untouched outer event objective:

| arm - BASE | mean season event-loss delta | SEM | favorable seasons |
|---|---:|---:|---:|
| `TEAM_01` | +0.000057 | 0.000010 | 1/11 |
| `TEAM_1` | +0.000629 | 0.000054 | 0/11 |

The stronger dose trades away event fidelity in every season to move the team
target by about half a squared point-per-100. The total MSE denominator contains
substantial outcome noise: its 0.027% change does not measure the fraction of
learnable signal recovered. The current results do not justify replacing BASE,
but neither this percentage nor a smaller context response closes the whole
class of team-supervised models.

## Where the old event improvements went

The exact four-block Shapley accounting reconstructs every native point change
and squared-loss change. For `V9_SPREAD - V8_BASE`, exposure-weighted primary
mean changes were:

| block | prediction change (pts/100) | squared-error contribution |
|---|---:|---:|
| team FGA/FTA volume | -0.10308 | -0.16778 |
| player allocation | +0.00688 | -0.00075 |
| shot location | +0.08473 | -0.14280 |
| conversion | +0.24270 | -0.16849 |
| affine calibration | -0.41934 | +0.22031 |

Correction at independent review: the earlier draft printed the
`V9_SPREAD - V9_BASE` numbers under this combined `V9_SPREAD - V8_BASE`
heading. The table now uses the stated contrast. Both have favorable net
squared-error change; the accounting does not show calibration is dispensable.

Negative squared-error contributions help. Volume, location, and conversion all
help on average; allocation is nearly flat; calibration gives back much of the
gain. Changes also covary and cancel in totals. This explains why v8/v9's large,
consistent event-objective improvements need not create a similarly large
pooled-points change. It proves neither that the event objective is irrelevant
nor that only evaluation noise is responsible.

Integrity checks passed: exact event/point reconstruction error was at most
5.2e-14. `V8_STD` and `V9_BASE` ordinary predictions match exactly. Corrected
no-message replay differs from the historical v9 helper by up to 3.45 pts/100,
confirming the old depth/ALL no-message diagnostic was invalid while ordinary
forecasts remain historical results. The rank-positive v9 decoder can move FT
conversion through the message (maximum probability delta .00447); Day4's
rank-zero arms pass the isolation requirement.

## Basketball coherence

The named fixtures are mechanism checks, not targets or forced rankings.

- **Jokic/Korver versus Jokic/Westbrook:** additive ranks the Westbrook lineup
  1.084 points higher in total. BASE instead ranks Korver +1.772, `TEAM_01`
  +0.898, and `TEAM_1` +1.301. Relative to additive, the contextual correction
  favors the Korver pairing by +2.856 / +1.982 / +2.385. This is the intended
  question: fit relative to individual value, not a forced total ranking.
- **Five Jokics versus five Goberts:** BASE gives +9.36; `TEAM_01` +6.44;
  `TEAM_1` +5.81, versus additive +22.87. Structural arms preserve a large
  distinction without the additive model's extreme gap.
- **Limited centers versus a real lineup:** BASE -6.26; `TEAM_01` -5.93;
  `TEAM_1` -7.04; additive -7.90. All preserve the coherent direction.
- The clone ladder retains an increasingly negative context penalty as copies
  are added. `TEAM_1` attenuates context relative to BASE, consistent with the
  auxiliary target pulling the model toward observed lineup means.

These directional checks are incomplete. Five Goberts still score 117.85 under
BASE and 119.43 under TEAM_1, beside 118.27/119.13 for the real reference lineup.
Large negative no-message increments do not establish sufficiently poor final
offense. Nor does a smaller increment establish worse coherence without a
validated magnitude. For Korver versus Westbrook, the correction relative to
additive favors Korver, while the NN's message-on/off increment favors Westbrook;
those are different comparisons, and neither identifies causal chemistry.

## Uncertainty and expanded population

Observed-outcome intervals remain approximately calibrated. On all primary
cells, `TEAM_1` has 80% cell/possession coverage .789/.788 at width 31.77 and
95% coverage .946/.943 at width 49.57. Half-BASE has .795/.794 and .945/.941.
On novel fives, `TEAM_1` has .796/.791 and .938/.940. These are finite-batch
outcome intervals; they do **not** validate uncertainty about an arbitrary
synthetic lineup's latent mean.

The secondary positive-exposure expansion has 220,381 lineup-quarter cells and
2,760,546 possessions. It is much noisier, especially 190,937 cells with 1–19
possessions. Additive/BASE MAE is 21.8957/21.9235 overall and 26.2000/26.2205 on
novel fives. BASE narrowly wins the 20–79 band (15.8372 versus 15.8477) and loses
at >=80 (7.2526 versus 7.1930). This does not create a more powerful independent
benchmark; it mostly adds tiny cells. Regrouping and centering checks passed.
There were 49,652 unknown additive player slots, handled by the documented zero
convention.

The planned 2,000-game-cluster bootstrap was not run because exact reconstruction
would add substantial secondary runtime and storage. No IID possession bootstrap
was substituted. Equal-season paired intervals remain primary; neither captures
model-training uncertainty.

## Decision and next experiment

Keep corrected additive as the standalone predictive baseline, `V9_SPREAD` as
the structural research backbone, and fixed half as the best pre-registered
combined forecast. Do not promote a scorer from v10.

Run exactly one next experiment: **separate individual value from contextual
response**. Learn a strictly prior-only, cross-fitted, shrunk individual-value
mean arm, and train or constrain the structural path to be a zero-centred context
residual over a declared reference distribution. Compare additive, `V9_SPREAD`,
existing blends, mean alone, and mean+context on the same quarterly origins.
Preserve event accounting and the basketball panel, and test whether explicit
separation retains the novel-lineup context gain without the recurring-lineup
penalty. No player-pair effects or known-pair residuals.

Why this one: blending is Day4's only clear predictive help, while direct team
supervision improves its noisy target microscopically, damages event fidelity,
and attenuates context. Represent the two apparent sources explicitly instead of
asking one network objective to learn both.
