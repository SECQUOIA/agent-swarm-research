"""Reviewer check of certs/elecN.json (exact arithmetic only for the verdict).

1. h_k parsed as exact Fractions from the decimal strings; h_k >= 0 for k >= 1.
2. Legendre P_k from sympy.legendre (not the author's recurrence); P_k(1) = 1 checked.
3. g(s) = 1 - s*h(1 - s^2/2) built as a sympy Poly over QQ.
   h(t) <= (2-2t)^(-1/2) on [-1,1)  <=>  g(s) >= 0 on (0,2]  (s = sqrt(2-2t) > 0).
4. Positivity of g on [0,2], two methods:
   A. sympy root isolation (Vincent-Collins-Akritas, exact integers): no real root in [0,2],
      and g(0) = 1 > 0.
   B. own adaptive subdivision: on [c-r, c+r] exact Taylor coefficients a_j of g at c,
      require a_0 - sum_{j>=1} |a_j| r^j > 0 (a valid lower bound of g on the cell).
5. Bound (N^2 h_0 - N h(1))/2 recomputed exactly and compared with the certificate.
"""
import json
import sys
import time
from fractions import Fraction as F

import sympy as sp

s, t = sp.symbols("s t")
CERTDIR = "/home/sgusev/repo/minlp-notes/research-20260922/benchmark-observations/code/structural/certs/"


def taylor_shift(coeffs, c):
    """coeffs[j] of x^j -> coefficients of (x - c)^j (exact, Horner shift)."""
    a = list(coeffs)
    n = len(a)
    for i in range(n):
        for j in range(n - 2, i - 1, -1):
            a[j] += c * a[j + 1]
    return a


def method_B(coeffs, lo, hi, max_cells=200000):
    todo = [(lo, hi)]
    cells = 0
    maxdepth = 0
    while todo:
        a, b = todo.pop()
        c, r = (a + b) / 2, (b - a) / 2
        tc = taylor_shift(coeffs, c)
        lb = tc[0]
        rp = F(1)
        for j in range(1, len(tc)):
            rp *= r
            lb -= abs(tc[j]) * rp
        cells += 1
        if cells > max_cells:
            return False, cells, maxdepth
        if lb > 0:
            continue
        if tc[0] <= 0:
            return False, cells, maxdepth  # g(c) <= 0: genuine failure
        maxdepth = max(maxdepth, (F(hi - lo) / (b - a)).numerator.bit_length())
        todo += [(a, c), (c, b)]
    return True, cells, maxdepth


def check(path, perturb=None):
    d = json.load(open(path))
    N, K = int(d["N"]), int(d["K"])
    h = [F(x) for x in d["h"]]
    if perturb:
        k, eps = perturb
        h[k] += eps
    assert len(h) == K + 1
    nonneg = all(hk >= 0 for hk in h[1:])
    P = [sp.Poly(sp.legendre(k, t), t, domain="QQ") for k in range(K + 1)]
    assert all(Pk.eval(1) == 1 for Pk in P)
    hpoly = sum((sp.Rational(hk.numerator, hk.denominator) * Pk for hk, Pk in zip(h, P)),
                sp.Poly(0, t, domain="QQ"))
    h1 = sum(h)
    assert hpoly.eval(1) == sp.Rational(h1.numerator, h1.denominator)
    hs = sp.Poly(hpoly.as_expr().subs(t, 1 - s**2 / 2), s, domain="QQ")
    g = sp.Poly(1, s, domain="QQ") - sp.Poly(s, s, domain="QQ") * hs
    assert g.degree() == 2 * hpoly.degree() + 1
    assert g.eval(0) == 1
    # method A
    t0 = time.time()
    gi = g.clear_denoms()[1].set_domain("ZZ")
    rootsA = gi.intervals(inf=0, sup=2)
    okA = (len(rootsA) == 0) and g.eval(2) > 0
    tA = time.time() - t0
    # method B
    t0 = time.time()
    coeffs = [F(int(c.p), int(c.q)) for c in reversed(g.all_coeffs())]
    okB, cells, depth = method_B(coeffs, F(0), F(2))
    tB = time.time() - t0
    bound = (N * N * h[0] - N * h1) / 2
    wrong_formula = (N * N * h[0] - N * sum(h[1:])) / 2
    bound_ok = bound == F(d["bound"])
    # smallest sampled value of g on (0,2] (float, diagnostic only)
    import numpy as np
    from numpy.polynomial import legendre as L
    ss = np.linspace(1e-4, 2, 200001)
    gv = 1 - ss * L.legval(1 - ss**2 / 2, np.array([float(x) for x in h]))
    gmin = (float(gv.min()), float(ss[gv.argmin()]))
    return dict(N=N, nonneg=nonneg, okA=okA, rootsA=len(rootsA), tA=tA, okB=okB, cellsB=cells,
                depthB=depth, tB=tB, bound=bound, bound_ok=bound_ok, wrong=wrong_formula,
                gmin=gmin, nzero=sum(1 for x in h[1:] if x != 0))


if __name__ == "__main__":
    names = sys.argv[1:] or ["elec25", "elec50", "elec100", "elec200"]
    for nm in names:
        r = check(CERTDIR + nm + ".json")
        print(nm, {k: (float(v) if isinstance(v, F) else v) for k, v in r.items()})
        print("   exact bound =", r["bound"], "; matches certificate:", r["bound_ok"])
    # negative control: a tiny increase of one coefficient must break positivity
    for nm, pert in [("elec25", (5, F(1, 10**6))), ("elec25", (0, 2 * F(1, 400000000))),
                     ("elec200", (0, 2 * F(43, 10**9)))]:
        r = check(CERTDIR + nm + ".json", perturb=pert)
        print("negative control", nm, "h[%d] +=" % pert[0], float(pert[1]), ": okA", r["okA"],
              "okB", r["okB"], "gmin", r["gmin"])
