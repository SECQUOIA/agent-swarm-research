from fractions import Fraction as Q
from itertools import product, combinations
from math import comb, prod
from random import Random
from pathlib import Path
import json, hashlib
rng=Random(1010)
counts={'rank_generators':0,'face_atoms':0,'shifted_slack_cases':0,'gram_entries':0}
for m in range(1,7):
 n=2*m
 for trial in range(100):
  u=[Q(rng.randrange(21),20) for _ in range(n)]
  v=[Q(rng.randrange(21),20) for _ in range(n)]
  scale=max(max(u)*sum(v),max(v)*sum(u),Q(1,100))
  W=[[a*b/scale for b in v] for a in u]
  r=[sum(row) for row in W]; c=[sum(W[i][j] for i in range(n)) for j in range(n)]
  S=sum(r); D=1-sum(W[i][i] for i in range(n)); B=sum(W[i][m+i] for i in range(m))
  g=m-S+(2*m+1)*B+(4*m+1)*D
  assert g>=B+D>=0
  a=[int(t>=Q(1,2)) for t in r]
  if S:
   assert sum(abs(r[i]-c[i]) for i in range(n))<=2*S*D
   assert sum(abs(r[i]-a[i]) for i in range(n))<=6*S*D
   assert sum(abs(c[i]-a[i]) for i in range(n))<=8*S*D
  b=a.copy()
  for i in range(m):
   if b[i]==b[m+i]:b[i]=1-b[i]
  V=[[Q(b[i]*b[j],m) for j in range(n)] for i in range(n)]
  dist=sum(abs(W[i][j]-V[i][j]) for i in range(n) for j in range(n))
  assert dist<=8*m*B+116*m*D+5*abs(S-m)
  assert dist<=(136*m+10)*g
  assert dist<=28*m*B+156*m*D+5*(m-S)
  counts['rank_generators']+=1
 for x in product((0,1),repeat=m):
  b=list(x)+[1-t for t in x]
  W=[[Q(b[i]*b[j],m) for j in range(n)] for i in range(n)]
  for i,j in product(range(m),repeat=2):
   X=x[i]*x[j]
   assert m*W[i][j]==X
   assert m*W[i][m+j]==x[i]-X
   assert m*W[m+i][j]==x[j]-X
   assert m*W[m+i][m+j]==1-x[i]-x[j]+X
   assert m*(W[i][j]-W[i][m+j]-W[m+i][j]+W[m+i][m+j])==(2*x[i]-1)*(2*x[j]-1)
  counts['face_atoms']+=1
# Explicit univariate Lagrange representation of the source pseudo-density.
for k in range(3,14,2):
 t=Q(k,2)
 weights=[prod((t-a)/Q(w-a) for a in range(k+1) if a!=w) for w in range(k+1)]
 assert sum(weights)==1
 f=[((Q(w)-t)**2-Q(1,4))/k**2 for w in range(k+1)]
 assert sum(weights[w]*f[w] for w in range(k+1))==-Q(1,4*k*k)
 theta=Q(1,8*k*k)
 assert sum(weights[w]*(f[w]+theta) for w in range(k+1))==-Q(1,8*k*k)
 assert sum(Q(comb(k,w),2**k)*(f[w]+theta) for w in range(k+1))>=Q(1,6*k)
 for w in range(k+1):
  assert 0<=f[w]+theta<=1
  den=weights[w]*2**k/comb(k,w)
  assert den**2<=k**3
  assert ((2*w-k)**2-1)/Q(4*k*k)==f[w]
  counts['shifted_slack_cases']+=1
# Entrywise exact falling-factorial Gram identity including its vanishing boundary.
def falling(x,j):return prod(x-a for a in range(j))
for d in range(1,5):
 for s in range(max(2*d,4*d-2),max(2*d,4*d-2)+4):
  for t in [Q(2*d-1),Q(s,2),Q(s,2)+Q(1,4)]:
   if min(t,s-t)<2*d-1:continue
   for ell in range(d+1):
    lhs=falling(t,2*d-ell)/falling(s,2*d-ell)
    rhs=sum(comb(ell,j)*falling(t,2*d-j)*falling(s-t,j)/falling(s,2*d) for j in range(ell+1))
    assert lhs==rhs
    counts['gram_entries']+=1
out={'method':'Exact Fraction arithmetic; finite falsification checks, not universal proof', 'counts':counts,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
