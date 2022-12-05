#!/usr/bin/env python3

def find_line_dupe(chars):
    half_len = len(chars) // 2
    a = chars[:half_len]
    b = chars[half_len:]
    return (set(a) & set(b)).pop()

def find_group_dupe(lines):
    a, b, c = lines
    return (set(a) & set(b) & set(c)).pop()

def get_priority(char):
    char_ord = ord(char)
    if char_ord >= 97: return char_ord - 96
    if char_ord >= 65: return char_ord - 38
    raise Exception("Unexpected char", char)

line_dupes = []
group_acc = []
group_dupes = []
for line in map(str.strip, open('input.txt', 'r').readlines()):
    if len(line) == 0: continue
    line_dupes.append(find_line_dupe(line))
    group_acc.append(line)
    if len(group_acc) == 3:
        group_dupes.append(find_group_dupe(group_acc))
        group_acc.clear()

print("Step 1 Answer:", sum(map(get_priority, line_dupes)))
print("Step 2 Answer:", sum(map(get_priority, group_dupes)))
