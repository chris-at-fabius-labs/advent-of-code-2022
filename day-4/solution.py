#!/usr/bin/env python3

import re

line_pattern = re.compile(r"^(\d+)-(\d+),(\d+)-(\d+)")

def parse_line(line):
    match = line_pattern.search(line)
    if match:
        a1, a2, b1, b2 = match.groups()
        a = set(range(int(a1), int(a2) + 1))
        b = set(range(int(b1), int(b2) + 1))
        return a, b
    return set(), set()

superset_total = 0
overlap_total = 0
for line in map(str.strip, open('input.txt', 'r').readlines()):
    a, b = parse_line(line)
    if a.issuperset(b) or b.issuperset(a):
        superset_total += 1
    if len(a & b) > 0:
        overlap_total += 1

print("Step 1 Answer:", superset_total)
print("Step 2 Answer:", overlap_total)
