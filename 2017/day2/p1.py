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
    list_of_string = read_to_list(input)
    list_of_integers = to_integer(list_of_string)

    checksum = 0

    for row in list_of_integers:
        min, max = get_min_max(row)
        checksum = checksum + (max - min)

    solution = checksum
    return solution


def get_min_max(row):
    """ Get the minimum and maximum values in the row"""
    min = None
    max = None
    for number in row:
        if min is None or min > number:
            min = number
        if max is None or max < number:
            max = number
    return min, max


print(run())
