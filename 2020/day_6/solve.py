# https://adventofcode.com/2020/day/6

groups = []
questions = 26
total_true_answers = []


class Solution:
    def __init__(self):
        self.total_true_answers = 0
        self.unique_true_answer_sets = 0

    @staticmethod
    def get_new_group():
        """
        Return a fresh group dictionary
        """
        return {'all_answers': set(), 'personal_answers': []}

    def process_group_data(self, group):
        # Add the current grouo
        self.total_true_answers += len(group['all_answers'])
        self.unique_true_answer_sets += len(set.intersection(*group['personal_answers']))

    # Get group data
    def solve(self):

        with open(r"input.txt") as file:
            group = self.get_new_group()
            lines = file.readlines()
            last_line = lines[-1]

            # Iterate over all lines
            for line in lines:

                persons_answers = set()

                if line == '\n':
                    # An empty line signals that a new password block starts

                    self.process_group_data(group)

                    # Start a new group
                    group = self.get_new_group()
                    continue

                # Remove new line
                line = line.replace('\n', '')

                # Iterate over the True answers
                for char in line:
                    group['all_answers'].add(char)
                    persons_answers.add(char)

                # Add the unique personal answers
                group['personal_answers'].append(persons_answers)

                if line == last_line:
                    # We also need to account for the end of file (last line)
                    self.process_group_data(group)


solution = Solution()
solution.solve()
print(f"Part 1: {solution.total_true_answers}")
print(f"Part 2: {solution.unique_true_answer_sets}")
