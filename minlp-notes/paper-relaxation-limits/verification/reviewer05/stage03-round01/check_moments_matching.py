from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from random import Random
from pathlib import Path
import json
import networkx as nx
rng=Random(30501)
def choose(k,j):return comb(k,j) if 0<=j<=k else 0
def moments(p,N,fair=False):
 d=len(p);C=[Q(0)]*(d+2);P=C.copy();O=C.copy()
 def intlaw(coins):
  end=sorted({Q(0),Q(1),*p,*(1-x for x in p)})
  v=[Q(0)]*(d+2)
  for lo,hi in zip(end,end[1:]):
   t=(lo+hi)/2;K=sum(t<x if coins[i] else t>1-x for i,x in enumerate(p))
   for j in range(d+2):v[j]+=(hi-lo)*choose(K,j)
  return v
 C=intlaw([1]*d)
 for bits in product([0,1],repeat=d):
  prob=Q(1)
  for z,x in zip(bits,p):prob*=x if z else 1-x
  for j in range(d+2):P[j]+=prob*choose(sum(bits),j)
 coinslist=list(product([0,1],repeat=N)) if fair else [[int(i in S) for i in range(N)] for S in combinations(range(N),N//2)]
 for coins in coinslist:
  v=intlaw(coins)
  for j in range(d+2):O[j]+=v[j]/len(coinslist)
 s=sum(p);k=s.numerator//s.denominator;t=s-k
 V=[(1-t)*choose(k,j)+t*choose(k+1,j) for j in range(d+2)]
 return C,P,O,V
checks=0
for N in range(2,8):
 beta=Q(N*(N-1),2*(N//2)*(N-N//2))
 for _ in range(35):
  d=rng.randrange(1,N+1);p=[Q(rng.randrange(7),6) for i in range(d)]
  C,P,O,V=moments(p,N)
  F=[beta*(C[j]-O[j])+V[j]-P[j]+(C[j-1]-P[j-1] if j else 0) for j in range(d+2)]
  assert min(F)>=0
  L=Q(rng.randrange(5),2);a=[Q(rng.randrange(4)) for _ in range(min(d+1,3))]
  for j in range(3,d+1):a.append(a[-1]*L*Q(rng.randrange(5),4))
  assert sum(a[j]*(C[j]-V[j]) for j in range(d+1))<=sum(a[j]*((L+1)*(C[j]-P[j])+beta*(C[j]-O[j])) for j in range(d+1))
  checks+=1
for p,wanted in [([Q(2,5),Q(7,10),Q(24,25),Q(97,100)],Q(6201,12500)),([Q(2,5),Q(7,10),Q(959,1000),Q(971,1000)],Q(4961031,10000000))]:
 C,P,O,V=moments(p,4,True)
 assert 2*C[3]+V[3]-P[3]-2*O[3]+C[2]-P[2]==wanted
# Construct objective-specific gadget independently; compare exact optimum values.
for _ in range(100):
 n=rng.randrange(2,6);m=rng.randrange(1,8)
 edges=[tuple(rng.sample(range(n),2)) for i in range(m)]
 costs=[rng.randrange(-5,6) for i in edges]
 deg=[sum(v in e for e in edges) for v in range(n)]
 tables=[]
 for d in deg:
  inc=sorted(rng.randrange(-7,8) for i in range(d));T=[rng.randrange(-3,4)]
  for a in inc:T.append(T[-1]+a)
  tables.append(T)
 exact=min(sum(tables[v][sum(bits[i] for i,e in enumerate(edges) if v in e)] for v in range(n))+sum(c*z for c,z in zip(costs,bits)) for bits in product([0,1],repeat=m))
 G=nx.Graph()
 for i,(u,v) in enumerate(edges):
  G.add_edge(('e',i,0),('e',i,1),cost=0)
  for side,x in enumerate([u,v]):
   for j in range(deg[x]):G.add_edge(('e',i,side),('s',x,j),cost=tables[x][j+1]-tables[x][j]+(costs[i] if side==0 else 0))
 bonus=2*sum(abs(a['cost']) for u,v,a in G.edges(data=True))+1
 for u,v,a in G.edges(data=True):a['weight']=bonus*((u[0]=='e')+(v[0]=='e'))-a['cost']
 mat=nx.max_weight_matching(G)
 assert sum((u[0]=='e')+(v[0]=='e') for u,v in mat)==2*m
 got=sum(G[u][v]['cost'] for u,v in mat)+sum(T[0] for T in tables)
 assert got==exact
out={'exact_fixed_ambient_coefficient_and_regularity_cases':checks,'exact_arbitrary_spreading_values':'PASS','integer_matching_gadget_comparisons':100}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
