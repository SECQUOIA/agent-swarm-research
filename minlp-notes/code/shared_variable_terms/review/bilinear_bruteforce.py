"""Task 6: is the 6n-variable state form exact for equal widths?  Compare, for random linear objectives in (x,y,t),
the LP value of the state form (EF) with the TRUE minimum over {x in row polytope, y in [0,1]^n, t_i = x_i y_i}
solved as a nonconvex QCP by Gurobi (global, gap 1e-9), not with proto.py's vertex enumeration."""
import sys, itertools
import numpy as np, gurobipy as gp
rng = np.random.default_rng(1)

def true_min(n, k, w, r, cx, cy, ct):
    m = gp.Model(); m.Params.OutputFlag = 0; m.Params.NonConvex = 2; m.Params.MIPGap = 1e-9; m.Params.Threads = 1
    x = m.addVars(n, lb=0, ub=w); y = m.addVars(n, lb=0, ub=1); t = m.addVars(n, lb=-gp.GRB.INFINITY)
    m.addConstr(x.sum() == k * w + r)
    for i in range(n): m.addConstr(t[i] == x[i] * y[i])
    m.setObjective(gp.quicksum(cx[i] * x[i] + cy[i] * y[i] + ct[i] * t[i] for i in range(n)))
    m.optimize(); assert m.Status == 2; return m.ObjVal

def ef(n, k, w, r, cx, cy, ct):
    m = gp.Model(); m.Params.OutputFlag = 0; m.Params.Threads = 1
    x = m.addVars(n, lb=0, ub=w); y = m.addVars(n, lb=0, ub=1); t = m.addVars(n, lb=0, ub=w)
    s = m.addVars(n, 6, lb=0)
    for i in range(n):
        m.addConstr(gp.quicksum(s[i, q] for q in range(6)) == 1)
        m.addConstr(x[i] == w * (s[i, 2] + s[i, 3]) + r * (s[i, 4] + s[i, 5]))
        m.addConstr(y[i] == s[i, 1] + s[i, 3] + s[i, 5])
        m.addConstr(t[i] == w * s[i, 3] + r * s[i, 5])
    m.addConstr(gp.quicksum(s[i, 2] + s[i, 3] for i in range(n)) == k)
    m.addConstr(gp.quicksum(s[i, 4] + s[i, 5] for i in range(n)) == 1)
    m.setObjective(gp.quicksum(cx[i] * x[i] + cy[i] * y[i] + ct[i] * t[i] for i in range(n)))
    m.optimize(); assert m.Status == 2; return m.ObjVal

worst = 0.0; cnt = 0
for trial in range(60):
    n = int(rng.integers(2, 6)); k = int(rng.integers(1, n)); w = float(rng.uniform(0.5, 2.0)); r = float(rng.uniform(0.05, 0.95)) * w
    cx, cy, ct = rng.normal(size=n), rng.normal(size=n), rng.normal(size=n) * 3
    a, b = true_min(n, k, w, r, cx, cy, ct), ef(n, k, w, r, cx, cy, ct)
    worst = max(worst, abs(a - b)); cnt += 1
    if trial < 5: print(f"n={n} k={k} w={w:.2f} r={r:.2f} true {a:.6f} EF {b:.6f}")
print("trials", cnt, "max |true - EF|", worst)
