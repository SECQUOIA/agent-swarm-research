"""SCIP 10 (pyscipopt) on the cached OSIL model with the inputs fixed at SCIP 9.0.1's
reported optimal point (Zenodo 14961066, Default).  With exact arithmetic all other
variables are then determined (objective 0.0028684784 for n4, -0.0108512435 for n5),
so any lower value SCIP returns comes from its feasibility tolerances."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])
_PUBLIC_HOME = str(_PublicPath.home())

import sys
from pyscipopt import Model
OSIL = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/%s.osil')
CASES = {"kan_r3_h1_n4": ("x1075", "x1077", "x1079", 0.99064970236898897, 0.98118960678561296, 0.96330313134142198),
         "kan_r3_h1_n5": ("x1343", "x1345", "x1347", 0.99412127037819098, 0.98885022716926496, 0.97685176822519004)}
name = sys.argv[1]
c = CASES[name]
m = Model()
m.readProblem(OSIL % name)
vs = {v.name: v for v in m.getVars()}
for k in range(3):
    m.fixVar(vs[c[k]], c[3 + k])
m.setParam("limits/time", 300)
m.setParam("parallel/maxnthreads", 1)
m.setParam("display/verblevel", 2)
m.optimize()
print(name, "status", m.getStatus(), "primal", repr(m.getPrimalbound()), "dual", repr(m.getDualbound()))

# evaluate SCIP's solution on the OSIL rows with the reviewer's evaluator
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/publication/reviews/lit-network-r1'))
import mpmath as mp
import osil_eval as oe
V, obj, C = oe.read(OSIL % name)
sol = m.getBestSol()
x = [mp.mpf(repr(m.getSolVal(sol, vs[v["name"]]))) for v in V]
viols = sorted(((oe.viol(r, oe.body(r, x)), r["name"]) for r in C), reverse=True)
print(name, "SCIP solution: objective (OSIL)", mp.nstr(obj["const"] + mp.fsum(a * x[j] for j, a in obj["lin"].items()), 12),
      "; largest absolute row violations:", [(mp.nstr(v, 3), n) for v, n in viols[:5]],
      "; rows violated by more than 1e-9:", sum(1 for v, n in viols if v > 1e-9))
