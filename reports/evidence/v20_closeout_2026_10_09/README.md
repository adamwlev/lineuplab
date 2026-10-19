# Compact V20 closeout evidence

Small text extracts committed alongside the [scientific review](../../joint_capability_v20_scientific_review.md)
and [closeout](../../joint_capability_v20_closeout.md). Large local artifacts are
not included. `verification.json` records source hashes, output hashes and checks;
the exporter is `experiments/v20_closeout.py`. CSVs are reserialized extracts,
not replacements for the original output files.

- `point_recomputed.csv`: reference checkpoint-average-half plus additive
  controls, all and novel slices. Primary 44 quarters; warmup excluded.
- `registered_*_contrasts.csv`: complete frozen 17/44/4 comparison families.
  Point/event loss deltas: lower is better; uncertainty log score: higher better.
- `center_matchups.csv`: three-seed mean checkpoint-averaged ledgers and
  predictions. Event channels belong to the NN, not an invented additive ledger.
- `risk_population.csv`: all-future and primary-cohort tail counts per quarter;
  threshold uses only prior compositions, never outcomes.
- `training_summary.csv`: primary-quarter selected epochs and averaging windows.
- `bias_summary.csv`: reference-only pooled and quarterly bias, points/100.
- `bias_followup_summary.json`: earlier exploratory conversion/cohort study,
  not total point bias or a causal result. Its legacy `noncorner` field is a
  distance-bucket proxy, not measured shot-angle geometry; see closeout caveat.

No prediction is promoted by this bundle. Finite-game and synthetic-quality
uncertainty are not interchangeable, and repeated historical testing is not
untouched prospective confirmation.
