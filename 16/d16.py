import os

import heapq
from itertools import cycle

DAY = 16

TEST_DATA = '''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############'''

TEST_DATA = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################'''

START = 'S'
END = 'E'
WALL = '#'
FLOOR = '.'

WALK_COST = 1
TURN_COST = 1000

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

    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, (0, start, RIGHT))

    while pq:
        _, current_vertex, current_direction = heapq.heappop(pq)
        visited.add(current_vertex)

        neighbors = []
        for direction in DIRECTIONS:
            i, j = current_vertex
            di, dj = direction
            neighbor = ((i+di, j+dj), direction)
            if grid[neighbor[0]] != WALL:
                neighbors.append(neighbor)

        for neighbor in neighbors:
            neighbor_coords, neighbor_direction = neighbor
            if neighbor_direction != current_direction:
                distance = TURN_COST + WALK_COST
            else:
                distance = WALK_COST
            if neighbor_coords not in visited:
                old_cost = distances[neighbor_coords]
                new_cost = distances[current_vertex] + distance
                if new_cost < old_cost:
                    heapq.heappush(pq, (new_cost, neighbor_coords, neighbor_direction))
                    distances[neighbor_coords] = new_cost
    return distances


grid, start, end = parse(TEST_DATA)


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
print('Shortest path:', dijkstra(grid, start)[end] == 11048)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    grid, start, end = parse(data)
    print('Shortest path:', dijkstra(grid, start)[end])