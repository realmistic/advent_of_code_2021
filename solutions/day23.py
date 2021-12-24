import numpy as np

text_file = open('../inputs/day23/input_test.txt', 'r')
field = text_file.read().splitlines()
input_field = []
for line in field:
    arr = list(line)
    input_field.append(arr)


def print_map(field_):
    for line_ in field_:
        for elem in line_:
            print(elem, end='')
        print('')
    print('==============================')
    return None


def is_exit_cave(cur_x_: int, cur_y_: int) -> bool:
    # exits : [(1, 3), (1, 5), (1, 7), (1, 9)]
    if cur_x_ == 1 and cur_y_ in {3, 5, 7, 9}:
        return True
    else:
        return False


def find_one_char_moves(field_, start_x: int, start_y: int):
    res = []
    cur_x: int
    cur_y: int
    queue_ = [(start_x, start_y)]
    color = np.zeros((len(field_), len(field_[0])))
    color[start_x, start_y] = 1

    while len(queue_) > 0:
        cur_x, cur_y = queue_.pop(0)
        for next_x in [-1, 0, 1]:
            for next_y in [-1, 0, 1]:
                if next_x == 0 or next_y == 0:
                    if 0 <= cur_x + next_x < len(field_) \
                            and 0 <= cur_y + next_y < len(field_[cur_x + next_x]) \
                            and field_[cur_x + next_x][cur_y + next_y] == '.' \
                            and color[cur_x + next_x, cur_y + next_y] == 0:
                        queue_.append((cur_x + next_x, cur_y + next_y))
                        color[cur_x + next_x, cur_y + next_y] = 1
                        if (cur_x + next_x != start_x) or (cur_y + next_y != start_y):
                            if is_exit_cave(cur_x + next_x, cur_y + next_y):
                                continue
                            if start_x == 1 and cur_x + next_x == 1:
                                continue
                            if cur_x + next_x != 1:
                                if field_[start_x][start_y] == 'A' and cur_y + next_y != 3:
                                    continue
                                if field_[start_x][start_y] == 'B' and cur_y + next_y != 5:
                                    continue
                                if field_[start_x][start_y] == 'C' and cur_y + next_y != 7:
                                    continue
                                if field_[start_x][start_y] == 'D' and cur_y + next_y != 9:
                                    continue

                                if field_[start_x][start_y] == 'A' and cur_x + next_x < len(field_) - 1 and field_[
                                    cur_x + next_x][3] == '.':
                                    continue
                                if field_[start_x][start_y] == 'B' and cur_x + next_x < len(field_) - 1 and field_[
                                    cur_x + next_x][5] == '.':
                                    continue
                                if field_[start_x][start_y] == 'C' and cur_x + next_x < len(field_) - 1 and field_[
                                    cur_x + next_x][7] == '.':
                                    continue
                                if field_[start_x][start_y] == 'D' and cur_x + next_x < len(field_) - 1 and field_[
                                    cur_x + next_x][9] == '.':
                                    continue
                            res.append((cur_x + next_x, cur_y + next_y))

    return res


def find_all_moves(field_):
    res = []
    for i in range(len(field_)):
        for j in range(len(field_[i])):
            if field_[i][j] in {'A', 'B', 'C', 'D'}:
                # print(f'Found letter {field_[i][j]} at pos {i, j}')
                m = find_one_char_moves(field_, i, j)
                for q, v in m:
                    res.append((i, j, q, v))
    return res


def apply_moves_to_field(field_, moves_history_, debug_= False):
    if len(moves_history_) == 0:
        return field_, 0
    res = [row[:] for row in field_]
    cost_ = 0
    price = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    for move_ in moves_history_:
        # print(move_)
        # x1 = move_[0]
        # y1 = move_[1]
        # x2 = move_[2]
        # y2 = move_[3]
        (x1, y1, x2, y2) = move_
        cost_ += price[res[x1][y1]]
        res[x2][y2] = res[x1][y1] + ""  # hack: PYTHON doesn't support string assignment
        res[x1][y1] = '.'
        if debug_:
            print_map(res)
    return res, cost_


def is_final_solution_partA(field_):
    if field_[2][3] == 'A' and field_[3][3] == 'A':
        if field_[2][5] == 'B' and field_[3][5] == 'B':
            if field_[2][7] == 'C' and field_[3][7] == 'C':
                if field_[2][9] == 'D' and field_[3][9] == 'D':
                    return True
    return False


h = len(input_field)
w = [max(len(line) for line in input_field)][0]
print(f' Initial stage: \n')
print(f'h={h}, w={w}')
print_map(input_field)

queue = [(input_field, [])]
MAX_MOVES = 20
BEST_SOLUTION = 1e10
total_steps = 0

while len(queue) > 0:
    cur_field, cur_moves_history = queue.pop(0)

    if total_steps % 10000 == 0 and total_steps > 0:
        print(f'checked steps: {total_steps}, current moves hist = {cur_moves_history}')
    if total_steps % 100000 == 0 and total_steps > 0:
        field, cost = apply_moves_to_field(input_field, cur_moves_history, debug_=True)
    if is_final_solution_partA(cur_field):
        field, cost = apply_moves_to_field(input_field, cur_moves_history)
        if cost < BEST_SOLUTION:
            print(f'Found solution with cost: {cost}')
            print(f'Moves history: {cur_moves_history}')
            print('---------------')
            BEST_SOLUTION = cost
            continue

    if cur_moves_history and len(cur_moves_history) >= MAX_MOVES:
        continue

    next_moves = find_all_moves(cur_field)
    for move in next_moves:
        new_field, c = apply_moves_to_field(cur_field, [move])
        if not cur_moves_history:
            new_moves_history = [move]
        else:
            new_moves_history = [x for x in cur_moves_history]
            new_moves_history.append(move)
            # print(new_moves_history)
        queue.append((new_field, new_moves_history))

    total_steps += 1
