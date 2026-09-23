"""Independent exact checks of the rho+2 coefficient induction.

Orientation moments are integrated directly from conditional Bernoulli products.
No solver, floating arithmetic, or formulas from the spread proof are used to
evaluate the moments.
"""

from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import comb
from random import Random


def choose(n, j):
    return comb(n, j) if 0 <= j <= n else 0


def elementary(values):
    coefficients = [F(1)]
    for value in values:
        coefficients.append(F(0))
        for j in range(len(coefficients)-1, 0, -1):
            coefficients[j] += value*coefficients[j-1]
    return coefficients


def moments(u):
    n=len(u)
    p=elementary(u)
    # Direct integration on all breakpoints, separately for common-threshold
    # and orientation laws.
    points=sorted(set([F(0),F(1),*u,*(1-v for v in u)]))
    c=[F(0)]*(n+1)
    o=[F(0)]*(n+1)
    for left,right in zip(points,points[1:]):
        midpoint=(left+right)/2
        count=sum(midpoint<=v for v in u)
        conditional=elementary([F((midpoint<=v)+(midpoint>=1-v),2) for v in u])
        for j in range(n+1):
            c[j]+=(right-left)*choose(count,j)
            o[j]+=(right-left)*conditional[j]
    total=sum(u,F(0)); k=total.numerator//total.denominator
    theta=total-k
    v=[(1-theta)*choose(k,j)+theta*choose(k+1,j) for j in range(n+1)]
    return c,p,o,v


def coefficients(u):
    c,p,o,v=moments(u)
    n=len(u)
    c,p,o,v=[row+[F(0)] for row in (c,p,o,v)]
    f=[2*c[j]+v[j]-p[j]-2*o[j]+(c[j-1]-p[j-1] if j else 0) for j in range(n+2)]
    assert all(value>=0 for value in f)
    assert f[0]==f[1]==0
    assert f[n+1]==c[n]-p[n]
    if n>=2:
        lower=sum(max(F(0),a+b-1) for a,b in combinations(u,2))
        assert 2*o[2]==c[2]+lower
        assert v[2]>=lower
    return f


def check(u):
    u=tuple(sorted(u))
    f=coefficients(u)
    n=len(u)
    if not n:
        return
    if u[0]==0:
        child=coefficients(u[1:])+[F(0)]
        assert f==child
    elif u[-1]==1:
        child=coefficients(u[:-1])
        assert f==[value+(child[j-1] if j else 0) for j,value in enumerate(child+[F(0)])]
    elif n>=3:
        amount=min(u[0],1-u[-1])
        spread=(u[0]-amount,*u[1:-1],u[-1]+amount)
        after=coefficients(spread)
        assert all(after[j]<=f[j] for j in range(3,n+1))


def main():
    count=0
    for n in range(9):
        for u in combinations_with_replacement([F(i,4) for i in range(5)],n):
            check(u);count+=1
    rng=Random(20260904)
    for _ in range(300):
        n=rng.randrange(2,16)
        u=tuple(F(rng.randrange(101),100) for _ in range(n))
        check(u);count+=1
    # A spread line can lie entirely on an orientation break hyperplane.
    for u in ((F(1,5),F(1,2),F(4,5)), (F(1,2),)*6):
        check(u);count+=1
    before=coefficients((F(2,5),F(7,10),F(24,25),F(97,100)))[3]
    after=coefficients((F(2,5),F(7,10),F(959,1000),F(971,1000)))[3]
    assert before==F(6201,12500) and after==F(4961031,10000000)
    assert after-before==F(231,10000000)
    print(f'Passed {count} exact coefficient/induction cases and the non-Schur-concavity example.')


if __name__=='__main__':
    main()
