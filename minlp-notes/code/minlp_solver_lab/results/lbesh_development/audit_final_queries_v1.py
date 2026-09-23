"""Independent final sidecar linkage and all33 followup pair audit."""
import json,math,sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import lbesh_results_independent_audit as a
root=Path(__file__).parent; final=root/'analysis_v1'; fresh=a.read(root/'audit_final_v1.json')
for label,info in fresh['inputs'].items():assert a.digest(root/(label+'.jsonl'))==info['sha256']
linked=[]
for old,name in [('analysis_legacy_v2','legacy_scope'),('analysis_planned_v1','ablations_references'),('analysis_repeats_conic_v1','stability_context')]:
 before=a.read(root/old/(name+'.json'));after=a.read(final/(name+'.json'))
 assert after['input_sha256']==a.digest(final/'analysis.json')
 assert after['script_sha256']==a.digest(final/('derive_'+name+'.py')) if name!='ablations_references' else after['script_sha256']==a.digest(final/'derive_ablations_references.py')
 assert {k:v for k,v in before.items() if k!='input_sha256'}=={k:v for k,v in after.items() if k!='input_sha256'}
 linked.append(name)
d=a.read(final/'followups.json');assert d['input_sha256']==a.digest(final/'analysis.json');assert d['script_sha256']==a.digest(final/'derive_followups.py')
labels=['main_generated_v1','legacy_external_v1','gurobi_trig_sensitivity_v1','legacy_initialization_v1'];raw={label:[json.loads(s) for s in (root/(label+'.jsonl')).read_text().splitlines()] for label in labels}
for label,rs in raw.items():
 for r in rs:r['_file']=label
assert a.classify([r for rs in raw.values() for r in rs],[],False)==[]
by={label:{(r['instance'],r['method']):r for r in rs} for label,rs in raw.items()}
def category(r):
 if r['_solved']:return 'numerical_solve'
 if r['outcome']!='completed':return r['outcome']
 if r['_feasible']:return 'feasible_open_gap'
 if 'infeasible' in str(r.get('raw_status','')).lower():return 'reported_infeasible'
 return 'invalid_witness' if r.get('witness') else 'no_witness'
def original(label,n,m):return by['main_generated_v1' if label=='gurobi_trig_sensitivity_v1' else 'legacy_external_v1'][n,m.removesuffix('-feas1e8').removesuffix('-initialized')]
expected={(label,r['instance'],r['method']) for label in labels[2:] for r in raw[label]}
assert Counter((x['run'],x['instance'],x['method']) for x in d['paired'])==Counter(expected)
checked=0
for x in d['paired']:
 label,n,m=x['run'],x['instance'],x['method'];old=original(label,n,m);new=by[label][n,m]
 assert x['size']==a.dimensions(n)[1]
 for prefix,r in [('original',old),('followup',new)]:
  val=r.get('validation') or {};bound=r.get('dual_bound');obj=val.get('objective')
  gap=abs(obj-bound) if r['_feasible'] and r.get('bound_valid') is True and a.finite(bound) else None
  expected_fields=dict(category=category(r),feasible=r['_feasible'],solved=r['_solved'],wall_time=r['wall_time'],objective=obj,dual_bound=bound,absolute_gap=gap,raw_status=r.get('raw_status'),max_normalized_violation=val.get('max_normalized_violation'),validation_issues=val.get('issues',[{'kind':'no_witness'}]))
  for key,value in expected_fields.items():
   actual=x[prefix+'_'+key]
   if isinstance(value,float):assert math.isclose(actual,value,rel_tol=1e-12,abs_tol=1e-12),(n,m,key,actual,value)
   else:assert actual==value,(n,m,key,actual,value)
   checked+=1
assert Counter((x['run'],x['method']) for x in d['summaries'])==Counter({(r['run'],r['method']) for r in d['paired']})
for x in d['summaries']:
 label,m=x['run'],x['method'];rs=[r for r in raw[label] if r['method']==m];old=[original(label,r['instance'],m) for r in rs]
 assert x['scheduled']==len(rs)
 for prefix,group in [('original',old),('followup',rs)]:
  assert x[prefix+'_categories']==dict(Counter(category(r) for r in group))
  assert x[prefix+'_feasible']==sum(r['_feasible'] for r in group) and x[prefix+'_solved']==sum(r['_solved'] for r in group)
result=dict(accepted=True,linked_unchanged_previously_audited_sidecars=linked,paired_comparisons=len(d['paired']),paired_fields_checked=checked,followup_summary_groups=len(d['summaries']),analysis_sha256=a.digest(final/'analysis.json'),followup_sha256=a.digest(final/'followups.json'),audit_source_sha256=a.digest(Path(__file__)))
p=root/'audit_final_queries_v1.json';assert not p.exists();p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
