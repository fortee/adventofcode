# https://adventofcode.com/2020/day/16
import re
import math
from collections import defaultdict


class Solution:
    def __init__(self):
        self.rules = {}
        self.rule_positions = defaultdict(set)
        self.ticket = set()
        self.tickets = []
        self.valid_tickets = []
        self.all_valid_values = set()
        self.input_file = "input.txt"
        # self.input_file = "input_test.txt"
        # self.input_file = "input_test2.txt"
        self.process_input()

    def process_input(self):
        """
        Parse the input file
        """

        with open(self.input_file) as file:

            block = 0

            for line in file.readlines():

                if line == '\n':
                    # Step to the next block
                    block += 1
                    continue

                if block == 0:
                    # The Rules

                    results = re.findall('(.+?(?=:)):\s(.*)', line.strip())[0]

                    rule = results[0]  # Name of the rule
                    rule_set = set()

                    # Loop trough all rule ranges and collect them into a set
                    for value_range in results[1].split('or'):
                        values = value_range.strip().split('-')
                        rule_set.update(list(range(int(values[0]), int(values[1]) + 1)))

                    self.rules[rule] = rule_set
                    self.all_valid_values.update(rule_set)

                if block == 1:
                    if 'your ticket' in line:
                        # We don't need this line
                        continue
                    self.ticket = [int(x) for x in line.strip().split(',')]

                if block == 2:
                    if 'nearby tickets' in line:
                        # We don't need this line
                        continue
                    self.tickets.append([int(x) for x in line.strip().split(',')])

    def solve(self):
        """
        Solve the puzzle
        """

        self.part1()
        self.part2()

    def part1(self):

        # We collect the missing in to a list instead of an set
        # as it seems we need can have identical elements in this list
        invalid_values = []

        for ticket_array in self.tickets:

            ticket = set(ticket_array)
            values_not_in_any_rules = ticket - self.all_valid_values

            if values_not_in_any_rules:
                invalid_values += list(values_not_in_any_rules)
                continue

            self.valid_tickets.append(ticket_array)

        print(f"Part 1: {sum(invalid_values)}")

    def part2(self):
        """
        To many loops but it works and is quite fast
        """

        # Build a dictionary of indexes and possible rules
        possible_rules = defaultdict(set)
        for index in range(len(self.valid_tickets[0])):
            index_rules = set(self.rules.keys())
            for ticket in self.valid_tickets:
                value = ticket[index]
                # Possible rules for this value / index combination
                value_rules = set()
                for rule, rule_values in self.rules.items():
                    if value in rule_values:
                        value_rules.add(rule)
                index_rules &= value_rules
            possible_rules[index] = index_rules

        while possible_rules:

            # Search for pairs were there is only one possible rule
            solved = {k: v for k, v in possible_rules.items() if len(v) == 1}

            for index, rules in solved.items():
                # Remove this pair from the `possible_rules` dict
                possible_rules.pop(index)
                # Remove the rule from all other possible rules
                possible_rules = {k: v - rules for k, v in possible_rules.items()}
                # Save the solved rule
                self.rule_positions[index] = rules.pop()  # We know this set has only one element

        # Find the keys of the rules that have `departure` in the name
        departure_rule_keys = [k for k, v in self.rule_positions.items() if 'departure' in v]

        # Find the corresponding values from our ticket
        departure_ticket_values = [x for i, x in enumerate(self.ticket) if i in departure_rule_keys]

        # Multiply these values
        print(f"Part 2: {math.prod(departure_ticket_values)}")


solution = Solution()
solution.solve()
