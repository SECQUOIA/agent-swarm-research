#!/usr/bin/env python3
"""Exact diagnostics for S5a's polynomial/capacity measurement extension.

Small cases only: rational simplex LP for sign cones, exact polynomial
balance and capacity signs, separate root brackets for comparison. This
is not an implementation of the general monotone-root or convex oracle.
"""
from fractions import Fraction as F
from itertools import product
import sympy as sp
from sympy.solvers.simplex import InfeasibleLPError, lpmin


def balance(q, theta, degree):
    alpha, gamma = theta
    return (2 + gamma) * (q + 1)**degree + (1 + alpha) * q**degree


def bracket(theta, degree, width=F(1, 2**75)):
    lo, hi = F(-1), F(0)
    while hi - lo > width:
        q = (lo + hi) / 2
        value = balance(q, theta, degree)
        if value == 0:
            return q, q
        if value < 0:
            lo = q
        else:
            hi = q
    return lo, hi


def interpolate(q, degree, vertices):
    low = min(vertices, key=lambda t: balance(q, t, degree))
    high = max(vertices, key=lambda t: balance(q, t, degree))
    lv, hv = balance(q, low, degree), balance(q, high, degree)
    assert lv <= 0 <= hv
    lam = -lv / (hv - lv) if hv != lv else F(0)
    theta = tuple((1 - lam) * a + lam * b for a, b in zip(low, high))
    assert balance(q, theta, degree) == 0
    assert theta[0] >= 0 and theta[1] >= 0
    assert 3 * theta[0] + 2 * theta[1] <= 6
    return theta


def rational_cones(directions):
    h = sp.symbols('h:2')
    patterns = [()]
    for index in range(len(directions)):
        new = []
        for prefix in patterns:
            for sign in (-1, 1):
                pattern = prefix + (sign,)
                constraints = [s * sum(a * z for a, z in zip(row, h)) >= 1
                               for s, row in zip(pattern, directions)]
                try:
                    _, witness = lpmin(0, constraints)
                except InfeasibleLPError:
                    continue
                assert all(bool(c.subs(witness)) for c in constraints)
                new.append(pattern)
        patterns = new
    return patterns


def run():
    vertices = [(F(0), F(0)), (F(2), F(0)), (F(0), F(3))]
    # Positive polynomial laws on triangle paths: alternate coefficient
    # sum 2+gamma, direct coefficient 1+alpha, degrees 3,5,7,9.
    degrees = [3, 5, 7, 9, 3, 5]
    directions = [(1, 0), (0, 1), (1, 1), (1, 0), (-1, 1), (0, 0)]
    local_bounds = [(F(-3, 5), F(-12, 25))] * 6
    endpoint_profiles = []
    rational_clips = 0
    for i, (degree, (a, b)) in enumerate(zip(degrees, local_bounds)):
        lower, upper = vertices[2], vertices[1]
        # Ratio (2+gamma)/(1+alpha) is largest/smallest here.
        if balance(a, lower, degree) > 0:
            lower = interpolate(a, degree, vertices)
            rational_clips += 1
        if balance(b, upper, degree) < 0:
            upper = interpolate(b, degree, vertices)
            rational_clips += 1
        if i == 3:
            # A singleton parameter polytope gives an irrational singleton
            # physical interval. Preserve its rational original profile.
            lower = upper = vertices[0]
        for theta in (lower, upper):
            assert balance(a, theta, degree) <= 0 <= balance(b, theta, degree)
        endpoint_profiles.append((lower, upper))

    keep = [i for i, row in enumerate(directions) if any(row)]
    patterns = rational_cones([directions[i] for i in keep])
    candidates = []
    for pattern in patterns:
        bits = [0] * len(degrees)
        for i, sign in zip(keep, pattern):
            bits[i] = int(sign > 0)
        candidates.append(tuple(bits))
    roots = [[bracket(t, d) for t in ends]
             for d, ends in zip(degrees, endpoint_profiles)]
    epsilon = F(1, 2**20)
    # Both measurement magnitudes are <=6; root midpoint error <=2^-75.
    # For g=sum(y^4+y^2)+y0-2y1, |partial_j g|<=4*7^3+14+2.
    lip = 4 * 7**3 + 14 + 2
    value_error = 2 * lip * 6 * F(1, 2**75)

    def estimate(bits):
        q = [sum(ends[bit], F(0)) / 2 for ends, bit in zip(roots, bits)]
        y = [sum(a[j] * x for a, x in zip(directions, q)) for j in range(2)]
        return sum(z**4 + z**2 for z in y) + y[0] - 2*y[1]

    winner = max(candidates, key=estimate)
    all_bits = list(product((0, 1), repeat=len(degrees)))
    assert max(map(estimate, all_bits)) + value_error <= (
        estimate(winner) - value_error + epsilon)
    for i, bit in enumerate(winner):
        a, b = local_bounds[i]
        theta = endpoint_profiles[i][bit]
        assert balance(a, theta, degrees[i]) <= 0 <= balance(b, theta, degrees[i])

    # Shared parameters in two distinct cycles: exact capacity halfspaces.
    alpha, gamma = sp.symbols('alpha gamma')
    domain = [alpha >= 0, gamma >= 0, 3*alpha + 2*gamma <= 6]
    parameter = (alpha, gamma)
    constraints = domain + [balance(F(-3, 5), parameter, 3) <= 0,
                            balance(F(-1, 2), parameter, 3) >= 0,
                            balance(F(-3, 5), parameter, 5) <= 0,
                            balance(F(-1, 2), parameter, 5) >= 0]
    _, witness = lpmin(0, constraints)
    theta = tuple(F(witness[z]) for z in parameter)
    assert all(bool(c.subs(witness)) for c in constraints)
    for degree in (3, 5):
        assert balance(F(-3, 5), theta, degree) <= 0
        assert balance(F(-1, 2), theta, degree) >= 0
    # A second passive triangle has alternate coefficient sum 1+gamma
    # (split equally over two edges) and direct coefficient 1+alpha.
    def second_balance(q):
        return (1 + gamma) * (q + 1)**5 + (1 + alpha) * q**5

    # Incompatible globally shared physical capacities at q=-1/2:
    # first root >= -1/2 forces gamma-alpha<=-1; second root <= -1/2
    # forces gamma-alpha>=0.
    impossible = domain + [balance(F(-1, 2), parameter, 3) <= 0,
                           second_balance(F(-1, 2)) >= 0]
    try:
        lpmin(0, impossible)
        raise AssertionError('Globally inconsistent capacities accepted')
    except InfeasibleLPError:
        pass
    assert rational_clips and patterns
    print(f'PASS: {len(patterns)} exact rational cones; {len(all_bits)} '
          f'polynomial endpoint scenarios; {rational_clips} rational clips; '
          'degree-3..9 laws, repeated/zero directions, irrational singleton; '
          'exact shared-parameter feasible and infeasible capacity LPs')


if __name__ == '__main__':
    run()
