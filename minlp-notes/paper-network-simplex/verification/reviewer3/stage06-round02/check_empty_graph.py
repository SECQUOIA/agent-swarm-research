from fractions import Fraction as F
from pathlib import Path
import importlib.util,json,sys,numpy as np
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import optimize_ef
archive=Path('paper-network-simplex/verification/stage06-corrections/round1-archive/code/network_simplex_benchmarks/strong_baselines.py')
name='network_simplex_benchmarks._reviewer3_round1';spec=importlib.util.spec_from_file_location(name,archive);old=importlib.util.module_from_spec(spec);sys.modules[name]=old;spec.loader.exec_module(old)
instance=Instance([],np.zeros(1),2,[],np.zeros(0));evidence=[]
for merge in (False,True):
 before=old.optimize_ef(instance,[1,2],y_fixed=[F(1,3)]*2,merge=merge)
 assert before.status==0 and abs(before.fun-1)<1e-10
 try:
  after=optimize_ef(instance,[1,2],y_fixed=[F(1,3)]*2,merge=merge)
  error=None
 except Exception as exc:error=type(exc).__name__+': '+str(exc)
 assert error is not None
 evidence.append(dict(merge=merge,old_status=int(before.status),old_objective=before.fun,old_original_point=before.original_point.tolist(),new_error=error))
Path('paper-network-simplex/verification/reviewer3/stage06-round02/empty-graph.json').write_text(json.dumps(evidence,indent=2)+'\n');print(evidence)
