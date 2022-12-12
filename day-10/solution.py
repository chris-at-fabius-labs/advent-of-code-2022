#!/usr/bin/env python3

import re

addx_pattern = re.compile(r"^addx (-?\d+)$")

class OpNoop:
    def __init__(self):
        self.delay = 1

class OpAddx:
    def __init__(self, value):
        self.delay = 2
        self.value = value

class Cpu:
    def __init__(self):
        self.cycles = 0
        self.op_queue = list()
        self.register_x = 1

    def addx(self, value):
        self.op_queue.append(OpAddx(value))

    def noop(self):
        self.op_queue.append(OpNoop())

    def tick(self):
        self.cycles += 1
        op = self.op_queue[0]
        op.delay -= 1
        if op.delay == 0:
            if isinstance(op, OpAddx):
                self.register_x += op.value
            self.op_queue.pop(0)

    def run(self):
        while len(self.op_queue):
            value = self.register_x
            self.tick()
            yield self.cycles, value

cpu = Cpu()
for line in open('input.txt', 'r').readlines():
    line = line.rstrip("\n")
    addx_match = addx_pattern.match(line)
    if addx_match:
        addx_value = int(addx_match.group(1))
        cpu.addx(addx_value)
    elif line == "noop":
        cpu.noop()

def is_sprite_overlap(position, sprite_center):
    sprite = set([sprite_center - 1, sprite_center, sprite_center + 1])
    return (position % 40) in sprite

signal_samples = list()
pixels = list()
for cycle, value in cpu.run():
    # Gather signal samples for Step 1 answer
    if cycle == 20 or (cycle - 20) % 40 == 0:
        signal_samples.append(cycle * value)
    # Draw a pixel of the display for Step 2 answer
    pixels.append(is_sprite_overlap(cycle - 1, value))
    if cycle == 240: break

print("Step 1 Answer:", sum(signal_samples))

print("Step 2 Answer:")
for index, pixel in enumerate(pixels):
    print("#" if pixel else ".", end="")
    if (index + 1) % 40 == 0: print("")
print("")
