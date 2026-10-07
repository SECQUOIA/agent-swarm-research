import json
from fractions import Fraction
from decimal import Decimal
from collections import Counter
P={r['name']:r for r in json.load(open('pages.json'))}
def F(s):
    try: d=Decimal(s)
    except Exception: return None
    return Fraction(d) if d.is_finite() else None
solu={}
for line in open('minlplib.solu'):
    t=line.split()
    if len(t)>=3: solu.setdefault(t[1],{})[t[0]]=t[2]
    if len(t)>=6: solu[t[4]][t[3]]=t[5]
c=Counter(); ex=[]
for n,r in P.items():
    if r['sense'] not in ('min','max') or n not in solu: continue
    s=solu[n]
    if '=bestdual=' not in s: c['no bestdual:'+','.join(s)]+=1; continue
    sg=1 if r['sense']=='min' else -1
    bd=F(s['=bestdual='])
    ds=sorted([F(d['value']) for d in r['duals'] if F(d['value']) is not None], key=lambda v:-sg*v)
    third=ds[2] if len(ds)>=3 else None
    allp=[F(p['value']) for p in r['points'] if F(p['value']) is not None]
    worstp=min(allp,key=lambda v:sg*v) if allp else None
    cand = third
    if cand is not None and worstp is not None and sg*(cand-worstp)>0: cand=worstp
    tol=Fraction(6,10**9)*max(1,abs(bd))
    if cand is None: c['<3 duals']+=1; continue
    if abs(cand-bd)<=tol: c['= min(third, worst point)']+=1
    elif abs(third-bd)<=tol: c['= third']+=1
    else: c['other']+=1; ex.append((n,s['=bestdual='],[str(float(v)) for v in ds[:4]],str(float(worstp)) if worstp is not None else None))
print(c); print(ex[:15])
