def distance_to_miles(distance):
    miles = distance * 0.621371
    print(f"The distance in miles is: {miles}")

distance = float(input("Enter the distance in kilometers: "))
distance_to_miles(distance)


def distance_to_miles(distance): # Function to convert distance from kilometers to miles 
  return distance / 1.609

answer = distance_to_miles(10000) # Convert 10000 kilometers to miles.
print(answer)