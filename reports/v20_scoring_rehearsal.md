# V20 matched-scoring rehearsal — 2026-10-06

Eight completed pilots were consumed without refitting, through the new compact
archive reader. Original pilots, reused controls and historical outputs remain
unchanged. Full campaign is **not launched or launch-ready**.

## What passed

- Reference and realized-clock point panels at2016q1/2026q4; all eight factorial
  arms at the early date, four available arms at the late date. One seed17.
- Direct, half, checkpoint-average, checkpoint-average-half and both native
  views; all/novel/recurring/thin/debut slices, >=50 and <50possession populations.
- All neural controls use the same isolated cold calibration. No reuse of
  historical fitted calibration for P_BASE/P_CONTEXT. Reference additive controls
  retain their previously established predictions. These are operational pilot
  comparisons, **not production model rankings** or grounds to select arms.
- Conditional half blends with the equally informed conditional additive control.
  Realized future clock context is labeled diagnostic, never a forecast claim.
- Independent numpy aggregation, targets, affine calibration, seed means, half
  identities and sufficient statistics: **3,840rows**, four panels,50calibration
  checks, maximum calibration error0. Both chronological view keys and source
  row alignment enforced; production scoring only advances complete prefixes.
- Independent native arithmetic for all eight new pilots, both saved windows
  and both environments: **32event panels**. Conditional checkpoint-average loss
  uses actual saved state ledgers, not loss of collapsed matchup predictions.
  Maximum point-identity error8.53e-14points/100; event discrepancy4.44e-16.
- Read-only single-case preview matches the saved reference and conditional
  scorecards (all metrics,1e-10absolute tolerance). CLI sort/slice/view exercised.
-16targeted report/calibration/storage tests pass in3.42s. All42original pilot
  receipts and their producer fingerprints reverified unchanged.

Scoring took25.4seconds. No new training, input rebuild, database access, cleanup,
commit or promotion occurred. Scored artifacts occupy58.45MiB.

## Pilot numbers, not arm selection

Reference checkpoint-average-half r², seed17, same off5>=50cells within each date:

| Arm | 2016q1:187cells/23,039poss | 2026q4:206cells/24,528poss |
| --- | ---: | ---: |
| additive_defense | .048843 | .072761 |
| P_BASE | .102575 | .104917 |
| P_CONTEXT | .119116 | .109637 |
| P_ADJ | .103457 | — |
| P_BOTH | .120455 | — |
| S_BASE | .096536 | — |
| S_CONTEXT | .114666 | — |
| S_ADJ | .080285 | .102486 |
| S_BOTH | .120455 | .105562 |

P_BOTH/S_BOTH selected the same endpoint14at the early pilot, hence equal
five-checkpoint predictions. Selection stability does not guarantee better
outer-quarter accuracy. No change to the frozen experiment follows these results.
Basketball fixtures and hypothetical-lineup uncertainty remain untested at this
checkpoint; predictive pilot numbers cannot stand in for those standards.

## Measured partial resource forecast

Filesystem free196.55GiB after Adam's additional cleanup. A calendar-scaled
estimate subtracting the eight reusable pilots leaves856new cases:

- Compact case artifacts45.12GiB; scored outputs approximately3.65GiB.
- Including25%size allowance, three active temporary cases and13GiBreserve:
  **75.32GiB**, comfortably below current free space.
- Three-slot FIFO simulation: **44.38hours central**,52.69hours with1.2×training
  cost; all96inner+96final epochs would be226.76hours. The cap scenario is not
  an upper bound on machine contention or per-epoch cost.
- Origin-barrier alternative44.47/52.80/227.12hours. These are simulations;
  the full supervisor is still unimplemented, not a claim of deployed scheduling.

Runtime uses per-arm pilot-mean epoch counts and largest measured row-normalized
cost. Only S_ADJ/S_BOTH have late pilots. Epoch variation, state expansion and
the other local workload may change cost. **Remaining downstream artifacts/time
are excluded**, so this is not final full-campaign readiness or launch authority.
Original33.44hprofile build and completed pilots are sunk, not repeated here.

## Reproduction and artifacts

Derived roots under `experiments/cache/`:

- `v20_pilot_scored_2026_10_06`
- `v20_pilot_scoring_audit_2026_10_06`
- `v20_pilot_native_audit_2026_10_06`
- `v20_resources_2026_10_06`

Durable logs under `v20_implementation_2026_10_04/logs/`: `scoring.log`,
`scoring_audit.log`, `native_audit.log`, `resources.log`, `case_preview.log`,
`report_options.log`, `scoring_integration_tests.log`,
`scoring_final_verification2.log`. The first final-verification log preserves
an invocation mistake (nonexistent verifier context-manager method); corrected
installation-before-import completed successfully, no model/code changes.

Verified report command:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v20_report report \
  --out experiments/cache/v20_pilot_scored_2026_10_06 \
  --origin 2016q1 --view checkpoint_average_half --sort r2 --slice all
```

Verified read-only preview:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v20_case_preview \
  --scoring experiments/cache/v20_pilot_scored_2026_10_06 \
  --origin 2026q4 --arm S_BOTH
```

Pilots cannot be pooled by this reporter. New consumers are now source-bound to
completed derived outputs; later fixes/extensions need versioned successors and
new prefixes. No changes to frozen training, profile or storage producers.

## Next required work

Finish remaining downstream rehearsal: extra descriptive controls
C_FIXED/C_CLOCK/R_ALLOC/O_ORDER/J_BOTH, multi-seed mixture event scoring,
role/clock descriptors and nested uncertainty, fixed fixtures/average opponent,
persistence/covariance and registered contrast schemas. Then implement/audit
full supervisor/completion graph and include downstream costs in readiness.
Only then provide the verified full-launch command and seek approval.
