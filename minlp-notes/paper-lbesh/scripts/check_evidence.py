#!/usr/bin/env python3
"""Check the numerical statements outside generated tables, using local data only."""
import json, math, hashlib, random
from pathlib import Path
from collections import Counter
from statistics import median,mean
P=Path(__file__).resolve().parents[1]
load=lambda f:json.loads((P/'data'/f).read_text())
R=load('records.json'); O=load('oracle.json'); I=load('instance_parameters.json'); E=load('enumeration_summary.json'); scopes=load('legacy_scope.json'); roots=load('cone_roots.json')
def sel(run='main_generated_v1',**kw):return [r for r in R if r['run']==run and all(r[k]==v for k,v in kw.items())]
def sgm(rr):return math.expm1(mean(math.log1p(r['wall_time']) for r in rr))
report={}
report['primary_categories']=dict(Counter(r['category'] for r in sel()))
assert report['primary_categories']=={'numerical_solve':550,'feasible_open_gap':106,'invalid_witness':6,'wall_timeout':1}
assert sum(r['raw_status']=='optimal' for r in sel())==603
report['legacy_categories']=dict(Counter(r['category'] for r in sel('legacy_external_v1')))
assert report['legacy_categories']=={'numerical_solve':239,'feasible_open_gap':38,'invalid_witness':4,'error':61,'no_witness':7,'unsupported':2}
report['repeat_ranges']={}
for f in ['hull','bigm']:
 for o in ['esh','ecp']:
  m=f'lbesh-{o}-{f}-single';rr=[r for r in R if r['run'] in ['main_generated_v1','repeat_heldout_v1_r2','repeat_heldout_v1_r3'] and r['method']==m and r['split']=='held_out']; ratios=[]
  for n in set(r['instance'] for r in rr):
   row=[r for r in rr if r['instance']==n];assert len(row)==3 and len(set(r['category'] for r in row))==1;ratios.append(max(r['wall_time'] for r in row)/min(r['wall_time'] for r in row))
  report['repeat_ranges'][m]={'median':median(ratios),'maximum':max(ratios)}
report['pilot_pairs']={}
for f,t in [('hull','single'),('hull','multi'),('bigm','single'),('bigm','multi')]:
 a={r['instance']:r for r in sel(method=f'lbesh-esh-{f}-{t}',split='pilot') if r['solved']};b={r['instance']:r for r in sel(method=f'lbesh-ecp-{f}-{t}',split='pilot') if r['solved']};names=sorted(a.keys()&b.keys());report['pilot_pairs'][f'{f}-{t}']={'count':len(names),'ratio':sgm([a[n] for n in names])/sgm([b[n] for n in names])}
report['paired_extra_work']={}
for f,t in [('hull','single'),('hull','multi'),('bigm','single'),('bigm','multi')]:
 aa={r['instance']:r for r in sel(method=f'lbesh-esh-{f}-{t}',split='held_out') if r['solved']};bb={r['instance']:r for r in sel(method=f'lbesh-ecp-{f}-{t}',split='held_out') if r['solved']};names=sorted(aa.keys()&bb.keys());a=[aa[n] for n in names];b=[bb[n] for n in names]
 assert all(x['interior_nlps']==y['interior_nlps'] for x,y in zip(a,b))
 report['paired_extra_work'][f'{f}-{t}']={'names':names,'cut_count_reduction':1-mean(r['cuts'] for r in a)/mean(r['cuts'] for r in b),'cut_time_ratio':mean(r['time_cuts'] for r in a)/mean(r['time_cuts'] for r in b),'interior_count':mean(r['interior_nlps'] for r in a),'interior_times':[mean(r['time_interior'] for r in x) for x in [a,b]]}
report['lp_exits']={}
for f in ['hull','bigm']:
 for o in ['esh','ecp']:
  for t in ['single','multi']:
   rr=sel(method=f'lbesh-{o}-{f}-{t}',split='held_out');vals=[r['last_lp_max_perspective_violation'] for r in rr if r['last_lp_max_perspective_violation'] is not None]
   report['lp_exits'][f'{o}-{f}-{t}']={'reasons':dict(Counter(r['lp_end_reason'] for r in rr)),'maximum_residual':max(vals) if vals else None}
