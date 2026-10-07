from pathlib import Path as _CleanupPath

import sys, pyscipopt as ps, json
n=sys.argv[1]; tl=float(sys.argv[2])
m=ps.Model(); m.hideOutput()
m.readProblem((str(_CleanupPath.home()) + '/.cache/minlplib/minlplib/osil/')+n+'.osil')
m.setParam('limits/time',tl); m.setParam('parallel/maxnthreads',1)
m.optimize()
print(json.dumps(dict(name=n,status=m.getStatus(),dual=m.getDualbound(),primal=m.getPrimalbound(),nodes=m.getNNodes())))
