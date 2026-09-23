"""Exact rational checks for dyadic polynomial root approximation."""
from fractions import Fraction as F


def logceil_inverse(x):
    m=0
    while F(1,2**m)>x:
        m+=1
    return m


def root_interval(x,p,width):
    lo,hi=F(0),F(1)
    while hi-lo>width:
        mid=(lo+hi)/2
        if mid**p<=x:
            lo=mid
        else:
            hi=mid
    return lo,hi


def binomial(alpha,q):
    out=[F(1)]
    for j in range(1,q+1):
        out.append(out[-1]*(alpha-j+1)/j)
    return out


def main():
    count=0
    for B in (1,4,8):
        for A in (F(1),F(2**20),F(1,2**10)):
            epsilon=F(1,2**B)
            eta=epsilon/(16*max(F(1),A))
            m=logceil_inverse(eta)
            P=5; K=P*m; q=m+1
            assert F(1,3**q)/2<=eta/4
            for p in range(1,P+1):
                assert F(1,2**K)<=eta**p
                coeff=binomial(F(1,p),q)
                assert all(abs(c)<=1 for c in coeff)
                for k in sorted({0,1,K//2,K-1}):
                    center=F(3,2**(k+2))
                    low,high=root_interval(center,p,eta/4)
                    sigma=(low+high)/2
                    for u in (F(-1,3),F(-1,6),F(0),F(1,6),F(1,3)):
                        t=center*(1+u)
                        poly=sigma*sum(c*u**j for j,c in enumerate(coeff))
                        lo,hi=root_interval(t,p,eta/64)
                        assert max(abs(poly-lo),abs(poly-hi))<=eta
                        count+=1
    # Exact rational-output obstruction constants for the growing-power note.
    assert (F(3,8)-F(1,2))**2 == F(1,64)
    assert (F(5,8)-F(1,2))**2 == F(1,64)
    print(f'PASS: {count} certified dyadic approximation values; truncation/tail bounds; output-barrier constants')


if __name__ == '__main__':
    main()
