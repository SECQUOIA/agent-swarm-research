#!/usr/bin/env python3
"""Reviewer: fm336 under single setting changes, PySCIPOpt 6.2.1 wheel, seeds 0-4. WRONG if optimal and dual > 187/270 + 1e-4."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import pyscipopt as ps
T = (_PUBLIC_REPO + '/research-20260929/publication/scip-bug/')
cases = [("default", {}),
         ("propagating/maxrounds=0,maxroundsroot=0", {"propagating/maxrounds": 0, "propagating/maxroundsroot": 0}),
         ("constraints/nonlinear/propfreq=-1", {"constraints/nonlinear/propfreq": -1}),
         ("constraints/nonlinear/maxproprounds=0", {"constraints/nonlinear/maxproprounds": 0}),
         ("varboundrelax=a", {"constraints/nonlinear/varboundrelax": "a"}),
         ("varboundrelax=b", {"constraints/nonlinear/varboundrelax": "b"}),
         ("varboundrelax=n", {"constraints/nonlinear/varboundrelax": "n"}),
         ("varboundrelaxamount=1e-6", {"constraints/nonlinear/varboundrelaxamount": 1e-6}),
         ("conssiderelaxamount=1e-6", {"constraints/nonlinear/conssiderelaxamount": 1e-6}),
         ("propauxvars=FALSE", {"constraints/nonlinear/propauxvars": False}),
         ("propagating/redcost/freq=-1", {"propagating/redcost/freq": -1}),
         ("numerics/feastol=1e-9", {"numerics/feastol": 1e-9}),
         ("numerics/epsilon=1e-12", {"numerics/epsilon": 1e-12}),
         ("conflict/enable=FALSE", {"conflict/enable": False})]
for name, prm in cases:
    out = []
    for seed in range(5):
        m = ps.Model(); m.hideOutput(); m.readProblem(T + "min/fm336_v1010.cip")
        m.setParam("randomization/randomseedshift", seed)
        for k, v in prm.items():
            m.setParam(k, v)
        m.optimize()
        st, db = m.getStatus(), m.getDualbound()
        out.append((st, db, st == "optimal" and db > 187/270 + 1e-4))
    print("%-42s wrong %d/5  claims %s" % (name, sum(o[2] for o in out), sorted(set("%s %.6g" % (o[0], o[1]) for o in out))))
