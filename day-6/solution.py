#!/usr/bin/env python3

def find_start(line, count):
    markers = list()
    for index, char in enumerate(line):
        markers.append(char)
        if len(set(markers)) == count: return index + 1
        if len(markers) == count: markers.pop(0)

for line in open('input.txt', 'r').readlines():
    print("Packet:", line.rstrip("\n"))
    print("Start of Packet:", find_start(line, 4))
    print("Start of Message:", find_start(line, 14))
    print("")
