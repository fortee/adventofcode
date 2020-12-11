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
        result = get_divide_result(row)
        checksum += result

    solution = checksum
    return solution


def get_divide_result(row, base_number=None, index=None):
    """Get the result of the only evenly divisible numbers division"""

    for idx, current_number in enumerate(row):

        if base_number is None:
            base_number = current_number
            index = idx

        if idx != index:
            if evenly_divisible(base_number, current_number):
                result = int(base_number / current_number)
                return result

    index += 1
    if index <= len(row):
        return get_divide_result(row, row[index], index)


def evenly_divisible(base_number, current_number):
    """We check if the given two numbers are evenly divisible or not"""
    if base_number % current_number == 0:
        return True
    return False


print(run())
