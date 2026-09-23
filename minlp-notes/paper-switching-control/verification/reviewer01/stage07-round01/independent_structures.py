"""Independent exact checks of reordering, reaches, and floor-history counts."""
from fractions import Fraction as F
from itertools import product,combinations,permutations
from collections import Counter
from random import Random
rng=Random(709071)

def prefixes(word,n):
    c=[0]*n;out=[]
    for w in word:c[w]+=1;out.append(tuple(c))
    return out

def quarter_error(A,word):
    n=len(A[0]);c=[0]*n;E=0
    for j,a in enumerate(A[1:]):
        c[word[j//2]]+=2
        E=max(E,*[abs(a[i]-c[i]) for i in range(n)])
    return E

def deadline(A,i,r):
    if A[2*r][i]<=4:return F(r)
    j=max(j for j in range(2*r+1) if A[j][i]<=4)
    return (j+F(4-A[j][i],A[j+1][i]-A[j][i]))/2

cases=words=repairs=heavy_modes=0
for n in range(2,5):
  half_rates=[v for v in product(range(3),repeat=n) if sum(v)==2]
  for M in range(2,7):
    for trial in range(3):
      A=[(0,)*n]
      for j in range(2*M):
        rates=rng.choice(half_rates)
        A.append(tuple(a+b for a,b in zip(A[-1],rates)))
      heavy=[i for i in range(n) if A[-1][i]>4];supported_heavy=set()
      cases+=1
      for w in product(range(n),repeat=M):
        if quarter_error(A,w)>4:continue
        words+=1
        count=prefixes(w,n)
        if all(A[2*j][i]//4<=count[j-1][i]<=-(-A[2*j][i]//4) for j in range(1,M+1) for i in range(n)):
          supported_heavy.update(i for i in heavy if count[-1][i]>=2)
        if len(set(w))==len(w) or any(a==b for a,b in zip(w,w[1:])):continue
        r=next(j+1 for j in range(1,M) if w[j] in w[:j]);q=w[r-1]
        singles=[i for i in w[:r] if i!=q]
        assert len(singles)==len(set(singles))==r-2
        dq=deadline(A,q,r)
        singles.sort(key=lambda i:(deadline(A,i,r),i))
        for start in range(r-1):
          if not start<=dq<=start+2:continue
          changed=tuple(singles[:start])+ (q,q)+tuple(singles[start:])+w[r:]
          assert Counter(changed[:r])==Counter(w[:r])
          assert quarter_error(A,changed)<=4
          repairs+=1
      assert supported_heavy==set(heavy)
      heavy_modes+=len(heavy)
print('PASS first-repeat audit:',cases,'half-cell input profiles,',words,'feasible words,',repairs,'valid pair-position repairs,',heavy_modes,'prescribed-heavy integral-prefix witnesses',flush=True)

# Fresh exact latest-inverse evaluation, including flat pieces.
def evalA(A,t,i):
    if t>=len(A)-1:return A[-1][i]
    j=t.numerator//t.denominator
    return A[j][i]+(t-j)*(A[j+1][i]-A[j][i])
def phi(A,i,b,E):
    L=len(A)-1;target=b+E
    H=[F(j)-a[i] for j,a in enumerate(A)]
    if H[-1]<=target:return F(L)
    j=max(j for j,h in enumerate(H) if h<=target)
    return j+(target-H[j])/(H[j+1]-H[j])
actual=strong=full=0
for n in range(3,10):
  for trial in range(10):
    A=[(F(0),)*n]
    for j in range(16):
      if trial==0:v=[F(1,n)]*n
      elif trial%2:
        v=[F(0)]*n
        v[rng.randrange(n)]=1
      else:
        raw=[rng.randrange(6) for i in range(n)]
        if sum(raw)==0:raw[0]=1
        v=[F(x,sum(raw)) for x in raw]
      A.append(tuple(a+b for a,b in zip(A[-1],v)))
    E=F(1);R=[phi(A,i,0,E) for i in range(n)]
    pair={(a,b):phi(A,b,R[a],E) for a,b in permutations(range(n),2)}
    B2=n*(F(n,n-1)**2-1)
    assert max(pair.values())>=B2
    if n>=4:
      tri={(a,b,c):phi(A,c,pair[a,b],E) for a,b,c in permutations(range(n),3)}
      assert max(tri.values())>=n*(F(n,n-1)**3-1)
    if n>=5 and max(pair.values())<16:
      Pi={i:max(v for (a,b),v in pair.items() if i not in (a,b)) for i in range(n)}
      Qi={q:max(v for (a,b),v in pair.items() if all(i not in (a,b) for i in q)) for q in combinations(range(n),2)}
      for S in combinations(range(n),3):
        H=sum(Pi[i]+sum(Qi[tuple(sorted((i,j)))] for j in range(n) if i!=j) for i in S)
        for z in range(n):
          assert H>=F(3*n*n,n-1)+F(3*n*n,(n-1)**2)*sum(R[i] for i in range(n) if i!=z)
          strong+=1
      best4=max(phi(A,d,v,E) for word,v in tri.items() for d in range(n) if d not in word)
      assert best4>=n*(F(n,n-1)**4-1)
      full+=1
    actual+=1
print('PASS exact flat-aware reaches:',actual,'profiles,',strong,'weighted (S,z) inequalities,',full,'four-block maxima',flush=True)

# Full-word bitset intersection, independent of the paper's 3x3 cost recursion.
for N in (5,6,7):
  allw=list(product(range(3),repeat=N));sw=[sum(a!=b for a,b in zip(w,w[1:])) for w in allw]
  switches={s:sum(1<<j for j,c in enumerate(sw) if c==s) for s in set(sw)}
  masks=[{} for j in range(N)]
  for j,w in enumerate(allw):
    for t,c in enumerate(prefixes(w,3)):
      for off in product((0,1),repeat=3):
        if sum(off) not in (1,2):continue
        f=tuple(c[i]-off[i] for i in range(3))
        if min(f)<0:continue
        masks[t][f]=masks[t].get(f,0)|(1<<j)
  history_min={}
  def visit(hist,mask):
    t=len(hist)
    if t==N:
      assert mask
      history_min[hist]=min(s for s,eligible in switches.items() if mask&eligible)
      return
    for inc in product((0,1),repeat=3):
      f=tuple(hist[-1][i]+inc[i] for i in range(3))
      if t+1-sum(f) in (1,2):visit(hist+(f,),mask&masks[t].get(f,0))
  visit(((0,0,0),),masks[0][(0,0,0)])
  dist=Counter(history_min.values())
  expected={5:{0:3,1:138,2:255},6:{0:3,1:255,2:1377,3:237},7:{0:3,1:414,2:4542,3:3891,4:6}}[N]
  assert dist==expected
  if N==7:
    canonical=((0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1),(2,1,1),(2,1,2))
    orbit={tuple(tuple(f[i] for i in p) for f in canonical) for p in permutations(range(3))}
    assert {h for h,c in history_min.items() if c==4}==orbit
  print('PASS full-word bitset enumeration:',N,dict(sorted(dist.items())),flush=True)
