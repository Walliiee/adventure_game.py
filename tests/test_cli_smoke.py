import subprocess
import sys
import unittest


class TestCliSmoke(unittest.TestCase):
    def test_test_mode_quit_path(self):
        proc = subprocess.run(
            [sys.executable, "adventure_game.py", "--test"],
            input="6\nn\n",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Welcome to Wildlands", proc.stdout)
        self.assertIn("Adventure paused", proc.stdout)


if __name__ == "__main__":
    unittest.main()
