from cs50 import get_float

received = get_float("Change owed: ")

while True:
    if received > 0:
        break

cents = round(100*received)
coins = 0

array = [25, 10, 5, 1]

for i in range(25, 0, -1):
    if i in array:
        while cents >= i:
            cents -= i
            coins += 1

print(coins)