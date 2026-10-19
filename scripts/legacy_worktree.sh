#!/usr/bin/env bash
# Run pre-refactor code (tag pre-refactor-2026-10-09) without touching this tree.
#
# Creates ../basketball-legacy as a git worktree of the tag and points its
# experiments/cache at this repository's cache, so old builders read and write
# the same local artifacts. Old code writes there too: give it new output prefixes.
#
#   bash scripts/legacy_worktree.sh            # create (idempotent)
#   cd ../basketball-legacy && PYTHONPATH=. /Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.<module> ...
#   bash scripts/legacy_worktree.sh remove     # remove the worktree
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LEGACY="$(dirname "$ROOT")/basketball-legacy"
if [[ "${1:-}" == "remove" ]]; then
  git -C "$ROOT" worktree remove --force "$LEGACY"
  exit 0
fi
if [[ ! -d "$LEGACY" ]]; then
  git -C "$ROOT" worktree add --detach "$LEGACY" pre-refactor-2026-10-09
  rm -rf "$LEGACY/experiments/cache"
  ln -s "$ROOT/experiments/cache" "$LEGACY/experiments/cache"
fi
echo "legacy worktree: $LEGACY (cache -> $ROOT/experiments/cache)"
