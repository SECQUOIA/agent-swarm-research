"""Round-3 math lens: independent checks of the new and changed mathematics.

A. Four-variable path of Burer-Natarajan-Willemsen (2025), Example 4 / Section 6.4:
   A1 the rational point of BNW Section 6.4 (transcribed from the local PDF): exact PSD
      (Sylvester, Bareiss determinants), all McCormick/RLT inequalities of all products and
      squares, objective -109/1024;
   A2 exact minimum over [0,1]^4 by our own face enumeration (Fractions, no sympy);
   A3 dense relaxation value with two SDP solvers (Clarabel, SCS);
   A4 glued edge hulls: primal SDP (two solvers), an exactly checked rational feasible point
      (upper bound) and a Lagrangian re-splitting lower bound whose pair minima are computed
      exactly (Proposition 3.5(ii) duality, cutting-plane LP for the multipliers).
B. Full-gap instances of Proposition 3.4 (r = 1, 2, 3): objective built independently from
   the formula, own rational rounding (mix with a different interior point), exact PD test by
   leading principal minors; r = 1 lower bound 1/2 from identity (eq:sdp-identity), checked
   symbolically for the whole family.
C. Two-leaf strong NP-hardness (Section 4.2): exact vertex enumeration of
   {0 <= x <= 1, x_i + x_j <= 1 (ij in E)}: half-integrality, the value -|O| + h(n/4 - 1/2),
   and min = -alpha(G).
D. Section 8.5: c >= 1 on the 20 Part 4C4 instances; chord crossing m_y <= max A_i <= 3/4 on
   all path instances (seeds 0-9); nonconvexity rho_i = max(d_i - vex d_i) versus the recorded
   optimum - block closure (Shapley-Folkman remark).
E. Appendix A.4 examples, Proposition 3.4 binomial weights.

Run: OMP_NUM_THREADS=1 .venv/bin/python R10_math_checks.py
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction as F

sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np  # noqa: E402
import cvxpy as cp  # noqa: E402
import sympy as sp  # noqa: E402
from scipy.optimize import linprog  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FAIL = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


# ------------------------------------------------------------------ exact linear algebra
def bareiss_det(M):
    A = [list(r) for r in M]
    n = len(A)
    sign, prev = 1, F(1)
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None:
                return F(0)
            A[k], A[sw] = A[sw], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) / prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def positive_definite(M):
    """Sylvester: all leading principal minors > 0 (exact)."""
    return all(bareiss_det([row[:k] for row in M[:k]]) > 0 for k in range(1, len(M) + 1))


def solve_exact(M, b):
    n = len(M)
    A = [list(M[i]) + [b[i]] for i in range(n)]
    for k in range(n):
        p = next((i for i in range(k, n) if A[i][k] != 0), None)
        if p is None:
            return None
        A[k], A[p] = A[p], A[k]
        for i in range(n):
            if i != k and A[i][k] != 0:
                f = A[i][k] / A[k][k]
                A[i] = [A[i][j] - f * A[k][j] for j in range(n + 1)]
    return [A[i][n] / A[i][i] for i in range(n)]


def mccormick_ok(x, X, lo, hi):
    n = len(x)
    for i in range(n):
        for j in range(i, n):
            li, ui, lj, uj = lo[i], hi[i], lo[j], hi[j]
            xij = X[i][j]
            if (xij - lj * x[i] - li * x[j] + li * lj < 0 or ui * uj - uj * x[i] - ui * x[j] + xij < 0
                    or uj * x[i] + li * x[j] - li * uj - xij < 0 or lj * x[i] + ui * x[j] - ui * lj - xij < 0):
                return False
    return True


# ------------------------------------------------------------------ A. BNW path
Qm = [[8, -14, 0, 0], [-14, 25, -25, 0], [0, -25, 25, -14], [0, 0, -14, 8]]
cv = [12, 29, 0, 0]


def bnw_value(x, X):
    return sum(F(Qm[i][j]) * X[i][j] for i in range(4) for j in range(4)) + sum(F(cv[i]) * x[i] for i in range(4))


def part_A():
    print("A. four-variable path (BNW Example 4)")
    check(all(Qm[i][j] == 0 for i in range(4) for j in range(4) if abs(i - j) > 1), "Q is tridiagonal: path x1-x2-x3-x4")
    check([Qm[i][i] for i in range(4)] == [8, 25, 25, 8] and [Qm[i][i + 1] for i in range(3)] == [-14, -25, -14],
          "data as stated in Sec. 3.4 (diag 8,25,25,8; off-diagonal -14,-25,-14; c = (12,29,0,0))")
    # A1: BNW Proposition 12 point (local PDF, p. 43)
    xb = [F(3, 32), F(3, 16), F(9, 16), F(3, 4)]
    Xb = [[F(3, 32), F(3, 32), F(3, 32), F(61, 1024)],
          [F(3, 32), F(125, 1024), F(3, 16), F(3, 16)],
          [F(3, 32), F(3, 16), F(231, 512), F(9, 16)],
          [F(61, 1024), F(3, 16), F(9, 16), F(3, 4)]]
    Y = [[F(1)] + xb] + [[xb[i]] + Xb[i] for i in range(4)]
    check(positive_definite(Y), "BNW point: moment matrix positive definite (exact)")
    check(mccormick_ok(xb, Xb, [F(0)] * 4, [F(1)] * 4), "BNW point: all McCormick inequalities of all products and squares")
    v = bnw_value(xb, Xb)
    check(v == F(-109, 1024), f"BNW point: objective {v} = -109/1024")
    # A2: exact minimum by face enumeration
    best = None
    for pat in itertools.product((0, 1, None), repeat=4):
        free = [i for i in range(4) if pat[i] is None]
        fixed = {i: F(pat[i]) for i in range(4) if pat[i] is not None}
        if free:
            H = [[F(2 * Qm[i][j]) for j in free] for i in free]
            rhs = [-(F(cv[i]) + sum(2 * Qm[i][j] * fixed[j] for j in fixed)) for i in free]
            sol = solve_exact(H, rhs)
            if sol is None:
                continue
            x = [None] * 4
            for k, i in enumerate(free):
                x[i] = sol[k]
            for i in fixed:
                x[i] = fixed[i]
            if any(t < 0 or t > 1 for t in x):
                continue
        else:
            x = [fixed[i] for i in range(4)]
        val = sum(Qm[i][j] * x[i] * x[j] for i in range(4) for j in range(4)) + sum(cv[i] * x[i] for i in range(4))
        x = tuple(x)
        if best is None or val < best[0]:
            best = (val, {x})
        elif val == best[0]:
            best[1].add(x)
    check(best[0] == 0 and best[1] == {(0, 0, 0, 0)}, f"exact minimum over [0,1]^4 = {best[0]}, unique minimizer x = 0")
    # A3: dense relaxation, two solvers
    vals = {}
    for solver in (cp.CLARABEL, cp.SCS):
        Yv = cp.Variable((5, 5), symmetric=True)
        x, X = Yv[0, 1:], Yv[1:, 1:]
        cons = [Yv >> 0, Yv[0, 0] == 1]
        for i in range(4):
            for j in range(i, 4):
                cons += [X[i, j] >= 0, X[i, j] <= x[i], X[i, j] <= x[j], X[i, j] >= x[i] + x[j] - 1]
        prob = cp.Problem(cp.Minimize(cp.trace(np.array(Qm, float) @ X) + np.array(cv, float) @ x), cons)
        kw = {"eps": 1e-9, "max_iters": 200000} if solver == cp.SCS else {}
        prob.solve(solver=solver, **kw)
        vals[solver] = prob.value
    print(f"     dense SDP+all McCormick: Clarabel {vals[cp.CLARABEL]:.7f}, SCS {vals[cp.SCS]:.7f} (BNW: -0.1220566)")
    check(all(abs(v + 0.1220566) < 2e-5 for v in vals.values()), "dense relaxation value about -0.122 with two solvers")
    # A4: glued edge hulls
    gl = {}
    sol_keep = None
    for solver in (cp.CLARABEL, cp.SCS):
        m = cp.Variable(4)
        s = cp.Variable(4)
        p = cp.Variable(3)
        cons = []
        for e in range(3):
            i, j = e, e + 1
            B = cp.Variable((3, 3), symmetric=True)
            cons += [B >> 0, B[0, 0] == 1, B[0, 1] == m[i], B[0, 2] == m[j], B[1, 1] == s[i], B[2, 2] == s[j], B[1, 2] == p[e],
                     p[e] >= 0, p[e] <= m[i], p[e] <= m[j], p[e] >= m[i] + m[j] - 1]
        for i in range(4):
            cons += [s[i] <= m[i], s[i] >= 0, s[i] >= 2 * m[i] - 1]
        obj = sum(Qm[i][i] * s[i] for i in range(4)) + sum(2 * Qm[e][e + 1] * p[e] for e in range(3)) + sum(cv[i] * m[i] for i in range(4))
        prob = cp.Problem(cp.Minimize(obj), cons)
        kw = {"eps": 1e-9, "max_iters": 200000} if solver == cp.SCS else {}
        prob.solve(solver=solver, **kw)
        gl[solver] = prob.value
        if solver == cp.CLARABEL:
            sol_keep = (m.value.copy(), s.value.copy(), p.value.copy())
    print(f"     glued edge hulls SDP: Clarabel {gl[cp.CLARABEL]:.7f}, SCS {gl[cp.SCS]:.7f}")
    # rational feasible glued point (upper bound): mix with the uniform-distribution point
    mv, sv, pv = sol_keep
    ub = None
    for k in (8, 7, 6, 5, 4):
        eps = F(1, 10 ** k)
        mr = [(1 - eps) * F(t).limit_denominator(10 ** 10) + eps * F(1, 2) for t in mv]
        sr = [(1 - eps) * F(t).limit_denominator(10 ** 10) + eps * F(1, 3) for t in sv]
        pr = [(1 - eps) * F(t).limit_denominator(10 ** 10) + eps * F(1, 4) for t in pv]
        ok = True
        for e in range(3):
            i, j = e, e + 1
            B = [[F(1), mr[i], mr[j]], [mr[i], sr[i], pr[e]], [mr[j], pr[e], sr[j]]]
            ok &= positive_definite(B) and mccormick_ok([mr[i], mr[j]], [[sr[i], pr[e]], [pr[e], sr[j]]], [F(0)] * 2, [F(1)] * 2)
        if ok:
            ub = sum(Qm[i][i] * sr[i] for i in range(4)) + sum(2 * Qm[e][e + 1] * pr[e] for e in range(3)) + sum(cv[i] * mr[i] for i in range(4))
            break
    # Lagrangian lower bound with exact pair minima; params (a2, g2, a3, g3)
    base = [  # q_e as dict of monomials over (u, w) of edge e: keys (deg_u, deg_w)
        {(2, 0): 8, (1, 0): 12, (1, 1): -28, (0, 2): 25, (0, 1): 29},
        {(1, 1): -50, (0, 2): 25},
        {(1, 1): -28, (0, 2): 8},
    ]

    def edge_q(e, par):
        a2, g2, a3, g3 = par
        q = dict(base[e])
        if e == 0:
            q[(0, 1)] = q.get((0, 1), 0) + a2
            q[(0, 2)] = q.get((0, 2), 0) + g2
        if e == 1:
            q[(1, 0)] = q.get((1, 0), 0) - a2
            q[(2, 0)] = q.get((2, 0), 0) - g2
            q[(0, 1)] = q.get((0, 1), 0) + a3
            q[(0, 2)] = q.get((0, 2), 0) + g3
        if e == 2:
            q[(1, 0)] = q.get((1, 0), 0) - a3
            q[(2, 0)] = q.get((2, 0), 0) - g3
        return q

    def qval(q, u, w):
        return sum(c * u ** a * w ** b for (a, b), c in q.items())

    def box_min(q):
        """Exact min of a bivariate quadratic over [0,1]^2 (face candidates, Theorem 4.1)."""
        A, B, C = q.get((2, 0), 0), q.get((1, 1), 0), q.get((0, 2), 0)
        D, E = q.get((1, 0), 0), q.get((0, 1), 0)
        cands = [(F(u), F(w)) for u in (0, 1) for w in (0, 1)]
        for w in (0, 1):  # edges with w fixed: A u^2 + (B w + D) u
            if A != 0:
                u = -F(B * w + D) / (2 * A)
                if 0 <= u <= 1:
                    cands.append((u, F(w)))
        for u in (0, 1):
            if C != 0:
                w = -F(B * u + E) / (2 * C)
                if 0 <= w <= 1:
                    cands.append((F(u), w))
        det = 4 * F(A) * C - F(B) ** 2
        if det != 0:
            u = (-2 * F(C) * D + F(B) * E) / det
            w = (-2 * F(A) * E + F(B) * D) / det
            if 0 <= u <= 1 and 0 <= w <= 1:
                cands.append((u, w))
        vals_ = [(qval(q, u, w), (u, w)) for u, w in cands]
        return min(vals_)

    def dual(par):
        tot, arg = F(0), []
        for e in range(3):
            v_, a_ = box_min(edge_q(e, par))
            tot += v_
            arg.append(a_)
        return tot, arg

    # Kelley cutting plane: max sum theta_e, theta_e <= q_e'(u_e) at collected points
    pts = [[(F(0), F(0))] for _ in range(3)]
    par = (F(0), F(0), F(0), F(0))
    bestlb = None
    for it in range(400):
        lb, arg = dual(par)
        if bestlb is None or lb > bestlb[0]:
            bestlb = (lb, par)
        for e in range(3):
            if arg[e] not in pts[e]:
                pts[e].append(arg[e])
        # LP in z = (a2,g2,a3,g3,th1,th2,th3); maximize sum th
        A_ub, b_ub = [], []
        for e in range(3):
            for (u, w) in pts[e]:
                u, w = float(u), float(w)
                # q_e'(u,w) = base + coef . params ; theta_e - coef . params <= base
                b0 = float(qval(base[e], u, w))
                coef = [0.0] * 4
                if e == 0:
                    coef = [w, w * w, 0, 0]
                if e == 1:
                    coef = [-u, -u * u, w, w * w]
                if e == 2:
                    coef = [0, 0, -u, -u * u]
                row = [-c for c in coef] + [0.0] * 3
                row[4 + e] = 1.0
                A_ub.append(row)
                b_ub.append(b0)
        res = linprog(c=[0, 0, 0, 0, -1, -1, -1], A_ub=A_ub, b_ub=b_ub,
                      bounds=[(-300, 300)] * 4 + [(None, None)] * 3, method="highs")
        ublp = -res.fun
        par = tuple(F(t).limit_denominator(10 ** 9) for t in res.x[:4])
        if ublp - float(bestlb[0]) < 1e-9:
            break
    lb = bestlb[0]
    print(f"     glued: exact Lagrangian lower bound {float(lb):.9f}; exact rational feasible point {float(ub):.9f}")
    check(ub is not None and lb <= ub and float(ub) - float(lb) < 1e-6 and abs(float(lb) + 1.4544316) < 1e-5,
          "glued edge hulls value about -1.454 (exact sandwich lower <= value <= upper)")
    check(float(lb) < -0.1221, "glued pairs strictly weaker than the dense relaxation (-1.454 < -0.122 < 0)")


# ------------------------------------------------------------------ B. full gap
def fullgap_poly(r):
    xs = sp.symbols(f"x1:{r + 1}")
    zs = sp.symbols(f"z1:{r + 1}")
    y = sp.Symbol("y")
    PhiL = (y - sum(2 ** j * xs[j - 1] for j in range(1, r + 1))) ** 2 + sum(4 ** j * xs[j - 1] * (1 - xs[j - 1]) for j in range(1, r + 1))
    PhiR = (y - 1 - sum(2 ** j * zs[j - 1] for j in range(1, r + 1))) ** 2 + sum(4 ** j * zs[j - 1] * (1 - zs[j - 1]) for j in range(1, r + 1))
    vars_ = list(xs) + [y] + list(zs)
    return sp.Poly(sp.expand(PhiL + PhiR), *vars_), vars_


def part_B():
    print("B. full-gap instances of Proposition 3.4: dense first-level relaxation")
    for r in (1, 2, 3):
        P, vars_ = fullgap_poly(r)
        nv = len(vars_)
        lo = [F(0)] * nv
        hi = [F(1)] * nv
        hi[r] = F(2 ** (r + 1) - 1)
        # exact minimum: vertices in x, z, continuous y (min over y of the quadratic in y)
        y = vars_[r]
        best = None
        for bits in itertools.product((0, 1), repeat=2 * r):
            sub = {v: b for v, b in zip(vars_[:r] + vars_[r + 1:], bits)}
            g = sp.Poly(P.as_expr().subs(sub), y)
            a2, a1, a0 = [F(int(sp.fraction(c)[0]), int(sp.fraction(c)[1])) for c in g.all_coeffs()]
            yy = min(max(-a1 / (2 * a2), lo[r]), hi[r])
            val = a2 * yy * yy + a1 * yy + a0
            best = val if best is None else min(best, val)
        check(best == F(1, 2), f"r={r}: exact minimum {best}")
        # dense SDP
        n = nv + 1
        Yv = cp.Variable((n, n), symmetric=True)
        cons = [Yv >> 0, Yv[0, 0] == 1]
        for i in range(nv):
            for j in range(i, nv):
                xi, xj, xij = Yv[0, i + 1], Yv[0, j + 1], Yv[i + 1, j + 1]
                li, ui, lj, uj = float(lo[i]), float(hi[i]), float(lo[j]), float(hi[j])
                cons += [xij - lj * xi - li * xj + li * lj >= 0, ui * uj - uj * xi - ui * xj + xij >= 0,
                         uj * xi + li * xj - li * uj - xij >= 0, lj * xi + ui * xj - ui * lj - xij >= 0]
        terms = []
        coefs = {}
        for mon, c in zip(P.monoms(), P.coeffs()):
            idx = [k for k, d in enumerate(mon) for _ in range(d)]
            coefs[tuple(idx)] = F(int(c))
            if len(idx) == 0:
                terms.append(float(c))
            elif len(idx) == 1:
                terms.append(float(c) * Yv[0, idx[0] + 1])
            else:
                terms.append(float(c) * Yv[idx[0] + 1, idx[1] + 1])
        prob = cp.Problem(cp.Minimize(sum(terms)), cons)
        prob.solve(solver=cp.CLARABEL)
        Yn = Yv.value
        # interior point: product of the half-half mixture of the two-point and the uniform distribution
        # on each interval (E v^2 = (5 lo^2 + 2 lo hi + 5 hi^2)/12, strictly inside every McCormick inequality)
        mean = [(lo[i] + hi[i]) / 2 for i in range(nv)]
        sec = [(5 * lo[i] ** 2 + 2 * lo[i] * hi[i] + 5 * hi[i] ** 2) / 12 for i in range(nv)]
        U = [[F(1)] + mean] + [[mean[i]] + [sec[i] if i == j else mean[i] * mean[j] for j in range(nv)] for i in range(nv)]
        found = None
        for k in (9, 8, 7, 6, 5):
            eps = F(1, 10 ** k)
            Z = [[(1 - eps) * F(Yn[a, b]).limit_denominator(10 ** 11) + eps * U[a][b] for b in range(n)] for a in range(n)]
            for a in range(n):
                for b in range(a):
                    Z[a][b] = Z[b][a]
            Z[0][0] = F(1)
            xz = Z[0][1:]
            XZ = [row[1:] for row in Z[1:]]
            if mccormick_ok(xz, XZ, lo, hi) and positive_definite(Z):
                val = sum(c * (1 if len(ix) == 0 else Z[0][ix[0] + 1] if len(ix) == 1 else Z[ix[0] + 1][ix[1] + 1])
                          for ix, c in coefs.items())
                found = (eps, val)
                break
        print(f"     r={r}: SDP value {prob.value:.3e}; rational PD+McCormick point value {float(found[1]) if found else float('nan'):.3e} (eps {found[0] if found else None})")
        if r == 1:
            check(abs(prob.value - 0.5) < 1e-6, "r=1: dense value 1/2 (numerical)")
        else:
            check(found is not None and found[1] < F(1, 10 ** 6), f"r={r}: exactly checked rational point with value < 1e-6")
    # identity eq:sdp-identity for the whole family (symbolic), gives the r = 1 lower bound 1/2 rigorously
    x, y, z, a1, a2, c1, c2, wA, wC, dl = sp.symbols("x y z a1 a2 c1 c2 wA wC delta")
    xiA = y - a1 - (a2 - a1) * x
    xiC = y - c1 - (c2 - c1) * z
    Phi = xiA ** 2 + wA * x * (1 - x) + xiC ** 2 + wC * z * (1 - z)
    a = {1: a1, 2: a2}
    c = {1: c1, 2: c2}
    ell = {(0, 0): (1 - x) * (1 - z), (1, 0): x * (1 - z), (0, 1): (1 - x) * z, (1, 1): x * z}
    rhs = (xiA + xiC) ** 2 / 2 + sum(sp.Rational(1, 2) * ((c[j + 1] - a[i + 1]) ** 2 - dl ** 2) * ell[(i, j)] for i in (0, 1) for j in (0, 1)) \
        + (wA - (a2 - a1) ** 2 / 2) * x * (1 - x) + (wC - (c2 - c1) ** 2 / 2) * z * (1 - z)
    check(sp.expand(Phi - dl ** 2 / 2 - rhs) == 0, "identity (eq:sdp-identity) holds symbolically; with r=1 data (A={0,2}, C={1,3}, w=4) all terms are nonnegative on the dense relaxation")


# ------------------------------------------------------------------ C. two-leaf hardness
def vertices(n, E):
    rows = []  # (coef, rhs) for coef . x <= rhs
    for i in range(n):
        e = [0] * n
        e[i] = -1
        rows.append((e, 0))
        e = [0] * n
        e[i] = 1
        rows.append((e, 1))
    for (i, j) in E:
        e = [0] * n
        e[i] = e[j] = 1
        rows.append((e, 1))
    out = set()
    for I in itertools.combinations(range(len(rows)), n):
        M = [[F(t) for t in rows[k][0]] for k in I]
        if bareiss_det(M) == 0:
            continue
        x = solve_exact(M, [F(rows[k][1]) for k in I])
        if all(sum(F(c) * xi for c, xi in zip(co, x)) <= rh for co, rh in rows):
            out.add(tuple(x))
    return out


def alpha(n, E):
    adj = set(E) | {(j, i) for i, j in E}
    best = 0
    for S in range(1 << n):
        idx = [i for i in range(n) if S >> i & 1]
        if all((i, j) not in adj for i, j in itertools.combinations(idx, 2)):
            best = max(best, len(idx))
    return best


def part_C():
    print("C. two-leaf strong NP-hardness (Section 4.2)")
    rng = random.Random(1)
    graphs = []
    for n in (3, 4):
        allE = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(allE)):
            graphs.append((n, [allE[k] for k in range(len(allE)) if mask >> k & 1]))
    for n in (5, 6):
        allE = list(itertools.combinations(range(n), 2))
        for _ in range(6 if n == 5 else 3):
            graphs.append((n, [e for e in allE if rng.random() < 0.45]))
    ok_half = ok_formula = ok_min = True
    for n, E in graphs:
        V = vertices(n, E)
        vals = []
        for x in V:
            ok_half &= all(t in (0, F(1, 2), 1) for t in x)
            O = sum(1 for t in x if t == 1)
            h = sum(1 for t in x if t == F(1, 2))
            val = sum(n * t * (1 - t) - t for t in x)
            ok_formula &= val == -O + h * (F(n, 4) - F(1, 2))
            vals.append(val)
        ok_min &= min(vals) == -alpha(n, E)
    check(ok_half, f"vertices half-integral on {len(graphs)} graphs (n = 3..6)")
    check(ok_formula, "vertex value = -|O| + h(n/4 - 1/2), O the unit coordinates (a stable set)")
    check(ok_min, "minimum over the polytope = -alpha(G)")


# ------------------------------------------------------------------ D. Section 8.5
def part_D():
    print("D. Section 8.5 (path family)")
    sys.path.insert(0, os.path.join(ROOT, "experiments", "v4"))
    import mechanism  # noqa: E402
    import mechanism_c4  # noqa: E402
    cs = []
    for n in (10, 20, 40, 80):
        for s in range(5, 10):
            cs.append(mechanism_c4.coupling(mechanism_c4.blocks(n, s))[2])
    check(min(cs) >= 1, f"Part 4C4: c >= 1 on all 20 instances (min c = {min(cs)} = {float(min(cs))})")
    # chord crossing for the non-binding family, seeds 0..9
    worst = F(0)
    ok = True
    for n in (10, 20, 40, 80):
        for s in range(10):
            tot = F(0)
            for A, C in mechanism.draw_triples(n, s):
                A = sorted(F(t) for t in A)
                C = sorted(F(t) for t in C)
                # moments of the two-point chords: (m, s) = (a1 + a2) m - a1 a2 on the chord of A
                # crossing: (a1+a2) m - a1 a2 = (c1+c2) m - c1 c2
                m = (A[0] * A[1] - C[0] * C[1]) / ((A[0] + A[1]) - (C[0] + C[1]))
                ok &= (A[0] < m < A[1]) and (C[0] < m < C[1]) and m <= max(A) <= F(3, 4)
                worst = max(worst, m)
                tot += m
            ok &= tot <= F(4 * n, 5)
    check(ok, f"chords cross inside both segments with m_y <= max A_i <= 3/4 (max m_y = {float(worst):.4f}); sum <= 0.8 n")
    # nonconvexity rho_i versus optimum - block closure
    refs = json.load(open(os.path.join(ROOT, "experiments", "v4", "c4-references.json")))["instances"]
    grid = np.linspace(0, 1, 2 ** 14 + 1)
    worst_ratio = 0.0
    rows = []
    for rec in refs:
        n, s = rec["n"], rec["seed"]
        rho = 0.0
        for A, C, pairs in mechanism_c4.blocks(n, s):
            d = np.min([2 * (grid - float(m)) ** 2 + float(e) for (_, _, _, _, m, e) in pairs], axis=0)
            # lower convex envelope on the grid (monotone chain)
            hull = []
            for i in range(len(grid)):
                while len(hull) >= 2:
                    i1, i2 = hull[-2], hull[-1]
                    if (d[i2] - d[i1]) * (grid[i] - grid[i1]) >= (d[i] - d[i1]) * (grid[i2] - grid[i1]):
                        hull.pop()
                    else:
                        break
                hull.append(i)
            env = np.interp(grid, grid[hull], d[hull])
            rho = max(rho, float(np.max(d - env)))
        gap = float(F(rec["optimum_minus_bound_ii_exact"]))
        rows.append((n, s, gap, rho))
        worst_ratio = max(worst_ratio, gap / rho)
    print(f"     max over instances of (optimum - closure)/rho_max = {worst_ratio:.3f}; "
          f"max gap {max(r[2] for r in rows):.2e}; rho_max range {min(r[3] for r in rows):.4f}..{max(r[3] for r in rows):.4f}")
    check(worst_ratio <= 1.0 + 1e-9, "gap <= rho_max on every instance (the tight one-constraint bound), hence also <= 2 rho_max")


# ------------------------------------------------------------------ E. appendix examples
def part_E():
    print("E. Appendix A.4 examples and Proposition 3.4 weights")

    def inf_two(al, s, be, t):
        return al * be * (s - t) ** 2 / (al + be)

    # example 1: A={0,3}, C={1,2}, y in [0,3]; q1' = dist(y,A)^2 + 1/2 (y-3/2)^2, q2' = dist(y,C)^2 - 1/2 (y-3/2)^2
    m1 = min(inf_two(F(1), F(s), F(1, 2), F(3, 2)) for s in (0, 3))   # minimizer (s + 3/4)/(3/2) in [0,3]
    m2 = min(inf_two(F(1), F(t), F(-1, 2), F(3, 2)) for t in (1, 2))  # minimizer 2t - 3/2 in {1/2, 5/2}
    ys = [F(k, 1000) for k in range(3001)]
    dA = lambda yv, S: min((yv - s) ** 2 for s in S)  # noqa: E731
    g1 = min(dA(yv, (0, 3)) + F(1, 2) * (yv - F(3, 2)) ** 2 for yv in ys)
    g2 = min(dA(yv, (1, 2)) - F(1, 2) * (yv - F(3, 2)) ** 2 for yv in ys)
    bstar = min(dA(yv, (0, 3)) + dA(yv, (1, 2)) for yv in ys)
    check(m1 == F(3, 4) and m2 == F(-1, 4) and g1 == m1 and g2 == m2 and bstar == F(1, 2),
          "A.4 example 1: pair minima 3/4 and -1/4, beta* = 1/2, Delta' = 0")
    # example 2: three leaves A1={0,1}, A2={1,2}, A3={0,2} on [0,2]
    ys = [F(k, 3000) for k in range(6001)]
    val = min(dA(yv, (0, 1)) + dA(yv, (1, 2)) + dA(yv, (0, 2)) for yv in ys)
    check(val == F(2, 3), f"A.4 example 2: beta* = Delta = {val}; projections meet pairwise ({{1}},{{0}},{{2}}) but not jointly")
    # Proposition 3.4 binomial weights
    ok = True
    for k in range(1, 15):
        for mom in range(0, k + 1):
            ev = sum(sp.binomial(k + 1, i) * i ** mom for i in range(0, k + 2, 2))
            od = sum(sp.binomial(k + 1, i) * i ** mom for i in range(1, k + 2, 2))
            ok &= ev == od
        ok &= sum(sp.binomial(k + 1, i) for i in range(0, k + 2, 2)) == 2 ** k
    check(ok, "Prop. 3.4: binomial weights C(k+1,i) 2^-k on even/odd i <= k+1 are probability measures with equal moments up to k (k <= 14)")


if __name__ == "__main__":
    part_A()
    part_B()
    part_C()
    part_D()
    part_E()
    print("RESULT:", "PASS" if not FAIL else f"FAIL ({len(FAIL)}): " + "; ".join(FAIL))
    sys.exit(1 if FAIL else 0)
