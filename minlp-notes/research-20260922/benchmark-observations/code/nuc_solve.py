"""Run Gurobi or SCIP on a nuclear* instance, with or without the cuts of nuc_cuts.py.
usage: nuc_solve.py name solver(gurobi|scip) cuts(0|1) tlim"""
import sys, os, json, time
from osil_eval import Model, FloatB
from nuc_cuts import add_cuts

name, solver, cuts, tlim = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
path = os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil")
M = Model(path)
B = {r["name"]: r for r in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../nuclear_cw_bounds.json")))}[name]
KF, lamb = B["KF"], B["best_bound"]
lamT = list(M.objlin)[0]
out = {"name": name, "solver": solver, "cuts": cuts, "tlim": tlim}
t0 = time.time()
if solver == "gurobi":
    import gurobipy as gp
    from grb_build import build
    g, x = build(M)
    if cuts:
        def addlin(coefs, sense, rhs):
            it = coefs.items(); e = gp.LinExpr([c for _, c in it], [v for v, _ in it])
            g.addLConstr(e, {"<=": "<", ">=": ">", "==": "="}[sense], rhs)
        def newv(n, lb, ub):
            v = g.addVar(lb=lb, ub=gp.GRB.INFINITY if ub is None else ub, name=n); g.update(); return v
        out["ncuts"], out["nsteps"] = add_cuts(M, x, addlin, KF, lamb, newv)
        g.addLConstr(x[lamT], "<", lamb * (1 + 1e-9))
    g.Params.TimeLimit = tlim; g.Params.Threads = 1
    g.optimize()
    out.update(status=g.Status, time=g.Runtime, primal=g.ObjVal if g.SolCount else None, dual=g.ObjBound, nodes=g.NodeCount)
    xv = [v.X for v in x] if g.SolCount else None
else:
    import pyscipopt
    S = pyscipopt.Model(); S.readProblem(path)
    vmap = {v.name: v for v in S.getVars()}
    x = [vmap[n] for n in M.vnames]
    if cuts:
        def addlin(coefs, sense, rhs):
            e = pyscipopt.quicksum(c * v for v, c in coefs.items())
            S.addCons(e <= rhs if sense == "<=" else (e >= rhs if sense == ">=" else e == rhs))
        newv = lambda n, lb, ub: S.addVar(name=n, lb=lb, ub=ub)
        out["ncuts"], out["nsteps"] = add_cuts(M, x, addlin, KF, lamb, newv)
        S.addCons(x[lamT] <= lamb * (1 + 1e-9))
    S.setParam("limits/time", tlim); S.setParam("parallel/maxnthreads", 1)
    S.optimize()
    out.update(status=S.getStatus(), time=S.getSolvingTime(), primal=S.getPrimalbound() if S.getNSols() else None,
               dual=S.getDualbound(), nodes=S.getNNodes())
    xv = [S.getSolVal(S.getBestSol(), v) for v in x] if S.getNSols() else None
out["wall"] = time.time() - t0
if xv is not None:
    c = M.check(xv, FloatB)
    out.update(obj_eval=M.objective(xv, FloatB), max_bound_viol=c["bound"][0], max_row_viol=c["row"][0], max_int_viol=c["int"][0])
os.makedirs("../nuclear_runs", exist_ok=True)
json.dump(out, open(f"../nuclear_runs/{name}_{solver}_{cuts}.json", "w"), indent=1)
print(json.dumps(out))
