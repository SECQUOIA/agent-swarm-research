"""Independent finite exact checks; no manuscript or existing checker imports."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, prod
from random import Random
import json
from pathlib import Path

rng = Random(120301)
counts = {}

def choose(n, j):
    return comb(n, j) if 0 <= j <= n else 0

def moments(p, N, fair=False):
    d = len(p)
    out = [[Q(0) for j in range(d + 3)] for _ in range(4)]
    C, P, O, V = out
    for bits in product((0, 1), repeat=d):
        prob = prod(x if z else 1-x for x,z in zip(p,bits))
        for j in range(d + 3):
            P[j] += prob * choose(sum(bits), j)
    ends = sorted({Q(0), Q(1), *p})
    for a,b in zip(ends,ends[1:]):
        k = sum(x > (a+b)/2 for x in p)
        for j in range(d+3):
            C[j] += (b-a)*choose(k,j)
    if fair:
        patterns = [set(c) for r in range(N+1) for c in combinations(range(N),r)]
    else:
        patterns = [set(c) for c in combinations(range(N),N//2)]
    ends = sorted({Q(0),Q(1),*p,*(1-x for x in p)})
    for c in patterns:
        for a,b in zip(ends,ends[1:]):
            u=(a+b)/2
            k=sum(u < x if i in c else u > 1-x for i,x in enumerate(p))
            for j in range(d+3):
                O[j]+=(b-a)*choose(k,j)/len(patterns)
    s=sum(p); k=s.numerator//s.denominator
    for j in range(d+3):
        V[j]=(1-(s-k))*choose(k,j)+(s-k)*choose(k+1,j)
    beta=Q(2) if fair else Q(N*(N-1),2*(N//2)*(N-N//2))
    F=[beta*C[j]+V[j]-P[j]-beta*O[j]+(C[j-1]-P[j-1] if j else 0) for j in range(d+3)]
    return out,F,beta

nc=0
for N in range(2,8):
    for d in range(1,min(N,5)+1):
        for trial in range(12):
            p=sorted(Q(rng.randrange(11),10) for _ in range(d))
            vals,F,beta=moments(p,N)
            assert min(F)>=0
            if d>=3 and 0<p[0] and p[-1]<1:
                h=min(p[0],1-p[-1]); spread=p.copy()
                spread[0]-=h; spread[-1]+=h
                F2=moments(spread,N)[1]
                assert all(F2[j]<=F[j] for j in range(3,d+1))
            C,P,O,V=vals
            for L in (Q(0),Q(1,2),Q(2)):
                coeff=[Q(0),Q(0),Q(1)]
                for j in range(3,d+3):
                    coeff.append(coeff[-1]*L*Q(rng.randrange(4),3))
                t=sum(coeff[j]*(C[j]-V[j]) for j in range(d+1))
                rhs=sum(coeff[j]*((L+1)*(C[j]-P[j])+beta*(C[j]-O[j])) for j in range(d+1))
                assert t<=rhs
            nc+=1
counts['ambient_vectors']=nc
p=[Q(2,5),Q(7,10),Q(24,25),Q(97,100)]
assert moments(p,4,True)[1][3]==Q(6201,12500)
p[-2]-=Q(1,1000);p[-1]+=Q(1,1000)
assert moments(p,4,True)[1][3]==Q(4961031,10000000)

nr=0
for b in range(2,12):
    for L in range(2,26):
        w=[Q(b-1,b**(l+1)) for l in range(L)]+[Q(1,b**L)]
        M=lambda q:Q((L-q)*(b-1)+b,b**q)
        s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
        weight=(1-M(s+1))/(M(s)-M(s+1))
        vals=[]
        for q in (s,s+1):
            r=[b**(l-q+1) if l>=q else 0 for l in range(L+1)]
            assert sum(wi*ri for wi,ri in zip(w,r))==M(q)
            vals.append(sum(w[l]*sum(min(b**j,r[l]) for j in range(1,l+1)) for l in range(L+1)))
        assert weight*vals[0]+(1-weight)*vals[1]==s+Q(L-s,b**s)
        assert sum(M(q) for q in range(s+1,L+1))==Q(L-s,b**s)
        nr+=1
counts['radix_pairs']=nr

nh=0
for n in range(1,9):
    for trial in range(10):
        a=[2*rng.randrange(1,15) for _ in range(n)]; A=sum(a)
        eps=Q(1,16*A**3)
        d0=1-eps**2*A*A/8
        pi=[eps*x+eps**2*(A*x-x*x)/2 for x in a]
        found=False; vals=[]
        for z in product((0,1),repeat=n):
            S=sum(x*y for x,y in zip(a,z))
            C=prod(1+eps*x*y for x,y in zip(a,z))
            remainder=C-(1+eps*S+eps**2*(S*S-sum(x*x*y for x,y in zip(a,z)))/2)
            assert 0<=remainder<=eps**2/8
            tilted=C-sum(x*y for x,y in zip(pi,z))
            assert tilted==d0+eps**2*(S-Q(A,2))**2/2+remainder
            vals.append(tilted); found |= S*2==A
            nh+=1
        threshold=d0+eps**2/4
        assert min(vals)+eps**2/32<threshold if found else min(vals)-eps**2/32>threshold
counts['partition_vertices']=nh

payoffs={}
for z in product((0,1),repeat=6):
    E=lambda i,j:z[i]==z[j]
    g=(int(E(0,1) and E(4,5)),int(not E(0,1) and E(2,3)),int(not E(2,3) and not E(4,5)))
    assert sum(g)<=1
    payoffs[str(g)]=payoffs.get(str(g),0)+1
assert sorted(payoffs.values())==[16]*4
counts['parity_payoffs']=payoffs
Path(__file__).with_suffix('.json').write_text(json.dumps({'status':'PASS','arithmetic':'exact rational','counts':counts},indent=2)+'\n')
print(json.dumps(counts,indent=2))
