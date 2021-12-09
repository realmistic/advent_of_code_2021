text_file = open('../inputs/day8/input.txt', 'r')

lines = text_file.read().splitlines()


def get_mapping(arr_before):
    rez = {}

    for elem in arr_before:
        if len(elem) == 2:
            rez[1] = elem
        if len(elem) == 3:
            rez[7] = elem
        if len(elem) == 4:
            rez[4] = elem
        if len(elem) == 7:
            rez[8] = elem

    for elem in arr_before:
        if len(elem) == 5 and (set(rez[4])-set(elem) == set(rez[7])-set(elem)):
            # set(rez[1]).issubset(set(elem)):
            rez[5] = elem

    for elem in arr_before:
        if (len(elem) == 6) and (set(rez[5]).issubset(set(elem))) and (not set(rez[1]).issubset(set(elem))):
            rez[6] = elem

    for elem in arr_before:
        if len(elem) == 6 and set(rez[4]).issubset(set(elem)):
            rez[9] = elem

    for elem in arr_before:
        if len(elem) == 6 and elem != rez[6] and elem != rez[9]:
            rez[0] = elem
        if len(elem) == 5 and set(set(elem)).issubset(rez[9]) and elem != rez[5]:
            rez[3] = elem

    left_down_signal = set(rez[8]) - set(rez[9])

    for elem in arr_before:
        if len(elem) == 5 and left_down_signal.issubset(set(elem)):
            rez[2] = elem


    # mapping = {y:x for x,y in rez.iteritems()}
    mapping = {rez[k]: k for k in rez}

    return mapping


def seq_in_mapping(seq, mapping):
    for elem in mapping:
        if set(mapping[elem]) == set(seq):
            return True
    return False


sum = 0

for line in lines:
    part_before, part_after = line.split('|')
    # print(part_before)
    # print(part_after)
    arr_before = part_before.strip().split(' ')
    arr_after = part_after.strip().split(' ')
    print(line)
    # print(arr_before)
    # print(arr_after)

    mapping = get_mapping(arr_before)
    # print(set(mapping[8]) - set(mapping[9]))
    print(mapping)

    pow = 1000
    num = 0
    for seq in arr_after:
        for i in mapping.keys():
            if set(seq) == set(i) and len(set(seq)) == len(set(i)):
                num += mapping[i] * pow
                pow /= 10
    print(num)
    sum += num
print(sum)
