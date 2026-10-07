"""Numerical test of the sign-class results (note.md, Section 2.3).

Samples boundary rays of the cones
    S_sub = P3plus  cap {q_xy, q_xz, q_yz <= 0}   (submodular part)
    S_sup = P3plus  cap {q_xy, q_xz, q_yz >= 0}   (supermodular part)
by minimizing a moment-like linear functional w over their base
(<p, u> = 1, u = uniform moments), with the exact cube description of
P3plus.  For each sampled quadratic p (normalized to max |coef| = 1) it
records
    r_d3   = min <p, y> over the D3 moment relaxation (27 localizing matrices)
    r_bnw  = min over the Burer-Natarajan-Willemsen relaxation
             {[1 x; x X] psd, X <= x e^T}
    r_R    = min over R (D3 + 24 family LMIs)   [only for 'sup']
    cubemin = min of p over the cube (face enumeration).
Theorem 2.11 predicts r_d3 >= 0 (up to solver accuracy) on S_sub.
Numerical only.

usage: python signclass.py SEED N {sub|sup}
"""
import json
import sys
import time
import warnings

import cvxpy as cp
import numpy as np

warnings.filterwarnings("ignore")
from cube3 import QINDEX, QKEYS  # noqa: E402
from sdp3 import SOLVER_OPTS, Relaxation, Separation, cube_min  # noqa: E402

CROSS = [QINDEX[(1, 1, 0)], QINDEX[(1, 0, 1)], QINDEX[(0, 1, 1)]]


class SignSep(Separation):
    def __init__(self, sign):
        super().__init__()
        cons = list(self.prob.constraints)
        for j in CROSS:
            cons.append(self.pv[j] <= 0 if sign == 'sub' else self.pv[j] >= 0)
        self.prob = cp.Problem(self.prob.objective, cons)


class BNW:
    def __init__(self):
        self.x = cp.Variable(3)
        self.X = cp.Variable((3, 3), symmetric=True)
        Y = cp.bmat([[np.ones((1, 1)), cp.reshape(self.x, (1, 3), order='F')],
                     [cp.reshape(self.x, (3, 1), order='F'), self.X]])
        cons = [Y >> 0]
        for i in range(3):
            for j in range(3):
                cons.append(self.X[i, j] <= self.x[i])
        self.c = cp.Parameter(10)
        x, X = self.x, self.X
        mom = [1, x[0], x[1], x[2], X[0, 0], X[1, 1], X[2, 2], X[0, 1], X[0, 2], X[1, 2]]
        self.prob = cp.Problem(cp.Minimize(sum(self.c[i] * mom[i] for i in range(10))), cons)

    def solve(self, p):
        self.c.value = np.asarray(p, float)
        return self.prob.solve(**SOLVER_OPTS)


def mom(x):
    return np.array([1, x[0], x[1], x[2], x[0]**2, x[1]**2, x[2]**2,
                     x[0]*x[1], x[0]*x[2], x[1]*x[2]])


def random_w(rng):
    """Moments of a mixture of atoms, some coordinates snapped to the
    boundary and a few pushed outside the cube (as in explore_psd.py)."""
    k = rng.integers(3, 9)
    pts = rng.random((k, 3))
    snap = rng.random((k, 3)) < 0.5
    pts[snap] = np.round(pts[snap])
    out = rng.random((k, 3)) < 0.2
    pts[out] += rng.normal(0, 0.15, out.sum())
    wts = rng.random(k) + 0.1
    return sum(a * mom(x) for a, x in zip(wts, pts)) / wts.sum()


if __name__ == '__main__':
    seed, n, sign = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = np.random.default_rng(seed)
    S = SignSep(sign)
    R0 = Relaxation(use_family=False)
    R1 = Relaxation(use_family=True) if sign == 'sup' else None
    bnw = BNW()
    out = []
    t0 = time.time()
    for it in range(n):
        w = random_w(rng) if it % 2 == 0 else rng.normal(size=10)
        try:
            sv, st, p = S.solve(w)
            if p is None or st not in ('optimal', 'optimal_inaccurate'):
                continue
            p = p / np.abs(p).max()
            r0 = R0.solve(p)[0]
            rb = bnw.solve(p)
            r1 = R1.solve(p)[0] if R1 is not None else None
            cm = cube_min(p)
        except BaseException as e:  # Clarabel panics are BaseException
            if isinstance(e, KeyboardInterrupt):
                raise
            continue
        out.append(dict(p=p.tolist(), r_d3=r0, r_bnw=rb, r_R=r1, cubemin=cm, status=st))
    vals = lambda key: [o[key] for o in out if o[key] is not None]
    summary = dict(sign=sign, seed=seed, n=len(out),
                   min_r_d3=min(vals('r_d3')), min_r_bnw=min(vals('r_bnw')),
                   n_d3_below_1e6=sum(v < -1e-6 for v in vals('r_d3')),
                   n_bnw_below_1e6=sum(v < -1e-6 for v in vals('r_bnw')),
                   min_cubemin=min(vals('cubemin')), max_cubemin=max(vals('cubemin')),
                   time=time.time() - t0)
    if sign == 'sup':
        summary.update(min_r_R=min(vals('r_R')), n_R_below_1e6=sum(v < -1e-6 for v in vals('r_R')))
    print(summary, flush=True)
    json.dump(dict(summary=summary, records=out), open(f'../logs/signclass_{sign}_{seed}.json', 'w'), default=float)
