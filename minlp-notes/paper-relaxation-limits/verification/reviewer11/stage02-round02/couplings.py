"""Integrate the actual O,I,B laws exactly, independently of their case formulas."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import prod

def expectations(x):
    k=len(x)
    orient=Q(0)
    for sides in product([0,1],repeat=k):
        lo=max([Q(0)]+[1-u for u,right in zip(x,sides) if right])
        hi=min([Q(1)]+[u for u,right in zip(x,sides) if not right])
        orient+=max(Q(0),hi-lo)/2**k
    cuts=sorted({Q(0),Q(1)}|{u if u<=Q(1,2) else 2*(1-u) for u in x})
    B=Q(0)
    for lo,hi in zip(cuts,cuts[1:]):
        t=(lo+hi)/2
        probabilities=[int(t<u) if u<=Q(1,2) else Q(1,2) if t<2*(1-u) else Q(1) for u in x]
        B+=(hi-lo)*prod(probabilities)
    return orient,prod(x),B

for i in range(21):
    u=Q(i,20)
    assert expectations((u,))==(u,u,u)
count=0
for k in [2,3]:
    for x in combinations_with_replacement([Q(i,20) for i in range(21)], k):
        es=expectations(x)
        ds=[min(x)-p for p in es]
        T=min(x)-max(Q(0),sum(x)-k+1)
        assert all(d>=0 for d in ds)
        assert 18*ds[0]+6*ds[1]+7*ds[2]>=12*T
        count+=1
for den in [10,100,1000]:
    e=Q(1,den)
    for x in [(e,1-e*e,1-e*e),(Q(1,2)+e,Q(3,4)-e/2,Q(3,4)-e/2)]:
        ds=[min(x)-p for p in expectations(x)]
        T=min(x)-max(Q(0),sum(x)-2)
        assert 18*ds[0]+6*ds[1]+7*ds[2]>=12*T
print(f'PASS: {count} quadratic/cubic tuples, six limiting tuples, 21 singleton marginals, all exact rational integration.')
