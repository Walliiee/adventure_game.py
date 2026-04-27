"""
Main game loop: one session from intro until win, quit, or game over.
"""
from game.cli import display_intro, print_stats, day_menu
from game.world import choose_region, find_creature, describe_region, get_npc_scene
from game.capture import attempt_capture
from game.exhibition import run_exhibition
from game.companions import (
    train_companion, 
    play_with_companion, 
    pick_companion,
    use_companion_ability,
    reset_daily_abilities,
)
from game.save import save_game
from game.endings import show_ending
from game.achievements import check_achievements, show_achievement
from game.inventory import show_inventory, use_item, find_item_on_explore
from game.encounters import roll_encounter, handle_encounter
from game.npc import npc_menu


def _check_and_show_achievements(state: dict) -> None:
    """Check for newly unlocked achievements and display them."""
    newly_unlocked = check_achievements(state)
    for ach_id in newly_unlocked:
        show_achievement(ach_id)
        state["achievements_unlocked"].append(ach_id)


def _inventory_menu(state: dict) -> None:
    """Handle 'use' command at camp — show inventory and let player pick an item."""
    from game.inventory import ITEMS
    inv = state.get("inventory", {})
    non_empty = {k: v for k, v in inv.items() if v > 0}
    if not non_empty:
        print("\n🎒 Your pack is empty.")
        return
    print("\n🎒 Inventory — choose an item to use, or press Enter to go back:")
    item_ids = list(non_empty.keys())
    for i, item_id in enumerate(item_ids, 1):
        item = ITEMS[item_id]
        print(f"  {i}. {item['name']} x{non_empty[item_id]}")
    try:
        choice = input("Pick a number (or Enter to cancel): ").strip()
        if choice == "":
            return
        idx = int(choice) - 1
        if 0 <= idx < len(item_ids):
            result = use_item(state, item_ids[idx])
            print(result)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")


def _companion_ability_menu(state: dict) -> bool:
    """Let player use a companion's daily ability. Returns True if action performed."""
    if not state["captured"]:
        print("You need a companion to use an ability.")
        return False
    
    companion = pick_companion(state, "use ability")
    if not companion:
        return False
    
    result = use_companion_ability(state, companion)
    print(result)
    return True


def run_session(state: dict) -> None:
    """
    Run a single game session. Returns when the player wins, quits, or game over.
    """
    display_intro(state)

    while state["health"] > 0:
        choice = day_menu(state)
        action_performed = False

        if choice == -1:
            # 'i' — show inventory only
            show_inventory(state)
        elif choice == -2:
            # 'use' — use item menu
            _inventory_menu(state)
        elif choice == 0:
            region = choose_region(state)
            print(f"\n{describe_region(region)}")
            scene = get_npc_scene(state, region)
            if scene:
                print(scene)

            # Random encounter while traveling to region
            enc = roll_encounter(state)
            if enc and enc != "nothing":
                enc_result = handle_encounter(enc, state)
                print(f"\n⚡ {enc_result}")
                if state["health"] <= 0:
                    print("\nYou collapse from exhaustion. Your companions guard you until help arrives.")
                    show_ending(state)
                    return

            # 10% chance to find an item while exploring
            found = find_item_on_explore(state)
            if found:
                from game.inventory import ITEMS
                print(f"\n🎁 You found a {ITEMS[found]['name']} during your trek!")

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
            # Use companion ability
            action_performed = _companion_ability_menu(state)
        elif choice == 4:
            # Visit NPCs
            action_performed = npc_menu(state)
        elif choice == 5:
            print_stats(state)
        elif choice == 6:
            won, action_performed = run_exhibition(state)
            if won:
                _check_and_show_achievements(state)
                show_ending(state)
                save_game(state)
                return
        elif choice == 7:
            save_game(state)
            print("Game saved.")
            continue
        else:
            # choice == 8 (quit) or unrecognized — save and return to main
            print("You pack your gear and leave Ridgecamp. Adventure paused.")
            save_game(state)
            return

        if action_performed:
            # Reset daily abilities when a new day starts (turn increments)
            old_turn = state["turn"]
            state["turn"] += 1
            if state["turn"] > old_turn:
                reset_daily_abilities(state)
            _check_and_show_achievements(state)
            save_game(state)
        if state["health"] <= 0:
            print("\nYou collapse from exhaustion. Your companions guard you until help arrives.")
            show_ending(state)
            return
