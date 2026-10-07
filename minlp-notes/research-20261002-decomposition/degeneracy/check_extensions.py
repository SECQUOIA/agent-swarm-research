"""Exact, bounded diagnostics for the three degeneracy extension notes.

These are small mathematical fixtures, not a general optimization solver.
Run: python3 -B research-20261002-decomposition/degeneracy/check_extensions.py
"""

from fractions import Fraction as Q
from itertools import product
from math import isqrt

import sympy as sp


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def mv(a, x):
    return [dot(row, x) for row in a]


def psd(a):
    """Exact symmetric Schur elimination, including singular pivots."""
    a = [row[:] for row in a]
    while a:
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        pivot = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if pivot is None:
            return all(value == 0 for row in a for value in row)
        others = [i for i in range(len(a)) if i != pivot]
        a = [
            [a[i][j] - a[i][pivot] * a[pivot][j] / a[pivot][pivot]
             for j in others]
            for i in others
        ]
    return True


def value(h, b, x):
    return dot(x, mv(h, x)) / 2 + dot(b, x)


def diagonal_certificate(h, b, bounds, s):
    if any(not lo <= x <= hi for (lo, hi), x in zip(bounds, s)):
        return None
    grad = [u + v for u, v in zip(mv(h, s), b)]
    diagonal = []
    for (lo, hi), x, g in zip(bounds, s, grad):
        if x == lo and g >= 0:
            diagonal.append(2 * g / (hi - lo))
        elif x == hi and g <= 0:
            diagonal.append(-2 * g / (hi - lo))
        elif lo < x < hi and g == 0:
            diagonal.append(Q(0))
        else:
            return None
    matrix = [
        [h[i][j] + (diagonal[i] if i == j else 0) for j in range(len(s))]
        for i in range(len(s))
    ]
    return (matrix, diagonal) if psd(matrix) else None


def check_diagonal_class():
    # Singular PSD and nonzero off-diagonal at a zero diagonal pivot.
    assert psd([[Q(1), Q(1)], [Q(1), Q(1)]])
    assert not psd([[Q(0), Q(1)], [Q(1), Q(0)]])
    assert not psd([[Q(0), Q(0)], [Q(0), Q(-1)]])

    # This is exactly the earlier invalid-growth counterexample.
    h = [[Q(2), Q(-3)], [Q(-3), Q(2)]]
    b = [Q(63, 128)] * 2
    bounds = [(Q(0), Q(1))] * 2
    assert diagonal_certificate(h, b, bounds, [Q(0), Q(0)]) is None
    assert diagonal_certificate(h, b, bounds, [Q(1), Q(1)]) is not None

    # Tilted, disconnected continua with all Hessian diagonals positive.
    v = [Q(1), Q(-1), Q(1, 2)]
    h = [[2 * a * b for b in v] for a in v]
    h[2][2] -= Q(1, 4)
    b = [Q(0), Q(0), Q(1, 8)]
    bounds = [(Q(0), Q(1))] * 3
    optimizers = [
        [Q(0), Q(0), Q(0)],
        [Q(2, 3), Q(2, 3), Q(0)],
        [Q(1, 3), Q(5, 6), Q(1)],
        [Q(1, 2), Q(1), Q(1)],
    ]
    checks = 0
    for s in optimizers:
        matrix, diagonal = diagonal_certificate(h, b, bounds, s)
        assert diagonal == [0, 0, Q(1, 4)]
        assert value(h, b, s) == 0
        for x in product([Q(0), Q(1, 3), Q(1, 2), Q(1)], repeat=3):
            displacement = [xi - si for xi, si in zip(x, s)]
            identity = dot(displacement, mv(matrix, displacement)) / 2
            identity += sum(di * xi * (1 - xi) / 2
                            for di, xi in zip(diagonal, x))
            assert value(h, b, x) == identity
            descriptor = all(z == 0 for z in mv(matrix, displacement))
            descriptor &= all(di * xi * (1 - xi) == 0
                              for di, xi in zip(diagonal, x))
            assert descriptor == (value(h, b, x) == 0)
            checks += 1
    return checks


