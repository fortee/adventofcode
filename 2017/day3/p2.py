import re
import matplotlib.pyplot as plt
import math


def run():
    """ Run the daily"""
    return solve_it(get_file())


def get_file():
    """ We read in the input data from the input file"""
    return open('input.txt', 'r')


def read_to_list(input):
    """ We convert all lines (tab separated string) to list of strings
    and remove the newline character if any"""
    result = []
    for line in input:
        result.append(re.split(r'\t+', line.rstrip()))
    return result


def to_integer(list):
    """ Convert all strings in the line to an integer"""
    result = []
    for row in list:
        result.append([int(x) for x in row])
    return result


def read_file(input):
    """Read the file"""
    return input.read()


def solve_it(input):
    """ Solve the daily"""

    input = 325489
    matrix = Matrix(input)

    return matrix.stress_number


class Matrix:
    def __init__(self, input):
        # Set up staring values
        self.input = input
        self.number_of_squares = 1
        self.current_squares_width = 3
        self.stepper = 0
        self.coordinate_map = {}
        self.stress_map = {}
        self.set_up_pase_figure()
        self.stress_number = None
        self.draw()

    def draw(self):
        """ Draw the matrix"""

        # Create origo of taxicab matrix
        x = 0
        y = 0

        self.stress_map = {
            1: {
                'x': x,
                'y': y,
            }
        }
        self.coordinate_map['{}_{}'.format(0, 0)] = 1

        # Add elements to the map
        for number in range(2, self.input + 1):
            x, y = self.move(x, y, number)

            stress_number = self.get_neighbour_values(x, y)

            self.coordinate_map['{}_{}'.format(x, y)] = stress_number

            print 'x:{} y:{} s:{}'.format(x, y, stress_number)
            self.stress_map[stress_number] = {
                'x': x,
                'y': y,
            }

            if stress_number > self.input:
                self.stress_number = stress_number
                return

            plt.scatter(x, y, alpha=0)
            # plt.text(x, y, number, ha="center", va="center")
            plt.text(x, y, stress_number, ha="center", va="center")

    def move(self, x, y, number):
        """ We return in which way we want to move the next coordinate"""
        dist = get_distance_to_origo(self.current_squares_width)

        max = dist
        min = dist * -1

        f = (self.current_squares_width * 4) - 4

        # print 'd:{} n: {}, x:{}, y:{}, s:{}, f:{}'.format(dist, number, x, y, self.stepper, f)

        if self.stepper >= f:
            self.number_of_squares += 1
            self.current_squares_width += 2
            self.stepper = 1
            return x + 1, y

        self.stepper += 1

        # Going up on the y axis
        if x >= max and y < max:
            return x, y + 1

        # Going left on the x axis
        if x > min and y >= max:
            return x - 1, y

        # Going down on the y axis
        elif x <= min and y > min:
            return x, y - 1

        # Going right on the x axis
        elif x < max and y <= min:
            return x + 1, y

        # Making the first step from the origin
        elif x == 0 and y == 0:
            return x + 1, y

    def set_up_pase_figure(self):
        """ Set up the figure and base values"""
        plt.figure()
        plt.scatter(0, 0, alpha=0)
        plt.text(0, 0, 1, ha="center", va="center")

    def get_coordinate(self, number):
        """Return the coordinates for a number"""
        if number > self.input:
            self.map = {}
            self.input = number
            self.set_up_pase_figure()
            self.draw()
            return self.map.get(number)

        return self.map.get(number)

    def steps(self, number):
        """Return the number of steps in the shortest path
        from the number to the origin
        this is the Manhattan distance |a-c|+|b-d|"""
        coordinates = self.get_coordinate(number)

        return abs(0 - coordinates['x']) + abs(0 - coordinates['y'])

    def get_neighbour_values(self, x, y):

        neighbour_values = [
            self.coordinate_map.get('{}_{}'.format(x + 1, y + 0), 0),
            self.coordinate_map.get('{}_{}'.format(x + 1, y + 1), 0),
            self.coordinate_map.get('{}_{}'.format(x + 0, y + 1), 0),
            self.coordinate_map.get('{}_{}'.format(x - 1, y + 1), 0),
            self.coordinate_map.get('{}_{}'.format(x - 1, y + 0), 0),
            self.coordinate_map.get('{}_{}'.format(x - 1, y - 1), 0),
            self.coordinate_map.get('{}_{}'.format(x + 0, y - 1), 0),
            self.coordinate_map.get('{}_{}'.format(x + 1, y - 1), 0)
        ]

        print '{} {} {} {} {} {} {} {}'.format(self.coordinate_map.get('{}_{}'.format(x + 1, y + 0), 0),
                                               self.coordinate_map.get('{}_{}'.format(x + 1, y + 1), 0),
                                               self.coordinate_map.get('{}_{}'.format(x + 0, y + 1), 0),
                                               self.coordinate_map.get('{}_{}'.format(x - 1, y + 1), 0),
                                               self.coordinate_map.get('{}_{}'.format(x - 1, y + 0), 0),
                                               self.coordinate_map.get('{}_{}'.format(x - 1, y - 1), 0),
                                               self.coordinate_map.get('{}_{}'.format(x + 0, y - 1), 0),
                                               self.coordinate_map.get('{}_{}'.format(x + 1, y - 1), 0))

        return sum(neighbour_values)


def get_distance_to_origo(current_squares_width):
    """ Return the maximum distance of the origin centered square's side from the origin"""
    return int(current_squares_width / 2)


print(run())
plt.show()
