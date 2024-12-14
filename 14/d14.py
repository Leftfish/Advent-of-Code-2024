import os

import re

DAY = 14


def parse(data):
    regex = r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'
    robots = []

    for line in data.splitlines():
        x, y, dx, dy = (int(d) for d in re.findall(regex, line)[0])
        robot = ((x, y), (dx, dy))
        robots.append(robot)

    return robots


def move_robot(robot, steps, w, h):
    x, y = robot[0]
    dx, dy = robot[1]
    new_x = (x + dx * steps) % w
    new_y = (y + dy * steps) % h
    return (new_x, new_y)


def calculate_safety(robots, seconds, w, h):
    mid_w = w // 2
    mid_h = h // 2
    q1, q2, q3, q4 = 0, 0, 0, 0

    for robot in robots:
        x, y = move_robot(robot, seconds, w, h)
        if x in range(0,mid_w) and y in range(0,mid_h):
            q1 += 1
        elif x in range(0,mid_w) and y in range(mid_h+1, h):
            q2 += 1
        elif x in range(mid_w+1, w) and y in range(0, mid_h):
            q3 += 1
        elif x in range(mid_w+1, w) and y in range(mid_h+1, h):
            q4 += 1

    return q1*q2*q3*q4


def update_robots(robots, w, h, second):
    new_robots = []

    for robot in robots:
        dx, dy = robot[1]
        x, y = move_robot(robot, second, w, h)
        new_robot = ((x, y), (dx, dy))
        new_robots.append(new_robot)

    return new_robots


def find_tree(robots, w, h, search_term):
    sec = 0

    while True:
        current_robots = update_robots(robots, w, h, sec)
        picture = [['.' for x in range(w)] for y in range(h)]
        for robot in current_robots:
            x, y = robot[0]
            picture[y][x] = '#'
        for line in picture:
            if search_term in ''.join(line):
                for line in picture:
                    print(''.join(line))
                return sec
        sec += 1


TEST_DATA = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
w, h = 11, 7
robots = parse(TEST_DATA)
print('Safety factor:', calculate_safety(robots, 100, w, h) == 12)


input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    w, h = 101, 103
    robots = parse(data)
    print('Safety factor:', calculate_safety(parse(data), 100, w, h))
    print('Tree after:', find_tree(robots, w, h, '########'))
