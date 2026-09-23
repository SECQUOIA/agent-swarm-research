"""Reformulated lower-bound family in Gurobi with modelling variants: base (x substituted), x (explicit x_i),
g (objective through defined variables), gp (padded bounds), xgp.  Usage: explicit_x_check.py <n> <variant>"""
import sys, time
import gurobipy as gp
n=int(sys.argv[1]); var=sys.argv[2]; k=n//3
m=gp.Model(); m.Params.OutputFlag=0; m.Params.TimeLimit=20; m.Params.Threads=4; m.Params.NonConvex=2; m.Params.MIPGap=1e-4
u=m.addVars(n,vtype="B"); t_=m.addVars(n,vtype="B"); s=m.addVars(n,lb=0,ub=1)
m.addConstrs(s[i]<=t_[i] for i in range(n)); m.addConstrs(u[i]+t_[i]<=1 for i in range(n))
m.addConstr(t_.sum()<=1)
if "x" in var:
    x=m.addVars(n,lb=0,ub=1); m.addConstrs(x[i]==u[i]+s[i] for i in range(n)); m.addConstr(x.sum()==k+0.5)
else:
    m.addConstr(u.sum()+s.sum()==k+0.5)
if "g" in var:
    lo=-0.0125 if "p" in var else 0.0
    g=m.addVars(n,lb=lo,ub=0.2625); m.addConstrs(g[i]==s[i]-s[i]*s[i] for i in range(n)); m.setObjective(g.sum())
else:
    m.setObjective(gp.quicksum(s[i]*(1-s[i]) for i in range(n)))
t=time.time(); m.optimize()
print(f"{var} n={n} status={m.Status} bound={m.ObjBound:.4f} nodes={m.NodeCount:.0f} t={time.time()-t:.1f}")
