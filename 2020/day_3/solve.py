# https://adventofcode.com/2020/day/3
from functools import reduce

with open(r"input.txt") as file:
    input = [x.replace("\n", "") for x in file.readlines()]

trees_encountered = []
max_x = len(input[0]) - 1
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

for slope in slopes:
    x = slope[0]
    y = slope[1]
    slope_trees = 0

    while y < len(input):
        position = input[y][x]
        if position == "#":
            slope_trees += 1

        # Get the new `x` value considering the map duplications
        # `-1` to make up for the index difference when moving to a new duplication
        x += slope[0]
        if x > max_x:
            x = x - max_x - 1
        y += slope[1]

    trees_encountered.append(slope_trees)

    if slope == (3, 1):
        print(f'Part 1: {slope_trees}')

print(f'Part 2: {reduce(lambda x, y: x*y, trees_encountered)}')
