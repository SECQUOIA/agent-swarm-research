"""Exact checks of ordered approximate bisection and implicit knot merging.

Checks the combinatorial/encoding mechanism, not the quadrature oracle.
"""
from fractions import Fraction as F
from bisect import bisect_right


def inverse(target, oracle, zeta, depth):
    lo,hi=F(0),F(1)
    for _ in range(depth):
        x=(lo+hi)/2
        estimate=oracle(x)
        if target < estimate-zeta:
            hi=x
        elif target > estimate+zeta:
            lo=x
        else:
            return x
    return (lo+hi)/2


oracles=[lambda x:x,
         lambda x:F((13*x.numerator+7*x.denominator)%17,8),
         lambda x:x+F((3*x.numerator+x.denominator)%3-1,512)]
monotonicity_checks=0
for oracle in oracles:
    outputs=[inverse(F(k,256),oracle,F(1,512),10) for k in range(-128,641)]
    for a,b in zip(outputs,outputs[1:]):
        assert a<=b
        monotonicity_checks+=1


def count_right(evaluate, cells, v):
    lo,hi=0,cells
    while lo<hi:
        mid=(lo+hi+1)//2
        if evaluate(mid)<=v:
            lo=mid
        else:
            hi=mid-1
    return lo


def kth_right(arrays, denominator, rank):
    lo,hi=0,denominator
    while lo<hi:
        mid=(lo+hi)//2
        count=sum(count_right(f,n,mid) for f,n in arrays)
        if count>=rank:
            hi=mid
        else:
            lo=mid+1
    return lo


small_checks=containment_checks=0
for denominator in [17,60,128]:
    arrays=[]
    explicit=[]
    for n,power in [(7,2),(4,1),(9,3)]:
        f=lambda k,n=n,power=power: denominator*k**power//n**power
        arrays.append((f,n))
        explicit.append([f(k) for k in range(n+1)])
    merged=sorted(v for a in explicit for v in a[1:])
    for rank,v in enumerate(merged,1):
        assert kth_right(arrays,denominator,rank)==v
        small_checks+=1
    for a,b in zip([0]+merged,merged):
        for values in explicit:
            idx=min(len(values)-2,bisect_right(values,a)-1)
            assert values[idx]<=a<=b<=values[idx+1]
            containment_checks+=1

large_checks=0
H=2**80
arrays=[(lambda k: k*2**40,2**40),
        (lambda k: k*2**45,2**35)]
for rank in [1,2,31,32,33,2**35,2**39,2**40+2**35]:
    v=kth_right(arrays,H,rank)
    count=lambda z: min(2**40,z//2**40)+min(2**35,z//2**45) if z>=0 else 0
    assert count(v)>=rank and count(v-1)<rank
    large_checks+=1

# Exact band extrema suffice because each allowed residual is an interval.
band_checks=0
for lower,upper,band_lower,band_upper in [
    (F(-1,16),F(13,16),F(-13,16),F(1,8)),
    (F(-13,16),F(1,16),F(-1,8),F(13,16)),
    (F(-1,8),F(1,16),F(-13,16),F(1,8))]:
    for j in range(33):
        residual=lower+(upper-lower)*F(j,32)
        assert residual+band_lower<=0<=residual+band_upper
        assert max(abs(residual+band_lower),abs(residual+band_upper))<=F(15,16)
        band_checks+=1
print(f'PASS: {monotonicity_checks} ordered-search checks; '
      f'{small_checks} exact order statistics; {containment_checks} source-cell containments; '
      f'{large_checks} implicit large-grid ranks; {band_checks} directed band checks')
