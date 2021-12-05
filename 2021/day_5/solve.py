# https://adventofcode.com/2021/day/3
from collections import defaultdict

with open(r"input.txt") as file:

    # Dict of coordinates
    #   {tuple(coordinate): int(number of times visited}
    all_line_points = defaultdict(int)
    straight_line_points = defaultdict(int)
    for line in file.readlines():
        # for line in ['1,1 -> 1,3', '9,7 -> 7,7']:
        end, start = [[int(i) for i in x.split(',')] for x in line.strip().split(' -> ')]

        # Check how "long" the line
        line_length = max(abs(end[0] - start[0]), abs(end[1] - start[1]))

        # Move for the length of the line
        for i in range(line_length + 1):

            # Find in which way we need to move
            x_mod = i if start[0] < end[0] else 0 if start[0] == end[0] else -i
            y_mod = i if start[1] < end[1] else 0 if start[1] == end[1] else -i

            # Set the point coordinates
            point = (start[0] + x_mod, start[1] + y_mod)

            if start[0] == end[0] or start[1] == end[1]:
                # Part 1 onlty needs horizontal and vertical lines
                straight_line_points[point] += 1

            all_line_points[point] += 1

    def draw(points):
        """
        Draw the map of the points
        """
        points_coords = list(points.keys())
        x_min = min(points_coords, key=lambda item: item[0])[0]
        x_max = max(points_coords, key=lambda item: item[0])[0]
        y_min = min(points_coords, key=lambda item: item[1])[1]
        y_max = max(points_coords, key=lambda item: item[1])[1]
        print(f"")
        for y in range(y_min, y_max + 1):
            line = ''
            for x in range(x_min, x_max + 1):
                point = points.get((x, y), False)
                val = str(point) if point else '.'
                line += val.center(2)
            print(line)
        print("-" * 20)

    # Print the resutls of each part
    for idx, line_points in enumerate([straight_line_points, all_line_points]):
        # Find point where the lines crossed more than once
        points = [point for point, qty in line_points.items() if qty >= 2]
        print(f"")
        print(f"Part {idx+1} solution: {len(points)}")
        draw(line_points)
