"""Independent raw-record audit of legacy strata, ablations, and cone comparisons."""
import json,math,statistics,sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import lbesh_results_independent_audit as a
root=Path(__file__).parent
files=['main_generated_v1','legacy_external_v1','ablations_pilot_v1']
raw={label:[json.loads(s) for s in (root/(label+'.jsonl')).read_text().splitlines()] for label in files}
for label,rs in raw.items():
 for r in rs:r['_file']=label
assert a.classify([r for rs in raw.values() for r in rs],[],False)==[]
by={label:{(r['instance'],r['method']):r for r in rs} for label,rs in raw.items()}
def near(x,y):assert math.isclose(x,y,abs_tol=1e-11,rel_tol=1e-10),(x,y)
def cat(r):
 if r['_solved']:return 'numerical_solve'
 if r['outcome']!='completed':return r['outcome']
 if r['_feasible']:return 'feasible_open_gap'
 if 'infeasible' in str(r.get('raw_status','')).lower():return 'reported_infeasible'
 return 'invalid_witness' if r.get('witness') else 'no_witness'
def time(r):return min(r['wall_time'],150)
def mean(rs):return a.shifted([time(r) for r in rs])
def provenance(folder,name,script):
 d=a.read(root/folder/name);assert d['input_sha256']==a.digest(root/folder/'analysis.json');assert d['script_sha256']==a.digest(root/folder/script);return d
legacy=provenance('analysis_legacy_v2','legacy_scope.json','derive_legacy_scope.py')
names=sorted({r['instance'] for r in raw['legacy_external_v1']});norm=[n for n in names if n.startswith('pyomo.constrained_layout.') and n.endswith('.l2')]
assert len(norm)==6
expected={'all_legacy':names,'without_norm_objectives':[n for n in names if n not in norm],'nonsmooth_norm_objectives':norm,'conic_supported':[n for n in names if n not in ('gdplib.batch_processing','gdplib.small_batch')]}
expected['without_norm_and_conic_supported']=[n for n in expected['conic_supported'] if n not in norm]
assert legacy['scopes']==expected,legacy['scopes'].keys()
lookup=by['legacy_external_v1'];methods=sorted({r['method'] for r in raw['legacy_external_v1']})
assert Counter((x['scope'],x['method']) for x in legacy['outcomes'])==Counter((s,m) for s in expected for m in methods)
for x in legacy['outcomes']:
 rs=[lookup[n,x['method']] for n in expected[x['scope']]]
 assert x['scheduled']==len(rs) and x['categories']==dict(Counter(cat(r) for r in rs)) and x['numerical_solves']==sum(r['_solved'] for r in rs)
 near(x['par10_mean'],statistics.fmean(time(r) if r['_solved'] else 1500 for r in rs))
assert len(legacy['oracle_pairs'])==20 and len(legacy['conic_pairs'])==16
for x in legacy['oracle_pairs']+legacy['conic_pairs']:
 ns=expected[x['scope']];m1,m2=x['first'],x['second'];common=[n for n in ns if lookup[n,m1]['_solved'] and lookup[n,m2]['_solved']]
 assert x['scheduled']==len(ns) and x['common_instances']==common and x['common_solved']==len(common)
 ga,gb=[mean([lookup[n,m] for n in common]) for m in (m1,m2)]
 near(x['first_wall_sgm'],ga);near(x['second_wall_sgm'],gb);near(x['first_over_second'],ga/gb)
d=provenance('analysis_planned_v1','ablations_references.json','derive_ablations_references.py')
assert len(d['ablations'])==8
for x in d['ablations']:
 m=x['base_method'];v=m+'-'+x['variant'];ns=sorted({r['instance'] for r in raw['ablations_pilot_v1']});rs=[by['ablations_pilot_v1'][n,v] for n in ns];base=[by['main_generated_v1'][n,m] for n in ns]
 assert x['scheduled']==18 and x['default_solved']==sum(r['_solved'] for r in base) and x['variant_solved']==sum(r['_solved'] for r in rs)
 assert x['categories']==dict(Counter(cat(r) for r in rs)) and x['raw_statuses']==dict(Counter(r['raw_status'] for r in rs))
 common=[n for n in ns if by['main_generated_v1'][n,m]['_solved'] and by['ablations_pilot_v1'][n,v]['_solved']]
 assert set(x['common_instances'])==set(common) and x['common_solved']==len(common)
 ga,gb=mean([by['ablations_pilot_v1'][n,v] for n in common]),mean([by['main_generated_v1'][n,m] for n in common])
 if common:near(x['variant_wall_sgm'],ga);near(x['default_wall_sgm'],gb);near(x['variant_over_default_wall_sgm'],ga/gb)
 else:assert x['variant_wall_sgm'] is None and x['default_wall_sgm'] is None and x['variant_over_default_wall_sgm'] is None
 metrics=[r['solver_metrics'] for r in rs]
 for field,key in [('recorded_user_cuts','user_cuts'),('integer_nlp_solves','nlp_solves'),('interior_nlp_solves','interior_nlps')]:near(x[field],sum(z.get(key,0) for z in metrics))
 assert x['instances_with_user_cuts']==sum(z.get('user_cuts',0)>0 for z in metrics)
