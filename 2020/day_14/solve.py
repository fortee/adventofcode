# https://adventofcode.com/2020/day/14
import re


class Solution:
    def __init__(self):
        self.input_file = "input.txt"
        # self.input_file = "input_test2.txt"
        self.program = []
        self.memory = {}
        self.bitmask = ''
        self.process_input()

    def process_input(self):
        """
        Parse the input file
        """

        with open(self.input_file) as file:
            self.program = file.readlines()

    def solve(self):
        """
        Solve the puzzle
        """

        self.part1()
        self.part2()

    def part1(self):
        for line in self.program:

            if 'mask = ' in line:
                self.bitmask = line.strip().split('mask = ')[1]
                continue

            result = re.findall('(?<=\[)(.*)(?=\]).*=\s(.*)', line)[0]
            memory_address = int(result[0])
            decimal = int(result[1])
            value = self.apply_value_bitmask(decimal)
            self.memory[memory_address] = value

        print(f"Part 1: {sum(self.memory.values())}")

    def apply_value_bitmask(self, decimal):

        binary = '{:036b}'.format(decimal)  # Convert the decimal binary
        binary_array = list(binary)  # Convert the list to array

        for idx, bit in enumerate(self.bitmask):

            if bit == 'X':
                # We don't care about empty bitmask bit represented by `X`
                continue

            # Replace the bit in the given index
            binary_array[idx] = bit

        # Convert the array to a string again
        new_binary = ''.join(binary_array)

        # Convert binary to decimal and retur
        return int(new_binary, 2)

    def part2(self):

        # Reset the memory and bitmask
        self.memory = {}
        self.bitmask = ''

        for line in self.program:

            if 'mask = ' in line:
                self.bitmask = line.strip().split('mask = ')[1]
                continue

            result = re.findall('(?<=\[)(.*)(?=\]).*=\s(.*)', line)[0]
            memory_address = int(result[0])
            value = int(result[1])
            self.write_value_to_memory(memory_address, value)

        print(f"Part 2: {sum(self.memory.values())}")

    def write_value_to_memory(self, memory_address, value):

        memory_addresses = []
        binary_address = '{:036b}'.format(memory_address)  # Convert the decimal binary
        binary_array = list(binary_address)  # Convert the list to array

        for idx, bit in enumerate(self.bitmask):

            if bit == '0':
                # If the bitmask bit is 0, the corresponding memory address bit is unchanged.
                continue

            if bit == '1':
                # If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1
                binary_array[idx] = '1'

            if bit == 'X':
                binary_array[idx] = 'X'

        memory_addresses.append(''.join(binary_array))

        # Calculate the memory addresses based on the floating bits
        memory_addresses = self.get_all_memory_addresses(memory_addresses)

        # Make the list unique
        memory_addresses = list(set(memory_addresses))

        # Write the value to the memory addresses
        for memory_address in memory_addresses:
            memory_address_decimal = int(memory_address, 2)
            self.memory[memory_address_decimal] = value

    def get_all_memory_addresses(self, memory_addresses):

        if not any([x for x in memory_addresses if 'X' in x]):
            return memory_addresses

        for memory_address in memory_addresses:

            # Remove the current address
            memory_addresses.remove(memory_address)

            for idx, mas_bit in enumerate(memory_address):

                if mas_bit != 'X':
                    # We only care about floating bits
                    continue

                for bit in ['1', '0']:
                    new_address = list(memory_address)
                    new_address[idx] = bit
                    memory_addresses.append(''.join(new_address))

                return self.get_all_memory_addresses(memory_addresses)


solution = Solution()
solution.solve()
