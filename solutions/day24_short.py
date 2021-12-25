# https://www.reddit.com/r/adventofcode/comments/rnejv5/2021_day_24_solutions/


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


with open("../inputs/day24/input.txt", 'r') as file:
    data = [x.strip('\n').strip().splitlines() for x in file.read().split('inp w\n')[1:]]
    non_matching = [e for e,x in enumerate(data[0]) if not all(data[y][e] == x for y in range(len(data)))]
    diffs = [[int(data[i][e].split()[-1]) for e in non_matching] for i in range(len(data))]
    q, mx, mn = [], [0] * 14, [0] * 14
    for a, x in enumerate(data):
        if diffs[a][0] == 1:
            q.append((a, diffs[a][2]))
        else:
            b, y = q.pop()
            delta = y + diffs[a][1]
            if not delta >= 0:
                a, b, delta = b, a, -delta
            mx[a], mx[b] = 9, 9 - delta
            mn[b], mn[a] = 1, 1 + delta
    print(''.join([str(x) for x in mx]))
    print(''.join([str(x) for x in mn]))