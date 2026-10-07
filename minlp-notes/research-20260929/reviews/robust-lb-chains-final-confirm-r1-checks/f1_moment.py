"""Referee check (final confirmation, round 4) of robust-chains.md, Section 4.6 and Section 8.

Own code: shares nothing with chains/ or with the earlier reviews' checks.
Order-2 sparse moment relaxation (moment side) of the chiral chain
  f_n = a sum_i x_i^2 + b sum_i x_i x_{i+1} + (g/2) sum_i x_i x_{i+1} (x_{i+1} - x_i),
(b, g, ev) = (0.6, 0.3, 0.05), a = b + ev, on [-1, 1]^n; f* = 0 (Proposition C.1), and the
Dirac measure at 0 is feasible, so every value is <= 0 and a negative value is minus the gap.

Moments are indexed globally by frozenset-free sorted tuples ((var, power), ...), so the
univariate moments are automatically shared by neighbouring cliques.
- clique moment matrix: basis (1, u, v, u^2, uv, v^2) of clique (u, v) = (x_e, x_{e+1}), PSD;
- clique localizing matrix: basis (1, u, v), PSD;
- univariate localizing matrix (placement "uni"): basis (1, x_i), PSD.
Placements:
  opp  : 1 - x_i in clique (i-1, i), 1 + x_i in clique (i, i+1); x_1 and x_n: their only clique;
  uni  : 1 - x_i and 1 + x_i with univariate multipliers (Waki et al. form (20));
  ball : 2 M^2 - u^2 - v^2 localized in every clique (added to opp).
Moment bounds on every clique monomial of degree 1..4:
  yb : |L(u^p v^q)| <= 1;
  zb : 0 <= L(((1 + u)/2)^p ((1 + v)/2)^q) <= 1 (Waki et al., Section 5.6).
Floating point (Clarabel; SCS where stated). Not certified.

Usage: python3 f1_moment.py lasserre | bounds
"""
import sys
import json
import time
from math import comb

import cvxpy as cp

B, G, EV = 0.6, 0.3, 0.05
A = B + EV


def key(*pairs):
    d = {}
    for v, p in pairs:
        if p:
            d[v] = d.get(v, 0) + p
    return tuple(sorted(d.items()))


def mul(k1, k2):
    return key(*k1, *k2)


class Relax:
    def __init__(self, n):
        self.n = n
        self.y = {(): 1.0}
        self.cons = []

    def m(self, k):
        if k not in self.y:
            self.y[k] = cp.Variable()
        return self.y[k]

    def L(self, poly):  # poly: list of (coef, key)
        return sum(c * self.m(k) for c, k in poly)

    def psd(self, basis, poly):
        r = len(basis)
        X = cp.Variable((r, r), symmetric=True)
        for i in range(r):
            for j in range(i, r):
                self.cons.append(X[i, j] == self.L([(c, mul(mul(basis[i], basis[j]), k)) for c, k in poly]))
        self.cons.append(X >> 0)


def build(n, place, M=None, bounds=None):
    R = Relax(n)
    one = [(1.0, ())]
    for e in range(n - 1):
        u, v = e, e + 1
        R.psd([(), key((u, 1)), key((v, 1)), key((u, 2)), key((u, 1), (v, 1)), key((v, 2))], one)
    lin_basis = lambda e: [(), key((e, 1)), key((e + 1, 1))]
    if place == "opp":
        for i in range(n):
            e_minus = i - 1 if i >= 1 else 0          # clique holding 1 - x_i
            e_plus = i if i <= n - 2 else n - 2       # clique holding 1 + x_i
            R.psd(lin_basis(e_minus), [(1.0, ()), (-1.0, key((i, 1)))])
            R.psd(lin_basis(e_plus), [(1.0, ()), (1.0, key((i, 1)))])
    elif place == "uni":
        for i in range(n):
            for s in (1.0, -1.0):
                R.psd([(), key((i, 1))], [(1.0, ()), (s, key((i, 1)))])
    else:
        raise ValueError(place)
    if M is not None:
        for e in range(n - 1):
            R.psd(lin_basis(e), [(2.0 * M * M, ()), (-1.0, key((e, 2))), (-1.0, key((e + 1, 2)))])
    if bounds is not None:
        seen = set()
        for e in range(n - 1):
            for d in range(1, 5):
                for p in range(d + 1):
                    q = d - p
                    k = key((e, p), (e + 1, q))
                    if k in seen:
                        continue
                    seen.add(k)
                    if bounds == "yb":
                        R.cons += [R.m(k) <= 1, R.m(k) >= -1]
                    else:  # zb: L(((1+u)/2)^p ((1+v)/2)^q)
                        poly = [(comb(p, r) * comb(q, s) / 2.0 ** (p + q), key((e, r), (e + 1, s)))
                                for r in range(p + 1) for s in range(q + 1)]
                        expr = R.L(poly)
                        R.cons += [expr >= 0, expr <= 1]
    obj = []
    for i in range(n):
        obj.append((A, key((i, 2))))
    for i in range(n - 1):
        obj += [(B, key((i, 1), (i + 1, 1))), (G / 2, key((i, 1), (i + 1, 2))), (-G / 2, key((i, 2), (i + 1, 1)))]
    return cp.Problem(cp.Minimize(R.L(obj)), R.cons)


def solve(n, place, M=None, bounds=None, solvers=("CLARABEL",)):
    out = dict(n=n, place=place, M=M, bounds=bounds)
    for s in solvers:
        t = time.time()
        prob = build(n, place, M, bounds)
        prob.solve(solver=s)
        out[s] = [prob.status, float(f"{prob.value:.7g}"), round(time.time() - t, 1)]
    print(json.dumps(out), flush=True)


def lasserre():
    # The Lasserre paragraph now cites n = 5, 8, 16, 32 (note) and n = 12, 24 (third review).
    for M in (1.1, 1.3, 1.5, 2.0):
        for n in (5, 8, 12, 16, 24, 32):
            solve(n, "opp", M)
    for n in (5, 8):
        solve(n, "opp", 10.0)


def bounds():
    # The three rows of Section 8 ("all three rows"), plus the unbounded-free control.
    for n in (5, 8):
        solve(n, "uni", None, "yb", ("CLARABEL", "SCS"))
        solve(n, "uni", None, "zb", ("CLARABEL", "SCS"))
        solve(n, "opp", None, "zb", ("CLARABEL", "SCS"))
        solve(n, "opp", None, None)


if __name__ == "__main__":
    {"lasserre": lasserre, "bounds": bounds}[sys.argv[1]]()
