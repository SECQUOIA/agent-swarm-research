"""Independent, finite exact checks for the rational-optimizer lower bound.

These support the accompanying analytical review; they are not its proof.
Run from the repository root with Python and SymPy installed.
"""

from fractions import Fraction as Q
from itertools import product

import sympy as s


def mul(a, b):
    w, x, y, z = a
    v, i, j, k = b
    return (
        w * v - x * i - y * j - z * k,
        w * i + x * v + y * k - z * j,
        w * j - x * k + y * v + z * i,
        w * k + x * j - y * i + z * v,
    )


def inv(a):
    return a[0], -a[1], -a[2], -a[3]


def rot(a):
    return a[0], a[3], a[1], a[2]


def proj(a):
    return mul(a, (a[0], a[1], -a[2], -a[3]))


def comm(a, b):
    return mul(mul(mul(a, b), inv(a)), inv(b))


def mult_signal(a, b):
    return proj(rot(comm(a, rot(b))))


def sqnorm(a):
    return sum(x * x for x in a)


def stereo(v):
    r = sqnorm(v)
    return ((1 - r) / (1 + r), *(2 * x / (1 + r) for x in v))


def assert_signal(q, coefficient, order, bound, delta):
    error = (q[1] - coefficient * delta**order, q[2], q[3])
    assert sqnorm(q) == 1 and q[0] > 0
    assert abs(coefficient) <= bound
    assert sqnorm(error) <= (bound * delta ** (order + 1)) ** 2


def signal_checks():
    t = Q(1, 2**20)
    q = stereo((t, Q(0), Q(0)))
    for _ in range(2):
        x = q[1]
        assert 0 < x <= Q(1, 2**16)
        assert q[2] ** 2 + q[3] ** 2 <= (64 * x * x) ** 2
        next_q = mult_signal(q, q)
        assert x * x <= next_q[1] <= 6 * x * x
        assert next_q[0] > 0
        assert next_q[2] ** 2 + next_q[3] ** 2 <= (64 * next_q[1] ** 2) ** 2
        q = next_q

    delta, bound = Q(1, 2**50), 128
    next_bound = 2**20 * bound**4
    cases = 0
    for c, d, order_a, order_b in product((-3, 0, 2), (-2, 0, 3), (1, 2), (1, 2)):
        a = stereo((c * delta**order_a / 2, delta ** (order_a + 1), -delta ** (order_a + 1)))
        b = stereo((d * delta**order_b / 2, -delta ** (order_b + 1), 2 * delta ** (order_b + 1)))
        assert_signal(a, c, order_a, bound, delta)
        assert_signal(b, d, order_b, bound, delta)
        assert_signal(inv(a), -c, order_a, next_bound, delta)
        assert_signal(proj(a), 2 * c, order_a, next_bound, delta)
        assert_signal(mult_signal(a, b), 4 * c * d, order_a + order_b, next_bound, delta)
        if order_a == order_b:
            assert_signal(proj(mul(a, b)), 2 * (c + d), order_a, next_bound, delta)
        cases += 1
    return cases


def exposing_checks():
    blocks = [tuple(s.symbols(f"x{i}_0:4")) for i in range(4)]
    c = (s.Rational(3, 5), s.Rational(4, 5), s.Integer(0), s.Integer(0))
    values = [c, mul(c, c)]
    values.append(inv(values[1]))
    values.append(mul(values[1], values[2]))
    parents = [None, (0, 0), (1,), (1, 2)]
    residuals, forms = [], []
    centered = [tuple(x - p for x, p in zip(block, value)) for block, value in zip(blocks, values)]
    norm_residuals = [sqnorm(block) - 1 for block in blocks]
    for i, pa in enumerate(parents):
        if pa is None:
            predicted = c
            subtract = 0
            expected = sqnorm(centered[i])
        elif len(pa) == 1:
            predicted = inv(blocks[pa[0]])
            subtract = norm_residuals[pa[0]]
            expected = sqnorm(centered[i]) - sqnorm(centered[pa[0]])
        else:
            a, b = pa
            predicted = mul(blocks[a], blocks[b])
            subtract = norm_residuals[a] + norm_residuals[b]
            previous = mul(values[i], inv(centered[b]))
            expected = sqnorm(centered[i]) - sqnorm(tuple(x - y for x, y in zip(centered[a], previous)))
        residual = tuple(x - y for x, y in zip(blocks[i], predicted))
        residuals.append(residual)
        form = norm_residuals[i] - 2 * sum(p * r for p, r in zip(values[i], residual)) - subtract
        assert s.expand(form - expected) == 0
        forms.append(form)
    variables = sum((list(block) for block in blocks), [])
    point = dict(zip(variables, sum((list(value) for value in values), [])))
    residual_vector = s.Matrix(sum((list(r) for r in residuals), []))
    assert residual_vector.subs(point) == s.zeros(16, 1)
    assert residual_vector.jacobian(variables).subs(point).det() == 1
    exposed = sum(s.Rational(1, 16**i) * f for i, f in enumerate(forms))
    matrix = s.hessian(exposed, variables) / 2
    floor = s.Rational(11, 15 * 16**3)
    assert (matrix - floor * s.eye(16)).is_positive_definite
    assert (s.eye(16) - matrix).is_positive_semidefinite
    eta = s.Rational(1, 2**30)
    rounded = exposed
    for i, (value, residual) in enumerate(zip(values, residuals)):
        for p, r in zip(value, residual):
            approximation = s.floor(p / eta) * eta
            rounded -= 2 * s.Rational(1, 16**i) * (approximation - p) * r
    assert s.expand(rounded).subs(point) == 0
    rounded_hessian = s.hessian(rounded, variables) / 2
    assert (rounded_hessian - s.eye(16) / (4 * 16**3)).is_positive_definite
    gradient = s.Matrix([s.diff(rounded, x).subs(point) for x in variables])
    assert gradient.dot(gradient) <= (12 * 4 * eta) ** 2


