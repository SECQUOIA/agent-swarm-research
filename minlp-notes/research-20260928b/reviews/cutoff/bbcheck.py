"""Reviewer's independent re-run of a subset of Table 7.1 of cutoff-propagation.md.

Node model as in the note: UBD = f* = 0 from the start; per node, one
propagation phase (off / fixed point / R rounds) with cutoff -eps using the
reviewer's propagator; then the uniform alphaBB bound on the contracted box;
prune if bound >= -eps; else bisect the widest side (lowest index on ties) at
its midpoint.  The alphaBB minimum is computed differently from the author's:
bisection on the derivative in 1D, scipy TNC plus a linearization bound in nD.
Run: OMP_NUM_THREADS=1 python3 bbcheck.py > logs/bbcheck.jsonl
"""
import json
import sys
from multiprocessing import Pool
import numpy as np
import sympy as sp
from scipy.optimize import minimize
import inst as I


class Bound:
    def __init__(self, d):
        s = d['syms']
        self.n = len(s)
        self.F = sp.lambdify(s, d['f'], 'math')
        self.G = sp.lambdify(s, [sp.diff(d['f'], v) for v in s], 'math')
        self.a = d['alpha']

    def lb(self, box):
        l = np.array([b[0] for b in box]); u = np.array([b[1] for b in box]); a = self.a
        phi = lambda x: self.F(*x) - a * float(np.sum((x - l) * (u - x)))
        dphi = lambda x: np.array(self.G(*x), float) - a * (u + l - 2 * x)
        if self.n == 1:
            lo, hi = l[0], u[0]
            if dphi(np.array([lo]))[0] >= 0:
                x = lo
            elif dphi(np.array([hi]))[0] <= 0:
                x = hi
            else:
                for _ in range(80):
                    mid = 0.5 * (lo + hi)
                    if dphi(np.array([mid]))[0] > 0:
                        hi = mid
                    else:
                        lo = mid
                x = 0.5 * (lo + hi)
            xh = np.array([x])
        else:
            r = minimize(phi, 0.5 * (l + u), jac=dphi, method='TNC', bounds=list(zip(l, u)),
                         options=dict(maxfun=2000, ftol=1e-16, xtol=1e-14, gtol=1e-14))
            xh = np.clip(r.x, l, u)
        g = dphi(xh)
        return phi(xh) + float(np.sum(np.minimum(g * (l - xh), g * (u - xh))))


def run(task):
    name, rep, mode, eps = task
    d = I.make(name)
    bd = Bound(d)
    dag = d['reps'][rep] if rep != '-' else None
    cut = -eps
    stack = [list(d['box'])]
    c = dict(nodes=0, rounds=0, prop_leaves=0, limit=0)
    while stack:
        box = stack.pop()
        c['nodes'] += 1
        if c['nodes'] > 60000:
            c['aborted'] = True
            break
        if mode != 'off':
            R = 200000 if mode == 'fix' else int(mode)
            st, Z, r = dag.propagate(box, cut, max_rounds=R)
            c['rounds'] += r
            if st == 'empty':
                c['prop_leaves'] += 1
                continue
            if mode == 'fix' and st == 'limit':
                c['limit'] += 1
            box = [tuple(v) for v in dag.xbox(Z)]
        if bd.lb(box) >= cut:
            continue
        w = [b - a for a, b in box]
        i = int(np.argmax(w))
        lo, hi = box[i]; m = 0.5 * (lo + hi)
        b1 = list(box); b1[i] = (lo, m)
        b2 = list(box); b2[i] = (m, hi)
        stack += [b2, b1]
    return dict(inst=name, rep=rep, mode=mode, eps=eps, **c)


TASKS = []
for e in (1e-2, 1e-4, 1e-6, 1e-8):
    TASKS += [('nondeg1', '-', 'off', e), ('nondeg1', 'u', 'fix', e), ('nondeg1', 'mono', 'fix', e)]
for e in (1e-2, 1e-4, 1e-6):
    TASKS += [('h1', '-', 'off', e), ('h1', 'exp', '10', e), ('h1', 'exp', '3', e), ('h1', 'exp', 'fix', e),
              ('nondeg1s', 'exp', '10', e), ('nd2', '-', 'off', e), ('nd2', 'mono', 'fix', e)]
for e in (1e-2, 1e-4):
    TASKS += [('iso2', '-', 'off', e), ('iso2', 'exp', 'fix', e), ('rot0.1', '-', 'off', e),
              ('rot0.1', 'exp', 'fix', e), ('rot0.1', 'st', 'fix', e), ('rot0.01', 'exp', 'fix', e),
              ('rot0.01', '-', 'off', e)]
TASKS += [('linediag', '-', 'off', 1e-3), ('linediag', 'exp', 'fix', 1e-3), ('linediag', 's', 'fix', 1e-3),
          ('linediag', 's', '10', 1e-3), ('linediag', 's', '3', 1e-3), ('linediag', 's', 'fix', 1e-6),
          ('line3', 'st', 'fix', 1e-2), ('line3', '-', 'off', 1e-2)]

if __name__ == '__main__':
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as p:
        for r in p.imap_unordered(run, TASKS):
            print(json.dumps(r), flush=True)
