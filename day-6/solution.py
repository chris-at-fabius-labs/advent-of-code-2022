#!/usr/bin/env python3

def find_start(line, count):
    markers = list()
    for i, c in enumerate(line):
        markers.append(c)
        if len(markers) < count: continue
        if len(set(markers)) == count: return i + 1
        markers.pop(0)

for line in open('input.txt', 'r').readlines():
    line = line.rstrip('\n')
    start_of_packet = find_start(line, 4)
    start_of_message = find_start(line, 14)
    print(line, start_of_packet, start_of_message)
