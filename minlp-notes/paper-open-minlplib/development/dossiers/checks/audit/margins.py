# Exact margins of the class (i) and (i-r) pairs from the audit's results.json (read-only copy).
import json
from fractions import Fraction as F
from decimal import Decimal as D
R=json.load(open('results.json'))
rows={}
for x in R:
    if not (x['cls'].startswith('(i)') or x['cls'].startswith('(i-r)')): continue
    d=F(D(x['d_listed'])); hi=F(D(x['obj_hi'])); m=d-hi
    s=x['d_listed']; dec=len(s.split('.')[1]) if '.' in s else 0
    unit=F(1,10**dec); key=(x['name'],x['solver'])
    if key not in rows or m>rows[key][0]: rows[key]=(m,x,unit)
for (n,sv),(m,x,unit) in sorted(rows.items(), key=lambda t:-float(t[1][0]/abs(F(D(t[1][1]['d_listed']))))):
    d=F(D(x['d_listed']))
    print(f"{n:28s} {sv:8s} {x['point']} d={x['d_listed']} f_hi={float(F(D(x['obj_hi']))):.13g} d-f={float(m):.4g} rel={float(m/abs(d)):.3g} m/slack={float(m/F(x['d_slack'])):.3g} m/unit={float(m/unit):.4g} {x['cls'][:5]} {x.get('i_group','')}")
