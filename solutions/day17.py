def read_stats():
    text_file = open('../inputs/day17/input.txt', 'r')
    lines = text_file.read().splitlines()
    line = lines[0].split(' ')
    print(line)
    # all_condition = line[1].split(',')
    x_cond = line[2].split('=')[1].split('..')
    int_x_cond = [int(x.replace(',', '')) for x in x_cond]
    y_cond = line[3].split('=')[1].split('..')
    int_y_cond = [int(y.replace(',', '')) for y in y_cond]
    return int_x_cond, int_y_cond


def emulate_path(initial_x, initial_y, is_debug=False):
    x = initial_x
    y = initial_y
    cur_x = 0
    cur_y = 0
    while True:
        cur_x += x
        cur_y += y
        if is_debug:
            print(cur_x, cur_y)
        if x > 0:
            x -= 1
        elif x < 0:
            x += 1
        y -= 1

        if x_cond[0] <= cur_x <= x_cond[1]:
            if y_cond[0] <= cur_y <= y_cond[1]:
                return cur_x, cur_y

        if cur_y < y_cond[0]:
            break

    return -1, -1


x_cond, y_cond = read_stats()
print(f' Initial conditions to be in : {x_cond}, {y_cond}')


x_best = 0
y_best = 0
highest_y_pos = 0
total_solutions = 0

#DEBUG:  x_best, y_best = emulate_path(7, -1, True)

for initial_forward in range(1, x_cond[1]+5, 1):
    for initial_upward in range(-500, 500, 1):
        if initial_forward % 50 == 0 and initial_upward % 50 == 0:
            print(initial_forward, initial_upward)

        hit_point_x, hit_point_y = emulate_path(initial_forward, initial_upward)
        if hit_point_x != -1 and hit_point_y != -1:
            # DEBUG: if (initial_forward < x_cond[0] or initial_forward > x_cond[1]) and (initial_upward < y_cond[0] or initial_upward > y_cond[1]):
            #     print(initial_forward, initial_upward, ';', end=' ')
            h_pos = initial_upward*(initial_upward+1)/2
            total_solutions += 1

            if h_pos > highest_y_pos:
                highest_y_pos = h_pos
                x_best = initial_forward
                y_best = initial_upward


print(f'Result initial velocity : {x_best}, {y_best}')
print(f'Highest y pos: {highest_y_pos}')
print(f'Total solutions: {total_solutions}')