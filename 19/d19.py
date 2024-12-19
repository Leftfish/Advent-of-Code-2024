import os

from functools import cache

DAY = 19

TEST_DATA = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb'''
def parse(data):
    towels, patterns = data.split('\n\n')
    return frozenset(towels.split(', ')), patterns.splitlines()

@cache
def go(source, rest, target, towels):
    #print(f'Checking source={source}, rest={rest} to look for {target}')

    if not rest:
        #print('END', source, source == target)
        return source == target

    candidates = [] 
    for towel in towels:
        if rest.startswith(towel):
            new_source = source + towel
            new_rest = rest[len(towel):]
            candidates.append((new_source, new_rest))

    return any([go(new_source, new_rest, target, towels) for new_source, new_rest in candidates])

s = 0
towels, patterns = parse(TEST_DATA)
for target in patterns:
    #print('check', target, patterns)
    start = ''
    rest = target
    if go(start, target, target, towels):
        s += 1
print(s)


print(f'Day {DAY} of Advent of Code!')
print('Testing...')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()


s = 0
towels, patterns = parse(data)
for target in patterns:
    #print('check', target)
    start = ''
    rest = target
    if go(start, target, target, towels):
        s += 1
print(s)