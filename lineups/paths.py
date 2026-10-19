"""Where local artifacts live. Everything under CACHE is untracked.

LINEUPS_CACHE (environment) replaces CACHE with another cache directory: a
rebuild root's experiments/cache (scripts/rebuild_legacy_chain.sh), so the
downstream builders read that rebuild's artifacts and write beside them.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ["LINEUPS_CACHE"]).resolve() if os.environ.get("LINEUPS_CACHE") else ROOT / "experiments" / "cache"

# The clean-data rebuild (2026-10-14/15): possessions from the pages, exact player ids
# (scripts/after_download.sh). Fixed to the main cache, whatever LINEUPS_CACHE says.
CLEAN = (Path(os.environ["LINEUPS_CLEAN"]).resolve() if os.environ.get("LINEUPS_CLEAN")      # a rehearsal root
         else ROOT / "experiments" / "cache" / "rebuild_pages_2026_10_14" / "experiments" / "cache")
# Running at the clean root (LINEUPS_CACHE = CLEAN) puts every producer in the clean-data world: its history
# (lineups.history) and the possession table its queries read (2026-10-16, reports/refresh_protocol_2026_10_16.md).
CLEAN_ROOT = CACHE == CLEAN.resolve()
POSSESSIONS_TABLE = "nba_pages.possessions" if CLEAN_ROOT else "nba.possessions"

# Origin calendar: quarter-season windows with start/stop dates.
SCHEDULE = CACHE / "asof_points_2026" / "schedule.csv"

# Pre-refactor v16 production artifacts behind the retained reference.
V16_RUN = CACHE / "joint_capability_2026_09_19_v16_fast2_ready"         # native fits and predictions
# The registered named lineups (a definition, not a fit), read from the main cache in every root
FIXTURES = ROOT / "experiments" / "cache" / V16_RUN.name / "manifest.json"
V16_SCORED = CACHE / "joint_capability_2026_09_26_v16_repaired"         # repaired calibration/scoring
V16_INPUTS = CACHE / "joint_capability_2026_09_18_v16_training_inputs_dev2"  # matchup labels (mapped arrays)
V16_CONTROLS = CACHE / "joint_capability_2026_09_18_v16_controls_dev1"  # additive controls per row
V16_LIBRARY = CACHE / "joint_capability_2026_09_18_v16_library_full1"   # adjusted capability banks
V15_ARCHIVE = CACHE / "joint_capability_2026_09_17_v15_prod"            # legacy cohort membership

# Clean input store for lineups.features (exported once from the v3/v14/v15/v16 caches).
STORE = CACHE / "lineups_store_v16"
