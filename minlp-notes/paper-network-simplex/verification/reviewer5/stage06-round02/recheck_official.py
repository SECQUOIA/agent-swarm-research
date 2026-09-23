from pathlib import Path
from fractions import Fraction as F
import json
import numpy as np
from network_simplex_benchmarks.baselines import block_chain
from network_simplex_benchmarks.paper_stage06 import local_labels_instance,opt_case
raw=json.loads(Path('paper-network-simplex/verification/stage06-benchmarks.json').read_text())
results=[]
for prior in raw['optimization']:
 instance=local_labels_instance() if 'all_labels' in prior['name'] else block_chain(seed=33,blocks=4,paths=5,states=128)
 rows=[(np.asarray(row['coefficients']),F(row['rhs'])) for row in prior['extra_rows']]
 result=opt_case(instance,np.asarray(prior['objective_vector']),list(map(F,prior['y'])),rows,list(prior['warmup']),1)
 assert abs(result['objective']-prior['objective'])<1e-7
 for method in prior['warmup']:
  assert result['warmup'][method]['stats']==prior['warmup'][method]['stats'],method
  assert abs(result['warmup'][method]['objective']-prior['objective'])<1e-7
 result['name']=prior['name'];results.append(result)
print(json.dumps(dict(status='PASS',cases=results),indent=2))
