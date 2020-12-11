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


def to_integer_list(list):
    with list as f:
        content = f.readlines()
    return [int(x.strip()) for x in content]


def read_file(input):
    """Read the file"""
    return input.read()


def solve_it(input):
    """ Solve the daily"""
    input = to_integer_list(input)

    idx = 0
    steps = 0
    while 0 <= idx <= len(input) - 1:
        move = input[idx]
        input[idx] += 1
        steps += 1
        # print'i:{} v:{} v(n):{} s:{}'.format(idx, move, move + 1, steps)
        idx += move

    return steps


print(run())
