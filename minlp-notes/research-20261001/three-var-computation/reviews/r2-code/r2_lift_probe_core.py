"""Reviewer r2 core (copied from r2_lift_probe.py): independent hull depth (five-tetrahedron primal lift, cvxpy + Clarabel) at the
saved near-strict base points of the failed strict attempts spar100-050-1 and spar100-050-2,
for the 100 triples that were deepest in the original audits. Diagnostic only: these points
are not strict (enforced triangles up to 1.6e-8) and not all triples are probed.
depth(M) = -min{t : M + t*Mc = sum_p A_p W_p A_p', W_p PSD and >= 0}  (Lemma 2 by duality).
Run from three-var-computation/: python reviews/r2-code/r2_lift_probe.py
"""
import itertools
import json
import os

import cvxpy as cp
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MC = np.full((4, 4), 0.25)
MC[0, :] = MC[:, 0] = 0.5
MC[0, 0] = 1
for a in range(1, 4):
    MC[a, a] = 1 / 3
TETS = [[(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)], [(1, 1, 0), (1, 0, 0), (0, 1, 0), (1, 1, 1)],
        [(1, 0, 1), (1, 0, 0), (0, 0, 1), (1, 1, 1)], [(0, 1, 1), (0, 1, 0), (0, 0, 1), (1, 1, 1)],
        [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]]
ABAR = [np.array([[1, *v] for v in t], float).T for t in TETS]
Mpar = cp.Parameter((4, 4), symmetric=True)
t = cp.Variable()
Ws = [cp.Variable((4, 4), PSD=True) for _ in ABAR]
prob = cp.Problem(cp.Minimize(t), [W >= 0 for W in Ws] +
                  [sum(A @ W @ A.T for A, W in zip(ABAR, Ws)) == Mpar + t * MC])


def depth(M):
    Mpar.value = (M + M.T) / 2
    prob.solve(solver='CLARABEL', tol_gap_abs=1e-11, tol_gap_rel=1e-11, tol_feas=1e-11)
    return -float(t.value), prob.status


