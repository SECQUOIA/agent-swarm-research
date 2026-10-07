"""Lane M1: exact checks of the worked examples in development/M1.md.

All arithmetic is exact (fractions / sympy) unless a line says otherwise.
Run: code/minlp_solver_lab/.venv/bin/python paper-certified-support-cuts/verification/M1_examples.py
"""
from fractions import Fraction as Fr
import random

import sympy as sp

u = sp.symbols("u", real=True)
random.seed(20261003)


def exact_min_on_interval(expr, lo, hi):
    """Exact minimum of a univariate polynomial on [lo, hi] (rational ends)."""
    p = sp.Poly(sp.expand(expr), u)
    cands = [sp.Rational(lo), sp.Rational(hi)]
    dp = p.diff(u)
    if dp.degree() >= 1:
        for r in sp.real_roots(dp):
            if sp.Rational(lo) <= r <= sp.Rational(hi):
                cands.append(r)
    vals = [sp.nsimplify(p.eval(c)) if c.is_Rational else p.eval(c) for c in cands]
    best = min(vals, key=lambda v: sp.N(v, 50))
    return sp.simplify(best)


def check_quarter_example():
    """D=[0,1], equality x^2 = 1/4: closure in x is exactly [1/4, 1/2]."""
    # 1. every cut accepts x = 1/4 (and x = 1/2): random rational (a, nu)
    for _ in range(300):
        a = sp.Rational(random.randint(-40, 40), random.randint(1, 9))
        nu = sp.Rational(random.randint(-40, 40), random.randint(1, 9))
        phi = exact_min_on_interval(a * u + nu * u**2, 0, 1)
        for xbar in (sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 8)):
            # cut: a*x >= phi - nu/4
            assert a * xbar - (phi - nu / 4) >= 0, (a, nu, xbar)
    # 2. two explicit cuts give x >= 1/4 and x <= 1/2
    phi1 = exact_min_on_interval(u - u**2, 0, 1)        # a=1, nu=-1
    assert phi1 == 0                                     # cut: x >= 0 + 1/4
    phi2 = exact_min_on_interval(-u + u**2, 0, 1)       # a=-1, nu=1
    assert phi2 == sp.Rational(-1, 4)                    # cut: -x >= -1/4 - 1/4
    # 3. mixture 3/4 at 0 and 1/4 at 1 has E u = E u^2 = 1/4
    assert sp.Rational(3, 4) * 0 + sp.Rational(1, 4) * 1 == sp.Rational(1, 4)
    print("x^2=1/4: closure = [1/4,1/2] confirmed (300 random cuts, 2 facet cuts)")


def check_joint_example():
    """Rows x^2 - s <= 0 and -x^3 + t <= 0 on D=[0,1]; point (1/2,1/4,1/2)."""
    xs, ss, ts = sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 2)
    # single-row envelope relaxations:
    #   env(u^2) = u^2 (convex); env(-u^3) on [0,1] = -u (chord of concave fn)
    assert sp.diff(-u**3, u, 2).subs(u, sp.Rational(1, 2)) < 0
    # -u^3 >= -u on [0,1] with equality at both ends, and -u is affine:
    assert sp.factor(-u**3 + u) == sp.factor(u * (1 - u) * (1 + u))
    assert xs**2 - ss <= 0 and -xs + ts <= 0          # point satisfies both
    # joint cut a=-5/4, lambda=(2,1):  -5/4 x + 2 s - t >= -1/4
    cert = sp.expand(-sp.Rational(5, 4) * u + 2 * u**2 - u**3 + sp.Rational(1, 4))
    assert sp.expand(cert - (u - sp.Rational(1, 2))**2 * (1 - u)) == 0
    assert exact_min_on_interval(-sp.Rational(5, 4) * u + 2 * u**2 - u**3, 0, 1) == sp.Rational(-1, 4)
    lhs = -sp.Rational(5, 4) * xs + 2 * ss - ts
    assert lhs == sp.Rational(-5, 8) and sp.Rational(-1, 4) - lhs == sp.Rational(3, 8)
    # envelope of the aggregated function 2u^2 - u^3 at 1/2 equals 3/8
    f = 2 * u**2 - u**3
    c = sp.symbols("c")
    tang = sp.factor(f.subs(u, c) + sp.diff(f, u).subs(u, c) * (1 - c) - 1)
    assert sp.expand(tang - (c - 1)**2 * (2 * c - 1)) == 0
    assert f.subs(u, sp.Rational(1, 2)) == sp.Rational(3, 8)
    # exact joint upper bound tau(x,m) = m - (x-m)^2/(1-x) for E u^3:
    X, M = sp.symbols("X M")
    cc = sp.symbols("cc")
    ineq = sp.expand((u - cc)**2 * (1 - u))      # >= 0 on [0,1]
    coeffs = sp.Poly(ineq, u).all_coeffs()       # [-1, 1+2c, -(c^2+2c), c^2]
    assert [sp.expand(z) for z in coeffs] == [-1, 1 + 2 * cc, -cc**2 - 2 * cc, cc**2]
    bound = (1 + 2 * cc) * M - (cc**2 + 2 * cc) * X + cc**2
    cstar = (X - M) / (1 - X)
    assert sp.simplify(bound.subs(cc, cstar) - (M - (X - M)**2 / (1 - X))) == 0
    # attainment by two atoms {c*, 1}: check on random rational (x, m), x^2<=m<=x
    for _ in range(200):
        x = sp.Rational(random.randint(1, 99), 100)
        m = x**2 + (x - x**2) * sp.Rational(random.randint(0, 50), 50)
        cs = (x - m) / (1 - x)
        assert 0 <= cs <= x
        th = (x - cs) / (1 - cs) if cs != 1 else sp.Integer(1)
        assert 0 <= th <= 1
        m1 = th + (1 - th) * cs
        m2 = th + (1 - th) * cs**2
        m3 = th + (1 - th) * cs**3
        assert m1 == x and m2 == m and m3 == m - (x - m)**2 / (1 - x)
    tau = sp.Rational(1, 4) - (sp.Rational(1, 2) - sp.Rational(1, 4))**2 / sp.Rational(1, 2)
    assert tau == sp.Rational(1, 8)
    print("joint example: point in both single-row closures; violated by 3/8; "
          "joint closure gives t <= 1/8 at (x,s)=(1/2,1/4)")
    return tau


