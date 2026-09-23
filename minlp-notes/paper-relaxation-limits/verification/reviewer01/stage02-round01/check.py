"""Independent exact checks of frozen Stage 2 certificates (no optimizer)."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, prod
import json
from pathlib import Path
import sympy as S

out = {}
cases = [
    (6, (2,3,9,10,7,7), (962,778,842,-4816), 13,
     [((1,4,4),Q(17,26)),((2,1,6),Q(4,13)),((6,2,1),Q(1,26))]),
    (8, (2,3,13,12,8,7), (793,770,798,-5882), 7,
     [((1,2,8),Q(2,7)),((1,5,6),Q(4,7)),((8,4,2),Q(1,7))]),
    (64,(2,3,120,105,70,63),(871710,900446,899046,-51743768),105,
     [((4,19,64),Q(241,735)),((5,19,64),Q(12,735)),
      ((16,40,43),Q(419,735)),((64,31,17),Q(63,735))]),
]
def value(state, co):
    a,b,c = state
    return (co[0]*c*(c-1)*(c-2)//6 + co[1]*b*c*(c-1)//2
            +co[2]*b*(b-1)//2+co[3]*a*c+co[4]*a*b+co[5]*a*(a-1)//2)
records = []
for m,co,dual,D,law in cases:
    residual_by_c = [min(D*value((a,b,c),co)-sum(z*t for z,t in zip((a,b,c,1),dual))
                         for a,b in product(range(m+1),repeat=2)) for c in range(m+1)]
    assert min(residual_by_c) == 0
    assert sum(p for _,p in law) == 1 and min(p for _,p in law)>=0
    means = [sum(p*st[j] for st,p in law) for j in range(3)]
    assert means == [Q(m,4),Q(m,2),Q(3*m,4)]
    vex = sum(p*value(st,co) for st,p in law)
    assert vex == sum(z*t for z,t in zip(means+[1],dual))/D
    counts = [comb(m,3),m*comb(m,2),comb(m,2),m*m,m*m,comb(m,2)]
    cav = sum(c*n*u for c,n,u in zip(co,counts,[Q(3,4),Q(1,2),Q(1,2),Q(1,4),Q(1,4),Q(1,4)]))
    lower = Q(co[0]*comb(m,3),4)
    records.append({'n':3*m,'vex':str(vex),'cav':str(cav),'H':str(cav-vex),
                    'ratio':str((cav-lower)/(cav-vex)), 'states':(m+1)**3})
    if m == 8:
        assert residual_by_c == [168,42,0,30,22,0,0,16,0]
out['finite_cubics'] = records

a,b,c,t = S.symbols('a b c t')
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
h = F-37*a-S.Rational(79,2)*b-38*c+S.Rational(103,3)
p = S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c**2/4}))
stationary = S.solve([S.diff(h,a),S.diff(h,b)],[a,b])
r = S.expand(h.subs(stationary))
rows = [
 (p,0,S.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
 (p,S.Rational(1,5),S.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
 (r,S.Rational(3,10),S.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
 (r,S.Rational(1,2),S.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
 (r,S.Rational(3,4),1,190464,[15869,22508,34520,45920,31040]),
]
for pol,lo,hi,D,vs in rows:
    expansion = sum(S.Rational(v,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vs))
    assert S.expand(pol.subs(c,lo+(hi-lo)*t)-expansion)==0
delta = min(Q(v,D) for _,_,_,D,vs in rows for v in vs)
assert delta == Q(901,120000)
assert Q(161,4)/(Q(223,12)-delta) == Q(1610000,743033)
for k,al,cl,cn,center,residue in [
 (S.Rational(5,4),S.Rational(11,6),S.Rational(20,27),S.Rational(-95,108),
  (11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
 (S.Rational(24,25),S.Rational(41,25),S.Rational(4,5),S.Rational(-68,75),
  (41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert S.expand(a*c*c+k*a*a-al*a-cl*c-cn-k*(a-center)**2-residue)==0
out['symbolic'] = {'bernstein_rows':5,'minimum_coefficient':str(delta),'two_level_identities':2}

# Integrate O and B from their definitions, without using the case formulas.
def expectation_O(xs):
    return sum(max(Q(0),min(x if not o else Q(1) for x,o in zip(xs,os))
                   -max(Q(0) if not o else 1-x for x,o in zip(xs,os)))
               for os in product((0,1),repeat=len(xs)))/2**len(xs)
def expectation_B(xs):
    cuts = sorted({Q(0),Q(1),*[x if x<=Q(1,2) else 2*(1-x) for x in xs]})
    return sum((hi-lo)*prod((int(mid<=x) if x<=Q(1,2) else
                             Q(1,2) if mid<=2*(1-x) else Q(1)) for x in xs)
               for lo,hi in zip(cuts,cuts[1:]) for mid in [(lo+hi)/2])
number = 0
for degree in (2,3):
    for xs in combinations_with_replacement([Q(i,12) for i in range(13)],degree):
        u=min(xs)
        gap=u-max(Q(0),sum(xs)-degree+1)
        D=18*(u-expectation_O(xs))+6*(u-prod(xs))+7*(u-expectation_B(xs))
        assert D>=12*gap,(xs,D,gap)
        number+=1
out['exact_rational_rounding_checks'] = number

# Integer count dual and its one-state primal, independently of cubic table code.
mins=[min(2*(a*c*(c-1)//2+20*a*(a-1)//2)-428*a-177*c+3372
          for c in range(17)) for a in range(17)]
assert mins==[540,352,204,96,28,0,9,7,0,0,19,63,132,235,369,540,742]
assert 8*12*11//2+20*8*7//2==1088
assert Q(2160,1072)==Q(135,67)
assert Q(2160)/(1072+Q(12,5))==Q(2700,1343)
assert Q(943)-2*Q(80947,175)==Q(3131,175)
assert Q(3131,2275)-Q(1,2)>0
assert 25002-Q(1000**3,23200)<0
out['finite_refinements'] = 'two-level dual; 25-, 52-, and 25,000-variable arithmetic passed'

# Exact dyadic two-profile resources, affine dual, and prefix realization.
for L in range(2,13):
    m=2**L
    w=[Q(1,2**(l+1)) for l in range(L)]+[Q(1,m)]
    B=lambda q:Q(L-q+2,2**q)
    for s in range(1,L):
        if not B(s+1)<=1<=B(s): continue
        lam=(1-B(s+1))/(B(s)-B(s+1))
        countmean=payoff=Q(0)
        for q,weight in [(s,lam),(s+1,1-lam)]:
            for l in range(L+1):
                R=0 if l<q else 2**(l-q+1)
                countmean+=weight*w[l]*R
                payoff+=weight*w[l]*sum(min(2**j,R) for j in range(1,l+1))
        assert countmean==1 and payoff==s+Q(L-s,2**s)
        for l in range(L+1):
            intercept=0 if l<=s else 2**(l-s+1)-2
            for R in range(m+1):
                assert sum(min(2**j,R) for j in range(1,l+1))<=s*R+intercept
    if L<=7:
        rev=[int(f'{i:0{L}b}'[::-1],2) for i in range(m)]
        for R in range(m+1):
            for j in range(1,L+1):
                assert len({v>>(L-j) for v in rev[:R]})==min(2**j,R)
out['dyadic'] = 'exact resources and affine dual L=2..12; all prefix counts L=2..7'
print(json.dumps(out,indent=2))
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
