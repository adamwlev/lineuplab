# Current handoff — v16 implementation, 2026-09-18

## Scope and status

Adam asked to begin v16 implementation after documentation commit **b60ab2a**.
Codex implemented directly; no agents. The unchanged
[22-arm design](JOINT_CAPABILITY_V16_PLAN.md) is the authority.
**Implementation is incomplete; no full-run command or production launch yet.**

The previous handoff is preserved in the
[pre-implementation archive](docs/archive/2026-09-18_v16_start/SESSION_HANDOFF.md).
Current implementation choices, empirical preparation results and explicit
remaining work are in the
[implementation checkpoint](reports/joint_capability_v16_implementation_notes.md).

## Completed in this session

- Constrained actor/teammate/defender GLM primitives, causal input/validation
  construction, joint curvature draws and bounded early/late audit runner.
  All 16 fixed-lambda fits and 512 joint draws completed. Every fit met the
  registered convergence criterion; league-only likelihood comparisons are
  positive feasibility evidence, not proof against raw profiles or additive.
- Qualified phase labels with exact independent source reconciliation:
  4,846,590 possessions and 440,850 renewal entries. Use **phase_dev2**.
  phase_dev1 is preserved but rejected for training because it selected made
  FTs through overly broad rebound exclusions; the correction is documented.
- All archived controls replayed over both registered cohorts and actual
  two-team game margins. Shared prior-only calibration is implemented.
- Exact opponent-integration audit, 252 saved-v15 fixture/model/seed cases.
  Worst 4,096-reference native error .054880 pts/100; the 512 approximation
  still requires its prespecified sensitivity.
- All 22 neural forward paths and common loss/ledger-average primitives.
  88 real-parent inner/final replay checks passed at early/late cutoffs.
  No NN optimization has been run, and no predictive v16 result is claimed.

## Artifacts and process state

All paths below begin
`experiments/cache/joint_capability_2026_09_18_`:

| Suffix | Status / contents |
| --- | --- |
| `v16_profile_dev1` | Preserved failed numerical diagnostic; not accepted |
| `v16_profile_dev2` | Completed 16-case profile audit, fixed lambda1000, 32 joint draws each; 43 minutes total |
| `v16_phase_dev1` | Preserved rejected phase labels; orientation alignment itself verified |
| `v16_phase_dev2` | Completed corrected phase labels |
| `v16_controls_dev1` | Completed 48-origin × three-seed control replay; uses dev1 orientation only, not phase labels |
| `v16_integration_dev1` | Completed exact numerical integration audit |
| `v16_replay_dev1` | Preserved earlier forward checks, before WIDE capacity correction |
| `v16_replay_dev2` | Completed 88 current-code real-parent forward checks |
| `v16_curvature_dev1` | Same-Hessian solver parity/timing benchmark; optional preconditioner, not yet wired into joint draws |
| `v16_development/logs` | Durable unit-test and frozen-producer verification logs |

All bounded preparation jobs have completed. The former profile PID **73624**
is no longer an active task; do not use that PID as a status indicator. No full campaign,
scraper, database operation, old input rebuild, promotion or deployment ran.

Read the completed bounded audit log:

```bash
tail -n 60 experiments/cache/joint_capability_2026_09_18_v16_profile_dev2/logs/audit.log
```

## Working tree and verification

New uncommitted v16 modules/tests and the implementation report are present;
current state/backlog/navigation and this handoff are updated. Original reports,
the v16 plan, original runs and old scientific producers are untouched. Do not
stage caches. **No commit is authorized for this implementation task.**

Tests cover constraints/gradients/curvature, temporal poisoning, masks, phase
attribution, common calibration, pooling/margins, quadrature, all-arm nesting,
permutations, disabled banks, frozen unsupported outputs, recovery direction,
loss gradients and complete event averaging. All **40 tests** passed in
`foundation_tests_07.log`. `frozen_producer_audit.log` verifies all **256**
source hashes from the v13/v14/v15 frozen code manifests.

## Precise restart

1. Read the completed bounded profile audit and implementation checkpoint:
   review timing,
   curvature receipts, gauge errors and held-out channel likelihoods. These
   fixed-lambda league comparisons are feasibility checks, not the registered
   selected-penalty library or proof against raw profiles/additive points.
2. Implement the strictly dated monthly + exact-origin capability library:
   annual last-quarter penalty selection, row-own-date lookup, matched raw
   summaries, per-coordinate support, covariance/unknown-player handling and
   prefix-only normalizers. **Do not assign final-prefix GLM coefficients to
   earlier training rows.** Covariance draw cost needs attention before launch.
3. Wire common prefix references and the fresh-inner/final training lifecycle;
   finish feature integration, exact resume, non-NN channel controls, U0/U1/U2,
   new fixtures/support/novelty cohorts, reports and independent auditor.
4. Freeze the complete scientific manifest before inspecting NN pilots.
   Complete all-arm one-epoch smoke and the prescribed **48 full-stopping
   operational pilot cases**, then runtime/disk acceptance and preflight.
5. Only then provide verified launch/log/status/leaderboard commands. Do not
   launch the full 3,168-case campaign without Adam's separate request.

The new forward implementation has not passed training acceptance. Parameter
reports now distinguish nominal/trainable/enabled-module and structurally active
coordinates, including disabled banks and masked outputs; WIDE matches attention
within 0.5% for nominal and active counts. Fix the preparation-only lifecycle
issues listed in the checkpoint before freezing the full runner. Keep all three
product standards equal; no automatic promotion and no forced player rankings.
