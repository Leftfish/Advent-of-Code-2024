import os

from itertools import product

DAY = 25

def parse(data):
    locks, keys = [], []
    chck = '#####'
    for scheme in data.split('\n\n'):
        lines = scheme.splitlines()
        if lines[0] == chck:
            keys.append([sum([1 for r in range(1, len(lines)) if lines[r][c] == '#']) for c in range(len(lines[0]))]) 
        if lines[-1] == chck:
            locks.append([sum([1 for r in range(len(lines)-2, 0, -1) if lines[r][c] == '#']) for c in range(len(lines[0]))])
    return locks, keys

def check_all(locks, keys):
    return sum([all([5 >= a + b >= 0 for a, b in zip(k, l)]) for k, l in product(locks, keys)])


TEST_DATA = '''#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
print('Testing keys:', check_all(*parse(TEST_DATA)) == 3)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    print('Testing keys:', check_all(*parse(data)))
