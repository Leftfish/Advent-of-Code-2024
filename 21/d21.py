### The solution implements this tutorial:
### https://www.reddit.com/r/adventofcode/comments/1hjx0x4/2024_day_21_quick_tutorial_to_solve_part_2_in/
### I gave up after three unsuccessful attempts to solve Day 21 by myself.

import os

from itertools import product
import networkx as nx

DAY = 21

NUMPAD = '''789
456
123
.0A'''

KEYPAD = '''.^A
<v>'''

ENTER = 'A'

U, D, L, R, A = '^', 'v', '<', '>', 'A'

NUMPAD_DIRECTIONS = {('0', 'A'): R,
                      ('A', '0'): L,
                      ('1', '2'): R,
                      ('2', '1'): L,
                      ('2', '3'): R,
                      ('3', '2'): L,
                      ('4', '5'): R,
                      ('5', '4'): L,
                      ('5', '6'): R,
                      ('6', '5'): L,
                      ('7', '8'): R,
                      ('8', '7'): L,
                      ('8', '9'): R,
                      ('9', '8'): L,
                      ('1', '4'): U,
                      ('4', '1'): D,
                      ('4', '7'): U,
                      ('7', '4'): D,
                      ('0', '2'): U,
                      ('2', '0'): D,
                      ('2', '5'): U,
                      ('5', '2'): D,
                      ('5', '8'): U,
                      ('8', '5'): D,
                      ('A', '3'): U,
                      ('3', 'A'): D,
                      ('3', '6'): U,
                      ('6', '3'): D,
                      ('6', '9'): U,
                      ('9', '6'): D,
                      ('0', '0'): A,
                      ('1', '1'): A,
                      ('2', '2'): A,
                      ('3', '3'): A,
                      ('4', '4'): A,
                      ('5', '5'): A,
                      ('6', '6'): A,
                      ('7', '7'): A,
                      ('8', '8'): A,
                      ('9', '9'): A,
                      ('A', 'A'): A}

KEYPAD_DIRECTIONS = {('^', 'A'): R,
                     ('A', '^'): L,
                     ('<', 'v'): R,
                     ('v', '<'): L,
                     ('v', '>'): R,
                     ('>', 'v'): L,
                     ('v', '^'): U,
                     ('^', 'v'): D,
                     ('>', 'A'): U,
                     ('A', '>'): D,
                     ('A', 'A'): A,
                     ('>', '>'): A,
                     ('<', '<'): A,
                     ('v', 'v'): A,
                     ('^', '^'): A}

directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))


def get_shortest_paths(keyboard):
    grd = list(line for line in keyboard.splitlines())
    keyboard_graph = {}
    graph = nx.Graph()
    for i, line in enumerate(grd):
        for j, c in enumerate(line):
            if c != '.':
                keyboard_graph[(i, j)] = c
                graph.add_node(c)

    for k, v in keyboard_graph.items():
        i, j = k
        for direction in directions:
            di, dj = direction
            adj = (i+di, j+dj)
            if adj in keyboard_graph:
                graph.add_edge(v, keyboard_graph[adj])

    node_to_node = product(graph.nodes, graph.nodes)
    paths = {}
    for pair in node_to_node:
        start, end = pair

        paths[(start, end)] = list(nx.all_shortest_paths(graph, start, end))
        paths[(end, start)] = list(nx.all_shortest_paths(graph, end, start))
    return paths


def convert_to_arrows(current, target, pad_paths, pad_directions):
    paths = []
    candidates = pad_paths[(current, target)]
    for c in candidates:
        s = ''
        steps = zip(c, c[1:])
        for step in steps:
            s += pad_directions[step]
        paths.append(s)
    return paths


def build_sequence(to_write, idx, previous, current_path, result, translation_dict):
    if idx == len(to_write):
        result.append(current_path)
        return result
    for path in translation_dict[previous, to_write[idx]]:
        build_sequence(to_write, idx+1, to_write[idx], current_path + path + 'A', result, translation_dict)
    return result


def splita(seq):
    res = []
    i, j = 0, 0
    while j < len(seq):
        if seq[j] == 'A':
            res.append(seq[i:j+1])
            i = j + 1
        j += 1
    return res


def get_shortest(to_write, depth, cache):
    if depth == 0:
        return len(to_write)

    if (to_write, depth) in cache:
        return cache[(to_write, depth)]

    split = splita(to_write)
    total = 0

    for sub_to_write in split:
        sequences = build_sequence(sub_to_write, 0, 'A', '', [], keypad_paths_translated)
        lengths = [get_shortest(sequence, depth-1, cache) for sequence in sequences]
        total += min(lengths)

    cache[to_write, depth] = total

    return total


def solve(all_nums_to_write, max_depth, cache, numpad_paths_translated):
    result = 0
    for nums_to_write in all_nums_to_write:
        nums_to_arrows = build_sequence(nums_to_write, 0, 'A', '', [], numpad_paths_translated)
        to_int = int(nums_to_write[:-1])
        candidates = [get_shortest(sequence, max_depth, cache) for sequence in nums_to_arrows]
        result += min(candidates) * to_int
    return result


TEST_DATA = '''029A
980A
179A
456A
379A'''



keypad_paths = get_shortest_paths(KEYPAD)
keypad_paths_translated = {(this, other): convert_to_arrows(this, other, keypad_paths, KEYPAD_DIRECTIONS) for this, other in keypad_paths}
numpad_paths = get_shortest_paths(NUMPAD)
numpad_paths_translated = {(this, other): convert_to_arrows(this, other, numpad_paths, NUMPAD_DIRECTIONS) for this, other in numpad_paths}

print(f'Day {DAY} of Advent of Code!')
print('Testing...')
cache = {}
print('Two robots:', solve(TEST_DATA.splitlines(), 2, cache, numpad_paths_translated))
print('Twenty five robots:', solve(TEST_DATA.splitlines(), 25, cache, numpad_paths_translated))

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    cache = {}
    print('Two robots:', solve(data.splitlines(), 2, cache, numpad_paths_translated))
    print('Twenty five robots:', solve(data.splitlines(), 25, cache, numpad_paths_translated))
