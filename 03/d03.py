import os

import re
from operator import mul

def sum_multiples(memory):
    regex = r'mul\((\d{1,3}),(\d{1,3})\)'
    groups = re.findall(regex, memory)
    s = 0
    for group in groups:
        s += mul(int(group[0]), int(group[1]))
    return s


def sum_multiples_with_flags(memory):
    def remove_empty(group):
        new = []
        for element in group:
            if element:
                new.append(element)
        return new

    s = 0

    regex = r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))"
    groups = re.findall(regex, memory)
    execute_op = True
    for group in groups:
        params = remove_empty(group)
        if params[0] == "don't()":
            execute_op = False
        elif params[0] == "do()":
            execute_op = True
        else:
            if execute_op:
                s += mul(int(group[0]), int(group[1]))
    return s


DAY = 3
TEST_DATA = '''xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'''
TEST_DATA_2 = '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5)'''

print(f'Day {DAY} of Advent of Code!')
print('Testing...')
print('Uncorrupted multiplications:', sum_multiples(TEST_DATA) == 161)
print('Uncorrupted multiplications with flags:', sum_multiples_with_flags(TEST_DATA_2) == 48)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    print('Uncorrupted multiplications:', sum_multiples(data))
    print('Uncorrupted multiplications with flags:', sum_multiples_with_flags(data))
