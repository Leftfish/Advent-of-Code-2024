import os

DAY = 10

TEST_DATA = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''

HEAD = 0
END = 9

def parse_grid(data):
    grid = {}
    for i, row in enumerate(data.splitlines()):
        for j, val in enumerate(row):
            grid[(i, j)] = int(val)
    return grid

def find_starts(grid):
    starts = []
    for k, v in grid.items():
        if v == HEAD:
            starts.append(k)
    return starts



def find_paths(grid, trailhead):
    stack = []
    stack.append(trailhead)

    visited_ends = set()

    while stack:
        current = stack.pop()
        if grid[current] == END:
            visited_ends.add(current)
            continue
        i, j = current
        for adjacent in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)):
            if adjacent in grid and grid[adjacent] == grid[current] + 1:
                stack.append(adjacent)
    return len(visited_ends)

def simple_score(grid):
    return sum(find_paths(grid, head) for head in find_starts(grid))


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
print('Simple score:', simple_score(parse_grid(TEST_DATA)) == 36)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    print('Simple score:', simple_score(parse_grid(data)))