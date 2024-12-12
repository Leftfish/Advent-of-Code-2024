import os

from collections import deque

DAY = 12


def parse_grid(data):
    grid = {}
    for i, row in enumerate(data.splitlines()):
        for j, c in enumerate(row):
            grid[(i, j)] = c
    return grid


def find_island(grid, start):
    visited = set()
    Q = deque([start])
    while Q:
        current = Q.popleft()
        
        if current in visited:
            continue
        else:
            visited.add(current)
        i, j = current
        val = grid[current]
        adjacents = [(i+1, j), (i-1, j), (i, j-1), (i, j+1)]
        x = 0
        for adj in adjacents:
            if adj in grid and grid[adj] == val and adj not in visited:
                Q.append(adj)
    return visited


def get_all_islands(grid):
    islands = []
    checked = set()

    for point in grid:
        if point not in checked:
            island = find_island(grid, point)
            for pt in island:
                checked.add(pt)
            islands.append(island)
    return islands


def calc_perimeter(island, grid):
    peri = 0
    for spot in island:
        i, j = spot
        adjacents = [(i+1, j), (i-1, j), (i, j-1), (i, j+1)]
        for adj in adjacents:
            if adj not in grid or grid[adj] != grid[spot]:
                peri += 1
    return peri


def count_sides(island, grid):
    def different(this, other, grid):
        if other not in grid or this not in grid:
            return True
        elif grid[this] != grid[other]:
            return True
        return False
    
    total = 0
    sorted_points = sorted(island)

    for d in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        borders = set()
        to_check = set(sorted_points)
        for current in sorted_points:
            i, j = current
            adj = (i + d[0], j + d[1])
            if current not in to_check:
                continue
            if different(current, adj, grid):
                while True:
                    di = 1 if not d[0] else 0
                    dj = 1 if not d[1] else 0
                    nxt_adj = (i+d[0]+di, j+d[1]+dj)
                    nxt_diag = (i+di, j + dj)
                    if (different(nxt_adj, current, grid) and \
                        different(nxt_diag, current, grid)) or \
                        (not different(nxt_adj, current, grid) and \
                        not different(nxt_diag, current, grid)):
                        borders.add(current)
                        break
                    else:
                        if nxt_diag in to_check:
                            to_check.remove(nxt_diag)
                    i += di
                    j += dj
        total += len(borders)
    return total


def get_price(islands, grid):
    simple_price = 0
    proper_price = 0
    for island in islands:
        area = len(island)
        peri = calc_perimeter(island, grid)
        sides = count_sides(island, grid)
        simple_price += area * peri
        proper_price += area * sides
    return simple_price, proper_price


TEST_DATA = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
grid = parse_grid(TEST_DATA)

simple_price, proper_price = get_price(get_all_islands(grid), grid)
print('Area * perimeter score:', simple_price == 1930)
print('Area * sides score:', proper_price == 1206)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    grid = parse_grid(data)
    simple_price, proper_price = get_price(get_all_islands(grid), grid)
    print('Area * perimeter score:', simple_price)
    print('Area * sides score:', proper_price)
