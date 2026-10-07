"""Exact small diagnostics for the cubic-recourse theorem, not its full solver."""

from fractions import Fraction as Q
from itertools import product
import json

from sympy import Matrix


def clip(x):
    return min(Q(1), max(Q(0), x))


def core(gamma):
    # F(v,z)=v^2(2-z)-v; min_z F_gamma=v^2+(gamma-1)v.
    return clip((1 - gamma) / 2)


def dyadic_down(x, error):
    den = 1
    while Q(1, den) > error:
        den *= 2
    return Q((x * den).numerator // (x * den).denominator, den)


counts = {"face_draws": 0, "forced_endpoints": 0,
          "point_completions": 0, "lattice_margin_checks": 0,
          "lattice_acceptances": 0, "exact_relation_rejections": 0}
t = Q(1, 16)
Lbar = Q(4)
r = t / (8 * Lbar)
grid = [Q(-2) + Q(4 * i, 256) for i in range(257)]
missed = 0
for gamma in grid:
    a = core(gamma)
    bminus = core(gamma - t)
    bplus = core(gamma + t)
    # Deliberately use enclosures of positive radius, including at endpoints.
    fix_zero = bminus + r < t / Lbar
    fix_one = bplus - r > 1 - t / Lbar
    assert not (fix_zero and fix_one)
    if fix_zero:
        assert a == 0
    if fix_one:
        assert a == 1
    if a in (0, 1) and not (fix_zero or fix_one):
        missed += 1
    counts["face_draws"] += 1
    counts["forced_endpoints"] += int(fix_zero or fix_one)
assert Q(missed, len(grid)) <= t / 2 + Q(4, len(grid))

# Fixed selected optimizer is (a,1) when a>0 and (0,0) when a=0.
# Include extremely small positive free cores and exact boundary cores.
for a in [Q(0), Q(1), Q(1, 3), Q(7, 11), Q(1, 2**40), Q(1, 2**120)]:
    p = Q(int(a > 0))
    Gamma = max(Q(1), Q(1, a * a)) if a else Q(1)
    for q in (0, 2, 5, 10):
        eps = Q(1, 2**q)
        e = eps / 2
        tau = e**6 / (1024 * Gamma**4)
        G = Q(4)
        dq = min(eps / 2, tau * e * e / (32 * G))
        b = a if a in (0, 1) else dyadic_down(a, dq / 2)
        assert abs(b - a) <= dq
        z = clip(b * b / (2 * tau))
        assert (b - a)**2 + (z - p)**2 <= eps**2
        # Exact stationary/end-point tangent certificate for Q_b.
        grad = -b * b + 2 * tau * z
        tangent_gap = -grad * z if grad >= 0 else grad * (1 - z)
        assert tangent_gap == 0
        counts["point_completions"] += 1

# Actual LLL acceptance test from the lemma, followed by exhaustive checks
# only for this tiny height-one family. Production does not enumerate it.
s = 3
B = 1
T = 2**80
for a in [Q(123457 + 11317 * i, 1000003) for i in range(9)]:
    phi = [Q(1), a, a * a]
    b = dyadic_down(a, Q(1, 8 * T))
    phib = [Q(1), b, b * b]
    w = [int(x * T + Q(1, 2)) for x in phib]
    basis = Matrix([[int(i == j) for j in range(s)] + [w[i]]
                    for i in range(s)])
    reduced, transform = basis.lll_transform(delta=Q(3, 4))
    assert transform * basis == reduced
    assert abs(transform.det()) == 1
    norm2 = sum(int(x)**2 for x in reduced.row(0))
    accepted = norm2 > 2**(s - 1) * (4 * s * B)**2
    if accepted:
        counts["lattice_acceptances"] += 1
        for h in product(range(-B, B + 1), repeat=s):
            if not any(h):
                continue
            assert abs(sum(c * x for c, x in zip(h, phi))) > Q(s * B, T)
            counts["lattice_margin_checks"] += 1
assert counts["lattice_acceptances"] > 0
# At 0 and 1 an exact relation lies inside P_B. At 1/2, 2*x-1 has
# height two: rejection from this larger family is allowed by the
# sufficient (not necessary) acceptance test.
for a in (Q(0), Q(1), Q(1, 2)):
    for T in (2**16, 2**32, 2**64):
        phi = [Q(1), a, a*a]
        w = [int(x*T + Q(1, 2)) for x in phi]
        basis = Matrix([[int(i == j) for j in range(s)] + [w[i]]
                        for i in range(s)])
        reduced = basis.lll(delta=Q(3, 4))
        norm2 = sum(int(x)**2 for x in reduced.row(0))
        assert norm2 <= 2**(s-1) * (4*s*B)**2
        counts["exact_relation_rejections"] += 1

print(json.dumps({"status": "passed", **counts}, indent=2))
