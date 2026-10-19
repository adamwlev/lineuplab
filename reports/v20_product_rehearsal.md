# V20 basketball and average-opponent rehearsal — 2026-10-06

Read-only arbitrary-lineup inference now uses each arm's correct saved profile
bank, adjusted normalizer, common clock reference, endpoint and last-five
checkpoint window. All original models/artifacts remain unchanged. No neural
training, database access, cleanup, promotion or full-campaign launch.

The [product rehearsal protocol](v20_product_rehearsal_protocol.md) fixed the
fixture and average-opponent checks before those runs. The adapter replay was
their preceding prerequisite. These are the prescribed production-shaped pilot
checks, not an arm search or the completed full V20 analysis.

## Input and numerical verification

24saved forecast panels (12arm/date combinations ×endpoint/average) replay on
the fixed first16matchup rows. The arbitrary-lineup input tensors also match
ordinary observed-row tensors. Maximum point difference **.00001683points/100**,
within the pre-execution2e-5absolute+1e-7relative float32 re-association guard.
This is not a claim of byte-identical arbitrary-query inference; original
training/objective tolerances are untouched. Replay took11.75seconds.

Compact cases resolve retained weights/contexts through the storage-aware
verifier. Old controls retain original profiles; adjusted arms require matching
fit/data/normalizer provenance. Final endpoint must equal the final checkpoint;
only the saved T−4…T window is used, never the patience tail. Fixture ratios are
reconstructed from mixed physical masses. Point-only average-opponent outputs
use the algebraically equivalent average of checkpoint points, not mean logits.
Models are restored to their endpoint after inference, including failure paths.

## Basketball coherence: no new pass

All21registered2026q4fixtures plus three prior-common defensive references:
24×24mirrored pairings ×four available arms ×two estimators = **4,608rows**,
seed17. There is no registered2016q1fixture; none was invented. Full production
still owes32fixtures/10dates/three seeds. Fixture runtime13.88seconds,17.11MiB.

Primary checkpoint-average-half margins, points/100; positive favors the legal
five-center lineup. FTA columns are the centers' **native NN ledger**, not an
invented decomposition of the additive half. All NN calibrations are isolated
cold starts; these are not historical production fixture ratings.

| Arm | Margin vs Jokić/Korver | Margin vs Jokić/Westbrook | Center FTA/100 vs Korver | Center FTA/100 vs Westbrook |
| --- | ---: | ---: | ---: | ---: |
| P_BASE | +5.690 | +5.968 | 32.660 | 30.537 |
| P_CONTEXT | +7.618 | +6.921 | 40.279 | 36.114 |
| S_ADJ | +7.107 | +6.537 | 34.743 | 32.000 |
| S_BOTH | +7.265 | +6.510 | 40.328 | 36.269 |

The center problem remains. Context models still assign very high FTA to centers;
upstream adjustment plus S5 does not visibly solve it on this pilot. It would be
wrong to tune arms/fixtures from these numbers or treat the absence of a fix as
the final factorial conclusion. No late P_ADJ/P_BOTH pilot exists, so this panel
does not isolate profile adjustment from selection policy.

Opponent context matters: against the three prior-common defensive references,
centers' mean native offense is113.97–114.35rather than the121–125against the
Jokić examples. Both directions, additive residuals, initial/renewed usage,
shortfall summaries, per-player event ledgers and all selected-checkpoint context
curves are exported; a favorable margin alone does not certify sensible offense
or defense. The Korver raw-state injection retains the original mixed-date
limitation. Residuals/ledger decompositions are not identified causal effects.

Role stretch for centers is about.520–.534in the shown Jokić matchups; historical
clock mismatch is.1804. These are descriptors, not calibrated hypothetical-quality
intervals. C is common across mean models because it measures historical player
deployment. Unknown/thin-data flags remain available in descriptor exports.
Fixture uncertainty and as-of risk thresholds remain a separate pending consumer.

Independent fixture audit passes all4,608rows: physical point/opportunity/mass
identities, calibration/blends, context/checkpoint averaging, R and JS-clock
descriptors, and mirrored-margin antisymmetry. Per-checkpoint permutation checks
pass the existing tolerance; maximum difference.0001168points/100. Final
checkpoint/context mixture identities retain the original numerical guards.

