"""Allow running the game as: python -m game"""
import io
import sys

if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from game.main import main

if __name__ == "__main__":
    main(quick_test="--test" in sys.argv or "-t" in sys.argv)
