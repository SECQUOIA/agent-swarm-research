"""Diagnose: SCIP solution of window 0 at u_2 is better at the center than SCIP's optimum at the center."""
import json, sys
import numpy as np
from fractions import Fraction
import period, bundle

D = period.setup(6)
M, S = D['M'], D['S']
k = json.load(open('logs/bundle_06_w1_trial2.json'))  # multipliers of the diagnosis (second bundle run)
w = int(sys.argv[1]); j = int(sys.argv[2])
u0 = np.array(k['cuts'][w][0][2]); uj = np.array(k['cuts'][w][j][2])

def rowviol(x, t0, t1):
    worst = (0.0, None)
    rows = [i for t in range(t0, t1) for i in S['per_rows'][t]]
    for i in rows:
        r = M['rows'][i]
        s = 0.0
        for mono, a in r['poly'].items():
            tt = float(a)
            for v in mono: tt *= x[v]
            s += tt
        v = 0.0
        if r['lb'].upper() != '-INF': v = max(v, float(r['lb']) - s)
        if r['ub'].upper() not in ('INF', '+INF'): v = max(v, s - float(r['ub']))
        if v > worst[0]: worst = (v, r['name'])
    bw = 0.0
    for t in range(t0, t1):
        for vv in S['per_vars'][t]:
            if M['lb'][vv].upper() != '-INF': bw = max(bw, float(M['lb'][vv]) - x[vv])
            if M['ub'][vv].upper() not in ('INF', '+INF'): bw = max(bw, x[vv] - float(M['ub'][vv]))
    return worst, bw

for name, u in (('center', u0), ('uj', uj)):
    lam, mu = bundle.unpack(u, 6)
    r = period.solve_window(D, w, w + 1, lam, mu, 300)
    lam0, mu0 = bundle.unpack(u0, 6)
    objc0 = period.window_objective(D, w, w + 1, lam0, mu0)
    at_center = sum(c * r['x'][v] for v, c in objc0.items())
    print(name, r['status'], 'dual', r['dual'], 'primal', r['primal'], 'obj at center', at_center,
          'viol', rowviol(r['x'], w, w + 1), 'nodes', r['nodes'])
    bins = {M['names'][v]: r['x'][v] for v in S['per_vars'][w] if M['vt'][v] == 'B'}
    print('   binaries', {n: round(b, 9) for n, b in bins.items()})
    json.dump({M['names'][v]: val for v, val in r['x'].items()}, open(f'logs/diag_w{w}_{name}.json', 'w'))
