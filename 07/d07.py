import os

from operator import add, mul
from collections import deque # used only in the inefficient version

DAY = 7


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


''' FIRST ATTEMPT - INEFFICIENT
def test_equation(equation, ops):
    expected, params = equation
    result, rest = params[0], deque(params[1:])
    Q = deque()
    for op in ops:
        Q.append((result, rest.copy(), op))

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
            for op in ops:
                Q.append((res, params.copy(), op))
        else:
            if res == expected:
                return expected
    return 0
'''


def test_equation(exp, res, params, part):
    if res > exp:
        return False
    if not params:
        return res == exp
    if part == 1:
        return test_equation(exp, mul(res, params[0]), params.copy()[1:], part=1) or \
                test_equation(exp, add(res, params[0]), params.copy()[1:], part=1)
    elif part == 2:
        return test_equation(exp, mul(res, params[0]), params.copy()[1:], part=2) or \
                test_equation(exp, add(res, params[0]), params.copy()[1:], part=2) or \
                test_equation(exp, con(res, params[0]), params.copy()[1:], part=2)


def test_all_equations(equations):
    two_ops = 0
    three_ops = 0
    for equation in equations:
        exp, params = equation
        res = params.pop(0)
        if test_equation(exp, res, params, part=1):
            two_ops += exp
        if test_equation(exp, res, params, part=2):
            three_ops += exp
    return two_ops, three_ops


TEST_DATA = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
equations = parse_data(TEST_DATA)
two_ops, three_ops = test_all_equations(equations)
print(f'Two ops: {two_ops == 3749}. Three ops: {three_ops == 11387}.')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    equations = parse_data(data)
    two_ops, three_ops = test_all_equations(equations)
    print(f'Two ops: {two_ops}. Three ops: {three_ops}.')
