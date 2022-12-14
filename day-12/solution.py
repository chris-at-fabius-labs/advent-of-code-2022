#!/usr/bin/env python3

grid = dict()
start_coord = None
end_coord = None

def parse_elevation(char):
    if char == "S": return parse_elevation("a")
    if char == "E": return parse_elevation("z")
    return ord(char) - ord("a")

for y, line in enumerate(open('input.txt', 'r').readlines()):
    for x, char in enumerate(line.rstrip("\n")):
        grid[(x, y)] = parse_elevation(char)
        if char == "S": start_coord = (x, y)
        if char == "E": end_coord = (x, y)

x_max = max([x for x, y in grid.keys()])
y_max = max([y for x, y in grid.keys()])

VECTORS = {
    "^": (0, -1),
    "v": (0, +1),
    "<": (-1, 0),
    ">": (+1, 0)
}

def move_point(point, vector, distance = 1):
    return (
        point[0] + (vector[0] * distance),
        point[1] + (vector[1] * distance)
    )

def steps_iter(steps):
    head, tail = steps
    while head and tail:
        yield head
        head, tail = tail

def steps_len(steps):
    return sum(1 for _ in steps_iter(steps))

def steps_push(steps, coord):
    return (coord, steps)

def steps_has(steps, coord):
    for step in steps_iter(steps):
        if step == coord: return True
    return False

def steps_print(steps):
    lookup = dict()
    last_coord, rest_coords = steps
    if last_coord:
        lookup[last_coord] = "E"
        for coord in steps_iter(rest_coords):
            for d, v in VECTORS.items():
                if last_coord == move_point(coord, v):
                    lookup[coord] = d
                    break
            last_coord = coord
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            cell = lookup.get((x, y), ".")
            print(cell, end="")
        print("")
    print("")

def route_path(cursor, steps):
    if cursor == end_coord:
        count = steps_len(steps)
        print(f"Found a suitable route in {count} steps!")
        yield (cursor, steps)
        return
    # print("Currently visiting", cursor)
    cursor_elevation = grid[cursor]
    # print("Current elevation:", cursor_elevation)
    for direction, vector in VECTORS.items():
        # print(f"  Checking {direction}...")
        test_coord = move_point(cursor, vector)
        if steps_has(steps, test_coord):
            # print("    Destination has already been visited")
            continue
        test_elevation = grid.get(test_coord)
        if test_elevation is None:
            # print("    Destination is out-of-bounds")
            continue
        if test_elevation > cursor_elevation + 1:
            # print(f"    Destination elevation {test_elevation} is unreachable")
            continue
        next_steps = steps_push(steps, cursor)
        # print("    Destination is viable, exploring further")
        yield explore_routes(test_coord, next_steps)
    yield (cursor, steps)

def explore_routes(cursor, steps = (None, None)):
    # print(f"Exploring routes from {cursor}:")
    # steps_print(steps)
    winning_route, winning_len = None, None
    for next_cursor, next_steps in route_path(cursor, steps):
        if next_cursor == end_coord:
            next_steps_len = steps_len(next_steps)
            if not winning_route or winning_len > next_steps_len:
                winning_route = next_steps
                winning_len = next_steps_len
    if winning_route: return end_coord, winning_route
    return cursor, steps

print(f"Start: {start_coord} Goal: {end_coord}")
destination, steps = explore_routes(start_coord)
print(f"Destination: {destination} in {steps_len(steps)} steps")
print("Steps:")
steps_print(steps)
