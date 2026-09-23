from fractions import Fraction as Q
from itertools import product,combinations_with_replacement
from random import Random
from scipy.optimize import linprog
import sympy as sy

# Independent exact implementation of the reordering construction.
def cumul(cols,t):
 return [sum((max(Q(0),min(Q(1),t-j))*a[i] for j,a in enumerate(cols)),Q(0)) for i in range(len(cols[0]))]
def error(cols,word):
 n=len(cols[0]); occ=[0]*n; err=0
 for j,w in enumerate(word,1):
  occ[w]+=1; err=max(err,max(abs(a-o) for a,o in zip(cumul(cols,Q(j)),occ)))
 return err

def deadline(cols,i,r):
 out=Q(0); a=Q(0)
 for j in range(r):
  b=a+cols[j][i]
  if b<=1: out=Q(j+1)
  elif a<=1: return Q(j)+(1-a)/cols[j][i]
  else: break
  a=b
 return out

def reorder(cols,w):
 seen=set()
 for r,q in enumerate(w,1):
  if q in seen: break
  seen.add(q)
 else: return None
 d=deadline(cols,q,r)
 ceil=-((-d.numerator)//d.denominator)
 j=min(r-2,max(0,ceil-2))
 other=[i for i in w[:r] if i!=q]
 other.sort(key=lambda i:deadline(cols,i,r))
 return tuple(other[:j]+[q,q]+other[j:])+w[r:]

columns=[]
for i,j in combinations_with_replacement(range(3),2):
 columns.append(tuple(Q((a==i)+(a==j),2) for a in range(3)))
count=0; heavy=0
for cols in product(columns,repeat=4):
 found=False
 for w in product(range(3),repeat=4):
  if error(cols,w)>1: continue
  ww=reorder(cols,w)
  if ww is not None:
   assert error(cols,ww)<=1,(cols,w,ww)
   assert any(ww[i]==ww[i+1] for i in range(3))
   assert sorted(w)==sorted(ww)
   found=True; count+=1
 if max(cumul(cols,Q(4)))>1:
  assert found
  heavy+=1
print('PASS heavy/reorder:',count,'valid words and',heavy,'heavy profiles')

# Independent minimization for every length-three mode word on the published
# rational input, using all cells containing each switch. Numerical LP checks
# supplement the analytic strict exclusion, not replace it.
rows=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[Q(row[0],146) for row in rows]+[Q(57,8)]
alloc=[[Q(x,146) for x in row[1:]] for row in rows]
alloc.append([a+(knots[-1]-knots[-2])/3 for a in alloc[-1]])
slopes=[[(b-a)/(y-x) for a,b in zip(aa,bb)] for x,y,aa,bb in zip(knots,knots[1:],alloc,alloc[1:])]
assert all(0<=a<=Q(3,4) for col in slopes for a in col)
assert all(sum(col)==1 for col in slopes)
intercepts=[[a-s*x for a,s in zip(aa,ss)] for aa,ss,x in zip(alloc,slopes,knots)]
assert alloc[-1]==[Q(5281,1752),Q(3985,1752),Q(3217,1752)]
minimum=(1e9,None); programs=0
for w in product(range(3),repeat=3):
 for a in range(len(slopes)):
  for b in range(a,len(slopes)):
   # variables u,v,E; impose W_i(t)-A_i(t)<=E at u,v,L.
   mat=[[1,-1,0]]; rhs=[0]
   for i in range(3):
    p,q,r=[int(z==i) for z in w]
    mat.append([p-slopes[a][i],0,-1]);rhs.append(intercepts[a][i])
    mat.append([p-q,q-slopes[b][i],-1]);rhs.append(intercepts[b][i])
    mat.append([p-q,q-r,-1]);rhs.append(alloc[-1][i]-r*knots[-1])
   res=linprog([0,0,1],A_ub=mat,b_ub=rhs,bounds=[(knots[a],knots[a+1]),(knots[b],knots[b+1]),(0,None)],method='highs')
   assert res.success
   assert res.fun>1.0+1e-9,(w,a,b,res.fun)
   if res.fun<minimum[0]:minimum=(res.fun,(w,a,b,res.x.tolist()))
   programs+=1
print('PASS all-word minimum-error LP:',programs,'programs; minimum',minimum)

n,h=sy.symbols('n h')
p2=n**3-9*n**2+11*n-4
p3=n**4-14*n**3+26*n**2-19*n+5
assert sy.expand(p2.subs(n,8+h))==h**3+15*h**2+59*h+20
assert sy.expand(p3.subs(n,12+h))==h**4+34*h**3+386*h**2+1469*h+65
x=sy.symbols('x')
f2=(n-1)**3/(n*(3*n*n-3*n+1))
f3=(n-1)**4/(n*(4*n**3-6*n*n+4*n-1))
assert sy.series(f2.subs(n,1/x),x,0,3).removeO()==sy.Rational(1,3)-2*x/3+2*x*x/9
assert sy.series(f3.subs(n,1/x),x,0,3).removeO()==sy.Rational(1,4)-5*x/8+5*x*x/16
print('PASS transition polynomials and asymptotic coefficients')
