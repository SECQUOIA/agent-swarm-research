import json
from fractions import Fraction
from decimal import Decimal
P={r['name']:r for r in json.load(open('pages.json'))}
R=json.load(open('results.json'))
def F(s):
    try: d=Decimal(s)
    except Exception: return None
    return Fraction(d) if d.is_finite() else None
# proven worst objective per instance for class (i)/(i-r)
best={}
for x in R:
    if x['cls'].startswith('(i)') or x['cls'].startswith('(i-r)'):
        hi=Fraction(Decimal(x['obj_hi'])) if x['sense']=='min' else Fraction(Decimal(x['obj_lo']))
        n=x['name']; sg=1 if x['sense']=='min' else -1
        if n not in best or sg*hi<sg*best[n]: best[n]=hi
for n,f in sorted(best.items()):
    r=P[n]; sg=1 if r['sense']=='min' else -1
    ds=sorted([(F(d['value']),d['solver'],d['value']) for d in r['duals'] if F(d['value']) is not None], key=lambda t:-sg*t[0])
    top3=ds[:3]
    bp=[ (F(p['value']),p['point'],p['value']) for p in r['points'] if p['section']=='primal']
    bp=min(bp,key=lambda t: sg*t[0]) if bp else None
    third=top3[2] if len(top3)>=3 else None
    inv=[s for v,s,_ in ds if sg*(v-f)>0]
    print(n, 'S' if r['solved'] else '-', 'listing',r['listing_dual'],'primal',bp[2] if bp else None,'| top3',[(s,v) for _,s,v in top3],'| invalid solvers(>f_hi)',inv,'| third invalid?', third is not None and sg*(third[0]-f)>0, '| nduals',len(ds))
