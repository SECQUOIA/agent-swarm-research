"""Exact adversarial fixtures for scalar copositive block elimination.

Exercises singular supports, branching, long rational lifts, and early
private-block failure. This is a focused reference diagnostic.
"""

from fractions import Fraction as Q
from itertools import combinations


def solve(matrix, rhs):
    n = len(rhs)
    a = [list(map(Q, row)) + [Q(value)] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next((i for i in range(column, n) if a[i][column]), None)
        if pivot is None:
            return None
        a[column], a[pivot] = a[pivot], a[column]
        scale = a[column][column]
        a[column] = [x / scale for x in a[column]]
        for i in range(n):
            if i != column:
                scale = a[i][column]
                a[i] = [x - scale * y for x, y in zip(a[i], a[column])]
    return [row[-1] for row in a]


def value(matrix, x):
    return sum(x[i] * a * x[j] for i, row in enumerate(matrix) for j, a in enumerate(row))


def supports(n):
    for size in range(1, n + 1):
        yield from combinations(range(n), size)


def simplex_min(matrix):
    n = len(matrix)
    candidates = []
    for support in supports(n):
        bordered = [[matrix[i][j] for j in support] + [Q(-1)] for i in support]
        bordered.append([Q(1)] * len(support) + [Q(0)])
        stationary = solve(bordered, [Q(0)] * len(support) + [Q(1)])
        if stationary is None or any(x < 0 for x in stationary[:-1]):
            continue
        point = [Q(0)] * n
        for i, x in zip(support, stationary[:-1]):
            point[i] = x
        assert sum(point) == 1
        assert value(matrix, point) == stationary[-1]
        candidates.append((stationary[-1], point))
    return min(candidates, key=lambda item: item[0])


def recourse(matrix, linear):
    n = len(matrix)
    candidates = [(Q(0), [Q(0)] * n)]
    for support in supports(n):
        stationary = solve([[matrix[i][j] for j in support] for i in support],
                           [-linear[i] for i in support])
        if stationary is None or any(x < 0 for x in stationary):
            continue
        point = [Q(0)] * n
        for i, x in zip(support, stationary):
            point[i] = x
        objective = value(matrix, point) + 2 * sum(x * b for x, b in zip(point, linear))
        candidates.append((objective, point))
    return min(candidates, key=lambda item: item[0])


def eliminate(original, order):
    current = [row[:] for row in original]
    active = set(range(len(original)))
    records = []

    def fail(indices, point):
        full = [Q(0)] * len(original)
        for i, x in zip(indices, point):
            full[i] = x
        for private, parent, vector in reversed(records):
            for i, x in zip(private, vector):
                full[i] = full[parent] * x
        assert any(full) and all(x >= 0 for x in full)
        assert value(original, full) <= 0
        return False, full, records

    for private, parent in order:
        assert set(private) <= active and parent in active - set(private)
        assert all(current[i][j] == 0 for i in private for j in active - set(private) - {parent})
        block = [[current[i][j] for j in private] for i in private]
        minimum, witness = simplex_min(block)
        if minimum <= 0:
            return fail(private, witness)
        alpha, vector = recourse(block, [current[i][parent] for i in private])
        assert alpha <= 0
        current[parent][parent] += alpha
        active -= set(private)
        records.append((private, parent, vector))
    root = sorted(active)
    minimum, witness = simplex_min([[current[i][j] for j in root] for i in root])
    if minimum <= 0:
        return fail(root, witness)
    return True, None, records


def zero_matrix(n):
    return [[Q(0)] * n for _ in range(n)]


def add_square(matrix, terms):
    for i, a in terms.items():
        for j, b in terms.items():
            matrix[i][j] += a * b


def check_star(blocks, delta):
    # Sum_b (u_b+v_b-r_b*s)^2 + delta*s^2.
    matrix = zero_matrix(2 * blocks + 1)
    matrix[0][0] = delta
    for block in range(blocks):
        add_square(matrix, {0: -Q(block + 2, block + 3), 2 * block + 1: Q(1), 2 * block + 2: Q(1)})
    order = [([2 * block + 1, 2 * block + 2], 0) for block in reversed(range(1, blocks))]
    positive, witness, records = eliminate(matrix, order)
    assert positive == (delta > 0)
    assert len(records) == blocks - 1
    if blocks <= 2:
        assert (simplex_min(matrix)[0] > 0) == positive
    return int(witness is not None)


def check_chain(length, delta):
    matrix = zero_matrix(length + 1)
    ratio = Q(2, 3)
    for i in range(length):
        add_square(matrix, {i: Q(1), i + 1: -ratio})
    matrix[-1][-1] += delta
    positive, witness, records = eliminate(matrix, [([i], i + 1) for i in range(length - 1)])
    assert positive == (delta > 0)
    assert len(records) == length - 1
    if witness is not None:
        assert max(max(x.numerator.bit_length(), x.denominator.bit_length()) for x in witness) <= 4 * length + 100
        if delta == 0:
            assert all(witness[i] == ratio * witness[i + 1] for i in range(length))
    return int(witness is not None)


def check_early_failure():
    matrix = [[Q(x) for x in row] for row in
              [[5, -1, 1, -2], [-1, 1, 1, 0], [1, 1, 1, 0], [-2, 0, 0, 1]]]
    positive, witness, records = eliminate(matrix, [([3], 0), ([0, 1], 2)])
    assert not positive and len(records) == 1
    assert witness[2] == 0 and witness[3] == 2 * witness[0]
    assert value(matrix, witness) == 0


if __name__ == "__main__":
    ones = [[Q(1), Q(1)], [Q(1), Q(1)]]
    assert simplex_min(ones)[0] == 1
    assert recourse(ones, [Q(-1), Q(-1)])[0] == -1
    # A feasible stationary saddle must not be mistaken for the minimum.
    assert recourse([[Q(1), Q(2)], [Q(2), Q(1)]], [Q(-1), Q(-1)])[0] == -1
    assert simplex_min([[Q(0), Q(0)], [Q(0), Q(1)]])[0] == 0
    witnesses = 0
    for delta in (Q(1, 2**80), Q(0), Q(-1, 100)):
        for blocks in (1, 2, 9, 64):
            witnesses += check_star(blocks, delta)
        for length in (2, 17, 64):
            witnesses += check_chain(length, delta)
    check_early_failure()
    print(f"PASS: 4 singular/saddle support cases; 12 articulation stars; "
          f"9 rational chains; {witnesses} exact lifted witnesses; "
          "1 early private-block failure with reverse lift.")
