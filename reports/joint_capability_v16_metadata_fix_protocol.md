# v16 missing legacy metadata repair — frozen operational protocol

2026-09-19. Adam authorized fixing the first-production-launch failure.

The old parent can legitimately record `team_baseline=NaN`, `team_rows=0`,
`team_exposure=0` before historical additive-offset observations are available.
v16 does not use this legacy denominator, but hashes the whole shared context
with strict JSON. The original production run failed before optimization.

In **new** contexts only, replace that exact NaN/zero-rows/zero-exposure sentinel
with `None` (explicitly undefined). Do not rewrite original contexts, parent
fits, observations, profiles, receipts, or fingerprints. Do not coerce unrelated
NaN/Inf values or permit a missing baseline with positive/unknown exposure.
Finite contexts remain unchanged. No model computation reads this field.

Preserve all original scientific files. Versioned copies of the case/runner
modules change only (1) new-context canonicalization and its import and (2)
routing to that case module and to the versioned worker runner. Verify exact
source-text equivalence outside these declared substitutions. The original
trainer, loss, model, optimizer, stopping, reporter, analysis and auditor execute
unchanged. New production destination and new fingerprint-bound preflight.

Reuse the original 44 audited smoke cases, eight audited full-stopping pilots,
and passing local CPU preflight, conditional on source/configuration/receipt
parity. Do not repeat the expensive historical library or pilot campaign.

Additional bounded verification: inspect all six saved failed-origin contexts;
check finite/nonsentinel hash identity and strict rejection elsewhere; compare
real first-origin predictions/losses/gradients before and after canonicalization;
run one inner and reset-final epoch of J_RAW/s17 and J_ALL_BOTH/s17 at 2015q1
using the versioned case path. Replay saved outputs, verify finite native ledgers
and selected/final length, and compare numerical output within the existing
ledger/replay tolerances. This is an operational smoke check, not a predictive
experiment. Scan all dated parent fits for the same sentinel pattern, without
refitting them. Run the existing v16 tests and new regression tests with logs.

Retain the full 22-arm/48-quarter/three-seed/3,168-case production design and
all three product standards. No scorer promotion, database work, commit, or
automatic full launch. Full training awaits Adam's own restart command.
