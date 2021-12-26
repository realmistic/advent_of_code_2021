import numpy as np


def get_coords(line_str_: str, cut_boundaries=50, shift_right=50):
    splitted_line = line_str_.split(" ")
    mode_ = splitted_line[0]
    three_coords = splitted_line[1].split(',')

    res = []
    is_bad_cube = False

    for coord in three_coords:
        eq = coord.split('..')
        left_value = int(eq[0].split('=')[1])
        right_value = int(eq[1])

        if np.abs(left_value)> cut_boundaries and np.abs(right_value) > cut_boundaries:
            if np.sign(left_value) == np.sign(right_value):
                is_bad_cube = True

        if left_value < -cut_boundaries:
            left_value = -cut_boundaries
        if left_value > cut_boundaries:
            left_value = cut_boundaries

        if right_value < -cut_boundaries:
            right_value = -cut_boundaries
        if right_value > cut_boundaries:
            right_value = cut_boundaries
        res.append(
            (left_value + shift_right, right_value + shift_right))  # only positive indexes 0..100 instead of [-50,50]


    return mode_, res, is_bad_cube


def change_lights(mode_, coords_):
    global megacube
    value = 0
    if mode_ == 'on':
        value = 1
    for x in range(coords_[0][0], coords_[0][1] + 1):
        for y in range(coords_[1][0], coords_[1][1]+1):
            for z in range(coords_[2][0], coords_[2][1]+1):
                if megacube[x, y, z] == 1 and mode_ == 'off':
                    megacube[x, y, z] = 0
                if megacube[x, y, z] == 0 and mode_ == 'on':
                    megacube[x, y, z] = 1
    return


text_file = open('../inputs/day22/input.txt', 'r')
lines = text_file.read().splitlines()
# modes = []
# all_cube_coords = []
megacube = np.zeros((102, 102, 102))

for line in lines:
    print(line)
    mode, coords, is_bad = get_coords(line)
    print(coords)
    if not is_bad:
        change_lights(mode, coords)
    print(f'Now lights on {np.sum(megacube)}')


