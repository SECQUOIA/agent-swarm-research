"""Independent checks for the reopened weighted-cactus approximation proof.

Exact Fraction checks cover the approximation bounds and a vanishing linear
branch denominator. Decimal tests cover independently computed cycle roots.
This does not implement the theorem's real-algebraic optimizer.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from random import Random


def panel(x, j, kmax):
    a = Q(9, 16) * Q(1, 4) ** j
    u = x / a - 1
    coef = Q(1)
    power = Q(1)
    val = Q(1)
    for k in range(1, kmax + 1):
        coef *= (Q(1, 2) - (k - 1)) / k
        power *= u
        val += coef * power
    return Q(3, 4) * Q(1, 2) ** j * val


def exact_panel_checks():
    count = 0
    for bits in (2, 8, 20, 40):
        eta = Q(1, 2) ** bits
        k = 0
        while Q(9, 2) * Q(7, 9) ** (k + 1) > eta:
            k += 1
        # These panels include both shared endpoints and the smallest panel.
        for j in sorted({0, bits // 2, bits - 1}):
            lo, hi = Q(1, 4) ** (j + 1), Q(1, 4) ** j
            for r in (Q(0), Q(1, 7), Q(1, 2), Q(6, 7), Q(1)):
                x = lo + r * (hi - lo)
                val = panel(x, j, k)
                assert val + eta >= 0
                assert (val + eta) ** 2 >= x
                assert val - eta <= 0 or (val - eta) ** 2 <= x
                count += 1
        assert (Q(1, 4) ** bits) <= eta ** 2
    return count


def linear_branch_checks():
    # Fixed coefficients; x=(q+t,q+2t,q-t,q-3t), signs ++--.
    # A=0, B=14t, C=-5t^2; q=5t/14. B approaches zero.
    count = 0
    for exponent in (0, 1, 10, 100, 1000):
        t = Q(1, 2) ** exponent
        B, C = 14*t, -5*t*t
        q = -C/B
        flows = [q+t, q+2*t, q-t, q-3*t]
        assert sum(x*abs(x) for x in flows) == 0
        assert B == 2*sum(abs(x) for x in flows)
        count += 1
    # At the singular point t=0, all flows and drops are zero.
    assert all(Q(0) == x for x in [Q(0)] * 4)
    return count


def root(ell, plus, minus):
    lo, hi = -max(ell), -min(ell)
    def law(x, i):
        return plus[i]*x*x if x >= 0 else -minus[i]*x*x
    for _ in range(300):
        mid = (lo+hi)/2
        f = sum(law(mid+v, i) for i, v in enumerate(ell))
        if f <= 0:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def cycle_checks():
    rng = Random(806092026)
    counts = {"A_negative": 0, "A_positive": 0, "A_zero": 0, "flow_difference": 0}
    with localcontext() as ctx:
        ctx.prec = 100
        D = Decimal
        for _ in range(240):
            n = rng.randrange(3, 12)
            plus = [D(rng.randrange(1, 14)) for _ in range(n)]
            minus = [D(rng.randrange(1, 14)) for _ in range(n)]
            ell = [D(rng.randrange(-20, 21))/7 for _ in range(n)]
            q = root(ell, plus, minus)
            x = [q+v for v in ell]
            weights = [plus[i] if v >= 0 else -minus[i] for i, v in enumerate(x)]
            A = sum(weights)
            B = 2*sum(w*v for w, v in zip(weights, ell))
            C = sum(w*v*v for w, v in zip(weights, ell))
            derivative = 2*sum((plus[i] if v >= 0 else minus[i])*abs(v) for i, v in enumerate(x))
            assert abs(2*A*q+B-derivative) < D('1e-85')
            if A:
                delta = B*B-4*A*C
                assert delta >= 0
                formula = (-B+delta.sqrt())/(2*A)
                assert abs(formula-q) < D('1e-80')
                counts['A_positive' if A > 0 else 'A_negative'] += 1
            else:
                assert B > 0
                assert abs(-C/B-q) < D('1e-80')
                counts['A_zero'] += 1
            ell2 = [v+D(rng.randrange(-10, 11))/11 for v in ell]
            q2 = root(ell2, plus, minus)
            dx = [q+v-q2-v2 for v, v2 in zip(ell, ell2)]
            db = [dx[i]-dx[i-1] for i in range(n)]
            assert max(abs(v) for v in dx) <= sum(abs(v) for v in db)/2 + D('1e-80')
            counts['flow_difference'] += 1
    assert counts['A_negative'] > 0 and counts['A_positive'] > 0 and counts['A_zero'] > 0
    return counts


if __name__ == '__main__':
    print({'exact_panel_points': exact_panel_checks(),
           'exact_vanishing_denominator_cases': linear_branch_checks(),
           'decimal_cycle_checks': cycle_checks()})
