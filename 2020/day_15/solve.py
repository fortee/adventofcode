# https://adventofcode.com/2020/day/15


class Solution:
    def __init__(self):
        self.numbers = {}
        self.turn = 1
        self.last_number = False
        self.input_file = "input.txt"
        # self.input_file = "input_test.txt"
        self.process_input()

    def process_input(self):
        """
        Parse the input file
        """

        with open(self.input_file) as file:
            numbers = file.readline().strip().split(',')
            for idx, number in enumerate(numbers):
                if idx < len(numbers) - 1:
                    self.numbers[int(number)] = self.turn
                if idx == len(numbers) - 1:
                    self.last_number = int(number)
                self.turn += 1

    def solve(self, part, limit):
        """
        Solve the puzzle
        """

        while self.turn <= limit:

            if self.numbers.get(self.last_number, False):
                # If we already spoken that number
                new_number = (self.turn - 1) - self.numbers[self.last_number]
            else:
                new_number = 0

            # Save the last number, this is also the `new_number` from the pre round
            self.numbers[self.last_number] = self.turn - 1
            self.last_number = new_number
            self.turn += 1

        print(f"Part {part}: {self.last_number}")


solution = Solution()
solution.solve(part=1, limit=2020)
from datetime import datetime

st = datetime.now()
solution.solve(part=2, limit=30000000)
print(f"s: {datetime.now() - st}")
