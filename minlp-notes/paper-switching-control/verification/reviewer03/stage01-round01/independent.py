"""Independent stage-1 checks; no imports from author verification code."""
from fractions import Fraction as Q
from itertools import combinations, product, combinations_with_replacement
import json, hashlib, random
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
OUT=Path(__file__).resolve().parent
SNAP=OUT.parents[2]/'process/snapshots/stage01-round01'
results={}
manifest=json.loads((SNAP/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((SNAP/k).read_bytes()).hexdigest()==v for k,v in manifest.items())
results['snapshot_hashes']=len(manifest)

def uniform_value(n,k,T):
    r=Q(n,n-1)
    return T*max(Q(1,n),1/(n*(r**k-1)))

def rec(n,k,N):
    for K in range(N,N*(n-1)+1):
        b=0
        for _ in range(k): b=(n*b+K)//(n-1)
        if b>=N:return Q(K,n)

def uniform_direct(n,word,ends):
    W=[0]*n
    worst=0
    start=0
    for p,t in zip(word,ends):
        W[p]+=t-start
        worst=max(worst,max(abs(t-n*w) for w in W))
        start=t
    return Q(worst,n)

# Full enumeration includes repeated modes and all shorter schedules.
count=0;schedules=0
for n in range(2,6):
 for k in range(1,n):
  for N in range(1,8):
   best=Q(N)
   for m in range(1,min(k,N)+1):
    for cuts in combinations(range(1,N),m-1):
     for word in product(range(n),repeat=m):
      schedules+=1
      best=min(best,uniform_direct(n,word,(*cuts,N)))
   e=uniform_value(n,k,N)
   assert best==rec(n,k,N),(n,k,N,best,rec(n,k,N))
   assert e<=best<e+Q(n-1,n)
   count+=1
results['uniform_grid_cases']=count;results['full_schedules_enumerated']=schedules

# Independent continuous LP directly imposes every coordinate's +/- discrepancy
# at every variable block endpoint. Occupation is the sum of selected intervals.
lps=0
for n in range(2,6):
 for k in range(1,n):
  best=1.
  for word in product(range(n),repeat=k):
   rows=[];rhs=[]
   # Variables are t_1,...,t_{k-1},E; horizon one.
   def time(j):
    row=np.zeros(k)
    if 0<j<k:row[j-1]=1
    return row,float(j==k)
   for j in range(1,k+1):
    rj,cj=time(j)
    for i in range(n):
     row=rj/n;const=cj/n
     for a in range(1,j+1):
      if word[a-1]==i:
       ra,ca=time(a);rb,cb=time(a-1)
       row=row-ra+rb;const=const-ca+cb
     for sign in (1,-1):
      constraint=sign*row.copy();constraint[-1]-=1
      rows.append(constraint);rhs.append(-sign*const)
   for j in range(1,k):
    ra,ca=time(j);rb,cb=time(j+1)
    rows.append(ra-rb);rhs.append(cb-ca)
   obj=np.zeros(k);obj[-1]=1
   sol=linprog(obj,A_ub=rows,b_ub=rhs,bounds=[(0,1)]*k,method='highs')
   assert sol.success
   best=min(best,sol.fun);lps+=1
  assert abs(best-float(uniform_value(n,k,Q(1))))<1e-8,(n,k,best)
results['continuous_uniform_LPs']=lps

def cumulative(cols,t):
 n=len(cols[0]);a=[Q(0)]*n
 for j,col in enumerate(cols):
  dt=max(Q(0),min(Q(1),t-j))
  for i,x in enumerate(col):a[i]+=dt*x
 return a

def direct(cols,p,q,tau):
 T=len(cols);n=len(cols[0]);error=Q(0)
 for t in sorted(set([Q(j) for j in range(T+1)]+[tau])):
  A=cumulative(cols,t);W=[Q(0)]*n
  W[p]+=min(t,tau);W[q]+=max(Q(0),t-tau)
  error=max(error,max(abs(a-w) for a,w in zip(A,W)))
 return error

def three(cols,p,q,tau):
 T=len(cols);m=cumulative(cols,Q(T));A=cumulative(cols,tau)
 return max([m[i] for i in range(len(m)) if i not in (p,q)]+[tau-A[p],T-m[q]-tau])

def construct(cols):
 T=Q(len(cols));n=len(cols[0]);E=T*max(Q(1,3),Q((n-1)**2,n*(2*n-1)))
 m=cumulative(cols,T);order=sorted(range(n),key=lambda i:m[i],reverse=True);q,r=order[:2]
 if m[q]>=E:return r,q,max(Q(0),T-m[q]-E),E,'large'
 tq=T-m[q]-E;tr=T-m[r]-E
 A=cumulative(cols,tq)
 p=max((i for i in range(n) if i!=q),key=lambda i:A[i])
 if direct(cols,p,q,tq)<=E:return p,q,tq,E,'small_first'
 return q,r,tr,E,'small_second'

rng=random.Random(872)
profiles=[]
for n in (3,4,5):
 cs=[]
 for i,j in combinations_with_replacement(range(n),2):
  cs.append(tuple(Q((h==i)+(h==j),2) for h in range(n)))
 profiles.extend(product(cs,repeat=3))
for n in range(3,16):
 for _ in range(35):
  cols=[]
  for j in range(rng.randint(1,7)):
   numer=[rng.randrange(15) for _ in range(n)]
   if not sum(numer):numer[0]=1
   cols.append(tuple(Q(v,sum(numer)) for v in numer))
  profiles.append(cols)
# Force the second small-mass candidate: concentrate mode 0 in the first cell.
for n in range(5,16):
 profiles.append([tuple(Q(i==0) for i in range(n))]+[tuple(Q(0) if i==0 else Q(1,n-1) for i in range(n))]*(n-1))
branches={}; identities=0;threecells=0
for cols in profiles:
 p,q,tau,E,branch=construct(cols)
 branches[branch]=branches.get(branch,0)+1
 assert direct(cols,p,q,tau)<=E
 n=len(cols[0]);T=len(cols)
 for p0,q0 in ((0,1),(n-1,0)):
  for t in (Q(0),Q(T),Q(T,3),tau):
   assert direct(cols,p0,q0,t)==three(cols,p0,q0,t)
   identities+=1
 if T==3:
  masses=cumulative(cols,Q(3));order=sorted(range(n),key=lambda i:masses[i],reverse=True)
  assert direct(cols,order[1],order[0],Q(1))<=2-Q(3,n)
  threecells+=1
results['one_switch_profiles']=len(profiles);results['construction_branches']=branches
results['direct_three_term_identities']=identities;results['three_cell_constructions']=threecells
for n in range(3,51):
 cols=[tuple([Q(1,n)]*n)]*3
 assert min(direct(cols,0,1,Q(t)) for t in range(4))==2-Q(3,n)
results['three_cell_uniform_sharpness_cases']=48
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
