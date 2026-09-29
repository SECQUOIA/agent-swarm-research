"""Targeted search against conjecture C1 with 'lexicographic' Hessians.

Q = U^T D U with V = U^{-1} small (so rho_inf(Q) = 1/2 ||V||_inf is small),
U large, and D = diag of very different scales.  Work in y = U x, where the
objective is separable: f = 1/2 sum d_i y_i^2 + c'^T y, constraints (A V) y <= b.
Integer optima are enumerated exactly in y-space by iterative deepening on the
KKT ellipsoid  1/2 sum d_i (y_i - y*_i)^2 <= f(y) - f(y*).
"""
from fractions import Fraction as F
from itertools import product
import random, sys, math, json
import numpy as np
from qip import qp_opt, max_subdet

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
scale = int(sys.argv[3]) if len(sys.argv) > 3 else 100
random.seed(seed)
n = 3


def rand_small_unimodular(amp=2):
    while True:
        V = [[random.randint(-amp, amp) for _ in range(n)] for _ in range(n)]
        d = round(np.linalg.det(np.array(V, dtype=float)))
        if abs(d) == 1:
            return V


def enum_opt(Dg, cy, B, b, ys):
    """All integer optima of min 1/2 sum d y^2 + cy^T y s.t. B y <= b (exact)."""
    f = lambda y: sum(Dg[i] * F(y[i]) ** 2 for i in range(n)) / 2 + sum(cy[i] * y[i] for i in range(n))
    fstar = f(ys)
    G = F(max(Dg)) / 8
    for _ in range(40):
        pts, best, arg = 0, None, []
        r0 = math.sqrt(2 * float(G) / float(Dg[0]))
        for y0 in range(math.ceil(float(ys[0]) - r0), math.floor(float(ys[0]) + r0) + 1):
            b0 = 2 * float(G) - float(Dg[0]) * (y0 - float(ys[0])) ** 2
            if b0 < 0:
                continue
            r1 = math.sqrt(b0 / float(Dg[1]))
            for y1 in range(math.ceil(float(ys[1]) - r1), math.floor(float(ys[1]) + r1) + 1):
                b1 = b0 - float(Dg[1]) * (y1 - float(ys[1])) ** 2
                if b1 < 0:
                    continue
                r2 = math.sqrt(b1 / float(Dg[2]))
                for y2 in range(math.ceil(float(ys[2]) - r2), math.floor(float(ys[2]) + r2) + 1):
                    pts += 1
                    if pts > 3_000_000:
                        return None
                    y = (y0, y1, y2)
                    if any(sum(B[r][j] * y[j] for j in range(n)) > b[r] for r in range(len(B))):
                        continue
                    v = f(y)
                    if best is None or v < best:
                        best, arg = v, [y]
                    elif v == best:
                        arg.append(y)
        if best is not None and best - fstar <= G * F(99, 100):
            return arg
        G *= 4
    return None


results = []
for t in range(trials):
    V = rand_small_unimodular(2)
    U = [[int(round(v)) for v in row] for row in np.linalg.inv(np.array(V, dtype=float))]
    rho = 0.5 * max(sum(abs(v) for v in row) for row in V)
    Dg = [F(scale) ** 2, F(scale), F(1)]
    random.shuffle(Dg)
    m = random.randint(3, 5)
    A = [[random.randint(-2, 2) for _ in range(n)] for _ in range(m)]
    if any(not any(r) for r in A):
        continue
    b = [F(random.randint(-9, 15), random.randint(1, 7)) for _ in range(m)]
    cy = [F(random.randint(-30, 30), random.randint(1, 5)) * Dg[i] for i in range(n)]
    # x-space data: Q = U^T D U, c = U^T cy
    Q = [[sum(U[r][i] * Dg[r] * U[r][j] for r in range(n)) for j in range(n)] for i in range(n)]
    c = [sum(U[r][i] * cy[r] for r in range(n)) for i in range(n)]
    xs = qp_opt(Q, c, A, b)
    if xs is None:
        continue
    B = [[sum(A[r][k] * V[k][j] for k in range(n)) for j in range(n)] for r in range(m)]
    ys = [sum(U[i][j] * xs[j] for j in range(n)) for i in range(n)]
    opts = enum_opt(Dg, cy, B, b, ys)
    if not opts:
        continue
    xo = [[sum(V[i][j] * y[j] for j in range(n)) for i in range(n)] for y in opts]
    prox = min(max(abs(F(z[i]) - xs[i]) for i in range(n)) for z in xo)
    delta = max_subdet(A)
    ratio = float(prox) / (delta * max(0.5, rho))
    results.append((ratio, float(prox), delta, rho, max(abs(v) for r in U for v in r), V, A,
                    [str(v) for v in b], [str(v) for v in Dg], [str(v) for v in xs], xo[:2]))

results.sort(key=lambda r: -r[0])
print(f"seed={seed} scale={scale} evaluated={len(results)}")
for r in results[:6]:
    print(json.dumps({"ratio": round(r[0], 3), "prox": round(r[1], 3), "Delta": r[2], "rho": r[3],
                      "maxU": r[4], "V": r[5], "A": r[6], "b": r[7], "D": r[8], "xstar": r[9],
                      "zopt": r[10]}))
