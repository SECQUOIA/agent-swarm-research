"""SCIP estimate of the relaxation that dualizes only the horizon row (all
level links kept): mu*c + min over the full window.  Exploratory (SCIP)."""
import os, sys, json
import period
T = int(sys.argv[1])
D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
k = json.load(open(sys.argv[2]))
lam, mu = k['lam'], float(sys.argv[3]) if len(sys.argv) > 3 else k['mu']
r = period.solve_window(D, 0, T, lam, mu, float(sys.argv[4]) if len(sys.argv) > 4 else 600, {})
c = mu * float(D['hor_rhs'])
print(f"T={T} mu={mu:.4f}: status {r['status']} dual {r['dual'] + c:.4f} primal {r['primal'] + c:.4f} time {r['time']:.0f}s nodes {r['nodes']}")
