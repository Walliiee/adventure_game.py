"""Each of these operations is encapsulated in its own function, and the main() function calls them all to demonstrate their usage.
To run this program, you can copy the code into a Python file and execute it. 
The program will create a file named example.txt in the same directory to demonstrate file operations."""

import math
import random
import json

def string_operations():
    # String manipulation
    text = "Hello, World!"
    print(f"Original text: {text}")
    print(f"Uppercase: {text.upper()}")
    print(f"Lowercase: {text.lower()}")
    print(f"Capitalized: {text.capitalize()}")
    print(f"Replaced: {text.replace('World', 'Python')}")
    print(f"Split: {text.split(',')}")

def list_operations():
    # List operations
    numbers = [1, 2, 3, 4, 5]
    print(f"Original list: {numbers}")
    numbers.append(6)
    print(f"After append: {numbers}")
    numbers.extend([7, 8])
    print(f"After extend: {numbers}")
    numbers.insert(0, 0)
    print(f"After insert: {numbers}")
    popped = numbers.pop()
    print(f"Popped element: {popped}")
    print(f"After pop: {numbers}")
    print(f"Sorted list: {sorted(numbers, reverse=True)}")

def dictionary_operations():
    # Dictionary operations
    person = {"name": "John", "age": 30, "city": "New York"}
    print(f"Original dictionary: {person}")
    person["job"] = "Developer"
    print(f"After adding a key: {person}")
    print(f"Keys: {person.keys()}")
    print(f"Values: {person.values()}")
    print(f"Items: {person.items()}")

def file_operations():
    # File operations
    with open("example1.txt", "w") as f: # Open a file in write mode
        f.write("This is an example file.\n") # Write a line to the file 
        f.write("It demonstrates file operations in Python.") 
    
    with open("example1.txt", "r") as f: # 'r' is the default mode for open() function so it can be omitted here
        content = f.read() # Read the entire file
        print(f"File contents:\n{content}") # Print the file contents 

def math_operations():
    # Math operations
    print(f"Square root of 16: {math.sqrt(16)}")
    print(f"Ceiling of 3.7: {math.ceil(3.7)}")
    print(f"Floor of 3.7: {math.floor(3.7)}")
    print(f"Factorial of 5: {math.factorial(5)}") # 5! = 5*4*3*2*1 = 120
    print(f"Random number between 1 and 10: {random.randint(1, 10)}") 

def json_operations(): # JSON operations are demonstrated here
    # JSON operations
    data = {"name": "Alice", "age": 25, "city": "London"} # Sample data
    json_string = json.dumps(data) # Convert data to JSON string 
    print(f"JSON string: {json_string}") # Print JSON string
    parsed_data = json.loads(json_string) # Parse JSON string back to data
    print(f"Parsed JSON: {parsed_data}") # Print parsed data

def main():
    print("Demonstrating common Python functions:\n")
    string_operations()
    print("\n" + "-"*40 + "\n")
    list_operations()
    print("\n" + "-"*40 + "\n")
    dictionary_operations()
    print("\n" + "-"*40 + "\n")
    file_operations()
    print("\n" + "-"*40 + "\n")
    math_operations()
    print("\n" + "-"*40 + "\n")
    json_operations()

if __name__ == "__main__":
    main()