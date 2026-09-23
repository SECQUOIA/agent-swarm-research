"""Node counts with the *closed-form* row inequality (Proposition 3 with residual intervals from the
subset-sum program) recomputed on every node box: mode C.  Compare with bb.py modes T, R, L."""
import sys
import numpy as np
import gurobipy as gp
from gurobipy import GRB

import bb
from rowhull.closedform import closed_form_rows


def solve_node_cf(p, node, mode, max_rounds=30):
    if mode != "C":
        return _orig(p, node, mode, max_rounds)
    n = p.n
    m = gp.Model(); m.Params.OutputFlag = 0
    x = [m.addVar(lb=node.lo[i], ub=node.hi[i]) for i in range(n)]
    w = [m.addVar(lb=-GRB.INFINITY, obj=1.0) for _ in range(n)]
    v = {**{f"x{i}": x[i] for i in range(n)}, **{f"w{i}": w[i] for i in range(n)}}
    for i, f in enumerate(p.funcs):
        a, b = node.lo[i], node.hi[i]
        if b - a > 1e-12:
            m.addConstr(w[i] >= f(a) + (f(b) - f(a)) / (b - a) * (x[i] - a))
        else:
            m.addConstr(w[i] >= f(a))
    for r in range(p.A.shape[0]):
        m.addConstr(gp.quicksum(p.A[r, i] * x[i] for i in range(n) if p.A[r, i] != 0.0) == p.b[r])
    for q, row in enumerate(bb.node_rows(p, node.lo, node.hi)):
        out = closed_form_rows(row, f"r{q}", 2000)
        if out is None:
            continue
        for k, (lb, ub, _t) in out[0].items():
            v[k] = m.addVar(lb=lb, ub=ub)
        m.update()
        for rowd, sn, rhs in out[1]:
            lhs = gp.quicksum(c * v[k] for k, c in rowd.items())
            m.addConstr(lhs <= rhs if sn == "<=" else lhs >= rhs if sn == ">=" else lhs == rhs)
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        return None, None, []
    return m.ObjVal, np.array([xi.X for xi in x]), []


_orig = bb.solve_node
bb.solve_node = solve_node_cf

if __name__ == "__main__":
    from instances import transport
    mm, nn, cap, cost, seeds = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5])
    for seed in range(seeds):
        p = transport(mm, nn, seed, cap, cost)
        # root of mode C is the closed form as well
        o = bb.bb(p, "C")
        print(p.name, f"C: nodes {o['nodes']} root {o['root']:.4f} ub {o['ub']:.4f} {'done' if o['done'] else 'LIMIT'} {o['time']:.0f}s", flush=True)
