import numpy as np

text_file = open('../inputs/day9/input.txt', 'r')

lines = text_file.read().splitlines()

heights_matrix = np.zeros((len(lines[0]), len(lines[0])))

for i, line in enumerate(lines):
    heights_matrix[i] = list(line)


def is_min(matrix, row, col):
    if row > 0:
        if matrix[row, col] >= matrix[row - 1, col]:
            return False

    if row < len(matrix[0]) - 1:
        if matrix[row, col] >= matrix[row + 1, col]:
            return False

    if col > 0:
        if matrix[row, col] >= matrix[row, col - 1]:
            return False

    if col < len(matrix[0]) - 1:
        if matrix[row, col] >= matrix[row, col + 1]:
            return False
    return True


mins = []

for i in range(len(heights_matrix)):
    for j in range(len(heights_matrix[i])):
        if is_min(heights_matrix, i, j):
            mins.append(heights_matrix[i, j] +1)

print(mins)

print(np.sum(mins))
