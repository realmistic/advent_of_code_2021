# https://github.com/WilliamLP/AdventOfCode/blob/master/2021/day24.py#L4

# (NOT WORKING SOL!!!)

#  ANOTHER COMMENT USEFUL:::
# Zig (https://www.reddit.com/r/adventofcode/comments/rnejv5/2021_day_24_solutions/)
#
# This was a massive pain
#
# After solutions that would never yield a result (let me loop 914 numbers real quick) and a lot of hours, coming here
# for the first time before solving the problem (I gave a really quick look, but I actually didn't end up implementing
# the solutions, and really picked up just the hint about reaching 0 through divisions, that I remembered later), and
# a really long and tedious manual calculation, the solution came to my mind.
#
# The solution is based on the fact that z is always something like 26*(26*(in0 + n0) + in1 + n1) + in2 + n2 etc, and
# that there are 14 series of 18 instructions. Most of these instructions are actually useless. The important ones are
# the number that gets added to x after it gets cleared and z gets added to it, by what number z gets divided, and the
# number that gets added to y after w (which will make the pairs w + n on z)
#
# Briefly : z is a stack, and the top level is the one not multiplied by 26. Every time you multiply z by 26 you also
# push w + n onto the stack. Every time you divide z by 26 you pop from the stack. Because the objective is to get 0,
# and z will be multiplied by 26 at least 6 times (7, but the first time z is 0), you have to divide z by 26 7 times,
# without additional multiplications. The trick is that the multiplication by 26 of z is controlled by y. y gets added 25,
# then multiplies by x, and then gets added 1. If x is 0, y is 1 and z doesn't multiply. To get x to be 0, x has to be
# equal to w after it becomes the top element of z + another number. This gives us minimum and maximum values for both
# the w in question (the current digit) and the digit that came from z. After having calculated all the maximum and
# minimum mandatory values it's easy to just get the final result. For the maximum it's the maximum mandatory values
# and all the blanks get filled with 9 and for the minimum it's the minimum mandatory values and all the blanks get
# filled with 1.
#
# I actually don't even know if the solution is valid for other inputs. At least it's fast, 10-20μs.
# (EDIT: it's actually under 1μs, I forgot to move the print)
#
# code



REGS = {'w': 0, 'x': 1, 'y': 2, 'z': 3}


def execute(line, regs, input_arr):
    instr, reg, operand = line
    if instr == 'inp':
        regs[REGS[reg]] = int(input_arr.pop(0))
    else:
        if operand in REGS.keys():
            n = regs[REGS[operand]]
        else:
            n = int(operand)
        if instr == 'add':
            regs[REGS[reg]] += n
        elif instr == 'mul':
            regs[REGS[reg]] *= n
        elif instr == 'mod':
            regs[REGS[reg]] %= n
        elif instr == 'div':
            regs[REGS[reg]] //= n
        elif instr == 'eql':
            regs[REGS[reg]] = 1 if regs[REGS[reg]] == n else 0


MEMO2 = {}


def execute_all(chunks, pos, input, z):
    key = f'{pos} {input} {z}'
    if key in MEMO2:
        return MEMO2[key]
    regs = [0, 0, 0, z]
    input_arr = list(str(input))
    for line in chunks[pos]:
        execute(line, regs, input_arr)
    res = regs[REGS['z']]
    MEMO2[key] = res
    return res


MEMO = {}
MIN_Z = 999999


def find(chunks, pos, z):
    global MIN_Z

    key = f'{pos} {z}'
    if key in MEMO:
        return MEMO[key]
    found = None

    # PART 1
    # for i in (9,8,7,6,5,4,3,2,1):
    # PART 2
    for i in (1, 2, 3, 4, 5, 6, 7, 8, 9):
        exec_result = execute_all(chunks, pos, i, z)
        if (pos == 13):
            if abs(exec_result) < MIN_Z:
                print(f'Min z {exec_result}')
                MIN_Z = abs(exec_result)
            if exec_result == 0:
                found = [i]
                break
            else:
                found = None
        else:
            new_found = find(chunks, pos + 1, exec_result)
            if new_found:
                found = [i] + new_found
                break

    MEMO[key] = found
    return found


def main():
    code = []
    for line in open('../inputs/day24/input.txt'):
        tokens = line.strip().split(' ')
        code.append((tokens[0], tokens[1], tokens[2] if len(tokens) > 2 else None))

    chunks = []
    rest = code
    while rest:
        chunks.append(rest[0:18])
        rest = rest[18:]

    res = find(chunks, 0, 0)
    print(f"Part 2 Answer: {''.join([str(ch) for ch in res])}")


main()
