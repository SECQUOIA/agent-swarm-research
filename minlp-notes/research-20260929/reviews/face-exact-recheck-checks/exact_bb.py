"""Independent exact-rational bisection B&B for f = sum x_i^2 + (4/5) sum x_i x_{i+1} on [-1,1]^n
(kappa = 0, c = 0, so f* = 0 and x* = 0), with the termwise McCormick relaxation
    F_C(x) = sum x_i^2 + b sum_e max(P_e(x), Q_e(x)),
    P_e = l_j x_i + l_i x_j - l_i l_j,  Q_e = u_j x_i + u_i x_j - u_i u_j   (b > 0, e = (i, j = i+1)).

Node bound LB(C) = min_C F_C, computed EXACTLY in rational arithmetic:
  1. approximate minimiser from OSQP (a solver not used by bb_path.py);
  2. classify each variable (lower / upper / free) and edge (P / Q / kink) and solve the face's
     equality-constrained KKT system in Fractions; lambda_e = 1 + nu_e/b for kinks;
  3. certificate: x feasible and d(lambda) == F(x) exactly, where d(lambda) = min_box of the separable
     Lagrangian (weak duality: d(lambda) <= min F for every lambda in [0,1]^(n-1));
  4. fallback: full enumeration of all faces (min over feasible faces = exact min, no duals needed).
Prune iff LB(C) >= -eps with eps an exact rational (10^-k).  Bisection: widest side, lowest index on
ties, midpoint.  Optionally compares every node with bb_path.certified (the note's pruning bound).

Option 'seed0': the PROGRAM instance kappa = 1/10, c ~ U(-0.3, 0.3) from default_rng(0) (floats taken as exact
rationals), relaxation x^2 exact + secant of -kappa x^4 + c x (bb_path's 'mc'); the incumbent is bb_path's f*
(a float, taken exactly), so the threshold is f* - eps as for bb_path.

Usage: python3 exact_bb.py K n1 n2 ... [cmp] [seed0]   (eps = 10^-K)
"""
import itertools
import sys
import time
import warnings
from fractions import Fraction as Fr

import numpy as np
import cvxpy as cp

warnings.filterwarnings("ignore")
b = Fr(4, 5)
KAPPA = Fr(0)
CVEC = None          # None: c = 0


def uni(l, u):
    """Linear coefficient and constant of the univariate part x^2 + c x + secant of -kappa x^4 on [l, u]."""
    lin, con = [], []
    for i in range(len(l)):
        slope = -KAPPA * (l[i] + u[i]) * (l[i] ** 2 + u[i] ** 2)
        lin.append((CVEC[i] if CVEC else 0) + slope)
        con.append(-KAPPA * l[i] ** 4 - slope * l[i])
    return lin, con


def pieces(l, u):
    n = len(l)
    P = [(l[i + 1], l[i], -l[i] * l[i + 1]) for i in range(n - 1)]   # coef of x_i, x_{i+1}, const
    Q = [(u[i + 1], u[i], -u[i] * u[i + 1]) for i in range(n - 1)]
    return P, Q


def ev(c, x, i):
    return c[0] * x[i] + c[1] * x[i + 1] + c[2]


def Fval(l, u, x):
    P, Q = pieces(l, u)
    lin, con = uni(l, u)
    return sum(t * t + lin[i] * t + con[i] for i, t in enumerate(x)) + b * sum(max(ev(P[e], x, e), ev(Q[e], x, e)) for e in range(len(P)))


def dual(l, u, lam):
    """d(lam) = min over the box of sum x_i^2 + b sum_e (lam_e P_e + (1 - lam_e) Q_e): exact."""
    n = len(l)
    P, Q = pieces(l, u)
    a, con = uni(l, u)
    c0 = sum(con)
    for e in range(n - 1):
        a[e] += b * (lam[e] * P[e][0] + (1 - lam[e]) * Q[e][0])
        a[e + 1] += b * (lam[e] * P[e][1] + (1 - lam[e]) * Q[e][1])
        c0 += b * (lam[e] * P[e][2] + (1 - lam[e]) * Q[e][2])
    tot = c0
    for i in range(n):
        x = min(max(-a[i] / 2, l[i]), u[i])
        tot += x * x + a[i] * x
    return tot


