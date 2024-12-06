import os

from itertools import cycle
from collections import defaultdict

DAY = 6

PLAYER = '^'
OBJECT = '#'
FLOOR = '.'

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)



TEST_DATA = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''

def parse_data(data):
    parsed_map = {}
    raw_map = [list(row) for row in data.splitlines()]
    player = None
    for i in range(len(raw_map)):
        for j in range(len(raw_map[0])):
            current = raw_map[i][j]
            if current == PLAYER:
                player = (i, j)
                parsed_map[(i, j)] = FLOOR
            else:
                parsed_map[(i, j)] = current    
    return player, parsed_map

def step(player, direction):
    i, j = player
    di, dj = direction
    return (i+di, j+dj)

def is_facing_wall(player, direction, game_map):
    i, j = player
    di, dj = direction
    next_spot = (i+di, j+dj)
    if game_map[next_spot] == OBJECT:
        return True
    return False

def is_next_inside_map(player, direction, game_map):
    i, j = player
    di, dj = direction
    next_spot = (i+di, j+dj)
    return next_spot in game_map

def simulate_guard(data):
    player, game = parse_data(data)
    DIRECTIONS = cycle([UP, RIGHT, DOWN, LEFT])
    next_dir = next(DIRECTIONS)
    visited = set()

    while True:
        visited.add(player)
        if not is_next_inside_map(player, next_dir, game):
            break
        elif is_facing_wall(player, next_dir, game):
            next_dir = next(DIRECTIONS)
        else:
            player = step(player, next_dir)
    return len(visited)


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
print('Simulation:', simulate_guard(TEST_DATA) == 41)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    print('Simulation:', simulate_guard(data))