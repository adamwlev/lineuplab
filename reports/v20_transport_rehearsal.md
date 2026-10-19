# V20 transport uncertainty rehearsal — 2026-10-06

Implemented strict-date empirical role/clock descriptors and the prespecified
nested nonnegative-variance models. No NN means changed, no full training launched,
and no NBA latent-quality coverage claimed. The [protocol](v20_transport_rehearsal_protocol.md)
was frozen before these outputs; original V20 plan/artifacts are unchanged.

## Real data

Two prior-only snapshots:2016q1 has305,945historical matchup rows/797players;
2026q4 has346,149rows/1,068players. Role shares are aggregated by game/off5,
with observed-channel masks,730-day decay,200possession league shrinkage and.05SD
floor. Clock history has31states including unknown. Native averaged actor rates,
not an invented additive-half ledger, determine query roles.

P_BASE possession-weighted mean R=.242754/.268200 at the two dates; mean
C=.203129/.202577. R is max-player RMS standardized share deviation; C is
max-player square-root Jensen–Shannon distance, natural logs. Summaries use all
15,832/22,522exported matchup rows, not just the primary off5>=50cohort. Individual
shares, channel deviations, support and unknown/thin markers are retained.

Cold uncertainty rehearsal covers26/14models,1,508/728model-pair rows (not that
many independent cases). Primary averaged-half plus direct/half included.
U0/U1/transport correctly remain NOT_IDENTIFIED without prior calibration;
point scores remain available, no coverage gate or borrowed residual history.
Fixed146-cell transfer registry preserved. P_ADJ has no late pilot.

## Identified synthetic results

20replicates/world,1,200training and300held-out pairs,120final model fits plus
nested penalty subfits. Lower joint NLL is better; MCSE is over replicates.

| World | Model | NLL | NLL minus U1 (MCSE) | Variance RMSE | Nominal95coverage |
| --- | --- | ---: | ---: | ---: | ---: |
| Signal | U1 |6.423660|reference|8.4829|94.375%|
| Signal | U_ROLE |6.403956|−.019704(.002625)|3.8609|94.392%|
| Signal | U_ROLE_CLOCK |6.401705|−.021955(.002795)|3.0527|94.325%|
| Constant | U1 |6.279204|reference|.5706|94.733%|
| Constant | U_ROLE |6.279153|−.000051(.000164)|.7101|94.750%|
| Constant | U_ROLE_CLOCK |6.278887|−.000317(.000395)|.7968|94.767%|

Signal true slopes3/12are estimated2.1619/9.3011: shrinkage remains. Constant
world shows no clear predictive gain and worse variance recovery; mean clock
slope1.2786despite truth0. Nonnegative structure can still fit noise. Modest
undercoverage and favorable known-noise/mean generator limit the evidence.
No retuning; not a five-center or hypothetical-quality solution.

## Verification and operations

Independent pandas game/off5 aggregation and20spread players/date reproduce
role moments/both-side clock histories, max error2.01e-11. Matrix-form Gaussian
scoring reproduces120synthetic NLLs, max error8.88e-16; nested temporal/scaling
and cold-status checks pass. Complete V20 suite:46tests pass in7.06seconds.

Descriptor/cold/synthetic/audit runtimes7.20/13.84/1.53/2.47seconds;~77MiB new
outputs. Full254-date descriptor calendar is not built; no GLM refit needed.
First independent audit accumulated pandas counts in float32; corrected only
audit accumulation to float64 in a new prefix, retaining original tolerances
and failed evidence. Test discovery initially stalled in OpenBLAS thread init;
stopped only that confirmed test process, reran with all BLAS/thread env settings1.
Training and the user's unrelated project were untouched.

Cache roots: `v20_descriptor_rehearsal_2026_10_06`,
`v20_transport_synthetic_2026_10_06`, `v20_transport_cold_2026_10_06`,
`v20_transport_audit_2026_10_06_v2`. Logs under
`v20_implementation_2026_10_04/logs/`: descriptors, transport_synthetic,
transport_cold, transport_audit2, v20_checkpoint_tests_single_thread.

Remaining: full prior-only NBA uncertainty integration/chronological sensitivity;
full descriptor calendar/as-of risk thresholds; additional controls/multi-seed
conditional event mixtures; fixtures/average opponents; covariance/contrasts/
persistence; supervisor/completion graph and final downstream resource forecast.
New consumers are now source-bound; use versioned successors/new prefixes for
extensions. Full launch still requires readiness and explicit approval.
