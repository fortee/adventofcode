# https://adventofcode.com/2020/day/8
import re


class Solution:
    def __init__(self):
        self.accumulator = 0
        self.instructions = {}
        self.instructions_count = 0
        self.changed_instruction_index = 0
        self.swap_values = {'jmp': 'nop', 'nop': 'jmp'}
        self.part = 1

    def solve(self):
        """
        Solve the puzzle
        """
        self.process_input()

        # Solve Part 1
        self.part = 1
        self.run(0)

        # Solve Part 2
        self.part = 2
        while True:
            if self.run(0):
                break
            self.modify_instructions()

    def process_input(self):
        """
        Parse the input file
        """

        with open(r"input.txt") as file:
            lines = file.readlines()

            # Iterate over all lines
            for idx, line in enumerate(lines):

                # Separate the main bag and it's contained bags
                regex_result = re.findall(r'([a-z]+)\s(\D+)(\d*)', line.strip())[0]
                self.instructions[idx] = {
                    'operation': regex_result[0],
                    'value': int(regex_result[2]) * (1 if regex_result[1] == '+' else -1),
                    'original_command': line.rstrip(),
                    'executed': 0,
                }

            # Save the total number of instructions for convenience
            self.instructions_count = len(self.instructions)

    def run(self, instruction_index):
        """
        Run the program
        """

        # https://www.youtube.com/watch?v=WxnN05vOuSM
        next_instruction_index = self.instructions_count * 666

        if instruction_index >= self.instructions_count:
            return self.stop()

        instruction = self.instructions[instruction_index]
        if instruction['executed'] >= 1:
            # Infinite loop detected
            if self.part == 1:
                return self.stop()
            return False

        instruction['executed'] += 1
        operation = instruction['operation']

        if operation == 'acc':
            self.accumulator += instruction['value']
            next_instruction_index = instruction_index + 1

        if operation == 'jmp':
            next_instruction_index = instruction_index + instruction['value']

        if operation == 'nop':
            next_instruction_index = instruction_index + 1

        return self.run(next_instruction_index)

    def stop(self):
        """
        Stop the program from running
        """
        print(f"Part {self.part}: {self.accumulator}")
        return True

    def modify_instructions(self):
        """
        Try to swap the next instruction
        """

        self.reset()

        for idx in range(self.changed_instruction_index, self.instructions_count):
            instruction = self.instructions[idx]
            self.changed_instruction_index += 1

            new_operation = self.swap_values.get(instruction['operation'], False)
            if new_operation:
                self.instructions[idx]['operation'] = new_operation
                return

    def reset(self):
        """
        Reset values for next try
        """
        self.accumulator = 0
        self.process_input()


solution = Solution()
solution.solve()
