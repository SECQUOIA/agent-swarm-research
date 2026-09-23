"""Exact rational verification of the sparse dyadic counterexample.

See results/positive-multilinear-gap.md. The verification checks the explicit
optimal coupling, its required marginals, its attained objective, and the
pointwise upper certificate. It enumerates failure counts, not all 2^n vertices.
"""
from fractions import Fraction as F


def budget(levels, q):
    return F(levels-q+2,2**q)


def parameters(levels):
    if levels<2:raise ValueError('levels must be at least 2')
    s=next(s for s in range(1,levels) if budget(levels,s+1)<=1<=budget(levels,s))
    theta=(1-budget(levels,s+1))/(budget(levels,s)-budget(levels,s+1))
    gap=F(s)+F(levels-s,2**s)
    return s,theta,gap


def bit_reverse(value, levels):
    return int(f'{value:0{levels}b}'[::-1],2)


def verify(levels):
    m=2**levels
    s,theta,gap=parameters(levels)
    weights=[F(1,2**(ell+1)) for ell in range(levels)]+[F(1,m)]
    assert sum(weights)==1
    assert 0<=theta<=1
    expected_r=F(0); attained=F(0)
    anchor_means=[F(0)]*levels
    for q,mix in [(s,theta),(s+1,1-theta)]:
        for ell,w in enumerate(weights):
            r=0 if ell<q else 2**(ell-q+1)
            mass=mix*w
            failed=[bit_reverse(i,levels) for i in range(r)]
            for j in range(1,levels+1):
                hit=len({v>>(levels-j) for v in failed})
                assert hit==min(2**j,r)
                if j<=ell:
                    attained+=mass*hit
                    anchor_means[j-1]+=mass
            # XOR shifts give each leaf exactly r failures over m equally likely masks.
            if levels<=6:
                for leaf in range(m):
                    assert sum(leaf in {v^mask for v in failed} for mask in range(m))==r
            expected_r+=mass*r
    assert expected_r==1
    assert anchor_means==[F(1,2**j) for j in range(1,levels+1)]
    assert attained==gap
    # The piecewise-linear upper certificate holds for every integer failure count.
    for ell in range(levels+1):
        intercept=0 if ell<=s else 2**(ell-s+1)-2
        for r in range(m+1):
            assert sum(min(2**j,r) for j in range(1,ell+1))<=s*r+intercept
    integrated=F(s)+sum(weights[ell]*(2**(ell-s+1)-2) for ell in range(s+1,levels+1))
    assert integrated==gap
    return s,gap,F(levels)/gap


if __name__=='__main__':
    for levels in range(2,13):
        s,gap,ratio=verify(levels)
        print(f'L={levels} n={2**levels+levels} terms={2**(levels+1)-2} s={s} hull_gap={gap} ratio={ratio} ({float(ratio):.9f})',flush=True)
    print('All exact rational coupling and upper-certificate checks passed.')
