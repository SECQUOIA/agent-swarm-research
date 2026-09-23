"""Reproduce the fixed-weight empty-network regression; does not modify code."""
from fractions import Fraction as F
import importlib.util,json,sys
from pathlib import Path
import numpy as np
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import optimize_ef
path=Path('paper-network-simplex/verification/stage06-corrections/round1-archive/code/network_simplex_benchmarks/strong_baselines.py')
name='network_simplex_benchmarks._reviewer2_round1'
spec=importlib.util.spec_from_file_location(name,path); old=importlib.util.module_from_spec(spec);sys.modules[name]=old;spec.loader.exec_module(old)
instance=Instance([],np.array([0.]),2,[],np.array([]))
records=[]
for merge in [False,True]:
    previous=old.optimize_ef(instance,[2.,3.],[F(1,3),F(1,4)],merge=merge)
    assert previous.status==0 and abs(previous.fun-float(F(17,12)))<1e-12
    try:
        current=optimize_ef(instance,[2.,3.],[F(1,3),F(1,4)],merge=merge)
        outcome={'status':current.status,'objective':current.fun}
    except ValueError as error:outcome={'exception':type(error).__name__,'message':str(error)}
    records.append({'merge':merge,'expected_status':0,'expected_objective':'17/12','archived_status':previous.status,'archived_objective':previous.fun,'corrected_builder':outcome})
Path(__file__).with_name('empty-network-result.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records))
