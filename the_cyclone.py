# Type: Program - The Cyclone Ride
# Purpose: To determine if a person is tall enough and has enough credits to ride The Cyclone.

height = int(input("What is your height in cm? "))
credits = int(input("How many credits do you have? "))

if height >= 137 and credits >= 10:
    print("Enjoy the ride!")
elif height < 137 and credits >= 10:
    print("You are not tall enough to ride.")
elif height >= 137 and credits < 10:
    print("You don't have enough credits. You can buy more at the ticket booth.")
else:
    print("You have not met either requirement.")
