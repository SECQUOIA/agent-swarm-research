"""Independent raw-record replay of repeat and quadratic descriptive queries."""
import json,math,statistics,sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import lbesh_results_independent_audit as a
root=Path(__file__).parent; folder=root/'analysis_repeats_conic_v1';d=a.read(folder/'stability_context.json')
assert d['input_sha256']==a.digest(folder/'analysis.json')
assert d['script_sha256']==a.digest(folder/'derive_stability_context.py')
labels=['main_generated_v1','repeat_heldout_v1_r2','repeat_heldout_v1_r3'];assert d['repetition_order']==labels
batches={label:[json.loads(s) for s in (root/(label+'.jsonl')).read_text().splitlines()] for label in labels+['quadratic_conic_v1']}
for label,rows in batches.items():
 for r in rows:r['_file']=label
assert a.classify([r for rs in batches.values() for r in rs],[],False)==[]
lookup={(label,r['instance'],r['method']):r for label,rows in batches.items() for r in rows}
held=sorted({r['instance'] for r in batches[labels[1]]})
methods=sorted({r['method'] for r in batches[labels[1]]})
def near(x,y):assert math.isclose(x,y,abs_tol=1e-10,rel_tol=1e-10),(x,y)
def row(label,n,m):return lookup[label,n,m]
def wall(label,n,m):return min(row(label,n,m)['wall_time'],150)
def category(r):return 'numerical_solve' if r['_solved'] else 'feasible_open_gap' if r['_feasible'] else r['outcome']
assert len(d['oracle_stability'])==2
for x in d['oracle_stability']:
 form=x['formulation'];em=f'lbesh-esh-{form}-single';cm=f'lbesh-ecp-{form}-single'
 common=[n for n in held if all(row(label,n,m)['_solved'] for label in labels for m in (em,cm))]
 assert x['common_instances']==common and x['common_solved_all_three']==len(common)
 assert [z['run'] for z in x['repetitions']]==labels
 for label,z in zip(labels,x['repetitions']):
  ga,gb=[a.shifted([wall(label,n,m) for n in common]) for m in (em,cm)]
  near(z['esh_wall_sgm'],ga);near(z['ecp_wall_sgm'],gb);near(z['esh_over_ecp'],ga/gb)
assert {x['method'] for x in d['method_stability']}==set(methods)
for x in d['method_stability']:
 m=x['method'];assert x['instances']==33
 assert x['solved_counts']==[sum(row(label,n,m)['_solved'] for n in held) for label in labels]
 for label,par in zip(labels,x['par10_means']):near(par,statistics.fmean(wall(label,n,m) if row(label,n,m)['_solved'] else 1500 for n in held))
 assert {r['instance'] for r in x['ranges']}==set(held)
 ratios=[];consistent=True
 for r in x['ranges']:
  n=r['instance'];times=[row(label,n,m)['wall_time'] for label in labels];cats=[category(row(label,n,m)) for label in labels]
  assert r['times']==times and r['categories']==cats
  near(r['max_over_min'],max(times)/min(times));ratios.append(max(times)/min(times));consistent &= len(set(cats))==1
 assert x['all_categories_unchanged']==consistent
 near(x['median_instance_max_over_min'],statistics.median(ratios));near(x['max_instance_max_over_min'],max(ratios))
qnames=sorted(r['instance'] for r in batches['quadratic_conic_v1']);qmethods=sorted({r['method'] for r in batches[labels[0]]})+['conic-hull-gurobi']
assert Counter((x['method'],x['split']) for x in d['quadratic_controls'])==Counter((m,s) for m in qmethods for s in ('held_out','pilot','all'))
for x in d['quadratic_controls']:
 m=x['method'];label='quadratic_conic_v1' if m=='conic-hull-gurobi' else labels[0]
 cohort=[n for n in qnames if x['split']=='all' or a.dimensions(n)[2]==x['split']]
 common=[n for n in cohort if row(label,n,m)['_solved'] and row('quadratic_conic_v1',n,'conic-hull-gurobi')['_solved']]
 assert len(x['common_instances'])==len(common) and set(x['common_instances'])==set(common)
 assert x['scheduled']==len(cohort) and x['numerical_solves']==sum(row(label,n,m)['_solved'] for n in cohort)
 ga=a.shifted([wall(label,n,m) for n in common]);gb=a.shifted([wall('quadratic_conic_v1',n,'conic-hull-gurobi') for n in common])
 near(x['method_common_wall_sgm'],ga);near(x['conic_common_wall_sgm'],gb);near(x['method_over_conic_wall_sgm'],ga/gb)
 near(x['par10_mean'],statistics.fmean(wall(label,n,m) if row(label,n,m)['_solved'] else 1500 for n in cohort))
out=dict(independent_audit_sha256=a.digest(Path(__file__)),raw_sha256={k:a.digest(root/(k+'.jsonl')) for k in batches},context_sha256=a.digest(folder/'stability_context.json'),oracle_stability_cohorts=2,repeated_method_instance_combinations=132,all_categories_unchanged=all(x['all_categories_unchanged'] for x in d['method_stability']),quadratic_method_split_groups=42,accepted=True)
p=root/'audit_stability_v1.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
