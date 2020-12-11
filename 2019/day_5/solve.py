# https://adventofcode.com/2019/day/2


class Computer:
    def __init__(self):
        self.input = []
        self.pointer = 0
        self.reset()

    @staticmethod
    def get_input():
        with open(r"input.txt") as file:
            input = [int(x) for x in file.read().split(',')]
        return input

    @staticmethod
    def get_instructions_count(opcode):
        """
        The `opcode_rules` is defined in the description of the puzzle
        """
        opcode_rules = {1: 3, 2: 3, 3: 1, 4: 1, 99: False}
        return opcode_rules[opcode]

    def execute_start_instructions(self, instructions):
        """
        If we got start instructions loop trough it and change the `input` accordingly
        """
        for position, value in instructions.items():
            self.input[position] = value

    def get_opcode_and_parameters(self):
        value = self.read(size=1)

        # The opcode is the rightmost two digits
        opcode = abs(value) % 100
        # Parameter modes are single digits, one per parameter, read right-to-left from the opcode
        parameters = list(str(value)[::-1][2:]) or False
        return opcode, parameters

    def get_value(self, instructions, position, parameters):

        if not parameters:
            mode = 0
        else:
            mode = parameters[position : position + 1] or 0

        if mode == 0:
            return self.input[instructions[position]]
        else:
            return instructions[position]

    def run(self, instructions={}):
        """
        Process the input
        This will:
            - get the first instruction
                - position 0 in the input is the first opcode
                - based on the opcode we can get the rest of the instructions
            - execute the instructions
            - move the pointer to get the next opcode
            - rinse and repeat until we get opcode 99
        """
        self.reset()
        self.execute_start_instructions(instructions)

        while True:
            # Get opcode
            opcode, parameters = self.get_opcode_and_parameters()

            if opcode == 99:
                # Stop the program, we encountered `99`
                break

            instructions = self.read(size=self.get_instructions_count(opcode))

            if opcode == 1:
                # `0` - Input 1 Position, `1` - Input 2 Position, `2` - Output Position
                self.input[instructions[2]] = self.get_value(instructions, 0, parameters) + self.get_value(
                    instructions, 1, parameters
                )
                continue

            if opcode == 2:
                # `0` - Input 1 Position, `1` - Input 2 Position, `2` - Output Position
                self.input[instructions[2]] = self.get_value(instructions, 0, parameters) * self.get_value(
                    instructions, 1, parameters
                )
                continue

            if opcode == 3:
                print(f"opcode: {opcode} instruction: {instructions}")
                ################
                #      PDB     #
                ################
                import pdb

                pdb.set_trace()
                continue

            if opcode == 4:
                print(f"opcode: {opcode} instruction: {instructions}")
                ################
                #      PDB     #
                ################
                import pdb

                pdb.set_trace()
                continue

    def read(self, size=1):
        """
        Read the next values from the input than move the pointer to the next index.
        """

        result = self.input[self.pointer : self.pointer + size]
        self.pointer += size

        if size == 1:
            # If we only read one value return it directly instead of a list
            return result[0]

        return result

    def reset(self):
        """
        Restore the original input
        """
        self.input = self.get_input()
        self.pointer = 0


computer = Computer()

# Part 1
start_instructions = {
    1: 12,
    2: 2,
}
computer.run(start_instructions)
print(f"Part 1: {computer.input[0]}")

# Part 2
for noun in range(100):
    for verb in range(100):
        start_instructions = {
            1: noun,
            2: verb,
        }
        computer.run(start_instructions)
        result = computer.input[0]
        if result == 19690720:
            print(f"Part 2: {100 * noun + verb}")
            break
