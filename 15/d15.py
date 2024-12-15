import os

from collections import deque

DAY = 15

WALL = '#'
BOX = 'O'
BOX_L = '['
BOX_R = ']'
FLOOR = '.'
ROBOT = '@'
DIRS = {'<': (0, -1),
              'v': (1, 0),
              '>': (0, 1),
              '^': (-1, 0)}

def parse(data):
    grid = {}
    instructions = []
    robot = None

    raw_grid, raw_instructions = data.split('\n\n')

    for i, row in enumerate(raw_grid.splitlines()):
        for j, c in enumerate(row):
            grid[(i, j)] = c
            if c == ROBOT:
                robot = (i, j)

    for line in raw_instructions:
        for c in list(line.strip()):
            instructions.append(c)

    return grid, instructions, robot


def parse_and_resize(data):
    grid = {}
    instructions = []
    robot = None
    raw_grid = []
    initial_grid, raw_instructions = data.split('\n\n')

    for row in initial_grid.splitlines():
        row = row.replace('#', '##')
        row = row.replace('O', '[]')
        row = row.replace('.', '..')
        row = row.replace('@', '@.')
        raw_grid.append(row)

    for i, row in enumerate(raw_grid):
        for j, c in enumerate(row):
            grid[(i, j)] = c
            if c == ROBOT:
                robot = (i, j)

    for line in raw_instructions:
        for c in list(line.strip()):
            instructions.append(c)

    return grid, instructions, robot


def show(grid):
    max_i = max([pos[0] for pos in grid.keys()])
    max_j = max([pos[1] for pos in grid.keys()])

    pic = [[None for h in range(max_j+1)] for w in range(max_i+1)]

    for i in range(len(pic)):
        for j in range(len(pic[0])):
            pic[i][j] = grid[(i, j)]

    for line in pic:
        print(''.join(line))
    print()


def check_move(robot, direction, grid, part):
    def simple_move(robot, direction, grid):
        to_move = [robot]
        di, dj = DIRS[direction]
        next_field = (robot[0] + di, robot[1] + dj)
        while grid[next_field] != WALL:
            if grid[next_field] == FLOOR:
                return to_move
            to_move.append(next_field)
            next_field = (next_field[0] + di, next_field[1] + dj)
        return []

    def vertical_move(robot, direction, grid):
        to_move = []
        di, dj = DIRS[direction]
        next_field = (robot[0] + di, robot[1] + dj)
        if grid[next_field] == WALL:
            return to_move
        elif grid[next_field] == FLOOR:
            to_move.append(robot)
        else:
            to_move.append(robot)

            boxes = deque()
            if grid[next_field] == BOX_L:
                boxes.append((next_field, (next_field[0], next_field[1]+1)))
            elif grid[next_field] == BOX_R:
                boxes.append((next_field, (next_field[0], next_field[1]-1)))

            visited = set()
            while boxes:
                current_box = boxes.popleft()
                if current_box in visited:
                    continue

                visited.add(current_box)

                for coord in current_box:
                    to_move.append(coord)
                    next_field = (coord[0] + di, coord[1] + dj)
                    next_box = None
                    if grid[next_field] == WALL:
                        return []
                    elif grid[next_field] == BOX_L:
                        next_box = (next_field, (next_field[0], next_field[1]+1))
                    elif grid[next_field] == BOX_R:
                        next_box = ((next_field[0], next_field[1]-1), next_field)
                    if next_box and next_box not in boxes:
                        boxes.append(next_box)
        return to_move

    if part == 1:
        return simple_move(robot, direction, grid)
    elif part == 2:
        return simple_move(robot, direction, grid) if direction in ('<', '>') \
            else vertical_move(robot, direction, grid)


def make_moves(to_move, direction, grid, robot):
    di, dj = DIRS[direction]
    while to_move:
        i, j = to_move.pop()
        grid[(i+di, j+dj)] = grid[(i, j)]
        if grid[(i+di, j+dj)] == ROBOT:
            robot = (i+di, j+dj)
        grid[(i, j)] = FLOOR
    return grid, robot


def score(grid, part):
    s = 0
    for coord in grid:
        search = BOX if part == 1 else BOX_L
        if grid[coord] == search:
            s += 100 * coord[0] + coord[1]
    return s


def move_boxes(grid, instructions, robot, part):
    for direction in instructions:
        to_move = check_move(robot, direction, grid, part)
        grid, robot = make_moves(to_move, direction, grid, robot)
    return grid


TEST_DATA = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''


print(f'Day {DAY} of Advent of Code!')
grid, instructions, robot = parse(TEST_DATA)
print('Testing...')
print('Score on a small map:', score(move_boxes(*parse(TEST_DATA), 1), 1) == 10092)
print('Score on a large map:', score(move_boxes(*parse_and_resize(TEST_DATA), 2), 2) == 9021)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    print('Score on a small map:', score(move_boxes(*parse(data), 1), 1))
    print('Score on a large map:', score(move_boxes(*parse_and_resize(data), 2), 2))
