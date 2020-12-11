# https://adventofcode.com/2020/day/10
from collections import defaultdict


class Solution:
    def __init__(self):
        self.adapters = []
        self.own_device = False
        self.process_input()
        self.outlet_voltage = 0
        self.max_difference = 3
        self.differences = {
            1: 0,
            3: 0,
        }
        # The starter set
        self.adapters_in_positions = [{self.outlet_voltage: 1}]  # We only have one outlet
        self.number_of_combinations = 0
        self.visited_adapters = {}

    def process_input(self):
        """
        Parse the input file
        """

        with open(r"input.txt") as file:
            lines = file.readlines()

            # Iterate over all lines
            for adapter in lines:
                self.adapters.append(int(adapter))
            self.own_device = max(self.adapters) + 3
            self.adapters.append(self.own_device)  # Add own device
            self.adapters.sort()

    def solve(self):
        self.part1()
        # My original solution were I reinvent the wheel..
        # self.part2()

        # PLaying around with the DP solution from: https://www.youtube.com/watch?v=cE88K2kFZn0
        self.adapters.append(0)
        self.adapters.sort()
        possible_steps = self.solve_with_dynamic_programing(index=0)
        print(f'Part 2: {possible_steps}')

    def part1(self):
        needed_voltage = self.outlet_voltage
        remaining_adapters = self.adapters.copy()

        while remaining_adapters:

            # Get the next valid lowest voltage adapter
            next_adapter = self.get_next_adapter(remaining_adapters, needed_voltage)

            if next_adapter:
                # Remove it from the remaining list
                remaining_adapters.remove(next_adapter)
                # Calculate the difference
                difference = next_adapter - needed_voltage
                # print(remaining_adapters)
                # Assign the next voltage we need
                needed_voltage = next_adapter
                # Store the difference
                self.differences[difference] += 1
            else:
                raise Exception(f'Na valid adapter found for voltage: {needed_voltage}')

        print(f'Part 1: {self.differences[1] * self.differences[3]}')

    def get_next_adapter(self, remaining_adapters, current_voltage):
        """
        The valid adapter voltages
        """
        voltage = current_voltage + 1
        valid_adapter_voltages = list(range(voltage, voltage + self.max_difference))

        for adapter in remaining_adapters:
            if adapter in valid_adapter_voltages:
                return adapter

        return False

    def part2(self):
        """
        Find all possible adapters for all slots
        """
        for idx in range(len(self.adapters) + 1):
            self.get_adapters_in_positions(idx)
        print(f'Part 2: {self.number_of_combinations}')

    def get_adapters_in_positions(self, idx):
        """
        Find the next possible adapters based on the last output voltages (the last set of adapters)
        """

        next_adapters = defaultdict(int)
        # The previous adapters we have to connect to
        previous_adapters = self.adapters_in_positions[idx]

        for previous_adapter, amount in previous_adapters.items():
            next_adapters = self.get_next_valid_adapters(previous_adapter, amount, next_adapters)

        self.adapters_in_positions.append(next_adapters)

    def get_next_valid_adapters(self, previous_adapter, amount, next_adapters):
        """
        Get next valid adapters based on the previous adapter
        `previous_adapter`: int     The output voltage of the previous adapter
        `amount`:           int     How many of these adapters did we have
        `next_adapters`:    dict     The adapters (with amounts) that can connect to the previous chunk
        returns:            dict     The updated adapters (with amounts) that can connect to the previous chunk
        """

        # Next adapter voltage diff can't be greater than 3
        next_valid_voltages = self.get_next_valid_voltages(previous_adapter)

        # Next adapter can't be more than 3 indexes away from the current one
        next_valid_indexes = self.get_next_valid_indexes(previous_adapter)

        # Check the adapters in the valid indexes
        for index in next_valid_indexes:

            # Make sure we don't go over the available adapters
            if index >= len(self.adapters):
                continue

            # The adapters
            adapter = self.adapters[index]

            if adapter not in next_valid_voltages:
                # We can't use this adapter
                continue

            if adapter == self.own_device:
                # If this adapter is our own device it means we have reached the end of a valid adapter chain
                # As we are only looking at the last combination
                # it's possible that this means the end of multiple chains
                # this is why we add the amount and not just 1
                self.number_of_combinations += amount

            # Update the next adapter chunk
            next_adapters[adapter] += amount

        return next_adapters

    def get_next_valid_voltages(self, previous_adapter):
        """
        Next adapter's voltage cant be greater than `voltage` + 3
        """
        return list(range(previous_adapter + 1, previous_adapter + 1 + self.max_difference))

    def get_next_valid_indexes(self, previous_adapter):
        """
        Next adapter can't be further away than 3
        We know this as `self.adapters` is sorted ASC and we know the max voltage difference is 3
        """

        # A dirty fix for when we start the chains frm the outlet
        voltage_index = -1 if previous_adapter == 0 else self.adapters.index(previous_adapter)
        return range(voltage_index + 1, voltage_index + 1 + self.max_difference)

    def solve_with_dynamic_programing(self, index):
        adapter = self.adapters[index]

        if index == len(self.adapters) - 1:
            return 1  # possible_steps = 1

        if self.visited_adapters.get(index, False):
            return self.visited_adapters[index]

        possible_steps = 0

        for i in [1, 2, 3]:
            next_index = index + i

            if next_index >= len(self.adapters):
                continue

            next_adapter = self.adapters[next_index]

            if next_adapter - adapter > 3:
                continue

            possible_steps += self.solve_with_dynamic_programing(next_index)

        self.visited_adapters[index] = possible_steps
        return possible_steps


solution = Solution()
solution.solve()
