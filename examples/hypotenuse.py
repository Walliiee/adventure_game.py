import math

# Ask the user for input
a = float(input("Enter the length of side a: "))
b = float(input("Enter the length of side b: "))

# Calculate the hypotenuse using the Pythagorean theorem
c = math.sqrt(a**2 + b**2)

# Print the result
print("The length of the hypotenuse is:", c)