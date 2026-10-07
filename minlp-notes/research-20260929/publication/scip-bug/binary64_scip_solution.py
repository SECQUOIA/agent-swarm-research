"""Is SCIP's own reported optimal solution exactly feasible for the model with
all data rounded to binary64?  Evaluates every row and bound of the CIP file at
SCIP's solution (doubles, exact rationals) with double-rounded coefficients,
in exact arithmetic, and lists the binaries that are 0.
usage: python3 binary64_scip_solution.py MODEL.cip [param=value,...]"""
import sys
from fractions import Fraction as F

import pyscipopt as ps

import exact_check as ec
import run_scip

path = sys.argv[1]
m = ps.Model()
m.hideOutput()
m.readProblem(path)
for k, v in (run_scip.parse(sys.argv[2]) if len(sys.argv) > 2 else {}).items():
    m.setParam(k, v)
m.optimize()
s = m.getBestSol()
x = {v.name: F(m.getSolVal(s, v)) for v in m.getVars()}
vars_, rows = ec.parse_cip(path)
worst = (F(0), None)
for r in rows:
    lhs = ec.value([(F(float(a)), vs) for a, vs in r["terms"]], x)
    rhs = F(float(r["rhs"]))
    viol = abs(lhs - rhs) if r["op"] == "==" else max(F(0), (rhs - lhs) if r["op"] == ">=" else (lhs - rhs))
    worst = max(worst, (viol, r["name"]), key=lambda t: t[0])
bnd = max((max(F(0), (F(float(v["lb"])) - x[v["name"]]) if v["lb"] is not None else F(0),
               (x[v["name"]] - F(float(v["ub"]))) if v["ub"] is not None else F(0)), v["name"]) for v in vars_)
off = sorted(n for n, val in x.items() if n.startswith("b") and val == 0)
print(f"{path}: SCIP status {m.getStatus()} claimed {m.getDualbound()!r}; binaries at 0: {off}")
print(f"  binary64 data, exact arithmetic: max row violation {float(worst[0]):.3e} ({worst[1]}), "
      f"max bound violation {float(bnd[0]):.3e} ({bnd[1]}); exactly feasible: {worst[0] == 0 and bnd[0] == 0}")
