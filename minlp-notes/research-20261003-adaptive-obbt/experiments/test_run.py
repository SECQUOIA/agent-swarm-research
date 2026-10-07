"""Research provenance survives resuming an interrupted worker."""
from pathlib import Path
import tempfile
import unittest

from run import archive_incomplete_attempt


class ResumeTests(unittest.TestCase):
    def test_incomplete_raw_and_log_are_preserved_before_retry(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "raw").mkdir()
            (root / "logs").mkdir()
            for index in (1, 2):
                (root / "raw/task.json").write_text('{"attempt": '+str(index)+'}')
                (root / "logs/task.log").write_text("partial log "+str(index))
                archive_incomplete_attempt(root, "task")
                target = root / "attempts/task" / f"attempt-{index:03d}"
                self.assertIn(str(index), (target / "task.json").read_text())
                self.assertEqual((target / "task.log").read_text(), "partial log "+str(index))
                self.assertFalse((root / "raw/task.json").exists())
                self.assertFalse((root / "logs/task.log").exists())


if __name__ == "__main__":
    unittest.main()
