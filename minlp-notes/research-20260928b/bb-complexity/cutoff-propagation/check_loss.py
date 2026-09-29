"""Propagation bound pi_D(C) on cubes C = y + [-r, r]^n around optimal points.

pi_D(C) = inf{c : fixed-point cutoff FBBT does not empty C}, computed by
bisection on c with HC4 (up to 20000 rounds; a round limit counts as
"not empty", so the estimate can only be too low).

Compared with the first-order losses of Section 4 of the note, computed from
the term gradients of the flat monomial representation at y:
  L(y)   = sum_j |grad g_j(y)|_1 - 2 max_j |grad g_j(y)|_1      (cube witness)
  D_i(y) = sum_j |d_i g_j(y)|   - 2 max_j |d_i g_j(y)|           (segment witness)
The witness lemma gives pi_D(C) <= f(y) - max(L, max_i D_i) r + O(r^2).
Run: python3 check_loss.py > logs/check_loss.log
"""
import numpy as np
import sympy as sp
from fbbt import hc4, forward_lb, evaluate
import instances as I


def term_grads(inst, y):
    terms, _ = I.poly_terms(inst['f'], inst['syms'])
    G = []
    for coef, exps in terms:
        g = np.zeros(len(y))
        for i, e in exps.items():
            v = coef * e * y[i] ** (e - 1)
            for k, e2 in exps.items():
                if k != i:
                    v *= y[k] ** e2
            g[i] = v
        G.append(g)
    return np.array(G)


def losses(inst, y):
    G = term_grads(inst, y)
    l1 = np.abs(G).sum(axis=1)
    L = l1.sum() - 2 * l1.max()
    D = [np.abs(G[:, i]).sum() - 2 * np.abs(G[:, i]).max() for i in range(len(y))]
    return L, D


def pi_bisect(dag, box, fy, iters=40):
    lo = forward_lb(dag, box)
    hi = fy
    st, _, _ = hc4(dag, box, lo - 1e-12, max_rounds=20000)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        st, _, _ = hc4(dag, box, mid, max_rounds=20000)
        if st == 'empty':
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


CASES = [
    ('h1', 'exp', [1.0]),
    ('linediag', 's', [1.5, 0.5]),
    ('linediag', 'exp', [1.5, 0.5]),
    ('linediag', 'exp', [1.2, 0.2]),
    ('linediag', 'exp', [2.0, 1.0]),
    ('linediag', 'exp', [1.0, 0.0]),   # t = 0: D_i = 0 but L = 8 (revision item 4)
    ('iso2', 'exp', [1.0, 1.0]),
    ('rot0.1', 'st', [1.0, 0.0]),
    ('rot0.1', 'exp', [1.0, 0.0]),
    ('rot0.01', 'exp', [1.0, 0.0]),
]

if __name__ == '__main__':
    for name, rep, y in CASES:
        inst = I.make(name)
        dag = inst['reps'][rep]
        fy = evaluate(dag, y)
        if rep == 'exp':
            L, D = losses(inst, np.array(y))
            head = f'L={L:.4g} D_i={[round(d, 4) for d in D]}'
        else:
            head = 'lifted representation'
        print(f'{name} rep={rep} y={y} f(y)={fy:.2e} {head}')
        for r in (0.1, 0.03, 0.01, 0.003, 0.001):
            box = [(max(lo, yi - r), min(hi, yi + r)) for (lo, hi), yi in zip(inst['box'], y)]
            p = pi_bisect(dag, box, fy)
            fl = forward_lb(dag, box)
            print(f'   r={r:<6} pi_D(C)={p:+.4e}  (f(y)-pi)/r={(fy - p) / r:8.4f}  '
                  f'forward LB={fl:+.4e} (f(y)-LB)/r={(fy - fl) / r:8.4f}')
