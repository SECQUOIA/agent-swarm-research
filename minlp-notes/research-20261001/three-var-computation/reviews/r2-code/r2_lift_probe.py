"""Reviewer r2: independent hull depth (five-tetrahedron primal lift, cvxpy + Clarabel) at the
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


def tri_cap(M):
    x, Y = M[0, 1:], M[1:, 1:]
    tv = max(Y[0, 1] + Y[0, 2] - x[0] - Y[1, 2], Y[0, 1] + Y[1, 2] - x[1] - Y[0, 2],
             Y[0, 2] + Y[1, 2] - x[2] - Y[0, 1], x.sum() - Y[0, 1] - Y[0, 2] - Y[1, 2] - 1)
    return tv, float(np.max(np.diag(Y) - x))


# sanity: Mc has depth 1; rank-one cube points have depth ~0
print('depth(Mc) =', depth(MC))
rng = np.random.default_rng(1)
v = np.r_[1, rng.random(3)]
print('depth(rank one) =', depth(np.outer(v, v)))
for name in ('spar100-050-1', 'spar100-050-2'):
    z = np.load(os.path.join(ROOT, 'logs/strict_r1', name + '.base.npz'))
    x, Y = z['x'], z['Y']
    zo = np.load(os.path.join(ROOT, 'logs/spar_audit', name + '.json.base.npz'))
    T = np.load(os.path.join(ROOT, 'reviews/r2-logs', name + '_probe_triples.npy'))
    out = []
    for tr in T:
        idx = [0] + [a + 1 for a in tr]
        M = np.block([[np.ones((1, 1)), x[None, :]], [x[:, None], Y]])[np.ix_(idx, idx)]
        Mo = np.block([[np.ones((1, 1)), zo['x'][None, :]], [zo['x'][:, None], zo['Y']]])[np.ix_(idx, idx)]
        d, st = depth(M)
        do, _ = depth(Mo)
        tv, cap = tri_cap(M)
        out.append(dict(T=tr.tolist(), depth_new=d, depth_orig_point=do, status=st, tv=tv, cap=cap,
                        bound=min(-4 * max(tv, 0), -6 * max(cap, 0))))
    print(json.dumps(dict(name=name, probed=len(out),
                          statuses=sorted(set(o['status'] for o in out)),
                          min_depth_new=min(o['depth_new'] for o in out),
                          min_depth_orig_point=min(o['depth_orig_point'] for o in out),
                          max_tv_new=max(o['tv'] for o in out), max_cap_new=max(o['cap'] for o in out),
                          deepest_new=min(out, key=lambda o: o['depth_new']),
                          first=out[0])))
