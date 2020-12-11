# https://adventofcode.com/2020/day/17


class Solution:
    def __init__(self, part):
        # The currently active cubes active
        self.part = part
        self.active_cubes = []
        self.input_file = "input.txt"
        # self.input_file = "input_test.txt"
        self.process_input()

    def process_input(self):
        """
        Parse the input file
        """

        with open(self.input_file) as file:

            w = 0
            z = 0
            y = 0
            for line in file.readlines():
                x = 0
                for cube in line.strip():
                    if cube == '#':

                        if self.part == 1:
                            cube_coords = (z, y, x)
                        else:
                            # For part 2 add the forth dimension.... Woah Dude!
                            cube_coords = (w, z, y, x)

                        self.active_cubes.append(cube_coords)
                    x += 1
                y += 1

    def solve(self):
        """
        Solve the puzzle
        """

        for i in range(6):  # Run the 6 cycles

            new_active_cubes = set()

            # We only need to consider the neighbours of the currently active cubes
            for cube in self.cubes_to_check():
                active_neighbours = [x for x in self.get_neighbours(cube) if x in self.active_cubes]

                if cube in self.active_cubes:
                    # This is an active cube

                    if len(active_neighbours) in [2, 3]:
                        new_active_cubes.add(cube)
                else:
                    # This is an in-active cube
                    if len(active_neighbours) == 3:
                        new_active_cubes.add(cube)

            self.active_cubes = new_active_cubes

        print(f"Part {self.part}: {len(self.active_cubes)}")

    def cubes_to_check(self):
        """
        Collect the neighbours of all active cubes
        These will be all the cubes we need to check the rules against.
        Other cubes wouldn't get affected by the rules and would stay the same (in-active)
        """
        cubes = set()
        for active_cube in self.active_cubes:
            cubes |= self.get_neighbours(active_cube)

        return cubes

    def get_neighbours(self, cube, include_cube=False):
        """
        Return the 3 dimensional neighbours of the cube
        """
        coordinates = [-1, 0, 1]
        w_coordinates = coordinates if self.part == 2 else [0]
        neighbours = set()

        for w in w_coordinates:
            for z in coordinates:
                for y in coordinates:
                    for x in coordinates:

                        if self.part == 1:
                            nz = cube[0] + z
                            ny = cube[1] + y
                            nx = cube[2] + x
                            neighbour = (nz, ny, nx)
                        else:
                            nw = cube[0] + w
                            nz = cube[1] + z
                            ny = cube[2] + y
                            nx = cube[3] + x
                            neighbour = (nw, nz, ny, nx)

                        if not include_cube and cube == neighbour:
                            # Skip this 'neighbour' ff we don't want to include the cube it self
                            continue
                        neighbours.add(neighbour)

        return neighbours


Solution(part=1).solve()
Solution(part=2).solve()
