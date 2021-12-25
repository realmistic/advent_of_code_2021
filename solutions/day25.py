from pprint import pprint
from typing import List

import numpy as np

text_file = open('../inputs/day25/input.txt', 'r')
field = text_file.read().splitlines()
input_field = []
for line in field:
    arr = list(line)
    input_field.append(arr)


def get_herd_coords(matrix_: List[List], direction_) -> List:
    res = []
    for i in range(len(matrix_)):
        for j in range(len(matrix_[i])):
            if direction_ == 'east':
                if matrix_[i][j] == '>':
                    res.append((i, j))

            if direction_ == 'south':
                if matrix_[i][j] == 'v':
                    res.append((i, j))
    return res


east_herd = get_herd_coords(input_field, 'east')
south_herd = get_herd_coords(input_field, 'south')

data = np.matrix(input_field)  # better to store in a data
print(f' Input field: \n')
print(data)
print(f'Data shape == {data.shape}')
print('--------------------------------------')

def get_moves(data_: np.matrix):
    moves_right_ = []
    moves_down_ = []
    next_i: int
    next_j: int

    h, w = data_.shape

    for idx, x in np.ndenumerate(data_):
        if idx[1] + 1 > w - 1:
            next_j = 0
        else:
            next_j = idx[1] + 1
        if x == '>' and data_[idx[0], next_j] == '.':
            moves_right_.append(idx)

    for idx, x in np.ndenumerate(data_):
        if idx[0] + 1 > h - 1:
            next_i = 0
        else:
            next_i = idx[0] + 1
        if x == 'v' and data_[next_i, idx[1]] == '.':
            moves_down_.append(idx)

    return moves_right_, moves_down_


# moves_right, moves_down = get_moves(data)
# print(f'Moves right = {moves_right}')
# print(f'Moves down = {moves_down}')


def append_moves(data_: np.matrix, moves_: List, direction: str) -> np.matrix:
    res = np.matrix(data_)
    h, w = data_.shape

    for move in moves_:
        if direction == 'right':
            if move[1] + 1 > w - 1:
                res[move[0], 0] = '>'
            else:
                res[move[0], move[1] + 1] = '>'
            res[move] = '.'

        if direction == 'down':
            if move[0] + 1 > h - 1:
                res[0, move[1]] = 'v'
            else:
                res[move[0] + 1, move[1]] = 'v'
            res[move] = '.'

    return res


moves_right, moves_down = get_moves(data)
steps = 1
cur_data = np.matrix(data)
while len(moves_right) > 0 or len(moves_down) > 0:
    print(f'Moves right: {moves_right}')
    cur_data = append_moves(cur_data, moves_right, "right")
    moves_right, moves_down = get_moves(cur_data)
    print(f'Moves down: {moves_down}')
    cur_data = append_moves(cur_data, moves_down, "down")

    moves_right, moves_down = get_moves(cur_data)
    steps += 1
    print(f' After {steps} steps:')
    print(cur_data)
    if steps >= 1e5:
        break


print('================')
print('Result:')
print(cur_data)
print(f' Steps: {steps}')
