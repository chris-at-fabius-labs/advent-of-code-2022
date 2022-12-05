#!/usr/bin/env python3

acc, totals = 0, []
for line in map(str.strip, open('input.txt', 'r').readlines()):
    if len(line): acc += int(line)
    else: totals.append(acc); acc = 0
print("Step 1 Answer:", max(totals))
print("Step 2 Answer:", sum(sorted(totals, reverse=True)[0:3]))
