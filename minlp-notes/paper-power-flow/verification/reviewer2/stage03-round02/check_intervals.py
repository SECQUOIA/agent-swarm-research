"""Independent exact interval certification for composed arithmetic gate ranges."""
from fractions import Fraction as F
import sympy as s
class Interval:
 def __init__(self,lo,hi=None):self.lo=F(lo);self.hi=F(lo if hi is None else hi)
 def __add__(self,o):
  o=asint(o);return Interval(self.lo+o.lo,self.hi+o.hi)
 __radd__=__add__
 def __neg__(self):return Interval(-self.hi,-self.lo)
 def __sub__(self,o):return self+-asint(o)
 def __mul__(self,o):
  o=asint(o);vals=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)];return Interval(min(vals),max(vals))
 __rmul__=__mul__
 def inv(self):
  assert self.lo>0;return Interval(1/self.hi,1/self.lo)
 def __truediv__(self,o):return self*asint(o).inv()
def asint(x):return x if isinstance(x,Interval) else Interval(x)
count=0
margin=F(100)
def keep(x):
 global count,margin
 assert F(1,2)<x.lo<=x.hi<2,(x.lo,x.hi)
 margin=min(margin,x.lo-F(1,2),2-x.hi);count+=1;return x
half=F(1,2);tq=F(3,4);tt=F(2,3)
def square(a):
 b=keep(a+half);bp=keep(b.inv());ap=keep(a.inv())
 c=keep(ap+half);d=keep(c-tt);e=keep(d+half);f=keep(e-bp)
 g=keep(f+f);h=keep(g-tt);i=keep(h.inv())
 j=keep(i-half);k=keep(j+tq);l=keep(b/2);o=keep(k-l)
 return o
def multiply(a,b):
 ap=keep(a+half);bp=keep(b+half);ha=keep(ap/2);hb=keep(bp/2)
 t=keep(ha+hb);r=keep(t-half);sq=square(r);u=keep(sq+half)
 a2=square(a);b2=square(b);a3=keep(a2+half);b3=keep(b2+half)
 a4=keep(a3/2);b4=keep(b3/2);c=keep(a4+b4);d=keep(c/2)
 e=keep(u-d);f=keep(e+e);o=keep(f-half)
 return o
delta=F(1,2**16);small=Interval(-delta,delta)
a=keep(small+1);b=keep(small+1)
Bs=keep(small+tq);Bt=keep(small+tq);Cs=keep(small+F(3,2));Bu=keep(small+tq)
m=multiply(a,b);f=keep(m+half);g=keep(f-Bt);h=keep(g+tq)
assert F(1,2)<=F(1,2)+delta<=2
print(f'PASS: exact rational interval arithmetic certifies {count} composed gate variables for delta=2^-16, with strictly positive common endpoint margin {float(margin):.8f}.')
# Independent symbolic identities rather than a grid of satisfying assignments.
a,b=s.symbols('a b')
central=s.factor(2*(1/a+s.Rational(1,3)-1/(a+s.Rational(1,2)))-s.Rational(2,3))
assert s.cancel(central-1/(a*(a+s.Rational(1,2)) ))==0
out=1/central-s.Rational(1,2)+s.Rational(3,4)-(a+s.Rational(1,2))/2
assert s.cancel(out-a*a)==0
r=(a+b)/2;d=(a*a+b*b+1)/4
assert s.expand(2*(r*r+s.Rational(1,2)-d)-s.Rational(1,2)-a*b)==0
print('PASS: exact reciprocal-to-square and three-square-to-product identities.')
# Source preprocessing counterexample has multiple nonnegative extensions.
for u in (F(0),F(1),F(2),F(1000)):
 x,y,v=F(-1,2),F(1,2),F(1,2)
 assert (x-u)*(y-v)==0
print('PASS: inactive Boolean branch has arbitrarily many auxiliary extensions.')
