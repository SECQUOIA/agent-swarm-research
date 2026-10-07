"""SCIP on multi-period windows at given multipliers (exploratory; SCIP values are not certified)."""
import sys, json
import period, bundle

D = period.setup(int(sys.argv[2]))
k = json.load(open(sys.argv[1]))
lam, mu = k['lam'], k['mu']
wins = [tuple(map(int, w.split('-'))) for w in sys.argv[3].split(',')]
tl = float(sys.argv[4])
prm = bundle.NOPROP if (len(sys.argv) > 5 and sys.argv[5] == 'noprop') else {}
for a, b in wins:
    r = period.solve_window(D, a, b, lam, mu, tl, prm)
    print(a, b, r['status'], 'dual', r['dual'], 'primal', r['primal'], 'time', round(r['time'], 1), 'nodes', r['nodes'], flush=True)
print('period values at these multipliers:', k['best']['vals'], 'mu*c', mu * float(D['hor_rhs']))
