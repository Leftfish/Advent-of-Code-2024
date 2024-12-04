import os

import re
import numpy as np


DAY = 4

def parse_data(data):
    return np.array([list(row) for row in data.splitlines()])


def xmas_rows_and_diagonals(letters):
    xmas = 0
    size = len(letters)

    for row in letters:
        simple = re.findall('XMAS', ''.join(row))
        rev = re.findall('XMAS', ''.join(row)[::-1])
        xmas += len(simple) + len(rev)

    for i in range(-size+1, size, 1):
        diagonal = letters.diagonal(i)
        simple = re.findall('XMAS', ''.join(diagonal))
        rev = re.findall('XMAS', ''.join(diagonal)[::-1])
        xmas += len(simple) + len(rev)

    return xmas


def check_x_mas(letters, i, j):
    '''
    1.  2.  3.   4.
    M.M S.S M.S. S.M
    .A. .A. .A.  .A.
    S.S M.M M.S  S.M.
    '''

    if i <= 0 or j <= 0 or i >= len(letters[0])-1 or j >= len(letters)-1:
        return False

    top_left = letters[i-1][j-1]
    top_right = letters[i-1][j+1]
    bot_left = letters[i+1][j-1]
    bot_right = letters[i+1][j+1]

    if top_left == 'M' and top_right == 'M' and bot_left == 'S' and bot_right == 'S':
        return True

    elif top_left == 'S' and top_right == 'S' and bot_left == 'M' and bot_right == 'M':
        return True

    elif top_left == 'M' and top_right == 'S' and bot_left == 'M' and bot_right == 'S':
        return True

    elif top_left == 'S' and top_right == 'M' and bot_left == 'S' and bot_right == 'M':
        return True

    return False


def count_x_mas(letters):
    x_mas = 0
    for i, row in enumerate(letters):
        for j, letter in enumerate(row):
            if letter == 'A':
                x_mas += check_x_mas(letters, i, j)
    return x_mas


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

print(f'Day {DAY} of Advent of Code!')
print('Testing...')
l = parse_data(TEST_DATA)
print('XMAS:', xmas_rows_and_diagonals(l) + xmas_rows_and_diagonals(np.rot90(l)) == 18)
print('X-MAS:', count_x_mas(l) == 9)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    l = parse_data(inp.read())
    print('XMAS:', xmas_rows_and_diagonals(l) + xmas_rows_and_diagonals(np.rot90(l)))
    print('X-MAS:', count_x_mas(l))
