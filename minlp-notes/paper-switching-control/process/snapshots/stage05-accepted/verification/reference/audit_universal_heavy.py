"""Independent exact-rational DP checks of universal heavy-mode uncrossing.

This supplements the analytic proof; it does not establish arbitrary-size validity.
The DP independently rounds prefix counts without using the author flow code.
"""

from fractions import Fraction as F
import random
from collections import Counter
rng=random.Random(46092026)
stats=Counter()

def ceil(x): return -((-x.numerator)//x.denominator)
def make_rounding(A,h):
 n=len(A);M=len(A[0])-1; states={(0,)*n:()}
 for k in range(1,M+1):
  nxt={}
  for counts,w in states.items():
   for q in range(n):
    c=list(counts);c[q]+=1
    if all(A[i][k].numerator//A[i][k].denominator<=c[i]<=ceil(A[i][k]) for i in range(n)):
     nxt.setdefault(tuple(c),w+(q,))
  states=nxt
  assert states
 return next(w for c,w in states.items() if c[h]>=2)
def deadline(row,r):
 if row[r]<=1:return F(r)
 for k in range(r):
  if row[k+1]>1:
   return F(k)+(1-row[k])/(row[k+1]-row[k])
 raise AssertionError

def check(A,w):
 n=len(A);c=[0]*n
 for k,q in enumerate(w,1):
  c[q]+=1
  assert all(abs(A[i][k]-c[i])<=1 for i in range(n)),(A,w,k,c)

def uncross(A,w):
 seen=set()
 for idx,q in enumerate(w):
  if q in seen: r=idx+1;break
  seen.add(q)
 else:raise AssertionError
 d=deadline(A[q],r);j=min(r-2,max(0,ceil(d)-2))
 assert j<=d<=j+2
 others=sorted(seen-{q},key=lambda i:(deadline(A[i],r),i))
 assert len(others)==r-2
 pref=tuple(others[:j])+(q,q)+tuple(others[j:])
 out=pref+w[r:]
 assert Counter(pref)==Counter(w[:r])
 check(A,out)
 stats['instances']+=1;stats['r='+str(r)]+=1;stats['j='+str(j)]+=1
 stats['q_mass_equal_one']+=A[q][r]==1
 stats['integer_deadline']+=d.denominator==1
 stats['nontrivial_change']+=out!=w
 stats['unchanged_suffix_slots']+=len(w)-r
for case in range(1500):
 n=rng.randint(1,7); M=rng.randint(2,14)
 cols=[]
 for k in range(M):
  den=rng.choice([1,2,3,5,7]);counts=[0]*n
  for _ in range(den):counts[rng.randrange(n)]+=1
  cols.append([F(c,den) for c in counts])
 A=[[F(0)] for _ in range(n)]
 for col in cols:
  for i in range(n):A[i].append(A[i][-1]+col[i])
 h=max(range(n),key=lambda i:A[i][-1])
 if A[h][-1]<=1:continue
 w=make_rounding(A,h);check(A,w);uncross(A,w)
# The general uncrossing lemma also allows equality cases excluded by the
# tighter floor/ceiling rounding used above.
for cols,w in [
 ([[1,0,0],[0,1,0],[0,0,1]],(0,1,0)),
 ([[1,0],[1,0],[1,0]],(0,1,0)),
 ([[F(1,2),F(1,2),0],[F(1,2),0,F(1,2)],
  [0,F(1,2),F(1,2)],[1,0,0]],(0,1,2,0)),
]:
 n=len(cols[0]);A=[[F(0)] for _ in range(n)]
 for col in cols:
  for i in range(n):A[i].append(A[i][-1]+F(col[i]))
 check(A,w);uncross(A,w)
print(dict(stats))
