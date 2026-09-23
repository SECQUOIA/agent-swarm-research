"""Independent exact spot checks for pooling Sections 1--2 (not a proof)."""
from fractions import Fraction as F
from itertools import product
import sympy as s

values = sorted({F(a,b) for b in range(1,17) for a in range(1,33) if F(1,2)<=F(a,b)<=2})
count=0
for v in values:
    bar=F(5,2)-v
    assert F(1,2)<=bar<=2
    for a in (v,bar,1/v,1/bar):
        d=1/a
        assert 0<=2-d<=2
        assert (a/7)*d==2*F(1,14)
        assert d+(2-d)==2  # emission product and conversion product
        assert 7-a>=5
        assert 7-2*d>=3  # two worst identical non-slack emissions
        count+=1
for x,y in product(values,repeat=2):
    z=x+y
    if z<=2:
        assert (F(5,2)-x-y)/(7*(F(5,2)-z))==F(1,7)
        tau=2/z
        assert 1<=tau<=2
        assert z*tau==2 and (x+y)*tau==2
    y_inv=1/x
    assert (x/7)*y_inv==F(5,2)*F(2,35)

# A complete one-pool instance including repeated-summand normalization,
# self-inversion, range-only, and unused variables.
X={'x':F(1,2),'y':F(1),'z':F(3,2),'two':F(2),
   'one':F(1),'unused':F(7,6),'copy':F(1,2),'u':F(2)}
inv=[('x','two'),('one','one'),('x','u'),('u','copy')]
add=[('x','y','z'),('x','copy','y')]
aux=[]
pins=[]
for x,y in inv:
    h1=len(aux);aux.append(X[y]);h2=len(aux);aux.append(1/X[y])
    pins += [(h1,{x},F(1,2)),(h2,{('aux',h1)},F(1,2)),(h2,{y},F(1,2))]
for x,y,z in add:
    h=len(aux);aux.append(2/X[z]);pins += [(h,{z},F(1)),(h,{x,y},F(1))]
inv_vars={v for pair in inv for v in pair}
for v in X:
    if v not in inv_vars:
        h=len(aux);aux.append(1/X[v]);pins.append((h,{v},F(1,2)))
N=len(X)+len(aux);B=4*N
intakes=dict(X);intakes.update({('aux',h):a for h,a in enumerate(aux)})
filler=B-sum(intakes.values());slack=B-sum(aux)
assert F(B,2)<=filler<=B and F(B,2)<=slack<=B
assert sum(intakes.values())+filler==sum(aux)+slack==B
for h,support,kappaB in pins:
    assert ('aux',h) not in support
    q=sum(intakes[a] for a in support)/B
    assert q*aux[h]==2*kappaB/B
for a in aux: assert 0<=a<=2 and a+(2-a)==2
profit=sum(aux)+slack+2*sum(2-a for a in aux)+2*sum(aux)
assert profit==B+4*len(aux)

# Sign-safe Cramer transformation with positive, negative, singular bases.
t=s.symbols('t');C=s.Matrix([[t,1],[0,t-1]]);d=s.Matrix([1,t])
Delta=C.det();U=C.adjugate()*d
for tv in (F(-2),F(-1),F(0),F(1,2),F(1),F(2)):
    de=Delta.subs(t,tv)
    if de==0: continue
    for a,b in ((s.Matrix([[1,0]]),F(3)),(s.Matrix([[-1,2]]),F(-1))):
        raw=(a*U)[0]/Delta-b
        cleared=((a*U)[0]-b*Delta)*Delta
        assert (raw.subs(t,tv)<=0)==(cleared.subs(t,tv)<=0)

# Irrational example's derivative and exact feasible optimum.
t=s.symbols('t',positive=True);h=t/(t-1)-2*t;t0=(1+s.sqrt(3))/2
assert s.simplify(h.subs(t,t0)-1)==0
b=(s.sqrt(3)-1)/2
assert s.simplify(2*b*b+2*b-1)==0
assert s.simplify(3+2*b-b-(5+s.sqrt(3))/2)==0
print(f'PASS: {len(values)} rational variable values; {count} storage/emission checks; all addition pairs; complete one-pool pins and saturation; determinant signs; irrational optimum identities.')
