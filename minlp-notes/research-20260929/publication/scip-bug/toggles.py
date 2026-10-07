"""Default settings plus one change each, on a model, for seeds 0..N-1 (PySCIPOpt).
A run is WRONG if it reports 'optimal' with dual bound > witness value + 1e-4.
usage: python3 toggles.py MODEL.cip WITNESS_VALUE N"""
import sys

import run_scip

path, w, n = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
TOGGLES = [
    ("default", {}),
    ("propagating/maxrounds=0, maxroundsroot=0", {"propagating/maxrounds": 0, "propagating/maxroundsroot": 0}),
    ("constraints/nonlinear/propfreq=-1", {"constraints/nonlinear/propfreq": -1}),
    ("constraints/nonlinear/maxproprounds=0", {"constraints/nonlinear/maxproprounds": 0}),
    ("constraints/nonlinear/varboundrelax=a", {"constraints/nonlinear/varboundrelax": "a"}),
    ("constraints/nonlinear/varboundrelax=b", {"constraints/nonlinear/varboundrelax": "b"}),
    ("constraints/nonlinear/varboundrelax=n", {"constraints/nonlinear/varboundrelax": "n"}),
    ("constraints/nonlinear/varboundrelaxamount=1e-6", {"constraints/nonlinear/varboundrelaxamount": 1e-6}),
    ("constraints/nonlinear/conssiderelaxamount=1e-6", {"constraints/nonlinear/conssiderelaxamount": 1e-6}),
    ("constraints/nonlinear/propauxvars=FALSE", {"constraints/nonlinear/propauxvars": False}),
    ("propagating/obbt/freq=-1", {"propagating/obbt/freq": -1}),
    ("propagating/redcost/freq=-1", {"propagating/redcost/freq": -1}),
    ("propagating/rootredcost/freq=-1", {"propagating/rootredcost/freq": -1}),
    ("propagating/probing/maxprerounds=0, freq=-1", {"propagating/probing/maxprerounds": 0, "propagating/probing/freq": -1}),
    ("branching/relpscost/maxproprounds=0", {"branching/relpscost/maxproprounds": 0}),
    ("conflict/enable=FALSE", {"conflict/enable": False}),
    ("misc/usesymmetry=0", {"misc/usesymmetry": 0}),
    ("presolving/maxrestarts=0", {"presolving/maxrestarts": 0}),
    ("numerics/feastol=1e-9", {"numerics/feastol": 1e-9}),
    ("numerics/epsilon=1e-12", {"numerics/epsilon": 1e-12}),
]
for name, prm in TOGGLES:
    wrong, claims = 0, []
    for s in range(n):
        p = dict(prm)
        p["randomization/randomseedshift"] = s
        r = run_scip.solve(path, p)
        bad = r["status"] == "optimal" and r["dual"] > w + 1e-4
        wrong += bad
        claims.append(round(r["dual"], 4))
    print(f"{name:50s} wrong in {wrong} of {n} seeds; claimed optima {sorted(set(claims))}", flush=True)
