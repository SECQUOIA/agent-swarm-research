"""Pure-Python exact certificates for the positive cubic gap examples.

No numerical optimization is used. Each dual certificate is verified at every
possible group-count state, which covers every binary vertex by symmetry.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, lcm


def phi(a,b,c,coefficients):
    terms=[comb(c,3),b*comb(c,2),comb(b,2),a*c,a*b,comb(a,2)]
    return sum(v*w for v,w in zip(terms,coefficients))


EXAMPLES=[
    dict(m=8,coefs=[2,3,13,12,8,7],dual=[F(793,7),F(110),F(114),F(-5882,7)],
         support=[((1,2,8),F(2,7)),((1,5,6),F(4,7)),((8,4,2),F(1,7))],ratio=F(6601,3225)),
    dict(m=6,coefs=[2,3,9,10,7,7],dual=[F(74),F(778,13),F(842,13),F(-4816,13)],
         support=[((1,4,4),F(17,26)),((2,1,6),F(4,13)),((6,2,1),F(1,26))],ratio=F(20891,10411)),
    dict(m=64,coefs=[2,3,120,105,70,63],dual=[F(8302),F(900446,105),F(299682,35),F(-51743768,105)],
         support=[((4,19,64),F(241,735)),((5,19,64),F(4,245)),((16,40,43),F(419,735)),((64,31,17),F(3,35))],ratio=F(7443345,3445256)),
]


def verify(example):
    m=example['m'];coefs=example['coefs'];dual=example['dual'];support=example['support']
    denominator=lcm(*[v.denominator for v in dual])
    integer_dual=[int(v*denominator) for v in dual]
    minima=[]
    for c in range(m+1):
        slacks=[denominator*phi(a,b,c,coefs)-sum(v*w for v,w in zip([a,b,c,1],integer_dual)) for a,b in product(range(m+1),repeat=2)]
        assert min(slacks)>=0
        minima.append(F(min(slacks),denominator))
    assert sum(p for _,p in support)==1
    assert all(p>=0 for _,p in support)
    means=[sum(p*state[j] for state,p in support) for j in range(3)]
    assert means==[F(m,4),F(m,2),F(3*m,4)]
    primal=sum(p*phi(*state,coefs) for state,p in support)
    dual_value=sum(v*w for v,w in zip([*means,1],dual))
    assert primal==dual_value
    orbit_sizes=[comb(m,3),m*comb(m,2),comb(m,2),m*m,m*m,comb(m,2)]
    upper=[F(3,4),F(1,2),F(1,2),F(1,4),F(1,4),F(1,4)]
    lower=[F(1,4),0,0,0,0,0]
    cav=sum(a*s*u for a,s,u in zip(coefs,orbit_sizes,upper))
    tbtl=sum(a*s*l for a,s,l in zip(coefs,orbit_sizes,lower))
    gap=cav-primal;ratio=(cav-tbtl)/gap
    assert ratio==example['ratio'] and ratio>2
    print(f'n={3*m}, monomials={sum(orbit_sizes)}, cav={cav}, tbt_lower={tbtl}, vex={primal}, hull_gap={gap}, ratio={ratio}')
    print('Minimum dual slacks by high-group count:',minima)


if __name__=='__main__':
    for example in EXAMPLES:verify(example)
    print('All exact vertex-count and matching primal certificates passed.')
