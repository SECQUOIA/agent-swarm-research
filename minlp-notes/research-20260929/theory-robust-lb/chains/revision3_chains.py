"""Revision 3 of robust-chains.md (review round 3): targeted moment-relaxation runs for Section 4.6.

Order-2 sparse moment relaxation of the chiral chain (pair cliques, one moment vector per clique,
univariate moments shared between neighbouring cliques), (b, g, ev) = (0.6, 0.3, 0.05), f* = 0.
Floating point (Clarabel; SCS as a second solver where stated).

Commands:
  python3 revision3_chains.py waki    n = 5, 8: linear box constraints with univariate multipliers (Waki et al. (20)),
                                      (i) with |y_alpha| <= 1 (the row already in the note), (ii) with the bounds of
                                      Waki et al. Section 5.6: scale z = (1 + x)/2 in [0, 1] and add
                                      0 <= L(z^alpha) <= 1 for every clique monomial of degree 1..4;
                                      also one clique per constraint, opposite orientation, with the bounds (ii).
  python3 revision3_chains.py radius  opposite orientation + ball 2M^2 - x^2 - y^2 per clique,
                                      M = 1.1, 1.3, 1.5, 2 at n = 5, 8, 16, 32.
"""
import sys
import json
from math import comb

import cvxpy as cp

BB, GG, EE = 0.6, 0.3, 0.05
AA = BB + EE
MONS = [(i, d - i) for d in range(5) for i in range(d + 1)]
BASIS2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
BASIS1 = [(0, 0), (1, 0), (0, 1)]


def build(n, scheme, ball=None, ybound=False, zbound=False):
    ys = [{m: (cp.Variable() if m != (0, 0) else 1.0) for m in MONS} for _ in range(n - 1)]
    cons = []

    def loc(yv, basis, poly):  # localizing matrix of poly = [(coef, mon)] with respect to basis
        k = len(basis)
        Z = cp.Variable((k, k), PSD=True)
        for i, p in enumerate(basis):
            for j, q in enumerate(basis[i:], start=i):
                cons.append(Z[i, j] == sum(cf * yv[(p[0] + q[0] + s[0], p[1] + q[1] + s[1])] for cf, s in poly))

    for e in range(n - 1):
        yv = ys[e]
        loc(yv, BASIS2, [(1.0, (0, 0))])
        if e + 1 < n - 1:  # x_{e+2} is coordinate 1 of clique e and coordinate 0 of clique e+1
            cons += [yv[(0, d)] == ys[e + 1][(d, 0)] for d in range(1, 5)]
        if ball is not None:
            loc(yv, BASIS1, [(2 * ball ** 2, (0, 0)), (-1.0, (2, 0)), (-1.0, (0, 2))])
        if ybound:
            cons += [cp.abs(yv[m]) <= 1 for m in MONS if m != (0, 0)]
        if zbound:  # z = (1 + x)/2: L(z1^i z2^j) = 2^-(i+j) sum_{p<=i, q<=j} C(i,p) C(j,q) L(x1^p x2^q)
            for i, j in MONS:
                if (i, j) == (0, 0):
                    continue
                Lz = sum(comb(i, p) * comb(j, q) * yv[(p, q)] for p in range(i + 1) for q in range(j + 1)) / 2 ** (i + j)
                cons += [Lz >= 0, Lz <= 1]

    def where(i, side):  # variable i (1-based): clique index and coordinate; 'L' = clique (i-1,i), 'R' = (i,i+1)
        if side == "L" and i >= 2:
            return i - 2, 1
        if side == "R" and i <= n - 1:
            return i - 1, 0
        return (i - 1, 0) if i <= n - 1 else (i - 2, 1)

    def lin(sign, co):  # 1 + sign * x_co
        return [(1.0, (0, 0)), (float(sign), (1, 0) if co == 0 else (0, 1))]

    for i in range(1, n + 1):
        if scheme == "opp":  # 1 - x_i in clique (i-1, i), 1 + x_i in clique (i, i+1)
            e, co = where(i, "L"); loc(ys[e], BASIS1, lin(-1, co))
            e, co = where(i, "R"); loc(ys[e], BASIS1, lin(+1, co))
        elif scheme == "uni":  # univariate multipliers: localizing matrices in the basis (1, x_i)
            e, co = where(i, "R")
            ub = [(0, 0), (1, 0)] if co == 0 else [(0, 0), (0, 1)]
            loc(ys[e], ub, lin(-1, co)); loc(ys[e], ub, lin(+1, co))
        else:
            raise ValueError(scheme)

    obj = sum(AA / 2 * (yv[(2, 0)] + yv[(0, 2)]) + BB * yv[(1, 1)] + GG / 2 * (yv[(1, 2)] - yv[(2, 1)]) for yv in ys)
    obj += AA / 2 * ys[0][(2, 0)] + AA / 2 * ys[-1][(0, 2)]
    return cp.Problem(cp.Minimize(obj), cons)


def solve(n, scheme, ball=None, ybound=False, zbound=False, scs=True):
    out = dict(n=n, scheme=scheme, ball_M=ball, ybound=ybound, zbound=zbound)
    solvers = [("CLARABEL", {})] + ([("SCS", dict(eps=1e-8, max_iters=200000))] if scs else [])
    for solver, kw in solvers:
        prob = build(n, scheme, ball, ybound, zbound)
        try:
            prob.solve(solver=solver, **kw)
            out[solver] = (prob.status, None if prob.value is None else float(f"{prob.value:.7g}"))
        except Exception as exc:  # noqa: BLE001
            out[solver] = ("error", str(exc)[:80])
    print(json.dumps(out), flush=True)


def waki():
    for n in (5, 8):
        solve(n, "uni", ybound=True)
        solve(n, "uni", zbound=True)
        solve(n, "opp", zbound=True)


def radius():
    for M in (1.1, 1.3, 1.5, 2.0):
        for n in (5, 8, 16, 32):
            solve(n, "opp", ball=M, scs=n <= 8)


if __name__ == "__main__":
    {"waki": waki, "radius": radius}[sys.argv[1]]()