def gram_checks():
    n = 2
    u = s.Matrix(s.symbols("u0:2"))
    y = s.Matrix(s.symbols("y0:2"))
    h = s.Matrix([[2, s.Rational(1, 4)], [s.Rational(1, 4), 3]])
    eps = s.Rational(1, 10**8)
    ell = s.Matrix([eps / 2, eps / 3])
    bs = [s.Matrix([1, 1]), s.Matrix([0, 1])]
    ts = [s.diag(1, 0), s.Matrix([[0, s.Rational(1, 2)], [s.Rational(1, 2), 0]])]

    def scalar(b, t):
        return (b.T * u)[0] + (u.T * t * u)[0]

    def cross(b, t):
        return s.Matrix(n, n * n, lambda i, column: 2 * b[column // n] * t[i, column % n] + 4 * b[i] * t[column // n, column % n])

    def quadratic(t):
        flat = s.Matrix(list(t))
        return 8 * flat * flat.T + 4 * s.kronecker_product(t, t)

    c = 2 * ell * ell.T + 2 * eps * sum((b * b.T for b in bs), s.zeros(n))
    d = cross(ell, h) + eps * sum((cross(b, t) for b, t in zip(bs, ts)), s.zeros(n, n * n))
    q = quadratic(h) + eps * sum((quadratic(t) for t in ts), s.zeros(n * n))
    matrix = c.row_join(d).col_join(d.T.row_join(q))
    f = scalar(ell, h) ** 2 + eps * sum(scalar(b, t) ** 2 for b, t in zip(bs, ts))
    z = y.col_join(s.kronecker_product(u, y))
    assert s.expand((z.T * matrix * z)[0] - (y.T * s.hessian(f, u) * y)[0]) == 0
    assert matrix.is_positive_definite
    schur = c - d * q.inv() * d.T
    assert (schur - s.Rational(3, 2) * eps * s.Rational(1, 3) ** 2 * s.eye(n)).is_positive_definite

    center = s.Matrix([s.Rational(1, 3), s.Rational(2, 7)])
    shift = s.eye(n).row_join(s.zeros(n, n * n)).col_join((-s.kronecker_product(center, s.eye(n))).row_join(s.eye(n * n)))
    original = shift.T * matrix * shift
    perturbation = s.ones(6) * s.Rational(1, 10**20)
    approximate = original + perturbation
    groups = {}
    for i in range(6):
        for j in range(6):
            monomial = s.expand(z[i] * z[j])
            groups.setdefault(monomial, []).append((i, j))
    projected = approximate.copy()
    for entries in groups.values():
        correction = sum(original[i, j] - approximate[i, j] for i, j in entries) / len(entries)
        for i, j in entries:
            projected[i, j] += correction
    assert s.expand((z.T * (projected - original) * z)[0]) == 0
    assert projected.is_positive_definite
    assert sum(x * x for x in projected - original) <= sum(x * x for x in perturbation)


if __name__ == "__main__":
    count = signal_checks()
    exposing_checks()
    gram_checks()
    print(f"PASS: 2 exact signal-generator steps; {count} signed/cancelling gate cases; shared-parent quaternion exposing identities; rounded zero; full Hessian Gram and affine projection.")
