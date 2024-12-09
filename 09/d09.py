import os

from collections import deque, defaultdict
from itertools import cycle

DAY = 9


prog = '2333133121414131402'

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
        #print(f"Moving {memory[to_fill]} from {to_move} to {to_fill}")
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

TEST_DATA = '2333133121414131402'

memory, data, empty, files = parse_program(TEST_DATA)
empty = list(empty)

for file_id in reversed(files):
    size = files[file_id]
    space = find_space_for_file(empty, size)
    if space is not None:
        print(f'Found space for file {file_id} size={size} in {empty}. Starts at {empty[space]}')
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
        print(f'Found {space} space for file {file_id}')
        for i in range(size):
            data.pop()
        
print(calc_checksum(memory))


# find leftmost consecutive empty >= file
# move file (pop file lenght, uptaede memory), update empty (popleft file size)







print(f'Day {DAY} of Advent of Code!')
print('Testing...')
memory, data, empty, _ = parse_program(TEST_DATA)
print('Checksun with fragmentation:', calc_checksum(move_without_defrag(memory, data, empty)) == 1928)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    prog = inp.read()
    memory, data, empty, files = parse_program(prog)
    print('Checksun with fragmentation:', calc_checksum(move_without_defrag(memory, data, empty)))

'''
memory, data, empty, files = parse_program(prog)
empty = list(empty)

for file_id in reversed(files):
    size = files[file_id]
    space = find_space_for_file(empty, size)
    
    if space is not None:
        print(f'Found space for file {file_id} size={size}. Starts at {space}. Len empty is {len(empty)}')
        print(empty[space])
        addr_to_fill = empty[space]
        empty_range_to_fill = (space, space+size)
        for i in range(size):
            print('fill', i+1,'at')
            addr_to_get = data.pop()
            val_to_move = memory[addr_to_get]
            memory[addr_to_fill] = val_to_move
            memory[addr_to_get] = None
            space += 1
            addr_to_fill = empty[space]
        empty = empty[:empty_range_to_fill[0]] + empty[empty_range_to_fill[1]:]


    else:
        print(f'Found {space} space for file {file_id}')
        for i in range(size):
            data.pop()
        
print(calc_checksum(memory))

'''
memory, data, empty, files = parse_program(prog)
empty = list(empty)

for file_id in reversed(files):
    size = files[file_id]
    space = find_space_for_file(empty, size)
    if space is not None:
        #print(f'Found space for file {file_id} size={size}. Starts at {empty[space]}')
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
        #print(f'Found {space} space for file {file_id} of size {size}')
        for i in range(size):
            data.pop()
        
print(calc_checksum(memory))
