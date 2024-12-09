import os

from collections import deque
from itertools import cycle

DAY = 9


# PART 1 WITH DEQUES

def prase_program_simple(prog):
    switch = cycle(["DATA", "EMPTY"])
    memory = {}
    data = deque()
    empty = deque()

    addr = 0
    file = 0

    for digit in prog:
        d = int(digit)
        where = next(switch)
        if where == "DATA":
            for _ in range(d):
                memory[addr] = file
                data.append(addr)
                addr += 1
            file += 1
        elif where == "EMPTY":
            for _ in range(d):
                memory[addr] = None
                empty.append(addr)
                addr += 1
    return memory, data, empty

def move_without_defrag(memory, data, empty):
    while True:
        to_fill = empty.popleft()
        to_move = data.pop()
        if to_move < to_fill:
            break
        memory[to_fill] = memory[to_move]
        memory[to_move] = None
    return memory

def calc_checksum(memory):
    checksum = 0
    for i, val in enumerate(memory.values()):
        if val is not None:
            checksum += i * val
    return checksum

### PART 2 WITH OBJECTS AND POINTERS

class File:
    def __init__(self, file_id, size, start):
        self.file_id = file_id
        self.size = size
        self.start = start

    def __repr__(self):
        return f'<ID: {self.file_id} SIZE: {self.size} SPAN: {self.start}-{self.start+self.size-1}>'

    def checksum(self):
        s = 0
        for i in range(self.start, self.start+self.size):
            s += i * self.file_id
        return s


def parse_with_objects(prog):
    switch = cycle(["DATA", "EMPTY"])
    memory = []
    empty = []
    i = 0
    pointer = 0

    for digit in prog:
        current = next(switch)
        if current == "DATA":
            file_idx = i
            file_size = int(digit)
            file_start = pointer
            new_file = File(file_idx, file_size, file_start)
            memory.append(new_file)
            i += 1
            pointer += file_size
        elif current == "EMPTY":
            empty_size = int(digit)
            if empty_size:
                empty.append([pointer, empty_size])
                pointer += empty_size
    return memory, empty


def move_files(files_to_move, empty):
    while files_to_move:
        file_to_move = files_to_move.pop()
        file_size = file_to_move.size
        file_start = file_to_move.start
        for space in empty:
            space_start, space_size = space
            if space_size >= file_size and space_start < file_start:
                file_to_move.start = space[0]
                space[0] += file_to_move.size
                space[1] -= file_to_move.size
                break

TEST_DATA = '2333133121414131402'

print(f'Day {DAY} of Advent of Code!')
print('Testing...')
memory, data, empty = prase_program_simple(TEST_DATA)
print('Checksum without defrag:', calc_checksum(move_without_defrag(memory, data, empty)) == 1928)
memory, empty = parse_with_objects(TEST_DATA)
files_to_move = memory[::]
move_files(files_to_move, empty)
print('Checksum with defrag:', sum((file.checksum() for file in memory)) == 2858)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    raw_data = inp.read()
    memory, data, empty = prase_program_simple(raw_data)
    print('Checksum without defrag:', calc_checksum(move_without_defrag(memory, data, empty)))
    memory, empty = parse_with_objects(raw_data)
    files_to_move = memory[::]
    move_files(files_to_move, empty)
    print('Checksum with defrag:', sum((file.checksum() for file in memory)))
