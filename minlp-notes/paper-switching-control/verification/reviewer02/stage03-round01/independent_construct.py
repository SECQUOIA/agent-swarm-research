from fractions import Fraction as F
from random import Random
from collections import Counter
from pathlib import Path
from itertools import combinations
rng=Random(83731);counts=Counter()

class Input:
 def __init__(self,breaks,rows,labels=None):
  self.breaks=breaks;self.rows=rows;self.n=len(rows[0]);self.T=breaks[-1]
  self.labels=tuple(range(self.n)) if labels is None else labels
 def at(self,t):
  A=[F(0)]*self.n
  for a,b,row in zip(self.breaks,self.breaks[1:],self.rows):
   dt=max(F(0),min(t,b)-a)
   for i,x in enumerate(row):A[i]+=dt*x
  return A
 def reach(self,i,b,E):
  y=b+E;last=F(0)
  for a,c,row in zip(self.breaks,self.breaks[1:],self.rows):
   ha=a-self.at(a)[i];hc=c-self.at(c)[i]
   if hc<=y:last=c;continue
   assert row[i]<1
   return a+(y-ha)/(1-row[i])
  return last
 def remove(self,q,L):
  breaks=[F(0)];rows=[]
  for a,b,row in zip(self.breaks,self.breaks[1:],self.rows):
   if a>=L:break
   breaks.append(min(b,L));rows.append(tuple(x+row[q]/(self.n-1) for i,x in enumerate(row) if i!=q))
  return Input(breaks,rows,tuple(x for i,x in enumerate(self.labels) if i!=q))

def seed_c(m,ell):return 1/(m*(F(m,m-1)**ell-1))
def trans(n,c):return ((n-1)**2*c+1)/(n*(n-1)*(1+c))
def coefficient(n,m,ell):
 c=seed_c(m,ell)
 for j in range(m+1,n+1):c=trans(j,c)
 return c

def seed_schedule(A,k,E):
 states={frozenset(): (F(0),[])}
 for step in range(k):
  nxt={}
  for used,(b,word) in states.items():
   for i in range(A.n):
    if i in used:continue
    t=A.reach(i,b,E);path=word+[(A.labels[i],b,t)]
    if t==A.T:return path
    key=used|{i}
    if key not in nxt or t>nxt[key][0]:nxt[key]=(t,path)
  states=nxt
 raise AssertionError(('seed failed',A.n,k,E))

def construct(A,m,ell,equality_min):
 c=coefficient(A.n,m,ell);E=c*A.T
 if A.n==m:return seed_schedule(A,ell,E)
 C=coefficient(A.n-1,m,ell);a=A.at(A.T)
 if C<F(1,A.n-1):kind='minimum'
 elif C>F(1,A.n-1):kind='maximum'
 else:kind='equal_minimum' if equality_min else 'equal_maximum'
 counts[kind]+=1
 q=min(range(A.n),key=lambda i:a[i]) if kind.endswith('minimum') else max(range(A.n),key=lambda i:a[i])
 if a[q]>=A.T-E:
  counts['constant_branch']+=1
  return [(A.labels[q],F(0),A.T)]
 counts['recursive_branch']+=1
 L=A.T-a[q]-E;Ep=E-a[q]/(A.n-1)
 assert L>0 and Ep>0 and C*L<=Ep
 sub=A.remove(q,L)
 assert all(sum(row)==1 and min(row)>=0 for row in sub.rows)
 return construct(sub,m,ell,equality_min)+[(A.labels[q],L,A.T)]

def errors(A,path):
 best=[F(0),F(0)]
 assert path[0][1]==0 and path[-1][2]==A.T
 assert all(a[2]==b[1] for a,b in zip(path,path[1:]))
 assert len({i for i,a,b in path})==len(path)
 for t in set(A.breaks)|{b for i,a,b in path}:
  value=A.at(t);W=[sum(max(F(0),min(t,b)-a) for i,a,b in path if i==label) for label in A.labels]
  best[0]=max(best[0],max(w-a for w,a in zip(W,value)))
  best[1]=max(best[1],max(abs(w-a) for w,a in zip(W,value)))
 return best

cases=0;negative_cases=0
for n in range(3,10):
 for k in range(1,n):
  for ell in range(1,min(4,k)+1):
   m=n-k+ell
   for typ in range(4):
    widths=[F(1,7),F(2,7),F(4,7)];breaks=[F(0),F(1,7),F(3,7),F(1)]
    rows=[]
    for j in range(3):
     if typ==0:row=[F(1,n)]*n
     elif typ==1:row=[F(i==j%n) for i in range(n)]
     elif typ==2:row=[F(i==0) for i in range(n)]
     else:
      x=[rng.randrange(5) for _ in range(n)]
      if sum(x)==0:x[0]=1
      row=[F(a,sum(x)) for a in x]
     rows.append(row)
    A=Input(breaks,rows)
    for eqmin in (False,True):
     path=construct(A,m,ell,eqmin);em,full=errors(A,path)
     c=coefficient(n,m,ell)
     theta=F(m*(m-1),n*(n-1))*(2*F(m-1,m)**ell-1)
     closed=(1+theta)/(n*(1-theta))
     assert c==closed and len(path)<=k and em<=c
     if c<F(1,n):negative_cases+=1
     if max(A.at(A.T))<=c:assert full<=c
     cases+=1
print('Independent recursively constructed schedules:',cases)
print('Schedules using coefficient below reciprocal n:',negative_cases)
print('Removal contracts:',dict(counts))

# Fresh equal-mass profiles with sharp instance identity. A convex mixture of
# permutation matrices is doubly stochastic, so unit time cells give every
# terminal mass exactly one. Use the explicit all-light endpoint construction.
light_count=0
for n,k in ((2,1),(3,2),(6,4),(7,5),(12,9),(13,10),(20,16)):
 assert (n-k)**2<=k
 for _ in range(12):
  perms=[]
  for h in range(4):
   p=list(range(n));rng.shuffle(p);perms.append(p)
  rows=[[sum(F(p[j]==i,4) for p in perms) for i in range(n)] for j in range(n)]
  A=Input(list(map(F,range(n+1))),rows);assert A.at(A.T)==[1]*n
  used=set();path=[];b=F(0)
  for j in range(1,k+1):
   t=min(A.T,F(j*(n-j+1),n-j));v=A.at(t)
   i=max((i for i in range(n) if i not in used),key=lambda i:v[i])
   path.append((i,b,t));used.add(i);b=t
   if t==A.T:break
  assert b==A.T and len(path)<=k
  em,full=errors(A,path)
  assert full==1 # omitted mode gives a universal instance lower bound
  light_count+=1
print('Nonuniform equal-mass profiles with directly attained exact error T/n:',light_count)
