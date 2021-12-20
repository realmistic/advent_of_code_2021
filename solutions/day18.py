# Used some of this code: https://topaz.github.io/paste/#XQAAAQC8DgAAAAAAAAA6HIjg3LGCK4sYAkLOl3QSFTz/6DV6kEb4w9fzfZNTNhwUUqs6C0AvKg92LEU4HgLkCelXldj9ObeRxl6FZsXfxumKYisOUPYxrkttM591b2HRi2orIOzHsEjM9YLRVzlxBaBF8tZq7kNC6IK/waxn2GA9gjytECkOTzvAS7aTwY8wNnoBdLy0dNzVn1djwle9FEJo4/qEnOSlRd7CqptTHtoqr5+tiuDu3PQRFR4BXFXfuRsjx3Kn/SzydaNb0jOrxoHTg9VKUbhOcekYlda8dG4Ik8w8pOvc8xiI+kKzgoAopOm/ZCfZiEXL8EVQdBfOKPuUjV6X/FNhEKGSaw+LDnFgrWWlx6Xm77YQllBC4cHhyG+BHJpilaAPWPpoZFbvSs3BzZ3bB1iTqnFlLZkqjzYoMjQ9HSIEhA65PZJaknLdes3awWoBL3nstJzW0iwi6aO1Y51th7uN7YjyuH0pN54uikNE1E+DEonj3t+aMy23pB3qmtNYipxdfhO8Sxb2E/5pEaXOfzCs1LlDgVloGoVIBRvX/edt93SPNyIgSLHlh0OQfBnxDWvncNIzOF52DgDSDJ+NM6Eq8H/tQVbietrFRvYIYBbOhLXMrTDzHpTY6sR9xeNYskgf0QLoz0/hugS5UxPRY1RhUd7JFXlXS1p3QsBFT+4Ikp3lBcQJ1VLHTKya9opeftbabeASZP3OhP5OHHmO1I/mwpkKNeWDC0LTh5BYN11oYoLL29f0U5Ivd1I+kerybyaxmF64r2FbVrljDl89LPG+kq/uyswgGFmfwljffehAJeBoazAjybVKotvv9OabbeCGq2/lgEBMvd/MxSvUYGpeqT7FsfdBMo+K8FN3I/G+VySrrdQrycrjFqdnrJzQmN5gTV1qDOZHynNnANHHFJTASX52A53v9i4ZLsA2VFJb/5QMFFHceVDjdpSWLKkWUbT9yo8suBZtWCrIObCEQ367UodP/s1qLrl4Y+kMlWm4dAQpjOIcSFrwAVIbQKb87/ZBWxM8UVg2Cw14G5okDyqC6C5mEzQ8GRQYiYmvnmycRC5Z/K0ojhWNRQnimgL+4UieD3RuU8RyvYMk7FxcDzN4Ekgd9EDYjcpbfBe9S82Mm5eE4Re2TycG/RtGt0WpjnhYgKC9KKdbmCaZzAHAN83C7J+aPkDoejv2GnXzdEppObVB896R762lkd8owX4Ic6K+tO6VNIw4eVVDdc2tmJUQ4q84I7K9P2tfxKbHYnEDBBgxHRPWoS13qnZXcGcth0HKu0LQaitYI89Mt97HW+Xa7oS8GozUzWOLQw5aUtrq8HWTbqwofZV/4rctHyGqN+IJ9bX0wL/QlSEx58YX4+jhZpLuKkoLnwO7fHD78jFR9HZnm5EY3QncfWV6oV+HZbV67KzZlYyQ8fbzcNYflWamtKmXfBAgXd0jYnJdoi8ud9ttnTJTSo0S2uvKY27Z3Ay1QBr2JQPUoL8Lu8qyqfHrcdt6Dsv/NwIBfexnhKr+o+zeUxsFYqxyOJaeSLBOTbGkzicLdjeXfZn1uuAzQl5WcLupR19/DcD7BaaZF74p/j+g5g0MkusICDSpF9DW9iivRJi3N3o8qdfNEQS6A5++9IiFtBZQSMTmtBAAb2G87Vab3oKZA2l8xFQi++v/7vedFA==
from typing import Optional


class Node:
    # key == Value for the leaf node,
    def __init__(self, key: int, parent=None):
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.val: int = key
        self.parent: Node = parent

    def __str__(self):
        if self.val is not None:
            return f'{self.val}'
            # return f'{self.val}'
        else:
            return f'({self.left},{self.right})'


# -- find the next elem after the closing bracket
def find_closing_elem(str_, pos):
    if str_[pos] != '[':
        return str_.find(',')
    open_brackets = 1
    cur = pos
    while open_brackets > 0:
        cur += 1
        if str_[cur] == '[':
            open_brackets += 1
        elif str_[cur] == ']':
            open_brackets -= 1
    return cur + 1


