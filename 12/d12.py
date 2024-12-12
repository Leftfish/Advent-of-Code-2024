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

def simple_score(islands):
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

# posortuj tak, żeby zacząć od góry
# weź punkt, sprawdź czy po lewej jest poza gridem czy inny
# jeśli nie ma, jedź (patrząc o jeden w lewo) w dół
#   - jeśli trafiłeś na taki sam jak starter, skończ i dodaj bok
#   - jeśli trafiłeś na coś poza gridem albo innego, jedź dalej w dół i usuwaj te punkty z listy (to check)

def different(this, other, grid):
    if other not in grid or this not in grid:
        return True
    if grid[this] != grid[other]:
        return True
    return False

def get_sides(island, grid):
    left_borders = set()
    srtd = sorted(island)
    to_check = set(srtd)

    for current in srtd:
        i, j = current
        left = (i, j-1)
        if current not in to_check:
            continue
        if different(current, left, grid):
            #print(f'Start boku!', i, j)
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
                
    right_borders = set()
    srtd = sorted(island)
    to_check = set(srtd)

    for current in srtd:
        i, j = current
        right = (i, j+1)
        if current not in to_check:
            continue
        if different(current, right, grid):
            #print(f'Start boku!', i, j)
            while True:
                nxt_rgt = (i+1, j+1)
                nxt_bot = (i+1, j)
                if different(nxt_rgt, current, grid) and different(nxt_bot, current, grid):
                    #print('STOP - DIFF BOT LFT i BOT BOT', i, j)
                    right_borders.add(current)
                    break
                elif not different(nxt_rgt, current, grid) and not different(nxt_bot, current, grid):
                    #print('STOP - SAME BOT LFT i BOT BOT', i, j)
                    right_borders.add(current)
                    break
                else:
                    #print('removing', nxt_bot)
                    if nxt_bot in to_check:
                        to_check.remove(nxt_bot)
                i += 1

    top_borders = set()
    srtd = sorted(island, key=lambda x: x[1])
    to_check = set(srtd)


    for current in srtd:
        #print('check', current)
        i, j = current
        top = (i-1, j)
        if current not in to_check:
            continue
        if different(current, top, grid):
            #print(f'Start boku!', i, j)
            while True:
                nxt_top = (i-1, j+1)
                nxt_rgt = (i, j+1)
                if different(nxt_rgt, current, grid) and different(nxt_top, current, grid):
                    #print('STOP - DIFF TOP RGT i BOT BOT', i, j)
                    top_borders.add(current)
                    break
                elif not different(nxt_rgt, current, grid) and not different(nxt_top, current, grid):
                    #print('STOP - SAME TOP RGT i BOT BOT', i, j)
                    top_borders.add(current)
                    break
                else:
                    #print('removing', nxt_rgt)
                    if nxt_rgt in to_check:
                        to_check.remove(nxt_rgt)
                j += 1

    bot_borders = set()
    srtd = sorted(island, key=lambda x: x[1])#, reverse=True)
    to_check = set(srtd)
    #print(srtd)

    for current in srtd:
        #print('check', current)
        i, j = current
        bot = (i+1, j)
        if current not in to_check:
            continue
        if different(current, bot, grid):
            #print(f'Start boku!', i, j)
            while True:
                nxt_bot = (i+1, j+1)
                nxt_rgt = (i, j+1)
                if different(nxt_rgt, current, grid) and different(nxt_bot, current, grid):
                    #print('STOP - DIFF TOP RGT i BOT BOT', i, j)
                    bot_borders.add(current)
                    break
                elif not different(nxt_rgt, current, grid) and not different(nxt_bot, current, grid):
                    #print('STOP - SAME TOP RGT i BOT BOT', i, j)
                    bot_borders.add(current)
                    break
                else:
                    #print('removing', nxt_rgt)
                    if nxt_rgt in to_check:
                        to_check.remove(nxt_rgt)
                j += 1

    return len(left_borders) + len(right_borders) + len(bot_borders) + len(top_borders)


t = '''RRRRIICCFF
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


grid = parse_grid(data)
islands = []
checked = set()

for point in grid:
    if point not in checked:
        island = find_island(grid, point)
        for pt in island:
            checked.add(pt)
        islands.append(island)

s = 0
for i in islands:
    print(i)
    s += get_sides(i, grid) * len(i)

print(s)
