"""Independent exact checks of the [1,2] monomial mixture proof."""

from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import prod
from random import Random


def integrate(breaks, function):
    points = sorted(set(breaks))
    return sum((b-a)*function((a+b)/2) for a,b in zip(points,points[1:]))


def phi(s):
    k = s.numerator // s.denominator
    return F(2)**k * (1+s-k)


def check(u):
    low = [p for p in u if p <= F(1,2)]
    high = [1-p for p in u if p > F(1,2)]
    normalizer = 2**len(high)
    c = integrate([F(0),F(1),*u],lambda t:F(2)**sum(p>=t for p in u))/normalizer
    o = integrate([F(0),F(1),*u,*(1-p for p in u)],lambda t:prod(
        1+F((t<=p)+(t>=1-p),2) for p in u))/normalizer
    p = prod(1+v for v in u)/normalizer
    v = phi(sum(u))/normalizer
    grid = [F(0),F(1,2),*low,*high]
    def counts(t):return sum(q>=t for q in low),sum(q>=t for q in high)
    cl = 1+integrate(grid,lambda t:F(2)**counts(t)[0]-1)
    ch = 1+integrate(grid,lambda t:F(2)**(-counts(t)[1])-1)
    ol = 1+2*integrate(grid,lambda t:F(3,2)**counts(t)[0]-1)
    oh = 1+2*integrate(grid,lambda t:F(3,4)**counts(t)[1]-1)
    pl,ph = prod(1+q for q in low),prod(1-q/2 for q in high)
    ql,qh = sum(low,F(0)),sum(high,F(0))
    aa,bb = cl-1-ql,qh/2-1+ch
    dil,dih,dol,doh = cl-pl,ch-ph,cl-ol,ch-oh
    ji=(pl-1)*(1-ph)
    jo=2*integrate(grid,lambda t:(F(3,2)**counts(t)[0]-1)*(1-F(3,4)**counts(t)[1]))
    di,do,tt=c-p,c-o,c-v
    assert c==cl+ch-1 and p==pl*ph and v==phi(ql-qh)
    assert di==dil+dih+ji and do==dol+doh+jo
    assert min(aa,bb,dil,dih,dol,doh,ji,jo,tt)>=0
    assert dol>=aa/2
    assert ql<=max(low,default=F(0))+aa
    assert qh<=max(high,default=F(0))+4*bb
    assert jo>=min(max(low,default=F(0)),max(high,default=F(0)))/4
    assert tt<=aa+bb+min(ql,qh)/2
    if qh<=1:
        assert bb<=4*dih
        assert tt<=3*do+12*di
    if qh>=1:
        assert dih>F(1,64)
        assert ji>=ql/3
        assert tt<=64*di+2*do
    assert tt<=64*di+3*do


def main():
    count=0
    for d in range(8):
        for u in combinations_with_replacement([F(i,4) for i in range(5)],d):
            check(u);count+=1
    rng=Random(20260904)
    for _ in range(250):
        u=tuple(F(rng.randrange(101),100) for _ in range(rng.randrange(1,31)))
        check(u);count+=1
    check((F(1,2),F(51,100),F(99,100)))
    count+=1
    print(f'Passed {count} exact monomial formula and inequality checks, including all quarter-grid multisets through degree7.')


if __name__=='__main__':main()
