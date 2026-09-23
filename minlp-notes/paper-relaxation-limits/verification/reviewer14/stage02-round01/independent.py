"""Independent finite exact checks; not substitutes for universal proofs."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import prod, comb
from pathlib import Path
import json

report = {}
dyadic = []
for L in range(2, 65):
    B = lambda q: Q(L-q+2, 2**q)
    choices = [s for s in range(1,L) if B(s+1)<=1<=B(s)]
    values = []
    for s in choices:
        w = [Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
        theta = (1-B(s+1))/(B(s)-B(s+1))
        assert 0 <= theta <= 1 and sum(w)==1
        er=eh=Q(0)
        for q, weight in [(s,theta),(s+1,1-theta)]:
            for l in range(L+1):
                r=0 if l<q else 2**(l-q+1)
                h=sum(min(2**j,r) for j in range(1,l+1))
                assert h==s*r+(0 if l<=s else 2**(l-s+1)-2)
                er+=weight*w[l]*r
                eh+=weight*w[l]*h
        assert er==1 and eh==s+Q(L-s,2**s)
        assert all(sum(w[j:])==Q(1,2**j) for j in range(1,L+1))
        values.append(eh)
    assert len(set(values))==1
    dyadic.append((L,choices,str(values[0])))
# Check the geometry at every possible count, not just the mixture profiles.
for L in range(2,9):
    m=2**L
    order=[int(f'{i:0{L}b}'[::-1],2) for i in range(m)]
    for r in range(m+1):
        failed=set(order[:r])
        for j in range(1,L+1):
            assert len({v>>(L-j) for v in failed})==min(2**j,r)
        if L<=5:
            assert all(sum((leaf^shift) in failed for shift in range(m))==r for leaf in range(m))
report['dyadic_profiles_L2_to_64']=dyadic
report['all_count_bit_reversal_L2_to_8']='exact pass; XOR all leaves/shifts through L5'

def orientation_expectation(xs):
    total=Q(0)
    for signs in product((0,1),repeat=len(xs)):
        lo=max([Q(0)]+[1-x for x,s in zip(xs,signs) if s])
        hi=min([Q(1)]+[x for x,s in zip(xs,signs) if not s])
        total+=max(Q(0),hi-lo)
    return total/2**len(xs)

def b_expectation(xs):
    breaks=sorted({Q(0),Q(1)}|{x if x<=Q(1,2) else 2*(1-x) for x in xs})
    total=Q(0)
    for lo,hi in zip(breaks,breaks[1:]):
        mid=(lo+hi)/2
        probabilities=[Q(mid<x) if x<=Q(1,2) else (Q(1,2) if mid<2*(1-x) else Q(1)) for x in xs]
        total+=(hi-lo)*prod(probabilities)
    return total

grid=[Q(i,24) for i in range(25)]
minimum=Q(1)
count=0
for degree in (2,3):
    for xs in combinations_with_replacement(grid,degree):
        u=xs[0]
        gap=u-max(Q(0),sum(xs)-degree+1)
        do=u-orientation_expectation(xs)
        db=u-b_expectation(xs)
        di=u-prod(xs)
        assert min(do,db,di)>=0
        assert 18*do+7*db+6*di>=12*gap
        if gap: minimum=min(minimum,(18*do+7*db+6*di)/(31*gap))
        count+=1
assert all(b_expectation([x])==x and orientation_expectation([x])==x for x in grid)
report['actual_cubic_and_quadratic_laws']={'rational_tuples':count,'minimum_fraction':str(minimum)}
report['finite_sampling_log_upper']=str(Q(25002)-Q(1000**3,23200))
report['finite_sampling_margin']=str(Q(3131,2275)-Q(1,2))
assert Q(25002)-Q(1000**3,23200)<0
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0

equal_cases=0
for n in range(2,21):
    for u in grid[1:-1]:
        b=(n*u).__floor__(); theta=n*u-b
        for d in range(2,n+1):
            q=((1-theta)*comb(b,d)+theta*comb(b+1,d))/comb(n,d)
            gap=min(u,(d-1)*(1-u))
            assert 0<=q<=u**d<u and gap/(u-q)<2
            equal_cases+=1
report['equal_mean_exact_cases']=equal_cases
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='dyadic_profiles_L2_to_64'},indent=2))
