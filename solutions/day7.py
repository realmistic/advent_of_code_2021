import numpy as np

text_file = open('inputs/day7/input.txt', 'r')

lines = text_file.read().splitlines()

numbers = [int(x) for x in lines[0].split(',')]

print(f'Input: {numbers}')
print(f'Max number: {np.max(numbers)}')


def get_alignment_fuel(to_number):
    rez = 0
    for elem in numbers:
        # rez += abs(to_number - elem) : Part1
        n = abs(to_number - elem)+1
        rez += n* (n-1) /2
    return rez


min_level = np.inf
min_i = np.inf
for i in range(np.max(numbers)):
    cur_level = get_alignment_fuel(i)
    if cur_level < min_level:
        min_level = cur_level
        min_i = i

print(f'Min number {min_i}; min level fuel: {min_level}')
