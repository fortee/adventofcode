# https://adventofcode.com/2020/day/9


class Solution:
    def __init__(self):
        self.input = []
        self.block = []  # Numbers we need to take into account when searching for the numbers fo the sum
        self.pointer = 0  # This points to the current number we are looking at
        self.preamble_size = 25  # Size of the preamble and number of the block
        self.invalid_number = False
        self.process_input()

    def process_input(self):
        """
        Parse the input file
        """

        with open(r"input.txt") as file:
            numbers = file.readlines()

            # Iterate over all lines
            for number in numbers:
                self.input.append(int(number))

    def update_current_block(self, idx):
        """
        We know that the block size is 25
        """
        self.pointer = idx
        self.block = self.input[(self.pointer - self.preamble_size) : self.pointer]

    def solve(self):
        """
        Solve the puzzle
        """

        self.find_invalid_number()  # Part 1 solution
        self.find_block_for_invalid_number()  # Part 2 solution

    def find_invalid_number(self):
        for idx, number in enumerate(self.input):

            if idx < self.preamble_size:
                # Skip the numbers in the preamble
                continue

            # Set the pointer and update the current block
            self.update_current_block(idx)

            if not self.is_valid():
                # In `Part 1` we are searching for the first number that can't be a some of the current block
                self.invalid_number = number
                print(f'Part 1: {self.invalid_number}')
                return

    def is_valid(self):
        """
        Check if the any pair of numbers in the given block sums to the current number
        The current number is shown by the `self.pointer`
        """
        for idx, x in enumerate(self.block):
            for y in self.block[(idx + 1) :]:
                if x + y == self.input[self.pointer]:
                    return True
        return False

    def find_block_for_invalid_number(self):
        """
        Loop trough all possible `lists` defined by the rules to find the solution
        """

        input_length = len(self.input)
        for x in range(input_length):
            for y in range(x + 2, input_length):
                block = self.input[x:y]
                if sum(block) == self.invalid_number:
                    print(f'Part 2: {min(block) + max(block)}')
                    return

        print(f'Part 2: No Valid Solution Found!')


solution = Solution()
solution.solve()
