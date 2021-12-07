# https://adventofcode.com/2021/day/7

import statistics
from collections import defaultdict


with open(r"input.txt") as file:
    positions = [int(x) for x in file.readline().split(',')]

# Find the median and the mean
median = int(statistics.median(positions))
mean = int(statistics.mean(positions))

# For `Part1` median is the best position
fuel_consumption = [abs(median - position) for position in positions]
print(f"Part 1: {sum(fuel_consumption)}")

consumption_data = defaultdict(int)
# Create a list of all possible distances
distances = list(range(1, max(positions) + 1))
# Pre-calculate all possible consomptions
for position in distances:
    consumption_data[position] = sum(distances[:position])

# Based on the puzzle input we could brute force it by looping trough all possible positions
# But we can anticipate that the best position is going to be "around" the mean
# this method is much faster it's time complexity is way less
fuel_consumptions = defaultdict(int)
for target_position in range(median, median + mean):
    fuel_consumptions[target_position] = sum(
        [consumption_data[abs(target_position - position)] for position in positions]
    )
print(f"Part 2: {min(fuel_consumptions.values())}")