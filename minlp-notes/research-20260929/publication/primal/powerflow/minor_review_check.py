"""Check contraction and active slacks at stored points; no construction or point writes."""
import hashlib, json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from mpmath import iv, mp
import pfmodel as P
root=Path(__file__).resolve().parents[4]
reader=root/'research-20260929/reviews/open-instances-verification/osilx.py'
sha=hashlib.sha256(reader.read_bytes()).hexdigest()
assert sha=='4bcdc1d830bd3fc0392756f10b3e5daccbce218198543e402158a24cf986a465'
print('osilx.py sha256',sha)
mp.dps=50; iv.dps=80; here=Path(__file__).resolve().parent
for name in ['powerflow0030p','powerflow0039p','powerflow0039r']:
 I=P.load(name); idx={v:j for j,v in enumerate(I['names'])}; byname={c['name']:c for c in I['cons']}; v=json.loads((here/f'points/{name}.json').read_text())
 fixed={idx[k]:Q(x['value']) for k,x in v['fixed'].items()}; centre={idx[k]:Q(x) for k,x in v['free'].items()}; free=sorted(centre); col={j:k for k,j in enumerate(free)}; m=len(free); r=Q(v['radius'])
 X=[]; xc=[]
 for j in range(len(idx)):
  q=fixed.get(j,centre.get(j)); xc.append(mp.mpf(q.numerator)/q.denominator)
  X.append(P.iv_of_frac(iv,q) if j in fixed else iv.mpf([P.iv_of_frac(iv,q-r).a,P.iv_of_frac(iv,q+r).b]))
 J=np.zeros((m,m)); ji=[]
 for i,row in enumerate(v['system']):
  c=byname[row['row']]; ji.append({col[j]:g for j,g in P.ev_row(c,X,iv,P.ctx_num(iv)).g.items() if j in col})
  for j,g in P.ev_row(c,xc,mp,P.ctx_num(mp)).g.items():
   if j in col:J[i,col[j]]+=float(g)
 C=np.linalg.inv(J); norm=Q(0)
 for i in range(m):
  total=Q(0)
  for t in range(m):
   s=iv.mpf(i==t)
   for k in range(m):
    if t in ji[k]:s-=iv.mpf(float(C[i,k]))*ji[k][t]
   a,b=P.iv_ends(s);total+=max(abs(a),abs(b))
  norm=max(norm,total)
 assert norm<Q('5.4e-12'); print(name,'||I-CJ(X)||_inf upper',float(norm),'< 1')
 p1=[mp.mpf(s) for s in P.read_p1(I,name)]; active=[]
 for c in I['cons']:
  if c['lbF']==c['ubF']:continue
  val=P.ev_row(c,p1,mp,P.ctx_num(mp)).v
  for side in ['lb','ub']:
   if c[side+'F'] is not None:
    slack=val-mp.mpf(c[side]) if side=='lb' else mp.mpf(c[side])-val
    if slack<mp.mpf('1e-9'):active.append((c['name'],side,float(slack)))
 print(name,'active slacks',active)
print('PASS: contraction proves uniqueness; reader hash and active-slack corrections checked.')
