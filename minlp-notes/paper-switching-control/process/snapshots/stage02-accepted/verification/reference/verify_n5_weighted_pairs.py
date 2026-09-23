"""Exact dual certificates for the five-mode weighted excluded-pair inequality.

The checker uses only the Python standard library. Each case fixes a first-reach
ordering and the symmetry type of one globally maximizing pair. It does not
discretize time or assume an ordering of the excluded-pair reach times.
"""

from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
from pathlib import Path

N = 5
SELECTED = frozenset((0, 1, 2))
EXCLUDED_PAIRS = tuple(p for p in combinations(range(N), 2) if SELECTED.intersection(p))
LABELS = (("g", 0),) + tuple(("r", i) for i in range(N)) + tuple(
    ("q", p) for p in EXCLUDED_PAIRS
) + tuple(("m", i) for i in sorted(SELECTED))
POSITION = {v: j for j, v in enumerate(LABELS)}
VARIABLES = len(LABELS) * (N + 1)
TARGET = F(675, 16)


def cases():
    """All first-reach orders for three pair orbits under S_3 x S_2."""
    return product(((0, 1), (0, 3), (3, 4)), permutations(range(N)))


def time(v):
    return POSITION[v] * (N + 1)


def allocation(v, i):
    return time(v) + 1 + i


def program(pair, first_order):
    """Sparse integer A,b,B,d,c for min c*x, A*x<=b, B*x=d, x>=0."""
    inequalities, rhs, equalities, erhs = [], [], [], []

    def precedes(v, w):
        for i in range(N):
            inequalities.append({allocation(v, i): 1, allocation(w, i): -1})
            rhs.append(0)

    for v in LABELS:
        row = {time(v): -1}
        row.update({allocation(v, i): 1 for i in range(N)})
        equalities.append(row)
        erhs.append(0)

    for i, j in zip(first_order, first_order[1:]):
        precedes(("r", i), ("r", j))
    for i in range(N):
        v = ("r", i)
        equalities.append({time(v): 1, allocation(v, i): -1})
        erhs.append(1)

    for v in LABELS:
        if v[0] == "r":
            continue
        excluded = set(v[1]) if v[0] == "q" else ({v[1]} if v[0] == "m" else set())
        available = [i for i in range(N) if i not in excluded]
        for i in available:
            precedes(("r", i), v)
        for j, k in permutations(available, 2):
            inequalities.append({time(("r", j)): 1, time(v): -1, allocation(v, k): 1})
            rhs.append(-1)

    for p in EXCLUDED_PAIRS:
        for i in sorted(SELECTED.intersection(p)):
            precedes(("q", p), ("m", i))

    for p in EXCLUDED_PAIRS:
        precedes(("q", p), ("g", 0))
        if not set(p).intersection(pair):
            precedes(("g", 0), ("q", p))
    for i in sorted(SELECTED):
        precedes(("m", i), ("g", 0))
        if i not in pair:
            precedes(("g", 0), ("m", i))

    objective = {time(("q", p)): len(SELECTED.intersection(p)) for p in EXCLUDED_PAIRS}
    objective.update({time(("m", i)): 1 for i in SELECTED})
    return inequalities, rhs, equalities, erhs, objective


def verify(pair, first_order, certificate):
    A, b, B, d, c = program(pair, first_order)
    y = {int(j): F(v) for j, v in certificate["inequality"].items()}
    z = {int(j): F(v) for j, v in certificate["equality"].items()}
    assert all(0 <= j < len(A) and v <= 0 for j, v in y.items())
    assert all(0 <= j < len(B) for j in z)
    residual = [F(c.get(j, 0)) for j in range(VARIABLES)]
    for rows, multipliers in ((A, y), (B, z)):
        for k, value in multipliers.items():
            for j, coefficient in rows[k].items():
                residual[j] -= value * coefficient
    assert all(v >= 0 for v in residual), "Negative dual residual"
    bound = sum((value * b[j] for j, value in y.items()), F(0)) + sum(
        (value * d[j] for j, value in z.items()), F(0)
    )
    assert bound == F(certificate["lower_bound"]) == TARGET


def main():
    if not __debug__:
        raise RuntimeError("Run without -O: certificate verification requires assertions")
    data = json.loads(Path(__file__).with_name("certificates_n5_weighted_pairs.json").read_text())
    expected = list(cases())
    assert len(data) == len(expected) == 360
    for (pair, first_order), certificate in zip(expected, data):
        assert certificate["pair"] == list(pair)
        assert certificate["first_order"] == list(first_order)
        verify(pair, first_order, certificate)
    print("Verified all 360 cases using exact rational arithmetic.")
    print("For n=5 and uncapped pair reaches, every three-mode subset S has H_S >= 675/16.")
    print("No numerical solver, tolerance, or time discretization is used by this checker.")


if __name__ == "__main__":
    main()
