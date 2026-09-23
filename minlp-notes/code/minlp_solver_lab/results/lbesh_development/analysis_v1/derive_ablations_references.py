"""Declared pilot ablations and same-hull numerical reference diagnostics."""
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent
source=HERE/'analysis.json'
data=json.loads(source.read_text());rows=data['records']
by={(r['run'],r['instance'],r['method']):r for r in rows}
pilot=sorted({r['instance'] for r in rows if r['run']=='main_generated_v1' and r['split']=='pilot'})

def sgm(values):
    return math.expm1(statistics.mean(math.log1p(v) for v in values)) if values else None

out=dict(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
         script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),ablations=[],roots=[],inaccurate_roots=[])
for oracle,form in itertools.product(('esh','ecp'),('hull','bigm')):
    base=f'lbesh-{oracle}-{form}-single'
    for variant in ('nonlp','usercuts'):
        method=base+'-'+variant
        rs=[by['ablations_pilot_v1',i,method] for i in pilot]
        defaults=[by['main_generated_v1',i,base] for i in pilot]
        common=[i for i in pilot if by['ablations_pilot_v1',i,method]['solved'] and by['main_generated_v1',i,base]['solved']]
        av=sgm([by['ablations_pilot_v1',i,method]['wall_time'] for i in common])
        bv=sgm([by['main_generated_v1',i,base]['wall_time'] for i in common])
        out['ablations'].append(dict(base_method=base,variant=variant,scheduled=len(pilot),
            default_solved=sum(r['solved'] for r in defaults),variant_solved=sum(r['solved'] for r in rs),
            categories=dict(collections.Counter(r['category'] for r in rs)),
            raw_statuses=dict(collections.Counter(r['raw_status'] for r in rs)),
            common_instances=common,common_solved=len(common),variant_wall_sgm=av,default_wall_sgm=bv,
            variant_over_default_wall_sgm=av/bv if bv else None,
            recorded_user_cuts=sum(r['user_cuts'] or 0 for r in rs),
            instances_with_user_cuts=sum((r['user_cuts'] or 0)>0 for r in rs),
            integer_nlp_solves=sum(r['nlp_solves'] or 0 for r in rs),
            interior_nlp_solves=sum(r['interior_nlps'] or 0 for r in rs)))
roots=[r for r in data['cone_roots'] if r['run']=='main_generated_v1']
root_by={(r['instance'],r['method']):r for r in roots}
for oracle in ('esh','ecp'):
    method=f'lbesh-{oracle}-hull-single'
    rs=[r for r in roots if r['method']==method]
    for r in rs:
        assert r['lp_bound']==root_by[r['instance'],f'lbesh-{oracle}-hull-multi']['lp_bound']
    accurate=[r for r in rs if r['cone_status']=='optimal']
    gap=lambda r:r['cone_dual_minus_lp']/max(1,abs(r['cone_primal_objective']))
    gaps=[gap(r) for r in accurate]
    out['roots'].append(dict(oracle=oracle,reference_status='optimal',count=len(accurate),
        normalized_gap_min=min(gaps),normalized_gap_median=statistics.median(gaps),normalized_gap_max=max(gaps),
        within_1e4=sum(abs(g)<=1e-4 for g in gaps),
        worst_instance=max(accurate,key=gap)['instance'],same_recorded_lp_bounds_across_tree_modes=True,
        instance_values=[dict(instance=r['instance'],normalized_gap=gap(r),**{k:r[k] for k in
            ('lp_end_reason','cone_primal_residual','cone_dual_residual','cone_dual_estimate','lp_bound')}) for r in accurate]))
    out['inaccurate_roots'] += [dict(oracle=oracle,normalized_gap=gap(r),**r) for r in rs if r['cone_status']!='optimal']
refs=HERE.parent/'general_conic_enumeration_frozen_v1.jsonl'
enums=[json.loads(l) for l in refs.read_text().splitlines() if l.strip()]
reference={r['name']:r for r in enums}
agreements=[]
for r in rows:
    if r['run']=='main_generated_v1' and r['instance'] in reference and r['solved']:
        obj=reference[r['instance']]['obj'];diff=r['objective']-obj;tol=1e-6+1e-4*max(1,abs(obj))
        agreements.append(dict(instance=r['instance'],method=r['method'],objective_difference=diff,
                               comparison_tolerance=tol,within_tolerance=abs(diff)<=tol))
out['enumeration']=dict(reference_sha256=hashlib.sha256(refs.read_bytes()).hexdigest(),
    instances=len(enums),assignment_statuses=dict(collections.Counter(x['status'] for r in enums for x in r['rows'])),
    instance_statuses=dict(collections.Counter(r['status'] for r in enums)),
    primary_accepted_comparisons=len(agreements),agreements=agreements,
    meaning='Numerical exhaustive convex solves and objective agreement; no exact infeasibility or optimum certificates.')
(HERE/'ablations_references.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print('Wrote',HERE/'ablations_references.json')
