# v16 first-origin metadata repair — implementation and evidence

2026-09-19. Operational bug fix authorized by Adam. No full production relaunch
or commit performed by the agent. The three-seed, 22-arm experiment is unchanged.

## Cause and repair

The first 2015q1 workers failed before an optimizer update: strict provenance
hashing encountered a legacy `parent_shared.team_baseline=NaN`. Its legacy
row count and exposure were both zero. This explicitly undefined denominator
is not used by v16, which has separate finite event/point references.

`canonical_shared()` returns a new shallow context with this exact sentinel
represented by `None`. Finite contexts are unchanged. A nonfinite denominator
with positive/missing exposure, infinity, or an unrelated scalar NaN is not
silently accepted. No original parent fit or cache is modified.

The old producer files remain byte-for-byte unchanged. Versioned case/runner
copies make only these declared substitutions, checked automatically:

1. Import and apply the canonicalizer when constructing a new shared context.
2. Route the new runner to that case module and its own worker module name.

The model, training loop, optimizer, stopping, inputs, normalizers, objectives,
calibration, reporting, analysis and independent auditor are original code.
The copies are deliberately compatibility-isolated; source-parity checks reject
any undeclared divergence. This avoids runtime monkey-patching or rewriting old
manifest fingerprints. Future unification requires an explicit new revision.

## Evidence

**Final status: PASS.** Both first-origin native cases completed, saved-output
replay passed (maximum 0.000018601 pts/100), and all **95 tests** passed (88
existing plus seven new). Production preflight passed with 246.33 GB free
versus 209.69 GB required. Production remains unstarted in the new destination.
J_RAW took 61.8 seconds including initial shared-context construction;
J_ALL_BOTH took 130.9 seconds reusing those contexts. These are one-epoch
regressions, not full-stopping runtime estimates.

Frozen repair scope:
[metadata fix protocol](joint_capability_v16_metadata_fix_protocol.md).
New evidence prefix: `experiments/cache/v16_metadata_fix_2026_09_19_v1`.

- All 288 saved parent contexts scanned without refits. Nine have the sentinel:
  2015q1 inner/final and 2015q2 inner, each at seeds17/23/41. Every context hashes
  after the scoped canonicalization. Sources recorded in `parent_scan.json`.
- All six saved 2015q1 contexts reproduce the original failure. Corrected
  contexts leave generated input tensors exactly unchanged. Both J_RAW and
  J_ALL_BOTH have bit-identical predictions, loss and gradients before/after
  canonicalization: **12 real-data comparisons**, recorded in
  `numerical_parity.json`.
- One full-prefix inner epoch and one fresh-final epoch at 2015q1 are tested
  for each of J_RAW/s17 and J_ALL_BOTH/s17. The native output ledgers and saved
  states are independently replayed with original tolerances. Exact outcomes
  and timing are in `smoke_checks.json`; the bounded test is not a predictive
  comparison and its forecasts are not production fits.
- New regression tests cover the missing sentinel, source nonmutation,
  finite-hash identity, invalid exposure/infinity rejection, unrelated scalar
  NaN rejection, exact versioned-source scope, original-run protection, and
  refusal to proceed without repair evidence.
- The unchanged 44-case smoke, eight full-stopping pilots and successful local
  preflight are reused only after checking original code/data/configuration
  fingerprints and completion/audit receipts. No repeated library or pilot fits.

Definitive readiness comes from `v16_metadata_fix_2026_09_19_v1/complete.json`
and the new production `preflight/complete.json`, not this narrative alone.
Durable regression log: `v16_metadata_fix_2026_09_19_v1/logs/verification.log`.
Preflight test log is under the new production directory below.

## Restart destination and commands

Use **new** destination
`experiments/cache/joint_capability_2026_09_19_v16_hashfix`.
The failed `...v16_local` run, its six original shared contexts, logs and
receipts remain unchanged. Small new shared contexts will be built in the new
production prefix; the expensive historical input/profile library is reused.

The guarded entry point is `bash experiments/run_v16_hashfix.sh check` or
`run`. Check verifies current source parity, repair evidence, storage and tests
without launching production. Run executes the same checks, then hands off to
the versioned runner. Workers use that same runner revision. Never use the old
`run_v16_local.sh` command for the repair.

After actual preflight PASS, Adam can launch:

```bash
cd /Users/adam/Documents/basketball
mkdir -p experiments/cache/joint_capability_2026_09_19_v16_hashfix/logs
nohup /usr/bin/caffeinate -i bash experiments/run_v16_hashfix.sh run >> experiments/cache/joint_capability_2026_09_19_v16_hashfix/logs/launcher.log 2>&1 < /dev/null &
echo "Launcher PID: $!"
```

Monitor:

```bash
tail -F experiments/cache/joint_capability_2026_09_19_v16_hashfix/logs/launcher.log
bash experiments/run_joint_capability_v16.sh status --run-dir experiments/cache/joint_capability_2026_09_19_v16_hashfix
bash experiments/run_joint_capability_v16.sh report --run-dir experiments/cache/joint_capability_2026_09_19_v16_hashfix --sort rmse --slice all --view half
```

The original read-only status/report CLI can read the new destination; only
training must use the repaired routing. Full training still includes the
registered downstream analyses and audit, with all 3,168 cases. No changes to
prediction/coherence/OOD acceptance, no efficacy claim from these smoke tests,
and no scorer promotion.
