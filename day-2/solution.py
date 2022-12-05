#!/usr/bin/env python3

rock, paper, scissors = 1, 2, 3
lose, draw, win = 'X', 'Y', 'Z'

def rps_parse(input):
    if input in ('A', 'X'): return rock
    if input in ('B', 'Y'): return paper
    if input in ('C', 'Z'): return scissors
    raise Exception("Unexpected input", input)

def rps_score1(a, b):
    if a == b: return b + 3 # Draw
    if a == rock and b == scissors:  return b
    if a == scissors and b == paper: return b
    if a == paper and b == rock:     return b
    return b + 6 # Win

def rps_score2(a, outcome):
    if   outcome == draw:  b = a
    elif outcome == lose:
        if a == rock:      b = scissors
        if a == paper:     b = rock
        if a == scissors:  b = paper
    elif outcome == win:
        if a == rock:      b = paper
        if a == paper:     b = scissors
        if a == scissors:  b = rock
    else: raise Exception("Unexpected outcome", outcome)
    return rps_score1(a, b)
    
step1Total, step2Total = 0, 0
for line in map(str.strip, open('input.txt', 'r').readlines()):
    if len(line) == 0: continue
    col1, col2 = line.split(' ')
    step1Total += rps_score1(rps_parse(col1), rps_parse(col2))
    step2Total += rps_score2(rps_parse(col1), col2)
print("Step 1 Answer:", step1Total)
print("Step 2 Answer:", step2Total)
