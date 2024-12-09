import os

from collections import deque, defaultdict
from itertools import cycle

DAY = 9


prog = '233313312141413140222'

def parse_program(prog):
    switch = cycle(["DATA", "EMPTY"])
    memory = {}
    data = deque()
    empty = deque()
    files = defaultdict(int)

    addr = 0
    file = 0

    for digit in prog:
        d = int(digit)
        where = next(switch)
        if where == "DATA":
            for i in range(d):
                memory[addr] = file
                data.append(addr)
                addr += 1
                files[file] += 1
            file += 1
        elif where == "EMPTY":
            for i in range(d):
                memory[addr] = None
                empty.append(addr)
                addr += 1
    return memory, data, empty, files

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
        if val is None:
            continue
        checksum += i * val
    return checksum

def find_space_for_file(empty, size):
    i, j = 0, 1
    space = 1

    while True:
        if space == size:
            #print('found space for', size, 'at', i)
            return i
        if i >= len(empty) or j >= len(empty):
            #print('no space')
            return None
        
        #print(f'Empty[{i}] i = {empty[i]} empty [{j-1}] j-1 = {empty[j-1]} empty[{j}] j = {empty[j]}')
        
        if empty[j] == empty[j-1] + 1:
            j += 1
            #print(f'Consecutive. Now i = {i} and j = {j}')
            space = j - i 
        else:
            i += 1
            j = i + 1
            #print(f'Not consecutive. Now i = {i} and j = {j}')
            space = j - i 
        #print(f'Space is {space}')

def print_memory(memory):
    s = ''
    for item in memory:
        if memory[item] is None:
            s += '.'
        else:
            s += '@'
    return s


TEST_DATA = '2333133121414131402'

memory, data, empty, files = parse_program(TEST_DATA)
empty = list(empty)

for file_id in reversed(files):
    size = files[file_id]
    space = find_space_for_file(empty, size)
    if space is not None:
        #print(f'Found space for file {file_id} size={size} in {empty}. Starts at {empty[space]}')
        empty_range_to_fill = (space, space+size)
        for i in range(size):
            addr_to_fill = empty[space]
            addr_to_get = data.pop()
            val_to_move = memory[addr_to_get]
            memory[addr_to_fill] = val_to_move
            memory[addr_to_get] = None
            space += 1
            
        empty = empty[:empty_range_to_fill[0]] + empty[empty_range_to_fill[1]:]

    else:
        #print(f'Found {space} space for file {file_id}')
        for i in range(size):
            data.pop()
        
print(calc_checksum(memory))
print(print_memory(memory))

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


def parse(prog):
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

memory, empty = parse(TEST_DATA)

print(memory, empty)
to_move = memory[::]

while to_move:
    file_to_move = to_move.pop()
    file_size = file_to_move.size
    #print('Moving', file_to_move)
    for space in empty:
        if space[1] >= file_size:
            file_to_move.start = space[0]
            space[0] += file_to_move.size
            space[1] -= file_to_move.size
            #print('file moved', file_to_move)
            break
    #print('file not moved')

print(memory, empty)
x = 0
for file in memory:
    x += file.checksum()
print(x)


def pr(memory):
    s = ''
    for item in memory:
        if item is None:
            s += '.'
        else:
            s += str(item[0])
    print(s)

print()
print(f'Day {DAY} of Advent of Code!')
print('Testing...')
#memory, data, empty, _ = parse_program(TEST_DATA)
#print('Checksum with fragmentation:', calc_checksum(move_without_defrag(memory, data, empty)) == 1928)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    prog = inp.read()
    #memory, data, empty, files = parse_program(prog)
    #print('Checksum with fragmentation:', calc_checksum(move_without_defrag(memory, data, empty)))



memory, empty = parse(prog)

#print(memory, empty)
to_move = memory[::]

while to_move:

    file_to_move = to_move.pop()
    file_size = file_to_move.size
    #print('Moving', file_to_move)
    for space in empty:
        if space[1] >= file_size:
            file_to_move.start = space[0]
            space[0] += file_to_move.size
            space[1] -= file_to_move.size
            #print('file moved', file_to_move)
            break
    #print('file not moved')

#print(memory, empty)
x = 0
for file in memory:
    x += file.checksum()
print(x)
