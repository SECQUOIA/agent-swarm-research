"""Independent exact finite checks; no claim of a universal computational proof."""
from fractions import Fraction as Q
from itertools import product, combinations
from math import comb, prod
import json


def law(p, orientations):
    out = {}
    patterns = list(orientations)
    for signs in patterns:
        breaks = sorted({Q(0), Q(1), *(p[i] if signs[i] else 1-p[i] for i in range(len(p)))})
        for a, b in zip(breaks, breaks[1:]):
            t = (a+b)/2
            z = tuple(int(t < p[i] if signs[i] else t > 1-p[i]) for i in range(len(p)))
            out[z] = out.get(z, Q(0)) + (b-a)/len(patterns)
    assert sum(out.values()) == 1
    assert all(sum(w*z[i] for z,w in out.items()) == p[i] for i in range(len(p)))
    return out


feedback = 0
grid = [Q(0), Q(1,5), Q(1,2), Q(4,5), Q(1)]
for f in range(4):
    for p in product(grid, repeat=f+1):
        dist = law(p, (s+(1,) for s in product((0,1), repeat=f)))
        for z in product((0,1), repeat=f+1):
            cap = min(p[i] if z[i] else 1-p[i] for i in range(f+1))
            assert dist.get(z, 0) >= cap / 2**f
        feedback += 1


def choose(k,j):
    return comb(k,j) if 0 <= j <= k else 0


def moments(p, dist, support):
    return [sum(w*choose(sum(z[i] for i in support),j) for z,w in dist.items())
            for j in range(len(support)+2)]


coefficient = 0
cardinality = 0
vectors = [(Q(0),Q(1,5),Q(1,2),Q(4,5),Q(1)),
           (Q(1,7),Q(2,7),Q(3,7),Q(5,7),Q(6,7)),
           (Q(1,2),)*5,
           (Q(0),Q(1,6),Q(1,3),Q(2,3),Q(5,6),Q(1)),
           (Q(1,9),Q(2,9),Q(4,9),Q(5,9),Q(7,9),Q(8,9))]
for p in vectors:
    n=len(p)
    beta=Q(n*(n-1),2*(n//2)*(n-n//2))
    O=law(p, (tuple(int(i in selected) for i in range(n)) for selected in combinations(range(n),n//2)))
    C=law(p, [(1,)*n])
    P={z:prod(p[i] if z[i] else 1-p[i] for i in range(n)) for z in product((0,1),repeat=n)}
    for mask in product((0,1),repeat=n):
        support=[i for i in range(n) if mask[i]]
        d=len(support)
        c,o,vp=[moments(p,dist,support) for dist in (C,O,P)]
        total=sum((p[i] for i in support),Q(0)); k=int(total); theta=total-k
        v=[(1-theta)*choose(k,j)+theta*choose(k+1,j) for j in range(d+2)]
        for j in range(d+2):
            residual=beta*(c[j]-o[j])+v[j]-vp[j]+(c[j-1]-vp[j-1] if j else 0)
            assert residual >= 0
            coefficient += 1
        for L in (Q(0),Q(1,2),Q(3)):
            coeff=[Q(1),Q(2)]+[L**(j-2) for j in range(2,d+1)]
            vals=[sum(coeff[j]*arr[j] for j in range(d+1)) for arr in (c,o,vp,v)]
            cc,oo,pp,vv=vals
            assert cc-vv <= (L+1)*(cc-pp)+beta*(cc-oo)
            cardinality += 1

radix=0
for b in range(2,9):
    for L in range(2,17):
        w=[Q(b-1,b**(l+1)) for l in range(L)]+[Q(1,b**L)]
        M=lambda q:Q((L-q)*(b-1)+b,b**q)
        s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
        theta=(1-M(s+1))/(M(s)-M(s+1))
        means=[]; values=[]
        for q in (s,s+1):
            r=[b**(l-q+1) if l>=q else 0 for l in range(L+1)]
            means.append(sum(w[l]*r[l] for l in range(L+1)))
            values.append(sum(w[l]*sum(min(b**j,r[l]) for j in range(1,l+1)) for l in range(L+1)))
        assert means == [M(s),M(s+1)]
        assert theta*means[0]+(1-theta)*means[1] == 1
        assert theta*values[0]+(1-theta)*values[1] == s+Q(L-s,b**s)
        assert sum(M(q) for q in range(s+1,L+1))==Q(L-s,b**s)
        radix += 1

print(json.dumps(dict(arithmetic="exact rational",feedback_vectors=feedback,
                     coefficient_cases=coefficient,cardinality_cases=cardinality,
                     radix_cases=radix,passed=True),indent=2))
