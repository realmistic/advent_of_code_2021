# https://github.com/folded/aoc-2021/tree/main/23
#  working solution!

import sys
import numpy as np
import itertools
import dataclasses
import heapq
from typing import Optional


@dataclasses.dataclass
class Amphipod:
    a: str
    y: int
    x: int

    def __repr__(self):
        return f'<{self.a}:{self.y},{self.x}>'

    @property
    def idx(self):
        return ord(self.a) - ord('A')

    @property
    def target(self):
        return self.idx * 2 + 3

    @property
    def in_room(self):
        return self.y > 1

    @property
    def step_cost(self):
        return 10 ** self.idx

    @property
    def in_correct_room(self):
        return self.in_room and self.x == self.target

    def move_cost(self, y, x):
        return (abs(y - self.y) + abs(x - self.x)) * self.step_cost


def amphipods(layout):
    for y, x in itertools.product(range(layout.shape[0]),
                                  range(layout.shape[1])):
        if layout[y, x] in 'ABCD':
            yield Amphipod(layout[y, x], y, x)


def is_solved(layout):
    return all(a.in_correct_room for a in amphipods(layout))


def to_corridor_moves(layout, amphipod):
    assert amphipod.in_room
    y = amphipod.y - 1
    while y != 1:
        if layout[y, amphipod.x] != '.':
            return
        y -= 1
    for x in range(amphipod.x + 1, 12):
        if layout[1, x] != '.': break
        if x in (3, 5, 7, 9):
            continue
        yield amphipod, (1, x)
    for x in range(amphipod.x - 1, 0, -1):
        if layout[1, x] != '.':
            break
        if x in (3, 5, 7, 9): continue
        yield amphipod, (1, x)


def to_room_moves(layout, amphipod):
    assert not amphipod.in_room
    x = amphipod.x
    dx = -1 if amphipod.target < x else +1
    while x != amphipod.target:
        x += dx
        if layout[1, x] != '.': return

    moves = []
    y = 2
    room_contents = set(layout[2:-1, x])
    if len(room_contents - {'.', amphipod.a}):
        return
    while layout[y, x] == '.':
        yield amphipod, (y, x)
        y += 1


def generate_moves(layout):
    for amphipod in amphipods(layout):
        if amphipod.in_room:
            yield from to_corridor_moves(layout, amphipod)
        else:
            yield from to_room_moves(layout, amphipod)


def apply_move(layout, move):
    amphipod, (y, x) = move
    cost = amphipod.move_cost(y, x)
    layout = np.array(layout)
    layout[amphipod.y, amphipod.x] = '.'
    layout[y, x] = amphipod.a
    return cost, layout


def h(layout):
    c = 0
    for a in amphipods(layout):
        if a.in_correct_room:
            continue
        elif a.in_room:
            c += (a.y + abs(a.target - a.x)) * a.step_cost
        else:
            c += (1 + abs(a.target - a.x)) * a.step_cost
    return c


def layout_str(layout):
    return '\n'.join(''.join(row) for row in layout)


@dataclasses.dataclass(order=True)
class State:
    astar_cost: int
    cost: int
    layout: np.ndarray = dataclasses.field(compare=False)
    prev_state: Optional['State'] = dataclasses.field(default=None,
                                                      compare=False)

    def __repr__(self):
        return f'cost={self.cost}\nlayout:\n{layout_str(self.layout)}\n'


def solve(layout):
    visited = set()
    n_pruned = 0

    state_queue = [State(h(layout), 0, layout)]
    visited.add(layout_str(layout))
    while len(state_queue):
        state = heapq.heappop(state_queue)
        if is_solved(state.layout):
            return state
        for move in generate_moves(state.layout):
            move_cost, new_layout = apply_move(state.layout, move)
            key = layout_str(new_layout)
            if key in visited:
                n_pruned += 1
                continue
            visited.add(key)
            if len(visited) % 10000 == 0:
                n_states = len(visited)
                print(
                    f'n_states={n_states} n_pruned={n_pruned} ratio={n_pruned / n_states:.2f}'
                )

            heapq.heappush(
                state_queue,
                State(state.cost + move_cost + h(new_layout), state.cost + move_cost,
                      new_layout, state))

    return None

text_file = open('../inputs/day23/input2.txt', 'r')
field = text_file.read().splitlines()

layout = np.array([list(line.rstrip('\n')) for line in field]) #sys.stdin


def output(state):
    if not state:
        return
    output(state.prev_state)
    print(state)


output(solve(layout))
