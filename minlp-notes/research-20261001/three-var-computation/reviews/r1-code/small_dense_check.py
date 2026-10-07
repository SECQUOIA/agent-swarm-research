"""Reviewer r1: Section 4.2 checks (no stream imports).

1. Recount the small-dense logs: records, seeds per file, gaps (opt - B_safe > 1e-6 max(1,|opt|)),
   largest relative gaps.
2. The AP gap instance (n=9, density 75, seed 586): regenerate it with the generator as
   documented in code/small_dense.py (re-typed here), compute the optimum by an independent
   enumeration, and solve B (Shor + McCormick + Y_ii <= x_i + all triangles) and B + the
   six-tetrahedron exact lift on every triple with cvxpy/Clarabel.
Run from three-var-computation/: python reviews/r1-code/small_dense_check.py
"""
import glob
import itertools
import json
import os
import sys
import warnings

import cvxpy as cp
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lift_depth import ABAR6  # noqa: E402

warnings.filterwarnings('ignore')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L = os.path.join(ROOT, 'logs/small_dense')

for variant, pat in (('spar', 'n*_d*.jsonl'), ('ap', 'ap_*.jsonl')):
    recs, files = [], {}
    for p in sorted(glob.glob(os.path.join(L, pat))):
        rs = [json.loads(x) for x in open(p) if x.strip()]
        files[os.path.basename(p)] = (len(rs), len({r['seed'] for r in rs}), min(r['seed'] for r in rs), max(r['seed'] for r in rs))
        recs += rs
    gaps = [r for r in recs if r['opt'] - r['B_safe'] > 1e-6 * max(1, abs(r['opt']))]
    print(variant, 'files', len(files), 'records', len(recs), 'all files 1000 distinct seeds 1..1000:',
          all(v == (1000, 1000, 1, 1000) for v in files.values()))
    print('  gaps:', [(r['n'], r['dens'], r['seed'], r['opt'], r['B'], r['B_safe']) for r in gaps])
    print('  max (opt-B)/max(1,|opt|): %.3e   max (opt-B_safe)/max(1,|opt|): %.3e   min (opt-B): %.3e' % (
        max((r['opt'] - r['B']) / max(1, abs(r['opt'])) for r in recs),
        max((r['opt'] - r['B_safe']) / max(1, abs(r['opt'])) for r in recs),
        min(r['opt'] - r['B'] for r in recs)))
    st = {}
    for r in recs:
        st[r['B_st']] = st.get(r['B_st'], 0) + 1
    print('  B status counts:', st, ' plus-diagonal counts>=3:', sum(r['plus'] >= 3 for r in recs))


def gen(n, dens, seed, variant):
    rng = np.random.default_rng(seed)
    Q = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1):
            if rng.random() * 100 <= dens:
                Q[i, j] = rng.integers(-50, 51)
            Q[j, i] = Q[i, j]
    c = rng.integers(-50, 51, size=n).astype(float)
    if variant == 'ap':
        c = c * (rng.random(n) * 100 <= dens)
    return Q, c


def enum_min(H, g):
    """Minimum over [0,1]^n: every face, KKT point of the face interior (lstsq for singular faces
    is not needed for a lower bound check, so singular faces are handled by also taking vertices)."""
    n = len(g)
    best = np.inf
    for fixed in itertools.product((0, 1, None), repeat=n):
        F = [i for i in range(n) if fixed[i] is None]
        x = np.array([0.0 if v is None else float(v) for v in fixed])
        if F:
            G = [i for i in range(n) if fixed[i] is not None]
            A = 2 * H[np.ix_(F, F)]
            rhs = -(g[F] + 2 * H[np.ix_(F, G)] @ x[G])
            try:
                xf = np.linalg.solve(A, rhs)
            except np.linalg.LinAlgError:
                continue
            if (xf < -1e-12).any() or (xf > 1 + 1e-12).any():
                continue
            x[F] = np.clip(xf, 0, 1)
        best = min(best, x @ H @ x + g @ x)
    return best


def relax(H, g, lift):
    n = len(g)
    Z = cp.Variable((n + 1, n + 1), symmetric=True)
    x, Y = Z[0, 1:], Z[1:, 1:]
    cons = [Z >> 0, Z[0, 0] == 1, x >= 0, x <= 1, cp.diag(Y) <= x]
    for i in range(n):
        for j in range(i + 1, n):
            cons += [Y[i, j] >= 0, Y[i, j] >= x[i] + x[j] - 1, Y[i, j] <= x[i], Y[i, j] <= x[j]]
    for i, j, k in itertools.combinations(range(n), 3):
        cons += [Y[i, j] + Y[i, k] - x[i] - Y[j, k] <= 0, Y[i, j] + Y[j, k] - x[j] - Y[i, k] <= 0,
                 Y[i, k] + Y[j, k] - x[k] - Y[i, j] <= 0, x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] <= 1]
        if lift:
            idx = [0, i + 1, j + 1, k + 1]
            Ws = [cp.Variable((4, 4), PSD=True) for _ in ABAR6]
            cons += [W >= 0 for W in Ws]
            S = sum(A @ W @ A.T for A, W in zip(ABAR6, Ws))
            cons += [S[r, s] == Z[idx[r], idx[s]] for r in range(4) for s in range(r, 4)]
    pr = cp.Problem(cp.Minimize(cp.trace(H @ Y) + g @ x), cons)
    pr.solve(solver='CLARABEL', tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
    return pr.value, pr.status


Q, c = gen(9, 75, 586, 'ap')
H, g = -Q, -c
opt = enum_min(H, g)
B, sB = relax(H, g, False)
X, sX = relax(H, g, True)
print('\nAP n=9 d=75 seed 586: diag nonzero %d, plus %d, linear nonzero %d' % ((np.diag(Q) != 0).sum(), (np.diag(H) > 0).sum(), (c != 0).sum()))
print('  enumerated optimum %.10f' % opt)
print('  B (cvxpy, primal) %.10f %s   gap %.3e' % (B, sB, opt - B))
print('  B + 6-tetra lift on all 84 triples %.10f %s   gap %.3e' % (X, sX, opt - X))
