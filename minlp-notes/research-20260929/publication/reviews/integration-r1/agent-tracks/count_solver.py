# Independent recount of solver-runs/results.csv (read-only; no project imports).
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import csv, collections
from fractions import Fraction
from decimal import Decimal
B=(_PUBLIC_REPO + '/research-20260929/publication/solver-runs/')
R=list(csv.DictReader(open(B+'results.csv')))
T={(r['instance'],r['solver']):r for r in csv.DictReader(open(B+'results_table.csv'))}
print('rows',len(R),'instances',len({r['instance'] for r in R}))
print('solver versions',collections.Counter((r['solver'],r['solver_version']) for r in R))
print('settings',collections.Counter((r['reslim'],r['optcr'],r['optca']) for r in R))
print('threads_confirmed',collections.Counter(r['threads_confirmed'] for r in R))
print('valid',collections.Counter(r['valid'] for r in R))
inv=[(r['instance'],r['solver'],r['end_kind'],r['kill_reason'],r['solver_status'],r['model_status']) for r in R if r['valid']!='True']
print('invalid',inv)
print('end_kind',collections.Counter((r['solver'],r['end_kind']) for r in R))
claims=[(r['instance'],r['solver'],r['primal_objective']) for r in R if r['model_status']=='1' and r['solver_status']=='1']
print('opt claims (1/1)',claims)
print('model_status counts',collections.Counter((r['solver'],r['model_status']) for r in R))
def fr(s):
    s=s.strip()
    if s in ('','nan','NA'): return None
    if s.lower() in ('inf','-inf','infinity','-infinity','+inf'): return None
    return Fraction(Decimal(s))
fin=[]
for r in R:
    d=fr(r['dual_bound'])
    if d is not None: fin.append((r,d))
print('finite duals',len(fin),collections.Counter(r['solver'] for r,_ in fin))
gw=[(r['instance'],r['solver']) for r,_ in fin if r['globality_warning']=='True']
print('globality_warning among finite',gw)
print('globality_warning all rows',[(r['instance'],r['solver']) for r in R if r['globality_warning']=='True'])
tw=[(r['instance'],r['solver']) for r,_ in fin if r['scip_argument_bounds_tightened']=='True']
print('scip tightened among finite',tw)
print('scip tightened all',[(r['instance'],r['solver']) for r in R if r['scip_argument_bounds_tightened']=='True'])
nw=[x for x in fin if x[0]['globality_warning']!='True']
print('finite without warning',len(nw),collections.Counter(r['solver'] for r,_ in nw))
# compare to certificate
weaker=0; notweaker=[]; scope=collections.Counter()
for r,d in fin:
    t=T[(r['instance'],r['solver'])]
    c=Fraction(Decimal(t['certificate_dual'])); s=1 if r['sense']=='min' else -1
    scope[t['certificate_scope']]+=1
    if s*(c-d)>0: weaker+=1
    else: notweaker.append((r['instance'],r['solver'],str(d),str(c)))
    if t['dual']!='' :
        try:
            if Fraction(Decimal(t['dual']))!=d: print('table dual differs',r['instance'],r['solver'],t['dual'],r['dual_bound'])
        except Exception as e: print('parse',t['dual'],e)
print('weaker than cert',weaker,'not weaker',notweaker,'scope',scope)
fb=[(r['instance'],r['solver'],r['valid']) for r in R if r['loaded_first_batch']=='True']
print('first batch',len(fb),fb)
# camshape claims vs certificate
for r in R:
    if r['instance'] in('camshape100','camshape200') and r['solver']=='BARON':
        t=T[(r['instance'],'BARON')]
        p=Fraction(Decimal(r['primal_objective'])); c=Fraction(Decimal(t['certificate_dual']))
        print(r['instance'],'primal',r['primal_objective'],'cert',t['certificate_dual'],'P-C',float(p-c),'dual',r['dual_bound'], 'viol',r['reported_max_constraint_violation'],'notes',r['notes'][:200])
# BARON cpu vs wall
for r in R:
    if r['solver']=='BARON' and r['solver_time_s'] and float(r['solver_time_s'])>3600:
        print('BARON >3600',r['instance'],r['solver_time_s'],r['cpu_time_s'],r['wall_time_s'])
print('statuses of memory stops',[(r['instance'],r['solver'],r['solver_status'],r['model_status'],r['dual_bound'],r['kill_reason']) for r in R if r['valid']!='True'])
