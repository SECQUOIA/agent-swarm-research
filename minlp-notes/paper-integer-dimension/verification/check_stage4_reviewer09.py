"""Independent finite checks of the positive-power contact obstruction."""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb
import mpmath as mp

A=Q(7,4)
assert A*(Q(2,3)*Q(15,16)-Q(3,67))==Q(2177,2144)>1
assert A*(Q(2,3)*Q(15,16)-Q(25,2048))==Q(8785,8192)>1
pairs=0
for j,k in combinations(range(1,13),2):
    Dj,Dk=128*1024**(j-1),128*1024**(k-1)
    assert 1-Q(64*Dj,Dk)>=Q(15,16)
    pairs+=1
labels=0
for z in combinations(range(-5,6),3):
    for a in permutations(z):
        far=next(((i,j) for i,j in combinations(range(3),2) if abs(a[j]-a[i])>=3),None)
        if far:
            i,j=far; q=abs(a[j]-a[i]); k=(2*q+2)//3; t=Q(k,q)
            assert Q(2,3)<=t<=Q(4,5)
            assert ((1-t)*a[i]+t*a[j]).denominator==1
        else:
            assert z[1]-z[0]==z[2]-z[1]==1
            middle=(min(a)+max(a))/2
            assert middle==z[1]
            assert Q(sum(a),3).denominator==1
        labels+=1
# Exhaustive tiny cap sets, with no graph or formulation assumptions encoded.
cap=[]
for d in (1,2):
    pts=list(product(range(3),repeat=d)); best=0
    bad=[sum(1<<pts.index(v) for v in t) for t in combinations(pts,3)
         if all(sum(v[j] for v in t)%3==0 for j in range(d))]
    for mask in range(1<<len(pts)):
        if all(mask & b != b for b in bad):best=max(best,mask.bit_count())
    cap.append(best)
assert cap==[2,4]
# Generate exact degree-count distributions behind the cap theorem.
dist=[1]
for d in range(31):
    monomials=sum(dist[:2*d//3+1])
    assert monomials*4**d<=7**d*2**(2*d//3)  # t=1/2 indicator bound, rounded threshold
    nxt=[0]*(len(dist)+2)
    for i,v in enumerate(dist):
        for shift in range(3):nxt[i+shift]+=v
    dist=nxt
mp.mp.dps=100
D=[128*1024**j for j in range(8)]
x=[1-mp.mpf(64)/d for d in D]
def power(y,d):return mp.exp(d*mp.log(y))
actual_pairs=actual_triples=0
for j,k in combinations(range(8),2):
    for t in (mp.mpf(2)/3,mp.mpf(3)/4,mp.mpf(4)/5):
        u=(1-t)*x[j]+t*x[k]
        gap=mp.mpf(7)/4*((1-t)*power(x[j],D[j])+t*power(x[k],D[j])-power(u,D[j]))
        assert gap>1
        actual_pairs+=1
for ids in combinations(range(8),3):
    j=ids[0]; u=sum(x[k] for k in ids)/3
    gap=mp.mpf(7)/4*(sum(power(x[k],D[j]) for k in ids)/3-power(u,D[j]))
    assert gap>1
    actual_triples+=1
print(f'PASS: {pairs} rational scale checks; {labels} arbitrary-label orderings; exhaustive cap(1)=2 and cap(2)=4; 31 exact monomial-count bounds; {actual_pairs} high-precision pair gaps and {actual_triples} triple gaps.')
