import statistics
text_file = open('../inputs/day10/input.txt', 'r')

def get_completion_line(stack):
    closing_line = ''
    mapping_open_close = {'[' : ']',
                          '(':')',
                          '<':'>',
                          '{':'}'
                          }
    for elem in reversed(stack):
        closing_line = closing_line + mapping_open_close[elem]
    return closing_line

def analyse_line(line):
    stack = []
    open_chars = {'[', '(', '<', '{'}
    close_chars = {']', ')', '>', '}'}
    mapping_brackets = {']': '[',
                        '}': '{',
                        '>': '<',
                        ')': '('}

    for elem in line:
        if elem in open_chars:
            stack.append(elem)
        elif elem in close_chars:
            opened_elem = stack.pop()  # bad seq open->close
            if mapping_brackets[elem] != opened_elem:
                return elem
        else:
            raise Exception(f'Bad char {elem}')

    if len(stack) > 0:  # not completed line
        return get_completion_line(stack)
    return '0'


def get_completion_fine(completion_line):
    fine = 0
    mapping_points = {']': 2,
                     '}': 3,
                     '>': 4,
                     ')': 1}
    for elem in completion_line:
        fine = fine * 5 + mapping_points[elem]
    return fine

lines = text_file.read().splitlines()

mapping_fines = {']': 57,
                 '}': 1197,
                 '>': 25137,
                 ')': 3}

rez = 0
arr_fines = []

for line in lines:
    # print(line)
    one_line_outcome = analyse_line(line)
    # Part1
    if one_line_outcome in mapping_fines.keys():
        rez += mapping_fines[one_line_outcome]
    # Part2 if
    if len(one_line_outcome) > 1:
        print(f' Line to complete: {one_line_outcome} and fine = {get_completion_fine(one_line_outcome)}')
        arr_fines.append(get_completion_fine(one_line_outcome))

print(f'Total fines (Part1) {rez}')
print(f'Fines arr: {arr_fines}')
print(f'Middle point is (Part2 ans): {statistics.median(sorted(arr_fines))}')