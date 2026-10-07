"""M5: exact check of the chord curvature correction (Report B eq. chord-correction).

Claim: if p is C^2 on [a,b] and p'' <= M there, then
    min_[a,b] p >= min{p(a),p(b)} - max{0,M} (b-a)^2/8,
and for M <= 0 the chord itself is a lower bound.
Refinement checked here: with q(t) = chord_p(t) - (M/2)(t-a)(b-t),
p >= q on [a,b], so min_[a,b] q is a valid (and, given only p(a), p(b), M,
best possible) lower bound.  All checks are exact: nonnegativity of a
polynomial on a rational interval is decided with a square-free
decomposition and exact real-root counting.
"""
import random
from fractions import Fraction

import sympy as sp

random.seed(5)
t = sp.Symbol("t")


def nonneg_on(r, a, b):
    """Exact test: r(t) >= 0 for all t in [a,b] (a < b rational)."""
    r = sp.Poly(sp.expand(r), t, domain=sp.QQ)
    if r.is_zero:
        return True
    if r.eval(a) < 0 or r.eval(b) < 0:
        return False
    _, factors = r.sqf_list()
    odd = sp.Poly(1, t, domain=sp.QQ)
    for f, mult in factors:
        if mult % 2 == 1:
            odd *= f
    inside = odd.count_roots(a, b) - (odd.eval(a) == 0) - (odd.eval(b) == 0)
    if inside > 0:
        return False  # r changes sign strictly inside (a,b)
    # constant sign on (a,b) apart from even-order zeros: test a non-root point
    k = 2
    while True:
        c = a + (b - a) / k
        if r.eval(c) != 0:
            return r.eval(c) > 0
        k += 1


def rational_upper_bound_of(f, a, b):
    """A rational M with f <= M on [a,b], certified exactly."""
    crit = [a, b] + [x for x in sp.Poly(sp.diff(f, t), t).real_roots() if a <= x <= b]
    m = max(sp.N(f.subs(t, x), 40) for x in crit)
    M = sp.Rational(sp.nsimplify(m, rational=True)) + sp.Rational(1, 10**12)
    assert nonneg_on(M - f, a, b)
    return M


def bounds(p, a, b, M):
    pa, pb = p.subs(t, a), p.subs(t, b)
    h = b - a
    original = min(pa, pb) - max(0, M) * h**2 / 8
    q = pa + (pb - pa) * (t - a) / h - M / 2 * (t - a) * (b - t)
    crit = [a, b]
    if M > 0:
        s = sp.solve(sp.diff(q, t), t)
        crit += [x for x in s if a <= x <= b]
    refined = min(q.subs(t, x) for x in crit)
    return original, refined, q


def main():
    stats = {"cases": 0, "M_negative": 0, "refined_strictly_better": 0}
    for _ in range(150):
        deg = random.randint(2, 5)
        p = sum(sp.Rational(random.randint(-20, 20), random.randint(1, 5)) * t**i for i in range(deg + 1))
        a = sp.Rational(random.randint(-10, 10), random.randint(1, 4))
        b = a + sp.Rational(random.randint(1, 12), random.randint(1, 4))
        M = rational_upper_bound_of(sp.diff(p, t, 2), a, b)
        original, refined, q = bounds(p, a, b, M)
        assert nonneg_on(p - original, a, b), (p, a, b, M)
        assert nonneg_on(p - q, a, b), (p, a, b, M)          # p >= q pointwise
        assert nonneg_on(p - refined, a, b), (p, a, b, M)
        assert refined >= original
        stats["cases"] += 1
        stats["M_negative"] += 1 if M < 0 else 0
        stats["refined_strictly_better"] += 1 if refined > original else 0
        if M <= 0:  # chord is a lower bound
            chord = p.subs(t, a) + (p.subs(t, b) - p.subs(t, a)) * (t - a) / (b - a)
            assert nonneg_on(p - chord, a, b)
    # concave examples with M < 0 explicitly
    # (exact certified curvature bounds: -t^2 has p''=-2; -t^4-t has p''=-12t^2<=0)
    for p, a, b, M in [(-t**2, sp.Integer(-1), sp.Integer(2), sp.Integer(-2)),
                       (-t**4 - t, sp.Integer(0), sp.Integer(1), sp.Integer(0))]:
        assert nonneg_on(M - sp.diff(p, t, 2), a, b)
        original, refined, _ = bounds(p, a, b, M)
        assert refined == original
        assert original == min(p.subs(t, a), p.subs(t, b))
        assert nonneg_on(p - original, a, b)
    # tightness of (b-a)^2/8: p = M (t - m)^2 / 2 with equal endpoint values
    for M in [sp.Integer(1), sp.Rational(7, 3)]:
        a, b = sp.Integer(0), sp.Integer(3)
        p = M * (t - (a + b) / 2) ** 2 / 2
        original, refined, _ = bounds(p, a, b, M)
        assert original == 0 == refined  # equals the true minimum
    # necessity of max{0, M}: using M < 0 without the max would overstate the bound
    p, a, b = -t**2, sp.Integer(0), sp.Integer(2)
    wrong = min(p.subs(t, a), p.subs(t, b)) - sp.Integer(-2) * (b - a) ** 2 / 8
    assert not nonneg_on(p - wrong, a, b)
    print("chord correction checks:", stats)


if __name__ == "__main__":
    main()
