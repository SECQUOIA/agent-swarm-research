from pathlib import Path
from statistics import median
from fractions import Fraction as F
import json, hashlib
root=Path(__file__).resolve().parents[1]
source=root/'stage1-round1/paper-network-simplex/verification/stage06-benchmarks.json'
d=json.loads(source.read_text())
report={'data_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'optimization':[]}
for case in d['optimization']:
    results={}
    for method in case['warmup']:
        raw=[run['measurements'][method]['total_seconds'] for run in case['runs']]
        assert len(raw)==5
        assert case['summary'][method]['total_seconds']==dict(minimum=min(raw),median=median(raw),maximum=max(raw))
        size={run['measurements'][method]['stats']['variables'] for run in case['runs']}
        assert len(size)==1
        assert all(run['measurements'][method]['status']==0 for run in case['runs'])
        results[method]={'variables':size.pop(),'total_ms_median':1000*median(raw)}
    report['optimization'].append({'name':case['name'],'results':results})
# A rank-one block with an observed first label and an absent second label.
# Two parallel s->t arcs, capacity 1, unit s->t flow, weights (1/3,1/3,1/3).
# Every member below has the same original x,y,z but a different unobserved
# label-2 product; observed-complement cycle rank for label 1 is zero.
x=(F(1,2),F(1,2)); fixed_observation=F(1,6)
completions=[]
for t in [F(0),F(1,6),F(1,3)]:
    flows=[(F(1,3)-t,t),(F(1,6),F(1,6)),(t,F(1,3)-t)]
    assert all(sum(f)==F(1,3) and all(0<=a<=F(1,3) for a in f) for f in flows)
    assert tuple(sum(f[e] for f in flows) for e in range(2))==x
    assert flows[1][0]==fixed_observation
    completions.append([[str(a) for a in f] for f in flows])
report['completion_scope_example']={'rho_sum':0,'state_flows_residual_label1_label2':completions,'label2_product_not_determined':True}
(root/'stage1-review5-evidence/check-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
