import json, math
from fractions import Fraction
from decimal import Decimal
P=json.load(open('pages.json'))
def F(s):
    try:
        d=Decimal(s)
    except Exception:
        return None
    if not d.is_finite(): return None
    return Fraction(d)
npts=sum(len(r['points']) for r in P); nd=sum(len(r['duals']) for r in P)
nfin=sum(1 for r in P for d in r['duals'] if F(d['value']) is not None)
print('pages',len(P),'points',npts,'duals',nd,'finite',nfin)
from collections import Counter
print(Counter(r['sense'] for r in P))
pairs=[];ties=[];skip_inf=0
for r in P:
    if r['sense'] not in ('min','max'): continue
    sg=1 if r['sense']=='min' else -1
    for p in r['points']:
        pv=F(p['value']); 
        try: inf=float(p['infeas'])
        except: inf=None
        if pv is None: continue
        if inf is not None and inf>1e-5:
            # check if any dual beyond
            for d in r['duals']:
                dv=F(d['value'])
                if dv is not None and sg*(dv-pv)>0: skip_inf+=1
            continue
        for d in r['duals']:
            dv=F(d['value'])
            if dv is None: continue
            if sg*(dv-pv)>0: pairs.append((r['name'],p['point'],d['solver']))
            elif dv==pv: ties.append((r['name'],p['point'],d['solver']))
print('exact screen pairs',len(pairs),'points',len({(a,b) for a,b,c in pairs}),'inst',len({a for a,b,c in pairs}),'ties',len(ties),'tie inst',len({a for a,b,c in ties}),'skipped(infeas>1e-5) beyond',skip_inf)
S=json.load(open('screen.json'))
sp={(x['name'],x['point'],x['solver']) for x in S['pairs']}; st={(x['name'],x['point'],x['solver']) for x in S['ties']}
print('float screen pairs',len(sp),'ties',len(st))
print('pairs diff exact-float',set(pairs)-sp, sp-set(pairs))
print('ties diff', set(ties)-st, st-set(ties))
print('other section among pairs', sum(1 for x in S['pairs'] if x['section']=='other'))
