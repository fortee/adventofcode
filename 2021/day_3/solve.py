# https://adventofcode.com/2021/day/2
from collections import defaultdict

with open(r"input.txt") as file:
    input = [x.strip() for x in file.readlines()]

def find_common(numbers):
    total_numbers = 0
    bit_sums = defaultdict(int)
    # Add up the bits as integers, and take note of how many binary numbers we have
    for number in numbers:
        total_numbers += 1
        for idx, bit in enumerate(number.strip()):
            bit_sums[idx] += int(bit)

    most_common_list = []
    least_common_list = []
    half = total_numbers / 2
    for bit in bit_sums.values():
        if bit >= half:
            most_common_list.append('1')
            least_common_list.append('0')
        else:
            most_common_list.append('0')
            least_common_list.append('1')
    return most_common_list, least_common_list


most_common_list, least_common_list = find_common(input)
gamma_rate_binary = ''.join(most_common_list)
epsilon_rate_binary = ''.join(least_common_list)
print(f"Part 1 solution: {int(gamma_rate_binary, 2) * int(epsilon_rate_binary, 2)}")

# Part2
def filter_numbers(bits, numbers, idx, get_most_common=True):
    if len(numbers) == 1:
        return False, numbers
    new_numbers = []
    co2_bit = bits[idx]
    for number in numbers:
        if number[idx] == co2_bit:
            new_numbers.append(number)
    most, least = find_common(new_numbers)
    return most if get_most_common else least, new_numbers


# Set the defaults
o2_valid_bits = most_common_list
co2_valid_bits = least_common_list
o2_valid_numbers = co2_valid_numbers = input

# Loop trough each number index
for idx in range(len(most_common_list)):
    # print(f"co2_valid_bits: {co2_valid_bits} co2_valid_numbers: {co2_valid_numbers} bit: {o2_valid_bits[idx]}")
    o2_valid_bits, o2_valid_numbers = filter_numbers(o2_valid_bits, o2_valid_numbers, idx)
    co2_valid_bits, co2_valid_numbers = filter_numbers(
        co2_valid_bits, co2_valid_numbers, idx, get_most_common=False
    )

print(f"Part 2 solution: {int(o2_valid_numbers[0], 2) * int(co2_valid_numbers[0], 2)}")
