"""Exact independent checks for the observed-rank elimination theorem.

Run: python code/network_simplex_review/verify_observed_rank.py
Requires SymPy. This is a rank/elimination test, not an LP or novelty test.
"""

import random
from itertools import combinations

from sympy import Matrix, eye, zeros


def forest_edges(nodes, arcs, selected):
    parent = list(range(nodes))

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    forest, chords = [], []
    for e in selected:
        a, b = arcs[e]
        ra, rb = find(a), find(b)
        if ra == rb:
            chords.append(e)
        else:
            parent[ra] = rb
            forest.append(e)
    return forest, chords


def cycle_matrix(nodes, arcs):
    tree, chords = forest_edges(nodes, arcs, range(len(arcs)))
    assert len(tree) == nodes - 1
    a = zeros(nodes, len(arcs))
    for e, (tail, head) in enumerate(arcs):
        a[tail, e] -= 1
        a[head, e] += 1
    reduced = a[:-1, :]
    top = -reduced[:, tree].inv() * reduced[:, chords] if nodes > 1 else zeros(0, len(chords))
    c = zeros(len(arcs), len(chords))
    for i, e in enumerate(tree):
        c[e, :] = top[i, :]
    for i, e in enumerate(chords):
        c[e, i] = 1
    assert a * c == zeros(nodes, len(chords))
    return c


def check(nodes, arcs, observed, rng):
    c = cycle_matrix(nodes, arcs)
    r = c.cols
    observed = list(observed)
    observed_matrix = c[observed, :] if observed else zeros(0, r)
    _, independent = observed_matrix.T.rref()
    selected = [observed[i] for i in independent]
    d = len(selected)
    unobserved = [e for e in range(len(arcs)) if e not in observed]
    _, missing_chords = forest_edges(nodes, arcs, unobserved)
    assert r - d == len(missing_chords)
    # Completing with nonforest unobserved arcs supplies full observation rank.
    completion = observed + missing_chords
    assert c[completion, :].rank() == r if completion else r == 0
    if not d:
        return
    D = c[selected, :]
    _, pivots = D.rref()
    free = [i for i in range(r) if i not in pivots]
    b = D[:, pivots]
    assert b.det() in (-1, 1)
    W = c[:, pivots] * b.inv()
    R = c[:, free] - W * D[:, free]
    assert all(entry in (-1, 0, 1) for entry in W)
    assert all(entry in (-1, 0, 1) for entry in R)
    h = Matrix([rng.randint(-7, 7) for _ in range(r)])
    q = D * h
    g = h[free, :] if free else zeros(0, 1)
    assert W * q + R * g == c * h
    # Check the converse without taking q from a preexisting state vector.
    q2 = Matrix([rng.randint(-7, 7) for _ in range(d)])
    g2 = Matrix([rng.randint(-7, 7) for _ in free]) if free else zeros(0, 1)
    recovered = zeros(r, 1)
    pivot_values = b.inv() * (q2 - D[:, free] * g2)
    for i, column in enumerate(pivots):
        recovered[column] = pivot_values[i]
    for i, column in enumerate(free):
        recovered[column] = g2[i]
    assert D * recovered == q2
    assert c * recovered == W * q2 + R * g2
    # Nonselected observation rows add a distinct product column; selected
    # rows must be identities and therefore disappear.
    for i, e in enumerate(selected):
        assert W[e, :] == eye(d)[i, :]
        assert R[e, :] == zeros(1, len(free))


def run():
    rng = random.Random(8439)
    count = 0
    examples = [(4, list(combinations(range(4), 2))),
                (2, [(0, 1), (1, 0), (0, 1), (1, 1)]),
                (1, [(0, 0), (0, 0)])]
    for nodes, arcs in examples:
        for mask in range(1 << len(arcs)):
            check(nodes, arcs, [e for e in range(len(arcs)) if mask & (1 << e)], rng)
            count += 1
    for _ in range(120):
        nodes = rng.randint(2, 8)
        arcs = [(i, rng.randrange(i)) for i in range(1, nodes)]
        arcs += [(rng.randrange(nodes), rng.randrange(nodes)) for _ in range(rng.randint(1, 8))]
        arcs = [(a, b) if rng.randrange(2) else (b, a) for a, b in arcs]
        observed = [e for e in range(len(arcs)) if rng.random() < rng.choice([.2, .5, .8])]
        check(nodes, arcs, observed, rng)
        count += 1
    print(f"PASS: {count} exact observation patterns; rank identity, minimum forest completion, unit elimination coefficients, two-way reconstruction")


if __name__ == "__main__":
    run()
