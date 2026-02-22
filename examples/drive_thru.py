# Order food from a drive-thru menu, using functions and loops to manage the order process.
# It's from Jack in the Box, but you can modify it to match your favorite drive-thru menu.

def get_item(a):
    if a == 1:
        return "Jumbo Jack"
    elif a == 2:
        return "Sourdough Jack"
    elif a == 3:
        return "Ultimate Cheeseburger"
    elif a == 4:
        return "Oreo Milkshake"
    elif a == 5:
        return "Curly Fries"
    elif a == 6:
        return "Egg Rolls"
    elif a == 7:
        return "Tacos"
    else:
        return "Invalid item number"
    
def get_price(a):
    if a == 1:
        return 4.99
    elif a == 2:
        return 5.99
    elif a == 3:
        return 6.99
    elif a == 4:
        return 3.99
    elif a == 5:
        return 2.99
    elif a == 6:
        return 3.99
    elif a == 7:
        return 1.99
    else:
        return 0.0

def main():
    print("Welcome to Jack in the Box!")
    print("Here are the available items:")
    print("1. Jumbo Jack - $4.99")
    print("2. Sourdough Jack - $5.99")
    print("3. Ultimate Cheeseburger - $6.99")
    print("4. Oreo Milkshake - $3.99")
    print("5. Curly Fries - $2.99")
    print("6. Egg Rolls - $3.99")
    print("7. Tacos - $1.99")
    
    total_price = 0.0
    while True:
        try:
            item_number = int(input("Enter the item number (1-7) or 0 to finish: "))
            if item_number == 0:
                break
            item_name = get_item(item_number)
            item_price = get_price(item_number)
            if item_name == "Invalid item number":
                print(item_name)
            else:
                print(f"Added {item_name} - ${item_price:.2f}")
                total_price += item_price
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print(f"Total price: ${total_price:.2f}")

if __name__ == "__main__":
    main()