"""Independent exact audit of the cycle resistance LP threshold reduction.

Compares threshold/tie aggregation and recovery with exhaustive vertex search.
No real-algebraic global optimizer is implemented here.
"""
from fractions import Fraction as Q
from itertools import product
from random import Random


def vertex_optimum(f, w, lower, upper):
    n = len(f)
    if not any(f):
        return Q(0)
    values = []
    for free in range(n):
        if f[free] == 0:
            continue
        other = [i for i in range(n) if i != free]
        for bits in product((0, 1), repeat=n-1):
            beta = [Q(0)] * n
            for i, bit in zip(other, bits):
                beta[i] = upper[i] if bit else lower[i]
            beta[free] = -sum(f[i]*beta[i] for i in other)/f[free]
            if lower[free] <= beta[free] <= upper[free]:
                values.append(sum(w[i]*f[i]*beta[i] for i in range(n)))
    return max(values) if values else None


def threshold_optimum(f, w, lower, upper):
    values = []
    tied_sizes = []
    for lam in set(w):
        tied = [i for i in range(len(f)) if w[i] == lam]
        outside = [i for i in range(len(f)) if w[i] != lam]
        beta = [lower[i] for i in range(len(f))]
        for i in outside:
            beta[i] = upper[i] if (w[i]-lam)*f[i] > 0 else lower[i]
        S = sum(f[i]*beta[i] for i in outside)
        lows = {i: min(f[i]*lower[i], f[i]*upper[i]) for i in tied}
        highs = {i: max(f[i]*lower[i], f[i]*upper[i]) for i in tied}
        if S+sum(lows.values()) <= 0 <= S+sum(highs.values()):
            residual = -S-sum(lows.values())
            for i in tied:
                added = min(residual, highs[i]-lows[i])
                y = lows[i]+added
                beta[i] = y/f[i] if f[i] else lower[i]
                residual -= added
            assert residual == 0
            assert all(lower[i] <= beta[i] <= upper[i] for i in range(len(f)))
            assert sum(f[i]*beta[i] for i in range(len(f))) == 0
            value = sum((w[i]-lam)*f[i]*beta[i] for i in outside)
            assert value == sum(w[i]*f[i]*beta[i] for i in range(len(f)))
            assert sum(lower[i] < beta[i] < upper[i] for i in tied) <= 1
            values.append(value)
            tied_sizes.append(len(tied))
    # All feasible threshold branches must attain the same LP optimum.
    assert not values or min(values) == max(values)
    return (max(values) if values else None), max(tied_sizes, default=0)


def interior_optimizer_check():
    # The exact global upper bound is D(q)=-6(q+1)^2-12.
    ell = [Q(0), Q(0), Q(3), Q(0)]
    signs = [Q(-1), Q(-1), Q(1), Q(-1)]
    weights = [Q(2), Q(-1), Q(-3), Q(0)]
    lower = [Q(1)] * 4
    upper = [Q(4), Q(3), Q(4), Q(5)]
    lam = Q(-1)
    multipliers = [(w-lam)*lo for w,lo in zip(weights,lower)]
    coefficients = (sum(a*s for a,s in zip(multipliers,signs)),
                    sum(2*a*s*t for a,s,t in zip(multipliers,signs,ell)),
                    sum(a*s*t*t for a,s,t in zip(multipliers,signs,ell)))
    assert coefficients == (Q(-6), Q(-12), Q(-18))
    q = Q(-1)
    flows = [q+t for t in ell]
    f = [x*abs(x) for x in flows]
    beta = [Q(1), Q(2), Q(1), Q(1)]
    assert sum(a*b for a,b in zip(f,beta)) == 0
    assert sum(w*a*b for w,a,b in zip(weights,f,beta)) == -12
    assert all(lo <= b <= hi for lo,b,hi in zip(lower,beta,upper))
    assert lower[1] < beta[1] < upper[1]
    assert threshold_optimum(f,weights,lower,upper)[0] == -12
    return {'objective': -12, 'q': '-1', 'beta': ['1','2','1','1']}


def run():
    rng = Random(9092026)
    cases = [([Q(0)]*4, [Q(0),Q(1),Q(1),Q(2)], [Q(1)]*4, [Q(3)]*4),
             ([Q(-1),Q(1),Q(0)], [Q(2)]*3, [Q(1)]*3, [Q(4)]*3),
             ([Q(1)]*3, [Q(0),Q(1),Q(2)], [Q(1)]*3, [Q(4)]*3)]
    for _ in range(200):
        n = rng.randrange(3, 8)
        x = [Q(rng.randrange(-5, 6), rng.randrange(1, 5)) for _ in range(n)]
        f = [v*abs(v) for v in x]
        w = [Q(rng.randrange(-2, 3)) for _ in range(n)]
        lower = [Q(rng.randrange(1, 4), 2) for _ in range(n)]
        upper = [v+Q(rng.randrange(0, 8), 2) for v in lower]
        cases.append((f,w,lower,upper))
    counts = {'instances': len(cases), 'feasible': 0, 'infeasible': 0,
              'largest_feasible_tie_group': 0}
    for f,w,lower,upper in cases:
        expected = vertex_optimum(f,w,lower,upper)
        actual, tie_size = threshold_optimum(f,w,lower,upper)
        assert actual == expected
        counts['feasible' if actual is not None else 'infeasible'] += 1
        counts['largest_feasible_tie_group'] = max(counts['largest_feasible_tie_group'], tie_size)
    return counts


if __name__ == '__main__':
    print(run())
    print({'exact_interior_optimizer': interior_optimizer_check()})
