import os

from collections import deque, defaultdict

DAY = 22


def parse(data):
    return [int(d) for d in data.splitlines()]


def make_secret(secret):
    prune_number = 16777216

    result = secret << 6
    new_secret = secret ^ result
    secret = new_secret & (prune_number - 1)

    result = secret >> 5
    new_secret = secret ^ result
    secret = new_secret & (prune_number - 1)

    result = secret << 11
    new_secret = secret ^ result
    secret = new_secret & (prune_number - 1)

    return secret


def get_2000(numbers, iters):
    sequences = defaultdict(int)
    score = 0

    for secret in numbers:
        sequence = deque([])
        price = secret % 10
        visited = set()
        for _ in range(iters):
            new_secret = make_secret(secret)
            new_price = new_secret % 10
            sequence.append(new_price - price)
            if len(sequence) > 4:
                sequence.popleft()
                seq_to_store = tuple(sequence)
                if seq_to_store not in visited:
                    sequences[seq_to_store] += new_price
                    visited.add(seq_to_store)
            secret = new_secret
            price = new_price
        score += secret

    return score, max(sequences.values())


TEST_DATA = '''1
2
3
2024'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
numbers = parse(TEST_DATA)
sum_of_secrets, price_for_sequence = get_2000(numbers, 2000)
print('Sum of 2000th secret number:', sum_of_secrets == 37990510)
print('Best price:', price_for_sequence == 23)


input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    numbers = parse(data)
    sum_of_secrets, price_for_sequence = get_2000(numbers, 2000)
    print('Sum of 2000th secret number:', sum_of_secrets)
    print('Best price:', price_for_sequence)
