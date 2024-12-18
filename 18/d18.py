import os

import networkx as nx

DAY = 18


def parse_bytes(data):
    walls = []
    for pair in data.splitlines():
        j, i = pair.split(',')
        walls.append((int(i), int(j)))
    return walls


def make_grid(w, h, walls):
    grid = set()
    for i in range(w):
        for j in range(h):
            spot = (i, j)
            if spot not in walls:
                grid.add(spot)
    return grid


def check_grid(w, h, walls, wall_number):
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    grid = make_grid(w, h, walls[:wall_number])
    start = (0, 0)
    target = (w-1, h-1)

    G = nx.DiGraph()
    for spot in grid:
        G.add_node(spot)

    for node in G.nodes:
        i, j = node
        for dx in directions:
            di, dj = dx
            neighbor = (i+di, j+dj)
            if neighbor in G:
                G.add_edge(node, neighbor)

    return len(nx.shortest_path(G, start, target)) - 1


def binary_search(w, h, walls, start):
    low = start
    high = len(walls)
    best = []

    while low <= high:
        mid = (low + high) // 2
        try:
            check_grid(w, h, walls, mid)
            low = mid + 1
        except nx.NetworkXNoPath:
            best.append(mid)
            high = mid - 1

    blockade = walls[min(best)-1]
    return f'{blockade[1]},{blockade[0]}'

TEST_DATA = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0'''

print(f'Day {DAY} of Advent of Code!')
print('Testing...')
walls = parse_bytes(TEST_DATA)
w, h = 7, 7
start = 12
print(f'Shortest path after {start} bytes:', check_grid(w, h, walls, start) == 22)
print('First blockade:', binary_search(w, h, walls, start) == '6,1')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    walls = parse_bytes(data)
    w, h, = 71, 71
    start = 1024
    print(f'Shortest path after {start} bytes:', check_grid(w, h, walls, start))
    print('First blockade:', binary_search(w, h, walls, start))
