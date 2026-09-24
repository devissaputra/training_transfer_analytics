import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from training_transfer_analytics import core


class CoreTests(unittest.TestCase):
    def test_transfer_decay_and_barriers(self):
        index = core.transfer_index(0.8, 0.7, 0.9, 0.8)
        self.assertLess(core.retention_adjusted(index, 60), index)
        self.assertIn("manager_support", core.barrier_flags(0.2, 0.8, 0.8))

    def test_invalid_scale_is_rejected(self):
        with self.assertRaises(ValueError):
            core.transfer_index(1.2, 0.7, 0.9)


if __name__ == "__main__":
    unittest.main()
