import os

from itertools import cycle

DAY = 6

PLAYER = '^'
OBJECT = '#'
FLOOR = '.'

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)


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


def simulate_guard(player, game):
    DIRECTIONS = cycle([UP, RIGHT, DOWN, LEFT])
    next_dir = next(DIRECTIONS)
    visited = set()
    visited_cycle = set()
    path_is_cycle = False

    while True:
        visited.add(player)
        if (player, next_dir) in visited_cycle:
            path_is_cycle = True
            break
        else:
            visited_cycle.add((player, next_dir))

        if not is_next_inside_map(player, next_dir, game):
            break
        elif is_facing_wall(player, next_dir, game):
            next_dir = next(DIRECTIONS)
        else:
            player = step(player, next_dir)
    return visited, path_is_cycle


def find_obstacles(player, game):
    possible_obstacles, _ = simulate_guard(player, game)
    possible_obstacles.remove(player)

    obstacles = set()
    for candidate in possible_obstacles:
        changed_game = game.copy()
        changed_game[candidate] = OBJECT
        _, is_cycle = simulate_guard(player, changed_game)
        if is_cycle:
            obstacles.add(candidate)

    return len(obstacles)


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


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
player, game = parse_data(TEST_DATA)
print('Simulation:', len(simulate_guard(player, game)[0]) == 41)
print('Possible obstacles:', find_obstacles(player, game))

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    player, game = parse_data(data)
    print('Simulation:', len(simulate_guard(player, game)[0]))
    print('Possible obstacles:', find_obstacles(player, game))
