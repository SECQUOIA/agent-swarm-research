"""Exact incidence-based construction, elimination and completion checks.
No production or previous verification program is imported.
"""
from itertools import combinations
from pathlib import Path
import sympy as S
import json

graphs=[('K4',4,list(combinations(range(4),2))),('parallel',2,[(0,1)]*4),('articulation-loop-bridge',6,[(0,1),(1,2),(2,0),(2,3),(3,4),(4,2),(4,4),(4,5)]),('disconnected',5,[(0,1),(0,1),(2,3),(3,3)])]
counts=dict(oriented_graphs=0,cycle_minors=0,observation_sets=0,pivots=0,completion_sets=0)
for name,n,edges in graphs:
 for mask in sorted({0,(1<<len(edges))-1,sum(1<<i for i in range(0,len(edges),2)),1}):
  arcs=[(b,a) if mask>>i&1 else (a,b) for i,(a,b) in enumerate(edges)]
  A=S.zeros(n,len(arcs))
  for e,(a,b) in enumerate(arcs): A[a,e]-=1; A[b,e]+=1
  null=A.nullspace(); C=S.Matrix.hstack(*null); r=C.cols
  assert A*C==S.zeros(n,r)
  for k in range(1,r+1):
   for rows in combinations(range(C.rows),k):
    for cols in combinations(range(r),k):
     assert C.extract(rows,cols).det() in (-1,0,1); counts['cycle_minors']+=1
  for observed in range(1<<len(arcs)):
   O=[i for i in range(len(arcs)) if observed>>i&1]; U=[i for i in range(len(arcs)) if i not in O]
   d=C[O,:].rank(); rho=len(U)-A[:,U].rank(); assert r-d==rho
   independent=list(C[O,:].T.rref()[1]); D=C[[O[i] for i in independent],:]
   for I in combinations(range(r),d):
    B=D[:,I]
    if B.det()==0: continue
    F=[j for j in range(r) if j not in I]; W=C[:,I]*B.inv(); R=C[:,F]-W*D[:,F]
    assert all(v in (-1,0,1) for v in W) and all(v in (-1,0,1) for v in R)
    assert W*D[:,I]==C[:,I]
    counts['pivots']+=1
   forest=list(A[:,U].rref()[1]); added=[e for i,e in enumerate(U) if i not in forest]
   assert len(added)==rho and C[O+added,:].rank()==r
   counts['observation_sets']+=1; counts['completion_sets']+=1
  counts['oriented_graphs']+=1
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n'); print(json.dumps(counts,indent=2))