# start_pos = position of the sub_tree in the original string
def build_tree(str_):
    rez = Node(None)
    if str_.count('[') == 0:
        rez = Node(int(str_))
    elif str_.count('[') == 1:
        l_value = int(str_[1:-1].split(',')[0])
        r_value = int(str_[1:-1].split(',')[1])
        rez.left = Node(l_value)
        rez.right = Node(r_value)
    else:
        comma_pos = find_closing_elem(str_, 1)
        rez.left = build_tree(str_[1:comma_pos])
        rez.right = build_tree(str_[comma_pos + 1:-1])
    return rez


def get_right_closest_val(cur_node: Node) -> Optional[Node]:
    if cur_node is None: return None
    if cur_node.parent is None: return None
    if cur_node == cur_node.parent.right:
        return get_right_closest_val(cur_node.parent)
    n = cur_node.parent.right
    while n.left is not None:
        n = n.left
    return n


def get_left_closest_val(cur_node: Node) -> Optional[Node]:
    if cur_node is None: return None
    if cur_node.parent is None: return None
    if cur_node == cur_node.parent.left:
        return get_left_closest_val(cur_node.parent)
    n = cur_node.parent.left
    while n.right is not None:
        n = n.right
    return n


def get_node_to_explode(cur_node: Node, depth: int = 4) -> Optional[Node]:
    if depth == 0 and cur_node.val is None:
        return cur_node
    if cur_node.left is not None:
        gl = get_node_to_explode(cur_node.left, depth - 1)
        if gl: return gl
    if cur_node.right is not None:  # only after all left subtrees
        gr = get_node_to_explode(cur_node.right, depth - 1)
        if gr: return gr
    return None


def explode(cur_node: Node):  # the leftmost pair at depth>=4
    e = get_node_to_explode(cur_node, 4)
    if e is None:
        return False  # Nothing to explode

    closest_left = get_left_closest_val(e.left)
    if closest_left is not None:
        closest_left.val += e.left.val

    closest_right = get_right_closest_val(e.right)
    if closest_right is not None:
        closest_right.val += e.right.val

    print(f'Perform explode')
    e.left = None
    e.right = None
    e.val = 0

    return True  # there was an explode


def split(cur_node: Node):
    if cur_node.val and cur_node.val >= 10:
        print(f'Perform split')
        cur_node.left = Node(int(cur_node.val / 2))
        cur_node.left.parent = cur_node
        cur_node.right = Node(int((cur_node.val + 1) / 2))
        cur_node.right.parent = cur_node
        cur_node.val = None
        return True  # there was a split

    if cur_node.left is not None:
        sl = split(cur_node.left)
        if sl: return sl

    if cur_node.right is not None:
        sr = split(cur_node.right)
        if sr: return sr

    return False


def update_parent_links(subTree: Node):
    if subTree.left is not None:
        subTree.left.parent = subTree
        update_parent_links(subTree.left)
    if subTree.right is not None:
        subTree.right.parent = subTree
        update_parent_links(subTree.right)
    return None


def add_trees(root_left: Node, root_right: Node) -> Node:
    r = Node(None, None)
    root_left.parent = r
    root_right.parent = r
    r.left = root_left
    r.right = root_right
    return r  # new root


def get_magnitude(node: Node) -> int:
    if node is None:
        return 0
    if node.val is not None:
        return node.val
    else:
        return 3 * get_magnitude(node.left) + 2 * get_magnitude(node.right)


def read_stats():
    text_file = open('../inputs/day18/input.txt', 'r')
    lines_ = text_file.read().splitlines()
    return lines_


lines = read_stats()

root = build_tree(lines[0])
update_parent_links(root)
print(f'Initial first line: {root}')
for line in lines[1:]:
    root = add_trees(root, build_tree(line))
    print(f'New tree after adding: {root}')
    update_parent_links(root)
    while explode(root) or split(root):
        print(f'Performed split or explode {root}')
        update_parent_links(root)
        continue
    print(f'Reduced tree: {root}')
    print('-------')

print(f'PART1: Final magnitude: {get_magnitude(root)}')

max_magnitude = 0
for a in lines:
    for b in lines:
        if a != b:
            root = add_trees(build_tree(a), build_tree(b))
            update_parent_links(root)
            while explode(root) or split(root):
                print(f'Performed split or explode {root}')
                update_parent_links(root)
                continue
            print(f'Reduced tree: {root}')
            print('-------')
            cur_magnitude = get_magnitude(root)
            if cur_magnitude > max_magnitude:
                max_magnitude = cur_magnitude
print(f'PART 2: max pair magnitude: {max_magnitude}')