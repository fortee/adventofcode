# https://adventofcode.com/2021/day/3
from collections import defaultdict

with open(r"input.txt") as file:
    # Clean the input, this is an extra loop but we don't really care
    input = [x.strip() for x in file.readlines()]


def find_common(numbers):
    bit_sums = defaultdict(int)
    # Count the bits as integers
    for number in numbers:
        for idx, bit in enumerate(number):
            bit_sums[idx] += int(bit)

    # Create the binary strings
    # If the bit count is bigger than the half of the total numbers that will be the common one
    most_common = least_common = ''
    half = len(numbers) / 2
    for bit in bit_sums.values():
        most_common += '1' if bit >= half else '0'
        # We could use Bitwise Not but this is faster
        least_common += '0' if bit >= half else '1'
    return most_common, least_common

# Part 1
most_common, least_common = find_common(input)
print(f"Part 1 solution: {int(most_common, 2) * int(least_common, 2)}")

# Part2
def filter_numbers(bits, numbers, idx):

    if len(numbers) == 1:
        # Short circuit if only one numer is left, the puzzle rules defined this
        return False, False, numbers

    # Get the numbers where the bit at the given index matches
    new_numbers = [number for number in numbers if number[idx] == bits[idx]]

    # Get the commons for the new numbers
    most_common, least_common = find_common(new_numbers)

    return most_common, least_common, new_numbers


# Set the defaults for Part 2 start
o2_bits = most_common
co2_bits = least_common
o2_numbers = co2_numbers = input

for idx in range(len(most_common)):
    # Loop trough each bit index and filter down the valid numbers in each cycle
    o2_bits, _, o2_numbers = filter_numbers(o2_bits, o2_numbers, idx)
    _, co2_bits, co2_numbers = filter_numbers(co2_bits, co2_numbers, idx)

print(f"Part 2 solution: {int(o2_numbers[0], 2) * int(co2_numbers[0], 2)}")