def check_joint_lp_numeric():
    """Floating-point sanity check of tau via an LP over measures on a grid."""
    import numpy as np
    from scipy.optimize import linprog
    grid = np.linspace(0.0, 1.0, 2001)
    for x, m in [(0.5, 0.25), (0.3, 0.2), (0.7, 0.6), (0.5, 0.4)]:
        A_eq = np.vstack([np.ones_like(grid), grid, grid**2])
        b_eq = np.array([1.0, x, m])
        res = linprog(-grid**3, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method="highs")
        tau = m - (x - m)**2 / (1 - x)
        assert res.status == 0 and abs(-res.fun - tau) < 1e-6, (x, m, -res.fun, tau)
    print("joint example: grid-LP values of max E u^3 match tau (float, tol 1e-6)")


def check_integer_example():
    """x integer in {0,1,2}, row x^2 - s <= 0: closure s >= max(x, 3x-2)."""
    pts = [(0, 0), (1, 1), (2, 4)]
    for xq in [Fr(k, 8) for k in range(0, 17)]:
        # lower boundary of conv of the three points
        if xq <= 1:
            low = xq
        else:
            low = 3 * xq - 2
        assert low == max(xq, 3 * xq - 2)
        assert low >= xq * xq  # continuous-D closure s >= x^2 is weaker
    assert max(Fr(1, 2), 3 * Fr(1, 2) - 2) == Fr(1, 2) and Fr(1, 2)**2 == Fr(1, 4)
    # Prop 8.3(iii): D_Z={0,1,2}, row x^2 = 1; mixture 3/4 at 0, 1/4 at 2
    th = {0: Fr(3, 4), 1: Fr(0), 2: Fr(1, 4)}
    assert sum(th.values()) == 1
    assert sum(p * k for k, p in th.items()) == Fr(1, 2)
    assert sum(p * k * k for k, p in th.items()) == 1
    print("integer example: D={0,1,2} closure s>=max(x,3x-2) dominates s>=x^2")


def check_shared_remainder_gap():
    """D=[0,2] = S(Sigma); rows -(u-2)^2/2 + z <= 0, -u^2/2 + z <= 0.

    (1,1) lies in the closure R_D but not in conv(Sigma_D) (z <= 1/2 there)."""
    # mixture 1/2 at 0 and 1/2 at 2: E u = 1, E g1 = E g2 = -1  =>  z = 1 allowed
    Eg1 = sp.Rational(1, 2) * (-(0 - 2)**2 / sp.Integer(2)) + sp.Rational(1, 2) * (-(2 - 2)**2 / sp.Integer(2))
    Eg2 = sp.Rational(1, 2) * (-(0)**2 / sp.Integer(2)) + sp.Rational(1, 2) * (-(2)**2 / sp.Integer(2))
    assert Eg1 == -1 and Eg2 == -1
    # every aggregated cut a*x - (l1+l2)*z >= phi accepts (1,1)
    for _ in range(300):
        a = sp.Rational(random.randint(-30, 30), random.randint(1, 7))
        l1 = sp.Rational(random.randint(0, 30), random.randint(1, 7))
        l2 = sp.Rational(random.randint(0, 30), random.randint(1, 7))
        phi = exact_min_on_interval(a * u - l1 * (u - 2)**2 / 2 - l2 * u**2 / 2, 0, 2)
        assert a - (l1 + l2) - phi >= 0
    # on Sigma_D: z <= min((u-2)^2, u^2)/2 <= 1/2 for u in [0,2]
    assert exact_min_on_interval(1 - u**2, 0, 1) >= 0          # u in [0,1]: u^2 <= 1
    assert exact_min_on_interval(1 - (u - 2)**2, 1, 2) >= 0    # u in [1,2]: (u-2)^2 <= 1
    print("shared-remainder gap: (1,1) in R_D (all 300 random cuts accept), "
          "but z <= 1/2 on conv(Sigma_D) although D = S(Sigma_D)")


if __name__ == "__main__":
    check_quarter_example()
    check_joint_example()
    check_joint_lp_numeric()
    check_integer_example()
    check_shared_remainder_gap()
    print("M1_examples: all checks passed")
