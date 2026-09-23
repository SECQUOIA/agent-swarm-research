from fractions import Fraction as F
from itertools import permutations,combinations
from random import Random
from pathlib import Path
import hashlib,json
base=Path('paper-switching-control/process/snapshots/stage03-round01')
manifest=json.loads((base/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((base/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
print('PASS snapshot files:',len(manifest))

def allocation(a,t):
 N=len(a); n=len(a[0]);value=[F(0)]*n
 for j,col in enumerate(a):
  length=max(F(0),min(t-F(j,N),F(1,N)))
  for i in range(n):value[i]+=length*col[i]
 return value

def error(a,blocks,T):
 neg=pos=F(0)
 times={F(j,len(a)) for j in range(len(a)+1) if F(j,len(a))<=T}|{b for _,b,_ in blocks}|{e for _,_,e in blocks}
 for t in times:
  W=[F(0)]*len(a[0])
  for i,b,e in blocks:W[i]+=max(F(0),min(t,e)-b)
  for w,aa in zip(W,allocation(a,t)):neg=max(neg,w-aa);pos=max(pos,aa-w)
 return neg,pos

# Latest inverse computed directly from all affine cells, including flats.
def reach(a,i,b,E,T):
 target=b+E
 if T-allocation(a,T)[i]<=target:return T
 for j in range(len(a)):
  lo=F(j,len(a));hi=min(T,F(j+1,len(a)))
  if hi<lo:break
  Hlo=lo-allocation(a,lo)[i];Hhi=hi-allocation(a,hi)[i]
  if Hlo<=target<Hhi:return lo+(target-Hlo)/(1-a[j][i])
 raise AssertionError('No reach endpoint')

def greedy_light(a,k,E):
 n=len(a[0]);used=set();blocks=[];b=F(0)
 for j in range(1,k+1):
  end=min(F(1),F(j*(n-j+1),n-j)*E)
  values=allocation(a,end)
  i=max(set(range(n))-used,key=lambda i:values[i])
  blocks.append((i,b,end));used.add(i);b=end
  if b==1:break
 return blocks

rng=Random(20260907043); cases=0
for n,k in ((2,1),(3,2),(4,3),(5,4),(6,4),(7,5),(12,9),(13,10)):
 assert (n-k)**2<=k
 # Convex combinations of permutation matrices provide unequal temporal
 # profiles with exactly equal terminal masses, including pure ones.
 for trial in range(24):
  perms=[]; weights=[]
  for h in range(1 if trial==0 else 4):
   p=list(range(n));rng.shuffle(p);perms.append(p);weights.append(rng.randrange(1,8))
  a=[[sum(F(w,sum(weights)) for p,w in zip(perms,weights) if p[j]==i) for i in range(n)] for j in range(n)]
  assert allocation(a,F(1))==[F(1,n)]*n
  blocks=greedy_light(a,k,F(1,n))
  assert blocks[-1][2]==1 and len(blocks)<=k
  assert max(error(a,blocks,F(1)))==F(1,n)
  cases+=1
print('PASS independent all-input equal-mass-band construction samples:',cases)

# Independently propagate the analytic three-block seed, exercising both
# mass-selection signs and the constant-mode branch on exact rational data.
def coeff(n,k):
 m=n-k+3
 eta=F(m*(m-1),n*(n-1))*(2*F(m-1,m)**3-1)
 return (1+eta)/(n*(1-eta))
branches=set()
def seeded(a,k,T):
 n=len(a[0]);E=coeff(n,k)*T
 if k==3:
  for word in permutations(range(n),3):
   b=F(0);blocks=[]
   for i in word:
    e=reach(a,i,b,E,T);blocks.append((i,b,e));b=e
    if b==T:return blocks
  raise AssertionError('analytic seed failed')
 C=coeff(n-1,k-1);masses=allocation(a,T)
 if C<F(1,n-1):q=min(range(n),key=masses.__getitem__);branches.add('minimum')
 else:q=max(range(n),key=masses.__getitem__);branches.add('maximum')
 mass=masses[q]
 if mass>=T-E:branches.add('constant');return [(q,F(0),T)]
 L=T-mass-E
 assert E-mass/(n-1)>0 and C*L<=E-mass/(n-1)
 remaining=[i for i in range(n) if i!=q]
 completed=[[col[i]+col[q]/(n-1) for i in remaining] for col in a]
 prefix=seeded(completed,k-1,L)
 return [(remaining[i],b,e) for i,b,e in prefix]+[(q,L,T)]
cases=0
for n,k in ((5,4),(6,5),(7,6),(8,5),(9,6)):
 for trial in range(20):
  a=[]
  for j in range(7):
   weights=[rng.randrange(7) for i in range(n)]
   if trial==0:weights=[1]+[0]*(n-1)
   if not sum(weights):weights[0]=1
   a.append([F(w,sum(weights)) for w in weights])
  blocks=seeded(a,k,F(1))
  assert len(blocks)<=k and len(set(i for i,b,e in blocks))==len(blocks)
  assert error(a,blocks,F(1))[0]<=coeff(n,k)
  cases+=1
assert branches=={'minimum','maximum','constant'}
print('PASS independent recursive seed schedules:',cases,'; branches:',sorted(branches))

# Third-largest-mass example: enumerate two-mode prefix constructions, then
# append an unused member of the largest-mass triple.
cases=0; masses=[F(1,6)]*3+[F(1,10)]*5; E=F(245,1014);L=1-F(1,6)-E
for trial in range(30):
 # Perturb two equal-width cells in opposite directions without changing mass.
 a=[list(masses) for j in range(8)]
 for pair in range(4):
  i,j=rng.sample(range(8),2); amount=min(masses[i],masses[j])*F(rng.randrange(5),5)
  a[2*pair][i]+=amount;a[2*pair][j]-=amount
  a[2*pair+1][i]-=amount;a[2*pair+1][j]+=amount
 assert allocation(a,F(1))==masses
 for p,q in permutations(range(8),2):
  u=reach(a,p,F(0),E,L);v=reach(a,q,u,E,L)
  if v==L:
   r=next(i for i in range(3) if i not in (p,q))
   blocks=[(p,F(0),u),(q,u,L),(r,L,F(1))]
   assert max(error(a,blocks,F(1)))<=E
   break
 else:raise AssertionError('third-mass prefix failed')
 cases+=1
print('PASS independent third-largest-mass schedules:',cases)
