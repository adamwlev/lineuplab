# v18 scoring conventions

Frozen JOINT_CAPABILITY_V18_PLAN.md governs estimands and inference. Scoring
reuses the corrected v16 affine implementation and exact baseline forecasts.
All calibration uses completed earlier quarters only, never the scored quarter.
2015 supplies warmup; 2016–2026 is primary. Three separately calibrated seeds
are averaged, then scored on identical off5-quarter targets with actual opponents.
Half means 0.5 neural + 0.5 additive_defense. Half is the registered primary.
Direct, checkpoint_average, checkpoint_average_half and slices are descriptive.

J_POINT_BOTH, J_BOTH and J_ACTION_BOTH reuse native v16 fits. O_ORDER reuses
v17. Production recomputes chronological calibration and checks archived forecast
parity; engineering pilots use matched cold-start calibration and cannot select
arms. Native events and their accounting are not changed by point calibration.

No training launch, promotion, input rebuild or synthetic-quality coverage claim
is implied by a scorecard. Frozen reports and output directories remain intact.
