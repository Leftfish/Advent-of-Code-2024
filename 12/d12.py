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

def get_price(islands, grid):
    simple_price = 0
    proper_price = 0
    for island in islands:
        area = len(island)
        peri = calc_perimeter(island, grid)
        sides = get_sides(island, grid)
        simple_price += area * peri
        proper_price += area * sides
    return simple_price, proper_price


def get_sides(island, grid):
    def different(this, other, grid):
        if other not in grid or this not in grid:
            return True
        if grid[this] != grid[other]:
            return True
        return False

    left_borders = set()
    top_borders = set()
    bot_borders = set()
    right_borders = set()
    srtd = sorted(island)

    to_check = set(srtd)
    for current in srtd:
        i, j = current
        left = (i, j-1)
        if current not in to_check:
            continue
        if different(current, left, grid):
            while True:
                nxt_left = (i+1, j-1)
                nxt_bot = (i+1, j)
                if different(nxt_left, current, grid) and different(nxt_bot, current, grid):
                    left_borders.add(current)
                    break
                elif not different(nxt_left, current, grid) and not different(nxt_bot, current, grid):
                    left_borders.add(current)
                    break
                else:
                    if nxt_bot in to_check:
                        to_check.remove(nxt_bot)
                i += 1
                
    
    to_check = set(srtd)
    for current in srtd:
        i, j = current
        right = (i, j+1)
        if current not in to_check:
            continue
        if different(current, right, grid):
            while True:
                nxt_rgt = (i+1, j+1)
                nxt_bot = (i+1, j)
                if different(nxt_rgt, current, grid) and different(nxt_bot, current, grid):
                    right_borders.add(current)
                    break
                elif not different(nxt_rgt, current, grid) and not different(nxt_bot, current, grid):
                    right_borders.add(current)
                    break
                else:
                    if nxt_bot in to_check:
                        to_check.remove(nxt_bot)
                i += 1

    
    to_check = set(srtd)
    for current in srtd:
        i, j = current
        top = (i-1, j)
        if current not in to_check:
            continue
        if different(current, top, grid):
            while True:
                nxt_top = (i-1, j+1)
                nxt_rgt = (i, j+1)
                if different(nxt_rgt, current, grid) and different(nxt_top, current, grid):
                    top_borders.add(current)
                    break
                elif not different(nxt_rgt, current, grid) and not different(nxt_top, current, grid):
                    top_borders.add(current)
                    break
                else:
                    if nxt_rgt in to_check:
                        to_check.remove(nxt_rgt)
                j += 1

    to_check = set(srtd)
    for current in srtd:
        i, j = current
        bot = (i+1, j)
        if current not in to_check:
            continue
        if different(current, bot, grid):
            while True:
                nxt_bot = (i+1, j+1)
                nxt_rgt = (i, j+1)
                if different(nxt_rgt, current, grid) and different(nxt_bot, current, grid):
                    bot_borders.add(current)
                    break
                elif not different(nxt_rgt, current, grid) and not different(nxt_bot, current, grid):
                    bot_borders.add(current)
                    break
                else:
                    if nxt_rgt in to_check:
                        to_check.remove(nxt_rgt)
                j += 1

    return len(left_borders) + len(right_borders) + len(bot_borders) + len(top_borders)


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