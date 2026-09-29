"""Sanity checks: representations equal f; a few root propagation runs."""
import math, random
import sympy as sp
import inst as I
from ifbbt import DAG
random.seed(1)
for name in ['nondeg1', 'nondeg1s', 'h1', 'linediag', 'iso2', 'rot0.1', 'rot1', 'nd2', 'line3']:
    d = I.make(name)
    F = sp.lambdify(d['syms'], d['f'])
    err = 0
    for rep, g in d['reps'].items():
        for _ in range(200):
            p = [random.uniform(a, b) for a, b in d['box']]
            err = max(err, abs(g.f(p) - F(*p)))
    print(name, 'max rep error', f'{err:.1e}', list(d['reps']))
q = DAG(1); p2 = q.pow(0, 2); q.sum([p2, 0], [1, -2], 1)
for eps in [1e-2, 1e-4, 1e-6]:
    out = []
    for sch in ('hc4', 'chaotic'):
        st, Z, r = q.propagate([(0.2, 2.2)], -eps, max_rounds=10**6, schedule=sch)
        out.append(f'{sch}: {st} {r} ({r*math.sqrt(eps):.3f})')
    n1 = I.make('nondeg1')
    for rep in ('u', 'mono'):
        st, Z, r = n1['reps'][rep].propagate(n1['box'], -eps)
        out.append(f'nondeg1 {rep}: {st} {r}')
    print(eps, ' | '.join(out))
