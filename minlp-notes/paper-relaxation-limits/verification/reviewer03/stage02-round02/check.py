"""Independent exact boundary checks and replay of frozen printed certificates."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb
import re
import json
import sympy as s

out = Path(__file__).resolve().parent
paper = out.parents[2]
frozen = paper / 'process/snapshots/stage02-round02'
tex = (frozen/'sections/appendix-cubic-certificates.tex').read_text()
blocks = re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}', tex, re.S)
assert len(blocks) == 2
printed = ''.join(blocks)
assert printed == (frozen/'verification/check_stage02_finite.py').read_text()
exec(compile(printed, 'concatenated-frozen-checker', 'exec'), {})

# Integrate actual orientation and B product laws, independently of the formulas.
def interval_product(xs, bits):
    return max(Q(0), min(x if bit == 0 else Q(1) for x,bit in zip(xs,bits))
               - max(Q(0) if bit == 0 else 1-x for x,bit in zip(xs,bits)))

def b_law(xs):
    endpoints = sorted({Q(0),Q(1)} | {x if x <= Q(1,2) else 2*(1-x) for x in xs})
    means = [Q(0)] * len(xs)
    joint = Q(0)
    for left,right in zip(endpoints,endpoints[1:]):
        u = (left+right)/2
        probs = [Q(u<=x) if x<=Q(1,2) else (Q(1,2) if u<=2*(1-x) else Q(1)) for x in xs]
        val = Q(1)
        for i,p in enumerate(probs):
            means[i] += (right-left)*p
            val *= p
        joint += (right-left)*val
    assert means == list(xs)
    return joint

grid = sorted({Q(0),Q(1,100),Q(1,4),Q(499,1000),Q(1,2),Q(501,1000),Q(3,4),Q(99,100),Q(1)})
checks = 0
zero_gaps = 0
for degree in (2,3):
    for xs in combinations_with_replacement(grid,degree):
        upper = min(xs)
        gap = upper - max(Q(0),sum(xs)-degree+1)
        ori = sum(interval_product(xs,bits) for bits in product((0,1),repeat=degree))/2**degree
        indep = Q(1)
        for x in xs:
            indep *= x
        b = b_law(xs)
        assert (18*(upper-ori)+6*(upper-indep)+7*(upper-b))/31 >= Q(12,31)*gap
        if gap == 0:
            assert ori == indep == b == upper
            zero_gaps += 1
        checks += 1

# Every valid cutoff, including adjacent equality ties and extreme mixture weights.
ties = []
for L in range(2,81):
    weights = [Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    B = lambda q: Q(L-q+2,2**q)
    valid = [q for q in range(1,L) if B(q+1)<=1<=B(q)]
    values=[]
    for cut in valid:
        mix = (1-B(cut+1))/(B(cut)-B(cut+1))
        assert 0<=mix<=1
        ER=Q(0); objective=Q(0)
        for q,prob in ((cut,mix),(cut+1,1-mix)):
            for l,weight in enumerate(weights):
                r=0 if l<q else 2**(l-q+1)
                assert 0<=r<=2**L
                ER+=prob*weight*r
                val=sum(min(2**j,r) for j in range(1,l+1))
                intercept=0 if l<=cut else 2**(l-cut+1)-2
                assert val == cut*r+intercept
                objective+=prob*weight*val
        assert ER==1
        assert objective==cut+Q(L-cut,2**cut)
        values.append(objective)
    assert len(set(values))==1
    if len(valid)>1:
        ties.append(L)

# Independently eliminate a,b, then recover the frozen Bernstein rows.
a,b,c,t=s.symbols('a b c t'); R=s.Rational
h=6*c**3+27*b*c*c+18*b*b+30*a*c+20*a*b+9*a*a-37*a-R(79,2)*b-38*c+R(103,3)
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.factor(h.subs(stationary))
p=s.factor(h.subs({a:1,b:R(13,24)-3*c*c/4}))
source=(frozen/'sections/03-cubic-equal-means.tex').read_text()
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)',source)
assert len(rows)==5
slacks=[]
for kind,lo,hi,den,nums in rows:
    poly=s.Poly(s.expand({'p':p,'r':r}[kind].subs(c,R(lo)+(R(hi)-R(lo))*t)),t)
    recovered=[sum(poly.nth(j)*R(comb(i,j),comb(4,j)) for j in range(i+1)) for i in range(5)]
    assert recovered==[R(int(v),int(den)) for v in nums.split(',')]
    slacks.extend(recovered)
assert min(slacks)==R(901,120000)

# Equal-means endpoint-adjacent counts and the case of integral nu.
equal_checks=0
for n in range(2,25):
    for u in [Q(j,24) for j in range(1,24)]:
        b0=(n*u).numerator//(n*u).denominator
        theta=n*u-b0
        for d in range(2,n+1):
            q=((1-theta)*comb(b0,d)+theta*comb(b0+1,d))/comb(n,d)
            assert 0<=q<=u**d<u
            assert min(u,(d-1)*(1-u))/(u-q)<=2
            equal_checks+=1
result={'printed_blocks':2,'finite_certificates':'passed','exact_actual_law_checks':checks,
        'zero_gap_checks':zero_gaps,'dyadic_L_range':[2,80],'dyadic_tie_L':ties,
        'bernstein_rows':len(rows),'slack':str(min(slacks)), 'equal_mean_cases':equal_checks}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
