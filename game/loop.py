"""
Main game loop: one session from intro until win, quit, or game over.
"""
from game.cli import display_intro, print_stats, day_menu
from game.world import choose_region, find_creature, describe_region, get_npc_scene
from game.capture import attempt_capture
from game.companions import train_companion, play_with_companion, run_exhibition
from game.save import save_game, load_game, has_save
from game.endings import show_ending
from game.achievements import check_achievements, show_achievement


def start_game(fresh_state_factory) -> dict:
    """Handle save loading at game start, or create a fresh state."""
    if has_save():
        response = input("Continue your adventure? [y/n]: ").strip().lower()
        if response in {"y", "yes"}:
            state = load_game()
            if state is not None:
                print(f"Welcome back, {state['name']}! Loading save on Day {state['turn']}...")
                return state
            else:
                print("Save file corrupted. Starting a fresh adventure.")
        elif response in {"n", "no"}:
            print("Starting a new adventure!")
        else:
            print("Starting a new adventure!")
    return fresh_state_factory()


def _check_and_show_achievements(state: dict) -> None:
    """Check for newly unlocked achievements and display them."""
    newly_unlocked = check_achievements(state)
    for ach_id in newly_unlocked:
        show_achievement(ach_id)
        state["achievements_unlocked"].append(ach_id)


def run_session(state: dict) -> None:
    """
    Run a single game session. Returns when the player wins, quits, or game over.
    """
    display_intro(state)

    while state["health"] > 0:
        choice = day_menu(state)
        action_performed = False

        if choice == 0:
            region = choose_region(state)
            print(f"\n{describe_region(region)}")
            scene = get_npc_scene(state, region)
            if scene:
                print(scene)

            creature = find_creature(region)
            print(
                f"\nYou discover a {creature['size']} wild animal: {creature['name']} "
                f"({creature['temperament']})."
            )
            attempt_capture(state, creature)
            action_performed = True
        elif choice == 1:
            action_performed = train_companion(state)
        elif choice == 2:
            action_performed = play_with_companion(state)
        elif choice == 3:
            print_stats(state)
        elif choice == 4:
            won, action_performed = run_exhibition(state)
            if won:
                _check_and_show_achievements(state)
                show_ending(state)
                save_game(state)
                return
        elif choice == 5:
            save_game(state)
            print("Game saved.")
            continue
        else:
            print("You pack your gear and leave Ridgecamp. Adventure paused.")
            save_game(state)
            return

        if action_performed:
            state["turn"] += 1
            _check_and_show_achievements(state)
            save_game(state)
        if state["health"] <= 0:
            print("\nYou collapse from exhaustion. Your companions guard you until help arrives.")
            show_ending(state)
            return
