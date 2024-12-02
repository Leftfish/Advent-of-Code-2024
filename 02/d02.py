import os


def parse_data(data):
    return [[int(d) for d in line.split()] for line in data.splitlines()]


def check_safety(level, errors_allowed):
    increasing = None
    error_idx = None

    # find the index of the first error
    for i in range(len(level)-1):
        diff = level[i+1] - level[i]

        if increasing is None:
            increasing = diff > 0

        elif increasing and (diff > 3 or diff < 1) or \
            not increasing and (diff > -1 or diff < -3):
            error_idx = i
            break

    # if no errors, all good!
    if error_idx is None:
        return True

    # if dampener active: remove the number at index, index-1 and index+1, recheck
    if errors_allowed:
        updates = []
        for idx in (error_idx-1, error_idx, error_idx+1):
            if idx < 0 or idx > len(level)-1:
                continue
            new_level = level[::]
            new_level.pop(idx)
            updates.append(new_level)

        for updated_level in updates:
            if check_safety(updated_level, errors_allowed=False):
                return True

    return False


def check_levels(levels):
    safe = 0
    safe_dampened = 0

    for level in levels:
        if check_safety(level, False):
            safe += 1
        if check_safety(level, True):
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
safe, safe_damp = check_levels(parse_data(TEST_DATA))
print('Safe:', safe == 2, 'With dampener:', safe_damp == 4)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    safe, safe_damp = check_levels(parse_data(data))
    print('Safe:', safe, 'With dampener:', safe_damp)
