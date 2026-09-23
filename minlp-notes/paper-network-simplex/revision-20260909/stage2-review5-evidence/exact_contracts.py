"""Finite exact contracts against independently enumerated integer flows.
No author verification imports and no floating-point oracle.
"""
import sys, json, random, itertools, hashlib
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
CODE=ROOT/'stage2-round1/code'
sys.path.insert(0,str(CODE))
from network_simplex import NetworkSimplex,Point
from network_simplex.flat_chain import FlatChainSimplex
rng=random.Random(219905)
counts=dict(models=0,queries=0,accepted=0,rejected=0,exact_vertex_cut_checks=0,zero_weight_queries=0,tiny_weight_queries=0)
reasons={}
def balance(arcs,f,n):
 b=[F(0)]*n
 for (u,v,_),a in zip(arcs,f): b[u]-=a;b[v]+=a
 return tuple(b)
def verify(model,point,vertices,n):
 result=model.separate(point)
 counts['queries']+=1
 weights=tuple(point.y)+(1-sum(point.y),)
 if not all(weights):counts['zero_weight_queries']+=1
 if any(0<w<F(1,10**20) for w in weights):counts['tiny_weight_queries']+=1
 assert model.separate(point,decompose=False).feasible==result.feasible
 if result.feasible:
  counts['accepted']+=1
  dec=result.decomposition
  assert tuple(dec.weights)==weights
  total=[F(0)]*len(model.arcs)
  for j,w in enumerate(weights):
   if not w: continue
   f=dec.flow(j)
   assert balance(model.arcs,f,n)==tuple(model.balances)
   assert all(0<=x<=cap for x,(_,_,cap) in zip(f,model.arcs))
   for e,x in enumerate(f):total[e]+=w*x
   for (e,k),z in point.z.items():
    if k==j:assert w*f[e]==z
  assert tuple(total)==tuple(point.x)
  assert all(z==0 for (e,j),z in point.z.items() if not weights[j])
 else:
  counts['rejected']+=1
  cut=result.cut
  assert cut.evaluate(point)>0
  assert all(abs(v)<=1 for k,v in cut.coefficients.items() if k[0] in ('x','z'))
  reasons[cut.reason]=reasons.get(cut.reason,0)+1
  for f in vertices:
   for j in range(model.simplex_size+1):
    y=tuple(F(k==j) for k in range(model.simplex_size))
    vertex=Point(f,y,{(e,k):f[e]*y[k] for e,k in model.observations})
    assert cut.evaluate(vertex)<=0,(cut,vertex)
    counts['exact_vertex_cut_checks']+=1

def queries(model,vertices,n):
 m=model.simplex_size
 for repeat in range(4):
  w=[rng.randrange(3) for _ in range(m+1)]
  if not any(w):w[-1]=1
  if repeat==3 and m:w=[10**40]+[1]*m
  w=tuple(F(a,sum(w)) for a in w)
  flows=[]
  for j in w:
   f,g=rng.choices(vertices,k=2)
   flows.append(tuple((2*a+b)/3 for a,b in zip(f,g)))
  x=tuple(sum(a*f[e] for a,f in zip(w,flows)) for e in range(len(model.arcs)))
  z={(e,j):w[j]*flows[j][e] for e,j in model.observations}
  p=Point(x,w[:-1],z);verify(model,p,vertices,n)
  if z:
   for sign in [-1,1]:
    zz=dict(z);key=rng.choice(list(z));zz[key]+=sign*F(1,101)
    verify(model,Point(x,w[:-1],zz),vertices,n)

shapes=[(2,[(0,1)]*k) for k in [2,3,4]]
shapes += [(5,[(0,1),(1,3),(0,2),(2,3),(0,3)]),(5,[(0,1),(0,1),(1,2),(1,2),(2,3),(3,3)]),(6,[(0,1)]*3+[(2,3)]*2+[(4,4)])]
for n,edges in shapes:
 for repeat in range(6):
  arcs=[(u,v,rng.choice([0,1,1])) if rng.randrange(2) else (v,u,rng.choice([0,1,1])) for u,v in edges]
  ref=tuple(F(rng.randrange(cap+1)) for _,_,cap in arcs)
  b=balance(arcs,ref,n)
  vertices=[tuple(map(F,f)) for f in itertools.product(*(range(c+1) for _,_,c in arcs)) if balance(arcs,f,n)==b]
  for m in [0,1,3,7]:
   labels=range(m) if m<7 else [1,5]
   obs=[(e,j) for e in range(len(arcs)) for j in labels if rng.random()<.55]
   model=NetworkSimplex(arcs,b,m,obs);counts['models']+=1
   queries(model,vertices,n)
for L in [1,2,3]:
 vertices=[tuple([F(0)]*(2*L)+[F(1)])]
 vertices += [tuple(F(e%2==choices[e//2]) for e in range(2*L))+(F(0),) for choices in itertools.product([0,1],repeat=L)]
 for m in [0,1,2,3,9]:
  labels=range(m) if m<9 else [1,5,8]
  for repeat in range(5):
   obs=[(e,j) for e in range(2*L+1) for j in labels if rng.random()<.55]
   model=FlatChainSimplex(L,m,obs);counts['models']+=1
   queries(model,vertices,L+1)
report={'counts':counts,'rejection_families':reasons,'status':'PASS','method':'Exact feasible decomposition or exact cut at every enumerated integral-flow/simplex point.','seed':219905}
(ROOT/'stage2-review5-evidence/exact_contracts.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
