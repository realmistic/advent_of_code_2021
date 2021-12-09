text_file = open('inputs/day2_1/input.txt', 'r')

# lines = text_file.readlines()
lines = text_file.read().splitlines()

horizontal = 0
depth = 0
aim = 0

for line in lines:
    arr = line.split()
    if arr[0] == 'forward':
        horizontal += int(arr[1])
        depth += aim * int(arr[1])
    elif arr[0] == 'down':
        # depth += int(arr[1])
        aim += int(arr[1])
    elif arr[0] == 'up':
        # depth -= int(arr[1])
        aim -= int(arr[1])
    else:
        raise Exception('strange command')

print(f'depth = {depth}, horizontal = {horizontal}, product = {depth * horizontal}')

print(lines[0:10])
print(lines[-10:])
print(len(lines))