## Average-opponent interpretation

Both runs complete:2016q1 **382.70seconds**,2026q4 **219.63seconds**, run partly
concurrently with one numerical thread each. Outputs.554/.311MiB. No fits.

Possession-weighted r², checkpoint-average-half, seed17 and isolated cold NN
calibration. Same cells within each date; do not pool the two isolated pilots.

| Arm | 2016q1:187cells/23,039poss | 2026q4:206cells/24,528poss |
| --- | ---: | ---: |
| Integrated additive defense | .018443 | .072701 |
| P_BASE | .099775 | .094303 |
| P_CONTEXT | .106130 | .098125 |
| P_ADJ | .099774 | — |
| P_BOTH | .106827 | — |
| S_BASE | .089323 | — |
| S_CONTEXT | .098441 | — |
| S_ADJ | .066043 | .095077 |
| S_BOTH | .106827 | .096053 |

No broad conclusion about either adjustment or S5 follows from these two dates.
Early P_BOTH/S_BOTH share endpoint14and therefore the same last-five forecast.
512versus4096maximum absolute primary-blend difference is.17066points/100early,
.02881late on the fixed20-cell subsets; retain the sensitivity rather than
describing512as exact integration. These differences are small compared with
lineup-quarter RMSE, but not necessarily small relative to tiny arm contrasts.
Independent metric/population/blend/seed-average audits and fixed3-cell512-draw
replays for P_BASE/S_BOTH pass at both dates; replay errors are below.000001points/100.

Each pilot uses all broad off5>=50cells, the original prior365-day-decayed
defensive lineup distribution,512deterministic common draws, and4096on the
fixed first20lexicographic cells. New profile normalizers are not shared across
arms. All available arms and endpoint/averaged views are retained.

These forecasts intentionally remove the realized opponent schedule, while their
targets are still realized outcomes against actual opponents. Report the metrics
as a disclosed product-mode diagnostic, not neutral-opponent counterfactual
ground truth or an apples-to-apples causal comparison with the actual-opponent
scoreboard. Pilot outer results cannot select arms, weights or epoch counts.

## Verification, outputs and next work

52V20tests pass in8.64seconds, including complete-ledger versus probability
averaging, point-mixture equivalence, endpoint restoration and future calibration
date rejection. An audit-only date-format assumption was found by reading the
production calibration contract: fitted `latest_stop` is ISO text, not integer
days. New `v20_product_audit_v2` normalizes dates and preserves the original
completed cold-fixture audit; no forecast or numerical tolerance changed.

New cache roots under `experiments/cache/`:

- `v20_query_replay_2026_10_06`
- `v20_basketball_pilot_2026_10_06`
- `v20_basketball_audit_2026_10_06`
- `v20_average_pilot_2026_10_06/<origin>`
- `v20_average_audit_2026_10_06/<origin>`

Fixture outputs: `panel.csv.gz`, `matchups.csv.gz`, per-arm/seed native physical
ledgers, R/C/driver-share descriptors, original metadata and per-checkpoint
`context_curves.csv.gz`. Curves are explicitly labeled checkpoint-level
diagnostics, not a fabricated set of final averaged probabilities.
Average outputs: per-arm/seed and ensemble cell tables,512/4096sensitivity,
metric sufficient statistics, timings and immutable source references.

Logs under `v20_implementation_2026_10_04/logs/`: `query_replay.log`,
`basketball_pilot.log`, `basketball_audit.log`, `average_pilot_<origin>.log`,
`average_audit_<origin>.log`, `product_tests.log`, `product_checkpoint_tests.log`.
Consumers require the documented retention wrapper. No full launch command
exists yet; do not present these per-origin analysis commands as a training launch.

Still required: extra descriptive controls and three-seed event mixtures;
dated fixture uncertainty/as-of risk slice; observed context curves, transfer/
role/persistence/covariance and registered contrasts; full supervisor/completion
graph and updated downstream-inclusive resource forecast. Current adapter only
handles the eight registered V20 factorial arms. The extra historical controls
must be added via a new consumer rather than silently mutating frozen outputs.
