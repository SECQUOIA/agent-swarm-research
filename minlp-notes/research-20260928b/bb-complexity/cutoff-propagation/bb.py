"""Toy spatial branch-and-bound: alphaBB bounds + optional cutoff FBBT.

Model (as in the note): incumbent UBD = f* from the start; a node is pruned
when its bound is >= f* - eps.  At every node:
  1. (optional) cutoff FBBT: HC4 on the DAG with root <= f* - eps, either to a
     numerical fixed point ('fix') or for R rounds (integer).  Empty -> leaf.
     Otherwise the node box is replaced by the contracted box.
  2. alphaBB bound  min_B f - alpha * sum (x_i-l_i)(u_i-x_i)  (convex for the
     chosen alpha), computed by L-BFGS-B plus the linearization bound
     phi(xh) + sum_i min(g_i (l_i-xh_i), g_i (u_i-xh_i)), which is a valid
     lower bound for a convex phi.  Bound >= f* - eps -> leaf.
  3. Otherwise bisect the widest side at its midpoint.
Counts: processed nodes, relaxations solved, FBBT-pruned and relaxation-pruned
leaves, total FBBT rounds.
"""
import sys
import json
import numpy as np
from scipy.optimize import minimize
from fbbt import hc4
import instances as I


class Relax:
    def __init__(self, inst):
        self.F, self.G, _ = I.lambdas(inst)
        self.alpha = inst['alpha']
        self.n = len(inst['syms'])

    def lb(self, box):
        l = np.array([b[0] for b in box]); u = np.array([b[1] for b in box])
        a = self.alpha
        F, G = self.F, self.G

        def phi(x):
            return float(F(*x)) - a * float(np.sum((x - l) * (u - x)))

        def dphi(x):
            return np.array(G(*x), dtype=float).reshape(-1) - a * (u + l - 2 * x)

        x0 = 0.5 * (l + u)
        r = minimize(phi, x0, jac=dphi, method='L-BFGS-B', bounds=list(zip(l, u)),
                     options=dict(gtol=1e-13, ftol=1e-16, maxiter=500))
        xh = np.clip(r.x, l, u)
        g = dphi(xh)
        return phi(xh) + float(np.sum(np.minimum(g * (l - xh), g * (u - xh))))


def run(inst, rep, eps, mode='off', max_nodes=400000, max_rounds_fix=200000):
    relax = Relax(inst)
    dag = inst['reps'][rep] if rep else None
    fstar = inst['fstar']
    cut = fstar - eps
    stack = [list(inst['box'])]
    c = dict(nodes=0, relax=0, fbbt_leaves=0, relax_leaves=0, rounds=0, limit_hits=0)
    while stack:
        box = stack.pop()
        c['nodes'] += 1
        if c['nodes'] > max_nodes:
            c['aborted'] = True
            break
        if mode != 'off':
            R = max_rounds_fix if mode == 'fix' else int(mode)
            st, vb, r = hc4(dag, box, cut, max_rounds=R)
            c['rounds'] += r
            if st == 'empty':
                c['fbbt_leaves'] += 1
                continue
            if st == 'limit' and mode == 'fix':
                c['limit_hits'] += 1
            box = [tuple(v) for v in vb]
        c['relax'] += 1
        if relax.lb(box) >= cut:
            c['relax_leaves'] += 1
            continue
        w = [hi - lo for lo, hi in box]
        i = int(np.argmax(w))
        lo, hi = box[i]
        m = 0.5 * (lo + hi)
        b1 = list(box); b1[i] = (lo, m)
        b2 = list(box); b2[i] = (m, hi)
        stack += [b2, b1]
    return c


if __name__ == '__main__':
    name, rep, mode = sys.argv[1], sys.argv[2], sys.argv[3]
    eps_list = [float(e) for e in sys.argv[4].split(',')]
    inst = I.make(name)
    for eps in eps_list:
        res = run(inst, None if rep == '-' else rep, eps, mode)
        print(json.dumps(dict(inst=name, rep=rep, mode=mode, eps=eps, **res)), flush=True)
