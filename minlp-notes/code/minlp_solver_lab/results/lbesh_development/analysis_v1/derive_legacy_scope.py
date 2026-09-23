"""Legacy strata from model expressions and stated adapter scope, not winners.

All six Euclidean-norm objective models form one nonsmooth stratum, including
those that happened to solve. Exponential batch models are outside the conic
adapter scope. Original interface errors remain failures in every full table.
"""
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent
source=HERE/'analysis.json'
data=json.loads(source.read_text())
rows=[r for r in data['records'] if r['run']=='legacy_external_v1']
by={(r['instance'],r['method']):r for r in rows}
names=sorted({r['instance'] for r in rows})
methods=sorted({r['method'] for r in rows})
norm={i for i in names if i.startswith('pyomo.constrained_layout.') and i.endswith('.l2')}
exp={'gdplib.batch_processing','gdplib.small_batch'}
assert len(names)==27 and len(norm)==6
scopes={'all_legacy':names,'without_norm_objectives':[i for i in names if i not in norm],
        'nonsmooth_norm_objectives':sorted(norm),'conic_supported':[i for i in names if i not in exp],
        'without_norm_and_conic_supported':[i for i in names if i not in norm|exp]}


def sgm(values):
    return math.expm1(statistics.mean(math.log1p(v) for v in values)) if values else None


def pair(a,b,scope):
    common=[i for i in scope if by[i,a]['solved'] and by[i,b]['solved']]
    av,bv=[sgm([by[i,m]['wall_time'] for i in common]) for m in (a,b)]
    return dict(first=a,second=b,scheduled=len(scope),common_instances=common,common_solved=len(common),
                first_wall_sgm=av,second_wall_sgm=bv,first_over_second=av/bv if bv else None)


out=dict(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
         script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         scopes=scopes,outcomes=[],oracle_pairs=[],conic_pairs=[])
for label,scope in scopes.items():
    for method in methods:
        rs=[by[i,method] for i in scope]
        out['outcomes'].append(dict(scope=label,method=method,scheduled=len(scope),
            categories=dict(collections.Counter(r['category'] for r in rs)),
            numerical_solves=sum(r['solved'] for r in rs),
            par10_mean=statistics.mean(min(150,r['wall_time']) if r['solved'] else 1500 for r in rs)))
    for form,tree in itertools.product(('hull','bigm'),('single','multi')):
        out['oracle_pairs'].append(dict(scope=label,formulation=form,tree=tree,
            **pair(f'lbesh-esh-{form}-{tree}',f'lbesh-ecp-{form}-{tree}',scope)))
    if label in ('conic_supported','without_norm_and_conic_supported'):
        for method in methods:
            if method.startswith('lbesh-'):
                out['conic_pairs'].append(dict(scope=label,**pair('conic-hull-gurobi',method,scope)))
(HERE/'legacy_scope.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print('Wrote',HERE/'legacy_scope.json')
