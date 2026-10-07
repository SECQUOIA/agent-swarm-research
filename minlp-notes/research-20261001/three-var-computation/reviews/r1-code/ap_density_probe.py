"""Reviewer r1: does the AP-variant gap rate depend on the densities used (50, 75 in the note)?

Anstreicher-Puges Table 5 lists gap instances with densities 50-85. For n in {8, 10} and
densities {60, 70, 80, 85}, seeds 1..N, the AP-variant instance (generator re-typed from
code/small_dense.py) is solved with B = Shor + McCormick + Y_ii <= x_i + all triangles
(cvxpy, parameterized, Clarabel 1e-9). A candidate gap is flagged when f(x_B) - B >
1e-6 max(1, |B|); the optimum of flagged instances is then enumerated, and a gap is counted
when opt - B > 1e-5 max(1, |opt|) (B primal value; no safe bound here, so this is a screen).
Usage: python ap_density_probe.py n N d1,d2,...
"""
import itertools
import json
import sys
import time
import warnings

import cvxpy as cp
import numpy as np

warnings.filterwarnings('ignore')


def gen(n, dens, seed):
    rng = np.random.default_rng(seed)
    Q = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1):
            if rng.random() * 100 <= dens:
                Q[i, j] = rng.integers(-50, 51)
            Q[j, i] = Q[i, j]
    c = rng.integers(-50, 51, size=n).astype(float)
    c = c * (rng.random(n) * 100 <= dens)
    return -Q, -c


def enum_min(H, g):
    n = len(g)
    best = np.inf
    for r in range(n + 1):
        for F in itertools.combinations(range(n), r):
            F = list(F)
            G = [i for i in range(n) if i not in F]
            XG = np.array(list(itertools.product((0.0, 1.0), repeat=len(G))), dtype=float).reshape(2 ** len(G), len(G))
            X = np.zeros((len(XG), n))
            X[:, G] = XG
            if F:
                A = 2 * H[np.ix_(F, F)]
                if abs(np.linalg.det(A)) < 1e-9:
                    continue
                XF = np.linalg.solve(A, -(g[F][None, :] + 2 * XG @ H[np.ix_(G, F)]).T).T
                ok = ((XF >= -1e-12) & (XF <= 1 + 1e-12)).all(1)
                X = X[ok]
                X[:, F] = np.clip(XF[ok], 0, 1)
            if len(X):
                best = min(best, float((np.einsum('ki,ij,kj->k', X, H, X) + X @ g).min()))
    return best


def build(n):
    Hp = cp.Parameter((n, n), symmetric=True)
    gp = cp.Parameter(n)
    Z = cp.Variable((n + 1, n + 1), symmetric=True)
    x, Y = Z[0, 1:], Z[1:, 1:]
    cons = [Z >> 0, Z[0, 0] == 1, x >= 0, x <= 1, cp.diag(Y) <= x]
    for i in range(n):
        for j in range(i + 1, n):
            cons += [Y[i, j] >= 0, Y[i, j] >= x[i] + x[j] - 1, Y[i, j] <= x[i], Y[i, j] <= x[j]]
    for i, j, k in itertools.combinations(range(n), 3):
        cons += [Y[i, j] + Y[i, k] - x[i] - Y[j, k] <= 0, Y[i, j] + Y[j, k] - x[j] - Y[i, k] <= 0,
                 Y[i, k] + Y[j, k] - x[k] - Y[i, j] <= 0, x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] <= 1]
    pr = cp.Problem(cp.Minimize(cp.sum(cp.multiply(Hp, Y)) + gp @ x), cons)
    return pr, Hp, gp, x


n, N = int(sys.argv[1]), int(sys.argv[2])
dens_list = [int(d) for d in sys.argv[3].split(',')]
pr, Hp, gp, xv = build(n)
for d in dens_list:
    t0 = time.time()
    flagged, gaps = 0, []
    for seed in range(1, N + 1):
        H, g = gen(n, d, seed)
        Hp.value, gp.value = H, g
        pr.solve(solver='CLARABEL', tol_gap_abs=1e-9, tol_gap_rel=1e-9, tol_feas=1e-9)
        B = pr.value
        x = np.clip(xv.value, 0, 1)
        if x @ H @ x + g @ x - B > 1e-6 * max(1, abs(B)):
            flagged += 1
            opt = enum_min(H, g)
            if opt - B > 1e-5 * max(1, abs(opt)):
                gaps.append((seed, round(opt, 6), round(B, 6), round(opt - B, 6)))
    print(json.dumps({'n': n, 'dens': d, 'N': N, 'flagged': flagged, 'gaps': gaps, 'time': round(time.time() - t0, 1)}), flush=True)
