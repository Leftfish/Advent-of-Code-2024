import os

DAY = 10

HEAD = 0
END = 9

def parse_grid(data):
    grid = {}
    for i, row in enumerate(data.splitlines()):
        for j, val in enumerate(row):
            if val.isnumeric():
                grid[(i, j)] = int(val)
    return grid


def find_starts(grid):
    starts = []
    for k, v in grid.items():
        if v == HEAD:
            starts.append(k)
    return starts


def track_paths(grid, trailhead):
    stack = []
    position = (trailhead)

    visited_ends = set()
    all_paths = 0

    stack.append(position)
    while stack:
        current = stack.pop()
        if grid[current] == END:
            visited_ends.add(current)
            all_paths += 1
            continue
        i, j = current
        for adjacent in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)):
            if adjacent in grid and grid[adjacent] == grid[current] + 1:
                stack.append(adjacent)
    return len(visited_ends), all_paths


TEST_DATA = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''

print(f'Day {DAY} of Advent of Code!')
print('Testing...')
grid = parse_grid(TEST_DATA)
print('Simple score:', sum(track_paths(grid, head)[0] for head in find_starts(grid)) == 36)
print('Proper score:', sum([track_paths(grid, head)[1] for head in find_starts(grid)]) == 81)
input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    grid = parse_grid(data)
    print('Simple score:', sum(track_paths(grid, head)[0] for head in find_starts(grid)))
    print('Proper score:', sum([track_paths(grid, head)[1] for head in find_starts(grid)]))
