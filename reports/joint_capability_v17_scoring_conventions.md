# v17 scoring conventions — 2026-09-27

Implementation detail for the frozen v17 plan; no arm/objective changes.
Recorded before running the new scoring and control-replay analyses.

- Scoring writes to a separate derived namespace. Completed native cases,
  contexts and v16 reports are read-only, never linked to a writable subtree.
- Production must contain exactly48 quarterly origins ×5 arms ×3 seeds.
  Advance a single chronological frontier only when every case in that origin
  is complete. Reject missing earlier quarters; do not skip them.
- Calibrate each native NN view with the corrected `forecast` column, using
  only that model/seed/view's earlier completed broad>=50 cells. Keep player-ID
  columns intact. Blend only after calibration; average predictions across
  seeds before calculating metrics. Constant predictions get undefined
  correlation, never an invented zero or an excluded cell.
- Production J_POINT_BOTH/J_BOTH controls are reused from corrected v16, with
  independent prior-history replay proving parity. Deterministic additive and
  parent controls are read from the existing verified control library on exact
  row keys and the same seed set.
- An isolated one-origin pilot lacks its own earlier forecasts. Apply the same
  identity cold-start NN calibration to **both new and reused NN arms** in its
  descriptive scorecard. Additive/parent controls retain their existing dated
  calibration. Label this pilot-only, not a comparably calibrated production
  tournament. Independent archived-control parity checks still use the full
  appropriate prior history, in a separate audit.
- The plan's equally informed seasonal-level control is `seasonal_level`:
  dated league expectation plus the possession-weighted mean
  `(actual - dated league)` of prior completed broad>=50 cells in the **same
  quarter-of-season index**. If fewer than30 such cells are available, use all
  prior completed broad cells; if fewer than30 remain, use the dated league
  alone. No current-quarter outcome, future origin, optimized window or learned
  player term. The control reuses prior archived broad identities/outcomes and
  league values, not archived neural predictions. It is a diagnostic level
  forecast, not an extra registered arm or selected blend.
- Off5 cells are pooled from actual-opponent matchup rows with possession
  weights. Novel/recurring/thin/debut labels use exactly the existing v16 dated
  definitions. No dropping rows to improve metrics or match a partial control.
- Native per-family loss and native game/off5 point MSE are separate from the
  calibrated broad-quarter rating scorecard. Their units and populations differ.

The16 registered half-view contrasts and all three product standards remain
unchanged. A functioning leaderboard is not completion of the average-opponent,
coherence or uncertainty analyses, and does not authorize a full training run.
