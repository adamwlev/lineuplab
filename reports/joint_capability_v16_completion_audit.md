# v16 training completion / post-run failure audit

Verified 2026-09-26. Source:
`experiments/cache/joint_capability_2026_09_19_v16_fast2_ready`.
Read-only checks; no source artifacts, model code or frozen producers changed.

## Training is complete

- All 3,168 configured native cases (22 arms × 48 origins × 3 seeds) pass
  `joint_capability_v16_runtime.verify_complete`, including hashes for both
  saved prediction views, event summaries, fit summaries and child receipts.
- All 6,336 inner/final fit directories were additionally verified individually:
  the checkpoint files named in their receipts pass hash verification, not
  merely the child receipt files themselves.
- All 48 fit queue summaries show 3,168 successful jobs in total, zero failed
  and zero pending. The 48 context queues show 288 successful jobs, zero failed
  and zero pending.
- All 144 ADJUSTED_CHANNEL derived cases and all 48 scored-origin receipts
  verify. Scored-output integrity does **not** establish scientific validity:
  they contain the known calibration-history defect.
- `progress.json` reached 2026q4 at 593,325.705 elapsed seconds (about 6 days,
  20 hours, 49 minutes). This is the supervisor duration through the last
  origin, not a sum of training time or the duration through the final crash.

## Final error: post-training event-report schema mismatch

The launcher log records `POINT_ANALYSIS_COMPLETE`, followed by:

```text
joint_capability_v16_analysis.py:112, in events
    exposure=ev["exposure"][family]
KeyError: 'recovery'
```

The v16 family list calls the rebound likelihood `recovery`, whereas archived
v15 `evaluation.json` uses `rebound` in both `exposure` and `families`.
Inspection of v15 `loss_statistics` and v16 `event_statistics` confirms the
same collector-category negative-log-likelihood and rebound exposure formula.
An explicit `recovery` → `rebound` alias for the archived v15 schema matches
all four event-family exposure counts in all 576 v15 control cases against
the corresponding v16 J_RAW event exposures. Do not silently skip the family
or invent zero exposure; preserve the original archived schema.

This failure occurred after the training loop and point-table generation.
The overall run, full analysis and final audit lack completion receipts.
Existing analysis directories are `points` and an incomplete `events`;
later registered stages were not reached by this invocation. The completed
point analysis uses faulty calibration and must not be interpreted as final.
Process listing was sandbox-blocked, so this audit does not independently
certify the absence of other user-started processes.

## Next execution

No NN retraining is indicated by either identified defect. Do not rerun the
old full-run command to repair reporting. First implement the versioned
[calibration repair](../MODEL_RESEARCH_ROADMAP.md#post-v16-calibration-history-repair-first),
including the explicit archived-event schema adapter and regression tests.
Regenerate leaderboard/point analyses from corrected histories, then complete
the registered event, basketball, uncertainty and independent audit stages.
Keep all original outputs and receipts unchanged; use new derived output paths
and durable verbose logs. Repaired point rankings are not a three-pillar pass.

The correction and remaining analyses have **not** been implemented or launched
by this completion audit. Noise-ceiling and ensemble supplements remain queued
behind the repaired baseline and registered review. No commit or promotion.
