while True: # Loop until a valid pH value is entered
    pH = int(input("Enter a pH value between 0-14: "))
    if 0 <= pH <= 14: #In this case, the compound condition checks if the pH value is greater than or equal to 0 and less than or equal to 14.
        break # Exit the loop if the pH value is valid
    else: # If the pH value is not valid, display an error message
        print("Invalid pH value. Please try again.")

if pH > 7:
    print("The solution is basic")
elif pH < 7:
    print("The solution is acidic")
else:
    print("The solution is neutral")