"""Independent exact-certificate comparison of two sparse network/simplex EFs.

Two independent formulations use hand-specified block cores. They are compared
with production formulations with and without observed-rank elimination,
including graph preprocessing checks. SciPy finds LP solutions; Fraction
arithmetic checks complete primal/dual optimality certificates. The reference
EF has a flow on every arc in every simplex state.
Run from the repository root: python code/network_simplex_exploration/review_compression.py
"""

from fractions import Fraction as F
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from network_simplex_compressed.model import CompressedNetworkSimplex


class LP:
    def __init__(self, names):
        self.names = list(names)
        self.pos = {name: i for i, name in enumerate(self.names)}
        self.eq, self.beq, self.ub, self.bub = [], [], [], []

    def row(self, terms):
        out = [F(0)] * len(self.names)
        for name, value in terms.items():
            out[self.pos[name]] += F(value)
        return out

    def equal(self, terms, rhs=0):
        self.eq.append(self.row(terms))
        self.beq.append(F(rhs))

    def upper(self, terms, rhs=0):
        self.ub.append(self.row(terms))
        self.bub.append(F(rhs))

    def optimum(self, objective):
        c = self.row(objective)
        answer = linprog(
            np.array(c, float), A_eq=np.array(self.eq, float),
            b_eq=np.array(self.beq, float), A_ub=np.array(self.ub, float),
            b_ub=np.array(self.bub, float), bounds=[(None, None)] * len(c),
            method="highs",
        )
        assert answer.success, answer.message
        rational = lambda seq: [F(float(v)).limit_denominator(10**8) for v in seq]
        x = rational(answer.x)
        deq = rational(answer.eqlin.marginals)
        dub = rational(answer.ineqlin.marginals)
        dot = lambda a, b: sum((u * v for u, v in zip(a, b)), F(0))
        assert all(dot(a, x) == b for a, b in zip(self.eq, self.beq))
        assert all(dot(a, x) <= b for a, b in zip(self.ub, self.bub))
        assert all(v <= 0 for v in dub)
        for j in range(len(c)):
            assert c[j] == sum(a[j] * d for a, d in zip(self.eq, deq)) + sum(
                a[j] * d for a, d in zip(self.ub, dub)
            )
        primal = dot(c, x)
        dual = dot(self.beq, deq) + dot(self.bub, dub)
        assert primal == dual
        return primal


