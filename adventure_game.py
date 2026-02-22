#!/usr/bin/env python3
"""
Launcher for Wildlands: Orb Catcher Adventure.
Run with: python adventure_game.py
Alternatively: python -m game
Quick test (defaults, no prompts): python adventure_game.py --test
"""
import io
import sys

# On Windows, console often uses cp1252; use UTF-8 so emoji and symbols print.
if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from game.main import main

if __name__ == "__main__":
    quick_test = "--test" in sys.argv or "-t" in sys.argv
    main(quick_test=quick_test)
