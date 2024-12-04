import os

import numpy as np
import re

DAY = 4
TEST_DATA = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''

def parse_data(data):
    letters = []
    for row in data.splitlines():
        letters.append(list(row))
    return np.array(letters)



def rows_and_diagonals(letters):
    xmas = 0
    size = len(letters)

    for row in letters:        
        simple = re.findall('XMAS', ''.join(row))
        rev = re.findall('XMAS', ''.join(row)[::-1])
        xmas += len(simple)
        xmas += len(rev)

    for i in range(-size+1, size, 1):
        diagonal = letters.diagonal(i)
        simple = re.findall('XMAS', ''.join(diagonal))
        rev = re.findall('XMAS', ''.join(diagonal)[::-1])
        xmas += len(simple)
        xmas += len(rev)
    
    return xmas




print(f'Day {DAY} of Advent of Code!')
print('Testing...')
l = parse_data(TEST_DATA)
print('XMAS:', rows_and_diagonals(l) + rows_and_diagonals(np.rot90(l)) == 18)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    l = parse_data(data)
    print('XMAS:', rows_and_diagonals(l) + rows_and_diagonals(np.rot90(l)))