def cycle_matrix(n, edges):
    """Independent rational incidence-nullspace basis with chord identity."""
    incidence = sp.zeros(n, len(edges))
    for j, (u, v) in enumerate(edges):
        incidence[u, j] -= 1
        incidence[v, j] += 1
    basis = incidence.nullspace()
    matrix = sp.Matrix.hstack(*basis)
    pivots = list(matrix.T.rref()[1])
    matrix = matrix * matrix[pivots, :].inv()
    assert all(value in (-1, 0, 1) for value in matrix)
    assert incidence * matrix == sp.zeros(n, matrix.cols)
    return [[int(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)], pivots


def instance(seed):
    rng = random.Random(seed)
    # A K4 block, a nested series-parallel block, a parallel block, and a loop.
    cores = [
        (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
        (3, [(0, 1), (0, 1), (1, 2), (1, 2), (0, 2)]),
        (2, [(0, 1), (0, 1), (0, 1), (0, 1)]),
        (1, [(0, 0)]),
    ]
    # Small cases retain selected blocks; the last seed class combines all.
    if seed % 5 < 4:
        cores = [cores[seed % 5]]
    edges, caps, seedflow, blocks = [], [], [], []
    nextnode = 1
    for bi, (n, core) in enumerate(cores):
        # First blocks share vertex 0; third has a disconnected component.
        root = 0 if bi != 2 else nextnode
        if bi == 2:
            nextnode += 1
        vertices = [root] + list(range(nextnode, nextnode + n - 1))
        nextnode += n - 1
        C, pivots = cycle_matrix(n, core)
        paths = []
        shift = [rng.randint(-3, 3) for _ in pivots]
        for p, (u, v) in enumerate(core):
            # Include unsuppressed multiedges as well as long reversed paths.
            length = 1 if u == v else rng.randint(1, 3)
            nodes = [vertices[u]] + list(range(nextnode, nextnode + length - 1)) + [vertices[v]]
            nextnode += length - 1
            path = []
            for left, right in zip(nodes, nodes[1:]):
                sign = rng.choice([-1, 1])
                e = len(edges)
                edges.append((left, right) if sign == 1 else (right, left))
                cap = rng.randint(0, 5)
                caps.append(cap)
                seedflow.append(rng.randint(0, cap))
                path.append((e, sign))
            paths.append(path)
        blocks.append((C, pivots, paths, shift))
    # A bridge, a disconnected isolated vertex, and possibly a second loop.
    edges.append((0, nextnode))
    caps.append(4)
    seedflow.append(2)
    nextnode += 2
    A = [[0] * len(edges) for _ in range(nextnode)]
    for e, (u, v) in enumerate(edges):
        A[u][e] -= 1
        A[v][e] += 1
    b = [sum(a * x for a, x in zip(row, seedflow)) for row in A]
    reference = list(seedflow)
    for C, pivots, paths, shift in blocks:
        for p, path in enumerate(paths):
            deviation = sum(c * t for c, t in zip(C[p], shift))
            for e, sign in path:
                reference[e] += sign * deviation
    assert [sum(a * x for a, x in zip(row, reference)) for row in A] == b
    m = 4
    obs = [(e, j) for e in range(len(edges)) for j in range(m) if rng.random() < 0.13]
    return A, b, caps, seedflow, reference, blocks, m, obs


def common(data, auxiliary, fixed):
    A, b, caps, xseed, v, blocks, m, obs = data
    names = [("x", e) for e in range(len(caps))] + [("y", j) for j in range(m)]
    names += [("z", e, j) for e, j in obs] + auxiliary
    lp = LP(names)
    for e, cap in enumerate(caps):
        lp.upper({("x", e): -1})
        lp.upper({("x", e): 1}, cap)
    for row, rhs in zip(A, b):
        lp.equal({("x", e): a for e, a in enumerate(row) if a}, rhs)
    for j in range(m):
        lp.upper({("y", j): -1})
    lp.upper({("y", j): 1 for j in range(m)}, 1)
    if fixed:
        # Includes zero weights and zero residual weight on alternating cases.
        weights = [F(0), F(1, 3), F(1, 6), F(1, 2) if fixed == 2 else F(1, 7)]
        for j, weight in enumerate(weights):
            lp.equal({("y", j): 1}, weight)
        for e, value in enumerate(xseed):
            lp.equal({("x", e): 1}, value)
    return lp


def full(data, fixed):
    A, b, caps, xseed, v, blocks, m, obs = data
    lp = common(data, [("f", e, j) for e in range(len(caps)) for j in range(m + 1)], fixed)
    for e, cap in enumerate(caps):
        lp.equal({("x", e): -1, **{("f", e, j): 1 for j in range(m + 1)}})
        for j in range(m + 1):
            lp.upper({("f", e, j): -1})
            terms = {("f", e, j): 1}
            terms.update({("y", j): -cap} if j < m else {("y", i): cap for i in range(m)})
            lp.upper(terms, 0 if j < m else cap)
    for row, rhs in zip(A, b):
        for j in range(m + 1):
            terms = {("f", e, j): a for e, a in enumerate(row) if a}
            terms.update({("y", j): -rhs} if j < m else {("y", i): rhs for i in range(m)})
            lp.equal(terms, 0 if j < m else rhs)
    for e, j in obs:
        lp.equal({("z", e, j): 1, ("f", e, j): -1})
    return lp


def compressed(data, fixed):
    A, b, caps, xseed, v, blocks, m, obs = data
    labels = []
    for C, pivots, paths, shift in blocks:
        blockedges = {e for path in paths for e, sign in path}
        labels.append(sorted({j for e, j in obs if e in blockedges}))
    lp = common(data, [("h", bi, j, q) for bi, block in enumerate(blocks)
                       for j in labels[bi] for q in range(len(block[1]))], fixed)
    inblock = set()
    for bi, (C, pivots, paths, shift) in enumerate(blocks):
        J = labels[bi]
        inblock.update(e for path in paths for e, sign in path)
        chordarc = [paths[p][0] for p in pivots]
        for p, path in enumerate(paths):
            lower = max(-v[e] if sign == 1 else v[e] - caps[e] for e, sign in path)
            upper = min(caps[e] - v[e] if sign == 1 else v[e] for e, sign in path)
            for j in J:
                terms = {("h", bi, j, q): c for q, c in enumerate(C[p]) if c}
                lp.upper({**terms, ("y", j): -upper})
                lp.upper({**{key: -value for key, value in terms.items()}, ("y", j): lower})
                for e, sign in path:
                    if (e, j) in obs:
                        lp.equal({("z", e, j): 1, ("y", j): -v[e],
                                  **{key: -sign * value for key, value in terms.items()}})
            if J:
                terms = {("h", bi, j, q): -c for j in J for q, c in enumerate(C[p]) if c}
                offset = 0
                for q, c in enumerate(C[p]):
                    if c:
                        e, sign = chordarc[q]
                        terms[("x", e)] = c * sign
                        offset += c * sign * v[e]
                lp.upper({**terms, **{("y", j): upper for j in J}}, upper + offset)
                lp.upper({**{key: -value for key, value in terms.items()},
                          **{("y", j): -lower for j in J}}, -lower - offset)
    for e, j in obs:
        if e not in inblock:
            lp.equal({("z", e, j): 1, ("y", j): -v[e]})
    return lp


def production(data, fixed, eliminate):
    """Audit actual graph preprocessing and certify its separately assembled LP."""
    A, b, caps, xseed, v, blocks, m, obs = data
    E = len(caps)
    arcs = []
    for e in range(E):
        tails = [i for i, row in enumerate(A) if row[e] == -1]
        heads = [i for i, row in enumerate(A) if row[e] == 1]
        arcs.append((tails[0], heads[0], caps[e]) if tails else (0, 0, caps[e]))
    model = CompressedNetworkSimplex(arcs, b, m, obs, eliminate_observed=eliminate)
    expected_blocks = {frozenset(e for path in paths for e, _ in path)
                       for C, pivots, paths, shift in blocks}
    assert {frozenset(block.edges) for block in model.blocks} == expected_blocks
    assert [sum(a * x for a, x in zip(row, model.reference)) for row in A] == b
    hidden = 0
    for bi, block in enumerate(model.blocks):
        assert len(block.rows) <= (1 if block.rank == 1 else 3 * block.rank - 3)
        for q, chord in enumerate(block.chords):
            cycle = [0] * E
            for e in block.edges:
                _, p, sign = model.location[e]
                cycle[e] = sign * dict(block.rows[p]).get(q, 0)
            assert cycle[chord] == 1
            assert all(sum(a * c for a, c in zip(row, cycle)) == 0 for row in A)
        for j in block.labels:
            # Independent union-find cycle count on the unobserved multigraph.
            parent = list(range(len(A)))
            def find(a):
                while parent[a] != a:
                    a = parent[a]
                return a
            rho = 0
            for e in block.edges:
                if (e, j) in obs:
                    continue
                a, c, cap = arcs[e]
                ra, rc = find(a), find(c)
                if ra == rc:
                    rho += 1
                else:
                    parent[ra] = rc
            hidden += rho
            if eliminate:
                assert model.observed_ranks[bi, j] == block.rank - rho
    if eliminate:
        assert model.n - model.original_n == hidden
    else:
        assert model.n - model.original_n == sum(block.rank * len(block.labels) for block in model.blocks)
    names = [("x", e) for e in range(E)] + [("y", j) for j in range(m)]
    names += [("z", e, j) for e, j in model.observations]
    names += [("g", k) for k in range(model.n - model.original_n)]
    lp = LP(names)
    for rows, add in ((model.eq, lp.equal), (model.ub, lp.upper)):
        for terms, rhs in rows:
            assert all(value in (-1, 0, 1) for col, value in terms.items() if not E <= col < E + m)
            add({names[col]: value for col, value in terms.items()}, rhs)
    for name, (lower, upper) in zip(names, model.bounds):
        if lower is not None:
            lp.upper({name: -1}, -lower)
        if upper is not None:
            lp.upper({name: 1}, upper)
    if fixed:
        weights = [F(0), F(1, 3), F(1, 6), F(1, 2) if fixed == 2 else F(1, 7)]
        for j, weight in enumerate(weights):
            lp.equal({("y", j): 1}, weight)
        for e, value in enumerate(xseed):
            lp.equal({("x", e): 1}, value)
    return lp


def main():
    count = 0
    for seed in range(30):
        data = instance(seed)
        for fixed in (0, 1, 2):
            reference, candidate = full(data, fixed), compressed(data, fixed)
            actual, eliminated = production(data, fixed, False), production(data, fixed, True)
            rng = random.Random(10000 + 3 * seed + fixed)
            for trial in range(3):
                objective = {name: rng.randint(-9, 9) for name in candidate.names if name[0] != "h"}
                left, right = reference.optimum(objective), candidate.optimum(objective)
                assert left == right, (seed, fixed, trial, left, right)
                assert actual.optimum(objective) == left
                assert eliminated.optimum(objective) == left
                count += 1
    print(f"PASS: {count} matching support optima across four formulations; {4 * count} exact rational primal/dual certificates.")
    print("Includes general cores, parallel arcs, loops, reversed subdivided paths, articulation/disconnected blocks,")
    print("bridges, zero capacities/weights, varying local label sets, infeasible reference bounds, and fixed fractional slices.")
    print("Production graph extraction, cycle matrices, observed-rank elimination, hidden-cycle counts, and unit coefficients also passed.")
    print("Scope: these deterministic cases do not exhaust all graphs and are not a runtime benchmark.")


if __name__ == "__main__":
    main()
