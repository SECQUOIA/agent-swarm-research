"""Exact diagnostic of mixed recourse on ambient-noise coordinate lines.

This checks finite critical-region coverage, boundary overlaps, quadratic
value formulas, and branch gradients. It does not implement the solver or
test the expectation theorem by sampling. Uses Python's standard library.
"""

from fractions import Fraction as F
from itertools import product


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


ALPHA = F(4)
T = ((F(1, 4), F(1, 4), F(0)),
     (F(0), F(1, 4), F(1, 4)))
COLS = tuple(zip(*T))
# D=(TT^T)^(-1)T; the explicit rational values are checked below.
D = ((F(8, 3), F(4, 3), F(-4, 3)),
     (F(-4, 3), F(4, 3), F(8, 3)))

# Each piece is (left, right, quadratic curvature, linear term, constant).
PIECES = (
    ((F(-2), F(0), F(1), F(0), F(0)),
     (F(0), F(3), F(0), F(1), F(0))),
    ((F(-1), F(0), F(1), F(-1), F(0)),
     (F(0), F(1), F(0), F(0), F(0)),
     (F(1), F(2), F(2), F(-2), F(1))),
    ((F(-1), F(0), F(0), F(-1), F(0)),
     (F(0), F(1), F(0), F(1), F(0))),
)


def phi(i, x):
    values = [p * x * x / 2 + b * x + c
              for left, right, p, b, c in PIECES[i]
              if left <= x <= right]
    assert values and all(v == values[0] for v in values)
    return values[0]


def make_states(i):
    # State: (lower tilt, upper tilt, A, B, p, b, c), x=A*tilt+B.
    if i == 0:
        lo, hi = -2, 3
        return [(None if z == lo else phi(i, F(z)) - phi(i, F(z - 1)),
                 None if z == hi else phi(i, F(z + 1)) - phi(i, F(z)),
                 F(0), F(z), F(0), F(0), phi(i, F(z)))
                for z in range(lo, hi + 1)]
    pieces = PIECES[i]
    states = []
    for left, right, p, b, c in pieces:
        if p > 0:
            states.append((p * left + b, p * right + b,
                           1 / p, -b / p, p, b, c))
    knots = [pieces[0][0]] + [piece[1] for piece in pieces]
    for j, knot in enumerate(knots):
        lower = None if j == 0 else pieces[j - 1][2] * knot + pieces[j - 1][3]
        upper = None if j == len(pieces) else pieces[j][2] * knot + pieces[j][3]
        states.append((lower, upper, F(0), knot, F(0), F(0), phi(i, knot)))
    return states


STATES = tuple(make_states(i) for i in range(3))


def split_noise(gamma):
    d = tuple(dot(row, gamma) for row in D)
    residual = tuple(gamma[i] - dot(COLS[i], d) for i in range(3))
    assert all(dot(row, residual) == 0 for row in T)
    return d, residual


def scalar_oracle(i, tilt):
    # Independent candidate enumeration, without using state inequalities.
    if i == 0:
        candidates = [F(z) for z in range(-2, 4)]
    else:
        candidates = []
        for left, right, p, b, _ in PIECES[i]:
            candidates.extend((left, right))
            if p > 0 and left <= (tilt - b) / p <= right:
                candidates.append((tilt - b) / p)
    return min(phi(i, x) - tilt * x for x in candidates)


def actual_value(a, gamma):
    d, residual = split_noise(gamma)
    tilts = tuple(ALPHA * dot(COLS[i], a) - residual[i] for i in range(3))
    return ALPHA * dot(a, a) / 2 + dot(d, a) + sum(
        (scalar_oracle(i, tilt) for i, tilt in enumerate(tilts)), F(0))


def branch_value(a, d, residual, states):
    result = ALPHA * dot(a, a) / 2 + dot(d, a)
    witness = []
    for i, (_, _, slope, intercept, p, b, c) in enumerate(states):
        tilt = ALPHA * dot(COLS[i], a) - residual[i]
        x = slope * tilt + intercept
        witness.append(x)
        result += p * x * x / 2 + b * x + c - tilt * x
    return result, tuple(witness)


