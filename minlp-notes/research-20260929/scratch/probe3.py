import sys, time, numpy as np
from pyscipopt import Model, quicksum
def build(n, seed, alpha=1.0, b=0.8, kappa=0.1, sep=True):
    rng = np.random.default_rng(seed)
    c = rng.uniform(-0.3,0.3,n)
    m = Model(); m.hideOutput()
    x = [m.addVar(lb=-1, ub=1, name=f"x{i}") for i in range(n)]
    ts = []
    for i in range(n):
        ti = m.addVar(lb=None, name=f"t{i}")
        expr = alpha*x[i]*x[i] - kappa*x[i]**4
        if i < n-1: expr = expr + b*x[i]*x[i+1]
        m.addCons(ti >= expr)
        ts.append(ti)
    m.setObjective(quicksum(ts) + quicksum(c[i]*x[i] for i in range(n)), "minimize")
    return m
eps=float(sys.argv[1]); kappa=float(sys.argv[2])
for n in [int(a) for a in sys.argv[3:]]:
  for s in range(2):
    m=build(n,s,kappa=kappa)
    m.setParam("limits/time", 120); m.setParam("limits/absgap", eps); m.setParam("limits/gap", 0.0)
    t0=time.time(); m.optimize()
    print(n, eps, s, m.getNNodes(), m.getStatus(), round(time.time()-t0,2), round(m.getPrimalbound(),6), round(m.getDualbound(),6), flush=True)
