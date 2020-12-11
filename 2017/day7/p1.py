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
    names = []
    weights = {}
    children = set()

    for line in input:

        # Split line to sub strings
        line = line.strip().split()

        # Assign parts to variables
        name = line[0]
        weight = int(line[1].strip('()'))

        # Add the related list
        names.append(name)
        weights[name] = weight

        if '->' in line:
            # Find the index of the children marker
            index = line.index('->')

            # Add each stripped string after the 'children marker' to the current_children array
            current_children = [c.strip(',') for c in line[index + 1 :]]

            # Add each child to the children set (we use this as this will be unique)
            for child in current_children:
                children.add(child)

    # Loop over all found name, if the name if not in the childrens array
    # we know this is the root
    for name in names:
        if name not in children:
            return name


print(run())
