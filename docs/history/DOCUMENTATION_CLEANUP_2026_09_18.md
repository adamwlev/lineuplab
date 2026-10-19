# Documentation cleanup — 2026-09-18

Scope: reorganize current guidance before v16 implementation, preserving the
research record. The initial cleanup made no model/source changes and performed
no fitting, database work, cache rebuild, promotion, deployment, delegation or
commit. The subsequently requested documentation commit is recorded below.

## Changes

- Added a root README, current neural architecture, documentation index and
  compact research-practices guide.
- Replaced the accumulated operating/state/handoff/scorecard pages with one
  present-state view per role. MODEL_RESEARCH_ROADMAP is the canonical backlog;
  BACKLOG is a compatibility pointer to it and the old numbered record.
- Preserved seven replaced documents in the
  [dated archive](archive/2026-09-18_pre_cleanup/README.md), with SHA-256 hashes
  in its [manifest](archive/2026-09-18_pre_cleanup/manifest.json).
- Added scope banners above five legacy documents, preserving their bodies.
- Kept original reports, frozen plans and the product contract in place.
  The pre-existing uncommitted v16 plan and planning context were preserved.

## Verification

Read-only v15 status and the all-slice RMSE leaderboard were rerun successfully.
Status is ANALYSIS_COMPLETE, 576 cases; the leaderboard reproduces MAIN_RB
half RMSE 10.725732 versus old HALF+D 10.732151 on 5,607 cells / 726,364
possessions. These checks do not launch or rewrite the completed run.

Read-only preservation/navigation checks **PASS**:

- 7 archived snapshots match their pre-cleanup SHA-256 hashes and line counts.
- 5 legacy documents retain byte-identical bodies beneath the new notices.
- All 85 other previously tracked Markdown files are unchanged, including
  original reports/protocols, the product contract and supplied feedback.
- The previously untracked v16 plan is byte-identical
  (SHA-256 `3a928a6ef4e65d5eb110346cb0c816afe501fecf7c44737ee9513eeeed904203`).
- Frozen producer/protocol hashes pass: v13 77/77, v14 90/90, v15 89/89.
- All 238 local links/anchors in current authored guidance and new notices
  resolve; current-page heading spacing checks pass.
- Tracked edits are documentation only; `git diff --check` passes.

The temporary read-only verification script and captured baseline are in
`/tmp/basketball-docs-audit.N5nSIy/` (not a permanent runtime dependency).
The seven-document archive contains 7,231 preserved lines. The normal entry
path is much shorter: CLAUDE 1,108→81 lines, SESSION_HANDOFF 2,928→64,
current state 316→115. The canonical backlog is 237 lines instead of the
716-line roadmap plus a competing 1,917-line historical queue.

Architecture was checked against the v3/v9/v13/v14/v15 state, model, fitting,
control and runner code. No neural test suite or experiment was rerun for a
documentation-only change. External URLs and deployment availability were not
revalidated; dated source assessments and old private artifacts are not new
availability claims.

Historical snapshot bodies keep their original root-relative links by design.
The [current documentation index](README.md) supplies working navigation;
those exact historical links are excluded from current-page link validation.

## Restart

Use [current handoff](SESSION_HANDOFF.md). v16 remains a written plan,
without implementation, pilots or a launch command. The initial cleanup left
the documentation edits and existing v16 plan uncommitted. Adam subsequently
requested their commit; this documentation checkpoint includes both, with
generated caches excluded and untouched.
