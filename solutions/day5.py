import numpy as np

text_file = open('inputs/day5/input.txt', 'r')


def get_two_points(text_line):
    two_coord = text_line.split(' -> ')
    x1 = int(two_coord[0].split(',')[0])
    y1 = int(two_coord[0].split(',')[1])
    x2 = int(two_coord[1].split(',')[0])
    y2 = int(two_coord[1].split(',')[1])
    return x1, y1, x2, y2


def mark_points(field_param, x1, y1, x2, y2):
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2)+1, 1):
            field_param[x1, i] += 1
    if y1 == y2:
        for i in range(min(x1, x2), max(x1, x2)+1, 1):
            field_param[i, y1] += 1


def mark_points_diag(field_param, x1, y1, x2, y2):
    if (x1 - x2) == (y1 - y2):  # from left to right diag
        x_start = min(x1, x2)
        y_start = min(y1, y2)
        for i in range(abs(x1 - x2)+1):
            field_param[x_start, y_start] += 1
            x_start += 1
            y_start += 1

    else:  # from right to left diag
        x_start = min(x1, x2)
        y_start = max(y1, y2)
        for i in range(abs(x1 - x2)+1):
            field_param[x_start, y_start] += 1
            x_start += 1
            y_start -= 1


# lines = text_file.readlines()
lines = text_file.read().splitlines()

# x1_arr = []
# x2_arr = []
# y1_arr = []
# y2_arr = []

field = np.zeros((1000, 1000))

for line in lines:
    x1, y1, x2, y2 = get_two_points(line)
    if (x1 == x2) or (y1 == y2):
        # x1_arr.append(x1)
        # x2_arr.append(x2)
        # y1_arr.append(y1)
        # y2_arr.append(y2)
        mark_points(field, x1, y1, x2, y2)
    else:
        # True
        mark_points_diag(field, x1, y1, x2, y2)

rez = 0
for j in range(len(field)):
    for k in range(len(field[j])):
        if field[j, k] > 1:
            rez += 1

print(rez)

print(field[0:10, 0:10].T)
#
# print(lines[0])
# print(len(lines))
# #
# # print(len(x1_arr))
# print(np.max(x1_arr))
# print(np.max(x2_arr))
# print(np.max(y1_arr))
# print(np.max(y2_arr))

