"""Independent exact finite boundary checks; no universal theorem is inferred."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from collections import Counter
import json
from pathlib import Path

def bc(n,j): return comb(n,j) if 0<=j<=n else 0

def moments(p,N,balanced=True):
    d=len(p)
    C=[F(0)]*(d+2); O=C.copy()
    breaks=sorted(set([F(0),F(1)]+list(p)+[1-x for x in p]))
    patterns=list(combinations(range(N),N//2)) if balanced else list(combinations(range(N),0))
    if not balanced: patterns=[tuple(i for i in range(N) if bits[i]) for bits in product([0,1],repeat=N)]
    for lo,hi in zip(breaks,breaks[1:]):
        u=(lo+hi)/2; length=hi-lo
        k=sum(u<x for x in p)
        for j in range(d+2): C[j]+=length*bc(k,j)
        for pat in patterns:
            k=sum(u<x if i in pat else u>1-x for i,x in enumerate(p))
            for j in range(d+2): O[j]+=length*bc(k,j)/len(patterns)
    P=[F(1)]+[F(0)]*(d+1)
    for x in p:
        for j in range(d,0,-1): P[j]+=x*P[j-1]
    s=sum(p,F(0)); k=s.numerator//s.denominator; t=s-k
    V=[(1-t)*bc(k,j)+t*bc(k+1,j) for j in range(d+2)]
    return C,P,O,V

def coefficients(p,N,balanced=True):
    C,P,O,V=moments(p,N,balanced)
    beta=F(N*(N-1),2*(N//2)*(N-N//2)) if balanced else F(2)
    return [beta*(C[j]-O[j])+V[j]-P[j]+(C[j-1]-P[j-1] if j else 0) for j in range(len(C))]

coefficient_cases=0; cardinality_cases=0
for N in range(2,6):
    for d in range(N+1):
        for p in product([F(0),F(1,3),F(1,2),F(1)],repeat=d):
            Fs=coefficients(p,N)
            assert min(Fs)>=0,(N,p,Fs)
            C,P,O,V=moments(p,N)
            beta=F(N*(N-1),2*(N//2)*(N-N//2))
            for L in (F(0),F(1),F(2)):
                a=[F(0)]*(d+2)
                if d>=2:
                    a[2]=1
                    for j in range(3,d+1): a[j]=a[j-1]*L/2
                vals=[sum(aj*vj for aj,vj in zip(a,m)) for m in (C,P,O,V)]
                c,ind,ori,v=vals
                assert c-v<=(L+1)*(c-ind)+beta*(c-ori)
                cardinality_cases+=1
            coefficient_cases+=1
p=(F(2,5),F(7,10),F(24,25),F(97,100))
p2=(F(2,5),F(7,10),F(959,1000),F(971,1000))
assert coefficients(p,4,False)[3]==F(6201,12500)
assert coefficients(p2,4,False)[3]==F(4961031,10000000)

radix_cases=0
for b in range(2,9):
    for L in range(2,13):
        w=[F(b-1,b**(l+1)) if l<L else F(1,b**L) for l in range(L+1)]
        M=lambda q:F((L-q)*(b-1)+b,b**q)
        s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
        assert sum(M(q) for q in range(s+1,L+1))==F(L-s,b**s)
        weight=(1-M(s+1))/(M(s)-M(s+1))
        expected=F(0)
        for q,mix in ((s,weight),(s+1,1-weight)):
            mean=F(0)
            for l,wl in enumerate(w):
                R=b**(l-q+1) if l>=q else 0
                val=sum(min(b**j,R) for j in range(1,l+1))
                bound=s*R+sum(b**j for j in range(1,max(0,l-s)+1))
                assert val==bound
                mean+=wl*R; expected+=mix*wl*val
            assert mean==M(q)
        assert expected==s+F(L-s,b**s)
        radix_cases+=1

parity=Counter()
for bits in product([0,1],repeat=6):
    ab=bits[0]==bits[1]; bc_=bits[2]==bits[3]; ca=bits[4]==bits[5]
    value=(int(ab and ca),int(not ab and bc_),int(not bc_ and not ca))
    parity[value]+=1
assert sorted(parity.values())==[16]*4

residual_cases=0
for e in (F(1,100),F(1,3),F(1),F(2)):
    for a,b,c in product([0,1],repeat=3):
        B=e*e*a*b+2*e*a*c+2*e*b*c+2*e*e*a*b*c
        C=2*e*a*b+B
        assert B-e*e*(a+b+c-1)>=0
        assert C-2*e*(a+b+c-1)>=0
        residual_cases+=1
output={'arithmetic':'exact Fraction/integer','coefficient_vectors':coefficient_cases,'cardinality_vectors_and_L':cardinality_cases,'radix_profiles':radix_cases,'parity_assignments':64,'unequal_box_vertices':residual_cases,'schur_values':'both exact values agree','limits':'Finite checks supplement the independent written proof review; not universal proofs.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output))
