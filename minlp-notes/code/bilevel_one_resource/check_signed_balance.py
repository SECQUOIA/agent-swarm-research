"""Exact independent checks of the signed scalar-resource mechanism.

Uses rational linear marginals, so balancing and all errors are exact.
Includes negative/zero weights, saturation, endpoint balances, and tiny weights.
This tests the new balance transfer, not the already reviewed inverse lemma.
"""
from fractions import Fraction as F
from random import Random

rng = Random(270905)
def clip(q):
    return max(F(0), min(F(1), q))

def response(ell, slope, weights, multiplier):
    return [clip((e - multiplier*w)/a) for e,a,w in zip(ell,slope,weights)]

def residual(q, weights):
    return sum((w*z for w,z in zip(weights,q)), F(0))

def balance(ell, slope, weights, target):
    cuts = sorted({t for e,a,w in zip(ell,slope,weights) if w
                   for t in (e/w, (e-a)/w)})
    for t in cuts:
        q = response(ell,slope,weights,t)
        if residual(q,weights) == target:
            return t,q
    for lo,hi in zip(cuts,cuts[1:]):
        qlo = response(ell,slope,weights,lo)
        qhi = response(ell,slope,weights,hi)
        rlo,rhi = residual(qlo,weights),residual(qhi,weights)
        if rhi < target < rlo:
            t = lo+(hi-lo)*(rlo-target)/(rlo-rhi)
            q = response(ell,slope,weights,t)
            assert residual(q,weights) == target
            return t,q
    raise AssertionError('feasible balance missing')

checks = 0
for case in range(160):
    n = 2 + case % 5
    weights = [F(rng.randrange(-3,4), rng.choice([1,2,1<<20])) for _ in range(n)]
    if not any(weights):
        weights[0] = F(1)
    slopes = [F(rng.randrange(1,8),rng.randrange(1,5)) for _ in range(n)]
    intercept = [F(rng.randrange(-4,5),3) for _ in range(n)]
    direction = [F(rng.randrange(-4,5),2) for _ in range(n)]
    costs = [F(rng.randrange(-9,10),2) for _ in range(n)]
    low = sum((min(w,0) for w in weights),F(0))
    high = sum((max(w,0) for w in weights),F(0))
    W = high-low
    wmin = min(abs(w) for w in weights if w)
    cmax = max(map(abs,costs))
    # Global threshold bounds must work for every leader, not just this x.
    cuts = [v/w for e,d,a,w in zip(intercept,direction,slopes,weights) if w
            for v in (min(e,e+d),max(e,e+d),min(e,e+d)-a,max(e,e+d)-a)]
    L,U = min(cuts),max(cuts)
    assert L < U
    for x in [F(0),F(1,7),F(1)]:
        ell = [e+d*x for e,d in zip(intercept,direction)]
        assert residual(response(ell,slopes,weights,L),weights) == high
        assert residual(response(ell,slopes,weights,U),weights) == low
        for t in [F(0),F(2,5),F(1)]:
            target = low+t*W
            star,qstar = balance(ell,slopes,weights,target)
            for multiplier in [L,U,star,(L+star)/2,(star+U)/2]:
                q = response(ell,slopes,weights,multiplier)
                r = abs(residual(q,weights)-target)
                weighted_distance = sum((abs(w)*abs(z-zs) for w,z,zs in zip(weights,q,qstar)),F(0))
                assert weighted_distance == r
                error = abs(sum((c*(z-zs) for c,z,zs in zip(costs,q,qstar)),F(0)))
                assert error <= cmax*r/wmin
                for w,z,zs in zip(weights,q,qstar):
                    if not w:
                        assert z == zs
                checks += 1
print(f'PASS: {checks} exact signed-balance/error certificates across 160 instances')
