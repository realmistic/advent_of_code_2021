import numpy as np


def read_stats():
    text_file = open('../inputs/day14/input.txt', 'r')
    lines = text_file.read().splitlines()

    original_formula = lines[0]
    rules = []
    rules_dict = {}
    for line in lines[2:]:
        part0 = line.split(' -> ')[0]
        part1 = line.split(' -> ')[1]
        rules.append((part0, part1))
        rules_dict[part0] = part1
    return original_formula, rules, rules_dict


template, rules, rules_dict = read_stats()

print(f'Template = {template}')
print(f'Rules = {rules}')


def perform_insertion(current_str):
    new_str = ''
    for i in range(len(current_str) - 1):
        pattern = current_str[i:i + 2]
        wide_pattern = pattern[1:]
        for rule in rules:
            if rule[0] == pattern:
                wide_pattern = rule[1] + pattern[1:]
        if i == 0:
            wide_pattern = pattern[:1] + wide_pattern
        new_str = new_str + wide_pattern
    return new_str

cur_str = template
for step in range(10):
    print(f'Step number ={step}, current len of str = {len(cur_str)}')
    cur_str = perform_insertion(cur_str)
    if step<3:
        print(cur_str)

print(f'After 10 steps length: {len(cur_str)}')
print(f' Set of chars after 10 steps: {set(cur_str)}')

max_count = 0
min_count = len(cur_str)
for char in set(cur_str):
    count_cur_char = cur_str.count(char)
    if count_cur_char > max_count:
        max_count = count_cur_char
    if count_cur_char < min_count:
        min_count = count_cur_char
    print(f' Char {char} count is : {cur_str.count(char)}')

print(f'Max-min count: {max_count - min_count}')
print('=======================================')

# step0
step0_rules_count = {}
first_rule = ''
last_rule = ''
for i in range(len(template) - 1):
    pattern = template[i:i + 2]
    for rule in rules:
        if rule[0] == pattern:
            if rule[0] in step0_rules_count.keys():
                step0_rules_count[rule[0]] += 1
            else:
                step0_rules_count[rule[0]] = 1
            if i == 0:
                first_rule = rule[0]
            if i == len(template) - 2:
                last_rule = rule[0]
print(f'Initial rules count: {step0_rules_count}')
print(f'First rule = {first_rule}, last rule = {last_rule}')

def get_max_min_chars(char_count_dict):
    any_key = list(char_count_dict.keys())[0]
    min_ = char_count_dict[any_key]
    max_ = char_count_dict[any_key]

    for char in char_count_dict.keys():
        if char_count_dict[char] < min_:
            min_ = char_count_dict[char]
        if char_count_dict[char] > max_:
            max_ = char_count_dict[char]
    return min_, max_

def calc_chars_count(curStep_rules_count):
    rez = {}
    for rule in curStep_rules_count:
        if rule[0] in rez.keys():
            rez[rule[0]] += curStep_rules_count[rule]
        else:
            rez[rule[0]] = curStep_rules_count[rule]

    if last_rule[1] in rez.keys():
        rez[last_rule[1]] += 1
    else:
        rez[last_rule[1]] = 1
    return rez


def perform_advanced_insertion(curStep_rules_count):
    newStep_rules_count = {}
    changed_first = False
    changed_last = False
    for elem in curStep_rules_count.keys():
        if elem in rules_dict.keys():
            rule1 = elem[0] + rules_dict[elem]
            rule2 = rules_dict[elem] + elem[1]

            if rule1 in newStep_rules_count.keys():
                newStep_rules_count[rule1] += curStep_rules_count[elem]
            else:
                newStep_rules_count[rule1] = curStep_rules_count[elem]

            if rule2 in newStep_rules_count.keys():
                newStep_rules_count[rule2] += curStep_rules_count[elem]
            else:
                newStep_rules_count[rule2] = curStep_rules_count[elem]

            # newStep_rules_count[elem] = 0
            global first_rule
            global last_rule
            if elem == first_rule and not changed_first:
                first_rule = rule1
                changed_first = True
            if elem == last_rule and not changed_last:
                last_rule = rule2
                changed_last = True
        else:
            if elem in newStep_rules_count.keys():
                newStep_rules_count[elem] += curStep_rules_count[elem]
            else:
                newStep_rules_count[elem] = curStep_rules_count[elem]

    return newStep_rules_count


cur_rules_count = step0_rules_count
for step in range(40):
    print(f'Step {step+1}')
    cur_rules_count = perform_advanced_insertion(cur_rules_count)
    print(cur_rules_count)
    print(f'First rule = {first_rule}, last rule = {last_rule}')
    cur_char_count = calc_chars_count(cur_rules_count)
    print(f' Chars counts: {cur_char_count}')
    min_ch, max_ch = get_max_min_chars(cur_char_count)
    print(f' Min chars = {min_ch}, max chars = {max_ch}, max-min = {max_ch-min_ch}')
    print('------------------')


# def get_chars_count(rules_count, first_rule, last_rule):
