"""Evidence only: SCIP's own OSIL reader, all model variables fixed (bounds) at the
double-rounded point values; SCIP must report the fixed problem feasible, and its
objective is printed.  One thread, feastol 1e-9."""
import json, os, sys
from fractions import Fraction as Fr
import pyscipopt
from verify import OSIL, PTS

for name in sys.argv[1:]:
    P = json.load(open(os.path.join(PTS, name + ".json")))
    val = {v: float(Fr(d["value"])) for v, d in P["fixed"].items()}
    val.update({v: float(Fr(s)) for v, s in P["free"].items()})
    m = pyscipopt.Model()
    m.hideOutput()
    m.readProblem(os.path.join(OSIL, name + ".osil"))
    m.setParam("numerics/feastol", 1e-9)
    m.setParam("lp/threads", 1)
    m.setParam("parallel/maxnthreads", 1)
    m.setParam("limits/time", 120)
    n = 0
    for v in m.getVars():
        if v.name in val:
            m.chgVarLb(v, val[v.name]); m.chgVarUb(v, val[v.name]); n += 1
    m.optimize()
    print(f"{name}: fixed {n} of {len(m.getVars())} SCIP variables; status {m.getStatus()}; "
          f"obj {m.getObjVal() if m.getNSols() else None!r}")
