# https://adventofcode.com/2020/day/13
import math
import numpy as np


class Solution:
    def __init__(self):
        self.earliest = 0
        self.all_busses = []
        self.busses = []
        self.process_input()

    def process_input(self):
        """
        Parse the input file
        """

        with open(r"input.txt") as file:
            lines = file.readlines()
            self.earliest = int(lines[0].strip())
            bus_data = lines[1].strip()
            self.busses = [int(x) for x in bus_data.split(',') if x != 'x']
            self.all_busses = [int(x) if x != 'x' else x for x in bus_data.split(',')]

    def solve(self):
        """
        Solve the puzzle
        """

        self.part1()
        self.part2()

    def part1(self):
        bus_starts = {}
        for bus in self.busses:
            rounds = self.earliest / bus

            if self.earliest % bus == 0:
                time_left = 0
            else:
                time_left = (math.floor(rounds + 1) * bus) - self.earliest

            bus_starts[bus] = time_left

        earliest_bus = min(bus_starts, key=bus_starts.get)
        print(f"Part 1: {earliest_bus * bus_starts[earliest_bus]}")

    def part2(self):
        # index - Index of the next bus
        # timestamp - were to start from
        # step - The amount we increase the timestamp each recursion
        print(f"Part 2: {self.get_it(index=1, timestamp=7, step=1)}")

    def get_it(self, index, timestamp, step):
        """
        Get the first timestamp that fits the two rules

        Move on to the next bus, we get this from the self.busses that only has the valid bus IDs
            As a next `step` we use the lowest common multiple of the current step
            and the lowest common multiple of the first_bus and next_bus | line 81

        Example for 7 and 13
            timestamp % first_bus == 0 (168 % 7 == 0)
            (timestamp+offset) % next_bus == 0 (168+1 % 13 == 0)

        """

        if index > len(self.busses) - 1:
            return timestamp

        first_bus = self.busses[0]
        base_idx = 0

        next_bus = self.busses[index]
        next_bus_idx = self.all_busses.index(next_bus)

        offset = next_bus_idx - base_idx
        # lcm = np.lcm(first_bus, next_bus)
        while True:

            if (timestamp + offset) % next_bus == 0 and timestamp % first_bus == 0:
                # print(f"{base} -> {number} ({remainder}) | {timestamp}")

                index += 1
                # `lowest common multiple` of prime numbers is the same as multiplying them
                # lcm = np.lcm(step, lcm)
                lcm = step * next_bus
                return self.get_it(index=index, timestamp=timestamp, step=lcm)

            timestamp += step


solution = Solution()
solution.solve()
