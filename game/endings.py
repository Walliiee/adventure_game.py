"""
Endings system: 6 distinct endings based on playstyle.
"""
from __future__ import annotations
from typing import TypedDict

from game.constants import REGION_IDS


class EndingData(TypedDict):
    title: str
    message: str
    flavor_text: str


ENDINGS: dict[str, EndingData] = {
    "master_keeper": {
        "title": "The Master Keeper",
        "message": "Your companions follow you anywhere.",
        "flavor_text": "You caught 8+ creatures and built a strongly bonded core. Ridgecamp remembers your name."
    },
    "legend": {
        "title": "The Legend",
        "message": "They'll be telling this story for generations.",
        "flavor_text": "A perfect exhibition score. The crowd will never forget what they witnessed."
    },
    "explorer": {
        "title": "The Explorer",
        "message": "You mapped the whole of Ridgecamp.",
        "flavor_text": "Every region holds your footprints. No corner of this land remains hidden to you."
    },
    "gentle_one": {
        "title": "The Gentle One",
        "message": "Not every adventure ends with a trophy.",
        "flavor_text": "You left more creatures than you caught. Respect lives in the memory of those you let pass."
    },
    "dropout": {
        "title": "The Dropout",
        "message": "Some journeys end before they begin.",
        "flavor_text": "Fewer than 3 creatures caught. Perhaps this wasn't your path... or perhaps it begins again."
    },
    "default": {
        "title": "Keeper",
        "message": "A keeper's work is never done.",
        "flavor_text": "You competed and you endured. The badge is yours, but the calling continues."
    }
}


def determine_ending(state: dict) -> str:
    """
    Determine which ending the player receives based on their playstyle.
    Priority order: Legend > Master Keeper > Explorer > Gentle One > Dropout > Default
    """
    captured = state.get("captured", [])
    peaceful_leaves = state.get("peaceful_leaves", 0)
    region_progress = state.get("region_progress", set())
    exhibition_perfect = state.get("exhibition_perfect_win", False)
    all_regions = set(REGION_IDS)
    
    # Check for Legend: perfect exhibition score
    if exhibition_perfect:
        return "legend"
    
    # Check for Master Keeper: a big roster (8+) with a strongly bonded core (4+ at max bond).
    if len(captured) >= 8 and sum(1 for c in captured if c.get("bond", 0) >= 5) >= 4:
        return "master_keeper"
    
    # Check for Explorer: visited all regions
    if region_progress >= all_regions:
        return "explorer"
    
    # Check for Gentle One: left more than caught
    if peaceful_leaves > len(captured) and peaceful_leaves > 0:
        return "gentle_one"
    
    # Check for Dropout: fewer than 3 creatures
    if len(captured) < 3:
        return "dropout"
    
    # Default ending
    return "default"


def show_ending(state: dict) -> None:
    """Display the ending with some flair."""
    ending_key = determine_ending(state)
    ending = ENDINGS[ending_key]
    
    print("\n" + "=" * 50)
    print(f"  {ending['title'].upper()}")
    print("=" * 50)
    print(f"\n  \"{ending['message']}\"")
    print(f"\n  {ending['flavor_text']}")
    print("\n" + "=" * 50)
    
    # Show achievement summary if any unlocked
    achievements_unlocked = state.get("achievements_unlocked", [])
    if achievements_unlocked:
        print(f"\n  🏆 Achievements Unlocked: {len(achievements_unlocked)}/8")
        from game.achievements import ACHIEVEMENTS
        for ach_id in achievements_unlocked:
            ach = ACHIEVEMENTS.get(ach_id)
            if ach:
                print(f"     • {ach['title']}")
    print("=" * 50 + "\n")
