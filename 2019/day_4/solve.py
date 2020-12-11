# https://adventofcode.com/2020/day/3

with open(r"input.txt") as file:
    input = [int(x) for x in file.read().split('-')]


def validate(number, part_2=False):
    """
    Validate the number by the rules:
    """

    string = str(number)

    if len(string) != 6:
        # Check: It is a six-digit number.
        return False

    has_two_digit_adjacent = False

    for i in range(len(string)):

        current_digit = int(string[i])
        previous_digit = current_digit if i == 0 else int(string[i - 1])

        if current_digit < previous_digit:
            # Check: Going from left to right,
            # the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
            return False

        if not has_two_digit_adjacent and previous_digit == current_digit and i != 0:
            # Check: Two adjacent digits are the same (like 22 in 122345).
            # We don't check the first digit
            # If we have an repeated digits are exactly two digits long we don't need to check further!

            if part_2:
                #   The puzzle description was way to vague for Part 2....
                # Make sure this is not a longer repeated digit, ex. 888 or 8888
                if not string[i] * 3 in string:
                    has_two_digit_adjacent = True
            else:
                has_two_digit_adjacent = True

    return has_two_digit_adjacent


valid_passwords_part1 = 0
valid_passwords_part2 = 0
# for number in [666777]:
for number in range(input[0], input[1]):
    # The value is within the range given in your puzzle input.
    if validate(number):
        valid_passwords_part1 += 1

    if validate(number, part_2=True):
        valid_passwords_part2 += 1

print(f'Part 1: {valid_passwords_part1}')
print(f'Part 2: {valid_passwords_part2}')
