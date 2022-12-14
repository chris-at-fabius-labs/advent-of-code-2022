
CELL_ROCK = "#"
CELL_SAND = "o"
CELL_FALLING = "~"
CELL_EMPTY = "."
CELL_ORIGIN = "+"

POINT_ORIGIN = (500, 0)

SAND_VECTORS = [(0, 1), (-1, 1), (1, 1)]

def point_move(point, vector, distance = 1):
    return (
        point[0] + (vector[0] * distance),
        point[1] + (vector[1] * distance)
    )

def points_between(a, b):
    if a is None or b is None: return
    a_x, a_y = a
    b_x, b_y = b
    if a_x == b_x:
        for y in range(min(a_y, b_y), max(a_y, b_y) + 1):
            yield (a_x, y)
    elif a_y == b_y:
        for x in range(min(a_x, b_x), max(a_x, b_x) + 1):
            yield (x, a_y)
    else:
        raise Exception("points must be a straight line", a, b)

def parse_file(input_file):
    grid = dict()
    for line in open(input_file, "r").readlines():
        prev_point = None
        for point_str in line.rstrip("\n").split(" -> "):
            x_str, y_str = point_str.split(",")
            point = (int(x_str), int(y_str))
            grid[point] = CELL_ROCK
            for line_point in points_between(prev_point, point):
                grid[line_point] = CELL_ROCK
            prev_point = point
    return grid

def grid_rect(grid):
    min_x, min_y, max_x, max_y = None, None, None, None
    for x, y in grid.keys():
        min_x = x if min_x is None else min(x, min_x)
        min_y = y if min_y is None else min(y, min_y)
        max_x = x if max_x is None else max(x, max_x)
        max_y = y if max_y is None else max(y, max_y)
    return min_x, min_y, max_x, max_y

def grid_print(grid):
    min_x, min_y, max_x, max_y = grid_rect(grid)
    for y in range(max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            cell = grid.get((x, y), CELL_EMPTY)
            if (x, y) == POINT_ORIGIN: cell = CELL_ORIGIN
            print(cell, end="")
        print("")
    print("")

def sand_fall(grid, point):
    for v in SAND_VECTORS:
        test_point = point_move(point, v)
        if grid.get(test_point, CELL_EMPTY) == CELL_EMPTY:
            return test_point
    return point

def sand_generate(grid):
    min_x, min_y, max_y, max_y = grid_rect(grid)
    point = POINT_ORIGIN
    while True:
        next_point = sand_fall(grid, point)
        if point == next_point:
            grid[point] = CELL_SAND
            return True
        if next_point[1] > max_y:
            return False
        point = next_point

grid = parse_file("input.txt")
grid_print(grid)

sand_count = 0
while sand_generate(grid):
    sand_count += 1
    print(f"After {sand_count} units of sand:")
    grid_print(grid)

print("Step 1 Answer:", sand_count)
