"""W5 tu check: the polynomial curvature certificate of Remark rem:tu-curv(i).

For random rational polynomials F(x, z) of degree <= 4 (3 continuous, 1 discrete
variable), compute b_{ii'} = sum_m |c_m| max(|lo_m|, |hi_m|) over the monomials of
d^2F/dx_i dx_i' with exact monomial ranges on [l,u] x [min Z, max Z], and check
that max_i sum_i' b_{ii'} >= largest eigenvalue of the x-Hessian at many random
points (x in [l,u], z in Z), and that for quadratics the bound equals the largest
absolute row sum of H_xx.  Run: python3 -B tu-w5-polycurv.py
"""
import random
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

random.seed(5)
xs = sp.symbols("x1:4")
zs = sp.symbols("z1:2")
V = list(xs) + list(zs)


def power_range(lo, hi, k):
    vals = [lo**k, hi**k]
    if k % 2 == 0 and lo < 0 < hi:
        vals.append(Fr(0))
    return min(vals), max(vals)


def monomial_range(exps, box):
    lo, hi = Fr(1), Fr(1)
    for e, (a, b) in zip(exps, box):
        if e == 0:
            continue
        p, q = power_range(a, b, e)
        cands = [lo * p, lo * q, hi * p, hi * q]
        lo, hi = min(cands), max(cands)
    return lo, hi


def bound(F, box):
    n = len(xs)
    B = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            d = sp.Poly(sp.diff(F, xs[i], xs[k]), *V)
            for exps, c in d.terms():
                lo, hi = monomial_range(exps, box)
                B[i][k] += abs(Fr(str(c))) * max(abs(lo), abs(hi))
    return B, max(sum(row) for row in B)


def rand_poly(deg):
    F = 0
    for _ in range(8):
        e = [0] * 4
        for _ in range(random.randint(0, deg)):
            e[random.randrange(4)] += 1
        c = sp.Rational(random.randint(-9, 9), random.randint(1, 5))
        F += c * sp.Mul(*[v**k for v, k in zip(V, e)])
    return sp.expand(F)


fails = 0
for trial in range(60):
    deg = 2 if trial < 15 else 4
    F = rand_poly(deg)
    box = []
    for _ in range(3):
        a = Fr(random.randint(-6, 3), random.randint(1, 3))
        box.append((a, a + Fr(random.randint(1, 6), random.randint(1, 3))))
    Z = sorted(random.sample(range(-3, 4), 3))
    box.append((Fr(Z[0]), Fr(Z[-1])))
    B, Lbar = bound(F, box)
    Hs = sp.hessian(F, xs)
    Hf = sp.lambdify(V, Hs, "numpy")
    for _ in range(200):
        pt = [random.uniform(float(a), float(b)) for a, b in box[:3]] + [random.choice(Z)]
        lam = max(np.linalg.eigvalsh(np.array(Hf(*pt), dtype=float)))
        if lam > float(Lbar) + 1e-9:
            fails += 1
    if deg == 2:
        H = sp.Matrix(Hs)
        rows = max(sum(abs(Fr(str(H[i, k]))) for k in range(3)) for i in range(3))
        assert rows == Lbar, (rows, Lbar)
print("violations:", fails)
print("PASS" if fails == 0 else "FAIL")
