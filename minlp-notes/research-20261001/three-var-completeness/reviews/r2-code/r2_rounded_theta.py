"""Review round 2: why did one of the 265 low-cost position-search configurations
fail the retest (note.md Sec. 2.7, r1 issue 9)?

blocking_positions.py prints theta rounded to 4 decimals; positions_retest.py
and postprocess_positions.py read the rounded .txt logs, while the .json
logs keep full precision. This script re-solves the inner problem
    min ||A(theta) p||^2  s.t.  p in P3+ (six order simplices, COP_4 = PSD + NN),
    q_ii >= 0, <p, u> = 1 (uniform moments), p(0) >= 0.01
with my own implementation (no stream code imported), at the full-precision
and at the rounded theta of the excluded configuration and of a few
configurations that passed.
"""
import glob
import itertools
import json
import os

import cvxpy as cp
import numpy as np

LOGS = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
# monomial exponents: 1, x, y, z, x^2, y^2, z^2, xy, xz, yz
MONS = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 2, 0),
        (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]


def mon_val(pt):
    return np.array([np.prod([pt[i] ** a[i] for i in range(3)]) for a in MONS])


def mon_der(pt, j):
    out = []
    for a in MONS:
        if a[j] == 0:
            out.append(0.0)
            continue
        b = list(a)
        b[j] -= 1
        out.append(a[j] * np.prod([pt[i] ** b[i] for i in range(3)]))
    return np.array(out)


def rows(config, theta):
    it = iter(theta)
    R = []
    for s in config:
        pt = [next(it) if c == -1 else float(c) for c in s]
        R.append(mon_val(pt))
        for i in range(3):
            if s[i] == -1:
                R.append(mon_der(pt, i))
    return np.array(R)


def build():
    p = cp.Variable(10)
    A = cp.Parameter((12, 10))
    e = dict(zip(MONS, [p[i] for i in range(10)]))
    P = cp.bmat([
        [e[(0, 0, 0)], e[(1, 0, 0)] / 2, e[(0, 1, 0)] / 2, e[(0, 0, 1)] / 2],
        [e[(1, 0, 0)] / 2, e[(2, 0, 0)], e[(1, 1, 0)] / 2, e[(1, 0, 1)] / 2],
        [e[(0, 1, 0)] / 2, e[(1, 1, 0)] / 2, e[(0, 2, 0)], e[(0, 1, 1)] / 2],
        [e[(0, 0, 1)] / 2, e[(1, 0, 1)] / 2, e[(0, 1, 1)] / 2, e[(0, 0, 2)]]])
    u = np.array([1, .5, .5, .5, 1 / 3, 1 / 3, 1 / 3, .25, .25, .25])
    cons = [u @ p == 1, p[4] >= 0, p[5] >= 0, p[6] >= 0, p[0] >= 0.01]
    for perm in itertools.permutations(range(3)):
        verts = [np.zeros(3)]
        v = np.zeros(3)
        for i in perm:
            v = v.copy()
            v[i] = 1
            verts.append(v)
        V = np.array([np.concatenate([[1.0], w]) for w in verts]).T
        M = V.T @ P @ V
        N = cp.Variable((4, 4), symmetric=True)
        cons += [N >= 0, M - N >> 0]
    prob = cp.Problem(cp.Minimize(cp.sum_squares(A @ p)), cons)
    return prob, A


def main():
    prob, A = build()
    full = {}
    for f in sorted(glob.glob(os.path.join(LOGS, 'blocking_positions_*.json'))):
        for r in json.load(open(f)):
            full[repr(r['config'])] = r
    excluded = [[-1, -1, 0], [-1, 0, -1], [-1, 0, 0], [-1, 1, 1]]
    keys = [repr(excluded)]
    others = [kk for kk, r in full.items() if r['resid'] < 1e-8 and kk != keys[0]]
    rng = np.random.default_rng(3)
    keys += list(rng.choice(others, 5, replace=False))
    for kk in keys:
        r = full[kk]
        cfg = r['config']
        out = []
        for th in (np.array(r['theta']), np.round(np.array(r['theta']), 4)):
            Ap = np.zeros((12, 10))
            R = rows(cfg, th)
            Ap[:R.shape[0]] = R
            A.value = Ap
            try:
                prob.solve(solver='CLARABEL')
                out.append(prob.value)
            except Exception as ex:  # noqa: BLE001
                out.append('fail %s' % type(ex).__name__)
        print('%s stored %.3e | full theta %s | rounded theta %s'
              % (cfg, r['resid'], out[0] if isinstance(out[0], str) else '%.3e' % out[0],
                 out[1] if isinstance(out[1], str) else '%.3e' % out[1]), flush=True)


if __name__ == '__main__':
    main()
