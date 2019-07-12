from cs50 import get_int

while True:
    n = get_int("height - number from 1 to 8: ")
    if n > 0 and n < 9:
        break

for i in range(n):
    print(" " * (n-1-i), end="")  #print spaces
    print("#" * (1+i), end="")  #print hashes
    print(" " * 2, end="")     #in between spaces
    print("#" * (1+i), end="")  #print 2nd hashes
    print("")   #new line