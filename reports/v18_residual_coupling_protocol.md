# V18 residual coupling supplement

September 30, 2026. Frozen after inspecting the completed persistence study and
before calculating the cross-channel matrices below. This is explicitly a
result-motivated exploratory follow-up, not part of the original frozen protocol.
Adam authorized diagnostics to inform future direction. No new fits or inference.

Use completed persistence1 and persistence_summary1 artifacts, preserving them.
Four NN arms, identical primary saved predictions. Decompose the point residual
into conditional FG conversion, other FG error, conditional FT conversion, other
FT error, and saved calibration. Do not interpret calibration magnitude as a
calibration mistake or physical skill; it is a known deterministic transformation.

For the existing five random game partitions, use the original20-possession and
two-game-per-half support. For each arm estimate the full five-by-five cross-half
covariance matrix, symmetrizing Cov(A_i,B_j) and Cov(A_j,B_i). Weight by total
joint-label cell exposure and also report within-origin-centered matrices.
Mean the five matrices; repetitions are not independent samples. Print diagonal
sum, off-diagonal sum and total. Their total must exactly equal the corresponding
point residual covariance already reported. Negative off-diagonal terms are
offsetting errors, not causal compensation or proof the NN intentionally trades
off channels. Do not report a theoretical ceiling or attainable score gain.

Separately compute cross-half covariance/correlation between FGA and FTA count
residuals, raw and CLOCK adjusted. These are different units from the point-component
matrix, so do not add them to it. No new shrinkage constant, model selection,
population threshold, context fit or neural inference.

Export named, chronological high-support cases using the already prescribed
100joint-label possessions and two games in each half. Include every eligible
case for each arm, not only harms. Provide two descriptive top20 reference lists:
largest signed product of early/late point errors (persistent mismatch), and
largest CLOCK-adjusted FGA/FTA squared-rate sum averaged across halves (action
error). These lists are future-outcome-selected illustrations, not acceptance
sets, causal findings or honest estimates of selected-tail performance. Attach
existing role-change and transfer flags and archived player names.

Stop with an identity audit, complete matrices/case exports, and the combined
interpretation. No additional campaign launches automatically.
