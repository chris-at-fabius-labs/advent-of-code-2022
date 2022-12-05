#!/usr/bin/env python3

import re

init_row_pattern = re.compile(r"\[[A-Z]\]")
init_end_pattern = re.compile(r"^ 1 ")
move_pattern = re.compile(r"^move (\d+) from (\d+) to (\d+)$")

def parse_init_row(line):
    i = 0
    acc = list()
    for char in line:
        if i == 1: acc.append(char)
        i = 0 if i == 3 else i + 1
    return acc

def parse_init_state(rows):
    cols = dict()
    for row in reversed(rows):
        for i, cell in enumerate(row):
            col = cols.setdefault(str(i + 1), list())
            if cell != " ": col.append(cell)
    return cols

def process_move1(state, count, move_from, move_to):
    col_from, col_to = state.get(move_from), state.get(move_to)
    for i in range(0, int(count)):
        col_to.append(col_from.pop())

def process_move2(state, count, move_from, move_to):
    col_from, col_to = state.get(move_from), state.get(move_to)
    cells = list()
    for i in range(0, int(count)): cells.append(col_from.pop())
    col_to.extend(reversed(cells))

def get_top_order(state):
    return "".join([col[-1] for col in state.values()])

rows = list()
state1 = None
state2 = None
for line in open('input.txt', 'r').readlines():
    line = line.rstrip('\n')
    if init_row_pattern.search(line):
        rows.append(parse_init_row(line))
    if init_end_pattern.search(line):
        state1 = parse_init_state(rows)
        state2 = parse_init_state(rows)
    move_match = move_pattern.search(line)
    if move_match:
        move_count, move_from, move_to = move_match.groups()
        process_move1(state1, move_count, move_from, move_to)
        process_move2(state2, move_count, move_from, move_to)

print("Step 1 Answer:", get_top_order(state1))
print("Step 2 Answer:", get_top_order(state2))
