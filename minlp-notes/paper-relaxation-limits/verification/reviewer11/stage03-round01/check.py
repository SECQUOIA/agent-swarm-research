"""Independent exact finite checks; no claim of a universal proof."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import random
import json
from math import prod

def bc(n, j):
    return comb(n, j) if 0 <= j <= n else 0

def moments(p, patterns):
    d = len(p)
    ans = [F(0)] * (d + 2)
    endpoints = sorted(set([F(0), F(1)] + list(p) + [1-v for v in p]))
    for pattern in patterns:
        for a, b in zip(endpoints, endpoints[1:]):
            u = (a+b)/2
            k = sum(u < p[i] if pattern[i] else u > 1-p[i] for i in range(d))
            for j in range(d+2):
                ans[j] += (b-a)*bc(k, j)/len(patterns)
    return ans

def four(p, N, balanced=True):
    d = len(p)
    if balanced:
        pats = [tuple(i in J for i in range(d)) for J in combinations(range(N), N//2)]
        beta = F(N*(N-1), 2*(N//2)*(N-N//2))
    else:
        pats = list(product([False, True], repeat=d))
        beta = F(2)
    O = moments(p, pats)
    C = moments(p, [(True,)*d])
    P = [F(1)]+[F(0)]*(d+1)
    for v in p:
        for j in range(d, 0, -1):
            P[j] += v*P[j-1]
    s=sum(p, F(0)); k=s.numerator//s.denominator; theta=s-k
    V=[(1-theta)*bc(k,j)+theta*bc(k+1,j) for j in range(d+2)]
    return C, P, O, V, beta

rng=random.Random(110301)
coefficient_cases=regularity_cases=0
for N in range(2,8):
    for d in range(N+1):
        for repeat in range(12):
            p=[F(rng.randrange(9),8) for _ in range(d)]
            C,P,O,V,beta=four(p,N)
            for j in range(d+2):
                prev=C[j-1]-P[j-1] if j else 0
                assert P[j]-V[j] <= beta*(C[j]-O[j])+prev
                coefficient_cases += 1
            for L in [F(0), F(1,2), F(2)]:
                coeff=[F(3),F(2)]+[F(0)]*max(0,d-1)
                if d >= 2:
                    coeff[2]=F(1)
                for j in range(3,d+1):
                    coeff[j]=coeff[j-1]*L*F(rng.randrange(4),3)
                gap=sum(coeff[j]*(C[j]-V[j]) for j in range(d+1))
                di=sum(coeff[j]*(C[j]-P[j]) for j in range(d+1))
                do=sum(coeff[j]*(C[j]-O[j]) for j in range(d+1))
                assert gap <= (L+1)*di+beta*do
                regularity_cases+=1

countervalues=[]
for p in [[F(2,5),F(7,10),F(24,25),F(97,100)],
          [F(2,5),F(7,10),F(959,1000),F(971,1000)]]:
    C,P,O,V,beta=four(p,4,False)
    countervalues.append(beta*(C[3]-O[3])+V[3]-P[3]+C[2]-P[2])
assert countervalues == [F(6201,12500),F(4961031,10000000)]

radix_cases=0
for b in range(2,9):
    for L in range(2,21):
        w=[F(b-1,b**(l+1)) for l in range(L)]+[F(1,b**L)]
        M={q:F((L-q)*(b-1)+b,b**q) for q in range(1,L+1)}
        s=next(s for s in range(1,L) if M[s+1] <= 1 <= M[s])
        mix=(1-M[s+1])/(M[s]-M[s+1])
        hull=F(0); countmean=F(0)
        for q,weight in [(s,mix),(s+1,1-mix)]:
            for l in range(L+1):
                r=b**(l-q+1) if l>=q else 0
                countmean+=weight*w[l]*r
                hull+=weight*w[l]*sum(min(b**j,r) for j in range(1,l+1))
        assert countmean==1
        assert hull==s+F(L-s,b**s)
        assert sum(M[q] for q in range(s+1,L+1))==F(L-s,b**s)
        radix_cases+=1

parity_counts={}
for z in product([0,1],repeat=6):
    ab,bc,ca=(z[i]==z[i+1] for i in [0,2,4])
    payoff=(ab and ca, not ab and bc, not bc and not ca)
    assert sum(payoff)<=1
    parity_counts[str(tuple(map(int,payoff)))]=parity_counts.get(str(tuple(map(int,payoff))),0)+1
assert sorted(parity_counts.values())==[16]*4

unequal_cases=0
laws=[[("000",F(1,4)),("001",F(1,4)),("011",F(1,4)),("101",F(1,4))],
      [("001",F(3,4)),("110",F(1,4))],
      [("001",F(1,2)),("011",F(1,4)),("100",F(1,4))],
      [("000",F(1,4)),("001",F(1,2)),("111",F(1,4))]]
for law in laws:
    assert [sum(w*int(z[i]) for z,w in law) for i in range(3)]==[F(1,4),F(1,4),F(3,4)]
for eps in [F(1,50),F(1,7),F(1,2),F(1),F(2)]:
    def costs(z):
        a,b,c=map(int,z)
        A=2*eps*a*b
        B=eps**2*a*b+2*eps*(a*c+b*c)+2*eps**2*a*b*c
        return A,B,A+B
    for z in product([0,1],repeat=3):
        A,B,C=costs(z)
        assert A>=0 and B>=eps**2*(sum(z)-1) and C>=2*eps*(sum(z)-1)
    lower=[sum(w*costs(z)[i] for z,w in laws[i]) for i in range(3)]
    upper=sum(w*costs(z)[2] for z,w in laws[3])
    assert lower == [0,eps**2/4,eps/2]
    assert (upper-lower[0]-lower[1])/(upper-lower[2])==2*(eps+3)/(3*eps+4)
    unequal_cases+=1

hardness_states=0
for a in [[2,2],[2,4],[2,2,2],[2,4,6],[4,6,8],[2,2,4,6],[2,4,8,10,12]]:
    total=sum(a); eps=F(1,16*total**3)
    base=1+eps*F(total,2)+eps**2*(F(total**2,8)-F(sum(x*x for x in a),4))
    pi=[eps*x+eps**2*F(total*x-x*x,2) for x in a]
    d0=1-eps**2*F(total**2,8)
    tilted=[]; balanced=[]
    for z in product([0,1],repeat=len(a)):
        s=sum(x*b for x,b in zip(a,z))
        value=prod(1+eps*x*b for x,b in zip(a,z))
        rem=value-1-eps*s-eps**2*F(s*s-sum(x*x*b for x,b in zip(a,z)),2)
        assert 0<=rem<=eps**2/8
        tilt=value-sum(p*b for p,b in zip(pi,z))
        assert tilt==d0+eps**2*F((s-total//2)**2,2)+rem
        tilted.append(tilt)
        if s==total//2:
            balanced.append((value+prod(1+eps*x*(1-b) for x,b in zip(a,z)))/2)
        hardness_states+=1
    if balanced:
        assert min(balanced)<=base+eps**2/8
        assert min(tilted)+eps**2/32<d0+eps**2/4
    else:
        assert min(tilted)-eps**2/32>d0+eps**2/4

result=dict(coefficient_cases=coefficient_cases,regularity_cases=regularity_cases,
            radix_cases=radix_cases,schur_countervalues=list(map(str,countervalues)),
            parity_counts=parity_counts,unequal_cases=unequal_cases,
            hardness_states=hardness_states,status="PASS",arithmetic="exact rational/integer")
print(json.dumps(result,indent=2))
