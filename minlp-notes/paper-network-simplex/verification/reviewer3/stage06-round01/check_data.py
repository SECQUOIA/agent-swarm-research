import json,hashlib,statistics
from pathlib import Path
R=Path.cwd(); D=R/'paper-network-simplex'; E=D/'verification/reviewer3/stage06-round01'; S=D/'process/snapshots/stage06-round01'
v=json.loads((D/'verification/stage06-validation.json').read_text()); bad=[]
for name,digest in v['sha256'].items():
 p=R/name
 if hashlib.sha256(p.read_bytes()).hexdigest()!=digest: bad.append(name)
assert not bad,bad
b=json.loads((D/'verification/stage06-benchmarks.json').read_text()); count=0; fields=0
assert {(x['gadgets'],x['weights'],x['feasible']) for x in b['flat']}=={(L,w,f) for L in (8,32,128,512) for w in ('boundary','interior') for f in (True,False)}
assert {x['states'] for x in b['membership']}=={16,128,1024}
assert len({x['name'] for x in b['optimization']})==3
for case in b['flat']+b['membership']+b['optimization']:
 methods=list(case['warmup'])
 assert len(case['runs'])==5
 for r,run in enumerate(case['runs']):
  assert run['order']==methods[r%len(methods):]+methods[:r%len(methods)]
  assert set(run['measurements'])==set(methods)
  for method,raw in run['measurements'].items():
   count+=1
   assert raw['status']==(0 if case.get('feasible',True) else 2)
   assert raw['total_seconds']>=raw['build_seconds']+raw['solve_seconds']-1e-9
   if 'objective' in case: assert abs(raw['objective']-case['objective'])<1e-7
   if 'stats' in raw and method!='cuts': assert raw['stats']==case['warmup'][method]['stats']
 for method in methods:
  rawfields={k for k in case['warmup'][method] if k.endswith('_seconds')}
  assert rawfields==set(case['summary'][method])
  for key in rawfields:
   a=[run['measurements'][method][key] for run in case['runs']]
   assert case['summary'][method][key]==dict(minimum=min(a),median=statistics.median(a),maximum=max(a)); fields+=1
for path in (S/'tables').glob('*.tex'):
 assert path.read_bytes()==(E/'build/tables'/path.name).read_bytes(),path
for case in b['optimization']:
 Ecount,m,o=case['edges'],case['states'],case['observations']; a=case['observed_labels']
 assert case['warmup']['full']['stats']['variables']==m+(m+1)*Ecount
 assert case['warmup']['global']['stats']['variables']==m+(a+1)*Ecount
for case in b['flat']:
 L=case['gadgets']; q=3 if case['weights']=='interior' else 2
 assert case['warmup']['full']['stats']['variables']==q*(2*L+1)
 if q==2:
  assert case['warmup']['two_state']['stats']['variables']==2*L+1
budget=b['optimization'][1]
assert len(budget['extra_rows'])==1
from fractions import Fraction as F
assert F(budget['reference_resource'])<F(budget['extra_rows'][0]['rhs'])<F(budget['unconstrained_resource'])
out={'hashes':len(v['sha256']),'timed_method_runs':count,'summary_fields':fields,'tables_regenerated_identically':5,'grid_status_objective_order_size_checks':'PASS'}
(E/'data-checks.json').write_text(json.dumps(out,indent=2)+'\n'); print(out)
