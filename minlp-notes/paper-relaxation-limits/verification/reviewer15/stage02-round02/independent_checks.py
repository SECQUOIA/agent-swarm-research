from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, prod
from pathlib import Path
import json,re
import sympy as s
out=Path(__file__).parent
snapshot=out.parents[2]/'process/snapshots/stage02-round02'
summary={}
# Exact dyadic certificates, all counts, and explicit prefix construction.
for L in range(2,11):
    m=2**L
    B=lambda q:Q(L-q+2,2**q)
    cut=[q for q in range(1,L) if B(q+1)<=1<=B(q)]
    weights=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    for cut_s in cut:
        theta=(1-B(cut_s+1))/(B(cut_s)-B(cut_s+1))
        er=score=Q(0)
        means=[Q(0)]*L
        for q,mix in [(cut_s,theta),(cut_s+1,1-theta)]:
            for l,wl in enumerate(weights):
                r=0 if l<q else 2**(l-q+1)
                er+=mix*wl*r
                score+=mix*wl*sum(min(2**j,r) for j in range(1,l+1))
                for j in range(1,L+1): means[j-1]+=mix*wl*(j<=l)
        assert er==1 and means==[Q(1,2**j) for j in range(1,L+1)]
        assert score==cut_s+Q(L-cut_s,2**cut_s)
        for l,r in product(range(L+1),range(m+1)):
            intercept=0 if l<=cut_s else 2**(l-cut_s+1)-2
            assert sum(min(2**j,r) for j in range(1,l+1))<=cut_s*r+intercept
    strings=[int(f'{i:0{L}b}'[::-1],2) for i in range(m)]
    for j in range(1,L+1):
        prefixes=set()
        for r,v in enumerate(strings,1):
            prefixes.add(v>>(L-j))
            assert len(prefixes)==min(2**j,r)
summary['dyadic_exact']='L=2,...,10; all admissible cutoffs, marginals, expectations, affine inequalities, prefix hits'
# Independently integrate actual O and B laws (piecewise constant in shared U).
def deficiencies(xs):
    u=min(xs)
    do=Q(0)
    for orientations in product((0,1),repeat=len(xs)):
        lowers=[1-x if orient else 0 for x,orient in zip(xs,orientations)]
        uppers=[1 if orient else x for x,orient in zip(xs,orientations)]
        do+=u-max(Q(0),min(uppers)-max(lowers))
    do/=2**len(xs)
    di=u-prod(xs)
    breaks=sorted({Q(0),Q(1),*[x if x<=Q(1,2) else 2*(1-x) for x in xs]})
    joint=Q(0)
    for lo,hi in zip(breaks,breaks[1:]):
        mid=(lo+hi)/2
        ps=[Q(mid<x) if x<=Q(1,2) else (Q(1,2) if mid<2*(1-x) else Q(1)) for x in xs]
        joint+=(hi-lo)*prod(ps)
    return do,di,u-joint
ncheck=0
for degree in (2,3):
    for xs in combinations_with_replacement([Q(i,20) for i in range(21)],degree):
        t=min(xs[0],sum(1-x for x in xs[1:]))
        ds=deficiencies(xs)
        assert all(v>=0 for v in ds)
        assert 18*ds[0]+6*ds[1]+7*ds[2]>=12*t,(xs,ds,t)
        ncheck+=1
summary['actual_cubic_laws_rational_tuples']=ncheck
# Obtain coefficients from the frozen printed table, derive the two quartics afresh.
a,b,c,t=s.symbols('a b c t')
h=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2-37*a-s.Rational(79,2)*b-38*c+s.Rational(103,3)
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c*c/4}))
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.expand(h.subs(stationary))
tex=(snapshot/'sections/03-cubic-equal-means.tex').read_text()
pattern=r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)\$'
rows=re.findall(pattern,tex)
assert len(rows)==5
coefficients=[]
for name,lo,hi,D,vals in rows:
    lo,hi=s.Rational(lo),s.Rational(hi)
    vals=[s.Rational(v,int(D)) for v in vals.split(',')]
    bern=sum(v*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vals))
    assert s.expand(bern-{'p':p,'r':r}[name].subs(c,lo+(hi-lo)*t))==0
    coefficients+=vals
assert min(coefficients)==s.Rational(901,120000)
assert s.Rational(161,4)/(s.Rational(223,12)-min(coefficients))==s.Rational(1610000,743033)
assert s.expand(a*c*c+s.Rational(5,4)*a*a-s.Rational(11,6)*a-s.Rational(20,27)*c+s.Rational(95,108)-s.Rational(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0
assert s.expand(a*c*c+s.Rational(24,25)*a*a-s.Rational(41,25)*a-s.Rational(4,5)*c+s.Rational(68,75)-s.Rational(24,25)*(a-(41-25*c*c)/48)**2-(1-c)*(5*c-3)**2*(5*c+11)/480)==0
summary['symbolic']='all five Bernstein rows match independently eliminated quartics; both two-level identities exact'
# Finite arithmetic and exact equal-means positivity, bound, and dimension-free optimizer.
assert Q(943)-2*Q(80947,175)==Q(3131,175)
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)
assert 25002-Q(1000**3,23200)<0
neq=0
for n in range(2,31):
    for u in [Q(i,20) for i in range(1,20)]:
        count=n*u; b0=count.numerator//count.denominator; frac=count-b0
        for d in range(2,n+1):
            q=((1-frac)*comb(b0,d)+frac*comb(b0+1,d))/comb(n,d)
            assert 0<=q<=u**d<u
            assert min(u,(d-1)*(1-u))<=2*(u-q)
            neq+=1
summary['equal_mean_exact_parameter_cases']=neq
(out/'independent-results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
