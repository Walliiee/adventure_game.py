"""
Act 1 state: skills, time, focus. Matches docs/ACT1_DESIGN.md.
"""
from game.act1.constants import (
    SKILLS,
    BASELINE,
    PRIMARY_THRESHOLD,
    SUPPLEMENTARY_THRESHOLD,
    ACTIONS_PER_YEAR,
)


def create_act1_state(name: str) -> dict:
    """Create state for a 7-year-old character. All skills start at 0."""
    return {
        "name": name,
        "skills": {s: 0 for s in SKILLS},
        "actions": 0,
        "primary": None,
        "supplementary": [],
        "focus_chosen": False,
    }


def current_year(state: dict) -> int:
    """1, 2, or 3 based on actions so far."""
    return min(3, (state["actions"] // ACTIONS_PER_YEAR) + 1)


def all_at_baseline(state: dict) -> bool:
    return all(state["skills"][s] >= BASELINE for s in SKILLS)


def is_ready(state: dict) -> bool:
    """Ready at 10: Year 3, focus chosen, primary >= 4, both supplementary >= 3."""
    if not state["focus_chosen"] or state["primary"] is None or len(state["supplementary"]) != 2:
        return False
    if current_year(state) < 3:
        return False
    if state["skills"][state["primary"]] < PRIMARY_THRESHOLD:
        return False
    if any(state["skills"][s] < SUPPLEMENTARY_THRESHOLD for s in state["supplementary"]):
        return False
    return True
