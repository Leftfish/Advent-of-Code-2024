import os

from collections import defaultdict
from itertools import combinations

DAY = 8

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


SPACE = '.'

def parse_data(data):
    grid = {}
    for i, row in enumerate(data.splitlines()):
        for j, d in enumerate(row):
            grid[(i, j)] = d
    return grid


def find_antennae(grid):
    antennae = defaultdict(list)
    for coord, spot in grid.items():
        if spot != SPACE:
            antennae[spot].append(coord)
    return antennae


def check_antinode_pairs(this, other):
    nodes = set()
    
    di = this[0] - other[0]
    dj = this[1] - other[1]
    
    for p in (-1, 1):
        node_this = p * di + this[0], p * dj + this[1]
        node_other = p * di + other[0], p * dj + other[1]
        nodes.add(node_this)
        nodes.add(node_other)
    return nodes - set((this, other))


def find_antinodes(antennae, grid):
    antinodes = set()
    for atype in antennae:
        coords = antennae[atype]
        for this, other in combinations(coords, 2):
            antinodes |= check_antinode_pairs(this, other)
    return antinodes & grid.keys()


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
grid = parse_data(TEST_DATA)
ants = find_antennae(grid)
print('Total antinodes in pairs:', len(find_antinodes(ants, grid)) == 14)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    grid = parse_data(data)
    ants = find_antennae(grid)
    print('Total antinodes in pairs:', len(find_antinodes(ants, grid)))
