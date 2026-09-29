"""Independent finite checks for the constrained kernel proof; not an SDP test."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import prod
from random import Random


def clean(p):
    return {a: c for a, c in p.items() if c}


def add(*terms):
    out = defaultdict(F)
    for scale, p in terms:
        for a, c in p.items():
            out[a] += scale * c
    return clean(out)


def mul(p, q):
    out = defaultdict(F)
    for a, ca in p.items():
        for b, cb in q.items():
            for signs in product((1, -1), repeat=len(a)):
                index = tuple(abs(ai + s * bi) for ai, bi, s in zip(a, b, signs))
                out[index] += ca * cb / 2 ** len(a)
    return clean(out)


def power(p, k):
    ans = {(0,) * len(next(iter(p))): F(1)}
    for _ in range(k):
        ans = mul(ans, p)
    return ans


def c_norm(p):
    return sum(map(abs, p.values()), F(0))


def a_norm(p):
    return sum((abs(c) * sum(i * i for i in a) for a, c in p.items()), F(0))


def degree(p):
    return max(map(sum, p), default=0)


def jackson(p, m):
    b = {j: m - abs(j) for j in range(-m + 1, m)}
    denom = sum(v * v for v in b.values())

    def lam(k):
        return F(sum(v * b.get(j - k, 0) for j, v in b.items()), denom)

    return clean({a: c * prod(lam(k) for k in a) for a, c in p.items()})


def ordinary_operator(s, n):
    """Construct its own rational Chebyshev kernel, then integrate exactly."""
    source = {(0, 0): F(1)}
    source.update({(j, j): 2 * (1 - F(j, s)) for j in range(1, s)})
    square = mul(source, source)
    mass = {(a,): c for (a, b), c in square.items() if b == 0}
    cs = F(2 * s * s + 1, 3 * s)
    z = add((1, {(0,): F(1)}), (-1 / cs, mass))
    normalization = {}
    for j in range(n + 1):
        normalization = add((1, normalization), (1 / cs, power(z, j)))
    source_normalization = {(a[0], 0): c for a, c in normalization.items()}
    kernel = mul(source_normalization, square)
    columns = {}
    for k in range(s + 1):
        columns[k] = {
            (a,): c / (1 if k == 0 else 2)
            for (a, b), c in kernel.items()
            if b == k
        }

    def apply(p):
        out = {}
        for alpha, coeff in p.items():
            tensor = {(): F(1)}
            for k in alpha:
                tensor = {
                    prefix + beta: left * right
                    for prefix, left in tensor.items()
                    for beta, right in columns.get(k, {}).items()
                }
            out = add((1, out), (coeff, tensor))
        return out

    return apply, 2 * (s - 1) * (n + 1)


def coefficient_checks():
    rng = Random(97183)
    basis_count = 0
    random_count = 0
    residual_count = 0
    for dim in range(1, 4):
        indices = list(product(range(4), repeat=dim))
        for a, b in product(indices, repeat=2):
            p = mul({a: F(1)}, {b: F(1)})
            assert c_norm(p) == 1
            assert a_norm(p) == sum(i * i for i in a + b)
            basis_count += 1
        for _ in range(40):
            p = clean({rng.choice(indices): F(rng.randint(-4, 4), 3) for _ in range(7)})
            q = clean({rng.choice(indices): F(rng.randint(-4, 4), 5) for _ in range(7)})
            pq = mul(p, q)
            assert c_norm(pq) <= c_norm(p) * c_norm(q)
            assert a_norm(pq) <= c_norm(p) * a_norm(q) + a_norm(p) * c_norm(q)
            random_count += 1
            for m in (2, 3, 5, 8):
                square = mul(p, p)
                residual = add((1, jackson(square, m)), (-2, mul(p, jackson(p, m))), (1, square))
                assert degree(residual) <= 2 * degree(p)
                assert c_norm(residual) <= 12 * c_norm(p) * a_norm(p) / (2 * m * m + 1)
                residual_count += 1
    return basis_count, random_count, residual_count


def ordinary_checks():
    cases = 0
    for s, n in ((2, 2), (2, 4), (3, 2), (3, 4)):
        operator, d = ordinary_operator(s, n)
        for p in (
            {(0,): F(-1, 2), (1,): F(1)},
            {(0,): F(2)},
            {(0, 0): F(-1, 2), (1, 0): F(1), (0, 1): F(1)},
            {(0, 0): F(1, 3), (1, 1): F(-1)},
        ):
            dim = len(next(iter(p)))
            one = {(0,) * dim: F(1)}
            square = mul(p, p)
            # Avoid an irrational relaxation of eta: measure the exact largest
            # relevant basis error, making the tensor inequality stronger.
            eta = max(
                c_norm(add((1, operator({(k,): F(1)})), (-1, {(k,): F(1)})))
                for k in range(3)
            )
            gamma = (1 + eta) ** dim - 1
            for q in (one, p, square):
                assert c_norm(add((1, operator(q)), (-1, q))) <= c_norm(q) * gamma
            residual = add((1, operator(square)), (-2, mul(p, operator(p))), (1, mul(square, operator(one))))
            assert degree(residual) <= dim * d + 2 * degree(p)
            assert c_norm(residual) <= 4 * c_norm(p) ** 2 * gamma
            cases += 1
    return cases


def transport_checks():
    """Exact finite checks of the sharper displacement calculation.

    A coefficient norm bound here is a sufficient positivity check for the
    sampled polynomials. The all-order proof uses the circle integral and
    the univariate interval SOS theorem, not these finite samples.
    """
    slopes = 0
    for s in range(2, 81):
        b = {j: max(F(0), 1 - F(abs(j), s)) for j in range(-s, s + 1)}
        difference_square_sum = sum(
            (b.get(j, F(0)) - b.get(j - 1, F(0))) ** 2
            for j in range(-s, s + 2)
        )
        assert difference_square_sum == F(2, s)
        slopes += 1
    cases = 0
    one, x = {(0,): F(1)}, {(1,): F(1)}
    square = mul(x, x)
    for s, n in product(range(2, 8), (2, 4, 6)):
        operator, d = ordinary_operator(s, n)
        displacement = add(
            (1, operator(square)),
            (-2, mul(x, operator(x))),
            (1, mul(square, operator(one))),
        )
        cs = F(2 * s * s + 1, 3 * s)
        bound = 4 / (s * cs)
        assert degree(displacement) <= d + 2
        assert c_norm(displacement) <= bound <= F(6, s * s)
        cases += 1
    return slopes, cases


def finite_coupling_checks():
    """Lift maximal separator couplings and glue full bag records on a chain."""
    states = list(product((-1, 1), repeat=2))
    weights = ((1, 3, 2, 2), (3, 1, 3, 1), (1, 1, 4, 2))
    laws = [{state: F(weight, sum(ws)) for state, weight in zip(states, ws)} for ws in weights]

    def marginal(law, coordinate):
        return {value: sum(p for state, p in law.items() if state[coordinate] == value) for value in (-1, 1)}

    edge_laws = []
    tvs = []
    for left, right in zip(laws, laws[1:]):
        pl, pr = marginal(left, 1), marginal(right, 0)
        diagonal = {value: min(pl[value], pr[value]) for value in (-1, 1)}
        tv = 1 - sum(diagonal.values())
        tvs.append(tv)
        separator = {(a, b): (diagonal[a] if a == b else F(0)) for a, b in product((-1, 1), repeat=2)}
        if tv:
            for a, b in separator:
                separator[a, b] += (pl[a] - diagonal[a]) * (pr[b] - diagonal[b]) / tv
        pair_law = {
            (x, y): separator[x[1], y[0]] * left[x] / pl[x[1]] * right[y] / pr[y[0]]
            for x, y in product(states, repeat=2)
        }
        assert sum(p for (x, y), p in pair_law.items() if x[1] != y[0]) == tv
        edge_laws.append(pair_law)
    triple = {(x, y, z): edge_laws[0][x, y] * edge_laws[1][y, z] / laws[1][y] for x, y, z in product(states, repeat=3)}
    assert sum(triple.values()) == 1
    for bag in range(3):
        assert all(sum(p for record, p in triple.items() if record[bag] == state) == laws[bag][state] for state in states)
    bad = lambda record: record[0][1] != record[1][0] or record[1][1] != record[2][0]
    probability_bad = sum(p for record, p in triple.items() if bad(record))
    assert probability_bad <= min(1, sum(tvs))
    objective = (lambda x, y: 2 * x - y, lambda y, z: y * z, lambda z, t: z + t)
    constraint = (lambda x, y: x - y, lambda y, z: y + z - F(1, 2), lambda z, t: z - t)
    violation = lambda val: max(-val, F(0)) ** 2
    local_objective = sum(p * objective[b](*state) for b, law in enumerate(laws) for state, p in law.items())
    local_violation = sum(p * violation(constraint[b](*state)) for b, law in enumerate(laws) for state, p in law.items())
    # Exact box oscillations for these multilinear objectives; C(g)^2 sum.
    oscillation_sum = F(6 + 2 + 4)
    g2_bound = F(4) + F(25, 4) + F(4)
    cases = 0
    for replacement in product((-1, 0, 1), repeat=4):
        out_objective = F(0)
        out_violation = F(0)
        for record, probability in triple.items():
            point = replacement if bad(record) else (record[0][0], record[0][1], record[1][1], record[2][1])
            out_objective += probability * sum(objective[b](*point[b:b + 2]) for b in range(3))
            out_violation += probability * sum(violation(constraint[b](*point[b:b + 2])) for b in range(3))
        assert abs(out_objective - local_objective) <= oscillation_sum * probability_bad
        assert out_violation <= local_violation + g2_bound * probability_bad
        cases += 1
    return cases, probability_bad, sum(tvs)


if __name__ == "__main__":
    basis, products, jackson_cases = coefficient_checks()
    ordinary_cases = ordinary_checks()
    slope_cases, transport_cases = transport_checks()
    coupling_cases, bad, tv = finite_coupling_checks()
    print(f"PASS: {basis} basis products; {products} signed polynomial products; {jackson_cases} Jackson residual bounds.")
    print(f"PASS: {ordinary_cases} ordinary-kernel residual and tensor bounds.")
    print(f"PASS: {slope_cases} exact Fejer displacement constants; {transport_cases} ordinary-kernel displacement bounds.")
    print(f"PASS: {coupling_cases} simultaneous objective/violation repair checks; bad probability {bad}, TV sum {tv}.")
