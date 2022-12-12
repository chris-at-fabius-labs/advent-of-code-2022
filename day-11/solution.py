#!/usr/bin/env python3

import re

monkey_pattern = re.compile(r"^Monkey (\d+):$")
items_pattern  = re.compile(r"^  Starting items: (.+)$")
op_pattern     = re.compile(r"^  Operation: new = old ([*+]) (old|\d+)$")
test_pattern   = re.compile(r"^  Test: divisible by (\d+)$")
true_pattern   = re.compile(r"^    If true: throw to monkey (\d+)$")
false_pattern  = re.compile(r"^    If false: throw to monkey (\d+)$")

class Monkey:
    def __init__(self, number):
        self.number = number
        self.inspect_count = 0
        self.items = None
        self.op_type = None
        self.op_value = None
        self.divisible_by = None
        self.if_true = None
        self.if_false = None

    def inspect_item(self, old):
        self.inspect_count += 1
        a = old
        b = int(self.op_value) if self.op_value != "old" else old
        if self.op_type == "*":
            return a * b, f"multiplied by {str(b)}"
        if self.op_type == "+":
            return a + b, f"increased by {str(b)}"

    def test_worry_level(self, worry):
        return worry % self.divisible_by == 0

def create_monkeys(input_file):
    monkeys = list()
    monkey_acc = None

    for line in open('example.txt', 'r').readlines():
        line = line.rstrip("\n")

        monkey_match = monkey_pattern.match(line)
        if monkey_match:
            if monkey_acc: monkeys.append(monkey_acc)
            number = int(monkey_match.group(1))
            monkey_acc = Monkey(number)

        items_match = items_pattern.match(line)
        if items_match:
            items_str = items_match.group(1)
            monkey_acc.items = [int(x) for x in items_str.split(", ")]

        op_match = op_pattern.match(line)
        if op_match:
            op_type, op_value = op_match.groups()
            monkey_acc.op_type = op_type
            monkey_acc.op_value = op_value

        test_match = test_pattern.match(line)
        if test_match:
            monkey_acc.divisible_by = int(test_match.group(1))

        true_match = true_pattern.match(line)
        if true_match:
            monkey_acc.if_true = int(true_match.group(1))

        false_match = false_pattern.match(line)
        if false_match:
            monkey_acc.if_false = int(false_match.group(1))

    if monkey_acc: monkeys.append(monkey_acc)
    return monkeys

def run_round(monkeys, worry_divide):
    for index, monkey in enumerate(monkeys):
        # print(f"Monkey {index}")
        items_next = list()
        for item in monkey.items:
            # print(f"  Monkey inspects an item with a worry level of {item}.")
            worry_next, worry_debug = monkey.inspect_item(item)
            # print(f"    Worry level is {worry_debug} to {worry_next}.")
            if worry_divide:
                worry_next //= 3
                # print(f"    Monkey gets bored with item. Worry level is divided by 3 to {worry_next}.")
            worry_tested = monkey.test_worry_level(worry_next)
            # worry_divisible = "is" if worry_tested else "is not"
            # print(f"    Currrent worry level {worry_divisible} divisible by {monkey.divisible_by}.")
            throw_to_monkey = monkey.if_true if worry_tested else monkey.if_false
            # print(f"    Item with worry level {worry_next} is thrown to monkey {throw_to_monkey}.")
            monkeys[throw_to_monkey].items.append(worry_next)
        monkey.items = items_next

def print_monkey_items(monkeys):
    for index, monkey in enumerate(monkeys):
        items_str = ", ".join(map(str, monkey.items))
        print(f"Monkey {index}: {items_str}")

def print_monkey_inspect_counts(monkeys):
    inspect_counts = [m.inspect_count for m in monkeys]
    for index, count in enumerate(inspect_counts):
        print(f"Monkey {index} inspected items {count} times.")

def calculate_monkey_business(monkeys):
    inspect_counts = [m.inspect_count for m in monkeys]
    first, second = sorted(inspect_counts, reverse=True)[:2]
    return first * second

monkeys1 = create_monkeys("example.txt")
for i in range(20):
    run_round(monkeys1, worry_divide=True)
print("Step 1 Answer:", calculate_monkey_business(monkeys1))

# monkeys2 = create_monkeys("example.txt")
# for i in range(1, 21):
#     run_round(monkeys2, worry_divide=False)
#     # if i == 1 or i == 20 or i % 1000 == 0:
#     print(f"== After round {i} ==")
#     print_monkey_items(monkeys2)
#     # print_monkey_inspect_counts(monkeys2)
# print("Step 2 Answer:", calculate_monkey_business(monkeys2))
