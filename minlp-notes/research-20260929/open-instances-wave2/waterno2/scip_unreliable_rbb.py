"""Certified values for the periods of scip_unreliable.py (rbb), and a
tight-tolerance re-solve of each SCIP configuration with the binaries fixed."""
import json
import period, rbb, bundle

D = period.setup(6)
M, S = D['M'], D['S']
k = json.load(open('logs/scip_repro_mult.json'))
lam = [[float(v) for v in l] for l in k['lam']]
mu = float(k['mu'])
for t, lowest in ((0, 168.108652), (4, -6.730984), (5, -232.172990)):
    W = rbb.Window(D, t, t + 1)
    c = W.objective(lam, mu)
    obbt = sorted({a for kind, args in W.auxdef for a in args if not W.isbin[a]})
    res = rbb.solve(W, c, lowest - 1e-3, node_limit=200000, time_limit=1200, obbt_vars=obbt)
    print(f"period {t}: rbb certified phi >= {res['bound']:.6f} (target {lowest - 1e-3:.6f}, {res['status']}, "
          f"{res['nodes']} nodes, {res['time']:.0f}s)", flush=True)
    objc = period.window_objective(D, t, t + 1, lam, mu)
    for name, prm in (('default', {}), ('noprop', dict(bundle.NOPROP))):
        r = period.solve_window(D, t, t + 1, lam, mu, 300, prm)
        m, X = period.build(D, t, t + 1, objc, {'numerics/feastol': 1e-9})
        for v in S['per_vars'][t]:
            if M['vt'][v] == 'B':
                m.fixVar(X[v], round(r['x'][v]))
        m.setParam('limits/time', 300)
        m.optimize()
        print(f"   {name} configuration re-solved at feastol 1e-9: {m.getStatus()} {m.getPrimalbound():.6f}", flush=True)
        m.freeProb()
