from typing import List

import numpy as np

ADDITIONAL_DOTS = 5


def line2arr(line_: str, left_right_zeros=ADDITIONAL_DOTS) -> List[bool]:
    res = np.zeros(left_right_zeros)
    for elem in line_:
        if elem == '.':
            res = np.append(res, 0)
        else:
            res = np.append(res, 1)

    res = np.concatenate((res, np.zeros(left_right_zeros)))
    return res


def pretty_print_matrix(matrix_):
    for i in range(len(matrix_)):
        for j in range(len(matrix_[i])):
            if matrix_[i, j] == 0:
                print('.', end='')
            else:
                print('#', end='')
        print('')


def read_stats(add_empty_dots_size=ADDITIONAL_DOTS):
    text_file = open('../inputs/day20/input.txt', 'r')
    lines_ = text_file.read().splitlines()
    image_enhancement_string = lines_[0]

    matrix_ = np.zeros((len(lines_[2]) + 2 * add_empty_dots_size, len(lines_[2]) + 2 * add_empty_dots_size))

    for i, line in enumerate(lines_[2:]):
        # print(line)
        matrix_[i + add_empty_dots_size] = line2arr(line)
        # print(line2arr(line))
    return matrix_, image_enhancement_string


def widen_matrix(matrix_, val):
    new_matrix_ = np.zeros((len(matrix_)+2*val, len(matrix_) + 2*val))
    for i in range(len(matrix_)):
        for j in range(len(matrix_[i])):
            new_matrix_[val + i, val + j] = matrix_[i, j]
    return new_matrix_


def cut_matrix(matrix_, val):
    m_ = matrix_[val:len(matrix_) - val, val:len(matrix_) - val]
    return m_


def make_enhancement(matrix_):
    res = np.zeros(matrix_.shape)

    for i in range(2, len(matrix_) - 3):
        for j in range(2, len(matrix_[i]) - 3):
            arr = matrix_[i:i + 3, j:j + 3].reshape(9, )
            str_arr = [str(int(x)) for x in arr]
            binary_num_str = "".join(str_arr)
            int_val = int(binary_num_str, 2)
            if enhancement_string[int_val] == '.':
                res[i + 1, j + 1] = 0
            else:
                res[i + 1, j + 1] = 1
    return res


input_matrix, enhancement_string = read_stats()

# print(input_matrix)
print(f'Enh string 100chars: {enhancement_string[0:100]}')
print(f'Step 0:')
pretty_print_matrix(input_matrix)
print(f' Lit pixels: {np.sum(input_matrix)}')
print(input_matrix.shape)
print('------------------------')

step1 = make_enhancement(input_matrix)
print(f'Step 1:')
# pretty_print_matrix(step1)
step1_c_matrix = cut_matrix(step1, ADDITIONAL_DOTS - 1)
pretty_print_matrix(step1_c_matrix)
step1_w_matrix = widen_matrix(step1_c_matrix, ADDITIONAL_DOTS)
print(step1_c_matrix.shape)

print(f' Lit pixels: {np.sum(step1_c_matrix)}')
print('------------------------')

step2 = make_enhancement(step1_w_matrix)
step2_c_matrix = cut_matrix(step2, ADDITIONAL_DOTS - 1)
print(f'Step 2:')
pretty_print_matrix(step2_c_matrix)
print(step2_c_matrix.shape)
print(f' Lit pixels: {np.sum(step2_c_matrix)}')
print('------------------------')
