"""Independent finite exact checks; no universal theorem is inferred."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
import json

def orientation(p, balanced=False):
    n = len(p)
    masks = [set(c) for c in combinations(range(n), n//2)] if balanced else [set(i for i,b in enumerate(bits) if b) for bits in product((0,1), repeat=n)]
    law = {}
    cuts = sorted({Q(0), Q(1), *p, *(1-x for x in p)})
    for mask in masks:
        for a,b in zip(cuts,cuts[1:]):
            t = (a+b)/2
            state = tuple(int(t < x if i in mask else t > 1-x) for i,x in enumerate(p))
            law[state] = law.get(state,Q(0)) + (b-a)/len(masks)
    return law

def law_b(p):
    cuts = sorted({Q(0),Q(1), *(x for x in p if x<=Q(1,2)), *(2*(1-x) for x in p if x>Q(1,2))})
    law = {}
    for a,b in zip(cuts,cuts[1:]):
        t=(a+b)/2
        means=[Q(int(t<x)) if x<=Q(1,2) else Q(1,2) if t<2*(1-x) else Q(1) for x in p]
        for bits in product((0,1),repeat=len(p)):
            mass=b-a
            for bit,x in zip(bits,means): mass*=x if bit else 1-x
            law[bits]=law.get(bits,Q(0))+mass
    return law

def check_means(p,law):
    assert sum(law.values())==1 and all(v>=0 for v in law.values())
    assert all(sum(m*s[i] for s,m in law.items())==p[i] for i in range(len(p)))

counts={"cubic_or_quadratic_mean_vectors":0,"ambient_coefficient_inequalities":0,"radix_profiles":0}
for d in (2,3):
    for p in product([Q(i,8) for i in range(9)],repeat=d):
        O=orientation(p); B=law_b(p)
        check_means(p,O);check_means(p,B)
        upper=min(p); lower=max(Q(0),sum(p)-d+1)
        oi=upper-sum(m for s,m in O.items() if all(s))
        bi=upper-sum(m for s,m in B.items() if all(s))
        independent=Q(1)
        for x in p: independent*=x
        assert 18*oi+6*(upper-independent)+7*bi>=12*(upper-lower)
        counts["cubic_or_quadratic_mean_vectors"]+=1

for n in range(2,6):
    beta=Q(n*(n-1),2*(n//2)*(n-n//2))
    for p in product([Q(0),Q(1,2),Q(1)],repeat=n):
        law=orientation(p,True);check_means(p,law)
        # Keep the original ambient law when restricting to each prefix.
        for d in range(1,n+1):
            x=p[:d]; k=int(sum(x)); theta=sum(x)-k
            C=[];P=[];O=[];V=[]
            for j in range(d+2):
                C.append(sum(min(x[i] for i in e) for e in combinations(range(d),j)) if j else Q(1))
                products=[]
                for e in combinations(range(d),j):
                    val=Q(1)
                    for i in e: val*=x[i]
                    products.append(val)
                P.append(sum(products))
                O.append(sum(m*comb(sum(s[:d]),j) for s,m in law.items()))
                V.append((1-theta)*comb(k,j)+theta*comb(k+1,j))
            for j in range(d+2):
                prev=C[j-1]-P[j-1] if j else 0
                assert P[j]-V[j]<=beta*(C[j]-O[j])+prev
                counts["ambient_coefficient_inequalities"]+=1

for b in range(2,7):
    for L in range(2,13):
        cap=lambda q:Q((L-q)*(b-1)+b,b**q)
        s=next(s for s in range(1,L) if cap(s+1)<=1<=cap(s))
        w=[Q(b-1,b**(l+1)) if l<L else Q(1,b**L) for l in range(L+1)]
        alpha=(1-cap(s+1))/(cap(s)-cap(s+1))
        mean=Q(0);gap=Q(0)
        for q,weight in ((s,alpha),(s+1,1-alpha)):
            for l,mass in enumerate(w):
                R=b**(l-q+1) if l>=q else 0
                mean+=weight*mass*R
                gap+=weight*mass*sum(min(b**j,R) for j in range(1,l+1))
        assert mean==1 and gap==s+Q(L-s,b**s)
        assert all(sum(w[l] for l in range(j,L+1))==Q(1,b**j) for j in range(1,L+1))
        counts["radix_profiles"]+=1

print(json.dumps({"arithmetic":"exact rational", "status":"passed", "counts":counts},indent=2))
