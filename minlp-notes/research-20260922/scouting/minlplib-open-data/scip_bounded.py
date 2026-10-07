from pathlib import Path as _CleanupPath

import sys, pyscipopt as ps, json
n=sys.argv[1]; lo=float(sys.argv[2]); hi=float(sys.argv[3]); tl=float(sys.argv[4])
m=ps.Model(); m.hideOutput()
m.readProblem((str(_CleanupPath.home()) + '/.cache/minlplib/minlplib/osil/')+n+'.osil')
cnt=0
for v in m.getVars():
    if v.getLbGlobal()<-1e19: m.chgVarLb(v,lo); cnt+=1
    if v.getUbGlobal()>1e19: m.chgVarUb(v,hi); cnt+=1
m.setParam('limits/time',tl); m.optimize()
print(json.dumps(dict(name=n,box=[lo,hi],changed=cnt,status=m.getStatus(),dual=m.getDualbound(),primal=m.getPrimalbound())))
