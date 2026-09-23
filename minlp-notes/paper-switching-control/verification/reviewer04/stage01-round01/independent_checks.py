from fractions import Fraction as Q
from itertools import product
from random import Random
import hashlib,json
from pathlib import Path

root=Path('paper-switching-control/process/snapshots/stage01-round01')
manifest=json.loads((root/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
print('PASS snapshot hashes:',len(manifest))

# Independent schedule enumeration, including constant and returning-mode words.
count=0
for n in range(2,6):
 for N in range(1,7):
  by_switch=[None]*N
  for word in product(range(n),repeat=N):
   s=sum(a!=b for a,b in zip(word,word[1:]))
   occupation=[0]*n; err=0
   for t,mode in enumerate(word,1):
    occupation[mode]+=1
    err=max(err,max(abs(t-n*w) for w in occupation))
   if by_switch[s] is None or err<by_switch[s]:by_switch[s]=err
  for k in range(1,n):
   actual=min(v for v in by_switch[:k] if v is not None)
   for K in range(N,N*(n-1)+1):
    b=0
    for _ in range(k):b=(n*b+K)//(n-1)
    if b>=N:break
   assert actual==K,(n,N,k,actual,K)
   E=Q(N)*max(Q(1,n),1/(n*((Q(n,n-1)**k)-1)))
   assert E<=Q(K,n)<E+Q(n-1,n)
   count+=1
print('PASS exhaustive uniform-grid recurrence and strict gap cases:',count)

# Solve each ordered two-mode continuous problem by exact intersection,
# independently of the construction used in the manuscript.
def optimum(a):
 n=len(a[0]); T=len(a)
 cumulative=[[Q(0)]*n]
 for col in a:cumulative.append([u+v for u,v in zip(cumulative[-1],col)])
 m=cumulative[-1]
 best=Q(T)
 for p in range(n):
  for q in range(n):
   if p==q:continue
   target=T-m[q]
   for j in range(T):
    if 2*j-cumulative[j][p]<=target<=2*(j+1)-cumulative[j+1][p]:
     tau=Q(j)+(target-(2*j-cumulative[j][p]))/(2-a[j][p])
     break
   def allocation(t,i):
    if t==T:return m[i]
    j=int(t)
    return cumulative[j][i]+(t-j)*a[j][i]
   err=Q(0)
   for t in sorted(set([Q(j) for j in range(T+1)]+[tau])):
    for i in range(n):
     w=min(t,tau) if i==p else max(Q(0),t-tau) if i==q else Q(0)
     err=max(err,abs(allocation(t,i)-w))
   three=max(max((m[i] for i in range(n) if i not in (p,q)),default=Q(0)),tau-allocation(tau,p),T-m[q]-tau)
   assert err==three
   best=min(best,err)
 return best

rng=Random(2026090704); count=0
for n in range(3,11):
 for _ in range(12):
  a=[]
  for j in range(4):
   z=[rng.randrange(5) for i in range(n)]
   if not sum(z):z[0]=1
   a.append([Q(v,sum(z)) for v in z])
  H=4*max(Q(1,3),Q((n-1)**2,n*(2*n-1)))
  assert optimum(a)<=H
  count+=1
 for a in ([[Q(1,n)]*n for j in range(3)],[[Q(i==j) for i in range(n)] for j in range(3)]):
  target=3*max(Q(1,n),Q((n-1)**2,n*(2*n-1))) if a[0][0]==Q(1,n) else Q(1)
  assert optimum(a)==target
print('PASS exact continuous pair optimization: random profiles',count,'; uniform and pure-block sharpness profiles',16)
