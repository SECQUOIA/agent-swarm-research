"""Small dense BoxQP instances (n = 5..10) generated like the BoxQP 'spar' instances.

Generator (numpy re-implementation of util/genboxqp.m of the BoxQP repository, not
bit-identical to MATLAB's generator): Q_ij for j <= i is nonzero with probability
dens/100, then uniform integer in [-50, 50]; Q symmetric; c_i uniform integer in
[-50, 50]; problem max 0.5 x'Qx + c'x over [0,1]^n.  Anstreicher and Puges
(arXiv 2501.09150, Section 5) used instances of this kind with 5 <= n <= 10.

For each instance: the exact global minimum (min form H = -Q/2, g = -c) by
enumeration of all faces of the box (box_min), B = dense Shor + McCormick +
Y_ii <= x_i + all 4 C(n,3) triangle inequalities.  If opt - B_safe > 1e-6 max(1, |opt|)
the instance has a gap and the following are also solved, each with the constraint
family on ALL triples: X (exact Anstreicher-Burer lift), K, A, KA, F (all 24
orientations), KAF, KAX.
Resumable: seeds already present in the output file are skipped.
Variant 'ap' (optional 6th argument): c_i is also nonzero only with probability dens/100,
as in the description of Anstreicher and Puges (their data are not public), and the
problem is max x'Qx + c'x (their form, without the factor 0.5).
Usage: python small_dense.py n dens seed0 count out.jsonl [spar|ap]"""
import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from relax import Relax, ORIENTS


def gen(n, dens, seed, variant='spar'):
    rng = np.random.default_rng(seed)
    Q = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1):
            if rng.random() * 100 <= dens:
                Q[i, j] = rng.integers(-50, 51)
            Q[j, i] = Q[i, j]
    c = rng.integers(-50, 51, size=n).astype(float)
    if variant == 'ap':   # Anstreicher-Puges description: c_i also nonzero with probability dens/100
        c = c * (rng.random(n) * 100 <= dens)
    return Q, c


def box_min(H, g):
    """Exact (floating point) min of x'Hx + g'x over [0,1]^n by enumerating faces.
    On a face with free set F and fixed values x_G, an interior stationary point solves
    2 H_FF x_F = -(g_F + 2 H_FG x_G).  A minimizer exists in the relative interior of a
    face on which H_FF is nonsingular (same argument as Lemma 1 of note.md), so the
    minimum over these candidates and the vertices is the global minimum."""
    n = len(g)
    best, bestx = np.inf, None
    for r in range(n + 1):
        for F in itertools.combinations(range(n), r):
            F = list(F)
            G = [i for i in range(n) if i not in F]
            XG = np.array(list(itertools.product((0.0, 1.0), repeat=len(G))), dtype=float).reshape(2 ** len(G), len(G))
            X = np.zeros((len(XG), n))
            X[:, G] = XG
            if F:
                A = 2 * H[np.ix_(F, F)]
                if abs(np.linalg.det(A)) < 1e-9 * max(1.0, np.abs(A).max()) ** len(F):
                    continue
                rhs = -(g[F][None, :] + 2 * XG @ H[np.ix_(G, F)])
                XF = np.linalg.solve(A, rhs.T).T
                ok = ((XF >= -1e-12) & (XF <= 1 + 1e-12)).all(axis=1)
                if not ok.any():
                    continue
                X = X[ok]
                X[:, F] = np.clip(XF[ok], 0, 1)
            vals = np.einsum('ki,ij,kj->k', X, H, X) + X @ g
            k = int(np.argmin(vals))
            if vals[k] < best:
                best, bestx = float(vals[k]), X[k].copy()
    return best, bestx


def build(H, g, parts):
    n = len(g)
    R = Relax(H, g)
    for T in itertools.combinations(range(n), 3):
        for t in range(4):
            R.add_triangle(*T, t)
        if 'K' in parts:
            R.add_K(T)
        if 'A' in parts:
            R.add_A(T)
        if 'F' in parts:
            for o in ORIENTS:
                R.add_F(T, o)
        if 'X' in parts:
            R.add_X(T)
    return R


def main():
    n, dens, seed0, count, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    variant = sys.argv[6] if len(sys.argv) > 6 else 'spar'
    done = set()
    if os.path.exists(out):
        for line in open(out):
            try:
                done.add(json.loads(line)['seed'])
            except ValueError:
                pass
    with open(out, 'a') as f:
        for seed in range(seed0, seed0 + count):
            if seed in done:
                continue
            Q, c = gen(n, dens, seed, variant)
            H, g = (-Q / 2, -c) if variant == 'spar' else (-Q, -c)
            t0 = time.time()
            opt, xopt = box_min(H, g)
            rec = {'n': n, 'dens': dens, 'seed': seed, 'variant': variant, 'opt': opt, 'plus': int((np.diag(H) > 0).sum()),
                   't_enum': time.time() - t0}
            R = build(H, g, '')
            res = R.solve('clarabel', tol=1e-9)
            rec['B'] = res['pobj']; rec['B_safe'] = res['safe']; rec['B_st'] = res['status']
            rec['B_t'] = res['time_solve']; rec['B_size'] = R.m.size_summary()
            if opt - rec['B_safe'] > 1e-6 * max(1.0, abs(opt)):
                for m in ['X', 'K', 'A', 'KA', 'F', 'KAF', 'KAX']:
                    R = build(H, g, m)
                    res = R.solve('clarabel', tol=1e-9)
                    rec[m] = res['pobj']; rec[m + '_safe'] = res['safe']; rec[m + '_st'] = res['status']
                    rec[m + '_t'] = res['time_solve']; rec[m + '_size'] = R.m.size_summary()
            f.write(json.dumps(rec) + '\n')
            f.flush()


if __name__ == '__main__':
    main()
