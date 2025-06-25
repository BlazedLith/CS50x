from cs50 import get_float

# Prompt the user for the amount of change owed (in dollars)
while True:
    dollars_owed = get_float("Change owed: ")
    if dollars_owed >= 0:
        break

# Convert dollars to cents
cents_owed = round(dollars_owed * 100)

# Initialize variables to keep track of the number of coins
quarters = dimes = nickels = pennies = 0

# Calculate the number of each type of coin needed
while cents_owed > 0:
    if cents_owed >= 25:
        quarters += 1
        cents_owed -= 25
    elif cents_owed >= 10:
        dimes += 1
        cents_owed -= 10
    elif cents_owed >= 5:
        nickels += 1
        cents_owed -= 5
    else:
        pennies += 1
        cents_owed -= 1

# Calculate the total number of coins used
total_coins = quarters + dimes + nickels + pennies

# Print the minimum number of coins
print(total_coins)
