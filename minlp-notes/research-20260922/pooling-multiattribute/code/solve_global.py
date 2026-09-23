"""Global optimum of the pq formulation with Gurobi (NonConvex=2); prints primal and dual bounds."""
import sys, json
import gurobipy as gp
from gurobipy import GRB
import instance as I

def solve(path, tlim=600, threads=2):
    P = I.Inst(path)
    m, q, y, z, v = I.build_pq(P)
    for (i, l, j), var in v.items():
        m.addQConstr(var == q[i, l] * y[l, j])
    m.Params.NonConvex = 2; m.Params.TimeLimit = tlim; m.Params.Threads = threads; m.Params.MIPGap = 1e-6
    m.optimize()
    return dict(name=P.name, primal=m.ObjVal if m.SolCount else None, dual=m.ObjBound, status=m.Status, time=m.Runtime)

if __name__ == "__main__":
    for pth in sys.argv[1:]:
        print(json.dumps(solve(pth)), flush=True)
