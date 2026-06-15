"""JSON save/load system for Wildlands."""
from __future__ import annotations

import json
from pathlib import Path

from game.state import GameState

DEFAULT_SAVE_PATH = Path.home() / ".wildlands_save.json"


def _serialize(state: GameState) -> dict:
    """Convert sets to sorted lists for JSON compatibility."""
    out = dict(state)
    out["region_progress"] = sorted(state["region_progress"])
    out["seen_npc_scenes"] = sorted(state["seen_npc_scenes"])
    out["regions_visited"] = sorted(state.get("regions_visited", set()))
    return out


def _deserialize(data: dict) -> GameState:
    """Convert lists back to sets."""
    data["region_progress"] = set(data.get("region_progress", []))
    data["seen_npc_scenes"] = set(data.get("seen_npc_scenes", []))
    data["regions_visited"] = set(data.get("regions_visited", []))
    # Ensure every field the engine reads has a default, so older/partial saves
    # (written before a field existed) don't KeyError on first access after load.
    data.setdefault("peaceful_leaves", 0)
    data.setdefault("exhibition_perfect_win", False)
    data.setdefault("exhibition_won", False)
    data.setdefault("achievements_unlocked", [])
    data.setdefault("coins", 0)
    data.setdefault("inventory", {})
    # balls/npc_bond are indexed by fixed keys, so populate each key (not just the
    # top-level dict) or a capture/train would KeyError on a partial old save.
    balls = data.setdefault("balls", {})
    balls.setdefault("mini", 0)
    balls.setdefault("mega", 0)
    npc_bond = data.setdefault("npc_bond", {})
    from game.constants import NPC_NAMES
    for name in NPC_NAMES:
        npc_bond.setdefault(name, 0)
    data.setdefault("primary_skill", None)
    data.setdefault("supplementary_skills", [])
    data.setdefault("companion_energized", False)
    return data


def save_game(state: GameState, path: Path | None = None) -> None:
    """Persist game state to JSON. Never crashes the session on an I/O error."""
    path = path or DEFAULT_SAVE_PATH
    try:
        path.write_text(json.dumps(_serialize(state), indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"⚠️  Could not save game ({exc}). Continuing without saving.")


def load_game(path: Path | None = None) -> GameState | None:
    """Load game state from JSON. Returns None if missing or corrupted."""
    path = path or DEFAULT_SAVE_PATH
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return _deserialize(data)
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def has_save(path: Path | None = None) -> bool:
    """Check whether a save file exists."""
    path = path or DEFAULT_SAVE_PATH
    return path.exists()
