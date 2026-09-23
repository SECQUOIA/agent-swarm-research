"""Descriptive matched-cohort queries of the completed, audited primary data.

No raw validation decisions are changed. No solvers or significance tests.
"""
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent
source = HERE/'analysis.json'
data = json.loads(source.read_text())
rows = data['records']
by = {(r['instance'],r['method']):r for r in rows}
info = {r['instance']:r for r in rows}
metrics = ('cuts','lp_iters','milp_iters','nlp_solves','interior_nlps','nodes',
           'time_master','time_nlp','time_interior','time_cuts','time_setup','time_total')


def sgm(values):
    return math.expm1(statistics.mean(math.log1p(v) for v in values)) if values else None


def contrast(first, second, names):
    common = sorted(i for i in names if by[i,first]['solved'] and by[i,second]['solved'])
    result = dict(first=first,second=second,scheduled=len(names),common_instances=common,
                  common_solved=len(common),metrics={},lp_end_reasons={})
    for method in (first,second):
        rs = [by[i,method] for i in common]
        result[method] = dict(numerical_solves=sum(by[i,method]['solved'] for i in names),
            common_wall_sgm=sgm([min(150,r['wall_time']) for r in rs]),
            par10_mean=statistics.mean(min(150,by[i,method]['wall_time']) if by[i,method]['solved'] else 1500 for i in names))
        result['lp_end_reasons'][method] = dict(collections.Counter(r['lp_end_reason'] for r in rs))
        result['metrics'][method] = {}
        for metric in metrics:
            values = [r[metric] for r in rs if r[metric] is not None]
            result['metrics'][method][metric] = dict(available=len(values),
                mean=statistics.mean(values) if values else None,
                median=statistics.median(values) if values else None)
    a,b = [result[m]['common_wall_sgm'] for m in (first,second)]
    result['first_over_second_wall_sgm'] = a/b if b else None
    return result


output = dict(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              meaning='All telemetry uses the identical common-solved cohort within each contrast; component times overlap.',
              oracle=[],structure=[])
for split in ('held_out','pilot','all'):
    names = sorted(i for i,r in info.items() if split=='all' or r['split']==split)
    groups = [('all','all',names)]
    if split=='held_out':
        for dim in ('family','size'):
            groups += [(dim,v,[i for i in names if info[i][dim]==v]) for v in sorted({info[i][dim] for i in names})]
    for dim,val,cohort in groups:
        for form,tree in itertools.product(('hull','bigm'),('single','multi')):
            result = contrast(f'lbesh-esh-{form}-{tree}',f'lbesh-ecp-{form}-{tree}',cohort)
            output['oracle'].append(dict(split=split,dimension=dim,group=val,formulation=form,tree=tree,**result))
    if split=='held_out':
        for oracle in ('esh','ecp'):
            for tree in ('single','multi'):
                result=contrast(f'lbesh-{oracle}-hull-{tree}',f'lbesh-{oracle}-bigm-{tree}',names)
                output['structure'].append(dict(effect='hull/bigm',oracle=oracle,tree=tree,**result))
            for form in ('hull','bigm'):
                result=contrast(f'lbesh-{oracle}-{form}-single',f'lbesh-{oracle}-{form}-multi',names)
                output['structure'].append(dict(effect='single/multi',oracle=oracle,formulation=form,**result))
(HERE/'cohorts.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
print('Wrote',HERE/'cohorts.json')
