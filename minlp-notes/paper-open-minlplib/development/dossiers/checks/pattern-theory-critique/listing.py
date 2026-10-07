# pattern-theory critique check (2026-10-04). Run from a scratch dir holding copies of the inputs
# (pages.json, fetched.json, candidates.json, census_merged.json from research-20260929; OSIL from ~/.cache/minlplib).
import json, math
from decimal import Decimal as D
P=json.load(open('pages.json'))
def dec(x):
    try:
        v=D(str(x).strip()); return v
    except Exception: return None
tot=ok_exact=ok_round=ok_1e4=0; bad=[]
maxrel=[]
for r in P:
    ld=dec(r['listing_dual'])
    if ld is None or not ld.is_finite(): continue
    vals=[dec(d['value']) for d in r['duals']]
    fin=[v for v in vals if v is not None and v.is_finite()]
    if len(fin)<3: continue
    tot+=1
    # sort with inf counted
    allv=[v for v in vals if v is not None]
    if r['sense']=='min': allv.sort(reverse=True)
    else: allv.sort()
    fin.sort(reverse=(r['sense']=='min'))
    d3=fin[2]; d3i=allv[2]
    # display rounding: round d3 to the number of decimals shown in ld
    exp=ld.as_tuple().exponent
    q=D(1).scaleb(exp)
    def match(x):
        if not x.is_finite(): return False
        return abs(x-ld) <= q/2 + D('1e-30')
    if ld==d3: ok_exact+=1
    if match(d3): ok_round+=1
    elif match(d3i): bad.append((r['name'],'matches with inf counted'))
    else:
        rel=abs(float(ld-d3))/max(1,abs(float(d3)))
        bad.append((r['name'],str(ld),str(d3),str(d3i),rel))
print('instances',tot,'exact',ok_exact,'within display half-unit',ok_round)
print(len(bad))
for b in bad[:40]: print(b)
