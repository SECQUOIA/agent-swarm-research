"""Check two Krawczyk steps on stored boxes, without construction or point writes.
Also save the old-vector comparison using exact binary64 values and stored enclosures.
"""
import json
from fractions import Fraction as Q
from pathlib import Path
import lnts_primal as L
from mpmath import iv, mp
p=Path(__file__).resolve().parent
mp.dps=L.DPS; iv.dps=L.DPS
for n in [50,100,200,400]:
 v=json.loads((p/f'points/lnts{n}_point.json').read_text())
 th=[L.to_iv(Q(s)) for s in v['fixed_controls'].values()]
 z=[Q(x['centre']) for x in v['unknowns_box'].values()]; r=[Q(x['radius']) for x in v['unknowns_box'].values()]
 X=[L.hull(L.to_iv(z[k]-r[k]),L.to_iv(z[k]+r[k])) for k in range(3)]; Y=[L.to_iv(q) for q in z]
 K=L.krawczyk(th,Y,X); assert all(L.ends(X[k])[0]<L.ends(K[k])[0] and L.ends(K[k])[1]<L.ends(X[k])[1] for k in range(3))
 Z=[L.meet(K[k],X[k]) for k in range(3)]
 old_inside=all(L.ends(Z[k])[0]<=z[k]<=L.ends(Z[k])[1] for k in range(3))
 Y2=[iv.mpf(a.mid) for a in Z]; assert all(L.ends(Z[k])[0]<=L.ends(Y2[k])[0]<=L.ends(Y2[k])[1]<=L.ends(Z[k])[1] for k in range(3))
 Z2=[L.meet(a,b) for a,b in zip(L.krawczyk(th,Y2,Z),Z)]
 widths=[b-a for a,b in map(L.ends,Z2)]; ow=n*widths[2]
 assert max(widths)<Q('2.1e-106') and ow<Q('3e-109')
 print(n,'old centre inside step-1 box:',old_inside,'new centre inside:',True,'widths',[float(x) for x in widths],'objective width',float(ow))
 assert Q(v['objective_enclosure'][0])<=n*L.ends(Z2[2])[0] and n*L.ends(Z2[2])[1]<=Q(v['objective_enclosure'][1])
 old=[Q(float(s)) for s in (p.parents[2]/f'open-instances/logs/lnts_lnts{n}_primal.txt').read_text().split()]
 enc=[(Q(a),Q(b)) for _,a,b in v['enclosures']]; assert len(old)==len(enc)
 distances=[max(abs(o-a),abs(o-b)) for o,(a,b) in zip(old,enc)]
 same=sum(float(a)==float(b)==float(o) for o,(a,b) in zip(old,enc))
 print(n,'old-vector max distance upper',float(max(distances)),'index',distances.index(max(distances))+1,'identical roundings',same,'/',len(old))
 middle=Q(v['fixed_controls'][f'x{n//2+1}']); assert abs(middle)<Q('1e-110'); print(n,'middle stored rational:',float(middle))
print('PASS: valid midpoint step, unchanged objective displays, and saved old-vector comparison.')
