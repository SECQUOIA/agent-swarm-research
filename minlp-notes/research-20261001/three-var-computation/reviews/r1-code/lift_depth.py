"""Reviewer r1: independent QPB3 depth by the primal six-tetrahedron lift (no stream imports).

For a 4x4 moment matrix M (M00 = 1), t*(M) = min t s.t. M + t*Mc = sum_p Abar_p W_p Abar_p',
W_p doubly nonnegative, over the six simplices x_s(1) <= x_s(2) <= x_s(3) (Anstreicher-Burer
Theorem 7). By conic duality t* = -delta(M), with delta of Lemma 2 (normalization <C, Mc> = 1).
This uses a different triangulation (6 instead of 5) and the primal side instead of the dual.
"""
import itertools

import cvxpy as cp
import numpy as np

MC = np.array([[1, .5, .5, .5], [.5, 1 / 3, .25, .25], [.5, .25, 1 / 3, .25], [.5, .25, .25, 1 / 3]])
ABAR6 = []
for s in itertools.permutations(range(3)):
    verts = []
    for m in range(4):          # the m coordinates largest in the order are 1
        v = [0, 0, 0]
        for t in range(3 - m, 3):
            v[s[t]] = 1
        verts.append([1] + v)
    ABAR6.append(np.array(verts, float).T)


def lift_depth(M, solver='CLARABEL'):
    t = cp.Variable()
    Ws = [cp.Variable((4, 4), PSD=True) for _ in ABAR6]
    S = sum(A @ W @ A.T for A, W in zip(ABAR6, Ws))
    cons = [W >= 0 for W in Ws] + [S == M + t * MC]
    pr = cp.Problem(cp.Minimize(t), cons)
    kw = dict(tol_gap_abs=1e-11, tol_gap_rel=1e-11, tol_feas=1e-11) if solver == 'CLARABEL' else {}
    pr.solve(solver=solver, **kw)
    return -float(t.value), pr.status


def triangle_C():
    """1 - x1 - x2 - x3 + Y12 + Y13 + Y23 >= 0 as <C, M> >= 0, normalized by <C, Mc> = 1."""
    C = np.zeros((4, 4))
    C[0, 0] = 1
    for i in range(1, 4):
        C[0, i] = C[i, 0] = -0.5
    for i in range(1, 4):
        for j in range(1, 4):
            if i != j:
                C[i, j] = 0.5
    return C / np.sum(C * MC)


if __name__ == '__main__':
    rng = np.random.default_rng(0)
    print('<C_tri, Mc> before normalization = 1/4; normalized C_tri check:', np.sum(triangle_C() * MC))
    print('depth(Mc) =', lift_depth(MC))
    x = rng.random(3)
    v = np.r_[1, x]
    print('depth(rank-one cube point) =', lift_depth(np.outer(v, v)))
