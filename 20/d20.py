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
    relevant_walls = set()


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
            if neighbor in grid:
                if grid[neighbor] == WALL:
                    relevant_walls.add(neighbor)
                else:
                    neighbors.append(neighbor)

        for neighbor_coords in neighbors:
            if neighbor_coords in visited:
                continue

            
            old_cost = distances[neighbor_coords]
            new_cost = distances[current_vertex] + 1

            if new_cost < old_cost:
                heapq.heappush(pq, (new_cost, neighbor_coords))
                distances[neighbor_coords] = new_cost
    return distances, relevant_walls


def grid_dimensions(grid):
    w = max((i for i, j in grid.keys()))
    h = max((j for i, j in grid.keys()))
    return w, h

print(f'Day {DAY} of Advent of Code!')
print('Testing...')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()


def solve1_bad(data):
    grid, start, end = parse(data)
    w, h = grid_dimensions(grid)
    ways, relevant_walls = dijkstra(grid, start)
    init_result = ways[end]
    rel_walls = sorted([wall for wall in relevant_walls if 0 < wall[0] < h and 0 < wall[1] < w])

    cheat_results = 0

    print('Rel walls to check', len(relevant_walls))

    i = 1
    for wall in rel_walls:
        if i % 250 == 0: print('check', i/len(rel_walls)*100, 'for now', cheat_results)
        i += 1
        new_grid = grid.copy()
        new_grid[wall] = FLOOR
        ways, relevant_walls = dijkstra(new_grid, start)
        gain = init_result - ways[end]
        if gain >= 100:
            cheat_results += 1



    print(cheat_results)
