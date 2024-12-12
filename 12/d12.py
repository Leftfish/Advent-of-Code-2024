import os

from collections import defaultdict

DAY = 11


def parse(data):
    stones = defaultdict(int)
    for stone in data.split():
        stones[int(stone)] += 1
    return stones

def blink(stones):
    new_stones = defaultdict(int)

    for stone in stones:
        if stones[stone] > 0:
            if stone == 0:
                new_stones[1] += stones[0]
            elif len(str(stone)) % 2 == 0:
                split = len(str(stone)) // 2
                left = int(str(stone)[:split])
                right = int(str(stone)[split:])
                new_stones[left] += stones[stone]
                new_stones[right] += stones[stone]
            else:
                new = stone * 2024
                new_stones[new] += stones[stone]
    return new_stones

def sum_blinks(init_stones, steps):
    for _ in range(steps):
        init_stones = blink(init_stones)
    return sum(init_stones.values())


TEST_DATA = '125 17'

print(f'Day {DAY} of Advent of Code!')
print('Testing...')
print('After 25 steps:', sum_blinks(parse(TEST_DATA), 25) == 55312)
print('After 75 steps:', sum_blinks(parse(TEST_DATA), 75) == 65601038650482)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    print('After 25 steps:', sum_blinks(parse(data), 25))
    print('After 75 steps:', sum_blinks(parse(data), 75))
