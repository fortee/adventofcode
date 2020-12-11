# https://adventofcode.com/2020/day/7
import re
from collections import defaultdict


class Solution:
    def __init__(self):
        self.bags = {}
        self.unique_bags = set()
        self.can_contain_gold_bag = 0
        self.bag_trees = defaultdict(
            lambda: {'tree': {}, 'all_contained_bags': [], 'all_contained_bag_amounts': 0}
        )

    def solve(self):
        """
        Solve the puzzle
        """
        self.process_input()
        self.build_bag_trees()

    def process_input(self):
        """
        Parse the input file into a dict structure
        """

        with open(r"input.txt") as file:
            lines = file.readlines()

            # Iterate over all lines
            for line in lines:

                # Separate the main bag and it's contained bags
                regex_result = re.findall(r'^(.*?)\scontain\s(.*?)\.', line.strip())[0]
                main_bag = regex_result[0].replace('bags', 'bag')
                contained_bags = {}

                # Process each contained bag into a dictionary
                for bag in regex_result[1].split(','):

                    if bag == 'no other bags':
                        # We don't need to do anything if there are no other bags
                        continue

                    # Separate the bag name and the count
                    bag_res = re.findall('(^\d)\s(.*)', bag.strip())[0]
                    number = int(bag_res[0])
                    contained_bag = bag_res[1].replace('bags', 'bag')
                    contained_bags[contained_bag] = number

                    # Save the contained bag name to the unique bag names
                    self.unique_bags.add(contained_bag)

                self.bags[main_bag] = contained_bags
                # Save the main bag name to the unique bag names
                self.unique_bags.add(main_bag)

    def build_bag_trees(self):
        """
        Loop trough all the unique bags and
            - build a tree so we know what other bags they contain in hierarchy
            - build a list of all unique trees they could eventually contain
        """

        for bag in self.unique_bags:

            # Get the child bag data
            (
                self.bag_trees[bag]['tree'],
                self.bag_trees[bag]['all_contained_bags'],
                self.bag_trees[bag]['all_contained_bag_amounts'],
            ) = self.get_children(bag)

            if bag != 'shiny gold bag' and 'shiny gold bag' in self.bag_trees[bag]['all_contained_bags']:
                # if this is not the `shiny gold bag` and it contains the `shiny gold bag`
                self.can_contain_gold_bag += 1

    def get_children(self, bag):
        """
        The recursive function to get the child information
        """

        contained_bags = self.bags.get(bag, {})

        children_tree = {}
        parent_child_bags = list(contained_bags.keys()) + [bag]

        total_child_amounts = []
        for contained_bag, contained_bag_amount in contained_bags.items():
            child_tree, child_bags, child_amounts = self.get_children(contained_bag)
            # Tree
            children_tree[contained_bag] = child_tree
            # Unique bag list
            parent_child_bags += child_bags
            # Contained bag amounts
            total_child_amounts.append(contained_bag_amount + (child_amounts * contained_bag_amount))

        return children_tree, list(set(parent_child_bags)), sum(total_child_amounts)


solution = Solution()
solution.solve()
print(f"Part 1: {solution.can_contain_gold_bag}")
print(f"Part 2: {solution.bag_trees['shiny gold bag']['all_contained_bag_amounts']}")
