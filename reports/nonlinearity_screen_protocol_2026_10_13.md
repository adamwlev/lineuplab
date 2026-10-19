# Can the network learn the interactions itself? Screen protocol — 2026-10-13

This protocol is written and committed before any arm is trained. Adam
approved the screen on 2026-10-13 ("Yeah let's give it a try … As long as the
inputs don't have player identities"). It is exploratory: one seed and a
screen, not a registered result.
- Script: `scripts/nonlinearity_screen.py`.
- Output: `experiments/cache/nonlinearity_screen_2026_10_13/`.

## Question

The network adds up players. The 14 combination effects that held up
([results](interaction_discovery_results_2026_10_13.md)) are bolted on as a
separate layer ([layer](combination_layer_results_2026_10_13.md)). Can the
network learn real interactions itself, without inventing false ones?

Two routes:
1. **Remove the bias against nonlinearity.** Give the network explicit
   pairwise capacity: interactions that are first order in their parameters,
   with no weight decay.
2. **Adam's idea: reward nonlinearity** in the loss.

## Arms

All arms use seed 17. Each is fitted with the full reference protocol
(`lineups.train.fit_origin`: inner epoch selection, fresh final fit, last
five checkpoints), from the same v14 parent as the saved reference.

| Arm | Change from the reference |
| --- | --- |
| `reference` | none: the saved J_POINT_BOTH fit, seed 17, which `lineups.train` reproduces exactly |
| `pairs` | + `PairInteractions`, no weight decay on it |
| `pairs_fast` | `pairs`, with the module's learning rate 5× (early stopping selects only 6–10 epochs) |
| `reward` | the reference plus Adam's nonlinearity reward in the loss |

**PairInteractions** (`lineups/model.py`). Identity-free: its inputs are the
same capability states the network already reads, plus listed height. There
are no player IDs.
- **Features.** A centered feature map g = tanh(W s + b) − tanh(b), width 16.
  - Offense s is the player's standardized state (18), his two rebound-prior
    inputs and his height.
  - Defense s is the defender's 19 descriptors and his height.
- **Offense.** Player i's 15 log-rate and logit corrections (actions,
  locations, conversions) are tanh(Σ_{j≠i} Σ_r (U g_i)_r (V g_j)_r), rank 4.
- **Defense.** One lineup-level shift for all five attackers:
  tanh(½ Σ_{j≠l} Σ_r (P h_j)_r (Q h_l)_r).
- **Start.** U and P start at zero, so every arm starts at the reference's
  function.
- **Bounds.** The tanh bounds each correction at ±1, the same bound as the
  other heads. Clone lineups saturate instead of growing quadratically.

**Reward** (Adam's linearity penalty, with its sign as he put it). In each
training batch:
- Take 256 lineups. For each, pick a side and two slots i ≠ j.
- Swap in two players drawn from other lineups in the batch.
- Compute the second difference of native points per 100:
  Δ = f(L) − f(L with i swapped) − f(L with j swapped) + f(L with both).
  For a model that adds up players, Δ is zero.
- The loss subtracts λ · mean(Δ²).

The strength is set as λ = k × 0.25 / (the reference's point-loss level),
which matches the point term's own scale.
- **Pilot.** k ∈ {1, 10, 100}, at origin 2024q2.
- **Rule** (outcome-free): k is the smallest value whose outer-quarter
  points forecasts have a non-additive variance share at least 5× the
  reference's. If none reaches it, k = 100.
- Pilot fits are labeled and not scored.

## Rows

Origins are the 20 quarters of 2022–2026 (2022q1–2026q4). Each arm forecasts
its outer quarter: game × offense five × defense five rows, with inputs frozen
at the quarter's start, as the checkpoint mixture. That is 20 new fits per
arm, plus inference for the reference.

## Contrasts (declared)

**1. Interactions (primary).**
- Candidates: the 105 type pairings of the discovery protocol × 5 families:
  points, rim share, three share, turnovers and FTA. That makes 525 cells.
- For each arm, the residual (actual minus that arm's forecast) is regressed
  on the pair feature and its type counts, as in the discovery.
  - Centered within quarter, weighted by exposure.
  - SEs clustered by game.
  - Rows: all 2022–2026 outer rows.
- Statistics:
  - **χ²_H**: the sum of (coefficient / SE)² over the 14 held-up cells. It
    falls as an arm captures the real interactions.
  - **χ²_N**: the same over the other 511 cells. It rises as an arm invents
    interactions that the data do not show.
  - **Capture ratio**: Σ_H implied × actual / Σ_H actual².
    - *implied* is the arm's own forecast interaction: its forecast minus its
      additive projection, regressed the same way.
    - *actual* is the coefficient for the actual outcome minus the
      reference's additive projection.
    - The reference's ratio is about 0.
- **Success** for an arm: χ²_H below the reference's, and χ²_N no more than
  64 above it. 64 is 2 SD of a χ² with 511 degrees of freedom.
- **Invention:** χ²_N more than 64 above the reference's.

**2. Accuracy (non-inferiority).**
- Calibrated points r² on outer broad cells (≥ 50 possessions), the
  network alone.
- Calibration two ways, both reported: (a) the reference's prior-only affine
  applied to every arm; (b) each arm's in-quarter affine (an oracle, the same
  rule for all).
- Reported: arm minus reference, mean over the 20 origins, with origin-level
  SE and the count of positive origins. Margin: −0.003.

**3. Nonlinearity.** The non-additive share of each arm's points-forecast
variance on outer rows: the variance left after the best additive fit, per
quarter.

**4. Pillar 2.** At 2026q4, native fixture margins for:
- legal centers vs Jokić/Westbrook;
- legal centers vs Jokić/Korver;
- five Goberts vs Jokić/Westbrook;
- five Jokićs vs Jokić/Westbrook.

## Predictions, stated in advance

- **`reward`:** the non-additive share rises, as forced. χ²_N rises
  (invention). χ²_H falls little. Accuracy is slightly worse.
- **`pairs` / `pairs_fast`:** a small non-additive share, some capture of
  the held-up effects, χ²_N unchanged, and accuracy within ±0.001.

## What follows

An arm that succeeds on contrasts 1 and 2 becomes a candidate to replace the
bolted-on layer. That would need a three-seed fit at the release origin and a
look at the property suite before any change to what the tool prints, and it
would be Adam's call. Nothing here changes the tool.

## Compute

About 63 fits of about 10–15 minutes each, single-threaded, four at a time:
roughly 3 hours. That is inside the six-hour limit.
