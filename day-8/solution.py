#!/usr/bin/env python3
 
cells = dict()
row_count = 0
col_count = 0

def get_perimeter_count():
    return row_count * 2 + col_count * 2 - 4

def check_past_edge(row_index, col_index):
    return (
        row_index < 0 or
        row_index >= row_count or
        col_index < 0 or
        col_index >= col_count
    )

def check_visible_from_edge(origin_row, origin_col):
    return (
        check_direction1(origin_row, origin_col, 0, -1) or
        check_direction1(origin_row, origin_col, -1, 0) or
        check_direction1(origin_row, origin_col, 0, +1) or
        check_direction1(origin_row, origin_col, +1, 0)
    )

def get_scenic_score(origin_row, origin_col):
    return (
        check_direction2(origin_row, origin_col, 0, -1) *
        check_direction2(origin_row, origin_col, -1, 0) *
        check_direction2(origin_row, origin_col, 0, +1) *
        check_direction2(origin_row, origin_col, +1, 0)
    )

def check_direction1(origin_row, origin_col, delta_x, delta_y): 
    origin_value = cells[(origin_row, origin_col)]
    cursor_row, cursor_col = origin_row, origin_col
    while True:
        cursor_row += delta_x
        cursor_col += delta_y
        if (check_past_edge(cursor_row, cursor_col)): return True
        cursor_value = cells[(cursor_row, cursor_col)]
        if cursor_value >= origin_value: return False

def check_direction2(origin_row, origin_col, delta_x, delta_y): 
    origin_value = cells[(origin_row, origin_col)]
    cursor_row, cursor_col = origin_row, origin_col
    seen_count = 0
    while True:
        cursor_row += delta_x
        cursor_col += delta_y
        if (check_past_edge(cursor_row, cursor_col)): break
        seen_count += 1
        cursor_value = cells[(cursor_row, cursor_col)]
        if cursor_value >= origin_value: break
    return seen_count

# Process the input file into a data structure
for row_index, line in enumerate(open('input.txt', 'r').readlines()):
    row_count = max(row_count, row_index + 1)
    for col_index, char in enumerate(line.rstrip("\n")):
        cells[(row_index, col_index)] = int(char)
        col_count = max(col_count, col_index + 1)

# Iterate through inner cells of the grid
visible_from_edge_count = get_perimeter_count()
scenic_scores = list()
for row_index in range(1, row_count - 1):
    for col_index in range(1, col_count - 1):
        if check_visible_from_edge(row_index, col_index):
            visible_from_edge_count += 1
        score = get_scenic_score(row_index, col_index) 
        scenic_scores.append(score)

print("Step 1 Answer:", visible_from_edge_count)
print("Step 2 Answer:", max(scenic_scores))
