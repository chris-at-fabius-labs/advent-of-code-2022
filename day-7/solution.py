#!/usr/bin/env python3

import re

cmd_cd_pattern = re.compile(r"^\$ cd (.*)$")
cmd_ls_pattern = re.compile(r"^\$ ls$")
ls_dir_pattern = re.compile(r"^dir (.*)$")
ls_file_pattern = re.compile(r"^(\d+) (.*)$")

def cd_resolve(root, cd_path):
    cursor = root
    for dir in cd_path:
        cursor = cursor.get(dir)
    return cursor

def get_directory_size(dir):
    total_size = 0
    for item in dir.values():
        if isinstance(item, int):
            total_size += item
        elif isinstance(item, dict):
            total_size += get_directory_size(item)
    return total_size

def find_all_directories(dir):
    dirs = list()
    for item in dir.values():
        if isinstance(item, dict):
            dirs.append(item)
            subdirs = find_all_directories(item)
            dirs.extend(subdirs)
    return dirs

root = dict()
cd_path = list()
ls_pending = False
for line in open('input.txt', 'r').readlines():
    line = line.rstrip("\n")
    cd_match = cmd_cd_pattern.match(line)
    ls_match = cmd_ls_pattern.match(line)
    if cd_match:
        ls_pending = False
        dir = cd_match.group(1)
        if dir == "/": cd_path.clear()
        elif dir == "..": cd_path.pop()
        else: cd_path.append(dir)
    elif ls_match:
        ls_pending = True
    elif ls_pending:
        cwd = cd_resolve(root, cd_path)
        dir_match = ls_dir_pattern.match(line)
        file_match = ls_file_pattern.match(line)
        if dir_match:
            dir_name, = dir_match.groups()
            cwd[dir_name] = dict()
        elif file_match:
            file_size, file_name = file_match.groups()
            cwd[file_name] = int(file_size)

# Step 1
step_1_total = 0
for dir in find_all_directories(root):
    dir_size = get_directory_size(dir)
    if dir_size <= 100000:
        step_1_total += dir_size
print("Step 1 Answer", step_1_total)

# Step 2
disk_available = 70000000
disk_needed = 30000000
disk_used = get_directory_size(root)
disk_free = disk_available - disk_used
delete_threshold = disk_needed - disk_free
delete_candidates = list()
for dir in find_all_directories(root):
    dir_size = get_directory_size(dir)
    if dir_size >= delete_threshold:
        delete_candidates.append(dir)
delete_candidates.sort(key=get_directory_size)
print("Step 2 Answer", get_directory_size(delete_candidates[0]))