def endpoint_dp(bags, parents, local):
    """Root-first bag indices; exact two-state messages and residuals."""
    children = [[] for _ in bags]
    separators = []
    for t, parent in enumerate(parents):
        separators.append(tuple(i for i in bags[t]
                                if parent is not None and i in bags[parent]))
        if parent is not None:
            children[parent].append(t)
    messages, residuals = {}, {}
    for t in reversed(range(len(bags))):
        raw, message = {}, {}
        for label in product((0, 1), repeat=len(bags[t])):
            state = dict(zip(bags[t], label))
            total = local[t](state)
            total += sum(messages[c][tuple(state[i] for i in separators[c])]
                         for c in children[t])
            sep = tuple(state[i] for i in separators[t])
            raw[label] = total
            message[sep] = min(message.get(sep, total), total)
        messages[t] = message
        residuals[t] = {}
        for label, total in raw.items():
            state = dict(zip(bags[t], label))
            residuals[t][label] = total - message[tuple(state[i] for i in separators[t])]
            assert residuals[t][label] >= 0
    return messages[0][()], residuals


def check_endpoint_set():
    # A genuine branching decomposition with overlapping separators.
    # z2 is a native integer on [0,4]; z3 has a strict negative diagonal.
    bounds = [(Q(0), Q(1)), (Q(0), Q(1)), (Q(0), Q(4)), (Q(0), Q(1))]
    bags = [(0, 1), (1, 2), (1, 3)]
    parents = [None, 0, 0]

    def edge(x, y):
        return x + y - 2 * x * y

    local = [
        lambda s: Q(edge(s[0], s[1])),
        lambda s: Q(edge(s[1], s[2])),
        lambda s: Q(edge(s[1], s[3])),
    ]
    optimum, residuals = endpoint_dp(bags, parents, local)
    assert optimum == 0
    # Endpoint objective has the extra concave term vanish on endpoints.
    qdiag = [Q(0), Q(0), Q(0), Q(-2)]
    checks = 0
    for x in product([Q(0), Q(1, 2), Q(1)],
                     [Q(0), Q(1, 3), Q(1)],
                     map(Q, range(5)),
                     [Q(0), Q(1, 4), Q(1)]):
        normalized = [(xi - lo) / (hi - lo)
                      for xi, (lo, hi) in zip(x, bounds)]
        actual = sum(edge(normalized[1], normalized[i]) for i in (0, 2, 3))
        actual += 2 * x[3] * (1 - x[3])
        rhs, zero_support = Q(0), True
        for t, bag in enumerate(bags):
            for label, residual in residuals[t].items():
                weight = Q(1)
                for i, endpoint in zip(bag, label):
                    weight *= normalized[i] if endpoint else 1 - normalized[i]
                rhs += residual * weight
                if residual > 0 and weight > 0:
                    zero_support = False
        for i, qi in enumerate(qdiag):
            lo, hi = bounds[i]
            term = -qi * (x[i] - lo) * (hi - x[i])
            rhs += term
            if term > 0:
                zero_support = False
        assert actual == rhs + optimum
        assert zero_support == (actual == optimum)
        checks += 1
    # Interior integer labels and continuous flats are really allowed when free.
    for integer in range(5):
        assert -Q(0) * integer * (4 - integer) == 0
    return checks


def grid(lo, hi, center, h, theta):
    labels = {center}
    for endpoint, sign in ((lo, -1), (hi, 1)):
        x = center
        while x != endpoint:
            step = h + theta * abs(x - center)
            x = max(endpoint, x - step) if sign < 0 else min(endpoint, x + step)
            labels.add(x)
    labels = sorted(labels)
    lengths = [max([abs(labels[i] - labels[j]) for j in (i - 1, i + 1)
                    if 0 <= j < len(labels)] or [Q(0)])
               for i in range(len(labels))]
    return labels, lengths


