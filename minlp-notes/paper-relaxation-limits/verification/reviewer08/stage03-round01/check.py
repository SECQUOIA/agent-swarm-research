from fractions import Fraction as F
from itertools import combinations
from math import comb
from random import Random
import json

def choose(n,j):
    return comb(n,j) if 0 <= j <= n else 0

def moments(p,N):
    d=len(p)
    C=[F(1)]+[sum(v*choose(d-i-1,j-1) for i,v in enumerate(sorted(p))) for j in range(1,d+1)]
    P=[F(1)]+[F(0)]*d
    for v in p:
        for j in range(d,0,-1): P[j]+=v*P[j-1]
    s=sum(p); k=s.numerator//s.denominator; t=s-k
    V=[(1-t)*choose(k,j)+t*choose(k+1,j) for j in range(d+1)]
    O=[F(0)]*(d+1)
    patterns=list(combinations(range(N),N//2))
    breaks=sorted({F(0),F(1),*p,*(1-v for v in p)})
    for J in patterns:
        for a,b in zip(breaks,breaks[1:]):
            u=(a+b)/2
            K=sum((u < p[i]) if i in J else (u > 1-p[i]) for i in range(d))
            for j in range(d+1): O[j]+=(b-a)*choose(K,j)/len(patterns)
    return [x+[F(0)] for x in (C,P,V,O)]

rng=Random(806)
cases=0; spread=0; cardinality=0
for N in range(2,8):
    beta=F(N*(N-1),2*(N//2)*(N-N//2))
    for d in range(1,N+1):
        for _ in range(10):
            p=[F(rng.randrange(11),10) for i in range(d)]
            C,P,V,O=moments(p,N)
            Q=[beta*C[j]+V[j]-P[j]-beta*O[j]+(C[j-1]-P[j-1] if j else 0) for j in range(d+2)]
            assert min(Q)>=0
            cases+=1
            if d>=3 and min(p)>0 and max(p)<1:
                a=min(range(d),key=p.__getitem__); b=max(range(d),key=p.__getitem__)
                if a==b: b=(a+1)%d
                h=min(p[a],1-p[b]); r=p.copy(); r[a]-=h; r[b]+=h
                c,z,v,o=moments(r,N)
                q=[beta*c[j]+v[j]-z[j]-beta*o[j]+c[j-1]-z[j-1] for j in range(3,d+1)]
                assert all(x<=Q[j] for j,x in enumerate(q,3))
                spread+=1
            L=F(rng.randrange(4),2)
            coeff=[F(2),F(1),F(1)]
            for j in range(3,d+1): coeff.append(coeff[-1]*L*F(rng.randrange(4),3))
            coeff=coeff[:d+1]
            T=sum(coeff[j]*(C[j]-V[j]) for j in range(d+1))
            DI=sum(coeff[j]*(C[j]-P[j]) for j in range(d+1))
            DO=sum(coeff[j]*(C[j]-O[j]) for j in range(d+1))
            assert T <= (L+1)*DI+beta*DO
            cardinality+=1
radix=0
for b in range(2,13):
    for L in range(2,61):
        w=[F(b-1,b**(l+1)) for l in range(L)]+[F(1,b**L)]
        M=lambda q:F((L-q)*(b-1)+b,b**q)
        s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
        mix=(1-M(s+1))/(M(s)-M(s+1))
        val=F(0); mass=F(0)
        for q,prob in ((s,mix),(s+1,1-mix)):
            for l in range(L+1):
                r=b**(l-q+1) if l>=q else 0
                value=sum(min(b**j,r) for j in range(1,l+1))
                assert value==s*r+sum(b**j for j in range(1,l-s+1))
                val+=prob*w[l]*value
                mass+=prob*w[l]*r
        assert mass==1 and val==s+F(L-s,b**s)
        assert sum((M(q) for q in range(s+1,L+1)),F(0))==F(L-s,b**s)
        radix+=1
print(json.dumps({'exact_ambient_coefficient_vectors':cases,'exact_global_extremum_moves':spread,'exact_cardinality_vectors':cardinality,'exact_radix_cutoffs':radix,'result':'all passed'},indent=2))
