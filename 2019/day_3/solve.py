# https://adventofcode.com/2020/day/3

with open(r"input.txt") as file:
    input = [x.replace("\n", "") for x in file.readlines()]

# Convert a command character to dict with the axis (x,y = 0,1) and direction
converter = {
    'U': {
        'axis': 1,  # for y in the position array
        'direction': 1,
    },
    'R': {
        'axis': 0,  # for x
        'direction': 1,
    },
    'D': {
        'axis': 1,  # for x
        'direction': -1,
    },
    'L': {
        'axis': 0,  # for x
        'direction': -1,
    },
}


def get_positions(command_string):
    """
    Get the positions for the given command string
    """

    # Convert to an array
    instructions = command_string.split(',')

    positions = {}
    position = [0, 0]
    steps = 0

    for command in instructions:

        data = converter[command[:1]]
        # The axis we need to move on
        axis = data['axis']
        # If this is an increase or not 1 or -1
        direction = data['direction']
        # The amount we are moving
        move = int(command[1:]) * direction
        # The new position value
        new_position_value = position[axis] + move

        # Save each position (tuple) from the current position to the one the command takes us
        for i in range(position[axis] + direction, new_position_value + direction, direction):
            steps += 1
            position[axis] = i
            # Save steps taken to given position
            if tuple(position) not in positions:
                positions[tuple(position)] = steps

    return positions


# Get the wire positions
wire_1_positions = get_positions(input[0])
wire_2_positions = get_positions(input[1])

# Find the common positions
common_positions = set(wire_1_positions.keys()) & set(wire_2_positions.keys())

# Get the closest common position to origin
min_distance = False
min_steps = False
for pos in common_positions:

    dist = abs(pos[0]) + abs(pos[1])

    if not min_distance or dist < min_distance:
        min_distance = dist

    steps = wire_1_positions[pos] + wire_2_positions[pos]
    if not min_steps or steps < min_steps:
        min_steps = steps

print(f'Part 1: {min_distance}')
print(f'Part 2: {min_steps}')
