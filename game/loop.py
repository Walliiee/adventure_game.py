"""
Main game loop: one session from intro until win, quit, or game over.
"""
from game.cli import display_intro, print_stats, day_menu
from game.world import choose_region, find_creature, describe_region, get_npc_scene
from game.capture import attempt_capture
from game.companions import train_companion, play_with_companion, run_exhibition


def run_session(state: dict) -> None:
    """
    Run a single game session. Returns when the player wins, quits, or game over.
    """
    display_intro(state)

    while state["health"] > 0:
        choice = day_menu(state)

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
        elif choice == 1:
            train_companion(state)
        elif choice == 2:
            play_with_companion(state)
        elif choice == 3:
            print_stats(state)
            continue
        elif choice == 4:
            if run_exhibition(state):
                return
        else:
            print("You pack your gear and leave Ridgecamp. Adventure paused.")
            return

        state["turn"] += 1
        if state["health"] <= 0:
            print("\nYou collapse from exhaustion. Your companions guard you until help arrives.")
            return
