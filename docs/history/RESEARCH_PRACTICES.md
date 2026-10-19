# Research practices and historical conventions

This is a compact interpretation guide, not a new experiment protocol.
[AGENTS](../../AGENTS.md), [CLAUDE](../../CLAUDE.md), the
[product contract](CONTEXTUAL_MODEL.md), and the relevant registered plan
govern current work. The
[original numbered rules](archive/2026-09-18_pre_cleanup/CLAUDE.md#the-rules-of-evidence)
remain available for references embedded in old source files.

## Lessons to retain

- **Temporal honesty includes selection and inputs.** Training features cannot
  use their own future outcomes just because the final model fit stops before
  evaluation. Upstream fits, feature selection, normalizers, tuning, calibration
  and reference populations each need explicit dates.
- **Exact alignment is a scientific safeguard.** A possession mask and a cell
  mask are different objects; verify IDs and rollups before fitting. When two
  implementations disagree, replay the common control to locate the difference.
- **Controls must be equally informed and capable.** A blocked penalty grid,
  different opponent information, mismatched normalizers, or extra calibration
  can manufacture an apparent mechanism gain. Print boundary diagnostics and
  check gauge/level identifiability rather than quietly choosing a floor.
- **Shrinkage complicates nulls.** A near-zero estimate with tiny variation may
  indicate excessive shrinkage or an inactive path. Check whether the model can
  express and learn the proposed effect before declaring its scientific absence.
- **Training seeds and overlapping folds are not independent samples.** Use
  paired predictions and appropriate game/season blocks; report uncertainty
  and multiplicity/selection limitations. Do not stop at a favorable partial run.
- **Ceiling and reliability estimates are conditional on their rig.** Upstream
  common-fit error can inflate or reverse split-half covariance. The historical
  four-way, game-disjoint design addresses that specific contamination. It is
  not a universal hard ceiling on richer information or a different target.
- **Mean, mechanism and uncertainty are different claims.** A valid point
  identity does not establish causal attribution. A well-calibrated finite-game
  band does not establish latent/OOD quality coverage. Diagnostic oracle/context
  substitutions are not available forecasts.
- **Match the basketball claim to the contrast.** Counterfactual totals,
  contextual increments and native event contributions are not interchangeable.
  Do not tune a result until a famous-player comparison has the desired sign.
- **Name what changed.** Era adjustment and recency were once bundled; separate
  their controls. A decoder change, a new target, a different loss scale and a
  broader population must not be silently credited to one another.

## Conventions that are not universal

| Historical statement | Correct present interpretation |
| --- | --- |
| “Always detrend by season/week and home advantage” | Required for particular older possession/variance rigs; current raw lineup-quarter point evaluation uses its registered target and prior calibration, not future-week detrending |
| “Effects are about 10⁻⁴ r²” | Scale of older possession-level incremental effects, not a limit on aggregated-lineup raw r² |
| “A point evaluation with power must precede any model work” | Historical diagnosis, later qualified; current paired point, event, population and mechanism readouts proceed together |
| “Inputs/architecture/defense are closed” | Negative evidence about specific tested inputs, structures and targets, not all later mechanisms |
| “A coverage gate is the finished answer” | Legacy shipped-page behavior; explicitly not the contextual product contract |
| “A parameter on a grid boundary settles the result” | A warning requiring the registered diagnostic/selection rules, not permission for outcome-driven retuning |
| “A private artifact page is the standing state” | A historical exported copy; repository current pages are authoritative and no republishing is implied |

## Following old code references

Old “CLAUDE rule 9” means upstream fits inside the split; rule 10 concerns
unshrinking/nested-control capacity; rule 12 concerns unaudited default grids.
Their wording and examples are preserved in the archive. New CLAUDE numbering
is deliberately not used to reinterpret those historical comments.

The [research journal](RESEARCH_OVERVIEW.md) and
[old backlog](archive/2026-09-18_pre_cleanup/BACKLOG.md) retain detailed examples,
including failed methods. Read them when the relevant failure mode is in scope,
not as a mandatory restart sequence.
