"""Exhaust all observation subsets and legal row/column pivots on K4."""
import itertools as it
import json
from pathlib import Path
import sympy as S
C=S.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
A=S.zeros(4,6)
for e,(a,b) in enumerate([(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]):A[a,e]=-1;A[b,e]=1
pivots=0
for bits in it.product((0,1),repeat=6):
 O=[e for e,v in enumerate(bits) if v]; U=[e for e,v in enumerate(bits) if not v]
 d=C[O,:].rank();rho=len(U)-A[:,U].rank()
 assert 3-d==rho
 possible=any(C[O+list(add),:].rank()==3 for add in it.combinations(U,rho))
 assert possible
 if rho:
  assert not any(C[O+list(add),:].rank()==3 for add in it.combinations(U,rho-1))
 for chosen in it.combinations(O,d):
  D=C[list(chosen),:]
  if D.rank()!=d:continue
  for I in it.combinations(range(3),d):
   F=[j for j in range(3) if j not in I]
   B=D[:,list(I)]
   if B.det()==0:continue
   for row in range(6):
    W=C[[row],list(I)]*B.inv()
    R=C[[row],F]-W*D[:,F]
    assert all(abs(x)<=1 for x in W) and all(abs(x)<=1 for x in R)
   pivots+=1
result=dict(observation_sets=64,legal_pivots=pivots,status='PASS')
Path(__file__).with_name('completion-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(result)
