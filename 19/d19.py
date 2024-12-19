import os

from functools import cache

DAY = 19


def parse(data: str) -> tuple[frozenset, list[str]]:
    patterns, towels = data.split('\n\n')
    return frozenset(patterns.split(', ')), towels.splitlines()


@cache
def make_towels(source: str, rest: str, target: str, patterns: frozenset[str]):
    if not rest:
        return 1 if source == target else 0

    total = 0

    for pattern in patterns:
        if rest.startswith(pattern):
            total += make_towels(source + pattern, \
                                 rest[len(pattern):], target, patterns)

    return total


def make_all_towels(patterns: frozenset, towels: list):
    possible, ways = 0, 0
    for towel in towels:
        result = make_towels('', towel, towel, patterns)
        if result:
            possible += 1
            ways += result
    return possible, ways


TEST_DATA = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
possible, ways = make_all_towels(*parse(TEST_DATA))
print(f'Possible designs:', possible == 6, 'Available ways:', ways == 16)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    possible, ways = make_all_towels(*parse(data))
    print(f'Possible designs:', possible, 'Available ways:', ways)
