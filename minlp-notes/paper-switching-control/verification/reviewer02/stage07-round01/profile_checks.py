from fractions import Fraction as Q
from itertools import permutations,product
from random import Random
from collections import Counter
rng=Random(770204);stats=Counter()
def cumulative(rows,dt,t):
 out=[Q(0)]*len(rows[0]);left=Q(0)
 for row,d in zip(rows,dt):
  length=max(Q(0),min(t-left,d))
  for i,r in enumerate(row):out[i]+=length*r
  left+=d
 return out

def discrepancy(rows,dt,schedule,one=False):
 points={Q(0)};total=Q(0)
 for d in dt:total+=d;points.add(total)
 points.update(v for p,a,b in schedule for v in (a,b))
 peak=Q(0)
 for t in points:
  A=cumulative(rows,dt,t);W=[Q(0)]*len(A)
  for i,a,b in schedule:W[i]+=max(Q(0),min(t,b)-a)
  peak=max(peak,*[(w-a if one else abs(w-a)) for a,w in zip(A,W)])
 return peak

def L(n,k):return 1/(n*(Q(n,n-1)**k-1))
def C(n,k):return Q(n*(n-1)+(n-k)*(n-k-1),n*k*(2*n-k-1))
def seeded(n,k,ell):
 m=n-k+ell;theta=Q(m*(m-1),n*(n-1))*(2*Q(m-1,m)**ell-1)
 return (1+theta)/(n*(1-theta))
def latest(rows,dt,i,target):
 # Scan all cells, retaining the last feasible endpoint, including flats.
 time=Q(0);H=Q(0);last=Q(0)
 for row,d in zip(rows,dt):
  slope=1-row[i]
  if H+slope*d<=target:last=time+d
  elif H<=target:last=time+(target-H)/slope
  time+=d;H+=slope*d
 return last

def construct(rows,dt,k,ell=1):
 n=len(rows[0]);T=sum(dt);masses=cumulative(rows,dt,T)
 if k==ell:
  E=L(n,k)*T
  for word in permutations(range(n),k):
   now=Q(0);out=[]
   for p in word:
    end=latest(rows,dt,p,now+E);out.append((p,now,end));now=end
    if now==T:
     stats['seed_constructed']+=1
     return out
  raise AssertionError('seed failure')
 prev=seeded(n-1,k-1,ell);coef=((n-1)**2*prev+1)/(n*(n-1)*(1+prev));E=coef*T
 q=(max if prev>=Q(1,n-1) else min)(range(n),key=lambda i:masses[i]);mass=masses[q]
 stats['maximum_mass' if prev>=Q(1,n-1) else 'minimum_mass']+=1
 if mass>=T-E:stats['constant_branch']+=1;return [(q,Q(0),T)]
 horizon=T-mass-E;resid=E-mass/(n-1)
 assert horizon>0 and resid>0 and prev*horizon<=resid
 retained=[i for i in range(n) if i!=q];newrows=[];newdt=[];time=Q(0)
 for row,d in zip(rows,dt):
  length=min(d,horizon-time)
  if length>0:newdt.append(length);newrows.append([row[i]+row[q]/(n-1) for i in retained])
  time+=d
  if time>=horizon:break
 sub=construct(newrows,newdt,k-1,ell)
 return [(retained[p],a,b) for p,a,b in sub]+[(q,horizon,T)]
for n,k,ell in ((4,3,1),(6,4,1),(5,4,3),(6,5,4),(7,5,4),(9,6,4)):
 for trial in range(8):
  if trial==0:
   rows=[[Q(i==0) for i in range(n)]];dt=[Q(1)]
  else:
   dt=[Q(rng.randrange(1,10),rng.randrange(2,12)) for _ in range(5)];rows=[]
   for j in range(5):
    w=[rng.randrange(3) for _ in range(n)]
    if not sum(w):w[0]=1
    rows.append([Q(x,sum(w)) for x in w])
  out=construct(rows,dt,k,ell);E=seeded(n,k,ell)*sum(dt)
  assert len(out)<=k and len({p for p,a,b in out})==len(out)
  assert discrepancy(rows,dt,out,True)<=E
  stats['recursive_profile_cases']+=1
# Adversarial equal-mass profiles with pure phases (hence many flat portions).
for n,k in ((3,2),(6,4),(12,9),(20,16)):
 assert (n-k)**2<=k
 for trial in range(12):
  word=list(range(n))*3;rng.shuffle(word);dt=[Q(1,3*n)]*(3*n);rows=[[Q(i==p) for i in range(n)] for p in word]
  E=Q(1,n);start=Q(0);unused=set(range(n));out=[]
  for j in range(1,k+1):
   end=min(Q(1),Q(j*(n-j+1),n-j)*E)
   p=max(unused,key=lambda i:cumulative(rows,dt,end)[i]);unused.remove(p);out.append((p,start,end));start=end
   if start==1:break
  assert start==1 and discrepancy(rows,dt,out)<=E
  # Every at-most-k-block schedule omits a coordinate of terminal mass E.
  assert all(v==E for v in cumulative(rows,dt,Q(1)))
  stats['equal_mass_exact_instance_cases']+=1
print(dict(stats))
