import sys

digit_string = sys.argv[1]

if digit_string.isdigit():
    result = sum([int(char) for char in digit_string])

    print(result)
