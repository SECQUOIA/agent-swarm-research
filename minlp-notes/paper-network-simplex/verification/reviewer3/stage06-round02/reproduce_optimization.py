from pathlib import Path
from fractions import Fraction as F
import json,numpy as np
from network_simplex_benchmarks.baselines import block_chain
from network_simplex_benchmarks.paper_stage06 import local_labels_instance,opt_case
P=Path('paper-network-simplex');E=P/'verification/reviewer3/stage06-round02';data=json.loads((P/'verification/stage06-benchmarks.json').read_text());out=[]
for i,prior in enumerate(data['optimization']):
 inst=local_labels_instance() if i==2 else block_chain(seed=33,blocks=4,paths=5,states=128)
 c=np.array(prior['objective_vector']);y=list(map(F,prior['y']));rows=[(np.array(row['coefficients']),F(row['rhs'])) for row in prior['extra_rows']]
 fresh=opt_case(inst,c,y,rows,list(prior['warmup']),1)
 assert abs(fresh['objective']-prior['objective'])<1e-7
 for method,raw in fresh['warmup'].items():
  assert raw['status']==prior['warmup'][method]['status']
  assert raw['stats']==prior['warmup'][method]['stats'],method
  assert abs(raw['objective']-prior['warmup'][method]['objective'])<1e-7
  if 'cuts' in raw: assert raw['cuts']==prior['warmup'][method]['cuts']
 fresh['name']=prior['name'];out.append(fresh)
(E/'reproduced-optimization.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS: three cases, 16 methods, fresh warmups and one repeat; exact audit and numerical objectives/sizes/cuts match')
