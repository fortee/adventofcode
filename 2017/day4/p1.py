import re


def run():
    """ Run the daily"""
    return solve_it(get_file())


def get_file():
    """ We read in the input data from the input file"""
    return open('input.txt', 'r')


def read_to_list(input):
    """We convert all lines (tab separated string) to list of strings
    and remove the newline character if any"""
    result = []
    for line in input:
        result.append(re.split(r'\t+', line.rstrip()))
    return result


def to_integer(list):
    """ Convert all strings in the line to an integer"""
    result = []
    for row in list:
        result.append([int(x) for x in row])
    return result


def read_file(input):
    """Read the file"""
    return input.read()


def solve_it(input):
    """ Solve the daily"""
    # input = read_file(input)
    passphrase_array = read_to_list(input)

    valid_passphrase_counter = 0

    for passphrase in passphrase_array:

        if check_passphrase(passphrase):
            valid_passphrase_counter += 1

        continue

    solution = valid_passphrase_counter

    return solution


def check_passphrase(passphrase):
    """Check if the passphrase is valid.
    It does not contain duplicate words"""

    words_array = passphrase[0].split()

    for word in words_array:
        # Check if the word occurred more then once
        if words_array.count(word) > 1:
            return False
        continue

    return True


print(run())
