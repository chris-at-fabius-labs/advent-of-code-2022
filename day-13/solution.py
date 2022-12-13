#!/usr/bin/env python3

def find_close_bracket(s, i):
    next_close_index = s.find("]", i)
    if next_close_index == -1:
        raise Exception("No close bracket found", s, i)
    sub_open_index = s.find("[", i + 1, next_close_index)
    if sub_open_index == -1:
        return next_close_index
    sub_close_index = find_close_bracket(s, sub_open_index)
    return find_close_bracket(s, sub_close_index + 1)

def split_list_inner(s):
    if s == "": return list()
    elements = list()
    i = 0
    while i < len(s):
        if s[i] == "[":
            close_index = find_close_bracket(s, i)
            elements.append(s[i:close_index + 1])
            i = close_index + 1
            continue
        sep_index = s.find(",", i)
        if i == sep_index:
            i += 1
            continue
        if sep_index > -1:
            elements.append(s[i:sep_index])
            i = sep_index + 1
            continue
        else:
            elements.append(s[i:])
            break
    return elements


def parse_list_element(s):
    if len(s) >= 2 and s[0] == "[" and s[-1] == "]":
        elements = split_list_inner(s[1:-1])
        return [parse_list_element(e) for e in elements]
    return int(s)

def parse_file(input_file):
    left_acc = None
    right_acc = None
    for line in open(input_file, "r").readlines():
        if line == "\n":
            yield (left_acc, right_acc)
            left_acc = None
            right_acc = None
            continue
        parsed = parse_list_element(line.rstrip("\n"))
        if left_acc is None: left_acc = parsed
        elif right_acc is None: right_acc = parsed
    if left_acc and right_acc:
        yield (left_acc, right_acc)

def compare(left, right):
    print(f"Comparing {left} vs {right}")
    if isinstance(left, int) and isinstance(right, int):
        if left > right: return 1
        if right > left: return -1
        return 0
    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])
    for i in range(min(len(left), len(right))):
        i_compare = compare(left[i], right[i])
        if i_compare != 0: return i_compare
    return compare(len(left), len(right))

left_indexes = list()
for index, pair in enumerate(parse_file("input.txt"), start=1):
    left, right = pair
    print(f"Pair {index}\n{left}\n{right}")
    result = compare(left, right)
    print(f"Result: {result}\n")
    if result == -1: left_indexes.append(index)
print("Step 1 Answer:", sum(left_indexes))

divider_packets = list()
for line in open("divider_packets.txt", "r").readlines():
    parsed = parse_list_element(line.rstrip("\n"))
    divider_packets.append(parsed)
