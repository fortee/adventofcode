with open(r"input") as file:
    data = file.read()

# data = """6,10
# 0,14
# 9,10
# 0,3
# 10,4
# 4,11
# 6,0
# 6,12
# 4,1
# 0,13
# 10,12
# 3,4
# 3,0
# 8,4
# 1,10
# 2,14
# 8,10
# 9,0

# fold along y=7
# fold along x=5"""

split = data.split('\n\n')
dots = split[0].split('\n')
folds = split[1].split('\n')

width = 0
height = 0

for dot in dots:
    coordinates = dot.split(',')
    x = int(coordinates[0])
    y = int(coordinates[1])
    if x > width:
        width = x
    if y > height:
        height = y

canvas = []
for _ in range(height + 1):
    canvas.append(['.' for x in range(width + 1)])

for dot in dots:
    coordinates = dot.split(',')
    x = int(coordinates[0])
    y = int(coordinates[1])
    canvas[y][x] = "#"


def print_canvas(canvas):
    count = 0
    for row in canvas:
        count += len([x for x in row if x == '#'])
        print(''.join(row))
    print(f"")
    print(f"DOTS: {count}")
    print(f"=" * 50)
    print(f"")


def fold_up(canvas, size):
    onto = canvas[:size]
    to_fold = canvas[size+1:]
    for idx, row in enumerate(to_fold):
        onto_row = onto[len(onto)-1-idx]
        for point_idx, point in enumerate(row):
            if point == '#':
                onto_row[point_idx] = point
    return onto


def fold_left(canvas, size):
    final = []
    for idx, row in enumerate(canvas):
        onto = row[:size]
        to_fold = row[size+1:]
        for point_idx, point in enumerate(to_fold):
            if point == '#':
                onto[len(onto)-1-point_idx] = point
        final.append(onto)
    return final

print_canvas(canvas)

for fold in folds:
    if fold == '':
        continue
    instructions = fold.replace("fold along ", "").split("=")
    if instructions[0] == "y":
        canvas = fold_up(canvas, int(instructions[1]))
    else:
        canvas = fold_left(canvas, int(instructions[1]))
    print_canvas(canvas)