nonlp=[r for r in sel('ablations_pilot_v1') if r['method'].endswith('-nonlp')]
assert len(nonlp)==72 and sum(r['solved'] for r in nonlp)==1 and sum(r['nlp_solves'] for r in nonlp)==0
assert Counter(r['raw_status'] for r in nonlp)=={'stalled':62,'time_limit':9,'optimal':1}
assert sum(r['raw_status']=='stalled' and not r['feasible'] for r in nonlp)==53
assert sum(r['raw_status']=='stalled' and r['feasible'] for r in nonlp)==9
assert all(not r['feasible'] for r in nonlp if r['raw_status']=='time_limit')
for m in set(r['method'] for r in nonlp):assert sum(r['interior_nlps'] for r in nonlp if r['method']==m)==369
report['external_conic_comparisons']={}
for m in sorted(set(r['method'] for r in sel('legacy_external_v1') if r['method'].startswith('lbesh-'))):
 a={r['instance']:r for r in sel('legacy_external_v1',method=m) if r['solved']};b={r['instance']:r for r in sel('legacy_external_v1',method='conic-hull-gurobi') if r['solved']};names=set(a)&set(b)&set(scopes['without_norm_and_conic_supported']);assert len(names)==17
 x,y=[a[n] for n in sorted(names)],[b[n] for n in sorted(names)];report['external_conic_comparisons'][m]={'prototype':sgm(x),'conic':sgm(y),'ratio':sgm(y)/sgm(x)}
assert E['instances']==14 and E['primary_accepted_comparisons']==182 and len(E['agreements'])==182 and all(r['within_tolerance'] for r in E['agreements'])
report['maximum_enumeration_tolerance_fraction']=max(abs(r['objective_difference'])/r['comparison_tolerance'] for r in E['agreements'])
report['oracle_scalar_max_error']=max(r['geometric_error'] for r in O['scalar'] if r['policy']=='ecp')
report['oracle_max_recurrence_error']=max(r['recurrence_max_error'] for r in O['scalar'])
assert len(O['quadratic'])==896
report['oracle_esh_max_support_error']=O['summary']['quadratic_esh_max_support_constant_error']
report['oracle_scalar_median_time_ranges']={o:[min(median(r['elapsed_seconds_samples']) for r in O['scalar'] if r['policy']==o),max(median(r['elapsed_seconds_samples']) for r in O['scalar'] if r['policy']==o)] for o in ['esh','ecp']}
# Independently reconstruct every parameter stream in the mathematical appendix.
assert len(I)==51 and Counter(v['metadata']['split'] for v in I.values())=={'pilot':18,'held_out':33}
for name,entry in I.items():
 meta=entry['metadata'];rng=random.Random(meta['seed']);actual=entry['parameters'];pred=[]
 for i in range(meta['units']):
  if meta['family']=='logsumexp':
   centers=[[-.75,-.35],[.25,.7],[.8,-.45]]
   datum={'centers':[[a+rng.uniform(-.08,.08),b+rng.uniform(-.08,.08)] for a,b in centers], 'scale':[[rng.uniform(1.7,2.3),rng.uniform(1.7,2.3)] for _ in centers], 'radius':[rng.uniform(4.8,5.6) for _ in centers], 'price':[rng.uniform(.8,1.2),rng.uniform(.15,.35)], 'fixed':[rng.uniform(.02,.08) for _ in centers]}
  else:
   datum={'capacity':rng.uniform(.8,1.2),'weight':[rng.uniform(.75,1.25) for _ in range(2)],'cross':rng.uniform(.2,.5),'fixed':[0.,rng.uniform(.08,.12),rng.uniform(.25,.35)],'operating':[0.,rng.uniform(1.05,1.25),rng.uniform(.65,.85)],'mode_capacity':[0.,rng.uniform(.58,.68),1.],'resource':[rng.uniform(.7,1.3) for _ in range(2)]}
  pred.append(datum)
 assert pred==actual,name
 assert hashlib.sha256(json.dumps(pred,sort_keys=True,separators=(',',':')).encode()).hexdigest()==meta['parameters_sha256'],name
report['independent_parameter_reconstructions']=len(I)
report['cone_inaccurate_roots']=[r for r in roots if r['run']=='main_generated_v1' and r['method']=='lbesh-esh-hull-single' and r['cone_status']=='optimal_inaccurate']
assert len(report['cone_inaccurate_roots'])==2
(P/'evidence'/'stage03-claims.json').write_text(json.dumps(report,indent=2)+'\n')
print('Verified narrative arithmetic, 51 independent parameter reconstructions, all batch outcome totals, paired cohort work, repetitions, LP exits, references and oracle counts.')
