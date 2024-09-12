# Currency Converter

# Exchange rates as of September 1, 2021
peso_to_usd = 0.00026
sole_to_usd = 0.24
reais_to_usd = 0.19

# Get the amount in Colombian pesos from the user
pesos = float(input("Enter the amount in Colombian pesos: "))

# Get the amount in Peruvian soles from the user
soles = float(input("Enter the amount in Peruvian soles: "))

# Get the amount in Brazilian reais from the user
reais = float(input("Enter the amount in Brazilian reais: "))

# Calculate the total amount in USD
total_usd = (pesos * peso_to_usd) + (soles * sole_to_usd) + (reais * reais_to_usd)

# Display the total amount in USD
print("Total amount in USD:", total_usd)