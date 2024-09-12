import os
import math
import random

# 1. File Handling: Create a file and write some data into it
def write_to_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"Content written to {file_name}")

# 2. File Handling: Read data from the file
def read_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            content = file.read()
        print(f"Content of {file_name}:\n{content}")
        return content
    else:
        print(f"{file_name} does not exist.")
        return None

# 3. Mathematical Operations: Calculate the square root of a number
def calculate_square_root(number):
    if number < 0:
        print("Cannot calculate square root of a negative number.")
        return None
    else:
        result = math.sqrt(number)
        print(f"Square root of {number} is {result}")
        return result

# 4. String Manipulation: Reverse a string
def reverse_string(s):
    reversed_s = s[::-1]
    print(f"Original string: {s}")
    print(f"Reversed string: {reversed_s}")
    return reversed_s

# 5. List Operations: Shuffle a list
def shuffle_list(lst):
    print(f"Original list: {lst}")
    random.shuffle(lst)
    print(f"Shuffled list: {lst}")
    return lst

# 6. Dictionary Operations: Count the frequency of words in a string
def word_frequency(text):
    words = text.split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    print("Word frequency:\n", frequency)
    return frequency

# 7. Control Flow: Check if a number is even or odd
def is_even(number):
    if number % 2 == 0:
        print(f"{number} is even.")
        return True
    else:
        print(f"{number} is odd.")
        return False

# Example usage of the functions
if __name__ == "__main__":
    # 1. Write to a file
    write_to_file('example.txt', 'Hello World! This is a test file.')

    # 2. Read from a file
    content = read_from_file('example.txt')

    # 3. Calculate square root
    calculate_square_root(25)

    # 4. Reverse a string
    reverse_string("Hello World!")

    # 5. Shuffle a list
    shuffle_list([1, 2, 3, 4, 5])

    # 6. Count word frequency
    if content:
        word_frequency(content)

    # 7. Check if a number is even or odd
    is_even(42)
