from fractions import Fraction as Q
from itertools import permutations
from random import Random
rng=Random(1937)

def integ(a,t):
 N=len(a);return sum((v*max(Q(0),min(Q(1,N),t-Q(j,N))) for j,v in enumerate(a)),Q(0))
def reach(a,b,E,T):
 N=len(a);value=Q(0)
 for j,alpha in enumerate(a):
  lo=Q(j,N);hi=min(T,Q(j+1,N))
  if hi<lo:break
  h0=lo-value;value+=alpha*(hi-lo)
  h1=hi-value
  if h1>b+E:return lo+(b+E-h0)/(1-alpha)
  if hi==T:return T
 return T

def direct(a,blocks,T):
 times=set([Q(0),T]+[Q(j,len(a[0])) for j in range(len(a[0])+1) if Q(j,len(a[0]))<=T])
 for _,u,v in blocks:times|={u,v}
 neg=pos=Q(0)
 for t in times:
  W=[sum((max(Q(0),min(t,v)-u) for mode,u,v in blocks if mode==i),Q(0)) for i in range(len(a))]
  A=[integ(row,t) for row in a]
  neg=max(neg,max(w-z for w,z in zip(W,A)));pos=max(pos,max(z-w for w,z in zip(W,A)))
 return neg,pos

light=band=0
for n in range(2,19):
 for trial in range(5):
  N=2*n; words=[]
  for _ in range(4):
   w=list(range(n))*2;rng.shuffle(w);words.append(w)
  a=[[Q(sum(w[j]==i for w in words),4) for j in range(N)] for i in range(n)]
  assert all(integ(row,Q(1))==Q(1,n) for row in a)
  for k in range(1,n):
   b=Q(0);used=set();blocks=[]
   for j in range(1,k+1):
    t=min(Q(1),Q(j*(n-j+1),n*(n-j)))
    i=max((i for i in range(n) if i not in used),key=lambda i:integ(a[i],t))
    used.add(i);blocks.append((i,b,t));b=t
    if t==1:break
   neg,pos=direct(a,blocks,b)
   assert max(neg,pos)<=Q(1,n)
   assert b==min(Q(1),Q(k*(n-k+1),n*(n-k)))
   if (n-k)**2<=k:
    assert b==1 and max(neg,pos)==Q(1,n);band+=1
   light+=1
print('PASS independent all-light construction:',light,'profiles/budgets;',band,'equal-mass band instances')

branches=set()
def coef(n,k):
 m=n-k+3;r=Q(m,m-1);c=1/(m*(r**3-1))
 for j in range(m+1,n+1):c=((j-1)**2*c+1)/(j*(j-1)*(1+c))
 return c

def remove(a,k,T):
 n=len(a);E=coef(n,k)*T
 if k==3:
  for word in permutations(range(n),3):
   b=Q(0);blocks=[]
   for i in word:
    t=reach(a[i],b,E,T);blocks.append((i,b,t));b=t
    if b==T:return blocks
  raise AssertionError('seed failure')
 child=coef(n-1,k-1);mass=[integ(row,T) for row in a]
 side='min' if child<Q(1,n-1) else 'max';branches.add(side)
 q=(min if side=='min' else max)(range(n),key=lambda i:mass[i])
 if mass[q]>=T-E:branches.add('constant');return [(q,Q(0),T)]
 L=T-mass[q]-E
 assert E-mass[q]/(n-1)>0 and child*L<=E-mass[q]/(n-1)
 ids=[i for i in range(n) if i!=q]
 reduced=[[v+a[q][j]/(n-1) for j,v in enumerate(a[i])] for i in ids]
 return [(ids[i],b,t) for i,b,t in remove(reduced,k-1,L)]+[(q,L,T)]
count=0
for n in range(5,11):
 for k in range(4,n):
  for trial in range(8):
   cols=[]
   for j in range(7):
    raw=[rng.randrange(7) for _ in range(n)]
    if trial==0:raw=[1]+[0]*(n-1)
    if trial==1:raw=[1]*n
    if sum(raw)==0:raw[0]=1
    cols.append([Q(x,sum(raw)) for x in raw])
   a=[list(row) for row in zip(*cols)]
   blocks=remove(a,k,Q(1));neg,pos=direct(a,blocks,Q(1))
   assert len(blocks)<=k and len({i for i,_,_ in blocks})==len(blocks)
   assert neg<=coef(n,k)
   count+=1
assert branches=={'min','max','constant'}
print('PASS independently implemented recursive removal:',count,'instances; branches',sorted(branches))
# The equality branch is also valid for both terminal-mass choices.
for n in range(3,30):
 C=Q(1,n-1);E=Q(1,n)
 for mass in (Q(0),Q(1,2*n),Q(1,n),Q(n-1,n),Q(1)):
  if mass>=1-E:assert 1-mass<=E
  else:assert E-mass/(n-1)>0 and C*(1-mass-E)==E-mass/(n-1)
print('PASS equality branch including constant-boundary equality')
