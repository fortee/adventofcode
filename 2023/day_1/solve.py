import re

input_file = 'input-example.txt'
input_file = 'input.txt'
with open(input_file, 'r') as file:
    input_data = file.read().split("\n")

digit_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def is_int(char):
    """
    Check if this character is a string representation of an integer
    """
    try:
        return int(char)
    except:
        return False


def digit_words_to_digits(string):
    """
    Convert the string based on the chalange rules
    """

    # key - value pairs of location of found integers and the integer's string representation

    digits = {}
    for word, digit in digit_words.items():
        # Loop over each digit word and find all occurances of it in the string
        idx = -1
        while True:
            idx = string.find(word, idx + 1)
            if idx == -1:
                break
            # If found keep track of the first index and the integer's string representation
            digits[idx] = str(digit)
    for idx, char in enumerate(string):
        # Search the string for direct integers
        if digit := is_int(char):
            # If found keep track of the first index and the integer's string representation
            digits[idx] = str(digit)

    # Sort the found integers based on their location and assemble a new strng from them
    digits_string = ''.join(list(dict(sorted(digits.items())).values()))
    # Convert the fist and last integer from the string to an integers
    return int(f"{digits_string[0]}{digits_string[-1]}")


part1 = 0
for line in input_data:
    # Loop over each line
    # Get only the digits from the string
    just_digits = re.sub(r'\D', '', line)
    # Convert the fist and last integer from the string to an integers
    part1 += int(f"{just_digits[0]}{just_digits[-1]}")

print(f"Part1: {part1}")
part2 = sum(digit_words_to_digits(line) for line in input_data)
print(f"Part2: {part2}")
