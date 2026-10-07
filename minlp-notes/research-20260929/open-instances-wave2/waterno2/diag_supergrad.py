"""Diagnostic: check the supergradient inequality phi(u') <= phi(u) + g(u).(u'-u)."""
import json
import numpy as np
import period, bundle

D = period.setup(6)
k = json.load(open('logs/bundle_06_w1_part1.json'))
u0 = bundle.pack(k['lam'], k['mu'])
rng = np.random.default_rng(0)
u1 = u0 + rng.normal(0, 2.0, len(u0)); u1[-1] = max(u1[-1], 0)
windows = [(t, t + 1) for t in range(6)]
bundle._init(6)
R = {}
for name, u in (('u0', u0), ('u1', u1)):
    lam, mu = bundle.unpack(u, 6)
    R[name] = []
    for a, b in windows:
        r = period.solve_window(D, a, b, lam, mu, 120)
        g = bundle.window_supergradient(D, a, b, r['x'])
        # objective value of the returned x at u (recomputed)
        objc = period.window_objective(D, a, b, lam, mu)
        ov = sum(c * r['x'][v] for v, c in objc.items())
        R[name].append((r['dual'], r['primal'], ov, g, r['x'], r['status']))
for w in range(6):
    d0, p0, o0, g0, x0, s0 = R['u0'][w]
    d1, p1, o1, g1, x1, s1 = R['u1'][w]
    lam1, mu1 = bundle.unpack(u1, 6)
    objc1 = period.window_objective(D, w, w + 1, lam1, mu1)
    x0_at_u1 = sum(c * x0[v] for v, c in objc1.items())
    lin = d0 + g0 @ (u1 - u0)
    print(w, s0, s1, 'phi0', d0, 'objx0', o0, 'phi1', d1, 'lin', lin, 'x0@u1', x0_at_u1, 'viol', d1 - lin)
