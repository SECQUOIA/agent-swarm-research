import csv
from decimal import Decimal as D, getcontext
getcontext().prec=60
rows=list(csv.DictReader(open('results_table.csv')))
refs={r['instance']:r for r in csv.DictReader(open('references.csv'))}
print('rows',len(rows),'instances',len({r['instance'] for r in rows}))
def num(s):
    s=(s or '').strip()
    if s in('','—','-','NA','nan'): return None
    if s.lower() in('-infinity','infinity','inf','-inf','+inf'): return None
    try: return D(s)
    except Exception: return None
from collections import Counter
fin=Counter(); prim=Counter(); valid=Counter(); claims=[]; warn=Counter(); tight=Counter(); batch=0
minmargin=None; beyond=[]; listimp=[]; cutref=[]; osil=0; Rc=0
for r in rows:
    s=r['solver']; sense=r['sense']
    sg=D(1) if sense.lower().startswith('min') else D(-1)
    d=num(r['dual']); p=num(r['primal'])
    if r['valid_time_measurement'].lower()=='true': valid[s]+=1
    if r['globality_warning'].lower() in('true','1','yes'): warn[s]+=1
    if r['scip_argument_bounds_tightened'].lower() in('true','1','yes'): tight[s]+=1
    if r['loaded_first_batch'].lower() in('true','1','yes'): batch+=1
    if r['optimality_claim'].lower() in('true','1','yes'): claims.append((r['instance'],s))
    if p is not None and r['primal'] and 'no primal' not in r['status'] and r['status']!='capability failure': prim[s]+=1
    if d is not None:
        fin[s]+=1
        C=D(refs[r['instance']]['certificate_dual']); P=D(refs[r['instance']]['reference_primal'])
        m=sg*(C-d)
        if 'R' in refs[r['instance']]['certificate_scope'] or r['instance'].startswith('kan'): Rc+=1
        else: osil+=1
        if minmargin is None or m<minmargin[0]: minmargin=(m,r['instance'],s)
        if m<=0: beyond.append((r['instance'],s,m))
        if sg*(d-P)>0: cutref.append((r['instance'],s))
        L=num(refs[r['instance']]['listed_dual'])
        if L is not None and sg*(d-L)>0: listimp.append((r['instance'],s,str(d),str(L)))
print('finite duals',dict(fin),sum(fin.values()),'OSIL',osil,'R',Rc)
print('returned primals (rough)',dict(prim))
print('valid',dict(valid),sum(valid.values()))
print('claims',claims); print('warnings',dict(warn),'tightened',dict(tight),'first-batch rows',batch)
print('min margin',minmargin); print('dual >= cert',beyond); print('dual cuts ref primal',cutref)
print('listed-dual improvements',len(listimp)); [print('  ',x) for x in listimp]
