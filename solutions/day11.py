import numpy as np


def one_step_change(matrix):
    flashed_matrix = np.zeros((len(matrix), len(matrix)))
    queue_to_flash = []
    matrix = matrix + 1  # all elems are +1
    # print(f'New Matrix: {matrix}')
    # add initial candidates to flash
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i, j] > 9 and flashed_matrix[i, j] == 0:
                queue_to_flash.append((i, j))
                flashed_matrix[i, j] = 1  # there will be a flash for this cell!

    while len(queue_to_flash) > 0:
        i, j = queue_to_flash.pop(0)
        # matrix[i, j] = 0

        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if (a == 0) and (b == 0):
                    continue
                if (i+a >= len(matrix)) or (j+b >= len(matrix[i])):
                    continue
                if (i+a < 0) or (j+b < 0):
                    continue
                try:
                    matrix[i + a, j + b] += 1
                    if matrix[i + a, j + b] > 9 and flashed_matrix[i + a, j + b] == 0:
                        queue_to_flash.append((i + a, j + b))
                        flashed_matrix[i + a, j + b] = 1
                except IndexError:
                    continue

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if flashed_matrix[i, j] != 0:
                matrix[i, j] = 0

    return np.sum(flashed_matrix), matrix


text_file = open('../inputs/day11/input.txt', 'r')
lines = text_file.read().splitlines()
energy_matrix = np.zeros((len(lines), len(lines[0])))

for i, line in enumerate(lines):
    energy_matrix[i] = list(line)

print(f' Initial state: \n {energy_matrix}')

total_flashes = 0
all_flashed_step = -1
for step in range(1000):
    print(f'----------------------')
    print(f' After {step + 1} steps:')
    flashes, energy_matrix = one_step_change(energy_matrix)
    total_flashes += flashes
    print(f' Flashes this step = {flashes}')
    print(f' Total Flashes = {total_flashes}')
    print(f' Energy matrix after: \n {energy_matrix}')
    if flashes == len(lines) * len(lines[0]) and all_flashed_step == -1: #store only the first all-flash
        all_flashed_step = step + 1

print(f'The first all-flesh step: {all_flashed_step}')
