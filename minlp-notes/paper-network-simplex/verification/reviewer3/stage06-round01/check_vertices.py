from fractions import Fraction as F
from itertools import product
import json,random
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from network_simplex import Point
from network_simplex.flat_chain import FlatChainSimplex
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import membership_ef,optimize_ef,optimize_independent_states
rng=random.Random(619832); counts=dict(models=0,membership_comparisons=0,exact_decompositions=0,exact_cut_vertices=0,optimization_comparisons=0)
for test in range(100):
 L=1+test%4; m=(0,1,2,3,4,8)[test%6]; labels=rng.sample(range(m),min(m,3 if m==8 else m))
 obs=[(e,j) for e in range(2*L+1) for j in labels if rng.randrange(5)<3]
 model=FlatChainSimplex(L,m,obs); obs=list(model.observations); E=2*L+1;n=E+m+len(obs)
 paths=[tuple([0]*(2*L)+[1])]+[tuple(int(e%2==bits[e//2]) for e in range(2*L))+(0,) for bits in product((0,1),repeat=L)]
 vertices=[]
 for state in range(m+1):
  for p in paths:
   y=tuple(int(state==j) for j in range(m)); vertices.append(p+y+tuple(p[e]*y[j] for e,j in obs))
 V=np.array(vertices,dtype=float).T
 # Convex mixture explicitly includes boundary/zero weights on half the cases.
 picks=rng.sample(range(len(vertices)),min(len(vertices),1+test%7)); raw=[rng.randrange(1,8) for _ in picks]
 center=tuple(sum(F(w,sum(raw))*vertices[k][i] for k,w in zip(picks,raw)) for i in range(n))
 inst=Instance([(a,b,1) for a,b,_ in model.arcs],np.array([1]+[0]*(L-1)+[-1],dtype=float),m,obs,np.array(center[:E],float))
 for altered in (False,True):
  cand=list(center)
  if altered and obs: cand[E+m+rng.randrange(len(obs))]+=rng.choice((-1,1))*F(1,11)
  p=Point(cand[:E],cand[E:E+m],dict(zip(obs,cand[E+m:])))
  answer=model.separate(p); assert answer.feasible==model.separate(p,decompose=False).feasible
  direct=linprog(np.zeros(len(vertices)),A_eq=np.vstack((V,np.ones(len(vertices)))),b_eq=np.r_[np.array(cand,float),1.],bounds=(0,None),method='highs')
  assert direct.status in (0,2); assert answer.feasible==(direct.status==0),(test,cand)
  for merge in (False,True):
   for two in (False,True):
    other=membership_ef(inst,p.x,p.y,[p.z[o] for o in obs],merge=merge,two_state=two)
    assert other.status==direct.status,(test,merge,two); counts['membership_comparisons']+=1
  if answer.feasible:
   dec=answer.decomposition; assert dec.weights==p.y+(1-sum(p.y),)
   flows={j:dec.flow(j) for j in dec.positive_states()}
   for j,f in flows.items():
    assert all(0<=a<=1 for a in f)
    assert all(f[2*i]+f[2*i+1]+f[-1]==1 for i in range(L))
   assert all(sum(dec.weights[j]*f[e] for j,f in flows.items())==p.x[e] for e in range(E))
   assert all((dec.weights[j]*flows[j][e] if j in flows else 0)==p.z[e,j] for e,j in obs)
   counts['exact_decompositions']+=1
  else:
   cut=answer.cut;assert cut.evaluate(p)>0
   if len(model.labels)<=3:assert all(abs(v)<=1 for k,v in cut.coefficients.items() if k[0] in ('x','z'))
   for v in vertices:
    assert cut.evaluate(Point(v[:E],v[E:E+m],dict(zip(obs,v[E+m:]))))<=0
    counts['exact_cut_vertices']+=1
 if test<60:
  c=np.array([rng.randrange(-5,6) for i in range(n)],float)
  for coupled in (False,True):
   rows=[]
   if coupled:
    for k in range(3):
     coef=np.array([rng.randrange(-3,4) for i in range(n)],float)
     rhs=sum(F(int(a))*b for a,b in zip(coef,center))+F(rng.randrange(3),4)
     rows.append((coef,rhs))
   for fixed in (None,center[E:E+m]):
    ae=np.ones((1,len(vertices))); be=np.ones(1)
    if fixed is not None:
     ae=np.vstack((ae,V[E:E+m])); be=np.r_[be,np.array(fixed,float)]
    au=np.array([a@V for a,b in rows]) if rows else None;bu=np.array([float(b) for a,b in rows]) if rows else None
    direct=linprog(c@V,A_eq=ae,b_eq=be,A_ub=au,b_ub=bu,bounds=(0,None),method='highs');assert direct.status==0
    for merge in (False,True):
     other=optimize_ef(inst,c,y_fixed=fixed,merge=merge,extra_rows=rows)
     assert other.status==0 and abs(other.fun-direct.fun)<1e-7,(test,coupled,fixed,merge,other.fun,direct.fun)
     assert abs(c@other.original_point-other.fun)<1e-7
     counts['optimization_comparisons']+=1
    if fixed is not None and not coupled:
     other=optimize_independent_states(inst,c,fixed); assert other.status==0 and abs(other.fun-direct.fun)<1e-7
     counts['optimization_comparisons']+=1
 counts['models']+=1
Path('paper-network-simplex/verification/reviewer3/stage06-round01/vertex-checks.json').write_text(json.dumps(counts,indent=2)+'\n'); print(counts)
