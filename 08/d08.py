import os

from collections import defaultdict
from itertools import permutations

DAY = 8

SPACE = '.'


def parse_data(data):
    grid = {}
    for i, row in enumerate(data.splitlines()):
        for j, d in enumerate(row):
            grid[(i, j)] = d
    return grid


def find_antennae(grid):
    type_to_positions = defaultdict(list)
    for coord, spot in grid.items():
        if spot != SPACE:
            type_to_positions[spot].append(coord)
    return type_to_positions


def check_antinode_pairs(this, other, grid):
    nodes = set()

    di = this[0] - other[0]
    dj = this[1] - other[1]

    
    node_this = di + this[0], dj + this[1]
    node_other = di + other[0], dj + other[1]
    if node_this in grid:
        nodes.add(node_this)
    if node_other in grid:
        nodes.add(node_other)
    return nodes - set((this, other))


def check_antinode_harmonics(this, other, grid):
    nodes = set()
    di = this[0] - other[0]
    dj = this[1] - other[1]

    i, j = 1, 1
    while True:
        node_this = i * di + this[0], i * dj + this[1]
        if node_this not in grid:
            break
        nodes.add(node_this)
        i += 1
    while True:
        node_other = i * di + this[0], i * dj + this[1]
        if node_other not in grid:
            break
        nodes.add(node_other)
        j += 1

    return nodes | set((this, other))


def find_antinodes(type_to_positions, grid):
    antinodes = set()
    antinodes_harmonics = set()
    for atype in type_to_positions:
        coords = type_to_positions[atype]
        for this, other in permutations(coords, 2):
            antinodes |= check_antinode_pairs(this, other, grid)
            antinodes_harmonics |= check_antinode_harmonics(this, other, grid)
    return antinodes, antinodes_harmonics


TEST_DATA = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
grid = parse_data(TEST_DATA)
antinodes, antinodes_harmonics = find_antinodes(find_antennae(grid), grid)
print('Total antinodes in pairs:', len(antinodes) == 14)
print('Total antinodes with harmonics:', len(antinodes_harmonics) == 34)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    grid = parse_data(data)
    antinodes, antinodes_harmonics = find_antinodes(find_antennae(grid), grid)
    print('Total antinodes in pairs:', len(antinodes))
    print('Total antinodes with harmonics:', len(antinodes_harmonics))
