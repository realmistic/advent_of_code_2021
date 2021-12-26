# Source for the solution: https://pastebin.com/EpS1CyPd
# PART1 solution only!!

from pprint import pprint
from sys import exit


def heron(a, b, c):
    s = (a + b + c) / 2
    a = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    return a


def dist3d(x, y, z, x2, y2, z2):
    a = (x - x2) ** 2 + (y - y2) ** 2 + (z - z2) ** 2
    d = a ** 0.5
    return d


def get_triangle_properties(p1, p2, p3):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    a = dist3d(x1, y1, z1, x2, y2, z2)
    b = dist3d(x2, y2, z2, x3, y3, z3)
    c = dist3d(x3, y3, z3, x1, y1, z1)
    area = heron(a, b, c)
    return (area), (a + b + c)


def compute_fingerprints(group):
    n = len(group)
    fingerprints = []

    # Calculate distance of a point to every other point
    for i in range(n):
        distances = []
        x, y, z = group[i]
        m1, d1, m2, d2 = 0, 3001, 1, 3001
        for j in range(n):
            if i == j: continue
            x2, y2, z2 = group[j]
            d = abs(x - x2) + abs(y - y2) + abs(z - z2)
            if d < d1:
                if d2 > d1:
                    m2, d2 = m1, d1
                m1, d1 = j, d
            elif d < d2:
                m2, d2 = j, d
        # Compute fingerprint for current point
        p1, p2, p3 = group[i], group[m1], group[m2]
        area, perimeter = get_triangle_properties(p1, p2, p3)
        fingerprints.append((area, perimeter))

    return fingerprints


def cross_prod(v1, v2, third_axis):
    # Construct vector matrix
    a = [0, 0, 0]
    b = [0, 0, 0]
    a['xyz'.index(v1[-1])] = 1
    if v1[0] == '-': a['xyz'.index(v1[-1])] *= -1
    b['xyz'.index(v2[-1])] = 1
    if v2[0] == '-': b['xyz'.index(v2[-1])] *= -1
    mat = [a, b]
    # Cross Product
    c = [0, 0, 0]
    for i in range(3):
        cs = list({0, 1, 2} - {i})
        x, y = min(cs), max(cs)
        c[i] = mat[0][x] * mat[1][y] - mat[0][y] * mat[1][x]
    c[1] *= -1
    # Figure out sign for third axis
    third_side_sign = ''
    if c['xyz'.index(third_axis)] < 0:
        third_side_sign = '-'
    # Return the third side
    return third_side_sign + third_axis


# Compute all orientations
orientations = []
for f in ('x', 'y', 'z'):
    for fs in ('-', ''):
        face = fs + f
        # Up Side
        for u in ('x', 'y', 'z'):
            if u == f: continue
            for us in ('-', ''):
                up = us + u
                # Calculate sign of third side using vector cross product
                third = cross_prod(face, up, ({'x', 'y', 'z'} - {f} - {u}).pop())
                orientations.append((face, up, third))

print(len(orientations), "orientations computed.")


def map_to_orientation(coords, orientation):
    new_coords = []
    for o in orientation:
        si = +1
        if len(o) > 1:
            si = -1
        if o[-1] == 'x':
            new_coords.append(coords[0] * si)
        elif o[-1] == 'y':
            new_coords.append(coords[1] * si)
        else:
            new_coords.append(coords[2] * si)
    # Return mapped coordinates
    return new_coords


def match_orientation(g, g2, x, y):
    g_set = set(g)
    px = g[x]
    # Check all orientations
    for orientation in orientations:
        # Map one point from g2 to current orientation to compute delta
        py = map_to_orientation(g2[y], orientation)
        # Compute Delta
        dx, dy, dz = px[0] - py[0], px[1] - py[1], px[2] - py[2]
        # Check all points
        matches = 0
        for i in range(len(g2)):
            op = map_to_orientation(g2[i], orientation)
            op = (op[0] + dx, op[1] + dy, op[2] + dz)
            if op in g_set:
                matches += 1
                if matches >= 12:
                    return True, orientation, (dx, dy, dz)
    # No matches found
    return False, None, None


def combine_groups(groups):
    n = len(groups)
    print(f"Combining {n} groups.")

    # Compute Fingerprints of all groups
    fingerprints = []
    for group in groups:
        fingerprints.append(compute_fingerprints(group))

    # Compute neighbours
    neighbours = []
    for i in range(n):
        neighbours.append([])
        for j in range(i + 1, n):
            it = set(fingerprints[i]).intersection(set(fingerprints[j]))
            if len(it):  # Rough estimate 4
                neighbours[-1].append(j)

    # Combine groups with neighbour groups
    is_taken = [False] * n
    for i in range(n - 1, -1, -1):
        # Try to combine all neighbours of this group
        for j in neighbours[i]:
            if is_taken[j]: continue
            # Get matching point using fingerprints
            matches = []
            fp, fp2 = fingerprints[i], fingerprints[j]
            for x in range(len(fp)):
                for y in range(len(fp2)):
                    if fp[x] == fp2[y]:
                        matches.append((x, y))
                        break
            # Try to combine from matched points
            matched_orientation = None
            for x, y in matches:
                is_matched, matched_orientation, deltas = match_orientation(groups[i], groups[j], x, y)
                if is_matched: break
                # If matched, combine with ith group
            if not is_matched:
                continue
            ds = deltas  # Shorthand
            for point in groups[j]:
                # Convert point
                p = map_to_orientation(point, matched_orientation)
                op = (p[0] + ds[0], p[1] + ds[1], p[2] + ds[2])
                groups[i].append(op)
            # Label current group as 'taken' so it is removed in next iteration
            is_taken[j] = True

    # Remove used groups
    new_groups = []
    for i in range(n):
        if is_taken[i] == False:
            new_groups.append(list(set(groups[i])))

    if len(new_groups) == 1:
        return new_groups[0]
    else:
        return combine_groups(new_groups)


if __name__ == "__main__":

    with open("../inputs/day19/input.txt", 'r') as f:
        data = f.read().strip()

    data = data.split('\n\n')

    groups = []
    for d in data:
        group = d.strip().split('\n')[1:]
        group = [tuple(map(int, ls.split(','))) for ls in group]
        groups.append(group)

    print("Total", len(groups), "groups.")

    main_group = combine_groups(groups)
    print("Final group length:", len(main_group))