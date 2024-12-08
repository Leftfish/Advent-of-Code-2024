import os

from collections import defaultdict
from itertools import combinations

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
    ant_coords = set()
    for coord, spot in grid.items():
        if spot != SPACE:
            type_to_positions[spot].append(coord)
            ant_coords.add(coord)
    return type_to_positions, ant_coords


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


def check_antinode_harmonics(this, other, grid):
    nodes = set()
    di = this[0] - other[0]
    dj = this[1] - other[1]

    for p in (-1, 1):
        i, j = 1, 1
        while True:
            node_this = p * i * di + this[0], p * i * dj + this[1]
            if node_this not in grid:
                break
            nodes.add(node_this)
            i += 1
        while True:
            node_other = p * i * di + this[0], p * i * dj + this[1]
            if node_other not in grid:
                break
            nodes.add(node_other)
            j += 1
    return nodes


def find_antinodes(type_to_positions, grid):
    antinodes = set()
    for atype in type_to_positions:
        coords = type_to_positions[atype]
        for this, other in combinations(coords, 2):
            antinodes |= check_antinode_pairs(this, other)
    return antinodes & grid.keys()


def find_antinodes_harmonics(type_to_positions, grid, ant_coords):
    antinodes = set()
    for atype in type_to_positions:
        coords = type_to_positions[atype]
        for this, other in combinations(coords, 2):
            antinodes |= check_antinode_harmonics(this, other, grid)
    return antinodes & grid.keys() | ant_coords


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
ant_map, ant_coords = find_antennae(grid)
print('Total antinodes in pairs:', len(find_antinodes(ant_map, grid)) == 14)
print('Total antinodes with harmonics:', len(find_antinodes_harmonics(ant_map, grid, ant_coords)) == 34)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    grid = parse_data(data)
    ant_map, ant_coords = find_antennae(grid)
    print('Total antinodes in pairs:', len(find_antinodes(ant_map, grid)))
    print('Total antinodes with harmonics:', len(find_antinodes_harmonics(ant_map, grid, ant_coords)))
