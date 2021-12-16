# https://www.reddit.com/r/adventofcode/comments/rhj2hm/2021_day_16_solutions/  ==> taken Python solution from Derp_Derps

def read_stats():
    text_file = open('../inputs/day16/input_test.txt', 'r')
    lines = text_file.read().splitlines()
    return lines[0]

i, L = int, read_stats()


def p(N):
    V = i(N[:3], 2)
    T = i(N[3:6], 2)
    if T == 4:
        W = ''
        c = v = 6
        while v:
            v = i(N[c])
            W += N[c + 1:c + 5]
            c += 5
        W = i(W, 2)
    else:
        b = i(N[6])
        S = W = 0
        C = c = 22 - b * 4
        while [c - C, S][b] < i(N[7:C], 2):
            z, w, d = p(N[c:])
            W = [w, [W + w, W * w, min(W, w), max(W, w), 0, W > w, W < w, W == w][T]][S > 0]
            S += 1
            V += z
            c += d
    return V, i(W), c


print(p(bin(i(L, 16))[2:].zfill(len(L) * 4))[:2])
