import re


def run():
    """ Run the daily"""
    return solve_it(get_file())


def get_file():
    """ We read in the input data from the input file"""
    return open('input.txt', 'r')


def to_list_in_list(input):
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
    input = read_file(input)
    sum = 0
    idx = 0
    lenght = len(input)
    step = lenght / 2
    for number in input:

        if idx + step < lenght:
            next_key = idx + step
        else:
            next_key = idx + step - lenght

        # print 'Idx:{} Step:{} Length:{} Next_key:{} Next_number:{}'.format(idx, step, lenght, next_key, input[next_key])

        if int(number) == int(input[next_key]):
            sum += int(number)

        idx += 1

    solution = sum

    return solution


print(run())
