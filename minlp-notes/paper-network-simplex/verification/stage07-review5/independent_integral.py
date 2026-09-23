from fractions import Fraction as F
from functools import lru_cache
from collections import defaultdict
import json,random
import sympy as sp
rng=random.Random(7505)
counts=dict(networks=0,normalized_flows=0,refined_graph_mixtures=0,terminal_integral_flows=0)
for case in range(20):
 arcs=[(0,1),(1,2),(2,0),(0,1),(2,2),(1,0)]
 arcs=[(v,u) if rng.randrange(2) else (u,v) for u,v in arcs]
 E=len(arcs);A=sp.zeros(4,E)
 for e,(u,v) in enumerate(arcs):A[u,e]-=1;A[v,e]+=1
 capacities=tuple(F(2) for _ in arcs);base=tuple(F(1) for _ in arcs);b=tuple(A*sp.Matrix(base));kernel=A.nullspace()
 @lru_cache(None)
 def refine(x):
  noninteger=[e for e in range(E) if x[e].denominator!=1]
  if not noninteger:
   counts['terminal_integral_flows']+=1
   assert tuple(A*sp.Matrix(x))==b
   return ((F(1),x),)
  directions=A[:,noninteger].nullspace();assert directions
  d=[F(0)]*E
  for e,k in zip(noninteger,directions[0]):d[e]=F(k)
  plus=min((capacities[e]-x[e])/d[e] if d[e]>0 else -x[e]/d[e] for e in noninteger if d[e])
  minus=min(x[e]/d[e] if d[e]>0 else (x[e]-capacities[e])/d[e] for e in noninteger if d[e])
  assert plus>0 and minus>0
  xp=tuple(x[e]+plus*d[e] for e in range(E));xm=tuple(x[e]-minus*d[e] for e in range(E))
  assert sum(k.denominator!=1 for k in xp)<len(noninteger)
  assert sum(k.denominator!=1 for k in xm)<len(noninteger)
  result=defaultdict(F)
  for weight,point in refine(xp):result[point]+=minus/(minus+plus)*weight
  for weight,point in refine(xm):result[point]+=plus/(minus+plus)*weight
  return tuple((weight,point) for point,weight in result.items())
 states=[]
 for j in range(4):
  x=list(base)
  for d in kernel:
   scale=F(rng.randrange(-2,3),12)
   x=[value+scale*F(k) for value,k in zip(x,d)]
  x=tuple(x);assert all(0<=value<=2 for value in x)
  terms=refine(x);assert sum(w for w,p in terms)==1
  assert all(x[e]==sum(w*p[e] for w,p in terms) for e in range(E))
  states.append((x,terms));counts['normalized_flows']+=1
 for m in (0,1,3):
  weights=([F(1)] if m==0 else [F(1,3),F(2,3)] if m==1 else [F(1,4),F(0),F(1,4),F(1,2)])
  obs=[(e,j) for e in range(E) for j in range(m) if rng.randrange(2)]
  x=[sum(weights[j]*states[j][0][e] for j in range(m+1)) for e in range(E)]
  z={(e,j):weights[j]*states[j][0][e] for e,j in obs}
  terms=[(weights[j]*w,j,p) for j in range(m+1) for w,p in states[j][1] if weights[j]]
  assert sum(w for w,j,p in terms)==1
  assert all(x[e]==sum(w*p[e] for w,j,p in terms) for e in range(E))
  assert all(weights[j]==sum(w for w,k,p in terms if j==k) for j in range(m))
  assert all(z[e,j]==sum(w*p[e] for w,k,p in terms if j==k) for e,j in obs)
  counts['refined_graph_mixtures']+=1
 counts['networks']+=1
print(json.dumps(dict(status='PASS',arithmetic='Exact Fraction and SymPy; no production code or LP',counts=counts),indent=2))
