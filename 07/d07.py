import os

from operator import add, mul
from collections import deque

DAY = 7


TEST_DATA = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''

def parse_data(data):
    equations = []
    for line in data.splitlines():
        raw_result, raw_params = line.split(': ')
        result = int(raw_result)
        params = [int(p) for p in raw_params.split()]
        equations.append((result, params))
    return equations

def con(a, b):
    return int(str(a) + str(b))

def test_equation_two_ops(equation):
    expected, params = equation
    result, rest = params[0], deque(params[1:])
    Q = deque()
    Q.append((result, rest.copy(), add))
    Q.append((result, rest.copy(), mul))

    while Q:
        res, params, op = Q.popleft()
        if not params:
            if res == expected: 
                return expected

        next_param = params.popleft()
        res = op(res, next_param)        
        if res > expected:
            continue
        
        if params:
            Q.append((res, params.copy(), add))
            Q.append((res, params.copy(), mul))
        else:
            if res == expected: 
                return expected
    return 0

def test_equation_three_ops(equation):
    expected, params = equation
    result, rest = params[0], deque(params[1:])
    Q = deque()
    Q.append((result, rest.copy(), add))
    Q.append((result, rest.copy(), mul))
    Q.append((result, rest.copy(), con))

    while Q:
        res, params, op = Q.popleft()
        if not params:
            if res == expected: 
                return expected

        next_param = params.popleft()
        res = op(res, next_param)        
        if res > expected:
            continue
        
        if params:
            Q.append((res, params.copy(), add))
            Q.append((res, params.copy(), mul))
            Q.append((res, params.copy(), con))
        else:
            if res == expected: 
                return expected
    return 0


eq = parse_data(TEST_DATA)

s = 0
s2 = 0
for e in eq:
    s += test_equation_two_ops(e)
    s2 += test_equation_three_ops(e)

print(s, s2)


print(f'Day {DAY} of Advent of Code!')
print('Testing...')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()

eq = parse_data(data)
s = 0
for e in eq:
    s += test_equation(e)
print(s)
