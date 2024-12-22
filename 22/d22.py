import os

DAY = 22

TEST_DATA = '''1
10
100
2024'''


def make_secret(secret):
    result = secret << 6
    new_secret = secret ^ result
    secret = new_secret & (16777216 - 1)
    result = secret >> 5
    new_secret = secret ^ result
    secret = new_secret & (16777216 - 1)
    result = secret << 11
    new_secret = secret ^ result
    secret = new_secret & (16777216 - 1)
    return secret

def parse(data):
    return [int(d) for d in data.splitlines()]

def get_2000(numbers):
    score = 0
    for secret in numbers:
        for _ in range(2000):
            new_secret = make_secret(secret)
            secret = new_secret
        score += secret
    return(score)
    
numbers = parse(TEST_DATA)
print(get_2000(numbers))

print(f'Day {DAY} of Advent of Code!')
print('Testing...')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()

numbers = parse(data)
print(get_2000(numbers))