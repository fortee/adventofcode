# https://adventofcode.com/2020/day/18


class Solution:
    def __init__(self, part):
        self.input_file = "input.txt"
        # self.input_file = "input_test.txt"
        self.part = part
        self.lines = []

    def solve(self):
        """
        Solve the puzzle
        """
        with open(self.input_file) as file:

            total = 0  # The total amount
            for line in file.readlines():

                # Clean the string
                string = line.strip()

                while '(' in string:
                    # Convert the expressions in parenthesis to an integer until non is left
                    proc_string = self.process_parentheses(string)
                    string = proc_string

                # Evaluate the final string expression
                value = self.eval_string_expression(string)
                total += value

            print(f"Part {self.part}: {total}")

    def process_parentheses(self, string):
        """
        Convert the string expressions inside parentheses to an int
        Don't bother about nested parentheses, find the smallest one we can process and re-trigger (`while '(' in string:`)
        """

        str_in_phar = ''
        ph_opened = False

        for char in string:

            if ph_opened and char == '(':
                # This is the start of a new nested parentheses section
                str_in_phar = ''
                continue

            if not ph_opened and char == '(':
                # Start of the first parentheses section
                ph_opened = True
                continue

            if ph_opened and char not in ['(', ')']:
                # If we are inside a parentheses section add the character
                str_in_phar += char

            if ph_opened and char == ')':
                # This is the end of the parentheses section
                # Evaluate, and replace the section with the result
                value = self.eval_string_expression(str_in_phar)
                return string.replace(f"({str_in_phar})", str(value))

    def eval_string_expression(self, string):
        """
        Evaluate string as a mathematical expression
        """

        if self.part == 2:
            while '+' in string:
                proc_string = self.eval_additions(string)
                string = proc_string

        line_sum = 0
        operator = False
        for idx, expression in enumerate(string.strip().split(' ')):

            if idx % 2 == 0:
                # Odd expression is an integer
                if not line_sum:
                    line_sum = int(expression)
                    continue

                line_sum = self.do_operation(operator, line_sum, int(expression))

            else:
                # Even expression is an operator
                operator = expression
        return line_sum

    @staticmethod
    def eval_additions(string):
        """
        Convert all additions to to their values
        """

        string_array = string.strip().split(' ')
        for idx, char in enumerate(string_array):
            if char == '+':
                n1 = string_array[idx - 1]
                n2 = string_array[idx + 1]
                value = int(n1) + int(n2)
                string_array[idx - 1] = value
                # Replace the first number with the addition result
                string_array[idx - 1] = str(value)
                # Remove the operator and the second number
                string_array.pop(idx)
                string_array.pop(idx)
                proc_string = ' '.join(string_array)
                return proc_string

    @staticmethod
    def do_operation(operator, n1, n2):
        operators = {'+': lambda x, y: (x + y), '*': lambda x, y: (x * y)}
        return operators[operator](n1, n2)


Solution(part=1).solve()
Solution(part=2).solve()
