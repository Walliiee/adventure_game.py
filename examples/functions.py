# D.R.Y. 🧩
# Codédex

import random

list_of_foods = ['celery', 'broccoli', 'cabbage']

# This was the first function introduced in the course
print('Hello, World!')

# This function calculates the maximum of two numbers a and b
print(max(3, 5))

# This function calculates the minimum of two numbers a and b
print(min(-1, 7))

# This function calculates the length of a list
print(len(list_of_foods))

# This function calculates a to the power b
print(pow(2, 6))

# Function to calculate the factorial of a number
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to reverse a string
def reverse_string(s):
    return s[::-1]

# Function to calculate the Fibonacci sequence
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_seq = [0, 1]
        while len(fib_seq) < n:
            fib_seq.append(fib_seq[-1] + fib_seq[-2])
        return fib_seq

# Function to calculate the sum of a list of numbers
def sum_list(numbers):
    return sum(numbers)

# Function to find the maximum number in a list
def find_max(numbers):
    return max(numbers)

# Function to find the minimum number in a list
def find_min(numbers):
    return min(numbers)

# Function to sort a list in ascending order
def sort_list(numbers):
    return sorted(numbers)

# Function to calculate the average of a list of numbers
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

