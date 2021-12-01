# https://adventofcode.com/2021/day/1
with open(r"input.txt") as file:
    input = [int(x.replace('\n', '')) for x in file.readlines()]

last = last_window = False
changes = window_changes = 0
for idx, current in enumerate(input):
    # Part 1
    if last and last < current:
        changes += 1
    last = current

    # Part 2
    window = sum(input[idx : idx + 3])
    if last_window and last_window < window:
        window_changes += 1
    last_window = window

print(f"Part 1 solution: {changes}")
print(f"Part 2 solution: {window_changes}")