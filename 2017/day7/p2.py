import re
import json


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
    parent_children = {}

    for line in input:

        # Split line to sub strings
        line = line.strip().split()

        # Assign parts to variables
        name = line[0]
        weight = int(line[1].strip('()'))

        # Add the related list
        names.append(name)
        weights[name] = {'weight': weight, 'children_weight': 0, 'full_weight': 0}

        if '->' in line:
            # Find the index of the children marker
            index = line.index('->')

            # Add each stripped string after the 'children marker' to the current_children array
            current_children = [c.strip(',') for c in line[index + 1 :]]

            parent_children[name] = current_children

            # Add each child to the children set (we use this as this will be unique)
            for child in current_children:
                children.add(child)

    tree = Tree(names, children, parent_children, weights)

    # print json.dumps(tree.tree, sort_keys=True, indent=4)

    return tree.correct_weight


class Tree:
    def __init__(self, names, children, map, weights):
        self.names = names
        self.children = children
        self.map = map
        self.weights = weights
        self.correct_weight = None
        self.root = self.find_root()
        self.tree = self.get_tree()

    def find_root(self):
        # Loop over all found name, if the name if not in the childrens array
        # we know this is the root
        for name in self.names:
            if name not in self.children:
                return name

    def get_tree(self):

        return {self.root: self.build_branch(self.root, self.map[self.root])}

    def build_branch(self, root, children):
        """Build the tree branches with recursion"""
        tree = {}

        for child in children:

            if self.map.get(child, False):
                child_children = self.map[child]
                tree[child] = self.build_branch(child, child_children)
            else:
                tree[child] = {}

            # Set root and child weights
            full_weight = self.weights[child]['weight'] + self.weights[child]['children_weight']
            self.weights[child]['full_weight'] = full_weight
            self.weights[root]['children_weight'] += full_weight

        self.weights[root]['full_weight'] += (
            self.weights[root]['weight'] + self.weights[root]['children_weight']
        )

        self.check_weight_error(children)

        return tree

    def check_weight_error(self, children):
        """Check if any of the children full weights are off
        if they are we need to find the wrong one
        and calculate the amount we need to adjust it's base weight"""

        child_weights = []

        for child in children:
            child_weights.append(self.weights[child]['full_weight'])

        maximum = max(child_weights)
        minimum = min(child_weights)

        if maximum != minimum and not self.correct_weight:

            maximum_count = child_weights.count(maximum)
            minimum_count = child_weights.count(minimum)

            if maximum_count > minimum_count:
                wrong_index = child_weights.index(minimum)
                difference = maximum - minimum
            else:
                wrong_index = child_weights.index(maximum)
                difference = minimum - maximum

            wrong_name = children[wrong_index]

            correct_weight = self.weights[wrong_name]['weight'] + difference

            self.correct_weight = correct_weight

            return True

        return False


print(run())
