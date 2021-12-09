text_file = open('inputs/day1_1/input.txt', 'r')

# lines = text_file.readlines()
lines = text_file.read().splitlines()
print(lines[0:10])
print(lines[-10:])
print(len(lines))

rez = 0
rez3 = 0


def sum3(i):
    if i < 2:
        return None
    return int(lines[i]) + int(lines[i - 1]) + int(lines[i - 2])


for i, l in enumerate(lines):
    if i == 0:
        continue

    if int(lines[i]) >= int(lines[i - 1]):
        rez += 1

    if i > 2:
        if sum3(i) > sum3(i - 1):
            rez3 += 1

print(rez)
print(rez3)
# inputs/day1_1/input.txt
