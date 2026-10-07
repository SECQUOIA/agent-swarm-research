"""Reviewer's independent numerical check of the point-rule and BCM family bounds (review r1).

Point rule: F^T = P Mbar^{-1}, P symmetric (bisection over z with an SDP in P; no preconditioning).
BCM: F^T = cos(phi) I + sin(phi) J, dense scan over phi (2*10^5 points) with exact step lengths.
Instances A, B, S1 of the note and the scaling corner of Proposition 11.  Does not import the
stream's code.  Usage: python3 indep_families.py
"""
from fractions import Fraction as Fr
import numpy as np
import cvxpy as cp

J = np.array([[0.0, 1.0], [-1.0, 0.0]])


def m2(s):
    return np.array([[s[0], s[1]], [s[2], s[3]]], float)


def step(FT, sb, p):
    A = FT @ m2(sb); A = (A + A.T) / 2
    B = FT @ m2(p); B = (B + B.T) / 2
    ev = np.linalg.eigvalsh(A)
    if ev[0] <= 0:
        return -np.inf
    L = np.linalg.cholesky(A); Li = np.linalg.inv(L)
    mn = np.linalg.eigvalsh(Li @ B @ Li.T)[0]
    return np.inf if mn >= 0 else -1.0 / mn


def bound(FT, sb, P, w):
    v = [w[j] * step(FT, sb, P[:, j]) for j in range(P.shape[1])]
    return min(v)


def pr_best(sb, P, w, zhi):
    Mi = np.linalg.inv(m2(sb))
    lo, hi = 0.0, 1.0
    best = None
    for _ in range(34):
        z = (lo + hi) / 2 * zhi
        Pv = cp.Variable((2, 2), symmetric=True)
        t = cp.Variable()
        FT = Pv @ Mi
        cons = [Pv >> np.eye(2), t <= 1]
        for j in range(P.shape[1]):
            X = FT @ m2(sb + z / w[j] * P[:, j])
            cons.append((X + X.T) / 2 >> t * np.eye(2))
        tv = None
        for solver in ('CLARABEL', 'SCS'):
            try:
                cp.Problem(cp.Maximize(t), cons).solve(solver=solver)
                tv = t.value
                break
            except Exception:
                continue
        if tv is not None and tv >= -1e-9:
            lo = (lo + hi) / 2
            Fv = Pv.value @ Mi
            b = bound(Fv, sb, P, w)
            best = b if best is None else max(best, b)
        else:
            hi = (lo + hi) / 2
    return best, hi * zhi


def bcm_best(sb, P, w, n=200000):
    best = -np.inf
    for phi in np.linspace(0, 2 * np.pi, n, endpoint=False):
        FT = np.cos(phi) * np.eye(2) + np.sin(phi) * J
        b = bound(FT, sb, P, w)
        if b > best:
            best = b
    return best


INST = {
    'A': (['0', '5/2', '-1/2', '-1/2'], [['-5', '3', '4', '-4'], ['-8', '12', '-8', '8'],
                                        ['-3/2', '-4', '2', '-7/2'], ['-7/2', '-1/2', '3/2', '-4']]),
    'B': (['-3', '-5/2', '1/2', '-2'], [['1', '1', '-7', '-4'], ['-1/2', '-1/2', '-11/2', '-7'],
                                        ['1/2', '1', '-5/2', '0'], ['-7/2', '4', '-7/2', '2']]),
    'S1': (['-4', '-1', '-1/2', '-2'], [['3', '3', '-3', '-3'], ['95/24', '4', '-4', '-4'],
                                        ['17/3', '6', '-3/2', '-3/2'], ['41/6', '3', '-6', '-2']]),
}
for name, (sbs, vs) in INST.items():
    sb = np.array([float(Fr(x)) for x in sbs])
    P = np.stack([np.array([float(Fr(x)) for x in v]) - sb for v in vs], 1)
    w = np.ones(4)
    pr, prh = pr_best(sb, P, w, 1.0)
    print('%-3s point rule: explicit-set bound %.7f (bisection upper %.7f); BCM scan %.7f' % (
        name, pr, prh, bcm_best(sb, P, w)))

print('Proposition 11 corner (w = 1):')
for k in range(1, 7):
    dl = 10.0 ** (-k)
    sb = np.array([1.0, 0, 0, dl])
    P = np.array([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, -dl], [0, 0, -dl, 0]], float).T
    w = np.ones(4)
    scip = bound(np.eye(2), sb, P, w)
    cdiag = bound(np.diag([1, 1 / dl]), sb, P, w)
    b = bcm_best(sb, P, w, n=100000)
    print('  delta %.0e: SCIP %.6e (2 sqrt(delta) = %.6e), C_diag %.6f, BCM scan %.6f = %.3f sqrt(delta)' % (
        dl, scip, 2 * np.sqrt(dl), cdiag, b, b / np.sqrt(dl)))
