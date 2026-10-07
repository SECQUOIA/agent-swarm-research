from pathlib import Path as _CleanupPath

import sys, pyscipopt as ps
name, tl = sys.argv[1], float(sys.argv[2])
m = ps.Model(); m.hideOutput()
m.readProblem(f"{_CleanupPath.home()}/.cache/minlplib/minlplib/osil/{name}.osil")
m.setParam("limits/time", tl); m.setParam("parallel/maxnthreads",1)
m.optimize()
print(name, m.getStatus(), "primal", m.getPrimalbound(), "dual", m.getDualbound(), "nodes", m.getNNodes(), "time", m.getSolvingTime(), flush=True)
