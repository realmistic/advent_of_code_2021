# Conditions from day24_Ivan_manual_calc
#  a3+4 =a4
#  a6-3=a7
#  a8+6=a9
#  a10=a11
#  a5+1=a12
#

import numpy as np

text_file = open('../inputs/day24/input.txt', 'r')
lines = text_file.read().splitlines()
commands = []
for line in lines:
    commands.append(line.split(' '))
# print(commands)

# number = 13579246899999
memory = {'w': 0, 'x': 0, 'y': 0, 'z': 0}


def command_inp(line_stripped_, debug_=False):
    global number, cur_pos, memory
    s_number = str(number)
    ch = s_number[cur_pos]
    memory[line_stripped_[1]] = int(ch)
    cur_pos += 1
    if debug_:
        print(f' --- INPUT NEW AT POSITION = {cur_pos}')
        print(line_stripped_)
        print(memory)
    return


def command_others(line_stripped_, debug_ = False):
    global memory
    command: str = line_stripped_[0]
    param1: str = line_stripped_[1]
    param2: str = line_stripped_[2]

    if command == 'add':
        if param2.lstrip("-").isnumeric():
            memory[param1] += int(param2)
        else:
            memory[param1] += memory[param2]
    elif command == 'mul':
        if param2.lstrip("-").isnumeric():
            memory[param1] *= int(param2)
        else:
            memory[param1] *= memory[param2]
    elif command == 'div':
        if param2.lstrip("-").isnumeric():
            memory[param1] = memory[param1] // int(param2)
        else:
            memory[param1] = memory[param1] // memory[param2]
    elif command == 'mod':
        if param2.lstrip("-").isnumeric:
            memory[param1] = memory[param1] % int(param2)
        else:
            memory[param1] = memory[param1] % memory[param2]
    elif command == 'eql':
        if param2.lstrip("-").isnumeric():
            value = int(param2)
        else:
            value = memory[param2]
        if memory[param1] == value:
            memory[param1] = 1
        else:
            memory[param1] = 0

    if debug_:
        print(line_stripped_)
        print(memory)

    return


# number = 99598963999999

number = 11151411711111


valid = False

while number > 1e13:
    cur_pos = 0
    memory = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    for stripped_command in commands:
        if stripped_command[0] == 'inp':
            command_inp(stripped_command, debug_=False)
        else:
            command_others(stripped_command, debug_=False)

    if memory['z'] == 0:
        valid = True
        print(f'Found the first valid number: {number}')
        break

    # print(f' number = {number}, iterations passed = {99999999999999 - number}')
    # if 99999999999999 - number > 100:
    #     break
    if number % 100000 == 11111:
        print(f' number = {number}, memory = {memory}, iterations passed = {99999999999999 - number}')

    number += 1
    while str(number).find('0') > -1:
        number += 1