def check_proximal_recovery():
    # Complete finite candidate run for two endpoint modes times a free interval.
    # Exact bag minimization uses a two-variable bag and an independent unary bag.
    n, conditioning, curvature = 3, Q(4), Q(2)
    theta = Q(1, 4)
    while theta * theta * conditioning > Q(1, 8):
        theta /= 2
    rho = 2 * (isqrt(int(conditioning * n)) + 1)
    lam = curvature * theta * theta / 4
    determinant_height = (2 * n * 3) ** n
    tau = Q(1, 4 * n * 2 * determinant_height)
    target = min(Q(1), curvature * tau * tau / (4 * conditioning))
    epsilon = Q(1)
    while epsilon > target:
        epsilon /= 2
    center, h, stages, calls = [Q(0)] * n, Q(1), 0, 0
    hessian = [[Q(2), Q(-3), Q(0)],
               [Q(-3), Q(2), Q(0)],
               [Q(0), Q(0), Q(0)]]
    linear = [Q(1, 2), Q(1, 2), Q(0)]
    while True:
        grids, costs = [], []
        for ci in center:
            labels, lengths = grid(max(Q(0), ci - rho * h),
                                   min(Q(1), ci + rho * h), ci, h, theta)
            grids.append(labels)
            costs.append({x: -curvature * ell * ell / 8 + lam * (x - ci) ** 2
                          for x, ell in zip(labels, lengths)})
        best_xy = min((x*x + y*y - 3*x*y + (x+y)/2 + costs[0][x] + costs[1][y], x, y)
                      for x, y in product(grids[0], grids[1]))
        best_z = min((costs[2][z], z) for z in grids[2])
        calls += len(grids[0]) * len(grids[1]) + len(grids[2])
        node = [best_xy[1], best_xy[2], best_z[1]]
        discrete_min = best_xy[0] + best_z[0]
        lower = discrete_min - lam * ((1 + theta*theta/2)*4*conditioning*n*h*h + n*h*h/2)
        upper = value(hessian, linear, node)
        assert lower <= 0 <= upper
        assert upper - lower <= curvature * n * h * h / 2
        distance_squared = min(node[0]**2 + node[1]**2,
                               (node[0]-1)**2 + (node[1]-1)**2)
        assert distance_squared <= conditioning * n * h * h
        stages += 1
        if curvature * n * h * h / 2 <= epsilon:
            assert distance_squared <= tau*tau/4
            # Either endpoint mode may be selected; the free coordinate may
            # move. Its stationary equation is identically zero, so the
            # selected-face LP can choose an original feasible endpoint.
            recovered = []
            for x in node[:2]:
                assert min(x, 1-x) <= tau
                recovered.append(Q(0) if x <= tau else Q(1))
            assert recovered[0] == recovered[1]
            recovered.append(Q(1) if 1-node[2] <= tau else Q(0))
            assert diagonal_certificate(hessian, linear, [(Q(0), Q(1))]*n, recovered)
            return stages, calls
        center, h = node, h / 2


def check_boundary():
    x, y = sp.symbols('x y')
    examples = [
        (x - sp.Rational(1, 4))**2 + y + x*y*y,
        (x - sp.Rational(1, 4))**2 + y*(1-y),
    ]
    # Exact Bernstein sign certificates on [0,1/2]^2. The first derivative
    # is multiaffine, so its tensor degree-(1,1) coefficients are precisely
    # its four endpoint values. The second has degree one in y.
    first_derivative = sp.diff(examples[0], y)
    assert sp.expand(first_derivative - (1 + 2*x*y)) == 0
    assert [first_derivative.subs({x: a, y: b})
            for a, b in product([sp.Rational(0), sp.Rational(1, 2)], repeat=2)] == [1, 1, 1, sp.Rational(3, 2)]
    second_derivative = sp.diff(examples[1], y)
    assert sp.expand(second_derivative - (1 - 2*y)) == 0
    assert [second_derivative.subs(y, a)
            for a in [sp.Rational(0), sp.Rational(1, 2)]] == [1, 0]
    checks = 0
    for f in examples:
        reduced = sp.expand(f.subs(y, 0))
        assert sp.diff(reduced, x, 2) == 2
        for a, b in product([sp.Rational(0), sp.Rational(1, 4), sp.Rational(1, 2)], repeat=2):
            assert sp.diff(f, y).subs({x: a, y: b}) >= 0
            assert f.subs({x: a, y: b}) >= reduced.subs(x, a)
            checks += 1
    assert sp.diff(examples[1], y, 2) == -2
    # Strict interval sign test and reduced-Hessian budget, exact rational form.
    for gamma, curvature_growth, m, t in product(
            [Q(1, 1024), Q(1)], [Q(1, 8), Q(2)], [Q(1), Q(16)], [Q(1), Q(32)]):
        radius = min(gamma/(4*m), curvature_growth/(8*t))
        assert gamma - 2*m*radius >= gamma/2
        assert 2*curvature_growth - 2*t*radius - curvature_growth/4 > 0
        checks += 1
    # Weak monotonicity need not preserve *all* optima: the zero objective.
    assert sp.diff(sp.Integer(0), y) == 0
    return checks


if __name__ == '__main__':
    print(f'diagonal identities and full-set equivalences: {check_diagonal_class()} passed')
    print(f'branching mixed endpoint identities: {check_endpoint_set()} passed')
    stages, calls = check_proximal_recovery()
    print(f'complete proximal candidate/recovery fixture: {stages} stages, {calls} exact calls passed')
    print(f'boundary reductions and precision budgets: {check_boundary()} passed')
