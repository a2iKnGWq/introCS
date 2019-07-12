import sys
import cs50

if len(sys.argv) == 2:
    if not sys.argv[1].isdigit():
        sys.exit("key must be a digit")
else:
    sys.exit("Usage: caesar key")

key = int(sys.argv[1])

plain = cs50.get_string("plaintext: ")

numbers = []

for c in plain:
    if c.islower():
        numbers.append(ord(c) - ord('a'))
    else:               #dealing with non_alpha chars later
        numbers.append(ord(c) - ord('A'))

new_numbers = []

n = 0
for c in plain:
    new_numbers.append((numbers[n] + key)%26)
    n += 1

#transform "back" everything
cipher = []
m = 0
for c in plain:
    if c.isalpha():
        if c.islower():
            cipher.append(chr(new_numbers[m] + ord('a')))
        else:       #it's upper
            cipher.append(chr(new_numbers[m] + ord('A')))
    else:
        cipher.append(plain[m])
    m += 1

print("ciphertext: ", end="")
k = 0
for c in plain:
    print(f"{cipher[k]}", end="")
    k += 1
print()