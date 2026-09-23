"""Independent finite exact checks. These do not establish universal claims."""
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path
import json

def ff(v,a):
    z=Q(1)
    for j in range(a): z*=v-j
    return z

def mom(s,t,a): return ff(t,a)/ff(s,a)
counts={"gram_entries":0,"assignment_identities":0,"exact_psd_matrices":0,"clique_vertices":0}
for d in range(1,5):
 for s in range(4*d-2,4*d+4):
  if s<2*d: continue
  for j in range(4*(2*d-1),4*(s-2*d+1)+1):
   t=Q(j,4)
   for h in range(d+1):
    rhs=sum(Q(comb(h,a))*ff(t,2*d-a)*ff(s-t,a)/ff(s,2*d) for a in range(h+1))
    assert rhs==mom(s,t,2*d-h)
    counts["gram_entries"]+=1
   for a in range(2*d+1):
    for b in range(2*d+1-a):
     for c in range(2*d+1-a-b):
      lhs=sum((-1)**j*comb(b,j)*mom(s,t,a+c+j) for j in range(b+1))
      rhs=ff(t,a+c)*ff(s-t,b)/ff(s,a+b+c)
      assert lhs==rhs
      if c==0: assert rhs>=0
      counts["assignment_identities"]+=1

def psd(M):
 A=[list(row) for row in M]
 for i in range(len(A)):
  p=A[i][i]
  assert p>=0
  if p==0:
   assert all(A[i][j]==0 for j in range(i+1,len(A)))
  else:
   for j in range(i+1,len(A)):
    for k in range(j,len(A)):
     A[j][k]-=A[i][j]*A[i][k]/p
     A[k][j]=A[j][k]
 counts["exact_psd_matrices"]+=1

def tensor(indices,heavy):
 value=Q(1)
 for b in range(2):
  inds=[i%3 for i in indices if i//3==b]
  if b==1 and heavy:
   w=(Q(1),Q(1,6),Q(0))
   for i in inds: value*=w[i]
  else: value*=mom(9,Q(7,2),len(set(inds)))
 return value
# Principal localizing matrices: three observed Boolean coordinates in each
# nine-coordinate fractional block; second block can instead be exact.
# Repeated factors and opposite slacks are included. The indicator expansion
# evaluates products before reduction, with globally coupled square spans.
for heavy in (False,True):
 for fac in ((),((0,1),),((0,0),(3,1)),((0,1),(0,1)),((0,1),(0,0))):
  degree=(4-len(fac))//2
  basis=[()]+[(i,) for i in range(6)]
  if degree==2: basis += list(combinations_with_replacement(range(6),2))
  def entry(I,J):
   out=Q(0)
   zeros=[i for i,v in fac if not v]
   ones=[i for i,v in fac if v]
   for flags in product((0,1),repeat=len(zeros)):
    selected=[i for i,v in zip(zeros,flags) if v]
    out+=(-1)**len(selected)*tensor(tuple(I)+tuple(J)+tuple(ones)+tuple(selected),heavy)
   return out
  psd([[entry(I,J) for J in basis] for I in basis])
for n in range(2,9):
 for k in range(n):
  for bits in product((0,1),repeat=n):
   s=sum(bits)
   cut=2*sum(bits[i]*bits[j] for i,j in combinations(range(n),2))-2*k*s+k*(k+1)
   assert cut==(s-k)*(s-k-1)>=0
   counts["clique_vertices"]+=1
assert Q(1,4)-Q(1,32)*(Q(5,2)+Q(1,4))-Q(1,32)==Q(17,128)
assert Q(2)*Q(17,128)/6==Q(17,384)
counts["status"]="PASS"
counts["arithmetic"]="exact rational; PSD by symmetric elimination"
counts["limits"]="Finite Gram/indicator identities, sampled principal global localizer matrices, Boolean clique vertices; no universal proof or priority conclusion."
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,indent=2))
