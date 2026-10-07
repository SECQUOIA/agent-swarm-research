"""lukvle10: compute the KKT point near MINLPLib point p5 to about 600 digits (heuristic step).

The result is only used to choose the two rational seed values x_0, x_1 of the exactly feasible
point; the proof (lukvle10_enclose.py) does not depend on the accuracy of this computation.

Model (structure asserted in lukvle10_enclose.py):
  min sum_{i<500} f(x_{2i}, x_{2i+1}),  f(a, b) = (a^2)^(b^2+1) + (b^2)^(a^2+1)
  c_j(x) = -x_j + 3 x_{j+1} - 2 x_{j+2} - 2 x_{j+1}^2 + 1 = 0,   j = 0..997.
KKT system: grad f(x) + J(x)^T lam = 0, c(x) = 0 (1998 unknowns). Solved by Newton-type
iterative refinement: the residual is evaluated in DPS-digit mpmath; the correction is solved with
the double-precision KKT matrix (dense LU), after scaling the residual to unit size.
"""
import json
import sys
import time

import mpmath as mp
import numpy as np
from scipy.linalg import lu_factor, lu_solve

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
SOL = _REPO + "/research-20260929/open-instances/minlplib_sol/lukvle10.p5.sol"
N, M = 1000, 998
DPS = 650


def g_parts(a, b, log, exp):
    """g(a, b) = (a^2)^(b^2+1) and its first and second derivatives (a != 0)."""
    A, E = a * a, b * b + 1
    LA = log(A)
    g = exp(E * LA)
    ga = g * E * 2 / a
    gb = g * LA * 2 * b
    gaa = g * E * (4 * E - 2) / A
    gab = g * (4 * b / a) * (E * LA + 1)
    gbb = g * ((2 * b * LA) ** 2 + 2 * LA)
    return g, ga, gb, gaa, gab, gbb


def f_grad(x, log, exp):
    """objective value and gradient."""
    val, grad = 0, [0] * N
    for i in range(N // 2):
        a, b = x[2 * i], x[2 * i + 1]
        g1 = g_parts(a, b, log, exp)
        g2 = g_parts(b, a, log, exp)  # h(a, b) = g(b, a)
        val += g1[0] + g2[0]
        grad[2 * i] = g1[1] + g2[2]
        grad[2 * i + 1] = g1[2] + g2[1]
    return val, grad


def kkt_residual(x, lam, log, exp):
    _, grad = f_grad(x, log, exp)
    rx = list(grad)
    rc = [0] * M
    for j in range(M):
        rx[j] += -lam[j]
        rx[j + 1] += (3 - 4 * x[j + 1]) * lam[j]
        rx[j + 2] += -2 * lam[j]
        rc[j] = -x[j] + 3 * x[j + 1] - 2 * x[j + 2] - 2 * x[j + 1] ** 2 + 1
    return rx + rc


def kkt_matrix(x, lam):
    """double-precision KKT Jacobian."""
    K = np.zeros((N + M, N + M))
    for i in range(N // 2):
        a, b = x[2 * i], x[2 * i + 1]
        _, _, _, gaa, gab, gbb = g_parts(a, b, np.log, np.exp)
        _, _, _, haa_s, hab_s, hbb_s = g_parts(b, a, np.log, np.exp)
        K[2 * i, 2 * i] += gaa + hbb_s
        K[2 * i + 1, 2 * i + 1] += gbb + haa_s
        K[2 * i, 2 * i + 1] += gab + hab_s
        K[2 * i + 1, 2 * i] += gab + hab_s
    for j in range(M):
        K[j + 1, j + 1] += -4 * lam[j]
        for col, v in ((j, -1.0), (j + 1, 3 - 4 * x[j + 1]), (j + 2, -2.0)):
            K[col, N + j] = v
            K[N + j, col] = v
    return K


def read_p5():
    x = np.zeros(N)
    for line in open(SOL):
        nm, val = line.split()
        if nm.startswith("x"):
            x[int(nm[1:]) - 1] = float(val)  # OSIL variable x{k} has index k-1 (checked in enclose)
    return x


def main():
    t0 = time.time()
    x = read_p5()
    # gradient sanity check against central differences (double)
    _, gr = f_grad(x, np.log, np.exp)
    e = np.zeros(N); e[7] = 1e-6
    fd = (f_grad(x + e, np.log, np.exp)[0] - f_grad(x - e, np.log, np.exp)[0]) / 2e-6
    print("grad check", gr[7], fd, flush=True)
    # least-squares multipliers at p5
    Jt = np.zeros((N, M))
    for j in range(M):
        Jt[j, j], Jt[j + 1, j], Jt[j + 2, j] = -1.0, 3 - 4 * x[j + 1], -2.0
    lam, *_ = np.linalg.lstsq(Jt, -np.array(gr), rcond=None)
    K = kkt_matrix(x, lam)
    cond = np.linalg.cond(K)
    print("cond(K) at p5:", cond, flush=True)
    lu = lu_factor(K)
    mp.mp.dps = DPS
    X = [mp.mpf(float(v)) for v in x]
    L = [mp.mpf(float(v)) for v in lam]
    hist = []
    for it in range(200):
        r = kkt_residual(X, L, mp.log, mp.exp)
        s = max(abs(v) for v in r)
        hist.append(float(mp.log10(s)) if s > 0 else -float("inf"))
        print(f"it {it}: log10 max|residual| = {hist[-1]:.1f}  ({time.time() - t0:.0f} s)", flush=True)
        if s < mp.mpf(10) ** (-(DPS - 20)):
            break
        if it == 3:  # refresh the double matrix once at the more accurate iterate
            lu = lu_factor(kkt_matrix(np.array([float(v) for v in X]), np.array([float(v) for v in L])))
        d = lu_solve(lu, np.array([float(v / s) for v in r]))
        for k in range(N):
            X[k] -= s * mp.mpf(float(d[k]))
        for j in range(M):
            L[j] -= s * mp.mpf(float(d[N + j]))
    obj, _ = f_grad(X, mp.log, mp.exp)
    with open("logs/lukvle10_kkt_x.txt", "w") as f:
        for k in range(N):
            f.write(f"x{k + 1} {mp.nstr(X[k], DPS - 10, strip_zeros=False)}\n")
    with open("logs/lukvle10_kkt_lam.txt", "w") as f:
        for j in range(M):
            f.write(f"{j} {mp.nstr(L[j], 40)}\n")
    rec = dict(dps=DPS, cond_K_p5=float(cond), iterations=len(hist), log10_residual_history=hist,
               kkt_objective_40=mp.nstr(obj, 40), max_dev_from_p5=float(max(abs(X[k] - x[k]) for k in range(N))),
               lam_range=[float(min(L)), float(max(L))], seconds=time.time() - t0)
    print(json.dumps(rec, indent=1))
    json.dump(rec, open("logs/lukvle10_kkt.json", "w"), indent=1)


if __name__ == "__main__":
    main()
