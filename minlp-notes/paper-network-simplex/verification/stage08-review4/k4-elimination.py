import sympy as s
from itertools import combinations
from pathlib import Path
import json
C=s.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
edges=[(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]
A=s.zeros(4,6)
for k,(u,v) in enumerate(edges):A[u,k]=-1;A[v,k]=1
assert A*C==s.zeros(4,3)
minors=0
for k in range(1,4):
 for rows in combinations(range(6),k):
  for cols in combinations(range(3),k):
   assert C.extract(rows,cols).det() in (-1,0,1);minors+=1
pivots=0
for mask in range(64):
 obs=[i for i in range(6) if mask>>i&1];missing=[i for i in range(6) if not mask>>i&1]
 d=C.extract(obs,range(3)).rank();rho=len(missing)-A.extract(range(4),missing).rank()
 assert 3-d==rho
 for rows in combinations(obs,d):
  D=C.extract(rows,range(3))
  if D.rank()!=d:continue
  for cols in combinations(range(3),d):
   B=D.extract(range(d),cols)
   if B.det()==0:continue
   free=[i for i in range(3) if i not in cols]
   W=C.extract(range(6),cols)*B.inv();R=C.extract(range(6),free)-W*D.extract(range(d),free)
   assert all(v in (-1,0,1) for v in list(W)+list(R));pivots+=1
out={'TU_minors':minors,'observation_subsets':64,'valid_pivot_choices':pivots,'status':'PASS'}
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
