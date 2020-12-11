# https://adventofcode.com/2020/day/1
with open(r"input.txt") as file:
    input = [int(x.replace('\n', '')) for x in file.readlines()]

for idx_1, value_1 in enumerate(input):
    for value_2 in input[:idx_1]:
        if value_1 + value_2 == 2020:
            print(f'Part 1: {value_1 * value_2}')

for idx_1, value_1 in enumerate(input):
    for idx_2, value_2 in enumerate(input[:idx_1]):
        for value_3 in input[:idx_2]:
            if value_1 + value_2 + value_3 == 2020:
                print(f'Part 2: {value_1 * value_2 * value_3}')
