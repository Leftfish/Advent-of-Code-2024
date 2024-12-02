import os


def parse_data(data):
    levels = []
    for line in data.splitlines():
        level = [int(d) for d in line.split()]
        levels.append(level)
    return levels


def check_safety(level):
    diffs = [level[i+1] - level[i] for i in range(len(level)-1)]

    abs_check = all([3 >= abs(d) >= 1 for d in diffs])
    sign_check = all([d > 0 for d in diffs]) or all([d < 0 for d in diffs])

    return abs_check and sign_check


def check_safety_dampener(level):
    i = 0
    increasing = None
    candidate = None

    # find the index of the first error
    while i < len(level)-1:
        diff = level[i+1] - level[i]

        if increasing is None:
            increasing = diff > 0

        if increasing and (diff > 3 or diff < 1) or \
            not increasing and (diff > -1 or diff < -3):
            candidate = i
            break

        i += 1

    # if no errors, all good!
    if candidate is None:
        return True

    # remove the number at index, index-1 and index+1, recheck
    else:
        updates = []
        for idx in (candidate-1, candidate, candidate+1):
            if idx < 0 or idx > len(level)-1:
                continue
            new_level = level[::]
            new_level.pop(idx)
            updates.append(new_level)

        for updated_level in updates:
            if check_safety(updated_level):
                return True

    return False


def check_levels(levels):
    safe = 0
    safe_dampened = 0
    
    for level in levels:
        if check_safety(level):
            safe += 1
        if check_safety_dampener(level):
            safe_dampened += 1

    return safe, safe_dampened


DAY = 2
TEST_DATA = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
levels = parse_data(TEST_DATA)
safe, safe_damp = check_levels(levels)
print('Safe:', safe == 2, 'With dampener:', safe_damp == 4)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    levels = parse_data(data)
    safe, safe_damp = check_levels(levels)
    print('Safe:', safe, 'With dampener:', safe_damp)
