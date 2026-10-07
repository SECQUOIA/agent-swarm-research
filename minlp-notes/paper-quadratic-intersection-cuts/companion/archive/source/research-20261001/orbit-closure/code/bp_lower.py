"""Exact lower bound for the best single cut of SCIP's point-rule completion family (BP) at the
Theorem 14 corner in direction w = (1, 1, 1) (Theorem 9(c), Section 4 of note.md).

For a rational S > 0 (X = F^T M(sbar) = S) and mu = MU, it checks in exact arithmetic that
sbar + mu p_j lies in B_F = cl(C_F + R_+ e_w) for j = 1, 2, 3, by exhibiting rational tau_j >= 0 with
S + mu sym(S N_j) - tau_j Z >= 0 (Z = sym(S N_E)).  Since sbar is in int C_F, convexity gives
alpha_j(B_F) >= mu, so z_1,BP(1, 1, 1) >= min_j alpha_j >= mu.
Usage: python3 bp_lower.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[7])

import sys
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
from orbit_lib import Corner, S_of
from scipy.optimize import minimize

sb = [Fr(-9, 2), Fr(0), Fr(3, 2)]
V = [[Fr(-1), Fr(-6), Fr(18)], [Fr(-5), Fr(6), Fr(-18)], [Fr(0), Fr(5, 2), Fr(5, 2)]]
P = [[V[j][i] - sb[i] for i in range(3)] for j in range(3)]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


Mi = inv([[sb[2], sb[0]], [sb[1], Fr(1)]])
N = [mm(Mi, [[p[2], p[0]], [p[1], Fr(0)]]) for p in P]
NE = mm(Mi, [[Fr(1), Fr(0)], [Fr(0), Fr(0)]])


def sym(A):
    return [[A[0][0], (A[0][1] + A[1][0]) / 2], [(A[0][1] + A[1][0]) / 2, A[1][1]]]


def psd(X):
    return X[0][0] >= 0 and X[1][1] >= 0 and X[0][0] * X[1][1] - X[0][1] ** 2 >= 0


# numerical best single BP set
sbf = np.array([float(v) for v in sb]); Pf = np.array([[float(v) for v in p] for p in P]).T
cn = Corner(sbf, Pf)


def g(u):
    if u[0] ** 2 + u[1] ** 2 >= 1:
        return 1e3
    a = cn.cut_B_fast(S_of(u), 0.0)
    return -min(1 / x if x > 0 else np.inf for x in a)


best = None
rng = np.random.default_rng(0)
for k in range(60):
    r = minimize(g, rng.uniform(-0.7, 0.7, 2), method='Nelder-Mead', options=dict(xatol=1e-13, fatol=1e-15, maxiter=4000))
    if best is None or r.fun < best.fun:
        best = r
Sf = S_of(best.x); Sf = Sf / Sf[0, 0]
print('numerical best single BP cut: %.10f (16/63 = %.10f); S/S11 = %s' % (-best.fun, 16 / 63, np.round(Sf, 6).tolist()))
S = [[Fr(1), Fr(Sf[0, 1]).limit_denominator(10 ** 5)], [None, Fr(Sf[1, 1]).limit_denominator(10 ** 5)]]
S[1][0] = S[0][1]
MU = Fr(2539, 10000)
Z = sym(mm(S, NE))
ok = S[0][0] > 0 and S[0][0] * S[1][1] - S[0][1] ** 2 > 0
print('rational S = %s, positive definite: %s' % ([[str(v) for v in r] for r in S], ok))
for j in range(3):
    Aj = sym(mm(S, N[j]))
    base = [[S[i][k] + MU * Aj[i][k] for k in range(2)] for i in range(2)]
    found = None
    # search tau on a rational grid (exact check); tau = 0 first
    for tau in [Fr(0)] + [Fr(k, 64) for k in range(1, 64 * 40)]:
        X = [[base[i][k] - tau * Z[i][k] for k in range(2)] for i in range(2)]
        if psd(X):
            found = tau
            break
    print('ray %d: tau = %s gives S + mu sym(S N_j) - tau Z >= 0: %s' % (j + 1, found, found is not None))
    ok &= found is not None
print('=> alpha_j >= %s for j = 1, 2, 3, hence z_1,BP(1,1,1) >= %s = %.4f: %s' % (MU, MU, float(MU), 'PASS' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
