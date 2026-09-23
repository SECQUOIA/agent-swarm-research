from fractions import Fraction as F
from itertools import product
from pathlib import Path
import random,json
import numpy as np
from scipy.optimize import linprog
from network_simplex import Point
from network_simplex.flat_chain import FlatChainSimplex
rng=random.Random(6505)
feasible=outside=vertex_evaluations=0
for trial in range(48):
 L=1+trial%3;m=7+trial%5;a=trial%4
 labels=sorted(rng.sample(range(m),a))
 obs=[(e,j) for e in range(2*L+1) for j in labels if rng.random()<.45]
 obs=sorted(set(obs)|{(2*L,j) for j in labels})
 raw=[rng.randint(0,4) for _ in range(m+1)]
 if trial%3==0:raw[-1]=0
 if not sum(raw):raw[-1]=1
 weights=tuple(F(v,sum(raw)) for v in raw)
 flows=[]
 for j in range(m+1):
  branch=F(rng.randint(0,7),7);flow=[]
  for i in range(L):
   first=branch*F(rng.randint(0,5),5);flow += [first,branch-first]
  flows.append(tuple(flow+[1-branch]))
 x=tuple(sum(weights[j]*flows[j][e] for j in range(m+1)) for e in range(2*L+1))
 z={(e,j):weights[j]*flows[j][e] for e,j in obs}
 paths=[(F(0),)*(2*L)+(F(1),)]
 for choices in product((0,1),repeat=L):
  paths.append(tuple(F(e%2==choices[e//2]) for e in range(2*L))+(F(0),))
 vertices=[]
 for path in paths:
  for j in range(m+1):
   y=tuple(F(k==j) for k in range(m));vertices.append(Point(path,y,{(e,k):path[e]*y[k] for e,k in obs}))
 A=np.asarray([(1,)+v.x+v.y+tuple(v.z[o] for o in obs) for v in vertices],float).T
 model=FlatChainSimplex(L,m,obs)
 for perturb in (False,True):
  zz=dict(z)
  if perturb and obs:
   key=rng.choice(obs);zz[key]+=rng.choice([-1,1])*F(1,37)
  p=Point(x,weights[:-1],zz);target=np.asarray((1,)+p.x+p.y+tuple(p.z[o] for o in obs),float)
  numerical=linprog(np.zeros(len(vertices)),A_eq=A,b_eq=target,bounds=(0,None),method='highs')
  assert numerical.status in (0,2)
  ans=model.separate(p)
  assert ans.feasible==(numerical.status==0)
  if ans.feasible:
   d=ans.decomposition;assert d.weights==weights
   reconstructed={j:d.flow(j) for j in d.positive_states()}
   for j,f in reconstructed.items():
    assert all(0<=v<=1 for v in f)
    assert all(f[2*i]+f[2*i+1]+f[-1]==1 for i in range(L))
   assert tuple(sum(weights[j]*f[e] for j,f in reconstructed.items()) for e in range(2*L+1))==x
   for (e,j),v in zz.items():assert v==(weights[j]*reconstructed[j][e] if weights[j] else 0)
   assert len(d.group_profile)==a+1
   feasible+=1
  else:
   assert ans.cut.evaluate(p)>0
   assert all(abs(v)<=1 for key,v in ans.cut.coefficients.items() if key[0] in ('x','z'))
   for vertex in vertices:assert ans.cut.evaluate(vertex)<=0
   vertex_evaluations+=len(vertices);outside+=1
out={'numerical_vertex_hull_comparisons':feasible+outside,'exact_decompositions':feasible,'exact_valid_violated_cuts':outside,'exact_vertex_cut_evaluations':vertex_evaluations,'observed_labels':[0,1,2,3],'original_labels':[7,8,9,10,11],'status':'PASS'}
print(json.dumps(out,indent=2))
