"""Build a gurobipy model from an OSiL instance with only linear/quadratic rows (no <nl> expressions)."""
import gurobipy as gp
from osil_eval import Model

INF = gp.GRB.INFINITY


def build(M: Model, env=None):
    assert not M.nl, "general nonlinear rows not supported"
    g = gp.Model(M.name, env=env) if env else gp.Model(M.name)
    val = lambda s, d: d if s in ("INF", "-INF") else float(s)
    x = [g.addVar(lb=val(M.vlb[j], -INF), ub=val(M.vub[j], INF),
                  vtype={"B": "B", "I": "I"}.get(M.vtype[j], "C"), name=M.vnames[j]) for j in range(M.n)]

    def expr(r):
        lin = M.objlin if r == -1 else M.lin[r]
        if not M.quad.get(r):
            e = gp.LinExpr([float(c) for c in lin.values()], [x[j] for j in lin])
            e.addConstant(float(M.objconst if r == -1 else M.cconst[r]))
            return e
        e = gp.QuadExpr()
        for j, c in lin.items(): e.add(x[j], float(c))
        for i, j, c in M.quad.get(r, []): e.add(x[i] * x[j], float(c))
        e.addConstant(float(M.objconst if r == -1 else M.cconst[r]))
        return e
    for r in range(M.m):
        e, lb, ub = expr(r), M.clb[r], M.cub[r]
        q = bool(M.quad.get(r))
        add = g.addQConstr if q else g.addLConstr
        if lb == ub:
            add(e == float(lb), name=M.cnames[r])
        else:
            if lb != "-INF": add(e >= float(lb), name=M.cnames[r] + "_lo")
            if ub != "INF": add(e <= float(ub), name=M.cnames[r] + "_up")
    g.setObjective(expr(-1), gp.GRB.MINIMIZE if M.objsense == "min" else gp.GRB.MAXIMIZE)
    g.Params.NonConvex = 2
    return g, x
