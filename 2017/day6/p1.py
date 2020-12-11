import re


def run():
    """ Run the daily"""
    return solve_it(get_file())


def get_file():
    """ We read in the input data from the input file"""
    return open('input.txt', 'r')


def read_to_list(input):
    """ We convert all lines (tab separated string) to list of strings
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
    input = read_to_list(input)
    input = to_integer(input)[0]

    # Set up start values
    state = input
    found_states = []
    steps = 0
    length = len(state)

    while True:

        if state in found_states:
            # We break the loop if we get the same state again
            break

        # We pu the current state in to the found ones
        found_states.append(state[:])

        # Get the highest value, we can use this as we want use the first max value
        max_value = max(state)

        # Get the index of highest value
        max_index = state.index(max_value)

        # Zero out the highest value 'bank'
        state[max_index] = 0

        # Set the next index
        next_index = max_index

        for idx in range(1, max_value + 1):
            # Loop for amount of the found highest value

            # Incearse the next index
            next_index += 1

            if next_index > length - 1:
                # We want to get the fist elent if we go over the last one
                next_index = 0

            state[next_index] += 1

        print state

        # Inceare the step counter
        steps += 1

    return steps


print(run())
