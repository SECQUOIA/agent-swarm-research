"""Independent whole-paper checks: implicit overlay and separable packing.
Exact finite checks support, and do not replace, the analytic review.
"""
from bisect import bisect_right
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from math import comb
from random import Random

counts = {}
def merged_kth(arrays, H, k):
    if k == 0:
        return 0
    lo, hi = 0, H
    while lo < hi:
        v = (lo+hi)//2
        rank = sum(bisect_right(a[1:], v) for a in arrays)
        if rank >= k:
            hi = v
        else:
            lo = v+1
    return lo
H=4
arrays = [[0,*v,H] for k in range(4) for v in combinations_with_replacement(range(H+1),k)]
ranks=cells=0
for aa,bb in product(arrays,repeat=2):
    source=[aa,bb]
    truth=[0]+sorted(aa[1:]+bb[1:])
    got=[merged_kth(source,H,k) for k in range(len(truth))]
    assert got==truth
    ranks+=len(truth)
    for left,right in zip(got,got[1:]):
        for a in source:
            if left < right:
                j=bisect_right(a,left)-1
                assert j+1<len(a) and a[j]<=left<right<=a[j+1]
            else:
                assert any(a[j]<=left<=a[j+1] for j in range(len(a)-1))
            cells+=1
counts['merged_rank_queries']=ranks
counts['source_cell_containments']=cells
# Two arrays with 2^50 and 2^49 cells, queried without enumeration.
H=2**50
def rank_huge(v):
    return v+v//2
for k in [1,2,3,H//2,H,H+H//2-1,H+H//2]:
    lo,hi=0,H
    while lo<hi:
        mid=(lo+hi)//2
        if rank_huge(mid)>=k: hi=mid
        else: lo=mid+1
    assert rank_huge(lo)>=k and (lo==0 or rank_huge(lo-1)<k)
counts['huge_array_queries']=7
# Shared deterministic tree must remain monotone even for nonmonotone node values.
rng=Random(1201)
def evaluate(values,target,depth=5):
    lo,hi,node=F(0),F(1),1
    for _ in range(depth):
        midpoint=(lo+hi)/2
        estimate=values[node]
        if estimate-F(1,16)>target:
            hi=midpoint; node=2*node
        elif estimate+F(1,16)<target:
            lo=midpoint; node=2*node+1
        else:
            return midpoint
    return (lo+hi)/2
for _ in range(1000):
    values={j:F(rng.randrange(-8,25),16) for j in range(1,32)}
    outputs=[F(0)]+[evaluate(values,F(k,64)) for k in range(1,64)]+[F(1)]
    assert outputs==sorted(outputs)
counts['nonmonotone_estimate_trees']=1000
# Integer l1 ball: choose nonzero coordinates, signs, positive absolute values.
for n in range(1,9):
    for q in range(1,51):
        radius=q*n
        cardinality=sum(2**k*comb(n,k)*comb(radius,k) for k in range(min(n,radius)+1))
        assert cardinality < (3*(2*q+1))**n
counts['packing_ball_constants']=400
# Signed-band extrema and exact containment intervals, including brackets.
for kind,(emin,emax,lower,upper) in {
 'convex':(-F(1,16),F(13,16),-F(13,16),F(1,8)),
 'concave':(-F(13,16),F(1,16),-F(1,8),F(13,16)),
 'bracket':(-F(1,8),F(1,16),-F(13,16),F(1,8)),
}.items():
    for k in range(65):
        error=emin+(emax-emin)*F(k,64)
        assert error+lower<=0<=error+upper
        assert max(abs(error+lower),abs(error+upper))<=F(15,16)
counts['signed_band_checks']=195
# All six separable count factors, across n and rank, without floating logs.
for n in range(1,9):
    for r in range(1,33):
        cases=[(r,12,7,1),(2*r,5832,17,1),
               (2*r,12,8,1),(4*r,5832,18,1),
               (2*r*r,12,8,2),(36*r*r,5832,21,2)]
        for q,capacity,constant,power in cases:
            assert (capacity*3*(2*q+1))**n < (2**constant*r**power)**n
counts['separable_count_checks']=8*32*6
print(counts)
