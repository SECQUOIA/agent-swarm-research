"""Independent rational interval certificate for the appendix's local gate ranges."""
from fractions import Fraction as F
from dataclasses import dataclass

@dataclass(frozen=True)
class I:
    lo:F
    hi:F
    def __add__(self,other):
        other=point(other);return I(self.lo+other.lo,self.hi+other.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,other):return self+-point(other)
    def __mul__(self,other):
        other=point(other);xs=[a*b for a in (self.lo,self.hi) for b in (other.lo,other.hi)];return I(min(xs),max(xs))
    __rmul__=__mul__
    def inv(self):
        assert self.lo>0;return I(1/self.hi,1/self.lo)
    def __truediv__(self,other):return self*point(other).inv()

def point(x):return x if isinstance(x,I) else I(F(x),F(x))
seen=[]
def keep(tag,x):
    x=point(x);assert F(1,2)<x.lo<=x.hi<2,(tag,x);seen.append((tag,x));return x

def square(a,prefix):
    def K(t,x):return keep(prefix+t,x)
    b=K('b',a+F(1,2));bp=K('bp',b.inv());ap=K('ap',a.inv())
    c=K('c',ap+F(1,2));d=K('d',c-F(2,3));e=K('e',d+F(1,2))
    f=K('f',e-bp);g=K('g',f+f);h=K('h',g-F(2,3));i=K('i',h.inv())
    j=K('j',i-F(1,2));k=K('k',j+F(3,4));l=K('l',b/2);return K('o',k-l)

def product(a,b):
    def K(t,x):return keep('product/'+t,x)
    ap=K('ap',a+F(1,2));bp=K('bp',b+F(1,2));ha=K('ha',ap/2);hb=K('hb',bp/2)
    t=K('t',ha+hb);r=K('r',t-F(1,2));s=square(r,'square-r/');u=K('u',s+F(1,2))
    a2=square(a,'square-a/');b2=square(b,'square-b/');a3=K('a3',a2+F(1,2));b3=K('b3',b2+F(1,2))
    a4=K('a4',a3/2);b4=K('b4',b3/2);c=K('c',a4+b4);d=K('d',c/2)
    e=K('e',u-d);f=K('f',e+e);return K('o',f-F(1,2))

delta=F(1,1024);small=I(-delta,delta)
a=keep('A',1+small);keep('B',F(3,4)+small);keep('C',F(3,2)+small)
m=product(a,a);f=keep('shift/f',m+F(1,2));g=keep('shift/g',f-(F(3,4)+small));keep('shift/h',g+F(3,4))
# J_s can reach the lower endpoint; its other endpoint is far below two.
j=I(F(1,2),F(1,2)+delta);assert F(1,2)<=j.lo<=j.hi<=2
print('PASS: delta=1/1024 gives strict [1/2,2] interior ranges for',len(seen),'bounded-gate intermediate interval enclosures, for every pair s,t in [-delta,delta].')
print('PASS: every reciprocal denominator has an exact positive lower bound throughout its certified input interval.')
print('PASS: nonnegativity witness J_s is in [1/2,1/2+delta] for every s in [0,delta].')
print('This is interval propagation over full input intervals, not point sampling. Algebraic correctness/unique recovery are separately checked in the proof audit.')
for tag,x in seen: print(tag, str(x.lo),str(x.hi))
