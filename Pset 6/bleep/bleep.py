import cs50
import sys

def main():

    # Check for correct number of args
    if len(sys.argv) != 2:
        print("Usage: python bleep.py dictionary")
        sys.exit(1)

    # Load dictionary
    words = set()
    file = open(sys.argv[1], "r")
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()

    # Input text and make an array of the words in it
    print("What message would you like to censor?")
    text = cs50.get_string()
    arr = text.split()

    # Print out word or appropriate stars from array
    for word in arr:
        if word.lower() in words:
            print("*" * len(word), end=" ")
        else:
            print(word, end=" ")
    print()

if __name__ == "__main__":
    main()