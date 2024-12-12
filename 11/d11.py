import os

from collections import deque

DAY = 12

'''
zrób grid
znajdź punkt
sprawdź czy jest już w jakiejś zrobionej wyspie
jeśli nie:
zacznij od niego i BFS:
    - dodaj do visited
    - pole += 1
    - poszukaj adjacent
    - border += 4
    - za każdy adjacent który jest w grid i tej samej kategorii border -= 1
    - jeśli adjacent nie jest visited: zakolejkuj go
'''

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
                #print(f'cur {current}, appended {adj}')
                Q.append(adj)
        #print('---')
    return visited
    
def calc_perimeter(island, grid):
    peri = 0
    for spot in island:
        i, j = spot
        adjacents = [(i+1, j), (i-1, j), (i, j-1), (i, j+1)]
        for adj in adjacents:
            if adj not in grid or grid[adj] != grid[spot]:
                peri += 1
    return peri

def simple_score(grid):
    checked = set()
    score = 0
    for point in grid:
        if point not in checked:
            island = find_island(grid, point)
            area = len(island)
            peri = calc_perimeter(island, grid)
            for pt in island:
                checked.add(pt)
            score += area * peri
    return score


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
print('Area * perimeter score:', simple_score(grid) == 1930)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    grid = parse_grid(data)
    print('Area * perimeter score:', simple_score(grid))