import numpy as np

text_file = open('../inputs/day21/input.txt', 'r')
lines_ = text_file.read().splitlines()

cur_pos_player1 = int(lines_[0].split(' ')[4])
cur_pos_player2 = int(lines_[1].split(' ')[4])
print(f' INPUT: Player 1 starts at {cur_pos_player1}, player 2 start at {cur_pos_player2}')

score1 = 0
score2 = 0

whos_turn = 1
dice_value = 1
rolls = 0
while score1 < 1000 and score2 < 1000:
    move = (dice_value + dice_value + 1 + dice_value + 2) % 10
    dice_value += 3
    if dice_value > 100:
        dice_value -= 100
    rolls += 3

    if whos_turn == 1:
        cur_pos_player1 = (cur_pos_player1 + move) % 10
        if cur_pos_player1 == 0:
            cur_pos_player1 = 10
        score1 += cur_pos_player1
        whos_turn = 2
    elif whos_turn == 2:
        cur_pos_player2 = (cur_pos_player2 + move) % 10
        if cur_pos_player2 == 0:
            cur_pos_player2 = 10
        score2 += cur_pos_player2
        whos_turn = 1

# PART 1
part1_ans = 0
if score1 >= 1000:  # player1 wins
    part1_ans = score2 * rolls
    print(f'Player 1 wins (score2 = {score2}, rolls = {rolls}), the score is {part1_ans}')
if score2 >= 1000:  # player2 wins
    part1_ans = score1 * rolls
    print(f'Player 2 wins (score1 = {score1}, rolls = {rolls}), the score is {part1_ans}')

# PART 2
#  state[<pos1, pos2, score1, score2, step>]
state = np.zeros((11, 11, 21, 21, 101))
state[cur_pos_player1, cur_pos_player2, 0, 0, 0] = 1

won1 = 0
won2 = 0


def get_available_states_count(step_):
    global state
    res: int = 0
    for cur_pos1_ in range(1, 11, 1):
        for cur_pos2_ in range(1, 11, 1):
            for score1_ in range(0, 20, 1):
                for score2_ in range(0, 20, 1):
                    res += state[cur_pos1_, cur_pos2_, score1_, score2_, step_]
    return res


def make_one_step(step_):
    global won1
    global won2
    global state

    for cur_pos1_ in range(1, 11, 1):
        for cur_pos2_ in range(1, 11, 1):
            for score1_ in range(0, 20, 1):
                for score2_ in range(0, 20, 1):
                    if state[cur_pos1_, cur_pos2_, score1_, score2_, step_ - 1] > 0:  # at least one state of world
                        adds_ = [z + y + x for x in range(1, 4) for y in range(1, 4) for z in range(1, 4)]
                        for dice_ in adds_:
                            if step_ % 2 == 1:  # 1st player's turn
                                new_pos = (cur_pos1_ + dice_) % 10
                                if new_pos == 0:
                                    new_pos = 10
                                new_score = score1_ + new_pos
                                if new_score >= 21:
                                    won1 += state[cur_pos1_, cur_pos2_, score1_, score2_, step_ - 1]
                                else:
                                    state[new_pos, cur_pos2_, new_score, score2_, step_] += state[
                                        cur_pos1_, cur_pos2_, score1_,
                                        score2_, step_ - 1]

                            if step_ % 2 == 0:  # 2nd player's turn
                                new_pos = (cur_pos2_ + dice_) % 10
                                if new_pos == 0:
                                    new_pos = 10
                                new_score = score2_ + new_pos
                                if new_score >= 21:
                                    won2 += state[cur_pos1_, cur_pos2_, score1_, score2_, step_ - 1]
                                else:
                                    state[cur_pos1_, new_pos, score1_, new_score, step_] += state[
                                        cur_pos1_, cur_pos2_, score1_,
                                        score2_, step_ - 1]
    return


step = 0
while get_available_states_count(step) > 0:
    print(f'Available unfinished states after step {step} is {get_available_states_count(step)}')
    step += 1
    make_one_step(step)
    print(f'AFTER TRANSFORM: Available unfinished states after step {step} is {get_available_states_count(step)}')
    print('---------------------')

print(f' Player1 wins = {won1}')
print(f' Player2 wins = {won2}')


# One solution from https://www.reddit.com/r/adventofcode/comments/rl6p8y/2021_day_21_solutions/

init, goal, won = (8, 3, 0, 0), 21, [0, 0]
adds = [z + y + x for x in range(1, 4) for y in range(1, 4) for z in range(1, 4)]
perms = {a: adds.count(a) for a in adds}
states = {(x, y, z, w): 0 for x in range(1, 11) for y in range(1, 11) for z in range(0, goal) for w in range(0, goal)}
states[init] = 1
while not max(states.values()) == 0:
    for state, value in states.items():
        if value > 0:
            for p, n in perms.items():  # player 1
                for q, m in perms.items():  # try player 2 as well
                    pos = [(state[0] + p - 1) % 10 + 1, (state[1] + q - 1) % 10 + 1]
                    new = tuple(pos + [state[2] + pos[0], state[3] + pos[1]])
                    if max(new[2:]) < goal:  # neither player has won
                        states[new] += value * n * m
                    elif new[3] >= goal and new[2] < goal:  # player 2 won
                        won[1] += value * m * n
                if new[2] >= goal:  # player 1 won before player 2 even played
                    won[0] += value * n
            states[state] = 0
print(max([won[0], won[1]]))
