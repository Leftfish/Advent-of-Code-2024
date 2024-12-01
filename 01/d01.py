from collections import Counter

import os


def parse_data(data):
    left, right = [], []
    for line in data.splitlines():
        first, second = line.split()
        left.append(int(first))
        right.append(int(second))
    return sorted(left), sorted(right), Counter(right)


def sum_distances(left, right):
    return sum([abs(pair[0] - pair[1]) for pair in zip(left, right)])


def calculate_similarity(left, appearances):
    score = 0
    for num in left:
        if num in appearances:
            score += num * appearances[num]
    return score


DAY = 1
TEST_DATA = '''3   4
4   3
2   5
1   3
3   9
3   3'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
left, right, appearances = parse_data(TEST_DATA)
print('Sum of distances between lists:', sum_distances(left, right) == 11)
print('Similarity score:', calculate_similarity(left, appearances) == 31)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    left, right, appearances = parse_data(data)
    print('Sum of distances between lists:', sum_distances(left, right))
    print('Similarity score:', calculate_similarity(left, appearances))
