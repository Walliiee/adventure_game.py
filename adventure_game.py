import sys # Import the sys module to use the sys.exit() function

def display_intro():
    print("Welcome to the Mini Adventure Game!")
    print("You find yourself at a crossroads in a mysterious forest.")
    print("Your choices will determine your fate. Choose wisely!\n")

def get_player_choice(options): # This function takes a list of options and returns the player's choice
    while True:
        for i, option in enumerate(options, 1): # Loop through the options and print them with a number. Enumerate is used to get the index of the option 
            print(f"{i}. {option}")
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options): # Check if the input is a valid number. Len is the length of the list
            return int(choice) - 1 # Convert the input to an integer and return the index of the choice
        print("Invalid choice. Please try again.")

def game_over(message):
    print(message)
    print("Game Over. Thanks for playing!")
    sys.exit()

def start_game():
    display_intro()
    
    # First decision
    print("You see two paths ahead and a tall tree nearby:")
    options = ["Take the dark, overgrown path", "Follow the well-lit, clear trail", "Climb a nearby tree to get a better view"]
    choice = get_player_choice(options)
    
    if choice == 0:
        dark_path()
    elif choice == 1:
        clear_trail()
    else:
        climb_tree()

def dark_path():
    print("\nYou venture into the dark, overgrown path.")
    print("As you push through the thick vegetation, you hear strange noises...")
    options = ["Investigate the noise", "Try to quietly backtrack"]
    choice = get_player_choice(options)
    
    if choice == 0:
        game_over("You investigate and disturb a sleeping bear. It doesn't end well.")
    else:
        print("\nYou successfully backtrack and find yourself at the crossroads again.")
        clear_trail()

def clear_trail():
    print("\nYou follow the well-lit, clear trail.")
    print("After walking for a while, you come across a mysterious old house.")
    options = ["Enter the house", "Continue past the house"]
    choice = get_player_choice(options)
    
    if choice == 0:
        enter_house()
    else:
        game_over("You continue past the house and eventually find your way out of the forest. You win!")

def climb_tree():
    print("\nYou decide to climb the tall tree to get a better view.")
    print("After a challenging climb, you reach the top and survey the landscape.")
    print("\nFrom your vantage point, you can see:")
    print("1. The dark, overgrown path leads into a dense forest. You spot what looks like")
    print("   old ruins peeking through the trees in the distance.")
    print("2. The well-lit, clear trail winds through a meadow. You can see a small village")
    print("   at the end of this path, with smoke rising from chimneys.")
    print("\nArmed with this new information, you climb back down to make your choice.")
    
    options = ["Take the dark path towards the mysterious ruins", 
               "Follow the clear trail to the village"]
    choice = get_player_choice(options)
    
    if choice == 0:
        dark_path()
    else:
        clear_trail()

def enter_house():
    print("\nYou enter the old house. It's dark and dusty inside.")
    print("You see a glinting object on a table and a staircase leading upstairs.")
    options = ["Examine the glinting object", "Go upstairs"]
    choice = get_player_choice(options)
    
    if choice == 0:
        game_over("It's a magical amulet! Its power teleports you to safety. You win!")
    else:
        game_over("The stairs were weak and collapsed under you. Game over!")

if __name__ == "__main__":
    start_game()