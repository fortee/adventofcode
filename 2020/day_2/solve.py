# https://adventofcode.com/2020/day/2
import re
import shlex

with open(r"input.txt") as file:
    input = [x.replace('\n', '') for x in file.readlines()]


def process_line(line):
    data = shlex.split(line)
    limits = re.findall('\d+', data[0])
    return {
        'min': int(limits[0]),
        'max': int(limits[1]),
        'char': data[1].replace(':', ''),
        'pw': data[2],
    }


part1_passwords = 0
part2_passwords = 0
for line in input:
    data = process_line(line)
    number_of_chars = len([x for x in data['pw'] if x == data['char']])
    if data['min'] <= number_of_chars <= data['max']:
        part1_passwords += 1

    chars = [data['pw'][data['min'] - 1], data['pw'][data['max'] - 1]]
    if len([x for x in chars if x == data['char']]) == 1:
        part2_passwords += 1

print(f'Part 1: {part1_passwords}')
print(f'Part 2: {part2_passwords}')
