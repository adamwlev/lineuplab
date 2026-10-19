import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import lineups.data_version as version


class DataVersionTests(unittest.TestCase):
    def test_epoch_bump_invalidates_and_stamp_restores_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "artifact.pkl"
            artifact.write_bytes(b"cache")
            with patch.object(version, "EPOCH_FILE", Path(tmp) / "epoch.txt"):
                before = version.current_data_epoch()
                self.assertTrue(version.artifact_is_current(artifact))
                version.bump_data_epoch()
                self.assertNotEqual(version.current_data_epoch(), before)
                self.assertFalse(version.artifact_is_current(artifact))
                version.stamp_artifact(artifact)
                self.assertTrue(version.artifact_is_current(artifact))


if __name__ == "__main__":
    unittest.main()
