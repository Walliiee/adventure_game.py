"""
Act 1 state: skills, time, focus. Matches docs/ACT1_DESIGN.md.
"""
from __future__ import annotations

from typing import TypedDict

from game.act1.constants import (
    SKILLS,
    BASELINE,
    PRIMARY_THRESHOLD,
    SUPPLEMENTARY_THRESHOLD,
    ACTIONS_PER_YEAR,
)


class Act1State(TypedDict):
    name: str
    skills: dict[str, int]
    actions: int
    primary: str | None
    supplementary: list[str]
    focus_chosen: bool
    last_question_idx: dict[str, int]
    wrong_streak: int


def create_act1_state(name: str) -> Act1State:
    """Create state for a 7-year-old character. All skills start at 0."""
    return {
        "name": name,
        "skills": {s: 0 for s in SKILLS},
        "actions": 0,
        "primary": None,
        "supplementary": [],
        "focus_chosen": False,
        "last_question_idx": {},
        "wrong_streak": 0,
    }


def current_year(state: Act1State) -> int:
    """1, 2, or 3 based on actions so far."""
    return min(3, (state["actions"] // ACTIONS_PER_YEAR) + 1)


def all_at_baseline(state: Act1State) -> bool:
    return all(state["skills"][s] >= BASELINE for s in SKILLS)


def focus_thresholds_met(state: Act1State) -> bool:
    """Return True when focus has been chosen and skill thresholds are met."""
    if not state["focus_chosen"] or state["primary"] is None or len(state["supplementary"]) != 2:
        return False
    if state["skills"][state["primary"]] < PRIMARY_THRESHOLD:
        return False
    if any(state["skills"][s] < SUPPLEMENTARY_THRESHOLD for s in state["supplementary"]):
        return False
    return True


def actions_until_year_three(state: Act1State) -> int:
    """Actions remaining until Year 3 begins (age 10 threshold)."""
    year_three_start = ACTIONS_PER_YEAR * 2
    return max(0, year_three_start - state["actions"])


def is_ready(state: Act1State) -> bool:
    """Ready at 10: Year 3, focus chosen, primary >= 4, both supplementary >= 3."""
    if not focus_thresholds_met(state):
        return False
    if current_year(state) < 3:
        return False
    return True
