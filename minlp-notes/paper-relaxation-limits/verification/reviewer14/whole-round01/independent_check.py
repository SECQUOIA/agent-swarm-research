"""Bounded exact checks independently assembled for final review14."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import sympy as s

out = {}
# Polarization: all real-coefficient patterns from {-1,0,1} on K4.
edges = list(combinations(range(4), 2))
signs = list(product((-1, 1), repeat=4))
for weights in product((-1, 0, 1), repeat=6):
    vals = [sum(a*x[i]*x[j] for a,(i,j) in zip(weights,edges)) for x in signs]
    radius = Q(max(vals)-min(vals),2)
    polarized = max(sum(a*x[i]*x[j] for a,(i,j) in zip(weights,edges)
                        if ((mask>>i)&1) != ((mask>>j)&1))
                    for mask in range(16) for x in signs)
    assert radius == polarized
out['polarization_exact_patterns'] = 3**6

# General-radix affine cap and attaining resource profiles, including ties.
radix_cases = 0
for b in range(2,9):
    for L in range(2,16):
        M = lambda q: Q((L-q)*(b-1)+b,b**q)
        candidates = [q for q in range(1,L) if M(q+1)<=1<=M(q)]
        assert candidates
        for q in candidates:
            weights=[Q(b-1,b**(l+1)) for l in range(L)]+[Q(1,b**L)]
            mix=(1-M(q+1))/(M(q)-M(q+1))
            mean = objective = Q(0)
            for choice,prob in [(q,mix),(q+1,1-mix)]:
                for l,wl in enumerate(weights):
                    R=b**(l-choice+1) if l>=choice else 0
                    val=sum(min(b**j,R) for j in range(1,l+1))
                    cap=q*R+sum(b**j for j in range(1,max(0,l-q)+1))
                    assert val==cap
                    mean+=prob*wl*R; objective+=prob*wl*val
            assert mean==1 and objective==q+Q(L-q,b**q)
            radix_cases+=1
out['radix_exact_cutoffs'] = radix_cases

# Homogeneous Gram expansion as polynomial identities in real t.
t=s.symbols('t'); gram_entries=0
def falling(v,a):
    return s.prod(v-i for i in range(a))
for d in range(1,5):
    for n in range(2*d,2*d+5):
        for overlap in range(d+1):
            rhs=sum(comb(overlap,j)*falling(t,2*d-j)*falling(n-t,j)
                    for j in range(overlap+1))/falling(n,2*d)
            lhs=falling(t,2*d-overlap)/falling(n,2*d-overlap)
            assert s.cancel(lhs-rhs)==0
            gram_entries+=1
out['symbolic_gram_entries'] = gram_entries

# The exact five Bernstein identities, including their minimum slack.
c,z=s.symbols('c z')
p=(-972*c**4+576*c**3+1404*c**2-768*c+101)/96
r=(-78732*c**4+212256*c**3-203796*c**2+82032*c-11275)/2976
rows=[(p,0,Q(1,5),60000,[63125,39125,20975,9395,4133]),
      (p,Q(1,5),Q(3,10),240000,[16532,6008,1802,3788,11597]),
      (r,Q(3,10),Q(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
      (r,Q(1,2),Q(3,4),190464,[25808,18056,7964,9230,15869]),
      (r,Q(3,4),1,190464,[15869,22508,34520,45920,31040])]
for poly,l,u,D,v in rows:
    basis=sum(s.Rational(v[i],D)*comb(4,i)*z**i*(1-z)**(4-i) for i in range(5))
    assert s.expand(poly.subs(c,l+(u-l)*z)-basis)==0
assert min(Q(vv,D) for _,_,_,D,v in rows for vv in v)==Q(901,120000)
out['bernstein_identities'] = 5

# Independent scalar minimization certificate identities.
a=s.symbols('a')
assert s.expand(a*c*c+s.Rational(5,4)*a*a-s.Rational(11,6)*a-s.Rational(20,27)*c+s.Rational(95,108)
                -s.Rational(5,4)*(a-(11-6*c*c)/15)**2
                -(1-c)*(3*c-2)**2*(3*c+7)/135)==0
assert s.expand(a*c*c+s.Rational(24,25)*a*a-s.Rational(41,25)*a-s.Rational(4,5)*c+s.Rational(68,75)
                -s.Rational(24,25)*(a-(41-25*c*c)/48)**2
                -(1-c)*(5*c-3)**2*(5*c+11)/480)==0
out['two_level_identities']=2

# Fixed-scale diagnostic and P-split retained-domain counterexample.
for t in [Q(i,20) for i in range(61)]:
    assert t*t<=3*t and (t-3)**2<=9-3*t
for w in [-1,1]:
    assert 0**2+w*w<=1 and (3-3)**2+w*w<=1
out['psplit_box_link_points']=61

# Parity-rank support accounting, exhaustive multisets of small supports.
def binary_rank(rows):
    pivots={}
    for v in rows:
        while v:
            p=v.bit_length()-1
            if p not in pivots: pivots[p]=v; break
            v^=pivots[p]
    return len(pivots)
supports=[v for v in range(1,32) if v.bit_count()<=3]
count=0
for rows in combinations(supports,3):
    union=rows[0]|rows[1]|rows[2]
    assert union.bit_count()<=3*binary_rank(rows)
    count+=1
out['parity_rank_support_sets']=count
out['nature']='Exact integer/rational arithmetic and symbolic identities. Finite checks do not prove universal theorems.'
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
