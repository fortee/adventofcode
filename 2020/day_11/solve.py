# https://adventofcode.com/2020/day/11
import copy


class Solution:
    def __init__(self):
        self.seat_map = []
        self.taken_seats = 0
        self.round = 0
        self.part = 1
        self.process_input()
        self.width = len(self.seat_map[0])
        self.height = len(self.seat_map)

    @staticmethod
    def get_seat_taken_value(char):
        """
        Convert the seat's string representation to an integer
        """
        convert = {'L': 0, '#': 1, '.': 0}  # Empty seat  # Occupied seat  # Floor, nobody will sit hear
        return convert[char]

    def process_input(self):
        """
        Parse the input file
        """

        with open(r"input.txt") as file:
            lines = file.readlines()

            for row in lines:
                processed_row = []
                for seat in row.rstrip():
                    processed_row.append(seat)
                    self.taken_seats += self.get_seat_taken_value(seat)
                self.seat_map.append(processed_row)

    def solve(self, part=1):

        self.part = part
        previously_taken_seats = self.taken_seats
        seat_map = copy.deepcopy(self.seat_map)
        # self.draw(seat_map)

        while True:
            seat_map = self.play_round(seat_map)
            # self.draw(seat_map)
            # print(f"Taken Seats: {self.taken_seats}")

            if previously_taken_seats - self.taken_seats == 0:
                break

            previously_taken_seats = self.taken_seats

        print(f'Part {self.part}: {self.taken_seats}')

    def play_round(self, seat_map):
        """
        Apply to rules to all seats for the given seat map
        """

        self.taken_seats = 0
        new_seat_map = []
        for row_idx, row in enumerate(seat_map):
            new_row = []
            for seat_idx, seat in enumerate(row):
                new_seat = self.get_new_seat_value(seat_map, row_idx, seat_idx, seat)
                new_row.append(new_seat)
            new_seat_map.append(new_row)

        # Update to the new map
        self.round += 1
        return new_seat_map

    def get_new_seat_value(self, seat_map, row_idx, seat_idx, seat):

        if seat == '.':
            # This is a `Floor` won't change
            return '.'

        adjacent_seats = self.get_adjacent_taken_seats(seat_map, row_idx, seat_idx)

        if seat == '#' and adjacent_seats >= (4 if self.part == 1 else 5):
            # A taken seat with more 4 or more adjacent taken seats will get empty
            return 'L'

        if seat == 'L' and adjacent_seats == 0:
            # An empty seat with no adjacent taken seats will get occupied
            self.taken_seats += self.get_seat_taken_value('#')  # Note the taken seat
            return '#'

        # There was no change
        self.taken_seats += self.get_seat_taken_value(seat)
        return seat

    def get_adjacent_taken_seats(self, seat_map, row_idx, seat_idx):
        """
        Check the seats in the 8 view directions
        Seat: X` | Seats we are checking: `#`

        $..$..$
        .$.$.$.
        ..$$$..
        $$$X$$$
        ..$$$..
        .$.$.$.
        $..$..$

        """

        taken_seats = 0
        for direction_y in [-1, 0, 1]:
            for direction_x in [-1, 0, 1]:

                if direction_y == 0 and direction_x == 0:
                    # Skip if we would stay check the original position
                    continue

                # Move to the next coordinate for the given directions
                y = row_idx + direction_y
                x = seat_idx + direction_x

                if self.part == 2:
                    while not self.out_of_boundaries(y, x) and seat_map[y][x] == '.':
                        # Move in to the given direction until we reach the map boundaries
                        # or a non `floor` seat
                        y = y + direction_y
                        x = x + direction_x

                if self.out_of_boundaries(y, x):
                    # We only care about points in the map boundaries
                    continue

                if seat_map[y][x] == '#':
                    taken_seats += 1

        return taken_seats

    def out_of_boundaries(self, y, x):
        """
        Validate the given coordinates.
        Can't be outside of the map and can't be the same seat we are checking
        """

        if 0 <= y < self.height and 0 <= x < self.width:
            return False

        return True

    @staticmethod
    def get_coordinate_info(row_idx, seat_idx, y, x):
        """
        Exclude all coordinates that are not in the defined 8 directions
        """

        if x == seat_idx:
            # The column
            if y > row_idx:
                return 'column_negative'
            else:
                return 'column'

        if y == row_idx:
            # The row
            if x > seat_idx:
                return 'row'
            else:
                return 'row_negative'

        if y - row_idx == x - seat_idx:
            # The descending diagonal
            if x < seat_idx and y < row_idx:
                return 'diag_negative'
            else:
                return 'diag'

        if row_idx - y == x - seat_idx:
            if x < seat_idx and y > row_idx:
                return 'diag_rev_negative'
            else:
                return 'diag_rev'

        return False

    def draw(self, seat_map):
        print('')
        print('')
        print(f'Round: {self.round}')
        for row in seat_map:
            print(f"{''.join(row)}")


solution = Solution()
solution.solve(part=1)
solution.solve(part=2)
