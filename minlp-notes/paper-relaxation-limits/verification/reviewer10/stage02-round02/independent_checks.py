"""Independent exact finite and symbolic checks; numerical checks labeled separately."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb, log, exp
from pathlib import Path
import json
import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq

out = {}

def orientation(x):
    total = Q(0)
    for bits in product((0, 1), repeat=len(x)):
        left = max([Q(0)] + [1-u for u,b in zip(x,bits) if b])
        right = min([Q(1)] + [u for u,b in zip(x,bits) if not b])
        total += max(Q(0), right-left)
    return min(x)-total/2**len(x)

def law_b(x):
    breaks = sorted({Q(0),Q(1)} | {u if u <= Q(1,2) else 2*(1-u) for u in x})
    value = Q(0)
    for l,r in zip(breaks,breaks[1:]):
        t=(l+r)/2
        prob=Q(1)
        for u in x:
            prob *= Q(t<=u) if u<=Q(1,2) else (Q(1,2) if t<=2*(1-u) else Q(1))
        value+=(r-l)*prob
    return min(x)-value

checks=0
grid=sorted({Q(i,20) for i in range(21)}|{Q(1,1000),Q(499,1000),Q(501,1000),Q(999,1000)})
for n in (2,3):
    for x in combinations_with_replacement(grid,n):
        t=min(x)-max(Q(0),sum(x)-n+1)
        di=min(x)-s.prod(x)
        assert 18*orientation(x)+6*di+7*law_b(x)>=12*t,(x,t)
        checks+=1
out['exact_direct_cubic_and_quadratic_law_tuples']=checks

for L in range(2,11):
    w=[Q(1,2**(l+1)) for l in range(L)]+[Q(1,2**L)]
    B=lambda q:Q(L-q+2,2**q)
    cutoff=next(k for k in range(1,L) if B(k+1)<=1<=B(k))
    theta=(1-B(cutoff+1))/(B(cutoff)-B(cutoff+1))
    er=score=Q(0)
    for q,weight in ((cutoff,theta),(cutoff+1,1-theta)):
        for l in range(L+1):
            r=0 if l<q else 2**(l-q+1)
            er+=weight*w[l]*r
            score+=weight*w[l]*sum(min(2**j,r) for j in range(1,l+1))
    assert er==1 and score==cutoff+Q(L-cutoff,2**cutoff)
    for l,r in product(range(L+1),range(2**L+1)):
        cap=0 if l<=cutoff else 2**(l-cutoff+1)-2
        assert sum(min(2**j,r) for j in range(1,l+1))<=cutoff*r+cap
    for r in range(2**L+1):
        labels=[int(format(i,f'0{L}b')[::-1],2) for i in range(r)]
        for j in range(1,L+1):
            assert len({v>>(L-j) for v in labels})==min(2**j,r)
out['exact_dyadic_L']=list(range(2,11))

a,b,c,t=s.symbols('a b c t')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
h=F-37*a-s.Rational(79,2)*b-38*c+s.Rational(103,3)
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c*c/4}))
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.expand(h.subs(stationary))
rows=[(p,0,s.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
      (p,s.Rational(1,5),s.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
      (r,s.Rational(3,10),s.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
      (r,s.Rational(1,2),s.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
      (r,s.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for poly,l,u,D,v in rows:
    bern=sum(s.Rational(vv,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,vv in enumerate(v))
    assert s.expand(poly.subs(c,l+(u-l)*t)-bern)==0
delta=min(Q(vv,D) for _,_,_,D,v in rows for vv in v)
assert delta==Q(901,120000)
assert Q(161,4)/(Q(223,12)-delta)==Q(1610000,743033)
for lam,la,lc,l0,center,rem in [
    (s.Rational(5,4),s.Rational(11,6),s.Rational(20,27),-s.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
    (s.Rational(24,25),s.Rational(41,25),s.Rational(4,5),-s.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert s.expand(a*c*c+lam*a*a-la*a-lc*c-l0-lam*(a-center)**2-rem)==0
out['exact_symbolic']='Five Bernstein rows, both convex eliminations, strongest fraction, both two-level identities passed'

numeric=0
for d in (2,3,10,100,10000):
    for multiple in (1,2,10,100):
        M=(d-1)*multiple
        Lambda=1+log(M); eta=(d-1)/M
        J=lambda z:quad(lambda v:1-exp(-(1-eta*v)/(Lambda*v)),z,1,epsabs=1e-12)[0]
        zeta=brentq(lambda z:J(z)-z,1e-12,1-1e-12,xtol=1e-13)
        w=float(s.LambertW(Lambda*exp(-eta)))
        if w>=1: assert zeta+1e-11>=(w-1/(2*w))/Lambda
        for prob in (0.00001,0.1,0.499):
            hp=min(M*prob,1); Ap=1+log(hp/prob)
            integral=quad(lambda v:min(1,prob/v)/Ap,0,hp,points=[prob],epsabs=1e-12)[0]
            assert abs(integral-prob)<1e-9
        numeric+=1
out['numerical_harmonic_parameter_cases']=numeric
print(json.dumps(out,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
