from fractions import Fraction as Q
from itertools import product, combinations
from math import comb
import json
from pathlib import Path

def choose(k,j): return comb(k,j) if 0<=j<=k else 0

def moments(p, N):
 d=len(p); C=[Q(0)]*(d+2); P=C.copy(); O=C.copy()
 for bits in product((0,1),repeat=d):
  mass=Q(1)
  for x,b in zip(p,bits): mass*=x if b else 1-x
  for j in range(d+2): P[j]+=mass*choose(sum(bits),j)
 cuts=sorted(set([Q(0),Q(1),*p,*[1-x for x in p]]))
 patterns=list(combinations(range(N),N//2))
 for a,b in zip(cuts,cuts[1:]):
  t=(a+b)/2
  kc=sum(t<x for x in p)
  for j in range(d+2): C[j]+=(b-a)*choose(kc,j)
  for pat in patterns:
   ko=sum((t<x if i in pat else t>1-x) for i,x in enumerate(p))
   for j in range(d+2): O[j]+=(b-a)*choose(ko,j)/len(patterns)
 s=sum(p); k=s.numerator//s.denominator; theta=s-k
 V=[(1-theta)*choose(k,j)+theta*choose(k+1,j) for j in range(d+2)]
 return C,P,O,V

checks=0
for N in range(2,6):
 beta=Q(N*(N-1),2*(N//2)*(N-N//2))
 for d in range(1,N+1):
  for p in product([Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)],repeat=d):
   # Exchangeability makes sorted vectors exhaustive for these moments.
   if tuple(sorted(p))!=p: continue
   C,P,O,V=moments(p,N)
   for j in range(d+2):
    prev=C[j-1]-P[j-1] if j else 0
    assert beta*(C[j]-O[j])+prev-(P[j]-V[j])>=0,(N,p,j)
    checks+=1

# Exhaustive combinatorial theorem check on all connected bipartite atlas graphs <=7 vertices.
import networkx as nx
from functools import lru_cache
@lru_cache(None)
def width2(adj):
 n=len(adj)
 if n<=3:return True
 for v in range(n):
  neigh=[i for i in range(n) if adj[v]>>i&1]
  if len(neigh)>2:continue
  rest=[i for i in range(n) if i!=v]; new=[]
  for i in rest:
   row=adj[i]
   if i in neigh:
    for j in neigh:
     if j!=i:row|=1<<j
   new.append(sum((1<<k) for k,j in enumerate(rest) if row>>j&1))
  if width2(tuple(new)):return True
 return False

def all_bad_factor_sets(G,F):
 bad=set()
 # DFS each simple cycle, with its smallest vertex as start; keep both directions harmlessly.
 for start in G:
  def dfs(path):
   for v in G[path[-1]]:
    if v==start and len(path)>=4:
     fs=frozenset(set(path)&F)
     if len(fs)%2:bad.add(fs)
    elif v>start and v not in path:dfs(path+[v])
  dfs([start])
 return bad
ng=nc=0
for G in nx.graph_atlas_g():
 if len(G)==0 or not nx.is_connected(G) or not nx.is_bipartite(G):continue
 adj=tuple(sum(1<<j for j in G[i]) for i in G)
 if not width2(adj):continue
 color=nx.bipartite.color(G)
 for side in (0,1):
  F={v for v in G if color[v]==side}; factors=list(F)
  bad=all_bad_factor_sets(G,F)
  feasible=False
  for bits in product((0,1),repeat=len(factors)):
   c=dict(zip(factors,bits))
   if all(len({c[v] for v in fs})==2 for fs in bad):feasible=True;break
  assert feasible,(G.edges(),F)
  nc+=1
 ng+=1
result={'arithmetic':'exact Fraction and integer graph enumeration','spreading_coefficient_checks':checks,'connected_bipartite_atlas_width2_graphs':ng,'factor_side_colorings':nc,'scope':'N<=5, quarter-grid sorted means, every support size; connected atlas graphs <=7 vertices, both factor-side choices. Finite checks do not prove universal theorems.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
