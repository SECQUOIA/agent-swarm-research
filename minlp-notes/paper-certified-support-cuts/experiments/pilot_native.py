import sys, time
from pyscipopt import Model
def build(n, couple=True):
    m = Model(); m.hideOutput(True)
    ys=[]; ts=[]
    for i in range(n):
        x = m.addVar(f"x{i}", lb=0, ub=1); y = m.addVar(f"y{i}", lb=0, ub=1); z = m.addVar(f"z{i}", lb=0, ub=1)
        t = m.addVar(f"t{i}", lb=-10, ub=10)
        D = 1.25*x - 0.5*y + 1.0*z - 0.75*x*x + 2.0*y*y - 0.609375*z*z - 1.0*x*y - 1.25*y*z + 0.0625
        m.addCons(t >= D); ys.append(y); ts.append(t)
    if couple: m.addCons(sum(ys) <= 0.9*n)
    m.setObjective(sum(ts), "minimize")
    m.setParam("parallel/maxnthreads", 1); m.setParam("limits/time", 120); m.setParam("limits/gap", 1e-4)
    return m
for n in [int(a) for a in sys.argv[1:]]:
    m = build(n); t0=time.time(); m.optimize()
    print(n, m.getStatus(), "nodes", m.getNNodes(), "time %.2f"%(time.time()-t0), "dual %.6f"%m.getDualbound(), "primal %.6f"%m.getPrimalbound(), "opt", n/128, "rootdual %.6f"%m.getDualboundRoot(), flush=True)
