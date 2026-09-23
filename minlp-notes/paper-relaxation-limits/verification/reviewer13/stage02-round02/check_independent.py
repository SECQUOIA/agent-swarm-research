"""Independent exact checks; finite checks supplement the manuscript proofs."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import json
import re
import sympy as s

out = Path(__file__).resolve().parent
root = out.parents[2]
frozen = root / 'process/snapshots/stage02-round02'
record = {}

# Check dyadic certificates and realizing prefix sets without an LP solver.
dyadic = []
for L in range(2, 13):
    m = 2**L
    weights = [Q(1, 2**(l+1)) if l < L else Q(1, 2**L)
               for l in range(L+1)]
    B = lambda q: Q(L-q+2, 2**q)
    candidates = [q for q in range(1, L) if B(q+1) <= 1 <= B(q)]
    vals = []
    for q in candidates:
        theta = (1-B(q+1))/(B(q)-B(q+1))
        er = payoff = Q(0)
        for l, weight in enumerate(weights):
            intercept = 0 if l <= q else 2**(l-q+1)-2
            for r in range(m+1):
                assert sum(min(2**j, r) for j in range(1,l+1)) <= q*r+intercept
            for k, mix in [(q,theta),(q+1,1-theta)]:
                r = 0 if l < k else 2**(l-k+1)
                er += weight*mix*r
                payoff += weight*mix*sum(min(2**j,r) for j in range(1,l+1))
        assert er == 1
        assert payoff == q+Q(L-q,2**q)
        vals.append(payoff)
    assert len(set(vals)) == 1
    for j in range(1,L+1):
        assert sum(weights[j:]) == Q(1,2**j)
    # Prefix counts checked for every r; a uniform XOR shift makes inclusion r/m.
    rev = [int(f'{i:0{L}b}'[::-1],2) for i in range(m)]
    prefixes = [set() for _ in range(L)]
    for r, leaf in enumerate(rev,1):
        for j in range(1,L+1):
            prefixes[j-1].add(leaf >> (L-j))
            assert len(prefixes[j-1]) == min(2**j,r)
    dyadic.append({'L':L,'s':candidates,'H':str(vals[0])})
record['dyadic'] = dyadic

# Reconstruct both eliminated polynomials and read all Bernstein rows from TeX.
a,b,c,t=s.symbols('a b c t')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell=37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
h=F-ell
H=s.hessian(h,(a,b))
assert H.det()==248
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c**2/4}))
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.expand(h.subs(stationary))
tex=(frozen/'sections/03-cubic-equal-means.tex').read_text()
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)\$',tex)
assert len(rows)==5
coefficients=[]
for name,lo,hi,D,nums in rows:
    lo,hi,D=s.Rational(lo),s.Rational(hi),int(D)
    vals=[s.Rational(int(n),D) for n in nums.split(',')]
    bern=sum(v*s.binomial(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vals))
    assert s.expand({'p':p,'r':r}[name].subs(c,lo+(hi-lo)*t)-bern)==0
    coefficients.extend(vals)
delta=min(coefficients)
assert delta==s.Rational(901,120000)
assert s.Rational(161,4)/(s.Rational(223,12)-delta)==s.Rational(1610000,743033)
record['bernstein']={'rows':len(rows),'coefficients':len(coefficients),'minimum':str(delta)}
for lam,linear,center,residual in [
    (s.Rational(5,4),11*a/6+20*c/27-s.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
    (s.Rational(24,25),41*a/25+4*c/5-s.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert s.expand(a*c*c+lam*a*a-linear-lam*(a-center)**2-residual)==0
record['two_level_identities']=2

# Independently integrate actual O and B laws on a rational boundary-rich grid.
def deficiency(x,law):
    knots={Q(0),Q(1)}
    for v in x:
        knots.update([v,1-v] if law=='O' else [v if v<=Q(1,2) else 2*(1-v)])
    knots=sorted(knots)
    expectation=Q(0)
    for lo,hi in zip(knots,knots[1:]):
        u=(lo+hi)/2
        success=[]
        for v in x:
            if law=='O': success.append(Q(int(u<=v)+int(u>=1-v),2))
            elif v<=Q(1,2): success.append(Q(int(u<=v)))
            else: success.append(Q(1,2) if u<=2*(1-v) else Q(1))
        prod=Q(1)
        for v in success: prod*=v
        expectation+=(hi-lo)*prod
    return min(x)-expectation

grid=[Q(i,12) for i in range(13)]
count=0
for degree in [2,3]:
    for x in combinations_with_replacement(grid,degree):
        gap=min(x)-max(Q(0),sum(x)-degree+1)
        independent=Q(1)
        for v in x: independent*=v
        independent=min(x)-independent
        mix=(18*deficiency(x,'O')+7*deficiency(x,'B')+6*independent)/31
        assert mix>=Q(12,31)*gap
        count+=1
record['exact_mixture_grid_cases']=count

# Integer-count convexity and finite equal-mean formulas against every supporting line.
count=0
for n in range(2,19):
    for u in [Q(i,19) for i in range(1,19)]:
        b=int(n*u);theta=n*u-b
        for d in range(2,n+1):
            val=(1-theta)*comb(b,d)+theta*comb(b+1,d)
            sherali=max([Q(0)]+[comb(k,d-1)*n*u-(d-1)*comb(k+1,d) for k in range(d-1,n)])
            assert val==sherali
            q=val/comb(n,d)
            assert q<=u**d<u
            assert min(u,(d-1)*(1-u))/(u-q)<=2
            count+=1
record['equal_mean_exact_cases']=count
(out/'independent-results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
