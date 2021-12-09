text_file = open('inputs/day3_1/input.txt', 'r')


def str_to_binary(s):
    pow_of_two = 1
    rez = 0
    for i in reversed(s):
        if i == '1':
            rez += pow_of_two

        pow_of_two *= 2
    return rez


# lines = text_file.readlines()
lines = text_file.read().splitlines()

# array of zeros
most_popular = [0] * len(lines[0])

for line in lines:
    for key, v in enumerate(line):
        if line[key] == '1':
            most_popular[key] += 1

gamma_rate = ''
eps_rate = ''
for elem in most_popular:
    if elem >= len(lines) / 2:
        gamma_rate = gamma_rate + '1'
        eps_rate = eps_rate + '0'
    else:
        gamma_rate = gamma_rate + '0'
        eps_rate = eps_rate + '1'

print(most_popular)
print(f'Top 10 lines: {lines[0:10]}')
print(f'Total lines = {len(lines)}')

print(f'gamma_rate={gamma_rate}')
print(f'eps_rate={eps_rate}')

print(f'Power consumption= {str_to_binary(gamma_rate) * str_to_binary(eps_rate)}')

life_support_rating = 0



def get_most_popular(arr, position):
    rez = 0
    for elem in arr:
        if elem[position] == '1':
            rez += 1
    if rez >= len(arr) / 2:
        return '1'
    else:
        return '0'


def filter_arr(arr, num,position):
    rez = []
    for elem in arr:
        if elem[position] == num:
            rez.append(elem)
    return rez

print(get_most_popular(lines, 0))

lines2 = filter_arr(lines, '1',0)


arr1 = lines
pos = 0
while len(arr1)>1:
    print(f'Iteration {pos}, len(arr)={len(arr1)}')
    pop_value = get_most_popular(arr1, pos)
    arr1 = filter_arr(arr1, pop_value, pos)
    pos +=1

oxygen_gen_rating = arr1[0]
print(f'ox_gen_rating= {oxygen_gen_rating}')

arr1 = lines
pos = 0
while len(arr1)>1:
    print(f'Iteration {pos}, len(arr)={len(arr1)}')
    pop_value = get_most_popular(arr1, pos)
    less_pop = '0'
    if pop_value == '0':
        less_pop = '1'
    arr1 = filter_arr(arr1, less_pop, pos)
    pos +=1

co2_scrubber_rating = arr1[0]
print(f'co2_scrubber_rating= {co2_scrubber_rating}')

print(f' Life support value = {str_to_binary(oxygen_gen_rating) * str_to_binary(co2_scrubber_rating)}')
