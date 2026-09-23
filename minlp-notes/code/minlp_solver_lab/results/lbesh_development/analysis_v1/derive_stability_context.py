"""Queries of three completed repetitions and all supported quadratic controls."""
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent
source=HERE/'analysis.json'
data=json.loads(source.read_text())
rows=data['records']
by={(r['run'],r['instance'],r['method']):r for r in rows}
runs=['main_generated_v1','repeat_heldout_v1_r2','repeat_heldout_v1_r3']
held=sorted({r['instance'] for r in rows if r['run']==runs[0] and r['split']=='held_out'})


def sgm(values):
    return math.expm1(statistics.mean(math.log1p(v) for v in values)) if values else None


out=dict(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
         script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         repetition_order=runs,oracle_stability=[],method_stability=[],quadratic_controls=[])
for form in ('hull','bigm'):
    methods=[f'lbesh-{oracle}-{form}-single' for oracle in ('esh','ecp')]
    common=[i for i in held if all(by[run,i,m]['solved'] for run in runs for m in methods)]
    repeats=[]
    for run in runs:
        esh,ecp=[sgm([by[run,i,m]['wall_time'] for i in common]) for m in methods]
        repeats.append(dict(run=run,esh_wall_sgm=esh,ecp_wall_sgm=ecp,esh_over_ecp=esh/ecp))
    out['oracle_stability'].append(dict(formulation=form,common_instances=common,
                                        common_solved_all_three=len(common),repetitions=repeats))
    for method in methods:
        ranges=[]
        for i in held:
            times=[by[run,i,method]['wall_time'] for run in runs]
            ranges.append(dict(instance=i,times=times,max_over_min=max(times)/min(times),
                categories=[by[run,i,method]['category'] for run in runs]))
        out['method_stability'].append(dict(method=method,instances=len(held),
            solved_counts=[sum(by[run,i,method]['solved'] for i in held) for run in runs],
            par10_means=[statistics.mean(by[run,i,method]['wall_time'] if by[run,i,method]['solved'] else 1500 for i in held) for run in runs],
            all_categories_unchanged=all(len(set(r['categories']))==1 for r in ranges),
            median_instance_max_over_min=statistics.median(r['max_over_min'] for r in ranges),
            max_instance_max_over_min=max(r['max_over_min'] for r in ranges),ranges=ranges))
for method in sorted({r['method'] for r in rows if r['run'] in (runs[0],'quadratic_conic_v1')}):
    rs=[r for r in rows if r['run'] in (runs[0],'quadratic_conic_v1') and r['family']=='quadratic' and r['method']==method]
    for split in ('held_out','pilot','all'):
        subset=[r for r in rs if split=='all' or r['split']==split]
        common=[r['instance'] for r in subset if r['solved']]
        conic=[by['quadratic_conic_v1',i,'conic-hull-gurobi'] for i in common]
        assert all(r['solved'] for r in conic)
        a=sgm([r['wall_time'] for r in subset if r['solved']]);b=sgm([r['wall_time'] for r in conic])
        out['quadratic_controls'].append(dict(method=method,split=split,scheduled=len(subset),
            numerical_solves=len(common),common_instances=common,method_common_wall_sgm=a,
            conic_common_wall_sgm=b,method_over_conic_wall_sgm=a/b if b else None,
            par10_mean=statistics.mean(r['wall_time'] if r['solved'] else 1500 for r in subset)))
(HERE/'stability_context.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print('Wrote',HERE/'stability_context.json')
