# Joint capability v10 handoff

State: **complete and independently reviewed 2026-09-13**. Start with
`reports/joint_capability_v10_codex_review.md` for the final independent
qualifications, then `reports/joint_capability_v10_review.md`; the frozen contract is
`SOL_JOINT_CAPABILITY_DAY4_PLAN.md`.

## Completion and provenance

- Run: `experiments/cache/joint_capability_2026_09_12_v10/`
- New training: 96/96 arm-origins (`TEAM_01`, `TEAM_1`), 192 fits, 2,572.4 s,
  no failures or 48-epoch cap hits.
- Reused controls: corrected additive, V8_BASE/V8_STD, V9_BASE/V9_SPREAD and
  historical V9_ALL; no control was refit.
- Primary: 44 quarterly origins, 2016–2026, 5,607 cells / 726,364 possessions;
  novel 2,073 / 226,256. Four 2015 origins are warmup only.
- Production command and log: run-local `logs/production.command` and
  `logs/production.log`. `SUCCESS.json` and `reports/final_status.json` say
  complete. Source and code SHA-256 hashes are in `source_manifest.json` and
  `code_hashes.json`.

## Answers

1. The v8/v9 event gains improve point loss through volume, location and
   conversion, but calibration and cross-component cancellation return much of
   the gain. Exact reconstruction passed to 5.2e-14.
2. The pre-registered half additive/BASE blend scores 8.07274 MAE, 10.80812
   RMSE and .12576 raw r2 versus additive 8.09195/10.84099/.12043 and BASE
   8.14017/10.86667/.11626. GLOBAL is tied. Blending is useful; weight fitting
   adds no practical value.
3. `TEAM_1` scores 8.11221 MAE and `TEAM_01` 8.15905. `TEAM_1 - BASE` is
   -0.02619 mean season MAE, 95% CI [-0.07605,+0.02367]. It improves its direct
   native team MSE by only 0.027% and worsens outer event loss in 11/11 seasons.
   Direct team supervision is not adopted.

A labeled post-run half additive/`TEAM_1` blend reaches 8.05677 MAE, the best
pooled value on this fixed population, but its season interval versus additive
crosses zero and novel MAE 8.84645 is slightly worse than half-BASE 8.83865.

Basketball directions survive: every structural arm penalizes the limited-center
lineup; the contextual correction favors Korver beside Jokic relative to the
additive expectation; clone duplication remains penalized. Team supervision
attenuates some context. Finite-batch 80%/95% intervals remain near nominal, but
latent-mean uncertainty for arbitrary lineups is still unvalidated. Defense,
rebound facilitation, and actual-opponent interaction were not modeled.

## Deviations and limitations

The exact 2,000-replicate game-cluster bootstrap was not run because of its
secondary reconstruction/storage cost; no invalid IID substitute was used. The
expanded positive-exposure population was completed but mostly adds tiny noisy
cells. No scraping, database access/mutation, input rebuild, scorer promotion or
deployment occurred. Historical artifacts were not rewritten.

## Exactly one next experiment

Build a cross-fitted, shrunk **individual-value mean arm** and an explicitly
zero-centred `V9_SPREAD` **context residual**, then test mean, context, and their
combination on the frozen quarterly protocol. This follows the blend result and
directly tests whether individual value can be retained without suppressing the
novel-lineup context advantage. No known-pair chemistry.

Sol has stopped editing. The requested Codex review, documentation, verification,
and commit are recorded in the repository commit that contains this handoff.
Verification: 743 tests pass in 33.847 seconds; durable log at
`reports/joint_capability_v10_verification.log`. The fixed blend has a nominal
season-paired RMSE improvement versus additive overall and on novel fives;
overall MAE remains uncertain. The Shapley table's control label was corrected
without altering source results. Smaller context effects alone do not establish
worse coherence, and five-Gobert final offense remains unresolved. The proposed
mean/context experiment requires a precise prior reference decomposition first.
