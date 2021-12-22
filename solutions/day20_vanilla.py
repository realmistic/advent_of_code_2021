# solution from here: https://topaz.github.io/paste/#XQAAAQBuBgAAAAAAAAARiEJHiiMzw3cPM/1Vl+2nx/DqKkM2yi+HVdpp+qLh9JthAlPx4DmzLT4PGzwPoF1Bt8DcoyDmosYJFB+TUc+YdqzJ31jw/WN9NSYHEt5lpxQ6iXumO5EP3NtZHDCdWAdrgCLFlZHkRXABU8dHwipG3qmXNpyZnAp6p/ZURMa67D/35ps3XvPn6zYM9v9xbMk2o3ugy/JZ9j1PowF2edlAeaYY8K0PSjdaBGsz16Giy0iq2czpMSQ6TZy0PMfPHOs9CN6HK2KiMn85EmNRpqaCiSWnba/09DGCyPligQr6sgJ/U2XLpE0gBljzCneDfMEVqXhu0vG2MSzmv4kPE0qTBbjw8a1N6asmvVIrKDGO0ciUUprAt7HufoTcQ2P41ZMHRxtJtoj59wLWsoRiqzH6MHQkd2g2WG8YZsihujV2ATQQeOLHGBGBzVmyBtaL2/MWwK/f5MuH8pP73HwmksTv5CQGeKPNWBrmnvRqyg98tjUu3J+/brFZn9TjbxrV7J4OZCZnJmXcT0X1pi6L7xzKOW7RE4UdK4rEKB1Wy3vKwb/tTL1UvHNnxP8UELCzJZ4utbW53rVCxsp4/myOFr9QGi8PfeK6nAtBMue/+3eucKwqF84r7/D3cmhfM7yMmk3DVbpA7GTY8KbeU5PFod2NrguN1iAYs0t5wxb/q6XpiKYoYGLB0oeOcHOtY2PWmDJBdcWL9f0Fe9fUBkAzmeIpbQkzBCUVRbgaZ5h6EjuLXri1QGXBMl+4aC12q4aIoi6z1w1Ngp1MmwDR2fYzqi/3IXtYPfEE1gnV/q80JlruFUCgfOd8MLK6rJFSc53RsAGtnzAhpAspBqWSjx+os7P3Mdr96sfvu5rtK1YSodz7iVzJF57/8YxC2Q==
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