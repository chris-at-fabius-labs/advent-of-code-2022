
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
    cells = dict()
    for line in open(input_file, "r").readlines():
        prev_point = None
        for point_str in line.rstrip("\n").split(" -> "):
            x_str, y_str = point_str.split(",")
            point = (int(x_str), int(y_str))
            cells[point] = CELL_ROCK
            for line_point in points_between(prev_point, point):
                cells[line_point] = CELL_ROCK
            prev_point = point
    return cells

class Grid:
    def __init__(self, input_file, has_floor = False):
        self.cells = parse_file(input_file)
        if has_floor:
            min_x, min_y, max_x, max_y = self.get_bounds()
            self.floor_y = max_y + 2
        else:
            self.floor_y = None

    def get_cell(self, point):
        if self.floor_y and point[1] == self.floor_y:
            return CELL_ROCK
        return self.cells.get(point, CELL_EMPTY)

    def set_cell(self, point, value):
        self.cells[point] = value
    
    def get_bounds(self):
        min_x, min_y, max_x, max_y = None, None, None, None
        for x, y in self.cells.keys():
            min_x = x if min_x is None else min(x, min_x)
            min_y = y if min_y is None else min(y, min_y)
            max_x = x if max_x is None else max(x, max_x)
            max_y = y if max_y is None else max(y, max_y)
        return min_x, min_y, max_x, max_y
    
    def print(self):
        min_x, min_y, max_x, max_y = self.get_bounds()
        for y in range(max_y + 3):
            for x in range(min_x - 1, max_x + 2):
                cell = self.get_cell((x, y))
                if (x, y) == POINT_ORIGIN and cell == CELL_EMPTY:
                    cell = CELL_ORIGIN
                print(cell, end="")
            print("")
        print("")

    def sand_fall(self, point):
        for v in SAND_VECTORS:
            test_point = point_move(point, v)
            if self.get_cell(test_point) == CELL_EMPTY:
                return test_point
        return point

    def sand_generate(self):
        min_x, min_y, max_x, max_y = self.get_bounds()
        point = POINT_ORIGIN
        while True:
            if point == POINT_ORIGIN and self.get_cell(point) == CELL_SAND:
                return False
            next_point = self.sand_fall(point)
            if point == next_point:
                self.set_cell(point, CELL_SAND)
                return True
            if not self.floor_y and next_point[1] > max_y:
                return False
            point = next_point
    
    def sand_fill(self):
        sand_count = 0
        while self.sand_generate():
            sand_count += 1
            # print(f"After {sand_count} units of sand:")
            # self.print()
        return sand_count

grid1 = Grid("input.txt", has_floor = False)
# grid1.print()
print("Step 1 Answer:", grid1.sand_fill())

grid2 = Grid("input.txt", has_floor = True)
# grid2.print()
print("Step 2 Answer:", grid2.sand_fill())
