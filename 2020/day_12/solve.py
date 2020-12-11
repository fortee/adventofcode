# https://adventofcode.com/2020/day/12


class Solution:
    def __init__(self):
        self.instructions = []
        self.process_input()

    def process_input(self):
        """
        Parse the input file
        """

        with open(r"input.txt") as file:
            # with open(r"input_test.txt") as file:
            lines = file.readlines()

            for row in lines:
                self.instructions.append(row.strip())

    def solve(self):
        """
        Solve the puzzle
        """

        self.part1()
        self.part2()

    def part1(self):

        directions = {
            0: 'N',
            90: 'E',
            180: 'S',
            270: 'W',
        }

        position = (0, 0)  # (x, y)
        direction_degree = 90  # 'E'

        for instruction in self.instructions:

            action = instruction[0]
            unit = int(instruction[1:])

            if action in ['L', 'R']:
                res = direction_degree + unit * (1 if action == 'R' else -1)
                if res > 360:
                    direction_degree = res - 360
                elif res < 0:
                    direction_degree = 360 + res  # (+) as res is a negative number
                elif res == 360:
                    direction_degree = 0
                else:
                    direction_degree = res

            elif action == 'F':
                position = self.convert(position=position, action=directions[direction_degree], unit=unit)
            else:  # N, E, S, W
                position = self.convert(position=position, action=action, unit=unit)

        print(f"Part 1: {abs(position[0]) + abs(position[1])}")

    def part2(self):

        waypoint_position = (10, 1)  # (x, y)
        ship_position = (0, 0)  # (x, y)

        for instruction in self.instructions:

            action = instruction[0]
            unit = int(instruction[1:])

            if action == 'L':
                for x in range(int(unit / 90)):
                    waypoint_position = self.rotate_90ccw(waypoint_position)
            elif action == 'R':
                for x in range(int(unit / 90)):
                    waypoint_position = self.rotate_90cw(waypoint_position)
            elif action == 'F':
                ship_position = (
                    ship_position[0] + (waypoint_position[0] * unit),
                    ship_position[1] + (waypoint_position[1] * unit),
                )
            else:  # N, E, S, W
                waypoint_position = self.convert(position=waypoint_position, action=action, unit=unit)

        print(f"Part 2: {abs(ship_position[0]) + abs(ship_position[1])}")

    @staticmethod
    def convert(position, action, unit):

        conversion_dict = {
            'N': lambda x: (position[0], position[1] + unit),
            'E': lambda x: (position[0] + unit, position[1]),
            'S': lambda x: (position[0], position[1] - unit),
            'W': lambda x: (position[0] - unit, position[1]),
            'F': lambda x: (position[0] - unit, position[0]),
        }

        return conversion_dict[action](unit)

    @staticmethod
    def rotate_90cw(position):
        return position[1], position[0] * -1

    @staticmethod
    def rotate_90ccw(position):
        return -1 * position[1], position[0]


solution = Solution()
solution.solve()