def active_states(a, gamma):
    d, residual = split_noise(gamma)
    choices = []
    for i in range(3):
        tilt = ALPHA * dot(COLS[i], a) - residual[i]
        eligible = [state for state in STATES[i]
                    if (state[0] is None or state[0] <= tilt)
                    and (state[1] is None or tilt <= state[1])]
        assert eligible
        choices.append(eligible)
    return d, residual, choices


def gamma_on_line(fixed, axis, value):
    gamma = list(fixed)
    gamma[axis] = value
    return tuple(gamma)


counts = dict(lines=0, boundary_queries=0, open_intervals=0,
              active_branches=0, overlap_queries=0, gradient_identities=0,
              polynomial_identities=0)


def check_query(a, gamma, boundary=False):
    d, residual, choices = active_states(a, gamma)
    reference = actual_value(a, gamma)
    branches = list(product(*choices))
    counts["boundary_queries"] += int(boundary)
    counts["overlap_queries"] += int(len(branches) > 1)
    for states in branches:
        value, witness = branch_value(a, d, residual, states)
        assert value == reference
        # Differentiate the quadratic extension algebraically by exact
        # central differences, even if the region is lower-dimensional.
        for axis in range(2):
            plus, minus = list(a), list(a)
            plus[axis] += 1
            minus[axis] -= 1
            derivative = (branch_value(plus, d, residual, states)[0]
                          - branch_value(minus, d, residual, states)[0]) / 2
            assert derivative == ALPHA * (a[axis] - dot(T[axis], witness)) + d[axis]
            counts["gradient_identities"] += 1
        counts["active_branches"] += 1
    return branches[0]


def check_line(a, fixed, axis):
    gamma0, gamma1 = (gamma_on_line(fixed, axis, t) for t in (F(0), F(1)))
    _, residual0 = split_noise(gamma0)
    _, residual1 = split_noise(gamma1)
    cuts = set()
    for i in range(3):
        intercept = ALPHA * dot(COLS[i], a) - residual0[i]
        slope = residual0[i] - residual1[i]
        if slope:
            for state in STATES[i]:
                for boundary in state[:2]:
                    if boundary is not None:
                        cuts.add((boundary - intercept) / slope)
    cuts = sorted(cuts)
    for cut in cuts:
        check_query(a, gamma_on_line(fixed, axis, cut), boundary=True)
    # Cover both unbounded tails with bounded test subintervals. All finite
    # state boundaries have been enumerated exactly.
    endpoints = [cuts[0] - 2] + cuts + [cuts[-1] + 2]
    for left, right in zip(endpoints, endpoints[1:]):
        midpoint = (left + right) / 2
        states = check_query(a, gamma_on_line(fixed, axis, midpoint))
        # Recover the branch's quadratic polynomial on the full ambient
        # line, then compare inside this interval to independent recourse.
        values = []
        for t in (F(0), F(1), F(2)):
            d, residual = split_noise(gamma_on_line(fixed, axis, t))
            values.append(branch_value(a, d, residual, states)[0])
        c = values[0]
        q = (values[2] - 2 * values[1] + values[0]) / 2
        b = values[1] - c - q
        for fraction in (F(1, 5), F(2, 5), F(3, 5), F(4, 5)):
            t = left + fraction * (right - left)
            gamma = gamma_on_line(fixed, axis, t)
            d, residual = split_noise(gamma)
            assert branch_value(a, d, residual, states)[0] == q * t * t + b * t + c
            assert actual_value(a, gamma) == q * t * t + b * t + c
            counts["polynomial_identities"] += 1
        counts["open_intervals"] += 1
    counts["lines"] += 1


for i in range(2):
    for j in range(2):
        assert dot(D[i], T[j]) == int(i == j)

for a in ((F(0), F(0)), (F(1, 3), F(-1, 2)),
          (F(2), F(1)), (F(-3, 4), F(5, 4))):
    for fixed in ((F(0), F(0), F(0)),
                  (F(1, 3), F(-2, 5), F(4, 7))):
        for axis in range(3):
            check_line(a, fixed, axis)

assert counts["overlap_queries"] > 0
print("PASS:", ", ".join(f"{key}={value}" for key, value in counts.items()))
