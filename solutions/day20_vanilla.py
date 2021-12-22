import numpy as np

from bitstring import BitArray

with open('../inputs/day20/input.txt') as fh:
    data = fh.read()


def load_data(data):
    alg_s, pic_s = [x.strip() for x in data.split('\n\n')]

    alg_s = ''.join(alg_s.split())
    alg = np.zeros(len(alg_s), dtype=np.bool8)
    for i, c in enumerate(alg_s):
        alg[i] = (c == '#')

    piclines = pic_s.split()
    h = len(piclines)
    w = len(piclines[0])

    pic = np.zeros((h, w), dtype=np.bool8)
    for i, line in enumerate(piclines):
        for j, c in enumerate(line):
            pic[i, j] = (c == '#')

    return pic, alg


def printpic(pic):
    for row in pic:
        print(''.join('#' if b else '.' for b in row))


def resolve(pic, alg, infinite_light=False):
    h0, w0 = pic.shape
    h, w = h0 + 4, w0 + 4
    if alg[0] and infinite_light:
        pic1 = np.ones((h, w), dtype=np.bool8)
        pic2 = np.ones((h, w), dtype=np.bool8)
    else:
        pic1 = np.zeros((h, w), dtype=np.bool8)
        pic2 = np.zeros((h, w), dtype=np.bool8)
    pic1[2:h - 2, 2:w - 2] = pic
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            subpic = pic1[i - 1:i + 2, j - 1:j + 2]
            n = BitArray(subpic.ravel()).uint
            pic2[i, j] = alg[n]
    return pic2[1:-1, 1:-1], not infinite_light


pic1, alg = load_data(data)
infinite_light = False
for _ in range(2):
    pic1, infinite_light = resolve(pic1, alg, infinite_light)
print('part_1 =', pic1.sum())

# Part 2

pic2, alg = load_data(data)
infinite_light = False

for _ in range(50):
    pic2, infinite_light = resolve(pic2, alg, infinite_light)

print('part_2 =', pic2.sum())