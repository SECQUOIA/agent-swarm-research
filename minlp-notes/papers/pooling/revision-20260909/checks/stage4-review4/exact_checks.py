from fractions import Fraction as Q
from itertools import product
from random import Random
from math import comb

rng=Random(49092026)
checks={}
def outer(r,c):
 s=sum(r)
 return tuple(a*b/s for a in r for b in c) if s else (Q(0),)*(len(r)*len(c))
def norm(x,y): return sum(abs(a-b) for a,b in zip(x,y))
def metrics(w,m):
 n=2*m
 return sum(w),1-sum(w[i*n+i] for i in range(n)),sum(w[i*n+m+i] for i in range(m))
def paired(w,r,c,m):
 a=[int(v>Q(1,2)) for v in r]
 for i in range(m):
  if a[i]==a[m+i]: a[i],a[m+i]=1,0
 return tuple(Q(x*y,m) for x in a for y in a)
# Independently reconstruct every margin pair on the half grid up to 6 coordinates.
count=0; generators={}
for m in (1,2,3):
 groups={}
 for r in product((Q(0),Q(1,2),Q(1)),repeat=2*m): groups.setdefault(sum(r),[]).append(r)
 samples=[]
 for s,rows in groups.items():
  pairs=product(rows,rows) if m<3 else ((rng.choice(rows),rng.choice(rows)) for _ in range(min(100,len(rows)**2)))
  for r,c in pairs:
   w=outer(r,c); v=paired(w,r,c,m); t,d,b=metrics(w,m)
   assert t<=m+2*m*b+4*m*d
   assert norm(w,v)<=8*m*b+116*m*d+5*abs(t-m)
   assert norm(w,v)<=28*m*b+156*m*d+5*(m-t)
   samples.append((w,v));count+=1
 generators[m]=samples
checks['face_rounding_generators']=count
for m,samples in generators.items():
 for _ in range(100):
  atoms=rng.choices(samples,k=3); weights=[rng.randint(1,10) for _ in range(3)];den=sum(weights)
  w=tuple(sum(Q(k,den)*atom[0][i] for k,atom in zip(weights,atoms)) for i in range(4*m*m))
  v=tuple(sum(Q(k,den)*atom[1][i] for k,atom in zip(weights,atoms)) for i in range(4*m*m))
  t,d,b=metrics(w,m)
  assert norm(w,v)<=28*m*b+156*m*d+5*(m-t)
checks['face_rounding_convex_combinations']=300
# Unit repair independently chooses reductions from other coordinates sequentially.
def repair_margin(r):
 r=list(r);need=1-r[0];r[0]=Q(1)
 for i in range(1,len(r)):
  take=min(need,r[i]);r[i]-=take;need-=take
 assert need==0
 return tuple(r)
count=0
for m,samples in generators.items():
 n=2*m
 for w,_ in samples:
  r=tuple(sum(w[i*n+j] for j in range(n)) for i in range(n));c=tuple(sum(w[i*n+j] for i in range(n)) for j in range(n));s=sum(r)
  if s>=1: v=outer(repair_margin(r),repair_margin(c))
  else: v=(Q(1),)+(Q(0),)*(n*n-1)
  delta=2-r[0]-c[0]
  assert norm(w,v)<=2*delta
  costs=tuple(Q(rng.randint(-9,9)) for _ in w);bound=max(abs(x) for x in costs);penalty=2*bound+1
  old=sum(a*b for a,b in zip(costs,w))-penalty*(r[0]+c[0]);new=sum(a*b for a,b in zip(costs,v))-2*penalty
  assert new<=old-delta
  count+=1
checks['unit_repair_and_penalty']=count
# Telescoping, unique exposed vertices, physical interface balances and price identity.
count=0;edges=0
for n in range(2,9):
 e=Q(1,4);s=[e**(n-j-1) for j in range(n)];d=[(1-e)*e**(2*(n-j-1)-1) for j in range(n-1)]
 verts={}
 for bits in product((0,1),repeat=n):
  x=[];prev=Q(0)
  for b in bits:
   prev=b+(1-2*b)*e*prev;x.append(prev)
  t=x[-1];L=t-sum(a*b for a,b in zip(d,x));assert L==t*t
  assert t not in [v[-1] for v in verts.values()]
  verts[bits]=x
  z=t-t*t;q=2-t
  assert q*t<=t+z and 0<=z<=1
  profit=sum((s[j+1]-s[j])*s[j]*x[j] for j in range(n-1))-z
  assert profit==0
  count+=1
 for bits,x in verts.items():
  for j in range(n):
   other=list(bits);other[j]=1-other[j];y=verts[tuple(other)];dt=y[-1]-x[-1]
   assert -dt*dt+e**n*dt<0
   mid=[(a+b)/2 for a,b in zip(x,y)];F=mid[-1]-sum(a*b for a,b in zip(d,mid))-mid[-1]**2
   assert F==dt*dt/4
   edges+=1
 for _ in range(20):
  a,b=rng.choices(list(verts.values()),k=2);x=[(u+2*v)/3 for u,v in zip(a,b)];prev=Q(0);rhs=Q(0)
  for j,val in enumerate(x):
   rhs+=e**(2*(n-j-1))*(val-e*prev)*(1-e*prev-val);prev=val
  F=x[-1]-sum(a*b for a,b in zip(d,x))-x[-1]**2
  assert F==rhs and F>=0
checks['geometry_vertices']=count;checks['geometry_incident_directed_edges']=edges;checks['telescoping_nonvertices']=140
# Correlation-face inverse on every atom, plus nontrivial mixtures.
count=0
for m in range(1,8):
 for x in product((0,1),repeat=m):
  a=x+tuple(1-u for u in x);w=tuple(Q(u*v,m) for u in a for v in a);t,d,b=metrics(w,m)
  assert (t,d,b)==(m,0,0)
  X=[[m*w[i*2*m+j] for j in range(m)] for i in range(m)]
  assert all(X[i][j]==x[i]*x[j] for i in range(m) for j in range(m))
  assert all(m*w[i*2*m+m+j]==X[i][i]-X[i][j] for i in range(m) for j in range(m))
  assert all(m*w[(m+i)*2*m+m+j]==1-X[i][i]-X[j][j]+X[i][j] for i in range(m) for j in range(m))
  count+=1
checks['correlation_face_atoms']=count
for key,value in checks.items(): print(f'PASS {key}: {value}')
print('All checks use exact Fraction arithmetic. Finite cases do not prove asymptotic claims or cited theorems.')
