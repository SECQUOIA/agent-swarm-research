"""Exact checks for new Stage 2 preprocessing and the worked K4 example.

Run with a Python environment containing SymPy. Does not import the repository
formulation implementations. Small unit-capacity flow polytopes are integral;
enumerating their feasible 0/1 vectors therefore spans their affine hulls.
These finite checks supplement, rather than prove, the manuscript statements.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random

from sympy import Matrix, zeros


def incidence(nodes, arcs):
    a = zeros(nodes, len(arcs))
    for e, (tail, head) in enumerate(arcs):
        a[tail, e] -= 1
        a[head, e] += 1
    return a


def fixed_arc_checks():
    rng = random.Random(917023)
    count = 0
    for _ in range(80):
        nodes = rng.randint(1, 5)
        arcs = [(rng.randrange(nodes), rng.randrange(nodes))
                for _ in range(rng.randint(1, 8))]
        a = incidence(nodes, arcs)
        caps = [rng.randint(0, 1) for _ in arcs]
        witness = Matrix([rng.randint(0, u) for u in caps])
        balance = a * witness
        feasible = [Matrix(x) for x in product(*(range(u + 1) for u in caps))
                    if a * Matrix(x) == balance]
        fixed = [e for e in range(len(arcs))
                 if len({x[e] for x in feasible}) == 1]
        remaining = [e for e in range(len(arcs)) if e not in fixed]
        reduced_a = a[:, remaining]
        reduced_balance = balance - a[:, fixed] * witness[fixed, :]
        reduced = [Matrix(x) if remaining else zeros(0, 1)
                   for x in product(*(range(caps[e] + 1) for e in remaining))
                   if reduced_a * (Matrix(x) if remaining else zeros(0, 1))
                   == reduced_balance]
        assert {tuple(x[remaining, :]) for x in feasible} == {
            tuple(x) for x in reduced}
        differences = Matrix.hstack(*(x - reduced[0] for x in reduced))
        assert differences.rank() == len(remaining) - reduced_a.rank()
        if remaining:
            # An average of all feasible integral vectors is strictly inside
            # every surviving bound, independently checking the proof witness.
            average = sum(reduced, zeros(len(remaining), 1)) / len(reduced)
            assert all(0 < average[i] < caps[e]
                       for i, e in enumerate(remaining))
        count += 1
    return count


def k4_check():
    arcs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    a = incidence(4, arcs)
    x = [F(1, 2), F(1, 4), F(1, 4), F(1, 4), F(1, 4), F(1, 2)]
    assert a * Matrix(x) == Matrix([-1, 0, 0, 1])
    y = F(1, 2)
    z = {1: F(1, 5), 2: F(1, 5), 4: F(1, 5)}
    for e, value in z.items():
        assert 0 <= value <= y
        assert x[e] - (1 - y) <= value <= x[e]
    assert sum(z.values()) - y == F(1, 10)
    state = [y - z[1] - z[2], z[1], z[2],
             y - z[1] - z[2] - z[4], z[4], y - z[2] - z[4]]
    assert a * Matrix(state) == y * Matrix([-1, 0, 0, 1])
    assert state[3] == -F(1, 10)
    # All unit-flow vertices, independently enumerated, obey the path cut.
    vertices = [t for t in product((0, 1), repeat=6)
                if a * Matrix(t) == Matrix([-1, 0, 0, 1])]
    assert len(vertices) == 4
    assert all(t[1] + t[2] + t[4] <= 1 for t in vertices)
    return len(vertices)


if __name__ == "__main__":
    result = {"status": "PASS", "fixed_arc_models": fixed_arc_checks(),
              "k4_flow_vertices": k4_check(), "k4_violation": "1/10"}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
