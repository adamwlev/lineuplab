# Completed optimizer-restart retirement — 2026-09-30

## Scope and rationale

Adam authorized removing completed runs' obsolete optimizer restart artifacts,
after fixing verification. This maintenance does not change model predictions,
research conclusions or any of the three product standards. No full training
run or commit is part of this task.

The original verifier is itself fingerprinted into v16/v18/v19 sources. Editing
it or rewriting old `complete.json` receipts would invalidate frozen provenance.
Instead, `experiments/artifact_retention.py` provides an explicit, separately
sealed retirement ledger and opt-in verification. Original producer code,
completion receipts and retained scientific bytes remain unchanged.

Eligible roots:

- `experiments/cache/joint_capability_2026_09_19_v16_fast2_ready`
- `experiments/cache/joint_capability_2026_09_27_v17_prod`
- `experiments/cache/joint_capability_2026_09_28_v18_prod`

Only `resume_0.pt` and `resume_1.pt` in completed inner/final fit directories are
eligible. Final weights, averaging checkpoints, predictions, optimizer-slot
receipts, historical journals, curves and run metadata are retained. Removed
restart payloads are not recoverable from the metadata ledger.

## Verification protocol

1. Verify all original target fits and parent cases before planning deletion.
2. Test strict protection of retained data, exact authorization, stale manifests,
   partial-cleanup recovery, writer locks, path safety and fresh-process wrapper.
3. Capture a real v16 case-preview table before cleanup.
4. Apply the exact sealed plan with exclusive fit locks and durable authorization.
5. Audit every retained fit and parent case; verify v19's frozen producer hashes,
   existing source receipts, all 288 teachers and all seven untouched pilots.
6. Repeat the original preview through retention mode; require identical output
   after removing only the explicit retention-mode banner.

Initial focused verification: 21 tests pass (18 new retention tests plus three
existing runtime tests). Durable log: `experiments/cache/retention_tests1.log`.

## Operational compatibility

[Usage and safety contract](../docs/history/ARTIFACT_RETENTION.md) documents the required
wrapper. Original strict verification deliberately does NOT silently accept
missing files. New multiprocess launchers must explicitly wrap each child; the
forthcoming v19 launcher must include this in its acceptance checks.

Ledger prefix: `experiments/cache/completed_resume_retention_2026_09_30`.
Preparation log: same prefix plus `_prepare.log`.
## Executed results

| Production root | Completed fits | Restart payloads removed | Allocated GiB removed |
| --- | ---: | ---: | ---: |
| v16_fast2_ready | 6,336 | 12,562 | 9.0652 |
| v17_prod | 1,440 | 2,855 | 1.3975 |
| v18_prod | 2,016 | 4,003 | 2.3681 |
| Total | 9,792 | 19,420 | 12.8308 |

Some very short fits only created one restart slot. The 288 skipped phase paths
are the inner/final paths of v16's 144 non-NN control cases, not deleted partial
training jobs. No v19 artifact was retired.

The apply preflight reverified all fits and case receipts before authorization.
All 9,792 fits also passed retained verification immediately after removal.
Physical free space rose from 54.2330 to 67.0232 GiB during apply: **12.7902 GiB
net increase**. Allocated-file bytes and the disk's net change can differ because
of filesystem accounting and other activity. No external backup of the deleted
optimizer payloads was made; the ledger preserves hashes, not their contents.

Sealed plan SHA256:
`825e76b9b847ab3b3ea046b5b302cac772d093a4c6f32be6e3319be7af826cd2`.
The plan, fsynced authorization and final counts reside in the ledger prefix.
Apply log: `experiments/cache/completed_resume_retention_2026_09_30_apply.log`.

The explicit compatibility audit passed all **288 v19 teacher fits, seven
untouched pilot cases and 129 frozen code-file hashes**, together with v19's
existing source/input receipts. Log: same prefix plus `_compatibility.log`.

The real 2016q1/J_POINT_BOTH/s17 preview (187 cells / 23,039 possessions) is
text-identical before/after after stripping ONLY the retention-mode banner.
For example, half r² remains .108676 and RMSE 10.824984; all other printed views
and controls match too. This is a maintenance invariance check, not new evidence
of predictive improvement. Logs: `retention_preview_before.log` and
`retention_preview_after.log` under `experiments/cache/`.

The 21 focused tests passed again in `experiments/cache/retention_tests2.log`.
The separate exhaustive post-cleanup audit **passed all 9,792 fits and 4,896
cases**, with exactly 19,420 authorized absences and zero remaining restart
payloads on the list. It is recorded in the ledger prefix's `_audit.log`.

## Remaining v19 readiness work

Storage is improved, not automatically accepted for the full run. With the old
47.257 GiB native-artifact estimate and 10 GiB reserve, current headroom leaves
roughly 9.77 GiB for downstream outputs, temporary peaks and all other activity.
The previous estimate excluded these. Complete measured all-in disk/runtime
acceptance and scoring/downstream integration before launch. Original storage
report remains unchanged; no automatic launch or protocol change occurred.
