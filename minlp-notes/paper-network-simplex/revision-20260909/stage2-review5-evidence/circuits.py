"""Independent exact nullspace enumeration of the three-label normal universe."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd,lcm
from functools import reduce
from pathlib import Path
import json
m=3
normals=sorted({tuple(int(mask>>i&1) for i in range(m)) for mask in range(1,1<<m)}|{tuple(-int(i==j) for i in range(m)) for j in range(m)}|{(-1,)*m})
def kernel(rows):
 A=[[F(r[i]) for r in rows] for i in range(m)];n=len(rows);pivots=[];rank=0
 for col in range(n):
  index=next((k for k in range(rank,m) if A[k][col]),None)
  if index is None:continue
  A[rank],A[index]=A[index],A[rank]
  z=A[rank][col];A[rank]=[x/z for x in A[rank]]
  for k in range(m):
   if k!=rank:
    z=A[k][col];A[k]=[x-z*y for x,y in zip(A[k],A[rank])]
  pivots.append(col);rank+=1
 if n-rank!=1:return None
 free=next(i for i in range(n) if i not in pivots);v=[F(0)]*n;v[free]=1
 for k,col in enumerate(pivots):v[col]=-A[k][free]
 if not all(v):return None
 if all(x<0 for x in v):v=[-x for x in v]
 if not all(x>0 for x in v):return None
 den=reduce(lcm,[x.denominator for x in v],1);iv=[int(x*den) for x in v];g=reduce(gcd,iv)
 return tuple(x//g for x in iv)
found=[]
for size in range(2,5):
 for rows in combinations(normals,size):
  w=kernel(rows)
  if w is not None:found.append((rows,w))
assert len(found)==16
families=[0,0,0,0]
for rows,w in found:
 d=dict(zip(rows,w));full=(-1,-1,-1)
 if full not in d:family=0
 elif any(sum(a)==-1 for a in rows):family=2
 elif d[full]==2:family=3
 else:family=1
 families[family]+=1
 assert max(w)<=2
 if max(w)==2:assert d[full]==2
 # The occurrence exclusions used for original product coefficients.
 for j in range(3):
  neg=tuple(-int(i==j) for i in range(3));pos=tuple(int(i==j) for i in range(3))
  positives=[a for a in rows if min(a)>=0]
  if neg in d:assert all(a[j] for a in positives)
  if pos in d:assert all(a==pos or not a[j] for a in positives)
assert families==[7,5,3,1],families
report={'status':'PASS','normals':len(normals),'circuits':len(found),'family_counts':families,'product_occurrence_exclusions':'PASS','circuits_and_weights':found}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:v for k,v in report.items() if k!='circuits_and_weights'})
