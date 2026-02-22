"""
CLI presentation and input: menus, prompts, banners, stats.
"""
import sys

# Use ASCII banner on Windows when console doesn't support emoji
def _safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))

from game.constants import (
    DIFFICULTY_DISPLAY,
    DIFFICULTIES,
    REGION_DISPLAY,
    REGION_ALIASES,
    NPC_DISPLAY,
)


def get_player_choice(options, aliases=None, prompt="Enter your choice: "):
    """Prompt until the player picks a valid option (by number or alias). Returns 0-based index."""
    aliases = aliases or {}
    while True:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        choice = input(prompt).strip().lower()
        if choice in {"quit", "q", "exit"}:
            print("Thanks for playing!")
            sys.exit()
        if choice in aliases:
            return aliases[choice]
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1
        print("Invalid choice. Try a number or keyword.")


def choose_difficulty() -> str:
    """Prompt for difficulty; return 'story', 'classic', or 'hardcore'."""
    print("Choose your difficulty:")
    aliases = {"story": 0, "classic": 1, "hardcore": 2, "hard": 2}
    idx = get_player_choice(DIFFICULTY_DISPLAY, aliases)
    return DIFFICULTIES[idx]


def print_banner() -> None:
    print("\n" + "=" * 58)
    print("  WILDLANDS: ORB CATCHER ADVENTURE")
    print("=" * 58)
    print("  Forest   Meadow   Ruins   River   Canyon")
    print("=" * 58)


def show_characters() -> None:
    print("\nYour crew in Ridgecamp:")
    for line in NPC_DISPLAY:
        print(line)


def display_intro(state: dict) -> None:
    print_banner()
    print(f"Welcome, {state['name']}! Difficulty: {state['difficulty'].title()}")
    print("You are an Orb Keeper. Catch small and big wild animals in circular capture orbs,")
    print("then train and play with them so they become trusted companions.")
    show_characters()
    print("\nGoal: build a balanced team and win the Ridgecamp Exhibition Match.\n")


def print_stats(state: dict) -> None:
    mini = state["balls"]["mini"]
    mega = state["balls"]["mega"]
    print(f"\n[Day {state['turn']}] Health: {state['health']} | Mini Orbs: {mini} | Mega Orbs: {mega}")
    if state["captured"]:
        print("Companions:")
        for pet in state["captured"]:
            print(f" - {pet['name']} ({pet['size']}) Lv.{pet['level']} Bond:{pet['bond']} Mood:{pet['mood']}")
    else:
        print("Companions: none yet")


DAY_MENU_OPTIONS = [
    "Explore wild region and attempt a capture",
    "Train a companion",
    "Play with a companion",
    "View stats",
    "Start exhibition match",
    "Quit adventure",
]
DAY_MENU_ALIASES = {
    "explore": 0, "train": 1, "play": 2, "stats": 3, "match": 4, "quit": 5, "q": 5,
}


def day_menu(state: dict) -> int:
    """Show camp action menu; return 0–5 (explore, train, play, stats, match, quit)."""
    return get_player_choice(
        DAY_MENU_OPTIONS, DAY_MENU_ALIASES, prompt="Choose your camp action: "
    )


def ask_replay() -> bool:
    """Ask to play again; return True for yes, False for no."""
    while True:
        response = input("\nPlay again? (y/n): ").strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")
