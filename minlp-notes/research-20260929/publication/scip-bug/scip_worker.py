"""Solve one CIP file with PySCIPOpt and print the result as JSON (run as a
subprocess by minimize.py so that crashes and hangs are isolated).
usage: python3 scip_worker.py MODEL.cip SETTINGS_JSON [TIMELIMIT]"""
import json
import sys

import pyscipopt as ps

m = ps.Model()
m.hideOutput()
m.readProblem(sys.argv[1])
for k, v in json.loads(sys.argv[2]).items():
    m.setParam(k, v)
m.setParam("limits/time", float(sys.argv[3]) if len(sys.argv) > 3 else 60.0)
m.optimize()
print(json.dumps(dict(status=m.getStatus(), dual=m.getDualbound(),
                      primal=m.getPrimalbound() if m.getNSols() > 0 else None, nodes=m.getNNodes())))
