from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb
import json, re
import sympy as s

out=Path(__file__).resolve().parent
paper=out.parents[2]/'process/snapshots/stage02-round02'
dyadic=[]
for L in range(2,13):
    m=2**L
    weights=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    B=lambda q:Q(L-q+2,2**q)
    candidates=[k for k in range(1,L) if B(k+1)<=1<=B(k)]
    attained=[]
    for k in candidates:
        mix=(1-B(k+1))/(B(k)-B(k+1))
        er=Q(0); val=Q(0)
        for l,w in enumerate(weights):
            affine=0 if l<=k else 2**(l-k+1)-2
            for r in range(m+1):
                assert sum(min(2**j,r) for j in range(1,l+1))<=k*r+affine
            for q,prob in ((k,mix),(k+1,1-mix)):
                r=0 if l<q else 2**(l-q+1)
                er+=w*prob*r
                payoff=sum(min(2**j,r) for j in range(1,l+1))
                assert payoff==k*r+affine
                val+=w*prob*payoff
                failed=[int(format(i,f'0{L}b')[::-1],2) for i in range(r)]
                for j in range(1,L+1):
                    assert len({v>>(L-j) for v in failed})==min(2**j,r)
        assert er==1 and val==k+Q(L-k,2**k)
        for j in range(1,L+1):assert sum(weights[j:])==Q(1,2**j)
        attained.append(val)
    assert len(set(attained))==1
    dyadic.append((L,str(attained[0])))

def deficiencies(xs):
    u=min(xs)
    # Integrate each orientation's intersection interval exactly.
    inter=Q(0)
    for bits in product((0,1),repeat=len(xs)):
        lo=max([Q(0)]+[1-x for x,b in zip(xs,bits) if b])
        hi=min([Q(1)]+[x for x,b in zip(xs,bits) if not b])
        inter+=max(Q(0),hi-lo)/2**len(xs)
    do=u-inter
    di=u-s.prod(xs)
    cuts=sorted({Q(0),Q(1)}|{x if x<=Q(1,2) else 2*(1-x) for x in xs})
    inter=Q(0)
    for left,right in zip(cuts,cuts[1:]):
        t=(left+right)/2
        pr=Q(1)
        for x in xs:
            pr*=int(t<=x) if x<=Q(1,2) else (Q(1,2) if t<=2*(1-x) else 1)
        inter+=(right-left)*pr
    return do,di,u-inter

grid=[Q(j,12) for j in range(13)]
checks=0
for degree in (2,3):
    for xs in combinations_with_replacement(grid,degree):
        ds=deficiencies(xs)
        gap=min(xs[0],sum(1-x for x in xs[1:]))
        assert sum(a*b for a,b in zip((18,6,7),ds))>=12*gap
        checks+=1

a,b,c,t=s.symbols('a b c t')
R=s.Rational
h=6*c**3+27*b*c**2+18*b*b+30*a*c+20*a*b+9*a*a-37*a-R(79,2)*b-38*c+R(103,3)
p=s.expand(h.subs({a:1,b:R(13,24)-R(3,4)*c*c}))
sol=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.expand(h.subs(sol))
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)',(paper/'sections/03-cubic-equal-means.tex').read_text())
coeff=[]
for kind,l,u,den,nums in rows:
    vals=[R(n)/int(den) for n in nums.split(',')]
    coeff+=vals
    assert s.expand(dict(p=p,r=r)[kind].subs(c,R(l)+(R(u)-R(l))*t)-sum(vals[i]*comb(4,i)*t**i*(1-t)**(4-i) for i in range(5)))==0
assert len(rows)==5 and min(coeff)==R(901,120000)
for beta,lhs,rhs in [
 (R(5,4),R(11,6)*a+R(20,27)*c-R(95,108),R(5,4)*(a-(11-6*c*c)/15)**2+(1-c)*(3*c-2)**2*(3*c+7)/135),
 (R(24,25),R(41,25)*a+R(4,5)*c-R(68,75),R(24,25)*(a-(41-25*c*c)/48)**2+(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert s.expand(a*c*c+beta*a*a-lhs-rhs)==0
result={'dyadic_exact_L_H':dyadic,'exact_cubic_mixture_grid_tuples':checks,'bernstein_identity_rows':len(rows),'slack':str(min(coeff)),'two_level_polynomial_identities':2}
(out/'independent-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
