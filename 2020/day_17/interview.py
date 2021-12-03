from collections import defaultdict

input = """
#.#####.
#..##...
.##..#..
#.##.###
.#.#.#..
#.##..#.
#####..#
..#.#.##
"""

input = """
.#.
..#
###
"""


def draw_it(cubes, cycle):

    print(f"")
    print(f"")
    print(f"###########")
    print(f"CYCLE: {cycle}")
    print(f"###########")
    print(f"")
    
    
    size = 10
    full_range = range(-1 * size, size)
    
    header = ''.join([f"{idx:3}" for idx, _ in enumerate(full_range)])

    z_positions = set([x[2] for x in cubes])
    z_range = range(min(z_positions), max(z_positions)) if len(z_positions) > 1 else [list(z_positions)[0]] 
    
    for z in z_range:
        print(f"")
        print(f"")
        print(f"Z-Index: {z}")
        print(f"")
        print(f"  {header}")
        for idx, y in enumerate(full_range):
            row = f'{idx:3}'
            for x in full_range:
                coordinates = (x, y, z)
                row += ' # ' if coordinates in cubes else ' . '
            print(row)

def get_starting_active_cubes():
    rows = [x for x in input.split("\n") if x != '']
    active_cubes = set()
    for y, row in enumerate(rows):
        for x, active in enumerate(row):
            if active == '#':
                active_cubes.add((x, y, 0))
    return active_cubes


def get_neighbors(active_cube):
    cube_x, cube_y, cube_z = active_cube
    moves = [-1, 0, 1]
    neighbours = set()
    for x in moves:
        for y in moves:
            for z in moves:
                neighbour = (cube_x + x, cube_y + y, cube_z + z)
                if neighbour != active_cube:
                    neighbours.add((cube_x + x, cube_y + y, cube_z + z))
    return neighbours


def solve():
    active_cubes = get_starting_active_cubes()
    cycle = 0
    draw_it(active_cubes, cycle)
    for _ in range(3):
        cycle += 1
        # Get all the cubes to check
        # We only care about the neighbors of the active cubes
        cubes_to_check = set()
        for active_cube in active_cubes:
            neighbours = get_neighbors(active_cube)
            cubes_to_check |= neighbours

        new_active_cubes = set()
        for cube in cubes_to_check:
            neighbours = get_neighbors(cube)
            active_neighbours = len([x for x in neighbours if x in active_cubes])

            cube_is_active = cube in active_cubes
            if cube_is_active and active_neighbours in [2, 3]:
                new_active_cubes.add(cube)
            if not cube_is_active and active_neighbours == 3:
                new_active_cubes.add(cube)
        active_cubes = new_active_cubes
        draw_it(active_cubes, cycle)

    print(f"{len(active_cubes)} active cubes left after all cycles.")


solve()
