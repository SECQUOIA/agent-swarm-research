"""Check exact EF rows on known extensions; validate returned cuts independently."""
import sys,json,itertools,random
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'stage2-round1/code'))
from network_simplex_compressed.model import CompressedNetworkSimplex
from network_simplex_compressed.certificate import separate
from network_simplex import Point
rng=random.Random(909025)
counts={'models':0,'exact_extensions':0,'exact_model_rows':0,'nullity_counts':0,'exact_cut_vertex_checks':0}
statuses={}
def balance(edges,f,n):
 b=[0]*n
 for (u,v),a in zip(edges,f):b[u]-=a;b[v]+=a
 return tuple(b)
def cycle_rank(edges):
 nodes={v for e in edges for v in e};parent={v:v for v in nodes}
 def root(v):
  while parent[v]!=v:v=parent[v]
  return v
 for u,v in edges:parent[root(v)]=root(u)
 return len(edges)-len(nodes)+len({root(v) for v in nodes})
shapes=[(4,[(i,j) for i in range(4) for j in range(i+1,4)],(-1,0,0,1)),(6,[(i,j) for i in range(3) for j in range(3,6)],(-1,-1,-1,1,1,1)),(5,[(0,1),(0,1),(1,2),(2,2),(3,4),(3,4)],(-1,0,1,-1,1))]
for n,edges,b in shapes:
 integers=[f for f in itertools.product([0,1],repeat=len(edges)) if balance(edges,f,n)==b]
 assert integers
 vertices=[tuple(F(a,7) for a in f) for f in integers]
 arcs=[(u,v,F(1,7)) for u,v in edges];balances=tuple(F(a,7) for a in b)
 for trial in range(10):
  m=4;obs=[(e,j) for e in range(len(edges)) for j in [0,2,3] if rng.random()<.45]
  w=tuple(F(a,6) for a in [1,0,2,1,2])
  flows=[rng.choice(vertices) for _ in w]
  x=tuple(sum(a*f[e] for a,f in zip(w,flows)) for e in range(len(edges)))
  z={(e,j):w[j]*flows[j][e] for e,j in obs}
  point=Point(x,w[:-1],z)
  for eliminated in [False,True]:
   model=CompressedNetworkSimplex(arcs,balances,m,obs,eliminate_observed=eliminated);counts['models']+=1
   original=list(point.x)+list(point.y)+[point.z[o] for o in model.observations]
   old_n=model.n+model.eliminated_variables
   values=original+[F(0)]*(old_n-model.original_n)
   expected=0
   for block in model.blocks:
    for j in block.labels:
     for h,e in enumerate(block.chords):values[block.offsets[j]+h]=w[j]*(flows[j][e]-model.reference[e])
     unobserved=[edges[e] for e in block.edges if (e,j) not in point.z]
     expected+=cycle_rank(unobserved)
   if eliminated:
    vals=[None]*model.n
    for old,new in model.retained_variable_map.items():vals[new]=values[old]
    values=vals
    assert model.n-model.original_n==expected
    counts['nullity_counts']+=1
   for rows,equality in [(model.eq,True),(model.ub,False)]:
    for row,rhs in rows:
     lhs=sum(c*values[k] for k,c in row.items())
     assert lhs==rhs if equality else lhs<=rhs
     assert all(abs(c)<=1 for k,c in row.items() if not len(edges)<=k<len(edges)+m)
     counts['exact_model_rows']+=1
   for v,(lo,hi) in zip(values,model.bounds):assert (lo is None or lo<=v) and (hi is None or v<=hi)
   counts['exact_extensions']+=1
   if not z:continue
   zz=dict(z);key=rng.choice(list(z));zz[key]+=F(1,101)
   outside=Point(point.x,point.y,zz)
   result=separate(model,outside);statuses[result.status]=statuses.get(result.status,0)+1
   if result.status=='certified_outside':
    assert result.cut.evaluate(outside)>0
    for f in vertices:
     for j in range(m+1):
      y=tuple(F(k==j) for k in range(m))
      p=Point(f,y,{(e,k):f[e]*y[k] for e,k in model.observations})
      assert result.cut.evaluate(p)<=0
      counts['exact_cut_vertex_checks']+=1
report={'status':'PASS','counts':counts,'certificate_statuses':statuses,'note':'Numerically feasible status is not independently certified membership; returned cuts are checked exactly on all enumerated flow/simplex generators.'}
(ROOT/'stage2-review5-evidence/compressed_contracts.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
