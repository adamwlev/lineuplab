"""A cheap epoch marker that prevents experiments from reading stale caches.

The possession caches were historically keyed only by requested date bounds.
Appending games to PostgreSQL therefore left every experiment silently reading
the old corpus.  The updater bumps this marker *before* its first database
write; cache keys and fixed-name aggregate caches include/verify the epoch.
"""
from __future__ import annotations

import os
import tempfile
import time
import uuid
from pathlib import Path

from lineups.paths import CACHE


EPOCH_FILE = CACHE / "data_epoch.txt"


def current_data_epoch() -> str:
    try:
        return EPOCH_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        # Legacy caches predate the marker and remain valid until the first
        # updater write.  This avoids an unnecessary 5+ GB rebuild today.
        return ""


def bump_data_epoch() -> str:
    epoch = f"{time.time_ns()}-{uuid.uuid4().hex[:12]}"
    EPOCH_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=EPOCH_FILE.name + ".", suffix=".tmp", dir=EPOCH_FILE.parent)
    os.close(fd)
    try:
        Path(tmp_name).write_text(epoch + "\n", encoding="utf-8")
        os.replace(tmp_name, EPOCH_FILE)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
    return epoch


def artifact_is_current(path: str | Path) -> bool:
    epoch = current_data_epoch()
    if not epoch:
        return Path(path).exists()
    try:
        stored = Path(str(path) + ".epoch").read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return False
    return Path(path).exists() and stored == epoch


def stamp_artifact(path: str | Path) -> None:
    epoch = current_data_epoch()
    marker = Path(str(path) + ".epoch")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(epoch + "\n", encoding="utf-8")
