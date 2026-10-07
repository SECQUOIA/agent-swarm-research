"""Re-solve a period subproblem with SCIP at tight feasibility tolerance (1e-9)
and binaries fixed to the default solve's configuration; compare with rbb bound."""
import sys, json
import period, bundle
T = int(sys.argv[1]); t = int(sys.argv[2])
D = period.setup(T)
k = json.load(open(sys.argv[3]))
lam, mu = k['lam'], k['mu']
M, S = D['M'], D['S']
r = period.solve_window(D, t, t + 1, lam, mu, 120, bundle.NOPROP)
print('noprop 1e-6:', r['primal'], r['dual'])
objc = period.window_objective(D, t, t + 1, lam, mu)
for ft in (1e-8, 1e-9):
    m, X = period.build(D, t, t + 1, objc, {'numerics/feastol': ft, 'propagating/maxrounds': 0, 'propagating/maxroundsroot': 0})
    for v in S['per_vars'][t]:
        if M['vt'][v] == 'B':
            m.fixVar(X[v], round(r['x'][v]))
    m.setParam('limits/time', 120)
    m.optimize()
    print('feastol', ft, 'fixed config', m.getStatus(), m.getPrimalbound(), m.getDualbound())
    m.freeProb()
