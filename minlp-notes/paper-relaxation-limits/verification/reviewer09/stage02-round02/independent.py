"""Independent exact checks; finite coupling samples supplement the proofs."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import prod
from pathlib import Path
import json
import sympy as s

root = Path(__file__).resolve().parents[3]
result = {}
for L in range(2, 11):
    m = 2**L
    B = lambda q: Q(L-q+2, 2**q)
    valid = [q for q in range(1,L) if B(q+1) <= 1 <= B(q)]
    answers = []
    for cutoff in valid:
        mix = (1-B(cutoff+1))/(B(cutoff)-B(cutoff+1))
        mass = failure = objective = Q(0)
        anchors = [Q(0)]*L
        for q,weight in ((cutoff,mix),(cutoff+1,1-mix)):
            for ell in range(L+1):
                probability = weight*Q(1,2**(ell+1) if ell<L else 2**L)
                R = 0 if ell<q else 2**(ell-q+1)
                mass += probability
                failure += probability*R
                failed = [int(format(i,f'0{L}b')[::-1],2) for i in range(R)]
                for j in range(1,L+1):
                    hits = len({i>>(L-j) for i in failed})
                    assert hits == min(2**j,R)
                    if j<=ell:
                        anchors[j-1] += probability
                        objective += probability*hits
        assert mass == failure == 1
        assert anchors == [Q(1,2**j) for j in range(1,L+1)]
        expected = cutoff+Q(L-cutoff,2**cutoff)
        assert objective == expected
        for ell,R in product(range(L+1),range(m+1)):
            offset=0 if ell<=cutoff else 2**(ell-cutoff+1)-2
            assert sum(min(2**j,R) for j in range(1,ell+1))<=cutoff*R+offset
        answers.append(expected)
    assert len(set(answers))==1
result['dyadic_exact'] = 'L=2,...,10; every admissible cutoff, all integer surrogate states, explicit prefix hits'

def orientation_expectation(means):
    total=Q(0)
    for dirs in product((0,1),repeat=len(means)):
        left=max([Q(0)]+[1-x for x,d in zip(means,dirs) if d])
        right=min([Q(1)]+[x for x,d in zip(means,dirs) if not d])
        total+=max(Q(0),right-left)
    return total/2**len(means)

def B_expectation(means):
    cuts=sorted({Q(0),Q(1)}|{x if x<=Q(1,2) else 2*(1-x) for x in means})
    value=Q(0)
    for l,r in zip(cuts,cuts[1:]):
        t=(l+r)/2
        probabilities=[Q(t<x) if x<=Q(1,2) else Q(1,2) if t<2*(1-x) else Q(1) for x in means]
        value+=(r-l)*prod(probabilities)
    return value

count=0
for degree in (2,3):
    for means in combinations_with_replacement([Q(i,12) for i in range(13)],degree):
        anchor=means[0]
        t=min(anchor,sum(1-x for x in means[1:]))
        deficiencies=[anchor-orientation_expectation(means),anchor-prod(means),anchor-B_expectation(means)]
        assert sum(w*d for w,d in zip((18,6,7),deficiencies))>=12*t
        count+=1
result['cubic_exact_grid'] = count

a,b,c,t=s.symbols('a b c t')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell=37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
h=F-ell
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c**2/4}))
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.expand(h.subs(stationary))
rows=[(p,0,s.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
 (p,s.Rational(1,5),s.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
 (r,s.Rational(3,10),s.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
 (r,s.Rational(1,2),s.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
 (r,s.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for poly,l,u,D,nums in rows:
    bern=sum(s.Rational(v,D)*s.binomial(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(nums))
    assert s.expand(poly.subs(c,l+(u-l)*t)-bern)==0
slack=min(s.Rational(v,D) for _,_,_,D,nums in rows for v in nums)
assert slack==s.Rational(901,120000)
assert (s.Rational(161,4)/(s.Rational(223,12)-slack))==s.Rational(1610000,743033)
assert s.expand(a*c**2+s.Rational(5,4)*a*a-s.Rational(11,6)*a-s.Rational(20,27)*c+s.Rational(95,108)-s.Rational(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0
assert s.expand(a*c**2+s.Rational(24,25)*a*a-s.Rational(41,25)*a-s.Rational(4,5)*c+s.Rational(68,75)-s.Rational(24,25)*(a-(41-25*c*c)/48)**2-(1-c)*(5*c-3)**2*(5*c+11)/480)==0
result['symbolic']='Hessian elimination; five exact Bernstein expansions; minimum slack; reduced limit; both two-level identities'
(Path(__file__).parent/'independent-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
