"""Diagnose SCIP's wrong 'optimal' on a window at the bundle center: try settings.
usage: python3 diag_settings.py window testname"""
import json, sys
import numpy as np
import period, bundle

D = period.setup(6)
M, S = D['M'], D['S']
k = json.load(open('logs/bundle_06_w1_trial2.json'))  # multipliers of the diagnosis (second bundle run)
w = int(sys.argv[1])
u0 = np.array(k['cuts'][w][0][2])
lam, mu = bundle.unpack(u0, 6)
tests = {
    'default': {},
    'nopresolve': {'presolving/maxrounds': 0},
    'nodualreds': {'misc/allowstrongdualreds': False, 'misc/allowweakdualreds': False},
    'noprop': {'propagating/maxrounds': 0, 'propagating/maxroundsroot': 0},
    'feastol1e-8': {'numerics/feastol': 1e-8},
    'seed7': {'randomization/randomseedshift': 7},
    'nosymmetry': {'misc/usesymmetry': 0},
    'noobbt': {'propagating/obbt/freq': -1},
    'emph_numerics': 'numerics',
}
name = sys.argv[2]
prm = tests[name]
if isinstance(prm, str):
    import pyscipopt as ps
    prm = {}
    orig = period.build
    def build2(D_, a, b, objc, params=None):
        m, X = orig(D_, a, b, objc, params)
        m.setEmphasis(ps.SCIP_PARAMEMPHASIS.NUMERICS)
        return m, X
    period.build = build2
r = period.solve_window(D, w, w + 1, lam, mu, 300, prm)
print(w, name, r['status'], r['dual'], r['primal'], round(r['time'], 1), r['nodes'], flush=True)

def rowviol(x, t0, t1):
    worst = (0.0, None)
    rows = [i for t in range(t0, t1) for i in S['per_rows'][t]]
    for i in rows:
        rr = M['rows'][i]
        s_ = 0.0
        for mono, a in rr['poly'].items():
            tt = float(a)
            for v in mono: tt *= x[v]
            s_ += tt
        v = 0.0
        if rr['lb'].upper() != '-INF': v = max(v, float(rr['lb']) - s_)
        if rr['ub'].upper() not in ('INF', '+INF'): v = max(v, s_ - float(rr['ub']))
        if v > worst[0]: worst = (v, rr['name'])
    bw = 0.0
    for t in range(t0, t1):
        for vv in S['per_vars'][t]:
            if M['lb'][vv].upper() != '-INF': bw = max(bw, float(M['lb'][vv]) - x[vv])
            if M['ub'][vv].upper() not in ('INF', '+INF'): bw = max(bw, x[vv] - float(M['ub'][vv]))
    return worst, bw
print('viol', rowviol(r['x'], w, w + 1))
print('binaries', [round(r['x'][v]) for v in S['per_vars'][w] if M['vt'][v] == 'B'])
json.dump({M['names'][v]: val for v, val in r['x'].items()}, open(f'logs/diag_w{w}_{name}.json', 'w'))
