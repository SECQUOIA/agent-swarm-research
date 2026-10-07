"""Window 0 at the bundle center, binaries fixed to all-off: does default SCIP find 168.1087?"""
import json, sys
import numpy as np
import period, bundle

D = period.setup(6)
M, S = D['M'], D['S']
k = json.load(open('logs/bundle_06_w1_trial2.json'))  # multipliers of the diagnosis (second bundle run)
w = 0
u0 = np.array(k['cuts'][w][0][2])
lam, mu = bundle.unpack(u0, 6)
objc = period.window_objective(D, w, w + 1, lam, mu)
settings = {'default': {}, 'noprop': {'propagating/maxrounds': 0, 'propagating/maxroundsroot': 0},
            'nopresolve': {'presolving/maxrounds': 0}}
for name, prm in settings.items():
    m, X = period.build(D, w, w + 1, objc, prm)
    for v in S['per_vars'][w]:
        if M['vt'][v] == 'B':
            m.chgVarUb(X[v], 0.0)
    m.optimize()
    print(name, 'all-off:', m.getStatus(), m.getDualbound(), m.getPrimalbound() if m.getNSols() else None, flush=True)
    m.freeProb()
