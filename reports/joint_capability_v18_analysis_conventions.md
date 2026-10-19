# v18 derived analysis contract

JOINT_CAPABILITY_V18_PLAN.md is the frozen scientific authority. Original
artifacts, fits, inputs and producer fingerprints are never changed. Read the
v18 scoring conventions for prior-only calibration and point-view semantics.

- Primary half-view point contrasts: 23 tests, 10,000 season-block resamples,
  RNG180928, exact 2^11 season swaps, Holm23, leave-one-season-out sensitivity.
- Nine mechanisms × four native event families: 36 separately corrected tests.
  Pool loss/exposure sums over seeds and quarters within seasons. This is
  seed-average loss, not loss of ensemble event forecasts; not global Holm59.
- Role forecasts are native direct seed-mean events, not half-blend events.
  Preserve original matchup rows/player order/date in compact NPZ, and export
  player-quarter and player-off5-quarter aggregates with per-target exposure.
  Conditional allocation cross entropy and absolute team/player volume are
  different estimands. Do not condition forecasting on realized team counts.
- Frozen transfer registry: all matched cells, plus >=100/200/500 possessions
  with >=5 games. Report mappings/exclusions, retain all movers, count multi-mover
  cells once. Expected original primary146 cells/47,419poss is an audit, not an
  assumed present sample. Descriptive retrospective affiliations, not causal trades.
- U0 per-cell FINITE_GAME_BAND is valid; summary OK is a different contract.
  Validate arithmetic before aggregating either all-off5 or broad populations.
  U1 constant discrepancy uses prior balanced-game pairs. Neither validates
  arbitrary-lineup latent-quality uncertainty; no U2 or coverage gate.
- Fixture input-reference sensitivities zero standardized raw descriptors or
  adjusted banks while retaining raw anchors/physical priors. They are explicitly
  broader than isolated teammate-message removal, are not retrained arms, and
  must not be called causal teammate effects. A_ACCOUNT supplies the trained
  current-teammate comparator. All ordered matchups, gates/evidence and action/
  conversion/renewal ledgers remain available, without forcing named rankings.
- All new models use512 prior reference opponents, first20 cells/date4096
  sensitivity. Saved compatible controls are reused and key checked. J_ACTION_BOTH
  lacks compatible average-mode exports and receives saved-weight integration,
  never a refit. Existing primary.npz files already contain the required player
  event exports, so no control player-event replay is necessary.
- Independent metric arithmetic, exact half identity and recursive source
  checks precede the generated handoff. No automatic model selection/promotion.
