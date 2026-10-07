import sys, time, numpy as np
from pyscipopt import Model, quicksum
def solve(n, seed, tl=300):
    rng = np.random.default_rng(seed)
    d = rng.uniform(-1,1,n); o = rng.uniform(-1,1,n-1); c = rng.uniform(-1,1,n)
    m = Model(); m.hideOutput()
    x = [m.addVar(lb=0, ub=1, name=f"x{i}") for i in range(n)]
    t = m.addVar(lb=None, name="t")
    m.addCons(t >= quicksum(d[i]*x[i]*x[i] for i in range(n)) + quicksum(o[i]*x[i]*x[i+1] for i in range(n-1)) + quicksum(c[i]*x[i] for i in range(n)))
    m.setObjective(t, "minimize")
    m.setParam("limits/time", tl)
    t0=time.time(); m.optimize()
    return m.getNNodes(), m.getStatus(), time.time()-t0, m.getObjVal()
for n in [int(a) for a in sys.argv[1:]]:
    for s in range(3):
        print(n, s, *solve(n, s), flush=True)
