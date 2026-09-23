"""Solve an OSiL instance with SCIP (via PySCIPOpt's OSiL reader) and verify the incumbent
with the independent evaluator in osil_eval.py (float and 50-digit mpmath)."""
import sys, os, json, time
import pyscipopt
from osil_eval import Model, FloatB, mp_backend

name = sys.argv[1]; tlim = float(sys.argv[2]) if len(sys.argv) > 2 else 300
feastol = float(sys.argv[3]) if len(sys.argv) > 3 else None
tag = f"_ft{sys.argv[3]}" if feastol else ""
path = os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil")
S = pyscipopt.Model()
S.readProblem(path)
S.setParam("limits/time", tlim)
S.setParam("parallel/maxnthreads", 1)
if feastol:
    S.setParam("numerics/feastol", feastol)
t0 = time.time(); S.optimize(); wall = time.time() - t0
st = S.getStatus()
out = {"name": name, "feastol": feastol, "scip": pyscipopt.__version__, "status": st, "time": wall,
       "primal": S.getPrimalbound(), "dual": S.getDualbound(), "gap": S.getGap(), "nodes": S.getNNodes()}
M = Model(path)
if S.getNSols() > 0:
    sol = S.getBestSol()
    vals = {v.name: S.getSolVal(sol, v) for v in S.getVars()}
    x = [vals[n] for n in M.vnames]
    for bk, B in [("float", FloatB), ("mp50", mp_backend(50))]:
        xx = [B.num(repr(float(v))) for v in x]
        c = M.check(xx, B)
        out[bk] = {"obj": float(M.objective(xx, B)), "max_bound_viol": float(c["bound"][0]),
                    "max_row_viol": float(c["row"][0]), "row": c["row"][1],
                    "max_int_viol": c["int"][0]}
    json.dump({"x": dict(zip(M.vnames, x))}, open(f"../{name}_scip{tag}_sol.json", "w"))
print(json.dumps(out, indent=1))
json.dump(out, open(f"../{name}_scip{tag}.json", "w"), indent=1)
