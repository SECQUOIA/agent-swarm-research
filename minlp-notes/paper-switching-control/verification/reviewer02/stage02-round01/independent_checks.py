from fractions import Fraction as F
from itertools import product, combinations
from scipy.optimize import linprog
from pathlib import Path
import json

outdir=Path(__file__).parent
raw=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[tuple(F(x,146) for x in row) for row in raw]
L=F(57,8); t,*m=knots[-1]
knots.append((L,*(a+(L-t)/3 for a in m)))
terminal=knots[-1][1:]
segments=[]
for left,right in zip(knots,knots[1:]):
 lo,*a=left; hi,*b=right
 slopes=[(y-x)/(hi-lo) for x,y in zip(a,b)]
 intercepts=[x-s*lo for x,s in zip(a,slopes)]
 assert sum(slopes)==1 and all(0<=s<=F(3,4) for s in slopes)
 segments.append((lo,hi,slopes,intercepts))

def solve(A,b):
 rows=[list(map(F,row))+[F(rhs)] for row,rhs in zip(A,b)]
 for j in range(3):
  pivot=next((r for r in range(j,3) if rows[r][j]),None)
  if pivot is None:return None
  rows[j],rows[pivot]=rows[pivot],rows[j]
  z=rows[j][j];rows[j]=[x/z for x in rows[j]]
  for r in range(3):
   if r!=j:
    z=rows[r][j];rows[r]=[x-z*y for x,y in zip(rows[r],rows[j])]
 return [row[-1] for row in rows]

def dot(a,b):return sum(x*y for x,y in zip(a,b))

# Each segment pair is an LP in (u,v,E). Numerical optimization proposes a
# basis; exact primal and dual feasibility certify its optimal value.
word_minima={};count=0;certificates=[]
for word in product(range(3),repeat=3):
 best=None
 for j,first in enumerate(segments):
  for k in range(j,len(segments)):
   lo,hi,mu,bu=first; vlo,vhi,mv,bv=segments[k]
   A=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(-1,1,0),(0,0,1)]
   b=[lo,-hi,vlo,-vhi,F(0),F(0)]
   for i in range(3):
    p,q,r=[int(x==i) for x in word]
    A.extend([(mu[i]-p,0,1),(q-p,mv[i]-q,1),(q-p,r-q,1)])
    b.extend([-bu[i],-bv[i],r*L-terminal[i]])
   lp=linprog([0,0,1],A_ub=[[-float(x) for x in row] for row in A],b_ub=[-float(x) for x in b],bounds=[(None,None)]*3,method='highs')
   assert lp.success,(word,j,k,lp.message)
   active=[h for h in range(len(A)) if abs(dot(A[h],lp.x)-float(b[h]))<1e-7]
   found=None
   for inds in combinations(active,3):
    basis=[A[h] for h in inds];rhs=[b[h] for h in inds]
    x=solve(basis,rhs)
    if x is None or not all(dot(row,x)>=z for row,z in zip(A,b)):continue
    lam=solve(list(zip(*basis)),[0,0,1])
    if lam is None or min(lam)<0:continue
    assert x[2]==dot(lam,rhs)
    found=(inds,x,lam);break
   assert found is not None,(word,j,k,active)
   inds,x,lam=found
   assert x[2]>1,(word,j,k,x)
   count+=1
   if best is None or x[2]<best[0]:best=(x[2],x[0],x[1])
   certificates.append(dict(word=word,segments=(j,k),basis=inds,primal=list(map(str,x)),dual=list(map(str,lam))))
 word_minima[''.join(map(str,word))]=list(map(str,best))
minimum=min(F(v[0]) for v in word_minima.values())
print('Exact LP cell optima certified:',count)
print('Exact three-block one-sided instance optimum:',minimum,'=',float(minimum))
print('Optimal words:',{w:v for w,v in word_minima.items() if F(v[0])==minimum})
(outdir/'n3-exact-cell-certificates.json').write_text(json.dumps(certificates,indent=2)+'\n')
(outdir/'n3-word-minima.json').write_text(json.dumps(word_minima,indent=2)+'\n')

# Integer-scaled exhaustive check of heavy rounding, without implementing flow
# or first-repeat reordering. Every profile with a heavy mode must admit a
# full-error-one word with an adjacent repetition.
n=3; M=4
columns=[]
for i in range(n):
 for j in range(i,n):
  a=[0]*n;a[i]+=1;a[j]+=1;columns.append(a)
words=list(product(range(n),repeat=M))
heavy_count=0;feasible_repeated=0
for profile in product(columns,repeat=M):
 cumulative=[];a=[0]*n
 for col in profile:
  a=[x+y for x,y in zip(a,col)];cumulative.append(a)
 if max(a)<=2:continue
 heavy_count+=1;found=False
 for word in words:
  if all(x!=y for x,y in zip(word,word[1:])):continue
  N=[0]*n;good=True
  for p,A in zip(word,cumulative):
   N[p]+=2
   if any(abs(x-y)>2 for x,y in zip(N,A)):good=False;break
  if good:found=True;break
 assert found,profile
print('Exhaustive heavy-mode profiles admitting adjacent repetition:',heavy_count)

# Exact symbolic algebra of the plateau comparisons and asymptotic coefficients.
import sympy as s
n,h,x=s.symbols('n h x')
c2=(n-1)**3/(n*(3*n*n-3*n+1))
c3=(n-1)**4/(n*(4*n**3-6*n*n+4*n-1))
assert s.expand((n**3-9*n*n+11*n-4).subs(n,8+h))==h**3+15*h*h+59*h+20
assert s.expand((n**4-14*n**3+26*n*n-19*n+5).subs(n,12+h))==h**4+34*h**3+386*h*h+1469*h+65
assert s.series(c2.subs(n,1/x),x,0,3).removeO()==s.Rational(1,3)-2*x/3+2*x*x/9
assert s.series(c3.subs(n,1/x),x,0,3).removeO()==s.Rational(1,4)-5*x/8+5*x*x/16
print('Both shifted plateau polynomials and asymptotic expansions verified symbolically.')
