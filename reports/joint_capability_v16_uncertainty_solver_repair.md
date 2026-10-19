# v16 uncertainty optimizer recovery — 2026-09-27

The optimized analysis completed stages 1–4, then failed during 2018q4 U2
fitting for J_ALL_BOTH:half / first_second. All 15 completed uncertainty
quarters remain preserved. No neural fit, point forecast or calibration changes.

## Diagnosis and fixed numerical policy

The 828-pair prior fit (penalty 10) stopped after six iterations. A line-search
trial reached absolute log variance 806.21, beyond the existing overflow guard
650. The optimizer then reported relative objective convergence, although its
maximum mean gradient was .02295378 versus the existing required <1e-5.
The independent gradient check correctly stopped the campaign.

Keep the original optimizer and return accepted fits unchanged. Only on failure,
restart L-BFGS-B with fresh history at its finite, non-worse endpoint (otherwise
the original initial point). Scale the entire objective AND gradient, including
the same penalty, by pair count. Use maxiter2000, gtol1e-8, ftol1e-15, maxls100.
If that still fails, one BFGS attempt starts from the best finite non-worse
point, with maxiter2000 and gtol1e-8. Fail closed if recovery does not pass the
original <1e-5 mean-gradient check and nonincreasing objective. No variance
clipping, tolerance relaxation, changed penalty grid, data, selection or cutoff.
This is a bounded numerical retry, not a new statistical model or global-optimum
claim. It is selected without examining held-out predictive performance.

The reproduced failed objective 6587.125147799 improves to 6569.802496986
(mean 7.934544078485402). Restarted L-BFGS-B mean gradient 3.81e-9;
independent restarted BFGS agrees on the objective, with gradient 1.45e-9.

## Provenance and continuation

Frozen source files and the failed prefix remain unchanged. A new derived
prefix reuses receipt-verified completed stages and the first 15 uncertainty
quarters through explicit links. Incomplete 2018q4 outputs are not copied.
The new manifest binds the numerical wrapper, continuation runner and this
amendment. The override is process-local and limited to uncertainty fitting;
the same override applies to final identification simulations. No model training,
database access, input rebuild, scorer promotion, deployment or commit.

Stage 5 resumes chronologically; stage 6 follows only after full completion.
All original three-pillar interpretation limits remain, especially that
synthetic latent-quality interval coverage is not validated. No timeouts;
durable logs, single-writer protection and fail-stop behavior remain active.
