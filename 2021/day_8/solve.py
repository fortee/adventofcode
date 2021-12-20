# https://adventofcode.com/2021/day/8

import statistics
from collections import defaultdict

segments = [
    'abcefg',  # 0
    'cf',  # 1
    'acdeg',  # 2
    'acdfg',  # 3
    'bcdf',  # 4
    'abdfg',  # 5
    'abdefg',  # 6
    'acf',  # 7
    'abcdefg',  # 8
    'abcdfg',  # 9
]

# These digits use a unique mnumber of segments
digits_with_unique_number_of_segments = [1, 4, 7, 8]
unique_segment_numbers = [
    len(x) for idx, x in enumerate(segments) if idx in digits_with_unique_number_of_segments
]
part1_answer = 0
with open(r"input.txt") as file:
    for line in file.readlines():
        patterns, output = line.strip().split(' | ')
        patterns = patterns.split(' ')
        output = output.split(' ')
        part1_answer += len([x for x in output if len(x) in unique_segment_numbers])

print(f"Part 1: {part1_answer}")