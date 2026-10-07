"""Compare rbb certified bounds with SCIP on period subproblems at a multiplier vector."""
import sys, json, time
import numpy as np
import period, rbb, bundle

T = 6
D = period.setup(T)
k = json.load(open(sys.argv[1]))
lam, mu = k['lam'], k['mu']
ws = [int(a) for a in sys.argv[2].split(',')]
for w in ws:
    W = rbb.Window(D, w, w + 1)
    c = W.objective(lam, mu)
    r = period.solve_window(D, w, w + 1, lam, mu, 120, bundle.NOPROP)
    target = r['primal'] - 1e-3
    tic = time.time()
    res = rbb.solve(W, c, target, node_limit=int(sys.argv[3]), time_limit=float(sys.argv[4]), verbose=True)
    print(w, 'SCIP', r['dual'], r['primal'], 'rbb', res, flush=True)
