# https://adventofcode.com/2020/day/5
from collections import defaultdict

with open(r"input.txt") as file:
    seat_codes = [x.replace("\n", "") for x in file.readlines()]

# The information we got from teh puzzle description
data = {
    'row': {
        'amount': 128,
        'lower': 'F',
        'upper': 'B',
    },
    'column': {
        'amount': 8,
        'lower': 'L',
        'upper': 'R',
    },
}


def get_id(type, id_string):

    block = [0, data[type]['amount']]
    lower = data[type]['lower']

    # print('')
    # print(f'{type} {id_string} {block}')
    for char in id_string:

        range = block[1] - block[0]

        if char == lower:
            min = block[0]
            max = block[0] + range / 2
        else:
            min = block[0] + range / 2
            max = block[1]

        block = [min, max]
        # print(f'{char}: {block}')

    if block[0] != block[1] - 1:
        raise Exception(f'We have a calculation problem! [{block[0]}, {block[1]-1}]')

    # print(f"RESULT: {type} - {block[0]}")
    return block[0]


# Create
#   - Array of seat ID's
#   - Dict of row_ids and column_ids
seat_ids = []
seats = defaultdict(list)
for seat_code in seat_codes:
    row_id = get_id('row', seat_code[:7])
    column_id = get_id('column', seat_code[7:])
    seat_id = int((row_id * 8) + column_id)
    seats[row_id].append(column_id)
    seat_ids.append(seat_id)
print(f'Part 1: {max(seat_ids)}')

# Find the rows we need to exclude
first_row = min(seats.keys())
last_row = max(seats.keys())

# Loop trough all rows and find our seat
our_row = correct_row = False
for row, column in seats.items():
    if row in (first_row, last_row):
        # Skip the first and last rows
        continue

    if len(column) != data['column']['amount']:
        # The row missing a column is ours
        our_row = row
        break

our_column = list(set(range(data['column']['amount'])) - set(seats[our_row]))[0]
print(f'Part 2: {int((our_row * 8) + our_column)}')
