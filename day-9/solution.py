#!/usr/bin/env python3

import re

move_pattern = re.compile(r"^([UDLR]) (\d+)$")

VECTORS = {
    "U": (0, +1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (+1, 0),
    "UL": (-1, +1),
    "UR": (+1, +1),
    "DL": (-1, -1),
    "DR": (+1, -1),
    "Z": (0, 0)
}

def get_vectors(directions):
    return [VECTORS.get(d) for d in directions]

def move_point(point, vector, distance = 1):
    return (
        point[0] + (vector[0] * distance),
        point[1] + (vector[1] * distance)
    )

def is_valid_knot_point(leader, follower):
    for vector in VECTORS.values():
        if move_point(leader, vector) == follower:
            return True
    return False

def reconcile_knot(leader, follower):
    if is_valid_knot_point(leader, follower): return follower
    for cardinal_vector in get_vectors(["U", "D", "L", "R"]):
        if leader == move_point(follower, cardinal_vector, 2):
            return move_point(follower, cardinal_vector)
    for diagonal_vector in get_vectors(["UL", "UR", "DL", "DR"]):
        check_point = move_point(follower, diagonal_vector)
        if is_valid_knot_point(leader, check_point):
            return check_point
    raise Exception("Unable to reconcile knot", leader, follower)

class Rope:
    def __init__(self, knot_count):
        self.knots = [(0, 0) for i in range(knot_count)]
        self.tail_history = set(self.knots)
    
    def move_head(self, vector, distance):
        for step in range(0, distance):
            self.knots[0] = move_point(self.knots[0], vector)
            for knot_index in range(1, len(self.knots)):
                self.knots[knot_index] = reconcile_knot(
                    self.knots[knot_index - 1],
                    self.knots[knot_index]
                )
            self.tail_history.add(self.knots[-1])
    
    def print(self):
        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        for x, y in [*self.knots, *self.tail_history]:
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)

        for y in reversed(range(min_y, max_y + 1)):
            for x in range(min_x, max_x + 1):
                cell = "."
                if (x, y) in self.tail_history: cell = "#"
                if (x, y) == (0, 0): cell = "s"
                for knot_index, knot_point in enumerate(self.knots):
                    if (x, y) == knot_point:
                        if knot_index == 0: cell = "H"
                        else: cell = str(knot_index)
                        break
                print(cell, end="")
            print("")
        print("")

step_1 = Rope(knot_count = 2)
step_2 = Rope(knot_count = 10)
for line in open('input.txt', 'r').readlines():
    move_match = move_pattern.match(line.rstrip("\n"))
    vector = VECTORS.get(move_match.group(1))
    distance = int(move_match.group(2))
    step_1.move_head(vector, distance)
    step_2.move_head(vector, distance)

print("Step 1 Answer:", len(step_1.tail_history))
# step_1.print()
print("Step 2 Answer:", len(step_2.tail_history))
# step_2.print()
