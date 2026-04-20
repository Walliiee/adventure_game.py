"""
CLI presentation and input: menus, prompts, banners, stats.
"""
import sys

from game.constants import (
    DIFFICULTY_DISPLAY,
    DIFFICULTIES,
    NPC_DISPLAY,
)


# Use ASCII fallback when console doesn't support unicode output.
def _safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


def get_player_choice(options, aliases=None, prompt="Enter your choice: "):
    """Prompt until the player picks a valid option (by number or alias). Returns 0-based index."""
    aliases = aliases or {}
    while True:
        for i, option in enumerate(options, 1):
            _safe_print(f"{i}. {option}")
        choice = input(prompt).strip().lower()
        if choice in {"quit", "q", "exit"}:
            _safe_print("Thanks for playing!")
            sys.exit()
        if choice in aliases:
            return aliases[choice]
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1
        _safe_print("Invalid choice. Try a number or keyword.")


def choose_difficulty() -> str:
    """Prompt for difficulty; return 'story', 'classic', or 'hardcore'."""
    _safe_print("Choose your difficulty:")
    aliases = {"story": 0, "classic": 1, "hardcore": 2, "hard": 2}
    idx = get_player_choice(DIFFICULTY_DISPLAY, aliases)
    return DIFFICULTIES[idx]


def print_banner() -> None:
    _safe_print("\n" + "=" * 58)
    _safe_print("  WILDLANDS: ORB CATCHER ADVENTURE")
    _safe_print("=" * 58)
    _safe_print("  Forest   Meadow   Ruins   River   Canyon")
    _safe_print("=" * 58)


def show_characters() -> None:
    _safe_print("\nYour crew in Ridgecamp:")
    for line in NPC_DISPLAY:
        _safe_print(line)


def display_intro(state: dict) -> None:
    print_banner()
    _safe_print(f"Welcome, {state['name']}! Difficulty: {state['difficulty'].title()}")
    _safe_print("You are an Orb Keeper. Catch small and big wild animals in circular capture orbs,")
    _safe_print("then train and play with them so they become trusted companions.")
    show_characters()
    _safe_print("\nGoal: build a balanced team and win the Ridgecamp Exhibition Match.\n")


def print_stats(state: dict) -> None:
    mini = state["balls"]["mini"]
    mega = state["balls"]["mega"]
    coins = state.get("coins", 0)
    _safe_print(f"\n[Day {state['turn']}] Health: {state['health']} | Mini Orbs: {mini} | Mega Orbs: {mega} | Coins: {coins}")
    if state["captured"]:
        _safe_print("Companions:")
        for pet in state["captured"]:
            personality = pet.get("personality", "brave")
            ability_status = "✓" if not pet.get("ability_used_today", False) else "✗"
            _safe_print(f" - {pet['name']} ({pet['size']}, {personality}) Lv.{pet['level']} Bond:{pet['bond']} Mood:{pet['mood']} [Ability:{ability_status}]")
    else:
        _safe_print("Companions: none yet")


DAY_MENU_OPTIONS = [
    "Explore wild region and attempt a capture",
    "Train a companion",
    "Play with a companion",
    "Use companion ability (once per day)",
    "View stats",
    "Start exhibition match",
    "Save game",
    "Quit adventure",
]
DAY_MENU_ALIASES = {
    "explore": 0, "train": 1, "play": 2, "ability": 3, "stats": 4, "match": 5, "save": 6, "quit": 7, "q": 7, "i": -1, "use": -2,
}


def day_menu(state: dict) -> int:
    """Show camp action menu; return 0–7 (explore, train, play, ability, stats, match, save, quit)."""
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
        _safe_print("Please enter 'y' or 'n'.")
