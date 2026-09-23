import sympy as s
from fractions import Fraction as F
x,k,n,C=s.symbols('x k n C')
f=((n-1)**2*C+1)/(n*(n-1)*(1+C))
assert s.factor(f-F(1,1)/n)==(n-2)*(C*n-C-1)/(n*(C+1)*(n-1))
assert s.factor(s.diff(f,C))==(n-2)/((C+1)**2*(n-1))
elementary=(n*(n-1)+(n-k)*(n-k-1))/(n*k*(2*n-k-1))
assert s.simplify(elementary-1/(k+1)-2*(n-k-1)*(n-k*(k+1)/2)/(n*k*(k+1)*(2*n-k-1)))==0
for ell in range(1,5):
 d=k-ell;a=1-d*x;b=1-(d+1)*x
 N=s.expand(2*b**(ell+1)-a**ell*b)
 D=s.expand((1-x)*a**(ell-1))
 # Cancel the exact common x in the c-transform, then do three formal
 # coefficient divisions. This verifies the formulas with symbolic k.
 numerator=s.Poly(D+N,x);denominator=s.Poly(s.cancel((D-N)/x),x)
 coeff=[]
 for j in range(3):
  coeff.append(s.factor((numerator.nth(j)-sum(denominator.nth(h)*coeff[j-h] for h in range(1,j+1)))/denominator.nth(0)))
 expected=[1/k,-(k+1)/(2*k),(3*k**3-3*k-2*ell**3+2*ell)/(12*k*k)]
 assert all(s.simplify(a-b)==0 for a,b in zip(coeff,expected))
 gap=s.factor(coeff[2]-(k*k-1)/(12*k))
 assert s.simplify(gap-(k-ell)*(k*k+k*ell+ell*ell-1)/(6*k*k))==0
 print('Symbolic seed series verified for ell=',ell,'coefficient=',coeff[2])

count=0
for nn in range(5,81):
 for kk in range(4,nn):
  m=nn-kk+4
  theta=F(m*(m-1),nn*(nn-1))*(2*F(m-1,m)**4-1)
  c=(1+theta)/(nn*(1-theta))
  old=F(nn*(nn-1)+(nn-kk)*(nn-kk-1),nn*kk*(2*nn-kk-1))
  lhs=(nn+kk+1)*(m-1)*(2*(m-1)**4-m**4)
  rhs=(nn-kk-1)*nn*(nn-1)*m**3
  assert (c<=F(1,kk+1))==(lhs<=rhs)
  assert c<old
  assert (c<F(1,nn))==(m in (5,6))
  count+=1
  if (nn,kk)==(16,5):
   assert c==F(588449,3544816)<F(1,6)<old==F(35,208)
  if (nn,kk)==(17,5):assert c>F(1,6)
print('Strict seed comparison, sign, integer plateau equivalence:',count,'cases')
