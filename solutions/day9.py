import numpy as np

text_file = open('../inputs/day9/input.txt', 'r')

lines = text_file.read().splitlines()

heights_matrix = np.zeros((len(lines), len(lines[0])))

for i, line in enumerate(lines):
    heights_matrix[i] = list(line)


def is_min(matrix, row, col):
    if row > 0:
        if matrix[row, col] >= matrix[row - 1, col]:
            return False
    if row < matrix.shape[0] - 1:
        if matrix[row, col] >= matrix[row + 1, col]:
            return False
    if col > 0:
        if matrix[row, col] >= matrix[row, col - 1]:
            return False
    if col < matrix.shape[1] - 1:
        if matrix[row, col] >= matrix[row, col + 1]:
            return False
    return True


def get_basin_matrix(matrix, row, col):
    coloured = np.zeros(matrix.shape)
    coloured[row, col] = 1

    queue = [(row, col)]

    while len(queue) > 0:
        cur_row, cur_col = queue.pop(0)
        if cur_row > 0 and coloured[cur_row - 1, cur_col] == 0 and matrix[cur_row - 1, cur_col] < 9:
            queue.append((cur_row - 1, cur_col))
            coloured[cur_row - 1, cur_col] = 1

        if cur_row < matrix.shape[0] - 1 and coloured[cur_row + 1, cur_col] == 0 and matrix[cur_row + 1, cur_col] < 9:
            queue.append((cur_row + 1, cur_col))
            coloured[cur_row + 1, cur_col] = 1

        if cur_col > 0 and coloured[cur_row, cur_col - 1] == 0 and matrix[cur_row, cur_col - 1] < 9:
            queue.append((cur_row, cur_col - 1))
            coloured[cur_row, cur_col - 1] = 1

        if cur_col < matrix.shape[1] - 1 and coloured[cur_row, cur_col + 1] == 0 and matrix[cur_row, cur_col + 1] < 9:
            queue.append((cur_row, cur_col + 1))
            coloured[cur_row, cur_col + 1] = 1

    return coloured


mins = []
array_basins_size = []

for i in range(len(heights_matrix)):
    for j in range(len(heights_matrix[i])):
        if is_min(heights_matrix, i, j):
            mins.append(heights_matrix[i, j] + 1)
            array_basins_size.append(np.sum(get_basin_matrix(heights_matrix, i, j)))

array_basins_size.sort()

print(f' All min points: {mins}')
print(f' Part1 answer:"What is the sum of the risk levels of all low points on your heightmap?: {np.sum(mins)}')

# DEBUG: print(f'Get full basin coloured: {get_basin_matrix(heights_matrix, 2, 2)}')
# DEBUG: print(f'Number of cells in basin: {np.sum(get_basin_matrix(heights_matrix, 2, 2))}')
print(f'Sorted array of basin sizes: {array_basins_size}')
print(f' Part2 ans: "What do you get if you multiply together the sizes of the three largest basins":{array_basins_size[-1] * array_basins_size[-2] * array_basins_size[-3]}')
# print(f'Sorted array of basin sizes: {sorted(array_basins_size)[-2:0]}')