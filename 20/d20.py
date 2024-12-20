import os

import heapq
from collections import defaultdict
DAY = 20

TEST_DATA = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############'''


START = 'S'
END = 'E'
WALL = '#'
FLOOR = '.'

UP, RIGHT, DOWN, LEFT = ((-1, 0), (0, 1), (1, 0), (0, -1))

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


def parse(data):
    grid = {}
    start = (-1, -1)
    end = (-1, -1)
    for i, row in enumerate(data.splitlines()):
        for j, c in enumerate(row):
            grid[(i, j)] = c
            if c == START:
                start = (i, j)
            elif c == END:
                end = (i, j)
    return grid, start, end


def dijkstra(grid, start):
    distances = {vertex: float('inf') for vertex in grid if grid[vertex] != WALL}
    distances[start] = 0
    visited = set()
    path = [start]
    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, (0, start))

    while pq:
        _, current_vertex = heapq.heappop(pq)
        visited.add(current_vertex)

        neighbors = []
        for direction in DIRECTIONS:
            i, j = current_vertex
            di, dj = direction
            neighbor = (i+di, j+dj)
            if neighbor in grid and grid[neighbor] != WALL:
                neighbors.append(neighbor)

        for neighbor_coords in neighbors:
            if neighbor_coords in visited:
                continue
            
            old_cost = distances[neighbor_coords]
            new_cost = distances[current_vertex] + 1

            if new_cost < old_cost:
                heapq.heappush(pq, (new_cost, neighbor_coords))
                distances[neighbor_coords] = new_cost
                path.append(neighbor_coords)
    return distances, path

def grid_dimensions(grid):
    w = max((i for i, j in grid.keys()))
    h = max((j for i, j in grid.keys()))
    return w, h


def manhattan(this, other):
    return abs(this[0] - other[0]) + abs(this[1] - other[1])

def look_around(grid, vertex, distance):
    i, j = vertex
    for di in range(i-distance-1, i+distance+1):
        for dj in range(j-distance-1, j+distance+1):
            if (di, dj) in grid and \
                grid[(di, dj)] != WALL and \
                    manhattan(vertex, (di, dj)) <= distance:
                yield (di, dj)

grid, start, end = parse(TEST_DATA)
from_start, path_from_start = dijkstra(grid, start)
from_end, path_from_end = dijkstra(grid, end)

best = from_start[end]

cheats = defaultdict(int)
hop_dist = 20
for point in path_from_start:
    for candidate_hop in look_around(grid, point, hop_dist):
        new_dist = from_start[point] + hop_dist + from_end[candidate_hop]
        delta = best - new_dist
        if delta >= 50:
            cheats[delta] += 1
print(cheats)

# dijkstra od startu
# dijkstra od mety
# leć po ścieżce od startu, sprawdzaj hopki o 2-20
# jeśli od startu do hopka i od mety do target-hopka jest mniej niż miało być = cheat
# jeśli cheat dostatecznie dobry - policz go





print(f'Day {DAY} of Advent of Code!')
print('Testing...')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()

grid, start, end = parse(data)
from_start, path_from_start = dijkstra(grid, start)
from_end, path_from_end = dijkstra(grid, end)

best = from_start[end]

cheats = defaultdict(int)
hop_dist = 2
for point in path_from_start:
    for candidate_hop in look_around(grid, point, hop_dist):
        new_dist = from_start[point] + hop_dist + from_end[candidate_hop]
        delta = best - new_dist
        if delta >= 100:
            cheats[delta] += 1
print(sum(cheats.values()))