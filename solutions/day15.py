import numpy as np


def read_stats():
    text_file = open('../inputs/day15/input.txt', 'r')
    lines = text_file.read().splitlines()
    matrix = np.zeros((len(lines), len(lines[0])))

    for i, line in enumerate(lines):
        matrix[i] = list(line)

    return matrix


def calc_risk_level_matrix(input_matrix_):
    risk_level_ = np.zeros(input_matrix_.shape)

    for i in range(len(input_matrix_)):
        for j in range(len(input_matrix_[i])):
            if i == 0 and j == 0:
                risk_level_[i, j] = 0
            if i == 0 and j > 0:
                risk_level_[i, j] = risk_level_[i, j - 1] + input_matrix_[i, j]
            if j == 0 and i > 0:
                risk_level_[i, j] = risk_level_[i - 1, j] + input_matrix_[i, j]
            if i > 0 and j > 0:
                risk_level_[i, j] = min(risk_level_[i - 1, j], risk_level_[i, j - 1]) + input_matrix_[i, j]
    return risk_level_


input_matrix = read_stats()
print(input_matrix)
print(input_matrix.shape)
risk_level = calc_risk_level_matrix(input_matrix)

print(f'Part 1 (risk level map): {risk_level}')


# --------------------- Part2 ------------------------

def make_larger_matrix(matrix):
    matrix2 = matrix + 1
    for i in range(len(matrix2)):
        for j in range(len(matrix2[i])):
            if matrix2[i, j] > 9:
                matrix2[i, j] = 1
    return matrix2


def widen_matrix_down(full_matrix, cur_matrix_part_):
    new_full_matrix = np.zeros((full_matrix.shape[0] + cur_matrix_part_.shape[0], full_matrix.shape[1]))
    larger_matrix = make_larger_matrix(cur_matrix_part_)
    for i in range(len(full_matrix)):
        for j in range(len(full_matrix[i])):
            new_full_matrix[i, j] = full_matrix[i, j]

    for i in range(len(larger_matrix)):
        for j in range(len(larger_matrix[i])):
            new_full_matrix[len(full_matrix) + i, j] = larger_matrix[i, j]

    return new_full_matrix


def widen_matrix_right(full_matrix, cur_matrix_part_):
    new_full_matrix = np.zeros((full_matrix.shape[0], full_matrix.shape[1] + cur_matrix_part_.shape[1]))
    larger_matrix = make_larger_matrix(cur_matrix_part_)
    for i in range(len(full_matrix)):
        for j in range(len(full_matrix[i])):
            new_full_matrix[i, j] = full_matrix[i, j]

    for i in range(len(larger_matrix)):
        for j in range(len(larger_matrix[i])):
            new_full_matrix[i, len(full_matrix[i]) + j] = larger_matrix[i, j]

    return new_full_matrix


print('----------- Part2 -------------')
# print(input_matrix)
# print('=====')
# print(make_larger_matrix(input_matrix))
# print('=====')
# w = widen_matrix_down(input_matrix, input_matrix)
# print(w)
# print(input_matrix.shape)
# print(w.shape)
# print('=====')
# r = widen_matrix_right(input_matrix, input_matrix)
# print(r)
# print(r.shape)
# print('-!----@------@-----')

# 4 times going to the right
cur_matrix_part = input_matrix
cur_wide_matrix = input_matrix
for step_widen_right in range(4):
    cur_wide_matrix = widen_matrix_right(cur_wide_matrix, cur_matrix_part)
    cur_matrix_part = make_larger_matrix(cur_matrix_part)

#
# print(cur_wide_matrix)
# print(cur_wide_matrix.shape)


# 4 times going to the bottom
cur_long_matrix = cur_wide_matrix
cur_matrix_part = cur_wide_matrix

for step_longing_down in range(4):
    cur_long_matrix = widen_matrix_down(cur_long_matrix, cur_matrix_part)
    cur_matrix_part = make_larger_matrix(cur_matrix_part)

print(cur_long_matrix)
print(cur_long_matrix.shape)

risk_level_widelong = calc_risk_level_matrix(cur_long_matrix)

np.set_printoptions(precision=6)
print(risk_level_widelong)
print(f' Bottom right corner elem: {risk_level_widelong[len(risk_level_widelong) - 1, len(risk_level_widelong) - 1]}')


# Way 2
def make_5x_wide_matrix(input_matrix_):
    new_matrix = np.zeros((input_matrix_.shape[0] * 5, input_matrix_.shape[1] * 5))
    for i in range(5):
        for j in range(5):
            for k in range(len(input_matrix_)):
                for m in range(len(input_matrix_[k])):
                    value = input_matrix_[k, m] + i + j
                    if value > 9:
                        value = value - 9
                    new_matrix[k + input_matrix_.shape[0] * i, m + input_matrix_.shape[1] * j] = value

    return new_matrix


print('2) Another way to calc wide input matrix:')
large5xmatrix = make_5x_wide_matrix(input_matrix)
print(f'5x matrix: \n {large5xmatrix}')
print(large5xmatrix.shape)

risk_level_widelong2 = calc_risk_level_matrix(large5xmatrix)

np.set_printoptions(precision=6)
print(risk_level_widelong2)
print(
    f' Bottom right corner elem: {risk_level_widelong2[risk_level_widelong2.shape[0] - 1, risk_level_widelong2.shape[1] - 1]}')


# r[i,j,k steps] = min(4 options with i+-1, j+-1, k-1 steps) + input[i,j]
def calc_risk_level_matrix_advanced(input_matrix_, max_steps):
    max_cost = np.max(input_matrix_) * max_steps  # some big number on total path cost
    risk_level_ = max_cost * np.ones((input_matrix_.shape[0], input_matrix_.shape[1], max_steps))

    print('... Calculating opt path')
    for k in range(max_steps):
        if k == 0:
            risk_level_[0, 0, 0] = 0
            continue
        if k % 10 == 0:
            print(f'     step {k}/{max_steps}')
        for i in range(len(input_matrix_)):
            for j in range(len(input_matrix_[i])):
                if i + j > k:  # can't reach [i,j] for less than i+j steps
                    continue

                left_elem = risk_level_[i - 1, j, k - 1] if i > 0 else max_cost
                right_elem = risk_level_[i + 1, j, k - 1] if i < len(input_matrix_) - 1 else max_cost
                up_elem = risk_level_[i, j - 1, k - 1] if j > 0 else max_cost
                down_elem = risk_level_[i, j + 1, k - 1] if j < len(input_matrix_[i]) - 1 else max_cost
                cur_step = min(left_elem, right_elem, up_elem, down_elem) + input_matrix_[i, j]
                risk_level_[i, j, k] = min(risk_level_[i, j, k - 1], cur_step)

    # result = matrix of cost in max_steps
    res = np.zeros(input_matrix_.shape)
    for i in range(len(input_matrix_)):
        for j in range(len(input_matrix_[i])):
            res[i, j] = risk_level_[i, j, max_steps - 1]

    return res


print('3) Another way to calc cost paths (where you can go left-up-down-right - all 4 directions, not only 2):')
large5xmatrix = make_5x_wide_matrix(input_matrix)
print(f'5x matrix: \n {large5xmatrix}')
print(large5xmatrix.shape)

risk_level_widelong3 = calc_risk_level_matrix_advanced(large5xmatrix, 3 * large5xmatrix.shape[0])

np.set_printoptions(precision=6)
print(risk_level_widelong3)
print(
    f' Bottom right corner elem: {risk_level_widelong3[risk_level_widelong3.shape[0] - 1, risk_level_widelong3.shape[1] - 1]}')
