import os

DAY = 15

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

TEST_DATA2 = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<'''

WALL = '#'
BOX = 'O'
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

def show(grid):
    max_i = max([pos[0] for pos in grid.keys()])
    max_j = max([pos[1] for pos in grid.keys()])

    pic = [[None for i in range(max_i+1)] for j in range(max_j+1)]
    for i in range(max_i+1):
        for j in range(max_j+1):
            pic[i][j] = grid[(i, j)]

    for line in pic:
        print(''.join(line))
    print()



def check_move(robot, direction, grid):
    to_move = [robot]
    di, dj = DIRS[direction]
    next_field = (robot[0] + di, robot[1] + dj)
    while grid[next_field] != WALL:
        if grid[next_field] == FLOOR:
            return to_move
        to_move.append(next_field)
        next_field = (next_field[0] + di, next_field[1] + dj)
    return []

def make_moves(to_move, direction, grid, robot):
    di, dj = DIRS[direction]
    while to_move:
        i, j = to_move.pop()
        grid[(i+di, j+dj)] = grid[(i, j)]
        if grid[(i+di, j+dj)] == ROBOT:
            robot = (i+di, j+dj)
        grid[(i, j)] = FLOOR
    return grid, robot

def score(grid):
    s = 0
    for coord in grid:
        if grid[coord] == BOX:
            s += 100 * coord[0] + coord[1]
    return s

def move_boxes(grid, instructions, robot):
    for direction in instructions:
        to_move = check_move(robot, direction, grid)
        grid, robot = make_moves(to_move, direction, grid, robot)
    return grid


print(f'Day {DAY} of Advent of Code!')
grid, instructions, robot = parse(TEST_DATA)
print('Testing...')
print('Score on a small map:', score(move_boxes(*parse(TEST_DATA))) == 10092)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    print('Score on a small map:', score(move_boxes(*parse(data))))