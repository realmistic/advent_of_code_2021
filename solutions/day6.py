import numpy as np

text_file = open('inputs/day6/input.txt', 'r')

lines = text_file.read().splitlines()

numbers = [int(x) for x in lines[0].split(',')]

print(numbers)

state = np.zeros(9)

for i in numbers:
    state[i] += 1

print(f'Initial state (for (0,1,2,3,4,5,6,7,8): {state}')

for i in range(1, 257, 1):
    state1_old = state[1]
    state[1] = state[2]
    state[2] = state[3]
    state[3] = state[4]
    state[4] = state[5]
    state[5] = state[6]
    state[6] = state[7] + state[0]
    state[7] = state[8]
    state[8] = state[0]
    state[0] = state1_old



    print(f'After day {i}: {state}')


print(np.sum(state))