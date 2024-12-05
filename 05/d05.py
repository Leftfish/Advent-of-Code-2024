import os

from collections import defaultdict
from functools import cmp_to_key

DAY = 5


def parse_data(data):
    raw_rules, raw_pages = data.split('\n\n')

    rules = defaultdict(set)
    pages = []
    for line in raw_rules.splitlines():
        before, after = line.split('|')
        rules[int(after)].add(int(before))

    for line in raw_pages.splitlines():
        page = [int(d) for d in line.split(',')]
        pages.append(page)

    return rules, pages


def test_page(page, rules):
    for i in range(len(page)):
        current, rest = page[i], page[i+1:]
        if bool(set(rest) & rules[current]):
            return False
    return True


def sum_mid(pages, rules):
    s = 0
    for page in pages:
        if test_page(page, rules):
            s += page[len(page)//2]
    return s


def sum_mid_wrong(pages, rules):
    def comparator(a, b):
        if b in rules[a]:
            return 1
        elif a in rules[b]:
            return -1
        else:
            return 0

    s = 0
    for page in pages:
        if not test_page(page, rules):
            arranged = sorted(page, key=cmp_to_key(comparator))
            s += arranged[len(arranged)//2]

    return s


TEST_DATA = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47'''

print(f'Day {DAY} of Advent of Code!')
print('Testing...')
rules, pages = parse_data(TEST_DATA)
print('Sum of mid pages in proper:', sum_mid(pages, rules) == 143)
print('Sum of mid pages in rearranged:', sum_mid_wrong(pages, rules) == 123)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    rules, pages = parse_data(inp.read())
    print('Sum of mid pages in proper:', sum_mid(pages, rules))
    print('Sum of mid pages in rearranged:', sum_mid_wrong(pages, rules))
