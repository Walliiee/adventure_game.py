for num in range(1, 101):
    if num % 3 == 0 and num % 5 == 0: # if num is divisible by 3 and 5
        print("FizzBuzz")
    elif num % 3 == 0: # % 3 == 0 means num is divisible by 3. 3 % 3 == 0, 6 % 3 == 0, 9 % 3 == 0, etc.
        print("Fizz")
    elif num % 5 == 0: # 0 means num is divisible by 5. 5 % 5 == 0, 10 % 5 == 0, 15 % 5 == 0, etc.
        print("Buzz")
    else:
        print(num)