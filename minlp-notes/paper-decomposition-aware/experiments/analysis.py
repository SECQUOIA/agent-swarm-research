"""Exact quantities of the analysis, computed outside the solver.

* ``lemma_heights``: the height constants of (eq:exact-constants) in the
  paper (Delta, R, Omega). The solver's exact-output wrapper uses the larger
  row-sum constant of Remark rem:heights instead (exact_output.rational_heights).
* ``growth_certificate``: the sufficient condition of Lemma lem:growthcert(a)
  at a rational point of a continuous box QP, with a certified lower bound on
  the growth constant g and a certified upper bound on g, hence a bracket for
  kappa = max{1, L/g} with L = max_i max{H_ii, 0}.
All arithmetic that enters a claim is exact; floating point only proposes
numbers that are then checked exactly.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import lcm

import numpy as np

from instances import is_psd


def lemma_heights(problem):
    """Delta, R and Omega of (eq:exact-constants) for a BoxQP without fixed coordinates."""
    n = len(problem.b)
    H = problem.A
    for i, (lo, hi) in enumerate(problem.bounds):
        if lo == hi:
            raise ValueError('substitute fixed coordinates first')
        if i in problem.integers and (lo.denominator != 1 or hi.denominator != 1):
            raise ValueError('round integer endpoints inward first')
    dens = [problem.constant.denominator] + [v.denominator for v in problem.b]
    dens += [(H[i][i] / 2).denominator for i in range(n)]
    dens += [H[i][j].denominator for i in range(n) for j in range(i + 1, n)]
    dens += [v.denominator for pair in problem.bounds for v in pair]
    delta = lcm(*dens)
    R = delta
    for i in range(n):
        if i not in problem.integers and H[i][i] > 0:      # i in I_C^+
            pii = delta * H[i][i]
            assert pii.denominator == 1
            R *= pii.numerator
    return {'Delta': delta, 'R': R, 'Omega': delta * R * R}


def _lam_min(matrix) -> float:
    return float(np.linalg.eigvalsh(np.array([[float(v) for v in row] for row in matrix]))[0])


def growth_certificate(problem, x):
    """Check Lemma lem:growthcert(a) at x and bracket g and kappa.

    Returns a dict with 'status' ('certified' or the reason of failure). When
    certified, x is the unique global minimizer, F(z) - F(x) >= gamma |z - x|^2
    on the box, and g <= g_ub, where g is the best growth constant.
    """
    n = len(x)
    H, b = problem.A, problem.b
    if problem.integers:
        raise ValueError('continuous instances only')
    zeta = [b[i] + sum(H[i][j] * x[j] for j in range(n)) for i in range(n)]
    S = [i for i, (lo, hi) in enumerate(problem.bounds) if lo < x[i] < hi]
    A = [i for i in range(n) if i not in S]
    out = {'n_free': len(S), 'n_active': len(A)}
    if any(zeta[i] != 0 for i in S):
        return dict(out, status='gradient not zero on free coordinates')
    for i in A:
        lo, hi = problem.bounds[i]
        if (x[i] == lo and zeta[i] < 0) or (x[i] == hi and zeta[i] > 0):
            return dict(out, status='gradient not inward at an active coordinate')
    if any(zeta[i] == 0 for i in A):
        out['degenerate_active'] = sum(zeta[i] == 0 for i in A)
    mu = {i: abs(zeta[i]) / (problem.bounds[i][1] - problem.bounds[i][0]) for i in A}
    K = [[H[i][j] + (2 * mu.get(i, 0) if i == j else 0) for j in range(n)] for i in range(n)]
    lam = _lam_min(K)
    out['lambda_min_H_plus_2M'] = lam
    if lam <= 0:
        return dict(out, status='H + 2M not positive definite')
    gamma = None
    for factor in (0.999, 0.99, 0.9, 0.5):
        cand = F(int(lam / 2 * factor * 2 ** 30), 2 ** 30)
        if cand > 0 and is_psd([[K[i][j] - (2 * cand if i == j else 0) for j in range(n)]
                                for i in range(n)]):
            gamma = cand
            break
    if gamma is None:
        return dict(out, status='exact PSD test failed')
    # Upper bounds on g: Lemma lem:growthcert(b) on the free block, and the
    # definition of g at the feasible points that move one active coordinate
    # to its other endpoint.
    f0 = problem.value(tuple(x))
    ubs = []
    if S:
        hss = [[H[i][j] for j in S] for i in S]
        _, vecs = np.linalg.eigh(np.array([[float(v) for v in row] for row in hss]))
        v = [F(float(t)).limit_denominator(10 ** 6) for t in vecs[:, 0]]
        if any(v):
            ubs.append(sum(v[a] * hss[a][c] * v[c] for a in range(len(S)) for c in range(len(S)))
                       / (2 * sum(t * t for t in v)))
    for i in A:
        lo, hi = problem.bounds[i]
        y = list(x)
        y[i] = hi if x[i] == lo else lo
        ubs.append((problem.value(tuple(y)) - f0) / (y[i] - x[i]) ** 2)
    g_ub = min(ubs)
    assert g_ub >= gamma, 'inconsistent growth bracket'
    L = max(max(H[i][i], F(0)) for i in range(n))
    return dict(out, status='certified', gamma=str(gamma), g_ub=str(g_ub), L=str(L),
                kappa_lb=float(max(F(1), L / g_ub)), kappa_ub=float(max(F(1), L / gamma)))
