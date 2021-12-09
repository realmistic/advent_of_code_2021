import numpy as np

text_file = open('inputs/day4/input.txt', 'r')
lines = text_file.read().splitlines()

numbers = [int(x) for x in lines[0].split(',')]

board = np.zeros((5, 5))
array_of_boards = []
highlighted = []

board_no = 0
row_no = 0
for i, line in enumerate(lines):
    if i == 0 or i % 6 == 1:
        continue
    one_line = [int(x) for x in line.split()]
    board[row_no] = one_line
    row_no += 1
    if row_no == 5:
        array_of_boards.append(board)
        highlighted.append(np.zeros((5, 5)))
        row_no = 0
        board_no += 1
        board = np.zeros((5, 5))

print(array_of_boards[0])
print(highlighted[0])
print(len(array_of_boards))
# print(array_of_boards[1])


print(np.sum(array_of_boards[0][0]))
print(array_of_boards[0].T)


def check_board_win(highlighted):
    for i in range(5):
        if (np.sum(highlighted[:, i]) == 5) or (np.sum(highlighted[i, :]) == 5):
            # if (np.sum(highlighted[i]) == 5) or (np.sum(highlighted.T[i]) == 5):
            return True
    return False


# not winning for the matrix of zeros
print(check_board_win(np.zeros((5, 5))))
#  winning for the matrix of ones
print(check_board_win(np.ones((5, 5))))


won_boards_indexes = np.zeros(len(array_of_boards))

def highlight_one_value(value, array_of_boards, array_of_highlights):
    for i in range(len(array_of_boards)):
        cur_board = array_of_boards[i]
        cur_highlighted = array_of_highlights[i]
        for j in range(len(board)):
            for k in range(len(board[j])):
                if cur_board[j][k] == value:
                    cur_highlighted[j][k] = 1
                    if check_board_win(cur_highlighted):  # found a winner
                        if won_boards_indexes[i] != 0:  # this boards was already a winner previously
                            continue
                        won_boards_indexes[i] = 1
                        if np.sum(won_boards_indexes) == len(array_of_boards):  # break only if it was the last boaarrd
                            return cur_board, cur_highlighted, i

    return array_of_boards[0], np.zeros((5, 5)), 0  # return  np.zeros((5, 5)) in all losing states

winning_number = 0
for number in numbers:
    winning_board, winning_highlighted, index_of_win_board = highlight_one_value(number, array_of_boards, highlighted)
    if not np.allclose(winning_highlighted, np.zeros((5, 5))):  # found a winner
        # if won_boards_indexes[index_of_win_board] != 0:  # this boards was already a winner previously
        #     continue
        # won_boards_indexes[index_of_win_board] = 1
        winning_number = number
        break
        # if np.sum(won_boards_indexes) == len(array_of_boards):  # break only if it was the last boaarrd
        #     break
print('!!!!Winner found!!!!:')
print(f' Winning number: \n {winning_number}')
print(f' Winning boards: \n {winning_board}')
print(f' Winning_highlighted: \n {winning_highlighted}')

print(f' Highlighted inverted: \n {1 - winning_highlighted}')

print(f' Select all NON Highlighted values: \n {(1 - winning_highlighted) * winning_board}')
print(f' SUM of all non-highlighted: \n {np.sum((1 - winning_highlighted) * winning_board)}')
print(f' Mult prev sum on winning number: \n {winning_number * np.sum((1 - winning_highlighted) * winning_board)}')
# print(winning_number * np.sum((1-winning_highlighted)*winning_board))

ssum = np.sum((1 - winning_highlighted) * winning_board)
print(winning_number * ssum)
