# v16 operational amendment — eight pilots, 2026-09-19

Adam approved reducing the separate full-stopping pilot suite from 48 to eight
cases. This changes launch acceptance only. The original frozen plan and
implementation conventions remain preserved; this document supersedes their
48-pilot requirement, not their scientific experiment.

## Fixed cases and rationale

| Origin | Arm | Seed | Operational coverage |
| --- | --- | --- | --- |
| 2016q1 | J_RAW | 17 | Early-date raw-input joint training |
| 2016q1 | J_BOTH | 17 | Early-date adjusted offense and defense |
| 2016q1 | J_ALL_BOTH | 17 | Attention, allocation and separate renewal phases together |
| 2016q1 | J_BOTH | 23 | Independent seed and checkpoint namespace |
| 2026q4 | J_RAW | 17 | Late-date raw-input joint training |
| 2026q4 | J_BOTH | 17 | Late-date adjusted offense and defense |
| 2026q4 | J_ALL_BOTH | 17 | Larger-prefix combined mechanisms and resource stress |
| 2026q4 | J_POINT_BOTH | 17 | Auxiliary point-loss training path |

Selection is by implementation coverage, not predictive results. No completed
full-stopping v16 pilots were inspected to select these cases. All 44 one-epoch
smoke cases still run and must pass their independent audit. Every original
production case remains: 22 arms × three seeds × 48 origins = 3,168 cases.
Losses, profiles, cutoffs, normalization, stopping, checkpoint averaging,
calibration, controls, three product standards and all final analyses are
unchanged. Models absent from the pilot still receive full production fits.

## Preservation and reuse

The original prelaunch/commit supervisors were stopped while their smoke child
was running; that child was left to finish. Old outputs/logs remain intact.
The completed 2,032-snapshot library is unchanged and reused. No model producer,
old protocol, old convention, or existing manifest is edited for this amendment.

The amended runner creates new pilot, production and supervisor prefixes. It
requires the original 44-case smoke completion and independent audit, verifies
all original source/data fingerprints, and records their exact receipt hashes.
Its only extra producer dependencies are the new operational adapter and this
amendment. Comparing manifests must establish equality of all original fields
except stage, case schedule and the description of isolated-pilot overhead.
New operational metadata are explicit additions, never relabelled old outputs.
The original training, scoring and independent-audit functions execute the eight
cases directly from their frozen manifest. No monkey-patching or copied fits.
Pilots remain separate from production fits; overhead drops to eight cases
(about 0.25% of the campaign).

## Acceptance retained and limitations

- All 44 smoke and eight pilot cases must pass the original independent
  saved-state, temporal-cutoff, selected-epoch, final-fit-length, checkpoint-
  average, channel-denominator and ledger/calibration reconciliation.
- Existing interrupted/resumed training and uncertainty tests remain required.
  A second seed is not itself proof of interrupted-run equivalence.
- Keep the 96-epoch cap, patience eight and existing minimum improvement.
  No accuracy-based arm selection or early exit from the eight-case suite.
- Run the complete v16 unit-test suite, including amended acceptance/commit
  guards, with durable logs.
- Resource projection uses the **maximum measured** pilot case time and size,
  rather than pretending eight representative cases estimate all-arm
  quantiles. Retain 50% time overhead, 25% storage overhead plus 25 GiB, 10 GiB
  free-space reserve and the original RAM limit. Print measured and unmeasured
  arms; the projection is not a guarantee or proof that every arm is bounded.
- Architecture-specific multi-epoch failures in unpiloted arms can still occur
  in production. This is the explicitly accepted tradeoff for faster launch.

The guarded commit remains conditional on passing acceptance and unchanged
reviewed files/HEAD/index. The amendment does **not** authorize launching full
training, promoting a scorer or changing any research conclusion.
