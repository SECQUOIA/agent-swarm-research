"""Discrete-convexity tests for functions tabulated on an integer box.

A function is a dict mapping integer tuples to floats (math.inf = outside the
effective domain). Every test below is applied to the restriction of the
function to the tabulated box. Box restriction preserves L-natural, M-natural,
DDM and integral convexity (the box indicator is separable convex), so a
violation on the box is a violation for the underlying function.
"""
import itertools
import math

import numpy as np
from scipy.optimize import linprog

INF = math.inf


def mu(x, y):
    """Directed discrete midpoint (Tamura-Tsurumi): round (x+y)/2 toward x."""
    return tuple((xi + yi + 1) // 2 if xi >= yi else (xi + yi) // 2
                 for xi, yi in zip(x, y))


def _pairs(f):
    pts = [p for p, v in f.items() if v < INF]
    for a in range(len(pts)):
        for b in range(len(pts)):
            if a != b:
                yield pts[a], pts[b]


def ddm_violations(f, tol=1e-6):
    out = []
    for x, y in _pairs(f):
        p, q = mu(x, y), mu(y, x)
        lhs = f[x] + f[y]
        rhs = f.get(p, INF) + f.get(q, INF)
        if lhs < rhs - tol * (1 + abs(lhs)):
            out.append((x, y, lhs - rhs))
    return out


def lnat_violations(f, tol=1e-6):
    out = []
    for x, y in _pairs(f):
        c = tuple(-((-(xi + yi)) // 2) for xi, yi in zip(x, y))
        fl = tuple((xi + yi) // 2 for xi, yi in zip(x, y))
        lhs = f[x] + f[y]
        rhs = f.get(c, INF) + f.get(fl, INF)
        if lhs < rhs - tol * (1 + abs(lhs)):
            out.append((x, y, lhs - rhs))
    return out


def mnat_violations(f, tol=1e-6):
    """M-natural exchange: for x,y in dom and i with x_i>y_i there is
    j in {0} U {j: x_j<y_j} with f(x)+f(y) >= f(x-e_i+e_j)+f(y+e_i-e_j)."""
    out = []
    for x, y in _pairs(f):
        n = len(x)
        lhs = f[x] + f[y]
        for i in range(n):
            if x[i] <= y[i]:
                continue
            ok = False
            cands = [None] + [j for j in range(n) if x[j] < y[j]]
            for j in cands:
                xp = list(x); yp = list(y)
                xp[i] -= 1; yp[i] += 1
                if j is not None:
                    xp[j] += 1; yp[j] -= 1
                rhs = f.get(tuple(xp), INF) + f.get(tuple(yp), INF)
                if lhs >= rhs - tol * (1 + abs(lhs)):
                    ok = True
                    break
            if not ok:
                out.append((x, y, i))
    return out


def local_ext(f, m):
    """Local convex extension value at a point m (entries integer or half)."""
    choices = []
    for mi in m:
        if abs(mi - round(mi)) < 1e-12:
            choices.append([int(round(mi))])
        else:
            choices.append([math.floor(mi), math.ceil(mi)])
    pts = [z for z in itertools.product(*choices) if f.get(z, INF) < INF]
    if not pts:
        return INF
    if len(pts) == 1:
        return f[pts[0]] if np.allclose(pts[0], m) else INF
    A = np.array(pts, dtype=float).T
    A_eq = np.vstack([A, np.ones(len(pts))])
    b_eq = np.concatenate([np.array(m, dtype=float), [1.0]])
    c = np.array([f[z] for z in pts])
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method="highs")
    return res.fun if res.status == 0 else INF


def ic_violations(f, tol=1e-6):
    """Integral convexity via Murota-Tamura Theorem 3.2: for all x,y in dom
    with ||x-y||_inf >= 2, local_ext((x+y)/2) <= (f(x)+f(y))/2."""
    out = []
    for x, y in _pairs(f):
        if x > y:
            continue
        if max(abs(a - b) for a, b in zip(x, y)) < 2:
            continue
        m = tuple((a + b) / 2 for a, b in zip(x, y))
        val = local_ext(f, m)
        rhs = (f[x] + f[y]) / 2
        if val > rhs + tol * (1 + abs(rhs)):
            out.append((x, y, val - rhs))
    return out


def ninf_false_local_minima(f, tol=1e-9):
    """Points that are minimal over the l_inf unit neighbourhood but not global."""
    fin = {p: v for p, v in f.items() if v < INF}
    gmin = min(fin.values())
    out = []
    for p, v in fin.items():
        n = len(p)
        loc = all(v <= f.get(tuple(pi + di for pi, di in zip(p, d)), INF) + tol
                  for d in itertools.product((-1, 0, 1), repeat=n))
        if loc and v > gmin + 1e-7 * (1 + abs(gmin)):
            out.append((p, v, gmin))
    return out


def box(lo, hi, n):
    return list(itertools.product(range(lo, hi + 1), repeat=n))
