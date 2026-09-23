"""Independent exact Stage 2 review checks; finite tests are not universal proofs."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb
import re
import sympy as S

here = Path(__file__).resolve().parent
snap = here.parents[2] / 'process/snapshots/stage02-round02'
tex = (snap/'sections/appendix-cubic-certificates.tex').read_text()
blocks = re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}', tex, re.S)
assert len(blocks) == 2
printed = ''.join(blocks)
assert printed == (snap/'verification/check_stage02_finite.py').read_text()
exec(compile(printed, 'frozen-printed-certificate', 'exec'), {})
print('Printed certificate: both blocks match executable exactly.')

# Derive the scalar elimination directly from F and its gradient.
a,b,c,m,t = S.symbols('a b c m t')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell=37*a+S.Rational(79,2)*b+38*c-S.Rational(103,3)
h=F-ell
assert S.hessian(h,(a,b)).det()==248
bstar=S.Rational(13,24)-3*c**2/4
p=S.expand(h.subs({a:1,b:bstar}))
opt=S.solve([S.diff(h,a), S.diff(h,b)], (a,b))
r=S.expand(h.subs(opt))
rows=[(p,0,S.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
 (p,S.Rational(1,5),S.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
 (r,S.Rational(3,10),S.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
 (r,S.Rational(1,2),S.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
 (r,S.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for poly,lo,hi,D,v in rows:
    assert S.expand(poly.subs(c,lo+(hi-lo)*t)-sum(S.Rational(v[i],D)*comb(4,i)*t**i*(1-t)**(4-i) for i in range(5)))==0
delta=min(S.Rational(vv,D) for _,_,_,D,v in rows for vv in v)
assert delta==S.Rational(901,120000)
assert S.Rational(161,4)/(S.Rational(223,12)-delta)==S.Rational(1610000,743033)
f=2*(m*c)*(m*c-1)*(m*c-2)/6+3*m*b*(m*c)*(m*c-1)/2+2*m*(m*b)*(m*b-1)/2+5*m*(m*a)*(m*c)/3+10*m*(m*a)*(m*b)/9+m*(m*a)*(m*a-1)/2
assert S.expand(18*f/m**3-F+(18*c*c+27*b*c+18*b+9*a)/m-12*c/m**2)==0
num=S.Rational(161,4)-S.Rational(135,4)/m+6/m**2
den=S.Rational(223,12)+S.Rational(135,4)/m+9/m**2
assert (num/den).subs(m,36)==S.Rational(16985,8436)
assert (num/(den-delta)).subs(m,36)==S.Rational(42462500,21081891)
for lam,aa,cc,dd,square,rest in [
 (S.Rational(5,4),S.Rational(11,6),S.Rational(20,27),S.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
 (S.Rational(24,25),S.Rational(41,25),S.Rational(4,5),S.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert S.expand(a*c*c+lam*a*a-aa*a-cc*c+dd-lam*(a-square)**2-rest)==0
assert Q(3225,7)+Q(46,25)==Q(80947,175)
assert Q(943)-2*Q(80947,175)==Q(3131,175)
assert Q(3131,2275)-Q(1,2)>0
assert 25002-Q(1000**3,23200)<0
assert Q(2160)/(Q(1072)+Q(12,5))==Q(2700,1343)
print('Exact symbolic eliminations, Bernstein identities, count expansion, both SOS identities and finite constants passed.')

# Exact dyadic resources, all integer r for L<=12, and bit-reversal prefix counts.
for L in range(2,13):
    mm=2**L
    weights=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    B=lambda q: Q(L-q+2,2**q)
    candidates=[s for s in range(1,L) if B(s+1)<=1<=B(s)]
    for s in candidates:
        mix=(1-B(s+1))/(B(s)-B(s+1))
        assert 0<=mix<=1
        cost=0
        for q,theta in [(s,mix),(s+1,1-mix)]:
            resource=0
            for l,wl in enumerate(weights):
                rr=0 if l<q else 2**(l-q+1)
                resource+=wl*rr
                cap=0 if l<=s else 2**(l-s+1)-2
                assert sum(min(2**j,rr) for j in range(1,l+1))==s*rr+cap
                cost+=theta*wl*(s*rr+cap)
            assert resource==B(q)
        assert cost==s+Q(L-s,2**s)
        for l in range(L+1):
            cap=0 if l<=s else 2**(l-s+1)-2
            assert all(sum(min(2**j,rr) for j in range(1,l+1))<=s*rr+cap for rr in range(mm+1))
    assert all(sum(weights[j:])==Q(1,2**j) for j in range(1,L+1))
    if L<=8:
        rev=[int(format(i,f'0{L}b')[::-1],2) for i in range(mm)]
        for j in range(1,L+1):
            prefixes=set()
            for rr in range(mm+1):
                assert len(prefixes)==min(2**j,rr)
                if rr<mm: prefixes.add(rev[rr]>>(L-j))
print('Dyadic exact certificates L=2..12, prefix realization L=2..8 passed.')

# Independently integrate actual O and B laws on rational breakpoints.
def prod(xs):
    out=Q(1)
    for x in xs: out*=x
    return out
def Oexpect(xs):
    total=Q(0)
    for orientations in product([0,1],repeat=len(xs)):
        lo=max([Q(0)]+[1-x for x,o in zip(xs,orientations) if o])
        hi=min([Q(1)]+[x for x,o in zip(xs,orientations) if not o])
        total+=max(Q(0),hi-lo)
    return total/2**len(xs)
def Bexpect(xs):
    breaks=sorted(set([Q(0),Q(1)]+[x if x<=Q(1,2) else 2*(1-x) for x in xs]))
    total=Q(0)
    for lo,hi in zip(breaks,breaks[1:]):
        mid=(lo+hi)/2
        probs=[Q(mid<=x) if x<=Q(1,2) else Q(1,2) if mid<=2*(1-x) else Q(1) for x in xs]
        total+=(hi-lo)*prod(probs)
    return total
grid=[Q(i,16) for i in range(17)]
checked=0
for degree in [2,3]:
    for xs in combinations_with_replacement(grid,degree):
        u=xs[0]
        gap=min(u,sum(1-x for x in xs[1:]))
        deficiency=18*(u-Oexpect(xs))+6*(u-prod(xs))+7*(u-Bexpect(xs))
        assert deficiency>=12*gap,(xs,deficiency,gap)
        checked+=1
print(f'Actual cubic/quadratic mixtures: {checked} rational tuples passed (finite corroboration only).')
