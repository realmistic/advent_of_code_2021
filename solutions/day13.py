import numpy as np
from copy import copy, deepcopy

text_file = open('../inputs/day13/input.txt', 'r')
lines = text_file.read().splitlines()


def make_matrix_from_points(point_arr):
    points_st = [x[0] for x in point_arr]
    points_en = [x[1] for x in point_arr]

    matrix_new = np.zeros((np.max(points_st) + 1, np.max(points_en) + 1))
    for i in range(len(points_st)):
        matrix_new[points_st[i], points_en[i]] = 1
    return matrix_new


# noinspection PyShadowingNames
def print_matrix(matrix):
    print('----------------------')
    print(f'Matrix dims: {matrix.shape}')
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i, j] == 1:
                print('#', end='')
            else:
                print('.', end='')
        print('')


points_start = []
points_end = []
points = set()

for line in lines:
    if line.count(',') == 0:
        break
    coord_x = int(line.split(',')[0])
    coord_y = int(line.split(',')[1])

    points_start.append(coord_x)
    points_end.append(coord_y)
    points.add((coord_x, coord_y))

# we found the size of the matrix and the number of points
print(f'Number of input points: {len(points_start)}')
print(f'Max value of x coord: {np.max(points_start)}')
print(f'Max value of y coord: {np.max(points_end)}')

fold = []

for line in lines:
    splitted = line.split(' ')
    if len(splitted) > 0 and splitted[0] == 'fold':
        fold_axis = splitted[2].split('=')[0]
        fold_line = int(splitted[2].split('=')[1])
        fold.append((fold_axis, fold_line))

print(f'Fold along these axis and lines: {fold}')
print('---------------------------------------')

def intelligent_folding(points_array, fold_command):
    new_points_arr = deepcopy(points_array)
    fold_axis = fold_command[0]
    fold_point = fold_command[1]

    for point in points_array:
        c_x = 0
        c_y = 0

        if fold_axis == 'x':
            if point[0] > fold_point:
                c_x = 2 * fold_point - point[0]
                new_points_arr.remove(point)
            else:
                c_x = point[0]
            c_y = point[1]
        if fold_axis == 'y':
            if point[1] > fold_point:
                c_y = 2 * fold_point - point[1]
                new_points_arr.remove(point)
            else:
                c_y = point[1]
            c_x = point[0]

        new_points_arr.add((c_x, c_y))

    return new_points_arr


print('=======================================')
cur_points = points
for fold_step in fold:
    print(f'command: {fold_step}')
    print(f' Original points arr: {len(cur_points)}')
    cur_points = intelligent_folding(cur_points, fold_step)
    print(f' New points arr: {len(cur_points)}')
    print('------------------------------------')


m = make_matrix_from_points(cur_points)

print('Part1 ans: len(<New points Arr>) after folding command 1')
print('Part 2 ans : code')
print_matrix(m.T)

