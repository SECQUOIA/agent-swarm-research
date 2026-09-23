"""Independent exact LP dual bounds for all words/time cells of the instance.
HiGHS selects a dual support; rational linear algebra verifies every resulting
certificate. No numerical objective or tolerance establishes the lower bound.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json
import numpy as np
from scipy.optimize import linprog
import sympy as sp
OUT=Path(__file__).resolve().parent
SNAP=OUT.parents[2]/'process/snapshots/stage02-round02'
records=json.loads((SNAP/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((SNAP/p).read_bytes()).hexdigest()==v for p,v in records.items())
prev=SNAP.parent/'stage02-round01'
old=json.loads((prev/'snapshot-manifest.json').read_text())
assert records['verification/reference/verify_general_four_block.py']==old['verification/reference/verify_general_four_block.py']
assert records['verification/reference/certificates_general_four_block.json']==old['verification/reference/certificates_general_four_block.json']
raw=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[(F(r[0],146),tuple(F(x,146) for x in r[1:])) for r in raw]
L=F(57,8);tstar,m=knots[-1];terminal=tuple(a+(L-tstar)/3 for a in m);knots.append((L,terminal))
segments=[]
for (a,aa),(b,bb) in zip(knots,knots[1:]):
 slope=[(v-u)/(b-a) for u,v in zip(aa,bb)];intercept=[u-s*a for u,s in zip(aa,slope)]
 assert all(F(0)<=s<=F(3,4) for s in slope) and sum(slope)==1
 segments.append((a,b,slope,intercept))
E=F(18673,18396);delta=E-1
assert delta==F(277,18396) and L-tstar==F(63,2)*delta

def cum(t):
 for a,b,slope,intercept in segments:
  if a<=t<=b:return tuple(s*t+c for s,c in zip(slope,intercept))
 raise ValueError(t)

# Build the original one-sided discrepancy at u,v,L, all coordinates.
# Include complete cell bounds so every LP is bounded in u,v.
certs=[];minimum=None;minword=None;minpoint=None
for word in product(range(3),repeat=3):
 for j,first in enumerate(segments):
  for ell in range(j,len(segments)):
   second=segments[ell]
   a,b,mu,bu=first;c,d,mv,bv=second
   rows=[[F(-1),0,0],[F(1),0,0],[0,F(-1),0],[0,F(1),0],[1,-1,0],[0,0,-1]]
   rhs=[-a,b,-c,d,0,0]
   for i in range(3):
    q0,q1,q2=[int(p==i) for p in word]
    rows.extend([[q0-mu[i],0,-1],[q0-q1,q1-mv[i],-1],[q0-q1,q1-q2,-1]])
    rhs.extend([bu[i],bv[i],terminal[i]-q2*L])
   sol=linprog([0,0,1],A_ub=np.array(rows,float),b_ub=np.array(rhs,float),bounds=[(None,None)]*3,method='highs')
   assert sol.success
   support=[i for i,v in enumerate(sol.ineqlin.marginals) if abs(v)>1e-8]
   matrix=sp.Matrix([[sp.Rational(rows[i][j]) for i in support] for j in range(3)])
   multipliers,params=matrix.gauss_jordan_solve(sp.Matrix([0,0,1]))
   assert params.rows==0
   assert all(y<=0 for y in multipliers)
   assert matrix*multipliers==sp.Matrix([0,0,1])
   lower=sum(sp.Rational(rhs[i])*y for i,y in zip(support,multipliers))
   assert lower>=sp.Rational(E)
   certs.append({'word':word,'cells':[j,ell],'support':support,'multipliers':list(map(str,multipliers)),'lower':str(lower)})
   if minimum is None or lower<minimum:
    minimum=lower;minword=word
assert minimum==sp.Rational(E)
# Check the manuscript witness independently on all relevant time boundaries.
u=F(8341,4599);v=F(17639,4599)
values=[]
for t in sorted(set([p for p,_ in knots]+[u,v])):
 w=[min(t,u),max(F(0),t-v),max(F(0),min(t,v)-u)]
 values.extend(q-a for q,a in zip(w,cum(t)))
assert max(values)==E
assert u-cum(u)[0]==E and v-u-cum(v)[2]==E and L-v-terminal[1]==E
assert E/L==F(37346,262143)>F(8,57)
# All arithmetic premises of the manuscript's repeated-word exclusion.
R=[F(128,73),F(97,73),F(1)];M=[F(204,73),F(258,73),F(290,73)]
assert terminal[0]>2*E and terminal[1]>2*E and M[2]+20*delta<L
for p,gap in ((0,F(2923,4599)),(1,F(4372,4599))):
 assert L-terminal[p]-E-(M[2]-R[p]+16*delta)==gap>0
for i in range(3):assert L-terminal[i]==M[i]+1+21*delta
assert u==R[0]+4*delta and v==M[1]+20*delta
assert F(256,146)<=u<=F(408,146) and F(516,146)<=v<=F(580,146)
(OUT/'exact-duals.json').write_text(json.dumps(certs,indent=2)+'\n')
result={'snapshot_hashes':len(records),'exact_word_cell_dual_certificates':len(certs),'minimum_exact':str(minimum),'witness_word':[0,2,1],'witness_times':[str(u),str(v)],'witness_error':str(max(values)),'scaled_coefficient':str(E/L)}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
