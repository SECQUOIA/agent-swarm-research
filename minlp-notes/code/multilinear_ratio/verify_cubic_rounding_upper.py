"""Exact finite-grid replay of the actual three rounding distributions.

The continuous proof is in results/positive-cubic-rounding-upper-bound.md.
This check integrates each distribution from its definition; it is a sanity
check, not a replacement for the proof over all real marginals.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import prod


def orientation_mean(xs):
    result=Q(0)
    for choices in product([0,1],repeat=len(xs)):
        intervals=[(Q(0),x) if left else (1-x,Q(1)) for x,left in zip(xs,choices)]
        result += max(Q(0),min(b for a,b in intervals)-max(a for a,b in intervals))
    return result/2**len(xs)


def threshold_mean(xs):
    lows=[x for x in xs if x<=Q(1,2)]
    failures=[1-x for x in xs if x>Q(1,2)]
    cutoff=min(lows,default=Q(1))
    breaks=sorted({Q(0),cutoff,*[2*p for p in failures if 2*p<cutoff]})
    return sum((hi-lo)*prod(Q(1,2) if (lo+hi)/2<2*p else Q(1) for p in failures) for lo,hi in zip(breaks,breaks[1:]))


def run():
    checked=0
    for degree in [2,3]:
        for xs in combinations_with_replacement([Q(i,12) for i in range(13)],degree):
            upper=min(xs);lower=max(Q(0),sum(xs)-degree+1);gap=upper-lower
            means=(orientation_mean(xs),prod(xs),threshold_mean(xs))
            assert all(lower<=mean<=upper for mean in means),(xs,means)
            deficiency=upper-(18*means[0]+6*means[1]+7*means[2])/31
            assert deficiency>=Q(12,31)*gap,(xs,deficiency,gap)
            checked+=1
    assert Q(3,31)*Q(1,2)+(Q(4,31)+Q(24,31))*Q(3,8)==Q(12,31)
    assert -Q(3,31)/2+Q(4,31)*Q(3,8)==0
    assert -Q(4,31)*Q(3,8)+Q(24,31)/16==0
    print('PASS:',checked,'exact bilinear/cubic marginal tuples, including cube and classification boundaries.')
    print('PASS: actual orientation and threshold distributions integrated with rational arithmetic.')
    print('PASS: optimal-mixture dual averaging identity, alpha=12/31.')

if __name__=='__main__':run()