roots=[json.loads(s) for s in (root/'general_conic_roots_frozen_v1.jsonl').read_text().splitlines()];ref={r['name']:r for r in roots};main=by['main_generated_v1']
for x in d['roots']:
 m='lbesh-'+x['oracle']+'-hull-single';names=[r['name'] for r in roots if r['status']=='optimal'];vals={n:(ref[n]['lb']-main[n,m]['solver_metrics']['lp_bound'])/max(1,abs(ref[n]['obj'])) for n in names}
 assert x['count']==40 and {r['instance'] for r in x['instance_values']}==set(names)
 near(x['normalized_gap_min'],min(vals.values()));near(x['normalized_gap_median'],statistics.median(vals.values()));near(x['normalized_gap_max'],max(vals.values()))
 assert x['within_1e4']==sum(abs(v)<=1e-4 for v in vals.values()) and x['worst_instance']==max(vals,key=vals.get)
 assert x['same_recorded_lp_bounds_across_tree_modes'] is True
 for q in roots:assert main[q['name'],m]['solver_metrics']['lp_bound']==main[q['name'],m.replace('-single','-multi')]['solver_metrics']['lp_bound']
 for z in x['instance_values']:
  n=z['instance'];near(z['normalized_gap'],vals[n]);assert z['lp_bound']==main[n,m]['solver_metrics']['lp_bound'] and z['cone_dual_estimate']==ref[n]['lb']
  assert z['cone_primal_residual']==ref[n]['primal_residual'] and z['cone_dual_residual']==ref[n]['dual_residual'] and z['lp_end_reason']==main[n,m]['solver_metrics']['lp_end_reason']
assert len(d['inaccurate_roots'])==4
for z in d['inaccurate_roots']:
 q=ref[z['instance']];assert q['status']=='optimal_inaccurate' and z['bound_certified'] is False
 near(z['normalized_gap'],(q['lb']-main[z['instance'],z['method']]['solver_metrics']['lp_bound'])/max(1,abs(q['obj'])))
enums=[json.loads(s) for s in (root/'general_conic_enumeration_frozen_v1.jsonl').read_text().splitlines()];eref={r['name']:r for r in enums};e=d['enumeration']
assert e['reference_sha256']==a.digest(root/'general_conic_enumeration_frozen_v1.jsonl') and e['instances']==14
assert e['assignment_statuses']==dict(Counter(r['status'] for z in enums for r in z['rows'])) and e['instance_statuses']==dict(Counter(z['status'] for z in enums))
expected={(r['instance'],r['method']) for r in raw['main_generated_v1'] if r['instance'] in eref and r['_solved']}
assert e['primary_accepted_comparisons']==182 and Counter((x['instance'],x['method']) for x in e['agreements'])==Counter(expected)
ratios=[]
for x in e['agreements']:
 r=main[x['instance'],x['method']];diff=r['_objective']-eref[x['instance']]['obj'];near(x['objective_difference'],diff)
 near(x['comparison_tolerance'],a.tolerance(eref[x['instance']]['obj']));assert x['within_tolerance']==(abs(diff)<=x['comparison_tolerance']);ratios.append(abs(diff)/x['comparison_tolerance'])
out=dict(accepted=True,legacy_scope_method_groups=65,legacy_pair_groups=36,ablation_groups=8,root_policy_groups=2,root_inaccurate_policy_groups=4,enumeration_primary_comparisons=182,max_enumeration_fraction_of_tolerance=max(ratios),script_sha256=a.digest(Path(__file__)),legacy_derivation_sha256=a.digest(root/'analysis_legacy_v2/legacy_scope.json'),ablation_reference_derivation_sha256=a.digest(root/'analysis_planned_v1/ablations_references.json'))
p=root/'audit_secondary_queries_v1.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
