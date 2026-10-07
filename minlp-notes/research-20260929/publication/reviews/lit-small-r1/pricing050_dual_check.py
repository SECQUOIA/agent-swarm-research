"""Reviewer check (numerical evidence only, double precision): Lagrangian dual of pricing050
over its 5 rows, computed from the cached OSIL with the reviewer's own reader.
Min form: f(x) = sum_i c_i x_i (OSIL maximizes -f), rows sum_i G_ji(x_i) >= b_j.
q(lam) = lam.b + sum_i min_{t in [0,10]} (c_i t - sum_j lam_j G_ji(t)) <= min f (weak duality).
Also estimates the relative row relaxation delta needed for a point with f = 1813.3:
v(delta) >= q(lam) - delta * lam.b  for rows relaxed to sum G >= (1-delta) b.
"""
import os, sys
import numpy as np
from scipy.optimize import minimize, minimize_scalar
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from osil_eval import Model, _tag
m = Model(os.path.expanduser('~/.cache/minlplib/minlplib/osil/pricing050.osil'))
assert m.sense == 'max' and all(v['lb'] == '0' and v['ub'] == '10' for v in m.vars)
n, J = m.n, m.m
c = np.zeros(n)
for i, v in m.obj_lin.items():
    c[i] = -float(v)          # f = -objective
b = np.array([-float(con['ub']) for con in m.cons])
assert all(con['lb'] in ('-INF', '-inf') for con in m.cons) and all(len(l) == 0 for l in m.lin)

def npev(e, t):
    tg = _tag(e); ch = list(e)
    if tg == 'variable': return float(e.get('coef', '1')) * t
    if tg == 'number': return float(e.get('value')) + 0 * t
    if tg == 'sum': return sum(npev(x, t) for x in ch)
    if tg == 'product':
        p = 1.0
        for x in ch: p = p * npev(x, t)
        return p
    if tg == 'negate': return -npev(ch[0], t)
    if tg == 'power': return npev(ch[0], t) ** npev(ch[1], t)
    if tg == 'square': return npev(ch[0], t) ** 2
    if tg == 'exp': return np.exp(npev(ch[0], t))
    raise ValueError(tg)

def varidx(e):
    s = set()
    for x in e.iter():
        if _tag(x) == 'variable': s.add(int(x.get('idx')))
    return s

terms = {}   # (j, i) -> element tree of -G_ji
for j in range(J):
    for term in m.nl[j]:
        vs = varidx(term); assert len(vs) == 1
        i = vs.pop(); assert (j, i) not in terms
        terms[(j, i)] = term
T = np.linspace(0.0, 10.0, 20001)
G = np.zeros((J, n, T.size))
for (j, i), term in terms.items():
    G[j, i] = -npev(term, T)

def inner(lam, i, refine=False):
    vals = c[i] * T - lam @ G[:, i, :]
    k = int(np.argmin(vals))
    if not refine: return vals[k], T[k]
    def h(t):
        tt = np.array([t])
        return c[i] * t - sum(lam[j] * (-npev(terms[(j, i)], tt)[0]) for j in range(J) if (j, i) in terms)
    lo, hi = T[max(k - 1, 0)], T[min(k + 1, T.size - 1)]
    r = minimize_scalar(h, bounds=(lo, hi), method='bounded', options={'xatol': 1e-12})
    return min(vals[k], r.fun), (r.x if r.fun < vals[k] else T[k])

def q(lam, refine=False):
    lam = np.maximum(lam, 0)
    return lam @ b + sum(inner(lam, i, refine)[0] for i in range(n))

best = None
for start in [np.ones(J), 2 * np.ones(J), 0.5 * np.ones(J)]:
    r = minimize(lambda l: -q(l), start, method='Nelder-Mead',
                 options={'maxiter': 20000, 'maxfev': 20000, 'xatol': 1e-10, 'fatol': 1e-10})
    if best is None or r.fun < best.fun: best = r
lam = np.maximum(best.x, 0)
qv = q(lam, refine=True)
xs = np.array([inner(lam, i, True)[1] for i in range(n)])
rows = np.array([sum(G_ji for G_ji in [0]) for _ in range(J)])
print('lambda* ~', np.array2string(lam, precision=6))
print('q(lambda*) (refined 1-D minima) = %.6f' % qv)
print('lambda.b = %.3f' % (lam @ b))
print('f(x(lambda)) = %.6f' % (c @ xs))
target = 1813.3
print('relative row relaxation needed for f = 1813.3: delta >= (q - 1813.3)/(lambda.b) = %.2e' % ((qv - target) / (lam @ b)))
print('equivalently an absolute violation of about %.3f in the rows (b_j = %s)' % ((qv - target) / lam.sum() if lam.sum() > 0 else float('nan'), b.astype(int).tolist()))
