from fractions import Fraction as F
from itertools import product, combinations
from math import comb
import json, random
from pathlib import Path

def choose(n,j):
    return comb(n,j) if 0 <= j <= n else 0

def moments(p, orientations):
    d=len(p); out=[F(0)]*(d+2)
    cuts=sorted({F(0),F(1),*p,*(1-x for x in p)})
    for bits,weight in orientations:
        for l,r in zip(cuts,cuts[1:]):
            u=(l+r)/2
            k=sum(u<x if bit else u>1-x for x,bit in zip(p,bits))
            for j in range(d+2): out[j]+=weight*(r-l)*choose(k,j)
    return out

def check_coeff(p,N):
    d=len(p)
    pats=[]
    for subset in combinations(range(N),N//2):
        pats.append((tuple(i in subset for i in range(d)),F(1,comb(N,N//2))))
    O=moments(p,pats)
    C=moments(p,[(tuple([1]*d),F(1))])
    P=[F(0)]*(d+2)
    for bits in product((0,1),repeat=d):
        prob=F(1)
        for x,b in zip(p,bits): prob*=x if b else 1-x
        for j in range(d+2):P[j]+=prob*choose(sum(bits),j)
    s=sum(p,F(0)); k=s.numerator//s.denominator; theta=s-k
    V=[(1-theta)*choose(k,j)+theta*choose(k+1,j) for j in range(d+2)]
    beta=F(N*(N-1),2*(N//2)*((N+1)//2))
    vals=[beta*(C[j]-O[j])+V[j]-P[j]+(C[j-1]-P[j-1] if j else 0) for j in range(d+2)]
    assert min(vals)>=0,(p,N,vals)
    L=F(3,2);a=[F(0),F(0)]+[L**(j-2) for j in range(2,d+2)]
    # Terminate the expansion at its actual support degree.
    a[-1]=0
    c,v,ip,op=[sum(x*y for x,y in zip(a,Z)) for Z in (C,V,P,O)]
    assert c-v <= (L+1)*(c-ip)+beta*(c-op)

rng=random.Random(150301)
ncoef=0
for N in range(2,8):
    for d in range(N+1):
        for trial in range(8):
            p=tuple(F(rng.randrange(9),8) for _ in range(d))
            check_coeff(p,N); ncoef+=1

nradix=0
for b in range(2,11):
    for L in range(2,26):
        M=lambda q:F((L-q)*(b-1)+b,b**q)
        s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
        weights=[F(b-1,b**(l+1)) if l<L else F(1,b**L) for l in range(L+1)]
        mix=(1-M(s+1))/(M(s)-M(s+1))
        mean=F(0);value=F(0)
        for q,prob in ((s,mix),(s+1,1-mix)):
            for l,w in enumerate(weights):
                R=b**(l-q+1) if l>=q else 0
                mean+=prob*w*R
                value+=prob*w*sum(min(b**j,R) for j in range(1,l+1))
        assert mean==1 and value==s+F(L-s,b**s)
        assert sum((M(q) for q in range(s+1,L+1)),F(0))==F(L-s,b**s)
        nradix+=1

hist={}
for x in product((0,1),repeat=6):
    ab=x[0]==x[1];bc=x[2]==x[3];ca=x[4]==x[5]
    pay=(int(ab and ca),int(not ab and bc),int(not bc and not ca))
    hist[str(pay)]=hist.get(str(pay),0)+1
assert len(hist)==4 and set(hist.values())=={16}

# All eight vertices of both unequal-box residual certificates at rational epsilons.
neps=0
for eps in (F(1,1000),F(1,10),F(1,2),F(1),F(2)):
    for a,b,c in product((0,1),repeat=3):
        A=2*eps*a*b
        B=eps**2*a*b+2*eps*a*c+2*eps*b*c+2*eps**2*a*b*c
        assert B>=eps**2*(a+b+c-1)
        assert A+B>=2*eps*(a+b+c-1)
        neps+=1
out={'exact_coefficient_and_cardinality_cases':ncoef,'exact_radix_profiles':nradix,'parity_histogram':hist,'unequal_box_vertex_cases':neps,'status':'PASS','scope':'Finite rational checks only; universal proofs reviewed separately.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
