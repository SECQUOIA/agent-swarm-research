"""Exact finite and polynomial certificates for the general four-block reach lemma.

Only the Python standard library is used. A certificate for every integer n>=23
is checked by polynomial identities and nonnegative coefficients after n=23+t.
The remaining n=5,...,22 are checked with integer arithmetic.
"""

from itertools import combinations, permutations
import json
from math import comb
from pathlib import Path

CASES = (
    ((0, 1), 0), ((0, 1), 2), ((0, 1), 3),
    ((0, 3), 0), ((0, 3), 1), ((0, 3), 3), ((0, 3), 4),
    ((3, 4), 0), ((3, 4), 3), ((3, 4), 5),
)
START = 23


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p or [0]


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, v in enumerate(a):
        c[i] += v
    for i, v in enumerate(b):
        c[i] += v
    return trim(c)


def scale(a, k):
    return trim([k * v for v in a])


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, v in enumerate(a):
        for j, w in enumerate(b):
            c[i + j] += v * w
    return trim(c)


def shift(a, h):
    """Coefficients of a(h+t), in ascending order."""
    c = [0] * len(a)
    for j, v in enumerate(a):
        for k in range(j + 1):
            c[k] += v * comb(j, k) * h ** (j - k)
    return trim(c)


def quotient(n, pair, distinguished):
    """Integer orbit LP; objective is (n-1)^2 H - 3n^2 sum_{i!=z} R_i.

    Modes outside S union pair union {z} can be permuted. An invariant feasible
    point has equal variables on each resulting orbit. Convex averaging shows
    that this restriction preserves the LP's optimal objective.
    """
    selected = {0, 1, 2}
    special = selected | set(pair) | {distinguished}
    assert n >= 5 and max(special) < n
    excluded_pairs = [p for p in combinations(range(n), 2) if selected.intersection(p)]
    events = [("g",)] + [("q",) + p for p in excluded_pairs] + [("p", i) for i in sorted(selected)]

    def canonical(key):
        seen = {}

        def index(i):
            if i in special:
                return ("s", i)
            if i not in seen:
                seen[i] = len(seen)
            return ("b", seen[i])

        def event(v):
            return (v[0],) + tuple(index(i) for i in v[1:])

        if key[0] == "r":
            return ("r", index(key[1]))
        if key[0] == "t":
            return ("t", event(key[1]))
        return ("a", event(key[1]), index(key[2]))

    variables, lookup = [], {}

    def variable(key):
        orbit = canonical(key)
        if orbit not in lookup:
            lookup[orbit] = len(variables)
            variables.append(orbit)
        return lookup[orbit]

    for i in range(n):
        variable(("r", i))
    for v in events:
        variable(("t", v))
        for i in range(n):
            variable(("a", v, i))

    def row(terms):
        coefficients = {}
        for key, value in terms:
            j = variable(key)
            coefficients[j] = coefficients.get(j, 0) + value
        return tuple(sorted((j, value) for j, value in coefficients.items() if value))

    inequalities, equalities = {}, {}

    def insert(rows, coefficients, rhs):
        assert coefficients not in rows or rows[coefficients] == rhs
        rows[coefficients] = rhs

    def precedes(v, w):
        for i in range(n):
            insert(inequalities, row([(("a", v, i), 1), (("a", w, i), -1)]), 0)

    for v in events:
        insert(equalities, row([(("t", v), -1)] + [(("a", v, i), 1) for i in range(n)]), 0)
        available = [i for i in range(n) if i not in v[1:]]
        for j, k in permutations(available, 2):
            insert(inequalities, row([(("r", j), 1), (("t", v), -1), (("a", v, k), 1)]), -1)

    for p in excluded_pairs:
        v = ("q",) + p
        for i in sorted(selected.intersection(p)):
            precedes(v, ("p", i))
        precedes(v, ("g",))
        if not set(p).intersection(pair):
            precedes(("g",), v)
    for i in sorted(selected):
        precedes(("p", i), ("g",))
        if i not in pair:
            precedes(("g",), ("p", i))

    objective = [0] * len(variables)
    for p in excluded_pairs:
        objective[variable(("t", ("q",) + p))] += len(selected.intersection(p)) * (n - 1) ** 2
    for i in sorted(selected):
        objective[variable(("t", ("p", i)))] += (n - 1) ** 2
    for i in range(n):
        if i != distinguished:
            objective[variable(("r", i))] -= 3 * n * n
    return variables, list(inequalities), list(inequalities.values()), list(equalities), list(equalities.values()), objective