def solve_lin(A, r):
    """Gaussian elimination in Fractions; None if singular."""
    m = len(A)
    M = [row[:] + [r[k]] for k, row in enumerate(A)]
    for c in range(m):
        piv = next((k for k in range(c, m) if M[k][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        for k in range(m):
            if k != c and M[k][c] != 0:
                f = M[k][c] / pv
                M[k] = [a - f * bb for a, bb in zip(M[k], M[c])]
    return [M[k][m] / M[k][k] for k in range(m)]


def face(l, u, vs, es):
    """Minimise q = sum x^2 + b sum_e piece_e on the face; kink edges use piece P plus P - Q = 0.
    Returns (x, lam) or None (singular or infeasible)."""
    n = len(l)
    P, Q = pieces(l, u)
    lin, _ = uni(l, u)
    free = [i for i in range(n) if vs[i] == 'F']
    kinks = [e for e in range(n - 1) if es[e] == 'K']
    x = [l[i] if vs[i] == 'L' else u[i] if vs[i] == 'U' else None for i in range(n)]
    col = {('x', i): k for k, i in enumerate(free)}
    col.update({('nu', e): len(free) + k for k, e in enumerate(kinks)})
    m = len(col)
    A, r = [], []
    for i in free:                     # stationarity of free x_i
        row = [Fr(0)] * m
        rhs = -lin[i]
        row[col[('x', i)]] += 2
        for e in (i - 1, i):
            if e < 0 or e >= n - 1:
                continue
            k = 0 if e == i else 1       # position of x_i in edge e
            pc = P[e] if es[e] in 'PK' else Q[e]
            rhs -= b * pc[k]
            if es[e] == 'K':
                row[col[('nu', e)]] += P[e][k] - Q[e][k]
        A.append(row); r.append(rhs)
    for e in kinks:                    # (P - Q)(x) = 0
        row = [Fr(0)] * m
        rhs = -(P[e][2] - Q[e][2])
        for k, i in ((0, e), (1, e + 1)):
            coef = P[e][k] - Q[e][k]
            if vs[i] == 'F':
                row[col[('x', i)]] += coef
            else:
                rhs -= coef * x[i]
        A.append(row); r.append(rhs)
    if m:
        z = solve_lin(A, r)
        if z is None:
            return None
        for i in free:
            x[i] = z[col[('x', i)]]
    for i in range(n):
        if not (l[i] <= x[i] <= u[i]):
            return None
    lam = []
    for e in range(n - 1):
        dp, dq = ev(P[e], x, e), ev(Q[e], x, e)
        if es[e] == 'P':
            if dp < dq:
                return None
            lam.append(Fr(1))
        elif es[e] == 'Q':
            if dq < dp:
                return None
            lam.append(Fr(0))
        else:
            nu = z[col[('nu', e)]]
            lam.append(min(max(1 + nu / b, Fr(0)), Fr(1)))
    return x, lam


def approx(l, u):
    n = len(l)
    lf, uf = np.array([float(t) for t in l]), np.array([float(t) for t in u])
    x = cp.Variable(n); w = cp.Variable(n - 1)
    cons = [x >= lf, x <= uf,
            w >= cp.multiply(lf[1:], x[:-1]) + cp.multiply(lf[:-1], x[1:]) - lf[:-1] * lf[1:],
            w >= cp.multiply(uf[1:], x[:-1]) + cp.multiply(uf[:-1], x[1:]) - uf[:-1] * uf[1:]]
    linf = np.array([float(t) for t in uni(l, u)[0]])
    pr = cp.Problem(cp.Minimize(cp.sum_squares(x) + linf @ x + 0.8 * cp.sum(w)), cons)
    try:
        pr.solve(solver="OSQP", eps_abs=1e-11, eps_rel=1e-11, max_iter=400000, polishing=True)
    except Exception:
        pr.solve(solver="SCS", eps=1e-10, max_iters=200000)
    return np.asarray(x.value, float)


STATS = dict(guided=0, enum=0, ties=0, band=0)


def exact_lb(l, u, allow_enum=True):
    n = len(l)
    xa = approx(l, u)
    P, Q = pieces(l, u)
    Pf = [tuple(float(t) for t in c) for c in P]
    Qf = [tuple(float(t) for t in c) for c in Q]
    for tau in (1e-9, 1e-7, 1e-5, 1e-3):
        opts_v, opts_e = [], []
        for i in range(n):
            w = float(u[i] - l[i])
            o = []
            if xa[i] - float(l[i]) <= tau * w: o.append('L')
            if float(u[i]) - xa[i] <= tau * w: o.append('U')
            if not o: o = ['F']
            elif tau >= 1e-5: o.append('F')
            opts_v.append(o)
        for e in range(n - 1):
            d = (Pf[e][0] - Qf[e][0]) * xa[e] + (Pf[e][1] - Qf[e][1]) * xa[e + 1] + Pf[e][2] - Qf[e][2]
            sc = float((u[e] - l[e]) * (u[e + 1] - l[e + 1]))
            if abs(d) <= tau * sc:
                opts_e.append(['K', 'P', 'Q'])
            else:
                opts_e.append(['P'] if d > 0 else ['Q'])
        combos = 1
        for o in opts_v + opts_e:
            combos *= len(o)
        if combos > 3000:
            continue
        for vs in itertools.product(*opts_v):
            for es in itertools.product(*opts_e):
                res = face(l, u, vs, es)
                if res is None:
                    continue
                x, lam = res
                fv = Fval(l, u, x)
                if dual(l, u, lam) == fv:
                    STATS['guided'] += 1
                    return fv, x
    if not allow_enum:
        return None, None
    STATS['enum'] += 1
    return enum_lb(l, u)


def enum_lb(l, u):
    n = len(l)
    best, bx = None, None
    for vs in itertools.product('LUF', repeat=n):
        for es in itertools.product('PQK', repeat=n - 1):
            res = face(l, u, vs, es)
            if res is None:
                continue
            fv = Fval(l, u, res[0])
            if best is None or fv < best:
                best, bx = fv, res[0]
    return best, bx


def run(n, eps, compare=False, seed0=False):
    global CVEC
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../theory-face-exact"))
    if compare:
        import bb_path
        I = bb_path.Inst(n, float(KAPPA), "seed0" if seed0 else "zero")
        thr_f = I.fstar - float(eps) - bb_path.TIE
    fstar = Fr(0)
    CVEC = None
    if seed0:
        CVEC = [Fr(float(t)) for t in np.random.default_rng(0).uniform(-0.3, 0.3, n)]
        fstar = Fr(I.fstar)
    stack = [([Fr(-1)] * n, [Fr(1)] * n)]
    nodes = leaves = 0
    flips, worst_valid, near = 0, -1.0, []
    while stack:
        l, u = stack.pop()
        nodes += 1
        lb, _ = exact_lb(l, u)
        prune = lb >= fstar - eps
        if lb == fstar - eps:
            STATS['ties'] += 1
        if fstar - eps - Fr(1, 10 ** 12) <= lb < fstar - eps:
            STATS['band'] += 1
        if compare:
            lf, uf = np.array([float(t) for t in l]), np.array([float(t) for t in u])
            xh = bb_path.relax(I, "mc", lf, uf)[1]
            lbc, ubc = bb_path.certified(I, "mc", lf, uf, thr_f, xh)
            worst_valid = max(worst_valid, lbc - float(lb))     # > 0 would mean an invalid 'certified' bound
            if (lbc >= thr_f) != prune:
                flips += 1
                near.append((float(lb), lbc, ubc))
        if prune:
            leaves += 1
            continue
        w = [u[i] - l[i] for i in range(n)]
        i = max(range(n), key=lambda k: (w[k], -k))
        mid = (l[i] + u[i]) / 2
        u1 = u[:]; u1[i] = mid
        l2 = l[:]; l2[i] = mid
        stack.append((l2, u))
        stack.append((l, u1))
    return nodes, leaves, flips, worst_valid, near


def main():
    global KAPPA
    K = int(sys.argv[1])
    compare = 'cmp' in sys.argv
    seed0 = 'seed0' in sys.argv
    if seed0:
        KAPPA = Fr(1, 10)
    eps = Fr(1, 10 ** K)
    for n in [int(a) for a in sys.argv[2:] if a not in ('cmp', 'seed0')]:
        for k in STATS:
            STATS[k] = 0
        t0 = time.time()
        nodes, leaves, flips, worst, near = run(n, eps, compare, seed0)
        msg = (f"EXACT {'seed0 kappa=0.1 secant' if seed0 else 'kappa=0 c=0'} eps=1e-{K} n={n}: nodes={nodes} leaves={leaves} "
               f"[exact bounds: guided={STATS['guided']} enumerated={STATS['enum']} exact_ties(LB=-eps)={STATS['ties']} "
               f"in_TIE_band={STATS['band']}] t={time.time() - t0:.1f}s")
        if compare:
            msg += (f" | vs bb_path.certified: flipped decisions={flips}, "
                    f"max(certified LB - exact LB)={worst:.2e}")
            if near:
                msg += f" flips(exact, cert_lb, cert_ub)={near[:5]}"
        print(msg, flush=True)


if __name__ == "__main__":
    main()
