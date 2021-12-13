import numpy as np
import pandas as pd

text_file = open('../inputs/day12/input.txt', 'r')
lines = text_file.read().splitlines()


def check_small_caves(path, vertexes):
    one_small_cave_double = False
    for v in vertexes:
        if v.islower() and path.count(','+v) > 1:
            if one_small_cave_double: # >1 small caves visited twice
                return False
            else:
                one_small_cave_double = True
    return True

vertexes = set()

for line in lines:
    v_start, v_end = line.split('-')
    print(v_start, v_end)
    vertexes.add(v_start)
    vertexes.add(v_end)

print(vertexes)

df = pd.DataFrame([], index=vertexes, columns=vertexes)

for line in lines:
    v_start, v_end = line.split('-')
    df.at[v_start, v_end] = 1
    df.at[v_end, v_start] = 1

df.replace(to_replace=np.nan, value=0, inplace=True)

print(f'Adj. matrix: \n {df}')

# path with 0 len
queue = ['start']

total_paths = 0

while len(queue) > 0:
    next_step_queue = []
    for path in queue:
        v_start = path.split(',')[-1]  # last vertex in the path
        for v_end in vertexes:
            if df.at[v_start, v_end]:
                # if v_end.islower() and path.find(v_end) > -1:  # Part1: continue if lower and is already in the path
                if v_end.islower() and (path.count(','+v_end) > 1 or v_end == 'start'):  # Part2: can't have paths with >1 occurences of v_end
                    continue
                if not check_small_caves(path, vertexes): # early stage bad paths
                    continue
                cur_path = path + ',' + v_end
                if v_end == 'end' and check_small_caves(cur_path, vertexes):
                    # DEBUG: print(cur_path)
                    total_paths += 1
                    if total_paths % 1000 == 0:
                        print(total_paths)
                else:
                    next_step_queue.append(cur_path)
    queue = next_step_queue

print(f'Total paths = {total_paths}')
