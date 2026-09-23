from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from collections import Counter
from pathlib import Path
import hashlib,json

base=Path('paper-switching-control/process/snapshots/stage02-round01')
manifest=json.loads((base/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((base/f).read_bytes()).hexdigest()==h for f,h in manifest.items())
print('PASS snapshot integrity:',len(manifest))

# Exhaustively test the first-repeat operation on every feasible word,
# without using the bundled flow construction or its reordering code.
n=3; M=4
cols=[tuple(int(i==a)+int(i==b) for i in range(n)) for a,b in combinations_with_replacement(range(n),2)]
word_count=0; profile_count=0; flow_count=0
for profile in product(cols, repeat=M):
 cumulative=[[0]*n]
 for col in profile:cumulative.append([a+b for a,b in zip(cumulative[-1],col)])
 heavy=[i for i in range(n) if cumulative[-1][i]>2]
 rounded_for=set()
 for word in product(range(n), repeat=M):
  counts=[0]*n; good=True; rounded=True
  for j,p in enumerate(word,1):
   counts[p]+=1
   for i in range(n):
    good &= abs(2*counts[i]-cumulative[j][i])<=2
    rounded &= cumulative[j][i]//2<=counts[i]<=(cumulative[j][i]+1)//2
  if rounded:rounded_for.update(i for i in heavy if counts[i]>=2)
  if not good or len(set(word))==M:continue
  if any(a==b for a,b in zip(word,word[1:])):continue
  for r in range(2,M+1):
   if len(set(word[:r]))<r:break
  q=word[r-1]
  def deadline(i):
   for j in range(r):
    if cumulative[j+1][i]>2:
     return Q(j)+Q(2-cumulative[j][i],profile[j][i])
   return Q(r)
  d=deadline(q)
  j=min(r-2,max(0,-(-d.numerator//d.denominator)-2))
  singles=sorted(set(word[:r])-{q},key=deadline)
  new=list(word)
  new[j:j+2]=[q,q]
  for t,i in zip(list(range(j))+list(range(j+2,r)),singles):new[t]=i
  assert Counter(new[:r])==Counter(word[:r])
  assert new[r:]==list(word[r:])
  counts=[0]*n
  for t,p in enumerate(new,1):
   counts[p]+=1
   assert all(abs(2*counts[i]-cumulative[t][i])<=2 for i in range(n))
  word_count+=1
 assert set(heavy)<=rounded_for
 flow_count+=len(heavy)
 profile_count+=1
print('PASS heavy-flow feasibility profiles:',profile_count,'; forced-heavy instances:',flow_count)
print('PASS first-repeat rearrangements from all feasible nonadjacent words:',word_count)

# Independent rational Fourier-Motzkin elimination, rather than vertex
# enumeration, rules out every switching-time cell at threshold one.
def eliminate(rows,index):
 pos=[];neg=[];zero=[]
 for row in rows:
  c=row[index]
  if c>0:pos.append(row)
  elif c<0:neg.append(row)
  else:zero.append(row[:index]+row[index+1:])
 for p in pos:
  for m in neg:
   row=[(-m[index])*a+p[index]*b for a,b in zip(p,m)]
   zero.append(row[:index]+row[index+1:])
 # Scaling/deduplication optional; the examples stay small.
 return list(set(tuple(r) for r in zero))
data=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[(Q(t,146),tuple(Q(a,146) for a in alloc)) for t,*alloc in data]
L=Q(57,8); last_t,last_a=knots[-1]
terminal=tuple(a+(L-last_t)/3 for a in last_a)
assert terminal==tuple(Q(v,1752) for v in [5281,3985,3217])
knots.append((L,terminal));segments=[]
for (lo,a),(hi,b) in zip(knots,knots[1:]):
 slope=tuple((bi-ai)/(hi-lo) for ai,bi in zip(a,b))
 intercept=tuple(ai-s*lo for ai,s in zip(a,slope))
 assert sum(slope)==1 and min(slope)>=0 and max(slope)<=Q(3,4)
 segments.append((lo,hi,slope,intercept))
def reach(i,b):
 target=b+1
 for lo,hi,slope,intercept in segments:
  if hi-(slope[i]*hi+intercept[i])>=target:
   return (target+intercept[i])/(1-slope[i])
 return L
from itertools import permutations
for word in permutations(range(3)):
 t=Q(0)
 for i in word:t=reach(i,t)
 assert t==Q(971,146)
count=0
for word in product(range(3),repeat=3):
 for first in range(len(segments)):
  for second in range(first,len(segments)):
   lo,hi,s,b=segments[first]; vlo,vhi,ss,bb=segments[second]
   rows=[(Q(-1),Q(0),-lo),(Q(1),Q(0),hi),(Q(0),Q(-1),-vlo),(Q(0),Q(1),vhi),(Q(1),Q(-1),Q(0))]
   for i in range(3):
    p,q,r=[Q(mode==i) for mode in word]
    rows.extend([(p-s[i],Q(0),1+b[i]),(p-q,q-ss[i],1+bb[i]),(p-q,q-r,1+terminal[i]-r*L)])
   constants=eliminate(eliminate(rows,0),0)
   assert any(row[0]<0 for row in constants),(word,first,second)
   count+=1
print('PASS n3k3 independent Fourier-Motzkin infeasibility cells:',count)
print('PASS six distinct reaches, terminal masses and slope bounds')

from random import Random
from itertools import combinations
rng=Random(42917)
reach_cases=0; weighted_cases=0
for n,k in ((3,2),(4,3),(5,4),(7,4)):
 for trial in range(12):
  horizon=n*(Q(n,n-1)**k-1)
  rates=[]
  for j in range(6):
   weights=[0]*n if trial%3==0 else [rng.randrange(5) for _ in range(n)]
   weights[rng.randrange(n)]+=1
   rates.append([Q(w,sum(weights)) for w in weights])
  knots=[(Q(0),[Q(0)]*n)]
  for col in rates:
   t,a=knots[-1]
   knots.append((t+horizon/6,[ai+horizon*v/6 for ai,v in zip(a,col)]))
  def phi(i,b):
   target=b+1
   for j in range(5,-1,-1):
    lo,a=knots[j];hi,aa=knots[j+1]
    if lo-a[i]<=target:
     if hi-aa[i]<=target:return hi
     return lo+(target-lo+a[i])/(1-rates[j][i])
   raise AssertionError('zero always feasible')
  best=Q(0)
  for word in permutations(range(n),k):
   t=Q(0)
   for i in word:t=phi(i,t)
   best=max(best,t)
  assert best==horizon,(n,k,trial,best,horizon)
  reach_cases+=1
  R=[phi(i,Q(0)) for i in range(n)]
  pairs={(i,j):phi(j,R[i]) for i in range(n) for j in range(n) if i!=j}
  if n>=5 and max(pairs.values())<horizon:
   P=[max(v for (a,b),v in pairs.items() if i not in (a,b)) for i in range(n)]
   Qexc={(i,j):max(v for (a,b),v in pairs.items() if not {i,j}.intersection((a,b))) for i,j in combinations(range(n),2)}
   for S in combinations(range(n),3):
    H=sum(P[i]+sum(Qexc[tuple(sorted((i,j)))] for j in range(n) if i!=j) for i in S)
    for z in range(n):
     assert H>=Q(3*n*n,n-1)+Q(3*n*n,(n-1)**2)*sum(R[i] for i in range(n) if i!=z)
     weighted_cases+=1
print('PASS independent distinct-reach examples including flat H:',reach_cases)
print('PASS directly evaluated stronger weighted pair inequalities:',weighted_cases)
