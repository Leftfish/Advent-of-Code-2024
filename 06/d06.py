import os

from itertools import cycle

DAY = 6

GUARD = '^'
OBJECT = '#'
FLOOR = '.'

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)


def parse_data(data):
    parsed_map = {}
    raw_map = [list(row) for row in data.splitlines()]
    guard = None
    for i in range(len(raw_map)):
        for j in range(len(raw_map[0])):
            current = raw_map[i][j]
            if current == GUARD:
                guard = (i, j)
                parsed_map[(i, j)] = FLOOR
            else:
                parsed_map[(i, j)] = current
    return guard, parsed_map


def step(guard, direction):
    i, j = guard
    di, dj = direction
    return (i+di, j+dj)


def is_facing_wall(guard, direction, lab_map):
    i, j = guard
    di, dj = direction
    next_spot = (i+di, j+dj)
    if lab_map[next_spot] == OBJECT:
        return True
    return False


def is_next_inside_map(guard, direction, lab_map):
    i, j = guard
    di, dj = direction
    next_spot = (i+di, j+dj)
    return next_spot in lab_map


def simulate_guard(guard, lab):
    DIRECTIONS = cycle([UP, RIGHT, DOWN, LEFT])
    next_dir = next(DIRECTIONS)
    visited = set()
    visited_cycle = set()
    path_is_cycle = False

    while True:
        visited.add(guard)
        if (guard, next_dir) in visited_cycle:
            path_is_cycle = True
            break
        else:
            visited_cycle.add((guard, next_dir))

        if not is_next_inside_map(guard, next_dir, lab):
            break
        elif is_facing_wall(guard, next_dir, lab):
            next_dir = next(DIRECTIONS)
        else:
            guard = step(guard, next_dir)
    return visited, path_is_cycle


def find_obstacles(guard, lab):
    possible_obstacles, _ = simulate_guard(guard, lab)
    possible_obstacles.remove(guard)

    obstacles = set()
    for candidate in possible_obstacles:
        changed_lab = lab.copy()
        changed_lab[candidate] = OBJECT
        _, is_cycle = simulate_guard(guard, changed_lab)
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
guard, lab = parse_data(TEST_DATA)
print('Simulation:', len(simulate_guard(guard, lab)[0]) == 41)
print('Possible obstacles:', find_obstacles(guard, lab))

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    guard, lab = parse_data(data)
    print('Simulation:', len(simulate_guard(guard, lab)[0]))
    print('Possible obstacles:', find_obstacles(guard, lab))
