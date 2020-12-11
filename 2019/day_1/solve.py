import math

# https://adventofcode.com/2019/day/1
with open(r"input.txt") as file:
    input = [int(x.replace('\n', '')) for x in file.readlines()]


def get_fuel(mass):
    return math.floor(mass / 3) - 2


total = 0
for mass in input:
    total += get_fuel(mass)
print(f"Part 1: {total}")

total = 0
for mass in input:
    fuel = get_fuel(mass)
    while fuel > 0:
        total += fuel
        fuel = get_fuel(fuel)
print(f"Part 2: {total}")
