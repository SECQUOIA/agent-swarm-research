import sys, time, numpy as np
from pyscipopt import Model, quicksum
def solve(n, seed, alpha=1.0, b=0.8, kappa=0.0, tl=600, bestfirst=False):
    rng = np.random.default_rng(seed)
    c = rng.uniform(-0.3,0.3,n)
    m = Model(); m.hideOutput()
    x = [m.addVar(lb=-1, ub=1, name=f"x{i}") for i in range(n)]
    ts = []
    for i in range(n-1):
        ti = m.addVar(lb=None, name=f"t{i}")
        m.addCons(ti >= alpha*x[i]*x[i] + b*x[i]*x[i+1] - kappa*x[i]**4)
        ts.append(ti)
    tl_ = m.addVar(lb=None); m.addCons(tl_ >= alpha*x[n-1]*x[n-1] - kappa*x[n-1]**4); ts.append(tl_)
    m.setObjective(quicksum(ts) + quicksum(c[i]*x[i] for i in range(n)), "minimize")
    m.setParam("limits/time", tl)
    if bestfirst: m.setParam("nodeselection/bfs/stdpriority", 10**6)
    t0=time.time(); m.optimize()
    return m.getNNodes(), m.getStatus(), round(time.time()-t0,2), m.getObjVal(), m.getDualbound()
kappa=float(sys.argv[1])
for n in [int(a) for a in sys.argv[2:]]:
    for s in range(2):
        print(n, s, *solve(n, s, kappa=kappa), flush=True)
