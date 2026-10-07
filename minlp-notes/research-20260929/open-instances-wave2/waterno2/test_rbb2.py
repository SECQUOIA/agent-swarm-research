"""Check the vectorized rbb: certify phi_t >= (SCIP value - 1e-3) and also try
to certify an impossible target (SCIP value + 0.05), which must fail."""
import sys, json, time
import numpy as np
import period, rbb, bundle

T = int(sys.argv[1])
D = period.setup(T)
k = json.load(open(sys.argv[2]))
lam, mu = k['lam'], k['mu']
for w in [int(a) for a in sys.argv[3].split(',')]:
    W = rbb.Window(D, w, w + 1)
    c = W.objective(lam, mu)
    r = period.solve_window(D, w, w + 1, lam, mu, 120, bundle.NOPROP)
    for off in (-1e-3, +0.05):
        res = rbb.solve(W, c, r['primal'] + off, node_limit=int(sys.argv[4]), time_limit=float(sys.argv[5]))
        print(w, 'SCIP primal', r['primal'], 'target', r['primal'] + off, 'rbb', {kk: res[kk] for kk in ('bound', 'nodes', 'status', 'time')}, flush=True)