def symbolic_program(pair, distinguished):
    """Fixed topology for n>=9; mass rows and orbit counts are affine in n.

    At most six indices are special. Every inequality involves at most three
    other indices, so n>=9 contains every orbit pattern. Only sums over allocation
    modes and sums defining the objective have multiplicities depending on n.
    """
    V, A, b, B9, d, c9 = quotient(9, pair, distinguished)
    W, A10, b10, B10, d10, c10 = quotient(10, pair, distinguished)
    assert V == W and A == A10 and b == b10 and d == d10
    assert len(B9) == len(B10)
    symbolic_B = []
    for r9, r10 in zip(B9, B10):
        p9, p10 = dict(r9), dict(r10)
        row = {}
        for j in sorted(p9.keys() | p10.keys()):
            slope = p10.get(j, 0) - p9.get(j, 0)
            row[j] = trim([p9.get(j, 0) - 9 * slope, slope])
        symbolic_B.append(row)
    symbolic_c = []
    for key, a, b0 in zip(V, c9, c10):
        f9, f10 = (-3 * 9 ** 2, -3 * 10 ** 2) if key[0] == "r" else (8 ** 2, 9 ** 2)
        assert a % f9 == 0 and b0 % f10 == 0
        count9, count10 = a // f9, b0 // f10
        slope = count10 - count9
        count = [count9 - 9 * slope, slope]
        symbolic_c.append(mul(count, [0, 0, -3] if key[0] == "r" else [1, -2, 1]))
    return V, A, b, symbolic_B, d, symbolic_c


def check_finite(n, pair, distinguished, certificate):
    V, A, b, B, d, c = quotient(n, pair, distinguished)
    denominator = certificate["denominator"]
    assert isinstance(denominator, int) and denominator > 0
    y = {int(i): v for i, v in certificate["inequality"].items()}
    z = {int(i): v for i, v in certificate["equality"].items()}
    assert all(0 <= i < len(A) and isinstance(v, int) and v <= 0 for i, v in y.items())
    assert all(0 <= i < len(B) and isinstance(v, int) for i, v in z.items())
    residual = [denominator * v for v in c]
    for rows, multipliers in ((A, y), (B, z)):
        for i, value in multipliers.items():
            for j, coefficient in rows[i]:
                residual[j] -= value * coefficient
    assert all(v == 0 for v in residual)
    assert sum(y[i] * b[i] for i in y) + sum(z[i] * d[i] for i in z) == denominator * 3 * n * n * (n - 1)


def polynomial(value):
    assert isinstance(value, list) and value and all(isinstance(c, int) for c in value)
    return trim(value)


def check_symbolic(pair, distinguished, certificate):
    V, A, b, B, d, c = symbolic_program(pair, distinguished)
    D = polynomial(certificate["denominator"])
    D0 = polynomial(certificate["denominator_div_n_minus_one_squared"])
    assert D == mul(D0, [1, -2, 1])
    shifted = shift(D, START)
    assert shifted[0] > 0 and all(v >= 0 for v in shifted)
    y = {int(i): polynomial(v) for i, v in certificate["inequality"].items()}
    z = {int(i): polynomial(v) for i, v in certificate["equality"].items()}
    assert all(0 <= i < len(A) and all(v >= 0 for v in shift(scale(p, -1), START)) for i, p in y.items())
    assert all(0 <= i < len(B) for i in z)
    residual = [mul(D0, p) for p in c]
    for i, p in y.items():
        for j, coefficient in A[i]:
            residual[j] = add(residual[j], scale(p, -coefficient))
    for i, p in z.items():
        for j, coefficient in B[i].items():
            residual[j] = add(residual[j], scale(mul(p, coefficient), -1))
    assert all(p == [0] for p in residual), "Polynomial dual identity failed"
    bound = [0]
    for i, p in y.items():
        bound = add(bound, scale(p, b[i]))
    for i, p in z.items():
        bound = add(bound, scale(p, d[i]))
    assert bound == mul(D0, [0, 0, -3, 3])


def main():
    if not __debug__:
        raise RuntimeError("Run without -O: exact verification requires assertions")
    data = json.loads(Path(__file__).with_name("certificates_general_four_block.json").read_text())
    expected = [(n, pair, z) for n in range(5, START) for pair, z in CASES if z < n]
    assert len(data["finite"]) == len(expected) == 179
    for (n, pair, z), cert in zip(expected, data["finite"]):
        assert cert["n"] == n and cert["pair"] == list(pair) and cert["distinguished"] == z
        check_finite(n, pair, z, cert)
    assert len(data["symbolic"]) == len(CASES) == 10
    for (pair, z), cert in zip(CASES, data["symbolic"]):
        assert cert["pair"] == list(pair) and cert["distinguished"] == z
        check_symbolic(pair, z, cert)
    print("Verified 179 exact finite cases for n=5,...,22.")
    print("Verified 10 polynomial certificates for every n>=23.")
    print("All n>=5 satisfy the weighted pair-network inequality and four-block reach bound.")
    print("Only integer arithmetic and the Python standard library were used.")


if __name__ == "__main__":
    main()
