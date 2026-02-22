stock_prices = [34.68, 36.09, 34.94, 33.97, 34.68, 35.82, 43.41, 44.29, 44.65, 53.56, 49.85, 48.71, 48.71, 49.94, 48.53, 47.03, 46.59, 48.62, 44.21, 47.21]

def price_at(i): # i is the day 
    return stock_prices[i - 1] # Subtract 1 from i to get the correct index

def max_price(a, b):
    return max(stock_prices[a - 1:b]) # Subtract 1 from a to get the correct index

def min_price(a, b):
    return min(stock_prices[a - 1:b])

def average_price(a, b):
    return sum(stock_prices[a - 1:b]) / (b - a + 1)

if __name__ == "__main__": # This block of code will only run if the script is run directly and not imported which means it is a module in another script. if __name__ == "__main__": is used to prevent the code from running when the module is imported.
    print("Price on day 5:", price_at(5))
    print("Maximum price from day 1 to day 20:", max_price(1, 20))
    print("Minimum price from day 1 to day 20:", min_price(1, 20))
    print("Average price from day 1 to day 20:", average_price(1, 20))

stock_prices = [ 6.15, 5.81, 5.70, 5.65, 5.33, 5.62, 5.19, 6.13, 7.20, 7.34, 7.95, 7.53, 7.39, 7.59, 7.27 ]

def price_at(i):
  return stock_prices[i-1]

def max_price(a, b): # a and b are the days
  mx = 0 # Initialize the maximum price to 0 because the price cannot be negative
  for i in range(a, b + 1): # Loop through the days from a to b inclusive because we want to include the price on day b and +1 is used because the range function is exclusive 
    mx = max(mx, price_at(i)) # Get the maximum price from day a to day b because we want to find the maximum price in that range
  return mx

def min_price(a, b):
  mn = price_at(a)
  for i in range(a, b + 1):
    mn = min(mn, price_at(i))
  return mn

print(max_price(1, 15))
print(min_price(5, 10))
print(price_at(3))