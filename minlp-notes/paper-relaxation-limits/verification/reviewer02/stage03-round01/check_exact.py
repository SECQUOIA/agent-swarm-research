"""Independent exact checks of Stage3 identities; finite checks, not proofs."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from math import comb, prod
from functools import lru_cache
import json

def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0

@lru_cache(None)
def moments(p, N, fair=False):
    d = len(p)
    P = [F(1)] + [F(0)] * (d + 1)
    for x in p:
        for j in range(d, 0, -1):
            P[j] += x * P[j-1]
    C = [F(1)] + [sum((x * choose(d-i-1, j-1) for i, x in enumerate(sorted(p))), F(0)) for j in range(1, d+2)]
    s = sum(p, F(0)); k = s.numerator // s.denominator; theta = s-k
    V = [(1-theta)*choose(k,j)+theta*choose(k+1,j) for j in range(d+2)]
    O = [F(0)]*(d+2)
    breaks = sorted({F(0), F(1), *p, *(1-x for x in p)})
    for coins in product((0, 1), repeat=d):
        weight = F(1, 2**d) if fair else F(choose(N-d, N//2-sum(coins)), choose(N,N//2))
        if not weight:
            continue
        for a,b in zip(breaks, breaks[1:]):
            u=(a+b)/2
            K=sum(u<x if coin else u>1-x for x,coin in zip(p,coins))
            for j in range(d+2):
                O[j] += weight*(b-a)*choose(K,j)
    beta = F(2) if fair else F(N*(N-1),2*(N//2)*(N-N//2))
    coeff=[beta*C[j]+V[j]-P[j]-beta*O[j]+(C[j-1]-P[j-1] if j else 0) for j in range(d+2)]
    return C,P,V,O,coeff,beta

counts={"coefficient_vectors":0,"coefficient_orders":0,"spreading_orders":0,"cardinality_bounds":0,"radix_pairs":0,"hardness_vertices":0}
grid=[F(i,4) for i in range(5)]
for N in range(2,8):
    for d in range(min(N,5)+1):
        for p in combinations_with_replacement(grid,d):
            C,P,V,O,coef,beta=moments(p,N)
            assert all(x>=0 for x in coef), (N,p,coef)
            counts["coefficient_vectors"]+=1; counts["coefficient_orders"]+=len(coef)
            if d>=3 and p[0]>0 and p[-1]<1:
                h=min(p[0],1-p[-1]); moved=(p[0]-h,*p[1:-1],p[-1]+h)
                movedcoef=moments(moved,N)[4]
                for j in range(3,d+1):
                    assert movedcoef[j]<=coef[j], (N,p,j)
                    counts["spreading_orders"]+=1
            for L in (F(0),F(1,2),F(3)):
                weights=[F(0),F(0)]+[L**(j-2) for j in range(2,d+2)]
                vals=[sum(a*x for a,x in zip(weights,seq)) for seq in (C,P,V,O)]
                c,pp,v,o=vals
                assert c-v<=(L+1)*(c-pp)+beta*(c-o)
                counts["cardinality_bounds"]+=1

p=(F(2,5),F(7,10),F(24,25),F(97,100))
q=(F(2,5),F(7,10),F(959,1000),F(971,1000))
assert moments(p,4,True)[4][3]==F(6201,12500)
assert moments(q,4,True)[4][3]==F(4961031,10000000)
assert moments(q,4,True)[4][3]-moments(p,4,True)[4][3]==F(231,10000000)
for b in range(2,12):
    for L in range(2,31):
        ws=[F(b-1,b**(l+1)) if l<L else F(1,b**L) for l in range(L+1)]
        M=lambda s:F((L-s)*(b-1)+b,b**s)
        s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
        mix=(1-M(s+1))/(M(s)-M(s+1))
        values=[]
        for q in (s,s+1):
            rs=[b**(l-q+1) if l>=q else 0 for l in range(L+1)]
            assert sum(w*r for w,r in zip(ws,rs))==M(q)
            for l,r in enumerate(rs):
                assert sum(min(b**j,r) for j in range(1,l+1))==s*r+sum(b**j for j in range(1,max(l-s,0)+1))
            values.append(sum(ws[l]*sum(min(b**j,rs[l]) for j in range(1,l+1)) for l in range(L+1)))
        assert mix*values[0]+(1-mix)*values[1]==s+F(L-s,b**s)
        assert sum((M(q) for q in range(s+1,L+1)),F(0))==F(L-s,b**s)
        counts["radix_pairs"]+=1

for raw in combinations_with_replacement(range(1,5),4):
    a=[2*x for x in raw]; A=sum(a); eps=F(1,16*A**3)
    pi=[eps*x+eps**2*(A*x-x*x)/2 for x in a]
    d0=1-eps**2*A*A/8
    for z in product((0,1),repeat=4):
        S=sum(x*y for x,y in zip(a,z)); C=prod(1+eps*x*y for x,y in zip(a,z))
        R=C-1-eps*S-eps**2*(S*S-sum(x*x*y for x,y in zip(a,z)))/2
        assert 0<=R<=eps**2/8
        assert C-sum(x*y for x,y in zip(pi,z))==d0+eps**2*(S-F(A,2))**2/2+R
        counts["hardness_vertices"]+=1

for eps in (F(1,100),F(1,2),F(1),F(2)):
    for a,b,c in product((0,1), repeat=3):
        B=eps**2*a*b+2*eps*a*c+2*eps*b*c+2*eps**2*a*b*c
        C=2*eps*a*b+B
        assert B>=eps**2*(a+b+c-1)
        assert C>=2*eps*(a+b+c-1)

print(json.dumps({"arithmetic":"exact rational", "passed":True, "counts":counts},indent=2))
