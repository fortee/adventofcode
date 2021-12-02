# https://adventofcode.com/2021/day/2
with open(r"input.txt") as file:
    part1 = {'x': 0, 'z': 0}
    part2 = {'x': 0, 'z': 0, 'aim': 0}

    for line in file.readlines():
        direction, amount = line.split()
        amount = int(amount)

        if direction == 'forward':
            part1['x'] += amount
            part2['x'] += amount
            part2['z'] += part2['aim'] * amount
        else:
            part1['z'] += amount if direction == 'down' else amount * -1
            part2['aim'] += amount if direction == 'down' else amount * -1

print(f"Part 1 solution: {part1['x'] * part1['z']}")
print(f"Part 2 solution: {part2['x'] * part2['z']}")